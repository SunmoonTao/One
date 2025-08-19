# One
Personal Utils, could be useful for you as well.
## Plan: Website;App; or CLI app.

## Daily Fact Card (HTML5 + Python)

This repository now contains a minimal Flask app that serves a daily "fact card" from a predefined list of terms (see `data/terms.json`).

Quick start (create a virtualenv, install, run):

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

To edit terms, update `data/terms.json`. Each item is an object with `id`, `name`, `description`, `fact`, and optional `source`.
