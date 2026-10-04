# Data and Evaluation Guide

## Course corpus

The local corpus is built from nine text-based PE6201 course PDFs. The names, extracted page counts, and indexed-passage counts below describe the current local index (`data/index.json`); one PDF page can produce more than one passage.

| Source PDF | Pages | Indexed passages |
|---|---:|---:|
| Week 1 Exercise.pdf | 20 | 20 |
| Week 2 Exercise.pdf | 10 | 10 |
| Week 2 notes.pdf | 24 | 24 |
| Week 3 Exercise.pdf | 12 | 12 |
| Week 3 notes.pdf | 19 | 22 |
| Week 4 Exercise.pdf | 30 | 31 |
| Week 4 Notes.pdf | 21 | 21 |
| Week 5 notes.pdf | 46 | 48 |
| Week_1_notes_v2.pdf | 33 | 33 |
| **Total** | **215** | **221** |

The nine original PDFs are included under `data/uploads/` in this course submission, alongside the manifest and `evaluation/qa_gold.csv`, so the evaluator can reproduce the corpus. Uploads and the generated index are needed for a fresh local run. Keep access to course materials within the intended review audience unless course rules authorize broader distribution.

## Labeled question set

`qa_gold.csv` is the fixed question set used for development and held-out evaluation. It has 68 questions across the indexed files:

- Development: 46 questions (40 answerable, 6 unanswerable).
- Test: 22 questions (16 answerable, 6 unanswerable).

Columns record a stable ID, split, question, answerability label, concise reference answer, expected source filename, expected evidence page(s), and a short evidence note. The test split is kept out of threshold selection. The questions were authored specifically for this project and are not a third-party benchmark; that creates a risk of narrow wording and should be addressed with independently authored or independently generated questions in future work.

## Reproduce the local evaluation

From the project root, after uploading the nine authorized PDFs in the app:

```powershell
.\.venv\Scripts\python.exe evaluation\run_eval.py
```

The script selects the query-term abstention threshold using development answerability F1, saves it to the ignored local file `data/answer_threshold.json`, and then reports development and test results. It does not call an external model.

Metrics:

- **Raw answerability precision:** among questions with any keyword retrieval hit, the fraction labeled answerable.
- **Abstention-gated precision/recall:** whether the local selector returns any answer sentence, compared with the answerability label. These measure the abstention decision, not the factual correctness of the returned text.
- **Evidence page Hit@4:** whether a retrieved top-four passage matches both the gold source file and at least one gold evidence page.
- **Reference token F1:** token overlap between selected local answer text and the reference answer. This is a lexical proxy, not semantic grading.

Latest local snapshot: development abstention precision 0.91 and recall 1.00; test abstention precision 0.88 and recall 0.94; evidence page Hit@4 was 0.88 on development and 1.00 on test. Macro-average Hit@4 across source/split groups was 0.91. These are small-sample results, not a guarantee of general performance.

## Optional OpenRouter comparison

The model comparison sends the 22 held-out questions and up to four retrieved excerpts per question only with explicit authorization:

```powershell
$env:OPENROUTER_API_KEY = "your-api-key"
.\.venv\Scripts\python.exe evaluation\run_model_eval.py --send-to-openrouter
```

The script shares the app's spend ledger and US$4.50 stop, uses `store=False`, records outputs in `model_results.csv`, and reports binary answerability accuracy, exact expected-page citation hit, and lexical token F1. **Answerability accuracy is not factual answer accuracy.** The latest model snapshot shows 22/22 binary answerability decisions correct, 15/16 exact gold-page citations, and mean token F1 0.548 versus 0.224 for the local baseline. It uses the revised prompt and citation validation. Q020 still had a low token F1 (0.163) because its response substituted governance for the reference's maintenance-budget point. Any new API run overwrites `model_results.csv`.

## Evaluation limitations and next validation

The held-out split has only 22 cases, including six unanswerable questions. One case changes a headline rate by about 4.5 percentage points; among the 16 answerable questions, one case changes a rate by 6.25 points. Gold evidence currently names expected pages, but another page can also validly support an answer (for example, the appointment request types appear in both an exercise and lecture notes). Future annotation should permit multiple acceptable evidence pages and add a human-checked support label per answer/citation. Expand the test set with independent paraphrases, cross-file ambiguity, misleading keyword overlap, missing evidence, and exercise-versus-notes disagreements.
