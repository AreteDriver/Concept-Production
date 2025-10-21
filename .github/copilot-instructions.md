# Copilot instructions for TLS-Concept-production-2.0

Provide Copilot with concise, accurate, repository-specific context so it can generate code and suggestions that follow project conventions and domain constraints. Do not include unrelated project examples or external product plans.

## Development setup

- Python version: 3.12+
- Recommended: create a virtual environment: python -m venv .venv
- Activate: source .venv/bin/activate (macOS/Linux) or .venv\Scripts\activate (Windows)
- Install dependencies: pip install -r requirements.txt
- Run the Streamlit app for local development: streamlit run app.py
- Tests (if present): pytest

## Coding conventions and guidelines

- Follow PEP 8 style and idiomatic Python.
- Use black for formatting and ruff/flake8 for linting where configured.
- Keep functions small and well-documented. Add docstrings for public functions and classes.
- Use type hints where helpful; run mypy if configured.
- Avoid committing secrets or API keys. Use environment variables and the .env file (which must be gitignored).

## AI / OpenAI integration guidance

- Centralize OpenAI calls in a helper module and handle rate limits and retries with exponential backoff.
- Validate and sanitize all inputs sent to the model. Treat model output as untrusted until parsed and validated.
- Never embed API keys in source files or documentation. Read keys from environment variables.

## Streamlit-specific guidance

- Use st.cache_data and st.cache_resource appropriately to avoid unnecessary reruns.
- Keep UI logic separated from core business logic where possible.
- Keep the main streamlit entrypoint (app.py) simple and delegate functionality to modules.

## Repository ownership and review

- Use descriptive commit messages and small, focused pull requests.
- Add reviewers for core modules. Ensure tests and linters pass before merging.

Note

This file has been intentionally focused on repository-specific guidance. Any unrelated template/example content has been removed. If you want to expand sections with more detail (examples of error handling patterns, or explicit CI steps), add them in new commits.