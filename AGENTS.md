# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project

**FixFlow** — AI Bug-to-Fix Assistant, built for the IBM Bob 2.0 Hackathon. Streamlit + Python.

## Stack

- **Language**: Python, virtual environment at `.venv`
- **UI**: Streamlit (`app.py` is the single entry point)
- **Package manager**: pip (`requirements.txt`); uv also supported
- **Linter/formatter**: ruff
- **Type checker**: mypy
- **Test runner**: pytest

## Commands

```bash
# Install
pip install -r requirements.txt          # or: uv pip install -r requirements.txt

# Run app
streamlit run app.py

# Lint / format
ruff check .
ruff format .

# Type check
mypy .

# Run a single test
pytest path/to/test_file.py::TestClass::test_method
```

## Project Layout

```
app.py                  # Streamlit entry point (home page)
requirements.txt        # Runtime dependencies
analyzer/
  __init__.py
  parser.py             # TODO: log parsing logic
  fixer.py              # TODO: IBM Bob API integration
assets/                 # Static assets (images, CSS overrides)
reports/                # Generated fix reports (gitkeep placeholder)
bob_sessions/           # IBM Bob session data (gitkeep placeholder)
```

## Conventions

- All Streamlit page config (`set_page_config`) must be the **first** Streamlit call in any page file.
- Custom CSS is injected via `st.markdown(..., unsafe_allow_html=True)` — keep styles in the same file, not external CSS.
- Secrets (API keys) go in `.streamlit/secrets.toml` (gitignored) — access via `st.secrets["key"]`.
- `assets/`, `reports/`, `bob_sessions/` contain only `.gitkeep` now; remove `.gitkeep` when real files are added.

## Notes

- `tempCodeRunnerFile.py` is gitignored (VS Code Code Runner artefact — do not commit).
- `.env` / `.envrc` are also gitignored — use `.streamlit/secrets.toml` for Streamlit deployments.
