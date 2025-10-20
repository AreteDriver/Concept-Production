# TLS Concept Production 2.0 - GitHub Copilot Instructions

## Project Overview
This is an AI-driven QA/Lean system for Toyota Production methodologies. The project is a scaffold repository under development that demonstrates process optimization using AI guidance and live metrics.

**Purpose:** Reduce install/QA cycle time with AI guidance and live metrics  
**Target Audience:** Manufacturing teams, QA engineers, and process optimization specialists  
**Key Features:**
- AI-driven process optimization
- Real-time metrics and analytics
- Interactive Streamlit-based interface
- Integration with Toyota Production System principles

## Tech Stack
- **Language:** Python 3.12+
- **Web Framework:** Streamlit
- **Data Processing:** Pandas
- **Optimization:** OR-Tools (Google's optimization library)
- **AI Integration:** OpenAI API
- **Additional:** Protobuf (version <5 for compatibility)

## Project Structure
```
TLS-Concept-production-2.0/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── toyota-production-2.0/    # Additional modules (currently empty)
├── .venv/                    # Virtual environment (not tracked)
└── README.md                 # Project documentation
```

## Development Setup

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)

### Installation
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Activate virtual environment (if not already active)
source .venv/bin/activate

# Run the Streamlit app
streamlit run app.py
```

The application will start on `http://localhost:8501` by default.

## Coding Guidelines

### Python Style
- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose

### Code Organization
- Place reusable utilities in separate modules within `toyota-production-2.0/`
- Keep the main `app.py` focused on Streamlit UI logic
- Separate business logic from presentation logic

### Dependencies
- Always update `requirements.txt` when adding new dependencies
- Pin versions for critical dependencies (e.g., `protobuf<5`)
- Test compatibility before adding new packages

### Comments
- Write self-documenting code with clear variable names
- Add comments only when the code's intent is not immediately obvious
- Document complex algorithms or business logic
- Include TODO comments for planned improvements

## AI/OpenAI Integration Notes
- When working with OpenAI API calls, handle rate limits and errors gracefully
- Store API keys in environment variables, never in code
- Consider cost implications of API calls in production

## Streamlit Best Practices
- Use `st.cache_data` for expensive computations or data loading
- Organize the UI with clear sections using `st.header()` and `st.subheader()`
- Provide user feedback with `st.success()`, `st.warning()`, and `st.error()`
- Keep the UI responsive and avoid blocking operations

## Testing
Currently, there is no formal test infrastructure. When adding tests:
- Create a `tests/` directory for test files
- Use `pytest` as the testing framework
- Name test files with `test_` prefix
- Aim for high code coverage on critical paths

## Common Tasks

### Adding a New Feature
1. Create a new branch from `main`
2. Implement the feature with minimal changes
3. Update documentation if needed
4. Test the feature manually with the Streamlit app
5. Create a pull request with clear description

### Updating Dependencies
1. Update version in `requirements.txt`
2. Test for compatibility issues
3. Update this instructions file if new setup steps are needed

### Debugging
- Use Streamlit's built-in debug mode: `streamlit run app.py --logger.level=debug`
- Check browser console for client-side errors
- Review terminal output for server-side errors

## Important Files to Preserve
- `app.py` - Main application entry point (critical)
- `requirements.txt` - Dependency specifications (critical)
- `README.md` - Project documentation
- `.gitignore` - Version control exclusions

## Files to Ignore
- `.venv/` - Virtual environment (generated)
- `__pycache__/` - Python cache files (generated)
- `.DS_Store` - macOS system files
- `*.swp`, `*.swo` - Editor temporary files

## Toyota Production System Context
This project applies lean manufacturing principles from Toyota Production System:
- **Continuous Improvement (Kaizen):** Always look for ways to optimize
- **Just-In-Time:** Deliver value when needed, avoid waste
- **Jidoka:** Build quality into the process
- **Visual Management:** Make metrics and status visible

When implementing features, consider these principles and how they apply to software development and QA processes.

## Notes for AI Code Generation
- Prioritize simplicity and maintainability over clever solutions
- Make minimal changes to achieve the goal
- Preserve existing functionality unless explicitly asked to change it
- When adding new features, follow the existing code style and patterns
- Always consider the manufacturing/QA domain context
