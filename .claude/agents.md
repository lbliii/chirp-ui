# Agents

## test-runner

Run after writing or modifying Python source or templates.

```bash
uv run pytest -q --tb=short
```

## lint-check

Run after editing Python files.

```bash
uv run ruff check . && uv run ruff format . --check
```

## css-validator

Run after editing `.css` files or HTML templates that reference CSS classes.

```bash
uv run pytest tests/test_css_syntax.py tests/test_template_css_contract.py tests/test_transition_tokens.py -q
```

## ci-full

Run before opening a PR or releasing. Covers lint, format, CSS, types, and tests.

```bash
uv run poe ci
```
