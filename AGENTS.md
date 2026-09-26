# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project

**FixFlow** — AI Bug-to-Fix Assistant, IBM Bob 2.0 Hackathon. Single-page Streamlit app (`app.py`).

## Commands

```bash
# Install
pip install -r requirements.txt       # or: uv pip install -r requirements.txt

# Run app
streamlit run app.py

# Lint / format
ruff check .
ruff format .

# Type check
mypy .

# Run single test
pytest path/to/test_file.py::TestClass::test_method
```

## Architecture

```
app.py                  # Entire UI — all Streamlit code, CSS, layout
analyzer/
  parser.py             # analyze_log(), parse_uploaded_file() — public entry points
  detector.py           # DetectedError dataclass, detect_errors() — 26 error types
  advice.py             # ErrorAdvice dataclass, ADVICE dict, get_advice()
  confidence.py         # score_confidence(), estimate_fix_time()
  repo_context.py       # parse_traceback_frames(), analyze_repo_context(), ContextMatch
  fixer.py              # IBM Bob API integration stub
reports/
  report_generator.py   # generate_pdf(), build_report_data(), get_severity()
```

## Critical Non-Obvious Patterns

- **All CSS** lives in one `st.markdown("""<style>…</style>""", unsafe_allow_html=True)` block near the top of `app.py`. There are no external CSS files.
- **CSS custom properties** defined on `:root` — `--purple: #7c3aed`, `--purple-light: #a78bfa`, `--blue: #3b82f6`, `--bg-card`, `--bg-input`, `--border`, `--text-muted`, `--text-dim`, `--radius-md`, `--radius-sm`. Always use variables; avoid hardcoding colors except `#8B5CF6` for the uploader accent.
- **Streamlit widget overrides** require `!important`. Key selectors: `[data-testid="stFileUploader"]`, `[data-testid="stButton"] > button[kind="primary"]`, `[data-testid="stTextArea"] textarea`, `[data-testid="stProgressBar"] > div > div`.
- **`analyzer/` modules must have zero Streamlit / I/O dependencies** — they are pure-logic and return dataclasses. `get_advice()` in `advice.py` is the designated AI replacement point.
- **fpdf2 quirk**: `pdf.output()` returns `bytearray` — wrap with `bytes(pdf.output())` for Streamlit download. Core fonts (Helvetica/Courier) are latin-1 only; all text must pass through `_safe()` in `report_generator.py`.
- **`set_page_config`** must be the very first Streamlit call — it is already at line 17 of `app.py`; never add any `st.*` call above it.
- Secrets go in `.streamlit/secrets.toml` (gitignored), accessed via `st.secrets["key"]`.
