# PE6201 Course Materials Q&A Assistant

A course-specific learning assistant. Upload text-based lecture PDFs to create a searchable index and per-file summaries. Ask questions across the course and inspect the cited source pages, or generate short-answer revision prompts from indexed content and review the source evidence after submitting.

For the submission package, see [Product Documentation](docs/PRODUCT_DOCUMENTATION.md), [Data and Evaluation Guide](evaluation/README.md), [Final Project Report](docs/FINAL_REPORT.md), and [Demo Script](docs/DEMO_SCRIPT.md). The source-material manifest and evaluation results should be included in the repository. Original course PDFs are excluded from version control; include them only if course distribution rules permit.

## Run

In Windows PowerShell:

```powershell
cd 'F:\课程\pe6201作业\course_qa_assistant'
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\run.ps1
```

Open http://127.0.0.1:5000 and upload your course PDFs.

If the `python` command is unavailable, replace it with the full path to an installed Python executable:

```powershell
& 'C:\path\to\python.exe' -m venv .venv
```

## Data and privacy

- Uploaded PDFs and extracted indexes are stored in `data/uploads/`, `data/index.json`, and `data/summaries.json`.
- The app removes byte-identical PDF copies on startup and when files are uploaded, keeping one stored copy per PDF. The page shows unique uploaded PDFs, indexed PDFs, searchable passages, and whether each file produced searchable text; counts refresh after upload completes.
- The app is local-only unless a user checks the consent box for that question or quiz. `.gitignore` excludes uploaded documents, generated indexes, logs, environment files, and the virtual environment.
- Check course-material licensing and sharing restrictions before publishing the repository.
- Text-based PDFs are supported. Scanned PDFs require OCR; tables, diagrams, and formulas may need manual review.

## Method and limitations

The app ranks passages locally with keyword-based retrieval and creates deterministic extractive summaries. By default it answers with selected source sentences. If the user checks the explicit consent box, it sends only the question and up to four retrieved excerpts through OpenRouter for a synthesized answer with source IDs. Original PDF files stay local. The request sets `store=False`; this is not a claim of zero data retention. OpenRouter routes requests to model providers, whose retention practices vary; see [OpenRouter's privacy policy](https://openrouter.ai/privacy/) and [provider information](https://openrouter.ai/providers). The model is instructed to treat source excerpts as untrusted reference material, answer only from them, and abstain when they do not support an answer. Citations still need to be checked against the displayed excerpts.

The revision quiz samples evidence from across indexed pages and creates questions about named concepts, definitions, causes, conditions, lists, comparisons, numbers, and process steps. Every item shows its course week and material type, question direction, operational scenario, and the specific knowledge point being tested. Local mode builds this context from the source file and matching course topic without API calls. If the user checks the separate quiz consent box, the app sends up to five selected excerpts with the same context to the configured model, which is instructed to ask one concrete, verifiable question per excerpt and avoid broad “main idea” prompts. After submission, a lightweight keyword-overlap check gives a self-check signal and reveals the reference answer, source sentence, and page. This is not semantic grading: students should judge paraphrases against the displayed evidence. Quiz items are held in the local Flask session and are not stored as a score history.

This is a small RAG prototype, not a guarantee against hallucinations. A failed search does not prove the materials contain no answer. Evaluate it against the non-generative baseline using the labeled questions before making performance claims.

## Configure the external model

Install dependencies with the normal setup command, then set your OpenRouter API key in the same PowerShell session before starting the app. Never put the key in source code or a committed file:

```powershell
$env:OPENROUTER_API_KEY = "your-api-key"
.\run.ps1
```

The previous setup name `OPENAI_API_KEY` is also accepted for compatibility, but `OPENROUTER_API_KEY` is recommended.

The app uses OpenRouter's OpenAI-compatible endpoint (`https://openrouter.ai/api/v1`) with model ID `openai/gpt-6-luna`. The OpenAI Python SDK and Responses API are pointed at OpenRouter's endpoint. The API is called only when the user checks the relevant on-page consent box. If the key is absent, no request is made and the local answer or quiz is used. A failed network request may already have reached the provider.

## Budget

The full project budget is capped at **US$5**: local Python, Flask, PDF parsing, and local execution add no metered service cost; the app stops making new model requests once its tracked API spend plus a per-request reserve reaches **US$4.50**, leaving US$0.50 unallocated. Each request reserves $0.001 before it is sent; successful responses replace that reserve with the actual token cost, while failed requests retain the reserve conservatively. The ledger is stored in the ignored local file `data/api_usage.json`. The app limits questions to 500 characters, sends at most four 1,100-character excerpts, disables SDK retries, and caps answers at 250 output tokens and quizzes at 500 output tokens. OpenRouter currently lists GPT-6 Luna at $0.10 per million input tokens and $0.50 per million output tokens, making an allowance of 6,000 input and 250 output tokens about $0.000725 per request; 32 calls at that allowance would cost about $0.024. Check the current [OpenRouter model pricing](https://openrouter.ai/openai/gpt-6-luna/). The local cap covers calls made by this app only, not other uses of the same account or key.

## Evaluation pilot

The labeled set `evaluation/qa_gold.csv` now contains 68 questions (46 development, 22 held-out test), including answerable and unanswerable questions across all nine indexed PDFs. The abstention threshold is selected using development answerability F1 only, saved locally in `data/answer_threshold.json`, then applied unchanged to the app and held-out set. Run the local baseline with:

```powershell
.\.venv\Scripts\python.exe evaluation\run_eval.py
```

The script reports raw keyword answerability precision, abstention-gated answerability precision/recall, evidence-page Hit@4, and lexical reference-answer token F1. It also breaks results out by course file and split. Token F1 is only a lexical proxy, not semantic grading. The old 32-question single-file result is retained as `evaluation/baseline_results_pilot_32.csv`; rerun the expanded set before reporting current metrics.

An optional held-out OpenRouter RAG comparison is available. It sends the 22 held-out questions and retrieved passages only when explicitly invoked with `--send-to-openrouter`; each request uses the same API budget ledger and $4.50 stop as the web app:

```powershell
$env:OPENROUTER_API_KEY = "your-api-key"
.\.venv\Scripts\python.exe evaluation\run_model_eval.py --send-to-openrouter
```

It writes per-question answers, cited pages, answerability, and lexical reference token F1 to `evaluation/model_results.csv`. The model comparison is opt-in, costs depend on actual token use, and it should only be run when sharing course excerpts with OpenRouter is permitted. The question set is a small pilot rather than evidence of general performance; confirm course-material permissions before sharing the dataset or repository publicly.
