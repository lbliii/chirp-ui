# Alpine.js Magics in chirp-ui

chirp-ui uses [Alpine.js](https://alpinejs.dev/) for interactive components (dropdown, modal, tray, tabs, theme toggle, copy button). This document describes the magics and patterns used.

## Magics Used

| Magic | Purpose | Components |
|-------|---------|------------|
| **$el** | Current DOM element | dropdown_select (dataset.label), copy_button (dataset.copyText), theme_toggle (value), toast (parentElement) |
| **$refs** | DOM references for focus management | dropdown_menu, dropdown_select, dropdown_split |
| **$store** | Global state | tray, modal_overlay (modals/trays stores) |
| **$id** | Unique IDs for ARIA | dropdown, tabs_panels |
| **$watch** | Reactive sync | theme_toggle (style_select) |
| **$dispatch** | Custom events | dropdown, tabs, tray, modal |
| **$nextTick** | Post-render focus | dropdown_select |

## Custom Events

Components emit `chirpui:*` events for app-level handling (analytics, HTMX, URL sync).

| Event | Detail | When |
|-------|--------|------|
| `chirpui:dropdown-selected` | `{ label, href? }` or `{ label, action? }` or `{ label, value? }` | Dropdown item clicked |
| `chirpui:tab-changed` | `{ tab }` | Tab button clicked |
| `chirpui:tray-closed` | `{ id }` | Tray backdrop or close button clicked |
| `chirpui:modal-closed` | `{ id }` | Modal backdrop or close button clicked |

Listen on `document` or a parent:

```javascript
document.addEventListener('chirpui:dropdown-selected', (e) => {
  if (e.detail.action) {
    // Run HTMX or custom logic
  }
});
```

## Accessibility

- **Dropdown**: `x-ref` for trigger/panel; `$refs.trigger.focus()` on close; Escape, click-outside, focusin.window close with focus return.
- **dropdown_select**: Arrow-key navigation; `$nextTick` to focus first item when opening; `aria-activedescendant` for combobox.
- **Tabs**: `$id` for unique `aria-controls` / `aria-labelledby` when multiple tab sets exist.

## References

- [Alpine.js Magics](https://alpinejs.dev/globals/alpine-data#using-magic-properties)
- [Alpine Dropdown Component](https://alpinejs.dev/component/dropdown)
- [Alpine $id](https://alpinejs.dev/magics/id)
