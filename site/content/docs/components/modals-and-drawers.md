---
title: Modals and drawers
description: modal, drawer, tray, confirm, popover, tooltip
draft: false
weight: 14
lang: en
type: doc
keywords: [chirp-ui, modal, drawer, tray]
icon: bounding-box
---

# Modals and drawers

Overlay UI for focused tasks, transient panels, and contextual information. Native `<dialog>` modals and drawers use `closedby="any"` for light-dismiss. Alpine.js-driven overlays (tray, modal overlay, dropdown menu) use `Alpine.store` for open/close state. Pure CSS components (popover, dropdown, tooltip) need no JavaScript at all.

## Quick reference

| Template | Macro | Description |
|----------|-------|-------------|
| `modal.html` | `modal` | Native `<dialog>` modal, centered |
| `modal.html` | `modal_trigger` | Button to open a modal |
| `modal_overlay.html` | `modal_overlay` | Div-based overlay modal (Alpine.js) |
| `modal_overlay.html` | `modal_overlay_trigger` | Button to open an overlay modal |
| `drawer.html` | `drawer` | Slide-out panel from left or right (native `<dialog>`) |
| `drawer.html` | `drawer_trigger` | Button to open a drawer |
| `tray.html` | `tray` | Slide-out panel (Alpine.js, with backdrop and focus trap) |
| `tray.html` | `tray_trigger` | Button to open a tray |
| `popover.html` | `popover` | Floating panel (`<details>`/`<summary>`) |
| `tooltip.html` | `tooltip` | Hover tooltip, pure CSS |
| `dropdown.html` | `dropdown` | Native `<details>`/`<summary>` dropdown |
| `dropdown_menu.html` | `dropdown_menu` | Items-based dropdown (Alpine.js) |
| `dropdown_menu.html` | `dropdown_select` | Select-style dropdown (Alpine.js) |
| `dropdown_menu.html` | `dropdown_split` | Split button with dropdown (Alpine.js) |
| `overlay.html` | `overlay` | Gradient/dark layer for text readability on images |
| `confirm.html` | `confirm_dialog` | Confirmation modal for destructive actions |
| `confirm.html` | `confirm_trigger` | Button to open a confirm dialog |

## Sizes

`modal` uses `SIZE_REGISTRY["modal"]`: `small`, `medium`, `large`.

---

## modal.html

### modal

Native `<dialog>` modal centered in the viewport. Supports named slots for `header_actions` and `footer`.

```text
{% from "chirpui/modal.html" import modal, modal_trigger %}

{{ modal_trigger("settings-dlg", label="Settings") }}

{% call modal("settings-dlg", title="Settings", size="medium") %}
    <p>Modal body content.</p>
    {% fill footer %}
        <button class="chirpui-btn chirpui-btn--ghost"
                onclick="this.closest('dialog').close()">Cancel</button>
        <button class="chirpui-btn chirpui-btn--primary">Save</button>
    {% end %}
{% endcall %}
```

**Signature:**

```text
modal(id, title=none, size="medium", cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | string | required | Dialog element `id`; matched by `modal_trigger` |
| `title` | string | `none` | Header title; omit for a headerless modal |
| `size` | string | `"medium"` | Validated against `SIZE_REGISTRY["modal"]` (`small`, `medium`, `large`) |
| `cls` | string | `""` | Extra CSS classes |

**Slots:** default (body), `header_actions`, `footer`.

### modal_trigger

```text
modal_trigger(target, label="Open", cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `target` | string | required | `id` of the dialog to open |
| `label` | string | `"Open"` | Button text |
| `cls` | string | `""` | Extra CSS classes |

Uses Alpine `@click` to call `showModal()` on the target dialog.

---

## modal_overlay.html

Div-based overlay for apps that prefer Alpine.js state management over native `<dialog>`. Requires `Alpine.store('modals')`.

### modal_overlay_trigger

```text
{% from "chirpui/modal_overlay.html" import modal_overlay, modal_overlay_trigger %}

{{ modal_overlay_trigger("confirm", "Delete", variant="danger") }}
```

**Signature:**

```text
modal_overlay_trigger(id, label, variant="default", icon=none)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | string | required | Store key for `$store.modals[id]` |
| `label` | string | required | Button text |
| `variant` | string | `"default"` | Button variant (applied to `chirpui-btn`) |
| `icon` | string | `none` | Optional icon prepended to label |

### modal_overlay

```text
{% call modal_overlay("confirm", "Confirm delete") %}
    <p>Are you sure?</p>
{% endcall %}
```

**Signature:**

```text
modal_overlay(id, title)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | string | required | Store key; element rendered as `modal-{id}` |
| `title` | string | required | Header title |

Includes backdrop click-to-close, focus trap via `x-trap.inert.noscroll`, and dispatches `chirpui:modal-closed` on close.

---

## drawer.html

Slide-out panel using native `<dialog>`. Slides from the left or right edge.

```text
{% from "chirpui/drawer.html" import drawer, drawer_trigger %}

{{ drawer_trigger("filters", label="Open filters") }}

{% call drawer("filters", title="Filters", side="right") %}
    <form>...</form>
{% endcall %}
```

### drawer

**Signature:**

```text
drawer(id, title=none, side="right", cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | string | required | Dialog element `id` |
| `title` | string | `none` | Header title; omit for headerless |
| `side` | string | `"right"` | `"left"` or `"right"` |
| `cls` | string | `""` | Extra CSS classes |

**Slots:** default (body), `header_actions`.

### drawer_trigger

```text
drawer_trigger(target, label="Open", cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `target` | string | required | `id` of the drawer dialog |
| `label` | string | `"Open"` | Button text |
| `cls` | string | `""` | Extra CSS classes |

---

## tray.html

Alpine.js-driven slide-out panel with backdrop and focus trap. Requires `Alpine.store('trays')`.

```text
{% from "chirpui/tray.html" import tray, tray_trigger %}

{{ tray_trigger("filters", "Filters", icon="gear") }}

{% call tray("filters", "Filters", position="right") %}
    <form>...</form>
{% endcall %}
```

### tray_trigger

**Signature:**

```text
tray_trigger(id, label, icon=none)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | string | required | Store key for `$store.trays[id]` |
| `label` | string | required | Button text |
| `icon` | string | `none` | Icon name (passed through `icon` filter) |

### tray

**Signature:**

```text
tray(id, title, position="right")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | string | required | Store key; element rendered as `tray-{id}` |
| `title` | string | required | Header title |
| `position` | string | `"right"` | `"left"` or `"right"` |

Dispatches `chirpui:tray-closed` on close. Uses `x-trap.inert.noscroll` for focus management.

---

## popover.html

Floating panel built on `<details>`/`<summary>`. No JavaScript required.

```text
{% from "chirpui/popover.html" import popover %}

{% call popover(trigger_label="Filters") %}
    {% fill header %}<h3>Filters</h3>{% end %}
    <form>...</form>
    {% fill footer %}<button>Apply</button>{% end %}
{% endcall %}
```

**Signature:**

```text
popover(trigger_label, cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `trigger_label` | string | required | Text shown on the summary trigger |
| `cls` | string | `""` | Extra CSS classes |

**Slots:** default (panel body), `header`, `footer`.

---

## tooltip.html

Pure CSS tooltip shown on hover. Wraps child content in a `<span>` with a tooltip bubble.

```text
{% from "chirpui/tooltip.html" import tooltip %}

{% call tooltip("Copy to clipboard") %}
    <button>Copy</button>
{% endcall %}

{% call tooltip("Below the element", position="bottom") %}
    <span>Hover me</span>
{% endcall %}
```

**Signature:**

```text
tooltip(content=none, hint=none, position="top", cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `content` | string | `none` | Tooltip text (used if `hint` is not set) |
| `hint` | string | `none` | Alias for tooltip text; takes precedence over `content` |
| `position` | string | `"top"` | `"top"`, `"bottom"`, `"left"`, or `"right"` |
| `cls` | string | `""` | Extra CSS classes |

---

## dropdown.html

Native `<details>`/`<summary>` dropdown menu. No JavaScript required.

```text
{% from "chirpui/dropdown.html" import dropdown %}

{% call dropdown(label="Options") %}
    {% fill header %}<div class="chirpui-dropdown__header">Signed in as alice</div>{% end %}
    <a href="/settings">Settings</a>
    <a href="/profile">Profile</a>
    {% fill footer %}<a href="/logout">Log out</a>{% end %}
{% endcall %}
```

**Signature:**

```text
dropdown(label, cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | string | required | Trigger text |
| `cls` | string | `""` | Extra CSS classes |

**Slots:** default (menu items), `header`, `footer`.

---

## dropdown_menu.html

Items-based dropdowns powered by Alpine.js. Three macros for different use cases.

### dropdown_menu

Action menu driven by an items list. Each item is a dict with keys: `label`, `href` (link), `action` (button), `variant`, `icon`, `divider` (separator).

```text
{% from "chirpui/dropdown_menu.html" import dropdown_menu %}
{% from "chirpui/button.html" import btn %}

{{ dropdown_menu(
    btn("Actions", icon="chevron-down"),
    items=[
        {"label": "Edit", "href": "/edit"},
        {"label": "Duplicate", "action": "duplicate"},
        {"divider": true},
        {"label": "Delete", "action": "delete", "variant": "danger", "icon": "trash"}
    ]
) }}
```

**Signature:**

```text
dropdown_menu(trigger, items, id="chirpui-dropdown")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `trigger` | string/markup | required | Rendered trigger element (e.g. a `btn()` call) |
| `items` | list[dict] | required | Menu items |
| `id` | string | `"chirpui-dropdown"` | Container `id` |

**Item keys:** `label`, `href`, `action`, `variant` (validated), `icon`, `divider` (bool).

Dispatches `chirpui:dropdown-selected` with `{label, href|action}` on selection.

### dropdown_select

Select-style single-value picker with keyboard navigation.

```text
{% from "chirpui/dropdown_menu.html" import dropdown_select %}

{{ dropdown_select(
    "Sort by",
    items=[
        {"label": "Newest first", "value": "newest"},
        {"label": "Oldest first", "value": "oldest"},
        {"label": "Name A-Z", "value": "name"}
    ],
    selected="newest"
) }}
```

**Signature:**

```text
dropdown_select(trigger_label, items, selected=none, id="chirpui-dropdown-select")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `trigger_label` | string | required | Visible label (shown before first selection) |
| `items` | list[dict] | required | Options; each dict has `label`, optional `value` and `icon` |
| `selected` | string | `none` | Pre-selected value; defaults to first item |
| `id` | string | `"chirpui-dropdown-select"` | Container `id` |

Supports `ArrowUp`/`ArrowDown`/`Enter` keyboard navigation. Dispatches `chirpui:dropdown-selected`.

### dropdown_split

Split button: primary action on the left, dropdown menu on the right.

```text
{% from "chirpui/dropdown_menu.html" import dropdown_split %}

{{ dropdown_split(
    "Save",
    primary_href="/save",
    items=[
        {"label": "Save as draft", "action": "save-draft"},
        {"label": "Save and close", "action": "save-close"}
    ],
    icon="check"
) }}
```

**Signature:**

```text
dropdown_split(primary_label, primary_href=none, primary_action=none,
               items=[], icon=none)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `primary_label` | string | required | Primary button text |
| `primary_href` | string | `none` | If set, primary is an `<a>` link |
| `primary_action` | string | `none` | If set, primary is a `<button>` with `data-action` |
| `items` | list[dict] | `[]` | Dropdown items (same format as `dropdown_menu`) |
| `icon` | string | `none` | Icon for the primary button |

---

## overlay.html

Gradient or dark layer placed over an image so overlaid text stays readable. Place as a sibling inside a `position: relative` parent.

```text
{% from "chirpui/overlay.html" import overlay %}

<div style="position: relative;">
    <img src="hero.jpg" alt="...">
    {{ overlay("gradient-bottom") }}
    <div style="position: absolute; inset: 0; display: flex; align-items: flex-end; padding: 1rem;">
        <h2>Text on image</h2>
    </div>
</div>
```

**Signature:**

```text
overlay(variant="dark", cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `variant` | string | `"dark"` | `"dark"`, `"gradient-bottom"`, or `"gradient-top"` |
| `cls` | string | `""` | Extra CSS classes |

---

## confirm.html

Confirmation modal for destructive or high-friction actions. Built on native `<dialog>`, supports htmx submission.

```text
{% from "chirpui/confirm.html" import confirm_dialog, confirm_trigger %}

{{ confirm_trigger("del-dlg", label="Delete") }}

{% call confirm_dialog("del-dlg", title="Delete item?",
                       message="This cannot be undone.",
                       confirm_label="Delete", variant="danger",
                       confirm_url="/items/1/delete", confirm_method="POST") %}
{% endcall %}
```

### confirm_dialog

**Signature:**

```text
confirm_dialog(id, title, message=none, confirm_label="Confirm",
               cancel_label="Cancel", variant="default",
               confirm_url=none, confirm_method="POST",
               hx_target=none, hx_swap="innerHTML",
               hx_select=none, hx_push_url=none, cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | string | required | Dialog element `id` |
| `title` | string | required | Header title (danger variant prepends a warning icon) |
| `message` | string | `none` | Body text; if omitted, use the `message` slot instead |
| `confirm_label` | string | `"Confirm"` | Confirm button text |
| `cancel_label` | string | `"Cancel"` | Cancel button text |
| `variant` | string | `"default"` | `"default"` or `"danger"` |
| `confirm_url` | string | `none` | Form action URL; if set, confirm submits a form |
| `confirm_method` | string | `"POST"` | HTTP method for the confirm form |
| `hx_target` | string | `none` | htmx target selector (enables htmx mode) |
| `hx_swap` | string | `"innerHTML"` | htmx swap strategy |
| `hx_select` | string | `none` | htmx select filter |
| `hx_push_url` | string | `none` | htmx URL push |
| `cls` | string | `""` | Extra CSS classes |

**Slots:** `header_actions`, `message` (when `message` param is omitted), `form_content` (extra hidden inputs before the confirm button).

When `hx_target` is provided, the confirm form uses htmx attributes (`hx-post` or `hx-delete` based on method) with `hx-disinherit` set automatically.

### confirm_trigger

```text
confirm_trigger(target, label="Confirm", cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `target` | string | required | `id` of the confirm dialog |
| `label` | string | `"Confirm"` | Button text |
| `cls` | string | `""` | Extra CSS classes |

---

## CSS classes

| Class | Element |
|-------|---------|
| `chirpui-modal` | Modal dialog |
| `chirpui-modal--{size}` | Size modifier (`small`, `medium`, `large`) |
| `chirpui-modal__header` | Modal header |
| `chirpui-modal__body` | Modal body |
| `chirpui-modal__footer` | Modal footer |
| `chirpui-modal-trigger` | Modal trigger button |
| `chirpui-drawer` | Drawer dialog |
| `chirpui-drawer--{side}` | Side modifier (`left`, `right`) |
| `chirpui-tray` | Tray container |
| `chirpui-tray--{position}` | Position modifier |
| `chirpui-tray--open` / `chirpui-tray--closed` | State modifiers |
| `chirpui-popover` | Popover container |
| `chirpui-tooltip` | Tooltip wrapper |
| `chirpui-tooltip--{position}` | Position modifier (`top`, `bottom`, `left`, `right`) |
| `chirpui-dropdown` | Dropdown container |
| `chirpui-dropdown--select` | Select-style modifier |
| `chirpui-dropdown--split` | Split button modifier |
| `chirpui-dropdown__menu` | Dropdown menu panel |
| `chirpui-dropdown__item` | Menu item |
| `chirpui-overlay` | Overlay layer |
| `chirpui-overlay--{variant}` | Variant modifier (`dark`, `gradient-bottom`, `gradient-top`) |
| `chirpui-confirm` | Confirm dialog modifier |
| `chirpui-confirm--danger` | Danger variant |

## Alpine

Dropdowns (`dropdown_menu`, `dropdown_select`, `dropdown_split`), modal overlays, and trays use Alpine.js for open/close state. Chirp injects Alpine; see [Alpine integration](../concepts/alpine-integration.md).

## Related

- [Alerts](./alerts-and-feedback.md) -- toast for async feedback after close
- [Buttons](./buttons.md) -- `btn`, `split_button` for triggers
- [HTMX patterns](../guides/htmx-patterns.md) -- swapping modal content
- [Filters](../reference/filters.md) -- `validate_variant`, `validate_size`
