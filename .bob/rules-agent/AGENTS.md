# Agent Mode Rules

This file provides guidance to agents when working with code in this repository.

## Coding Rules (Non-Obvious)

- **`fpdf2` latin-1 constraint**: every string written to the PDF **must** pass through `_safe()` in `reports/report_generator.py`. Emojis, curly quotes, or any non-latin-1 character will crash `fpdf2` core fonts. Never add fpdf `multi_cell`/`cell` calls without `_safe()`.
- **AI swap point**: `analyzer/advice.py::get_advice()` is explicitly designed to be replaced by an LLM call. Keep `ErrorAdvice` as the return type — `app.py` and `report_generator.py` both destructure its fields directly.
- **Adding a new error type**: requires changes in two places — add to `_ERROR_CATALOGUE` in `analyzer/detector.py` **and** add a matching key in `ADVICE` dict in `analyzer/advice.py`. The `Exception` deduplication logic in `detect_errors()` must not be broken.
- **Circular import guard**: `reports/report_generator.py::build_report_data()` takes `list` (not typed `list[DetectedError]`) to avoid importing from `analyzer/`. Keep it that way.
- **No package-level exports**: `analyzer/__init__.py` is a comment stub. `app.py` imports directly from sub-modules (`from analyzer.parser import ...`, `from analyzer.detector import ...`). Do not add `__all__` or re-exports to `__init__.py` without updating all import sites.
- **Session state for PDF**: `app.py` stores PDF bytes in `st.session_state["pdf_bytes"]` and gates rendering on `st.session_state["pdf_ready"]`. The download button section is **outside** the `if analyze_clicked:` block intentionally — it persists across reruns.
- **uv preferred**: use `uv pip install` / `uv pip sync` over plain `pip` when possible. Add dependencies to `requirements.txt` only (no `pyproject.toml` exists yet).
- **ruff covers everything**: do not add `black`, `isort`, or `flake8`. `ruff format` handles formatting; `ruff check` handles linting.
