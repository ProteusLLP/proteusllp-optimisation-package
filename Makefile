# Makefile for Proteus Optimisation Package

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  lint           - Run ruff linting"
	@echo "  lint-fix       - Auto-fix lint issues with ruff"
	@echo "  format         - Run ruff formatting"
	@echo "  format-check   - Check ruff formatting without making changes"
	@echo "  typecheck      - Run mypy type checking"
	@echo "  static-analysis - Run all static analysis tools (lint, format, typecheck)"
	@echo "  test           - Run pytest with coverage"
	@echo "  check          - Run all checks (static-analysis + tests)"
	@echo "  build          - Build the package"
	@echo "  clean          - Clean build artifacts"

# Static analysis targets
.PHONY: lint
lint:
	pdm run ruff check optimizer tests

.PHONY: lint-fix
lint-fix:
	pdm run ruff check --fix optimizer tests

.PHONY: format
format:
	pdm run ruff format optimizer tests

.PHONY: format-check
format-check:
	pdm run ruff format --check optimizer tests

.PHONY: typecheck
typecheck:
	pdm run mypy optimizer/

.PHONY: static-analysis
static-analysis: lint format-check typecheck

# Testing targets
.PHONY: test
test:
	pdm run pytest tests/ -v --cov=optimizer --cov-report=term-missing --cov-report=xml

# Combined check target
.PHONY: check
check: static-analysis test

# Build targets
.PHONY: build
build:
	pdm build

.PHONY: clean
clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .coverage coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
