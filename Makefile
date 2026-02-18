# Chirp-UI Makefile
# Wraps uv commands to ensure Python 3.14t is used

PYTHON_VERSION ?= 3.14t
VENV_DIR ?= .venv

.PHONY: all help setup install test test-cov lint lint-fix format ty clean shell build publish release gh-release

all: help

help:
	@echo "Chirp-UI Development CLI"
	@echo "========================"
	@echo "Python Version: $(PYTHON_VERSION)"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup      - Create virtual environment with Python $(PYTHON_VERSION)"
	@echo "  make install    - Install dependencies in development mode"
	@echo "  make test       - Run the test suite"
	@echo "  make test-cov   - Run tests with coverage report"
	@echo "  make lint       - Run ruff linter"
	@echo "  make lint-fix   - Run ruff linter with auto-fix"
	@echo "  make format     - Run ruff formatter"
	@echo "  make ty         - Run ty type checker (fast, Rust-based)"
	@echo "  make build      - Build distribution packages"
	@echo "  make publish    - Publish to PyPI (uses .env for token)"
	@echo "  make release    - Build and publish in one step"
	@echo "  make gh-release - Create GitHub release (triggers PyPI via workflow)"
	@echo "  make clean      - Remove venv, build artifacts, and caches"
	@echo "  make shell      - Start a shell with the environment activated"

setup:
	@echo "Creating virtual environment with Python $(PYTHON_VERSION)..."
	uv venv --python $(PYTHON_VERSION) $(VENV_DIR)

install:
	@echo "Installing dependencies..."
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Error: $(VENV_DIR) not found. Run 'make setup' first."; \
		exit 1; \
	fi
	@bash -c 'source "$(VENV_DIR)/bin/activate" && uv sync --active --group dev --frozen'

test:
	uv run pytest -q --tb=short

test-cov:
	uv run pytest --cov=chirp_ui --cov-report=term-missing

lint:
	@echo "Running ruff linter..."
	uv run ruff check .

lint-fix:
	@echo "Running ruff linter with auto-fix..."
	uv run ruff check . --fix

format:
	@echo "Running ruff formatter..."
	uv run ruff format .

ty:
	@echo "Running ty type checker (Astral, Rust-based)..."
	uv run ty check src/chirp_ui/

# =============================================================================
# Build & Release
# =============================================================================

build:
	@echo "Building distribution packages..."
	rm -rf dist/
	uv build
	@echo "✓ Built:"
	@ls -la dist/

publish:
	@echo "Publishing to PyPI..."
	@if [ -f .env ]; then \
		export $$(cat .env | xargs) && uv publish; \
	else \
		echo "Warning: No .env file found, trying without token..."; \
		uv publish; \
	fi

release: build publish
	@echo "✓ Release complete"

# Create GitHub release; triggers python-publish workflow → PyPI
gh-release:
	@VERSION=$$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/'); \
	PROJECT=$$(grep '^name = ' pyproject.toml | sed 's/name = "\(.*\)"/\1/'); \
	echo "Creating release v$$VERSION for $$PROJECT..."; \
	git push origin main 2>/dev/null || true; \
	git push origin v$$VERSION 2>/dev/null || true; \
	echo "Release v$$VERSION. See repository for details." | gh release create v$$VERSION \
		--title "$$PROJECT $$VERSION" \
		-F -; \
	echo "✓ GitHub release v$$VERSION created (PyPI publish will run via workflow)"

# =============================================================================
# Cleanup
# =============================================================================

clean:
	rm -rf $(VENV_DIR)
	rm -rf build/ dist/ *.egg-info src/*.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ty_cache" -exec rm -rf {} + 2>/dev/null || true

shell:
	@echo "Activating environment with GIL disabled..."
	@bash -c 'source $(VENV_DIR)/bin/activate && export PYTHON_GIL=0 && echo "✓ venv active, GIL disabled" && exec bash'
