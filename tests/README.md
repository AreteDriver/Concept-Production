# Testing Guide

## Running Tests Locally

### Install pytest
```bash
pip install pytest
```

### Run all tests
```bash
pytest
```

### Run tests with verbose output
```bash
pytest -v
```

### Run tests with quiet output (like CI)
```bash
pytest -q
```

### Run specific test file
```bash
pytest tests/test_sample.py
```

## Running CI Commands Locally

The CI pipeline runs the following commands. You can run these locally to check your changes before pushing:

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run linting with ruff
```bash
pip install ruff
ruff check .
```

### 3. Run tests
```bash
pip install pytest
pytest -q
```

## Adding New Tests

1. Create test files in the `tests/` directory with names starting with `test_`
2. Write test functions with names starting with `test_`
3. Use pytest features like fixtures, parametrize, and markers as needed
4. Run tests locally to verify they work before pushing

## Test Structure

```
tests/
├── README.md          # This file
└── test_sample.py     # Sample test demonstrating test structure
```

## Tips

- Always run tests before committing
- Write tests for new features and bug fixes
- Keep tests independent and isolated
- Use meaningful test names that describe what is being tested
