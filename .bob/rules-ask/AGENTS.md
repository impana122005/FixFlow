# Ask Mode Rules

This file provides guidance to agents when working with code in this repository.

## Documentation Context (Non-Obvious)

- **FixFlow is fully implemented** (not a skeleton) — `analyzer/`, `reports/`, and `app.py` are all working code. The old "project is at inception" notes are stale.
- The only runtime dependencies are `streamlit` and `fpdf2` (see `requirements.txt`). No `requests`, no LLM SDK, no async queuing — IBM Bob integration (`analyzer/fixer.py`) is still a stub.
- `bob_sessions/` contains Markdown milestone notes (`task01_*.md`), not session data files. These document the development history, not runtime state.
- `reports/report_generator.py` uses fpdf2 with **built-in fonts only** (Helvetica, Courier) — no system font installation needed, which is why it works in any deploy environment.
- The `analyzer/` modules (detector, advice, repo_context) have **zero Streamlit imports** by design — they are independently testable pure-Python. Only `app.py` and `reports/` touch Streamlit/fpdf.
- `test_output.pdf` in the repo root is a sample output artefact from manual testing — not a test fixture.
