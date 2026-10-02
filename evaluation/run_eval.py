"""Run a small labeled retrieval baseline evaluation against the local PDF index."""

import csv
import json
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from app import answer_from_evidence, load_index, retrieve, tokenize  # noqa: E402


GOLD_PATH = Path(__file__).with_name("qa_gold.csv")


def main() -> None:
    with GOLD_PATH.open(encoding="utf-8-sig", newline="") as file:
        cases = list(csv.DictReader(file))
    chunks = load_index()
    if not chunks:
        raise SystemExit("No indexed PDF content found. Upload the lecture PDF in the app first.")

    prepared = []
    for case in cases:
        hits = retrieve(case["question"], chunks, limit=4)
        gold_answerable = case["answerable"] == "yes"
        prepared.append((case, hits, gold_answerable))

    # Select the answerability threshold using development data only.
    threshold_scores = []
    for threshold in (0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80):
        dev = [(case, hits, gold) for case, hits, gold in prepared if case["split"] == "development"]
        tp = sum(gold and bool(answer_from_evidence(case["question"], hits, min_coverage=threshold)) for case, hits, gold in dev)
        fn = sum(gold and not bool(answer_from_evidence(case["question"], hits, min_coverage=threshold)) for case, hits, gold in dev)
        tn = sum(not gold and not bool(answer_from_evidence(case["question"], hits, min_coverage=threshold)) for case, hits, gold in dev)
        fp = sum(not gold and bool(answer_from_evidence(case["question"], hits, min_coverage=threshold)) for case, hits, gold in dev)
        f1 = (2 * tp) / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0
        threshold_scores.append((f1, threshold))
    best_score = max(score for score, _ in threshold_scores)
    selected_threshold = max(threshold for score, threshold in threshold_scores if score == best_score)
    config_path = PROJECT_DIR / "data" / "answer_threshold.json"
    config_path.write_text(json.dumps({"min_coverage": selected_threshold}, indent=2), encoding="utf-8")

    totals = {split: {"n": 0, "retrieval_hits": 0, "answerable": 0, "raw_keyword_matches": 0, "predicted_answerable": 0,
                      "true_positive": 0, "false_positive": 0, "false_negative": 0}
              for split in {case["split"] for case in cases}}
    details = []
    per_source = {}
    for case, hits, gold_answerable in prepared:
        answer = answer_from_evidence(case["question"], hits, min_coverage=selected_threshold)
        raw_keyword_match = bool(hits)
        predicted_answerable = bool(answer)
        target_pages = {int(value) for value in case["evidence_pages"].split("-") if value.strip()} if case["evidence_pages"] else set()
        retrieval_hit = any(
            hit["source"] == case["source_file"] and hit["page"] in target_pages
            for hit in hits
        ) if target_pages else False
        reference_tokens = set(tokenize(case["reference_answer"])) if case["reference_answer"] else set()
        answer_tokens = set(tokenize(" ".join(answer)))
        overlap = len(reference_tokens & answer_tokens)
        token_precision = overlap / len(answer_tokens) if answer_tokens else 0.0
        token_recall = overlap / len(reference_tokens) if reference_tokens else 0.0
        token_f1 = (2 * token_precision * token_recall / (token_precision + token_recall)
                    if token_precision + token_recall else 0.0)
        row = totals[case["split"]]
        row["n"] += 1
        row["answerable"] += int(gold_answerable)
        row["raw_keyword_matches"] += int(raw_keyword_match)
        row["predicted_answerable"] += int(predicted_answerable)
        row["retrieval_hits"] += int(retrieval_hit)
        row["true_positive"] += int(gold_answerable and predicted_answerable)
        row["false_positive"] += int(not gold_answerable and predicted_answerable)
        row["false_negative"] += int(gold_answerable and not predicted_answerable)
        if gold_answerable:
            source_key = (case["split"], case["source_file"])
            source_row = per_source.setdefault(source_key, {"n": 0, "retrieval_hits": 0, "token_f1_sum": 0.0})
            source_row["n"] += 1
            source_row["retrieval_hits"] += int(retrieval_hit)
            source_row["token_f1_sum"] += token_f1
        details.append({**case, "predicted_answerable": predicted_answerable,
                        "raw_keyword_match": raw_keyword_match,
                        "retrieval_hit_at_4": retrieval_hit,
                        "top_pages": ";".join(str(hit["page"]) for hit in hits),
                        "answer_sentence_count": len(answer),
                        "reference_token_f1": round(token_f1, 4) if gold_answerable else ""})

    report_path = Path(__file__).with_name("baseline_results.csv")
    with report_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(details[0].keys()))
        writer.writeheader()
        writer.writerows(details)

    print(f"Corpus passages: {len(chunks)}")
    print(f"Cases: {len(cases)} (development={sum(c['split']=='development' for c in cases)}, test={sum(c['split']=='test' for c in cases)})")
    print(f"Abstention query-term coverage threshold selected on development set: {selected_threshold:.2f} (answerability F1={best_score:.2f})")
    for split, row in totals.items():
        precision = row["true_positive"] / (row["true_positive"] + row["false_positive"]) if row["true_positive"] + row["false_positive"] else 0
        recall = row["true_positive"] / (row["true_positive"] + row["false_negative"]) if row["true_positive"] + row["false_negative"] else 0
        raw_tp = sum(1 for case, hits, gold in prepared if case["split"] == split and gold and bool(hits))
        raw_fp = row["raw_keyword_matches"] - raw_tp
        raw_precision = raw_tp / (raw_tp + raw_fp) if raw_tp + raw_fp else 0
        hit_rate = row["retrieval_hits"] / row["answerable"] if row["answerable"] else 0
        print(f"{split}: n={row['n']}, raw keyword answerability precision={raw_precision:.2f}, abstention-gated precision={precision:.2f}, recall={recall:.2f}, retrieval page hit@4={hit_rate:.2f}")
    print("Per-course-file answerable-question results:")
    for (split, source), row in sorted(per_source.items()):
        hit_rate = row["retrieval_hits"] / row["n"] if row["n"] else 0
        mean_token_f1 = row["token_f1_sum"] / row["n"] if row["n"] else 0
        print(f"  {split} | {source}: n={row['n']}, page hit@4={hit_rate:.2f}, reference token F1={mean_token_f1:.2f}")
    source_hit_rates = [row["retrieval_hits"] / row["n"] for row in per_source.values() if row["n"]]
    if source_hit_rates:
        print(f"Macro-average page hit@4 across file/split groups: {sum(source_hit_rates) / len(source_hit_rates):.2f}")
    print(f"Per-question evaluation results: {report_path}")


if __name__ == "__main__":
    main()
