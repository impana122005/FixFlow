# Agent Mode Rules

This file provides guidance to agents when working with code in this repository.

## Coding Rules (Non-Obvious)

- **No source code exists yet** — scaffold `pyproject.toml` or `setup.py` before adding modules.
- Use **uv** for dependency management when possible (`.gitignore` has a dedicated UV section, indicating project preference).
- Prefer `ruff` over `flake8`/`black`/`isort` — it covers linting *and* formatting in one tool.
- `.env` / `.envrc` are gitignored; use them for secrets. Never hardcode API keys.
- `tempCodeRunnerFile.py` is gitignored — never commit it.
- Streamlit secrets belong in `.streamlit/secrets.toml` (gitignored), not in `.env`.
- When adding async task queues (Celery/RabbitMQ patterns are in `.gitignore`), store broker credentials in `.env`.

## Testing

- Run a **single test**: `pytest path/to/test_file.py::TestClass::test_method`
- Test cache (`__pycache__`, `.pytest_cache/`) is gitignored — safe to delete on clean runs.
