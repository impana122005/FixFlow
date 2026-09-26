# Agent Mode Rules

This file provides guidance to agents when working with code in this repository.

## Non-Obvious Coding Rules

- **CSS-only approach**: All styling lives in a single `st.markdown(<style>)` block in `app.py`. Never create external CSS files. Always use `!important` on Streamlit data-testid selectors — without it, Streamlit's own styles win.
- **CSS variable palette** (defined in `:root`): `--purple: #7c3aed`, `--purple-light: #a78bfa`, `--blue: #3b82f6`, `--bg-card`, `--bg-input`, `--border`, `--text-muted`, `--text-dim`, `--radius-md`, `--radius-sm`. Use these; hardcoding breaks theme consistency.
- **`analyzer/` purity contract**: No module under `analyzer/` may import `streamlit` or do any file I/O. They return dataclasses only. Violating this breaks the AI-replacement pathway.
- **`get_advice()` in `analyzer/advice.py`** is the single designated AI integration point — it currently returns from a static dict but is intended to be swapped for an IBM Bob API call.
- **fpdf2 byte wrapping**: `pdf.output()` → `bytearray`, not `bytes`. Always do `bytes(pdf.output())` before passing to `st.download_button(data=...)`.
- **`_safe()` in `report_generator.py`** must wrap all user-supplied text going into fpdf2 — it replaces non-latin-1 characters that crash core-font rendering.
- **`set_page_config`** is at line 17 of `app.py` and must stay the very first Streamlit call. Never insert `st.*` calls above it.
- Run `python -c "import ast; ast.parse(open('app.py', encoding='utf-8').read())"` to verify syntax after every edit to `app.py`.

## Testing

- No test suite exists yet — `pytest` is configured but there are no test files.
- When adding tests, co-locate them with source (e.g. `analyzer/test_detector.py`) — do not create a separate `tests/` directory unless the project explicitly adopts one.
