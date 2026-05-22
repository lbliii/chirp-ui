# Agent Curated Snippets

Status: curated source
Provenance: `docs-derived`

This file contains hand-curated, copyable snippets that passed the review gate in
`AGENT-SOURCE-INVENTORY.md`. Snippets here are intentionally small and
macro-first; generated site output, static showcase scaffolding, and browser
fixtures are not source material.

## Appearance And Tone Card

Source: `docs/APPEARANCE-TONE.md`
Inventory: `docs/AGENT-SOURCE-INVENTORY.md`
Eligibility: `copyable-curated`
Provenance: `docs-derived`
Runnable proof: `tests/test_components.py`

```jinja
{% from "chirpui/card.html" import card %}
{% from "chirpui/badge.html" import badge %}

{% call card(title="Deployment", appearance="outlined", tone="primary") %}
    <p>Production release candidate is ready for review.</p>
    {{ badge("healthy", variant="success") }}
{% end %}
```

Proof:

- Uses public macros and params instead of raw component classes.
- Uses `appearance=` and `tone=` params instead of modifier classes.
- Contains no inline scripts, browser-test selectors, static showcase classes,
  or unsafe attributes.
