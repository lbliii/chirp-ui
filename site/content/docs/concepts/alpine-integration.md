---
title: Alpine integration
description: How chirp-ui uses Alpine.js with Chirp
draft: false
weight: 50
lang: en
type: doc
keywords: [chirp-ui, alpine, htmx, chirp]
icon: lightning
---

# Alpine integration

Interactive chirp-ui pieces (dropdowns, modals, trays, tabs, inline state) use **Alpine.js** via `x-data` and related attributes. **Chirp** injects Alpine when `alpine=True` on the app config; `use_chirp_ui(app)` enables Alpine by default for convenience.

## Ownership

- **Chirp** owns Alpine script injection and lifecycle.
- **chirp-ui** does not ship inline `<script>` blocks in macros — only attributes and optional `chirpui.js` for theme/style bootstrapping.

## Named components

For htmx-safe behavior across full loads and boosted navigation, register Alpine data with **`Alpine.safeData`** (provided by Chirp) for named component factories.

## Magics

| Magic | Purpose | Components |
|-------|---------|------------|
| `$el` | Current DOM element (dataset access) | dropdown_select, copy_button, theme_toggle, toast |
| `$refs` | DOM references for focus management | dropdown_menu, dropdown_select, dropdown_split |
| `$store` | Global state (modals/trays stores) | tray, modal_overlay |
| `$id` | Unique IDs for ARIA attributes | dropdown, tabs_panels |
| `$watch` | Reactive sync between data properties | theme_toggle (style_select) |
| `$dispatch` | Custom event dispatch | dropdown, tabs, tray, modal |
| `$nextTick` | Post-render focus and DOM reads | dropdown_select |

## Custom events

Components emit `chirpui:*` events for app-level handling (analytics, HTMX triggers, URL sync).

| Event | Detail payload | When |
|-------|---------------|------|
| `chirpui:dropdown-selected` | `{ label, href? }` or `{ label, action? }` or `{ label, value? }` | Dropdown item clicked |
| `chirpui:tab-changed` | `{ tab }` | Tab button clicked |
| `chirpui:tray-closed` | `{ id }` | Tray backdrop or close button clicked |
| `chirpui:modal-closed` | `{ id }` | Modal backdrop or close button clicked |

### Listening for events

Listen on `document` or a parent element:

```javascript
document.addEventListener('chirpui:dropdown-selected', (e) => {
  if (e.detail.action) {
    // Run HTMX or custom logic
  }
});
```

```javascript
document.addEventListener('chirpui:tab-changed', (e) => {
  const url = new URL(window.location);
  url.searchParams.set('tab', e.detail.tab);
  history.replaceState(null, '', url);
});
```

## Accessibility

- **Dropdown**: `x-ref` for trigger/panel; `$refs.trigger.focus()` on close; Escape, click-outside, and `focusin.window` close with focus return.
- **dropdown_select**: Arrow-key navigation via `@keydown.arrow-up` / `@keydown.arrow-down`; `$nextTick` to focus the first item when opening; `aria-activedescendant` for combobox pattern.
- **Tabs**: `$id` generates unique `aria-controls` / `aria-labelledby` pairs so multiple tab sets on the same page do not collide.

## htmx + Alpine

When a fragment swaps in new HTML, ensure Alpine **initializes** on the new nodes (Chirp's integration handles common cases). For complex islands, prefer `fragment_island` patterns in [HTMX patterns](../guides/htmx-patterns.md).
