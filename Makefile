# Chirp-UI Makefile
# Wraps uv commands to ensure Python 3.14t is used

PYTHON_VERSION ?= 3.14t
VENV_DIR ?= .venv

.PHONY: all help setup install test test-js test-cov test-browser pre-pr lint lint-fix format ty clean shell build publish release gh-release release-preflight showcase showcase-public showcase-guard

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
	@echo "  make test-browser - Run browser integration tests (Playwright)"
	@echo "  make pre-pr     - Pre-PR gate: full ci + docs-chrome browser/a11y smoke"
	@echo "  make lint       - Run ruff linter"
	@echo "  make lint-fix   - Run ruff linter with auto-fix"
	@echo "  make format     - Run ruff formatter"
	@echo "  make ty         - Run ty type checker (fast, Rust-based)"
	@echo "  make build      - Build distribution packages"
	@echo "  make publish    - Publish to PyPI (uses .env for token)"
	@echo "  make release    - Build and publish in one step"
	@echo "  make gh-release - Create GitHub release (triggers PyPI via workflow)"
	@echo "  make release-preflight - Verify committed manifest.json + chirpui.css are fresh"
	@echo "  make showcase         - Assemble static showcase into _site/ for preview"
	@echo "  make showcase-public  - Copy showcase into site/public/showcase/ (after bengal build)"
	@echo "  make showcase-guard   - Fail if the published showcase still serves the placeholder"
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

test-js:
	npx vitest run

test-browser:
	uv run --group browser pytest tests/browser/ -q --timeout=30 --override-ini='addopts='

# Pre-PR gate a contributor runs before opening a PR: the full blocking `ci`
# gate plus the docs-chrome browser/a11y smoke (docs-build-all + focused chrome
# + docs-nav/landmark axe proof). The browser suite is intentionally NOT in
# `poe ci`; CI runs the same smoke in a separate, non-required job.
pre-pr:
	uv run --group browser poe pre-pr

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

# Regenerate committed generated artifacts (chirpui.css, manifest.json) and
# fail if the working tree now has uncommitted changes. Runs before every
# build/release — guarantees the tag carries a fresh manifest + CSS bundle,
# and refuses to ship if the dev forgot to commit a regeneration.
release-preflight:
	@echo "Regenerating generated artifacts..."
	uv run poe build-css
	uv run poe build-manifest
	uv run poe build-docs
	uv run poe build-component-index
	@echo "Verifying no uncommitted changes to generated artifacts..."
	@if ! git diff --quiet -- src/chirp_ui/manifest.json src/chirp_ui/templates/chirpui.css docs/COMPONENT-OPTIONS.md site/content/docs/components/all.md; then \
		echo ""; \
		echo "ERROR: one or more generated artifacts are stale." >&2; \
		echo "       Commit the regenerated files below, then re-run:" >&2; \
		echo ""; \
		git diff --stat -- src/chirp_ui/manifest.json src/chirp_ui/templates/chirpui.css docs/COMPONENT-OPTIONS.md site/content/docs/components/all.md >&2; \
		exit 1; \
	fi
	@echo "✓ Generated artifacts are fresh and committed"

build: release-preflight
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
gh-release: release-preflight
	@VERSION=$$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/'); \
	PROJECT=$$(grep -m1 '^name = ' pyproject.toml | sed 's/name = "\(.*\)"/\1/'); \
	echo "Creating release v$$VERSION for $$PROJECT..."; \
	git push origin main 2>/dev/null || true; \
	git push origin v$$VERSION 2>/dev/null || true; \
	echo "Release v$$VERSION. See repository for details." | gh release create v$$VERSION \
		--title "$$PROJECT $$VERSION" \
		-F -; \
	echo "✓ GitHub release v$$VERSION created (PyPI publish will run via workflow)"

# =============================================================================
# Showcase (GitHub Pages preview)
# =============================================================================

showcase:
	@bash scripts/assemble-static-showcase.sh "$(CURDIR)/_site"
	@echo "Open _site/index.html in a browser to preview"

# Run after: uv run bengal build --source site
showcase-public:
	@bash scripts/assemble-static-showcase.sh "$(CURDIR)/site/public/showcase"
	@$(MAKE) --no-print-directory showcase-guard

# Fail if the published showcase HTML still serves the build-command placeholder
# (section index "No section content yet" + "injected here after ...") instead of
# the assembled gallery. Guards the /showcase/ home-page CTA against regressions.
showcase-guard:
	@out="$(CURDIR)/site/public/showcase/index.html"; \
	if [ ! -f "$$out" ]; then \
		echo "ERROR: $$out missing — the static showcase was not assembled." >&2; \
		echo "       Run 'make showcase-public' after 'uv run bengal build --source site'." >&2; \
		exit 1; \
	fi; \
	if grep -Fq 'injected here after' "$$out" || grep -Fq 'No section content' "$$out"; then \
		echo "ERROR: $$out still contains the placeholder/empty-section sentinel." >&2; \
		echo "       The real gallery was not injected over the section index;" >&2; \
		echo "       the /showcase/ route would serve build-command placeholder text." >&2; \
		exit 1; \
	fi; \
	if ! grep -Fq 'Complete Component Showcase' "$$out"; then \
		echo "ERROR: $$out does not contain the assembled gallery marker." >&2; \
		echo "       Expected the static showcase but found a fallback page." >&2; \
		echo "       Run 'make showcase-public' after the Bengal build." >&2; \
		exit 1; \
	fi; \
	echo "✓ /showcase/ serves the assembled gallery (no placeholder sentinels)"

# =============================================================================
# Cleanup
# =============================================================================

clean:
	rm -rf $(VENV_DIR)
	rm -rf build/ dist/ *.egg-info src/*.egg-info _site/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ty_cache" -exec rm -rf {} + 2>/dev/null || true

shell:
	@echo "Activating environment with GIL disabled..."
	@bash -c 'source $(VENV_DIR)/bin/activate && export PYTHON_GIL=0 && echo "✓ venv active, GIL disabled" && exec bash'
