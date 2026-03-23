# Composition patterns

ChirpUI components are Kida macros: `{% call %}`, `{% slot %}`, and `{% def %}`. These patterns work well in practice; the main pitfalls are conditional wrappers and duplicate imports when mixing full pages with HTMX fragments.

## Nesting slots and calls

Prefer shallow trees. When you need a neutral wrapper for layout only, use a one-line macro in your app templates:

```kida
{% def passthrough() %}
{% slot %}
{% end %}
```

Then `{% call passthrough() %}…{% end %}` participates in `{% if %}` / `{% match %}` branches without adding DOM nodes.

## HTMX fragments and `{% from %}`

When a template is rendered as a **full page**, top-level `{% from "chirpui/…" import … %}` runs automatically. For **`render_block()`** / fragment targets, ensure macros imported in a **parent layout** are in scope: Kida runs `{% globals %}`, `{% imports %}`, and top-level `{% from %}` from the full `{% extends %}` chain before the block body (same as Chirp's fragment pipeline). You should not need to duplicate imports for every fragment unless a template is used standalone without extending that chain.

## View transitions

Chirp injects the root-level `@view-transition` rule and meta tag when `AppConfig(view_transitions=True)` (default). `chirpui-transitions.css` scopes transitions to `#main` (via `view-transition-name: page-content`), suppresses root animations so the shell stays frozen, and disables VT on `.chirpui-fragment-island` elements. No custom VT CSS is needed for the common app shell case. With `view_transitions=False`, full-page swaps will not use the View Transitions API.

## Explicit Kida end tags

For deeply nested templates, prefer `{% endif %}`, `{% endcall %}`, `{% endfor %}`, `{% endblock %}`, and `{% enddef %}` over bare `{% end %}` so reviewers can match open/close pairs quickly. See the Kida README and `kida check` for CI-friendly parsing.
