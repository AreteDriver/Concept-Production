# Contributor Guide - TLS Concept Production 2.0

## Project Overview

TLS Concept Production 2.0 is an AI-driven QA/Lean system scaffold repository for Toyota Production System improvements. The goal is to reduce install/QA cycle time with AI guidance and live metrics.

**Flow:** AI → Data Layer → AR Interface → Human feedback

This is a Streamlit-based application that demonstrates AI-driven process optimization.

## Tech Stack

- **Python 3.10+**: Core language
- **Streamlit**: Web application framework for data apps
- **Pandas**: Data manipulation and analysis
- **OpenAI API**: AI/LLM integration
- **OR-Tools**: Optimization library (note: platform-specific wheels may apply)
- **Protobuf**: Data serialization

## Setup

### Prerequisites
- Python 3.10, 3.11, or 3.12
- pip (Python package manager)
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/AreteDriver/TLS-Concept-production-2.0.git
   cd TLS-Concept-production-2.0
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `.env.template` to `.env`:
     ```bash
     cp .env.template .env
     ```
   - Fill in your API keys and configuration in `.env`
   - **IMPORTANT**: Never commit `.env` to the repository

## Running the App

### Start the Streamlit application
```bash
streamlit run app.py
```

By default, the app will be available at `http://localhost:8501` (or the port specified in your `STREAMLIT_PORT` environment variable).

## Testing

### Running Tests Locally

1. **Install pytest** (if not already installed)
   ```bash
   pip install pytest
   ```

2. **Run all tests**
   ```bash
   pytest
   ```

3. **Run tests with verbose output**
   ```bash
   pytest -v
   ```

4. **Run tests quietly (like CI)**
   ```bash
   pytest -q
   ```

See `tests/README.md` for more detailed testing documentation.

### Writing Tests

- Place test files in the `tests/` directory
- Name test files with `test_` prefix (e.g., `test_feature.py`)
- Name test functions with `test_` prefix (e.g., `def test_something():`)
- Keep tests independent and isolated

## CI (Continuous Integration)

This repository uses GitHub Actions for automated testing.

### CI Pipeline

The CI workflow (`.github/workflows/ci.yml`) runs on every push and pull request:

1. **Matrix Testing**: Tests against Python 3.10, 3.11, and 3.12
2. **Dependency Installation**: Installs all requirements
3. **Linting**: Runs `ruff check .` to catch code quality issues
4. **Testing**: Runs `pytest -q` to execute all tests

Example CI workflow:
```yaml
- Install dependencies: pip install -r requirements.txt
- Run linter: pip install ruff && ruff check .
- Run tests: pip install pytest && pytest -q
```

### Running CI Commands Locally

Before pushing, you can run the same checks locally:
```bash
# Install dependencies
pip install -r requirements.txt

# Run linter
pip install ruff
ruff check .

# Run tests
pip install pytest
pytest -q
```

## Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality before commits.

### Setup Pre-commit

1. **Install pre-commit**
   ```bash
   pip install pre-commit
   ```

2. **Install the git hooks**
   ```bash
   pre-commit install
   ```

3. **Run manually (optional)**
   ```bash
   pre-commit run --all-files
   ```

### Configured Hooks

- **Black**: Python code formatter (opinionated, PEP 8 compliant)
- **Ruff**: Fast Python linter (replaces flake8, pylint, isort, and more)

Pre-commit hooks will automatically format and check your code before each commit.

## Linting and Formatting

### Recommended Tools

1. **Black** (code formatter)
   ```bash
   pip install black
   black .
   ```

2. **Ruff** (linter and formatter)
   ```bash
   pip install ruff
   ruff check .
   ruff check --fix .  # Auto-fix issues
   ruff format .        # Format code
   ```

3. **isort** (import sorter) - *Note: Ruff includes isort functionality*
   ```bash
   pip install isort
   isort .
   ```

### Editor Integration

Consider setting up your editor with:
- Black formatter on save
- Ruff linter integration
- Python language server (Pylance, pyright, or jedi)

## Security & Secrets

### API Keys and Secrets

- **Local Development**: Store secrets in `.env` file (already in `.gitignore`)
- **GitHub Actions**: Use GitHub Secrets in repository settings
  - Navigate to: Settings → Secrets and variables → Actions
  - Add secrets like `OPENAI_API_KEY`
  - Access in workflows: `${{ secrets.OPENAI_API_KEY }}`

### Best Practices

- Never commit API keys or secrets to the repository
- Use `.env.template` to document required environment variables
- Review `.gitignore` to ensure sensitive files are excluded
- Use environment variables for configuration

## Dependencies

### Managing Dependencies

- All dependencies are listed in `requirements.txt`
- **Pin dependencies** for reproducible builds (e.g., `streamlit==1.28.0`)
- For loose pinning, use `>=` (e.g., `streamlit>=1.0`)
- Update dependencies carefully and test thoroughly

### Adding New Dependencies

1. Add to `requirements.txt`
2. Install: `pip install -r requirements.txt`
3. Test that the application still works
4. Commit the updated `requirements.txt`

### Note on OR-Tools

OR-Tools may have platform-specific wheels. If you encounter installation issues:
- Check the [OR-Tools documentation](https://developers.google.com/optimization/install)
- Ensure you're using a supported Python version and platform
- Consider using pre-built wheels for your specific platform

## Contributing

### Workflow

1. **Create a branch** for your feature or fix
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code following existing style
   - Add tests for new functionality
   - Update documentation as needed

3. **Test locally**
   ```bash
   pytest
   ruff check .
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Description of changes"
   ```
   (Pre-commit hooks will run automatically)

5. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Code Style

- Follow PEP 8 style guidelines
- Use Black for formatting (line length: 88 characters by default)
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions small and focused

### Pull Request Guidelines

- Provide a clear description of changes
- Reference related issues
- Ensure CI passes before requesting review
- Respond to review feedback promptly

## License

This project currently does not have a LICENSE file. Consider adding one to clarify usage rights and terms.

Common options:
- **MIT License**: Permissive, allows commercial use
- **Apache 2.0**: Permissive with patent grant
- **GPL**: Copyleft, requires derivative works to be open source

Add a `LICENSE` file to the repository root to specify the license.

## Onboarding Checklist

For new contributors, complete this checklist:

- [ ] Clone the repository
- [ ] Set up Python virtual environment
- [ ] Install dependencies from `requirements.txt`
- [ ] Copy `.env.template` to `.env` and configure
- [ ] Run the application locally with `streamlit run app.py`
- [ ] Install pre-commit hooks: `pre-commit install`
- [ ] Run tests locally: `pytest`
- [ ] Run linter: `ruff check .`
- [ ] Read through this contributor guide
- [ ] Review the codebase structure
- [ ] Review open issues and PRs
- [ ] Set up editor integration (Black, Ruff, Python LSP)
- [ ] Make a small test commit to verify pre-commit hooks work
- [ ] Introduce yourself in discussions or team chat

## Getting Help

- Check existing issues and documentation first
- Create an issue for bugs or feature requests
- Ask questions in pull request discussions
- Review CI logs if builds fail

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Black Documentation](https://black.readthedocs.io/)
- [pre-commit Documentation](https://pre-commit.com/)
