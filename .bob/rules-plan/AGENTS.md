# Plan Mode Rules

This file provides guidance to agents when working with code in this repository.

## Non-Obvious Architectural Constraints

- **`app.py` is monolithic by design** — all UI, state management, and layout live in one file. This is intentional for a hackathon single-page app. Do not split into pages or add a `pages/` directory unless there is a strong feature reason.
- **`analyzer/` → pure functions only**: The entire `analyzer/` layer is stateless. Streamlit session state is managed exclusively in `app.py`. This boundary must not be crossed.
- **AI integration seam**: `analyzer/fixer.py` + `get_advice()` in `analyzer/advice.py` are the two IBM Bob API integration points. Both are currently stubs. Any planning for AI features must route through these; do not add new Streamlit-level AI calls.
- **PDF generation is synchronous and blocking** — `generate_pdf()` runs on the main thread. If logs become large, this will block Streamlit's event loop. Plan for offloading only if log sizes grow significantly.
- **No database, no persistence** — `bob_sessions/` and `reports/` are placeholder directories. All state is ephemeral (Streamlit session). Any plan involving persistence needs to introduce a storage layer from scratch.
- **26 error types are hard-coded** in `analyzer/detector.py`. Adding new types requires editing `detect_errors()` and the `ADVICE` dict in `analyzer/advice.py` in sync. There is no plugin or registry pattern.
