# Agents

## lead-designer

Advisory design reviewer for Chirp UI visual quality, product coherence,
interaction polish, density, hierarchy, and screenshot-based critique.

Persona: `.claude/agents/lead-designer.md`

## accessibility-auditor

Advisory accessibility reviewer for keyboard flow, focus visibility, semantics,
contrast, reduced motion, responsive touch behavior, and browser-backed
interaction proof.

Persona: `.claude/agents/accessibility-auditor.md`

## release-captain

Advisory release-readiness reviewer for generated artifacts, changelog
fragments, CI proof, steward notes, docs/examples collateral, manifest/CSS
rebuilds, and PR hygiene.

Persona: `.claude/agents/release-captain.md`

## agent-grounding-auditor

Advisory reviewer for agent-facing source quality, manifest/docs/examples/site
consistency, snippet provenance, and hallucination-resistant guidance.

Persona: `.claude/agents/agent-grounding-auditor.md`

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
