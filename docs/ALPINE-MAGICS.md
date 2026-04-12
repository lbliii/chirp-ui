# Alpine Behavior API

chirp-ui uses [Alpine.js](https://alpinejs.dev/) for local UI behavior: dropdowns,
dialogs, copy buttons, tabs, theme/style persistence, shell chrome, and similar
client-only state. This document defines the public behavior contract for those
components.

## Ownership Model

- **Chirp owns Alpine bootstrap**: script injection, plugin loading, `Alpine.safeData()`,
  `alpine_json_config()`, and global startup guarantees.
- **chirp-ui owns the behavior API**: named controllers, documented store keys,
  `chirpui:*` events, and template conventions.
- **Macros stay script-free**: component templates may declare `x-data`,
  `x-ref`, `x-show`, `@click`, and `x-init`, but shared logic lives in the
  runtime asset `chirpui-alpine.js`.

When you call `use_chirp_ui(app)`, Chirp serves the static assets and injects
`chirpui-alpine.js` for named Alpine controllers. `chirpui.js` remains the
pre-paint theme/style asset for standalone/manual setups and inline layout
initializers.

For standalone setups without Chirp, include `chirpui-alpine.js` from
`chirp_ui.static_path()` **before** the Alpine core script so the controller
registrations are ready for Alpine's first initialization pass. The runtime also
creates the `modals` and `trays` stores when Chirp is not present.

## Public Controllers

These controller names are the stable behavior API for chirp-ui templates.

| Controller | Purpose | Used by |
|------------|---------|---------|
| `chirpuiDropdown()` | Shared floating-menu open/close/reposition state | `dropdown_menu`, `dropdown_split` |
| `chirpuiDropdownSelect()` | Dropdown select state, focus, keyboard navigation | `dropdown_select` |
| `chirpuiCopy()` | Clipboard copy + timed feedback | `copy_button`, `code`, `streaming` |
| `chirpuiThemeToggle()` | Theme cycle + persistence | `theme_toggle` |
| `chirpuiStyleToggle()` | Style cycle + persistence | `style_toggle` |
| `chirpuiStyleSelect()` | Style select sync + persistence | `style_select` |
| `chirpuiDialogTarget()` | Open a target `<dialog>` by id | modal/drawer/confirm/command palette triggers |
| `chirpuiSidebar({...})` | Shared shell sidebar collapse behavior | `app_shell`, `app_shell_layout` |

## Store Contract

Current store keys are intentionally small and explicit:

| Store key | Purpose | Used by |
|-----------|---------|---------|
| `modals` | Overlay modal open state | `modal_overlay` |
| `trays` | Tray open state | `tray` |

Do not invent new global stores casually. Prefer a named controller first; use a
store only when state must outlive one component instance or coordinate multiple
surfaces.

## When Inline `x-data` Is Acceptable

Inline `x-data` is allowed only for **trivial** one-state widgets.

Keep inline:

- one boolean or scalar
- one click handler
- no `$refs`, `$nextTick`, `$watch`, `localStorage`, geometry, or keyboard logic

Promote to a named controller when any of the following appear:

- `$refs`
- `$nextTick`
- `$watch`
- `localStorage`
- focus management
- dialog targeting
- viewport/geometry logic
- keyboard navigation
- repeated logic across templates

## Magics Used

| Magic | Purpose | Components |
|-------|---------|------------|
| **$el** | Current DOM element / dataset access | `chirpuiCopy`, `chirpuiDialogTarget`, `chirpuiStyleSelect` |
| **$refs** | Focus and panel references | `chirpuiDropdown`, `chirpuiDropdownSelect` |
| **$store** | Cross-instance UI state | `tray`, `modal_overlay` |
| **$id** | Unique IDs for ARIA wiring | dropdowns, `tabs_panels` |
| **$dispatch** | Component events | dropdowns, tabs, tray, modal |
| **$nextTick** | Post-open alignment / focus | dropdowns |

## Custom Events

Components emit `chirpui:*` events for app-level behavior such as analytics,
HTMX coordination, and URL sync.

| Event | Detail | When |
|-------|--------|------|
| `chirpui:dropdown-selected` | `{ label, href? }` or `{ label, action? }` or `{ label, value? }` | Dropdown item selected |
| `chirpui:tab-changed` | `{ tab }` | Client tab clicked |
| `chirpui:tray-closed` | `{ id }` | Tray backdrop or close button clicked |
| `chirpui:modal-closed` | `{ id }` | Overlay modal backdrop or close button clicked |

```javascript
document.addEventListener("chirpui:dropdown-selected", (event) => {
  if (event.detail.action) {
    // Run HTMX or custom logic here.
  }
});
```

## Accessibility Guarantees

- **Dropdowns** return focus to the trigger on close and support Escape and click-outside dismissal.
- **Dropdown select** focuses the first option on open and keeps combobox ARIA wiring stable.
- **Tabs** use `$id` so multiple tab sets can coexist safely.
- **Dialog triggers** only open native `<dialog>` elements; the dialog itself remains the accessibility authority.

## References

- [Alpine Start Here](https://alpinejs.dev/start-here)
- [Alpine.data() and magic properties](https://alpinejs.dev/globals/alpine-data#using-magic-properties)
- [Alpine dropdown patterns](https://alpinejs.dev/component/dropdown)
