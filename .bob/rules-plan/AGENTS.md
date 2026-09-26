# Plan Mode Rules

This file provides guidance to agents when working with code in this repository.

## Architectural Constraints (Non-Obvious)

- **Project is empty** — no coupling, no modules, no DB schema yet. Architecture is greenfield.
- `.gitignore` reveals planned infrastructure: Redis (cache/broker), Celery (task queue), RabbitMQ or ActiveMQ (message broker). Plan for async from the start if these are needed.
- Both Streamlit and Flask/Django are gitignored — choose one UI framework and commit to it; mixing them is a smell.
- `uv` is the implied package manager; plan `pyproject.toml` as the single source of truth for deps, scripts, and tool config (`[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]`).
- Hackathon context: IBM Bob 2.0 — the AI assistant platform may provide tools/APIs; plan integration points accordingly.
- Secrets architecture: `.env` for local, `.streamlit/secrets.toml` for Streamlit deploy — plan for both from day one.
