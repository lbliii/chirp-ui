---
name: chirpui-component
description: |
  Author a new chirp-ui component end-to-end: Kida macro template, BEM CSS,
  VARIANT_REGISTRY/SIZE_REGISTRY entries, render tests, and CI verification.
  Enforces chirpui conventions (BEM classes, slot-based macros, no <script> tags,
  | safe only on html_attrs/Markup output, motion tokens for animation).
tags:
  - chirpui
  - component
  - template
  - css
  - kida
triggers:
  - "::chirpui-component"
  - "::cc"
  - "add chirpui component"
  - "new chirpui component"
  - "create chirpui component"
inputs:
  - name: "Component name (kebab-case, e.g. stat-card)"
  - variants: "Optional — comma-separated variant names"
  - sizes: "Optional — comma-separated size names"
outputs:
  - template: "src/chirp_ui/templates/chirpui/<name>.html"
  - css: "section added to chirpui.css"
  - registry: "VARIANT_REGISTRY / SIZE_REGISTRY entries in validation.py"
  - tests: "test cases added to tests/test_components.py"
---

# chirpui Component Authoring

Add a new component to chirp-ui following all project conventions.

## Checklist

Work through these five steps in order. Do not skip any.

1. **Template** — `src/chirp_ui/templates/chirpui/<name>.html`
2. **CSS** — section in `src/chirp_ui/templates/chirpui.css`
3. **Registry** — `VARIANT_REGISTRY` / `SIZE_REGISTRY` in `validation.py`
4. **Tests** — render tests in `tests/test_components.py`
5. **CI** — run `uv run poe ci` and fix any failures

---

## Step 1: Template (Kida Macro)

Use `{% macro %}` / `{% call %}` pairs. Inject content with `{% slot %}`. Never use
wrapper divs without a reason. No `<script>` tags — Alpine.js `x-data` attributes only.

```jinja
{# src/chirp_ui/templates/chirpui/<name>.html #}
{% macro <name>(variant="", size="", cls="", attrs=None) %}
  {% set _variant = variant | validate_variant_block("<name>") %}
  {% set _size    = size    | validate_size("<name>") %}
  <div class="{{ "<name>" | bem(variant=_variant, cls=cls) }}"
       {{ attrs | html_attrs | safe }}>
    {% slot %}{% endslot %}
  </div>
{% endmacro %}
```

### Template rules
- **BEM classes** — use `| bem(variant=..., modifier=..., cls=...)` for all class attributes.
- **`| safe` usage** — only on outputs already escaped by `html_attrs` or `Markup`. Never on raw user input.
- **Variants/sizes** — always run through `validate_variant_block` / `validate_size` filters.
- **No hardcoded strings** — use filters, not f-strings in templates.
- **Icons** — use `{{ name | icon }}` filter, never raw Unicode literals.

---

## Step 2: CSS

Add a clearly delimited section to `chirpui.css`. Every class referenced in the
template must exist here (enforced by `test_template_css_contract.py`).

```css
/* <name> */
.chirpui-<name> {
  /* base styles */
}

.chirpui-<name>--<variant> {
  /* variant styles */
}
```

### CSS rules
- **Token-only animation** — use `--chirpui-duration-*` and `--chirpui-easing-*` tokens,
  never raw `200ms` or `ease-in-out` (enforced by `test_transition_tokens.py`).
- **Color mix** — prefer `color-mix()` and `--chirpui-*` color tokens over raw hex.
- **No hardcoded durations or easings** anywhere in the section.
- **Container queries** over media queries where the component is embedded.

---

## Step 3: Registry

Add to `src/chirp_ui/validation.py`:

```python
VARIANT_REGISTRY: dict[str, tuple[str, ...]] = {
    ...
    "<name>": ("<default>", "<variant-2>", ...),  # add here
}

SIZE_REGISTRY: dict[str, tuple[str, ...]] = {
    ...
    "<name>": ("", "sm", "md", "lg"),  # only if component has sizes
}
```

The first tuple entry is the fallback when an invalid variant is passed.

---

## Step 4: Tests

Add to `tests/test_components.py` using the `env` fixture (no Chirp app required):

```python
def test_<name>_renders(env):
    tmpl = env.get_template("chirpui/<name>.html")
    # default render
    html = tmpl.module.<name>()
    assert "chirpui-<name>" in html

def test_<name>_variant(env):
    tmpl = env.get_template("chirpui/<name>.html")
    html = tmpl.module.<name>(variant="<variant>")
    assert "chirpui-<name>--<variant>" in html

def test_<name>_invalid_variant_falls_back(env):
    tmpl = env.get_template("chirpui/<name>.html")
    html = tmpl.module.<name>(variant="bogus")
    assert "chirpui-<name>" in html
    assert "bogus" not in html
```

---

## Step 5: CI

```bash
uv run poe ci
```

Fix failures before opening a PR. Common failures:
- `test_template_css_contract` — a class in the template has no CSS rule.
- `test_transition_tokens` — hardcoded duration/easing in the new CSS section.
- `ruff` — import order or formatting issue.

---

## Accessibility baseline by component type

| Type | Required |
|------|----------|
| Interactive (button, link) | `role`, keyboard handler, visible focus ring |
| Form element | `<label for>` or `aria-label`, error association |
| Modal / overlay | `role="dialog"`, `aria-modal`, focus trap, Escape closes |
| Alert / toast | `role="alert"` or `aria-live="polite"` |
| Icon-only | `aria-label` on the parent control |
| List / nav | `<nav>` or `role="list"` as appropriate |

---

## State × Variant table (fill in before writing CSS)

| State | Base | `--<variant>` |
|-------|------|---------------|
| Default | | |
| Hover | | |
| Active | | |
| Disabled | | |
| Focus-visible | outline per token | outline per token |

---

## DORI Lifecycle

After routing to this skill:
- `dori_begin(skill="chirpui-component")`
- `dori_update(...)` as you complete each step
- `dori_complete(files_modified="...", files_created="...")`
