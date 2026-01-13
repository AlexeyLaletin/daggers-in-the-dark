.PHONY: help install check check-backend check-frontend test test-backend test-frontend format lint clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

install: ## Install all dependencies (backend + frontend)
	@echo "Installing backend dependencies..."
	cd backend && uv venv && uv pip install -e ".[dev]"
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Installing pre-commit hooks..."
	pre-commit install

check: check-backend check-frontend ## Run all quality checks

check-backend: ## Run backend quality checks (format, lint, typecheck, test)
	@echo "=== Backend: Format check ==="
	cd backend && ruff format --check .
	@echo "=== Backend: Lint ==="
	cd backend && ruff check .
	@echo "=== Backend: Type check ==="
	cd backend && mypy .
	@echo "=== Backend: Tests ==="
	cd backend && pytest

check-frontend: ## Run frontend quality checks (format, lint, typecheck, test)
	@echo "=== Frontend: Format check ==="
	cd frontend && npm run format:check
	@echo "=== Frontend: Lint ==="
	cd frontend && npm run lint
	@echo "=== Frontend: Type check ==="
	cd frontend && npm run typecheck
	@echo "=== Frontend: Tests ==="
	cd frontend && npm test

test: test-backend test-frontend ## Run all tests

test-backend: ## Run backend tests
	cd backend && pytest -v

test-frontend: ## Run frontend tests
	cd frontend && npm test

format: ## Format all code (backend + frontend)
	@echo "Formatting backend..."
	cd backend && ruff format .
	@echo "Formatting frontend..."
	cd frontend && npm run format

lint: ## Lint all code with auto-fix (backend + frontend)
	@echo "Linting backend..."
	cd backend && ruff check --fix .
	@echo "Linting frontend..."
	cd frontend && npm run lint:fix

clean: ## Clean build artifacts and caches
	@echo "Cleaning backend..."
	rm -rf backend/.venv backend/.pytest_cache backend/.mypy_cache backend/.coverage backend/htmlcov
	@echo "Cleaning frontend..."
	rm -rf frontend/node_modules frontend/dist frontend/coverage frontend/playwright-report
	@echo "Clean complete."
