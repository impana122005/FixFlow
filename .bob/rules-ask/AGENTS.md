# Ask Mode Rules

This file provides guidance to agents when working with code in this repository.

## Non-Obvious Documentation Context

- **FixFlow is a complete, working app** — all six milestones are implemented. The earlier `.bob/rules-ask/AGENTS.md` described the project as empty (inception phase); that is now outdated.
- The "IBM Bob" in hackathon context refers to the IBM AI coding assistant platform, not a person. `analyzer/fixer.py` is the planned IBM Bob API integration point.
- **`analyzer/advice.py`** contains the full static advice dictionary for 26 error types. The docstring on `get_advice()` explicitly marks it as the AI replacement point — the canonical reference for how fixes are structured.
- **`reports/report_generator.py`** is the PDF generation module. `_SEVERITY_MAP` and `_generate_report_id()` are internal; `generate_pdf()` and `build_report_data()` are the public API.
- There are no docs outside of `README.md` and the AGENTS.md files. The source code is the canonical reference.
