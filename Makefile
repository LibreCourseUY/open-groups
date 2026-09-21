VENV ?= venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: help setup install dev test lint format migrate docker clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

setup: ## Create the virtualenv and install dev dependencies
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt

install: ## Install/refresh dependencies in the existing virtualenv
	$(PIP) install -r requirements-dev.txt

dev: ## Run the app with autoreload on http://localhost:8000
	DBWARDEN_CONFIG_MODULE=database PYTHONPATH=. $(VENV)/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000

migrate: ## Apply pending dbwarden migrations (DEV sqlite)
	DBWARDEN_CONFIG_MODULE=database PYTHONPATH=. $(VENV)/bin/dbwarden migrate --verbose

test: ## Run the test suite
	$(VENV)/bin/pytest

lint: ## Check linting and formatting
	$(VENV)/bin/ruff check .
	$(VENV)/bin/ruff format --check .

format: ## Auto-fix lint issues and format code
	$(VENV)/bin/ruff check --fix .
	$(VENV)/bin/ruff format .

docker: ## Build and run with Docker Compose on http://localhost:8000
	docker compose up --build

clean: ## Remove caches and the local sqlite database
	rm -rf $(VENV) .pytest_cache .ruff_cache __pycache__ groups.db
