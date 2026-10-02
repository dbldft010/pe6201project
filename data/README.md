# Data Directory

## Course source PDFs

The nine course PDFs used to build the current index are stored locally in `data/uploads/`. They are excluded from version control because course-material redistribution permission has not been confirmed. The checked-in `SOURCE_MANIFEST.csv` records each filename, page count, and indexed-passage count without reproducing the PDF content.

For a fresh installation, obtain authorized copies of the listed PDFs from the course and upload them through the app. The app creates `index.json` and `summaries.json` locally. Those generated files are ignored by Git and should be regenerated from the PDFs instead of checked in.

## Evaluation data

The fixed, labeled question set is `evaluation/qa_gold.csv`. Evaluation scripts and the latest baseline/model result snapshots are in `evaluation/`; see [the evaluation guide](../evaluation/README.md) for labels, split sizes, metrics, commands, and limitations.

## Local-only state

`api_usage.json` records the local OpenRouter request and spend ledger, and `answer_threshold.json` records the threshold selected by the local evaluation script. Both are ignored by Git. Never add an API key, `.env` file, or private course content to a public repository.
