# Composition patterns

ChirpUI components are Kida macros: `{% call %}`, `{% slot %}`, and `{% def %}`. These patterns work well in practice; the main pitfalls are conditional wrappers and duplicate imports when mixing full pages with HTMX fragments.

## Primitive vocabulary

Prefer ChirpUI's composition primitives over helper-class chains. Reach first for `stack()`, `cluster()`, `grid()`, `frame()`, `block()`, `layer()`, `container()`, `flow`, `actions`, and `prose`; keep legacy helpers like `chirpui-mt-md`, `chirpui-font-sm`, and `chirpui-text-muted` for compatibility or narrow containment cases.

The full guide lives in [PRIMITIVES.md](primitives.md).

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

## Kida block inheritance — override-only (no `super()`)

Chirp's Jinja layout docs sometimes show child blocks that call `{{ super() }}` to prepend or append parent markup. **Kida 0.9.x does not implement `super` / `super()`.** Both resolve as undefined variables and fail at render time with a misleading stack trace.

Kida's model is **full block override**: a child `{% block head_extra %}…{% end %}` replaces the parent's block body entirely. To reuse shared markup, extract a partial and `{% include %}` it from each block that needs the same head/body chrome:

```kida
{% block head_extra %}
{% include "partials/shared_head_styles.html" %}
{% include "pages/my_page.css.html" %}
{% end %}
```

The component showcase uses this pattern in `examples/component-showcase/templates/showcase/_showcase_head_styles.html` (included from `base.html` and shell recipe pages). CI ratchets forbid `super()` in templates: `tests/test_kida_template_contracts.py`.

**Fragment routes:** when a handler returns `Fragment("partial.html", "block_name", …)`, the partial must define `{% block block_name %}…{% end %}`. The same static scan enforces that contract for showcase routes.

See also the [showcase add-a-page checklist](https://github.com/lbliii/chirp-ui/blob/main/examples/component-showcase/README.md#add-a-showcase-page).

## View transitions

Chirp injects the root-level `@view-transition` rule and meta tag when `AppConfig(view_transitions=True)` (default). `chirpui-transitions.css` scopes transitions to the direct shell main boundary (`body > #main` for `app_layout.html`, or `body > .chirpui-app-shell > #main` for `app_shell_layout.html`) via `view-transition-name: page-content`, suppresses root animations so the shell stays frozen, and disables VT on `.chirpui-fragment-island` elements. No custom VT CSS is needed for the common app shell case. With `view_transitions=False`, full-page swaps will not use the View Transitions API.

## Explicit Kida end tags

For deeply nested templates, prefer `{% endif %}`, `{% endcall %}`, `{% endfor %}`, `{% endblock %}`, and `{% enddef %}` over bare `{% end %}` so reviewers can match open/close pairs quickly. See the Kida README and `kida check` for CI-friendly parsing.
