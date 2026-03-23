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

Primary actions use `chirpui/button.html` (`btn`). Specialized buttons live in dedicated templates.

| Template | Macro | Notes |
|----------|-------|--------|
| `button.html` | `btn` | Variants: see `VARIANT_REGISTRY["btn"]`; sizes: `SIZE_REGISTRY["btn"]` |
| `icon_btn.html` | `icon_btn` | Icon-only; size registry `icon-btn` |
| `shimmer_button.html` | `shimmer_button` | Loading / emphasis |
| `ripple_button.html` | `ripple_button` | Ripple feedback |
| `pulsing_button.html` | `pulsing_button` | Attention / CTA pulse |
| `split_button.html` | `split_button` | Primary + dropdown affordance |
| `copy_button.html` | `copy_button` | Clipboard helper |

## Usage

```text
{% from "chirpui/button.html" import btn %}
{{ btn("Save", type="submit", variant="primary") }}
```

Prefer **`html_attrs`** for `data-*` and `hx-*` attributes — see [Filters](../reference/filters.md).

## CSS

`chirpui-btn`, `chirpui-btn--*`, `chirpui-icon-btn`, `chirpui-shimmer-btn`, etc.

## Related

- [Forms](./forms.md) — `form_actions`, submit wiring
- [Modals](./modals-and-drawers.md) — confirm flows
