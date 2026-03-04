# chirp-ui Component Options Reference

Valid variant, size, and option values for chirp-ui components. When **strict mode** is enabled (e.g. `app.debug=True` with Chirp's `use_chirp_ui`), invalid values log warnings and fall back to defaults.

See [Strict mode](#strict-mode) for setup.

---

## Macro Slot Context

Components that use `{% slot %}` (e.g. `form`, `card`, `card_link`, `field_wrapper`) render slot content in the **caller's context**. Page variables passed to the handler (e.g. `selected_tags`, `q`) are available inside macro slots without `| default()`.

```html
{% call form("/search", method="get") %}
  {{ search_field("q", value=q, placeholder="Search...") }}
  {% if selected_tags %}
    {{ hidden_field("tags", value=selected_tags | join(",")) }}
  {% end %}
{% end %}
```

Use `| default()` for optional variables that may be unset on first load (e.g. `selected_tags | default([])` when the handler may omit the key). Variables used inside macro slots must be in the page context — Chirp passes handler context through to `render_block()`.

---

## Components with Variants

| Component | Param | Valid values | Default |
|-----------|-------|--------------|---------|
| **alert** | `variant` | info, success, warning, error | info |
| **badge** | `variant` | primary, success, warning, error, muted, info | — |
| **surface** | `variant` | default, muted, elevated, accent, glass, frosted, smoke | default |
| **toast** | `variant` | info, success, warning, error | info |
| **hero** | `background` | solid, muted, gradient | solid |
| **page_hero** | `variant` | editorial, minimal | editorial |
| **page_hero** | `background` | solid, muted, gradient | solid |
| **description_list** | `variant` | stacked, horizontal | stacked |
| **skeleton** | `variant` | *(empty)*, avatar, text, card | *(empty)* |
| **confirm** | `variant` | default, danger | default |
| **overlay** | `variant` | dark, gradient-bottom, gradient-top | dark |
| **progress_bar** | `variant` | gold, radiant, success, watched | gold |
| **progress_bar** | `size` | sm, md, lg | md |
| **btn** | `variant` | *(empty)*, default, primary, ghost, danger, success, warning | *(empty)* |

---

## Usage Notes

### BEM-based components (alert, badge)

These use the `bem` filter internally. Pass `variant` directly; validation runs automatically when strict mode is on.

```html
{% from "chirpui/alert.html" import alert %}
{% call alert(variant="success") %}Saved.{% end %}
```

### Inline-variant components (surface, hero, toast, etc.)

These use `validate_variant` at macro top. Invalid values fall back to the default and log a warning in strict mode.

```html
{% from "chirpui/surface.html" import surface %}
{% call surface(variant="muted") %}...{% end %}

{% from "chirpui/toast.html" import toast %}
{{ toast("Done!", variant="success") }}
```

### Skeleton variant

Use `""` (empty) for the default block, or `avatar`, `text`, `card` for structured placeholders.

```html
{% from "chirpui/skeleton.html" import skeleton %}
{{ skeleton() }}
{{ skeleton(variant="avatar") }}
{{ skeleton(variant="text", lines=3) }}
```

### Progress bar

Both `variant` (color style) and `size` are validated.

```html
{% from "chirpui/progress.html" import progress_bar %}
{{ progress_bar(75, variant="gold", size="md") }}
```

---

## Strict Mode

**With Chirp:** Strict mode follows `app.debug` by default. Override with `strict=True` or `strict=False`:

```python
from chirp import App, use_chirp_ui
import chirp_ui

app = App(...)
use_chirp_ui(app, prefix="/static", strict=True)   # always validate
use_chirp_ui(app, prefix="/static", strict=False)  # never validate
use_chirp_ui(app, prefix="/static")                # strict=app.debug (from chirp)
```

**Standalone (Kida only):** Call `chirp_ui.set_strict(True)` before rendering:

```python
import chirp_ui
chirp_ui.set_strict(True)
# ... render templates
```

---

## Filters

- **`bem(block, variant="", modifier="", cls="")`** — Builds BEM class string; validates `variant` against `VARIANT_REGISTRY` when strict.
- **`validate_variant(value, allowed, default="")`** — Returns `value` if in `allowed`, else `default`. Logs warning when strict and invalid.

For custom components with inline variants:

```jinja2
{% set variant = variant | validate_variant(("a","b","c"), "a") %}
```
