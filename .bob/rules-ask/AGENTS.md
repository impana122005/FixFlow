# Ask Mode Rules

This file provides guidance to agents when working with code in this repository.

## Documentation Context (Non-Obvious)

- **FixFlow** is an IBM Bob 2.0 Hackathon project — "IBM Bob" refers to the IBM AI coding assistant platform, not an individual.
- The project is at **inception** (only README + .gitignore exist) — no architecture docs or source to reference yet.
- Stack signals come entirely from `.gitignore` patterns — treat them as intent, not fact, until `pyproject.toml` exists.
- Streamlit and Flask/Django are both hinted in `.gitignore`; the actual chosen framework is not yet committed.
- Redis/Celery/RabbitMQ/ActiveMQ ignore entries suggest planned async or messaging components, but none are implemented.
