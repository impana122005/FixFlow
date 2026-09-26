# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project

**FixFlow** — AI Bug-to-Fix Assistant (IBM Bob 2.0 Hackathon). Streamlit + Python.

## Stack

- **Language**: Python, virtual environment at `.venv`
- **UI**: Streamlit — `app.py` is the single entry point (no multi-page structure)
- **PDF generation**: `fpdf2` — only two runtime deps (`streamlit`, `fpdf2`)
- **Package manager**: pip (`requirements.txt`); uv also supported
- **Linter/formatter**: ruff | **Type checker**: mypy | **Test runner**: pytest

## Commands

```bash
pip install -r requirements.txt   # or: uv pip install -r requirements.txt
streamlit run app.py
ruff check . && ruff format .
mypy .
pytest path/to/test_file.py::TestClass::test_method   # single test
```

## Project Layout

```
app.py                        # Streamlit UI + all rendering logic (single page)
auth.py                       # Login/signup/forgot-password (session_state only, no DB)
analyzer/
  detector.py                 # Rule-based error scanner (regex, no AI); _ERROR_CATALOGUE drives all detection
  advice.py                   # ADVICE dict — one ErrorAdvice per exception name; get_advice() is the AI swap point
  parser.py                   # Thin wrapper: decode bytes → str, call detect_errors()
  repo_context.py             # Traceback frame parser + AST-based file matcher → ContextMatch list
  fixer.py                    # STUB — IBM Bob API integration not yet implemented
reports/
  report_generator.py         # fpdf2 PDF builder; uses only built-in Helvetica/Courier (no font files)
```

## Critical Conventions

- `auth.py` exposes three public functions: `init_auth()` (call once after `set_page_config`), `is_authenticated()`, `render_auth_page()`. All auth state lives in `st.session_state` under `ff_*` keys.
- The auth gate in `app.py` uses `st.stop()` — everything after the gate is only executed when the user is authenticated.
- `st.set_page_config()` **must be the first Streamlit call** in `app.py` — placing anything before it crashes the app.
- All CSS is injected as a single large `st.markdown(..., unsafe_allow_html=True)` block at the top of `app.py`. Never use external `.css` files or a second `st.markdown` style block — it will fight the existing theme.
- Custom CSS classes use the `ff-` prefix (e.g. `ff-err-card`, `ff-step`). Follow this naming when adding new classes.
- Secrets go in `.streamlit/secrets.toml` (gitignored), accessed via `st.secrets["key"]`. Do **not** use `.env` for Streamlit deployments.
- `fpdf2`'s core fonts support **latin-1 only**. All text passed to fpdf must go through `_safe()` in `report_generator.py` or it will crash on any non-latin-1 character (emoji, curly quotes, etc.).
- `analyzer/advice.py` is intentionally isolated (no Streamlit/I/O imports). `get_advice()` is the designated AI swap point — replace the dict lookup with an LLM call while keeping the same `ErrorAdvice` return type.
- `analyzer/detector.py` suppresses the generic `"Exception"` entry when any specific error is also found — this deduplication logic must be preserved when adding new error types.
- `reports/report_generator.py` avoids importing `DetectedError`/`ContextMatch` directly to prevent circular imports — it accepts `list` typed parameters in `build_report_data()`.
- `assets/`, `reports/.gitkeep`, `bob_sessions/.gitkeep` — remove `.gitkeep` only when real files are committed to those dirs.
- `analyzer/fixer.py` is a stub; `reports/` has a `__init__.py` but `analyzer/__init__.py` only has a comment — no package-level exports are defined.
