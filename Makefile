.PHONY: help install install-dev clean test lint format run check all

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)TLS Concept - Toyota Production 2.0$(NC)"
	@echo "$(GREEN)Available targets:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-15s$(NC) %s\n", $$1, $$2}'

install: ## Install production dependencies
	@echo "$(GREEN)Installing production dependencies...$(NC)"
	pip install -r requirements.txt

install-dev: install ## Install development dependencies
	@echo "$(GREEN)Installing development dependencies...$(NC)"
	pip install -r requirements-dev.txt
	pre-commit install

clean: ## Clean up cache and temporary files
	@echo "$(GREEN)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.swp" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov/ dist/ build/
	@echo "$(GREEN)Cleanup complete!$(NC)"

test: ## Run tests
	@echo "$(GREEN)Running tests...$(NC)"
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term-missing

test-quick: ## Run tests without coverage
	@echo "$(GREEN)Running quick tests...$(NC)"
	pytest tests/ -v

lint: ## Run linters
	@echo "$(GREEN)Running linters...$(NC)"
	@echo "$(BLUE)Black...$(NC)"
	black --check app.py config.py tests/ || true
	@echo "$(BLUE)isort...$(NC)"
	isort --check-only app.py config.py tests/ || true
	@echo "$(BLUE)flake8...$(NC)"
	flake8 app.py config.py tests/ --max-line-length=88 --extend-ignore=E203,W503 || true
	@echo "$(BLUE)pylint...$(NC)"
	pylint app.py config.py --exit-zero

format: ## Format code with black and isort
	@echo "$(GREEN)Formatting code...$(NC)"
	black app.py config.py tests/
	isort app.py config.py tests/

type-check: ## Run type checking with mypy
	@echo "$(GREEN)Running type checker...$(NC)"
	mypy app.py config.py --ignore-missing-imports || true

security: ## Run security checks
	@echo "$(GREEN)Running security checks...$(NC)"
	safety check || true

check: lint type-check ## Run all checks
	@echo "$(GREEN)All checks completed!$(NC)"

run: ## Run the application
	@echo "$(GREEN)Starting application...$(NC)"
	streamlit run app.py

run-prod: ## Run the application in production mode
	@echo "$(GREEN)Starting application in production mode...$(NC)"
	streamlit run app.py --server.port=8501 --server.address=0.0.0.0

setup: clean install-dev ## Complete setup for development
	@echo "$(GREEN)Development environment setup complete!$(NC)"
	@echo "$(BLUE)Run 'make run' to start the application$(NC)"

all: clean install-dev format lint test ## Run all tasks
	@echo "$(GREEN)All tasks completed successfully!$(NC)"

.DEFAULT_GOAL := help
