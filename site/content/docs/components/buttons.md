---
title: Buttons
description: btn, icon_btn, shimmer, ripple, pulsing, split, copy
draft: false
weight: 13
lang: en
type: doc
keywords: [chirp-ui, button, btn]
icon: cursor-click
---

# Buttons

Primary actions use `chirpui/button.html` (`btn`). Specialized buttons live in dedicated templates for loading states, clipboard, ripple feedback, and more. Links use `chirpui/link.html`.

## Quick reference

| Template | Macro | Description |
|----------|-------|-------------|
| `button.html` | `btn` | Button with variants, supports loading state for htmx |
| `button.html` | `button_group` | Container for grouping buttons |
| `icon_btn.html` | `icon_btn` | Square icon-only button for toolbars |
| `split_button.html` | `split_button` | Primary action with dropdown |
| `pulsing_button.html` | `pulsing_button` | CTA pulse effect |
| `ripple_button.html` | `ripple_button` | Material-style ripple (Alpine.js) |
| `shimmer_button.html` | `shimmer_button` | Animated shimmer overlay |
| `copy_button.html` | `copy_button` | Clipboard helper (Alpine.js) |
| `link.html` | `link` | Styled link |

---

## button.html

### btn

```text
{% from "chirpui/button.html" import btn %}
{{ btn("Save", variant="primary", type="submit") }}
```

**Signature:**

```text
btn(label, variant="", size=none, loading=false, type="submit", href=none,
    icon=none, cls="", attrs="", attrs_map=none,
    hx_get=none, hx_post=none, hx_put=none, hx_patch=none, hx_delete=none,
    hx_target=none, hx_swap=none, hx_trigger=none, hx_include=none,
    hx_select=none, hx_ext=none, hx_vals=none,
    disabled=false, data_action=none, aria_label=none)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | string | required | Button text |
| `variant` | string | `""` | Visual variant (validated against `VARIANT_REGISTRY["btn"]`) |
| `size` | string | `none` | Size token (validated against `SIZE_REGISTRY["btn"]`) |
| `loading` | bool | `false` | Show spinner; pairs with htmx `hx-indicator` |
| `type` | string | `"submit"` | HTML `type` attribute |
| `href` | string | `none` | If set, renders an `<a>` instead of `<button>` |
| `icon` | string | `none` | Icon name prepended to label |
| `cls` | string | `""` | Extra CSS classes |
| `attrs` | string | `""` | Raw attribute string (use `html_attrs` filter) |
| `attrs_map` | dict | `none` | Attribute dict merged via `html_attrs` |
| `disabled` | bool | `false` | Disables the button |
| `hx_get` ... `hx_vals` | string | `none` | htmx attributes passed through directly |
| `data_action` | string | `none` | `data-action` attribute |
| `aria_label` | string | `none` | Accessible label override |

**Examples:**

```text
{# Link-style button #}
{{ btn("View docs", href="/docs", variant="ghost") }}

{# htmx submit with loading spinner #}
{{ btn("Submit", variant="primary", loading=true,
       hx_post="/api/save", hx_target="#result", hx_swap="innerHTML") }}

{# Button with icon #}
{{ btn("Delete", variant="danger", icon="trash") }}
```

### button_group

```text
{% from "chirpui/button.html" import btn, button_group %}
{% call button_group() %}
  {{ btn("Cancel", variant="ghost") }}
  {{ btn("Save", variant="primary", type="submit") }}
{% endcall %}
```

**Signature:**

```text
button_group(cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cls` | string | `""` | Extra CSS classes on the group container |

---

## icon_btn.html

```text
{% from "chirpui/icon_btn.html" import icon_btn %}
{{ icon_btn("pencil", aria_label="Edit item") }}
```

**Signature:**

```text
icon_btn(icon, variant="", size="", href=none, aria_label="",
         disabled=false, type="button", cls="",
         hx_get=none, hx_post=none, hx_target=none, hx_swap=none)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `icon` | string | required | Icon name |
| `variant` | string | `""` | Visual variant |
| `size` | string | `""` | Size token (validated against `SIZE_REGISTRY["icon-btn"]`) |
| `href` | string | `none` | If set, renders as `<a>` |
| `aria_label` | string | `""` | Required for accessibility (no visible text) |
| `disabled` | bool | `false` | Disables the button |
| `type` | string | `"button"` | HTML `type` attribute |
| `cls` | string | `""` | Extra CSS classes |
| `hx_get`, `hx_post` | string | `none` | htmx request attributes |
| `hx_target`, `hx_swap` | string | `none` | htmx response handling |

**Examples:**

```text
{# Toolbar icon button #}
{{ icon_btn("trash", variant="danger", aria_label="Delete") }}

{# Icon link #}
{{ icon_btn("external-link", href="/settings", aria_label="Settings") }}
```

---

## split_button.html

```text
{% from "chirpui/split_button.html" import split_button %}
{% call split_button("Save", primary_submit=true, variant="primary") %}
  <button type="button">Save as draft</button>
  <button type="button">Save and close</button>
{% endcall %}
```

**Signature:**

```text
split_button(primary_label, primary_href=none, primary_submit=false,
             variant="primary", cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `primary_label` | string | required | Text for the primary action |
| `primary_href` | string | `none` | Link for the primary action |
| `primary_submit` | bool | `false` | If true, primary is a submit button |
| `variant` | string | `"primary"` | Visual variant applied to both parts |
| `cls` | string | `""` | Extra CSS classes |

The dropdown content is provided via `{% call %}` / `{% slot %}`.

---

## pulsing_button.html

```text
{% from "chirpui/pulsing_button.html" import pulsing_button %}
{{ pulsing_button("Get started", variant="primary", icon="arrow-right") }}
```

**Signature:**

```text
pulsing_button(text, variant="", icon=none, href=none, cls="",
               type="button", disabled=false)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | required | Button text |
| `variant` | string | `""` | Visual variant |
| `icon` | string | `none` | Optional icon |
| `href` | string | `none` | If set, renders as `<a>` |
| `cls` | string | `""` | Extra CSS classes |
| `type` | string | `"button"` | HTML `type` attribute |
| `disabled` | bool | `false` | Disables the button |

---

## ripple_button.html

Requires Alpine.js (injected by Chirp).

```text
{% from "chirpui/ripple_button.html" import ripple_button %}
{{ ripple_button("Click me", variant="primary") }}
```

**Signature:**

```text
ripple_button(text, variant="", size="", icon=none, cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | required | Button text |
| `variant` | string | `""` | Visual variant |
| `size` | string | `""` | Size token |
| `icon` | string | `none` | Optional icon |
| `cls` | string | `""` | Extra CSS classes |

---

## shimmer_button.html

```text
{% from "chirpui/shimmer_button.html" import shimmer_button %}
{{ shimmer_button("Upgrade", variant="primary", icon="sparkles") }}
```

**Signature:**

```text
shimmer_button(text, variant="", size="", icon=none, href=none, cls="",
               type="button", attrs="", attrs_map=none, disabled=false)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | required | Button text |
| `variant` | string | `""` | Visual variant |
| `size` | string | `""` | Size token |
| `icon` | string | `none` | Optional icon |
| `href` | string | `none` | If set, renders as `<a>` |
| `cls` | string | `""` | Extra CSS classes |
| `type` | string | `"button"` | HTML `type` attribute |
| `attrs` | string | `""` | Raw attribute string |
| `attrs_map` | dict | `none` | Attribute dict merged via `html_attrs` |
| `disabled` | bool | `false` | Disables the button |

---

## copy_button.html

Requires Alpine.js (injected by Chirp).

```text
{% from "chirpui/copy_button.html" import copy_button %}
{{ copy_button("pip install chirp-ui", label="Copy command") }}
```

**Signature:**

```text
copy_button(text, label="Copy")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | required | Text copied to clipboard on click |
| `label` | string | `"Copy"` | Visible button label |

---

## link.html

```text
{% from "chirpui/link.html" import link %}
{{ link("Documentation", "/docs") }}
{{ link("GitHub", "https://github.com/lbliii/chirp-ui", external=true) }}
```

**Signature:**

```text
link(text, href, external=false, cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | required | Link text |
| `href` | string | required | URL |
| `external` | bool | `false` | Adds `target="_blank"` and `rel="noopener"` |
| `cls` | string | `""` | Extra CSS classes |

---

## CSS classes

| Class | Element |
|-------|---------|
| `chirpui-btn` | Base button |
| `chirpui-btn--{variant}` | Variant modifier (e.g. `chirpui-btn--primary`) |
| `chirpui-btn--{size}` | Size modifier |
| `chirpui-btn-group` | Button group container |
| `chirpui-icon-btn` | Icon-only button |
| `chirpui-icon-btn--{variant}` | Icon button variant |
| `chirpui-split-btn` | Split button wrapper |
| `chirpui-pulsing-btn` | Pulsing button |
| `chirpui-ripple-btn` | Ripple button |
| `chirpui-shimmer-btn` | Shimmer button |
| `chirpui-copy-btn` | Copy button |
| `chirpui-link` | Styled link |

All classes follow the BEM convention `chirpui-<block>--<modifier>`.

## Related

- [Forms](./forms.md) — `form_actions`, submit wiring
- [Modals](./modals-and-drawers.md) — confirm flows
- [Filters](../reference/filters.md) — `html_attrs`, `validate_variant`, `validate_size`
- [Action strip](./action-strip.md) — toolbar button layouts
