# chirp-ui: Sidebar Navigation Refinements

## Goal

Refine ChirpUI's sidebar navigation styles so sectioned nav (NAVIGATE, TOOLS, SETTINGS, etc.) looks clean and sleek by default, with theme-overridable tokens for apps like Dori that want a bolder active state.

---

## Current State

- **Macros:** `sidebar`, `sidebar_section`, `sidebar_link` in `chirpui/sidebar.html`
- **BEM structure:** `chirpui-sidebar`, `chirpui-sidebar__section`, `chirpui-sidebar__section-title`, `chirpui-sidebar__section-links`, `chirpui-sidebar__link`, `chirpui-sidebar__link--active`
- **Collapsible sections:** `sidebar_section(..., collapsible=true)` uses `<details>/<summary>`
- **Active state:** Accent color + 10% accent background tint
- **Section spacing:** `gap: var(--chirpui-spacing-xs)` between sections (very tight)
- **Dori** uses these components; nvidia.css overrides tokens but not sidebar-specific styles

---

## Target Look (Reference: Dori screenshot)

- Clear visual hierarchy: section headers (NAVIGATE, TOOLS) with deliberate spacing
- Active item: prominent highlight (Dori uses full-width lime green background)
- Generous padding and spacing; uncluttered
- Icon + label alignment consistent

---

## Design Tokens (New)

Add optional sidebar tokens so themes can tune without component overrides:

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-sidebar-active-bg` | Active link background | `color-mix(in srgb, var(--chirpui-accent) 10%, transparent)` |
| `--chirpui-sidebar-active-color` | Active link text color | `var(--chirpui-accent)` |
| `--chirpui-sidebar-section-gap` | Vertical gap between sections | `var(--chirpui-spacing-md)` |
| `--chirpui-sidebar-link-gap` | Gap between links within a section | `var(--chirpui-spacing-xs)` |

Themes (e.g. nvidia.css) can override for a bolder active state:

```css
--chirpui-sidebar-active-bg: var(--chirpui-accent);
--chirpui-sidebar-active-color: white;
```

---

## Implementation Plan

### Phase 1: Add sidebar tokens to chirpui.css

1. In `:root`, add:
   - `--chirpui-sidebar-active-bg`
   - `--chirpui-sidebar-active-color`
   - `--chirpui-sidebar-section-gap`
   - `--chirpui-sidebar-link-gap`

2. Place near other layout/spacing tokens (after `--chirpui-spacing-*` or in a "Sidebar" subsection).

### Phase 2: Update sidebar component CSS

| Selector | Current | Change |
|----------|---------|--------|
| `.chirpui-sidebar__nav` | `gap: var(--chirpui-spacing-xs)` | `gap: var(--chirpui-sidebar-section-gap)` |
| `.chirpui-sidebar__section` | `padding: var(--chirpui-spacing-sm) var(--chirpui-spacing)` | Keep; optionally add `margin-top` for first vs. subsequent (or rely on nav gap) |
| `.chirpui-sidebar__section-title` | — | Add `margin-bottom: var(--chirpui-spacing-xs)` for separation from links |
| `.chirpui-sidebar__section-links` | `gap: var(--chirpui-spacing-xs)` | `gap: var(--chirpui-sidebar-link-gap)` |
| `.chirpui-sidebar__link--active` | `color: var(--chirpui-accent)`; `background: color-mix(...)` | `color: var(--chirpui-sidebar-active-color)`; `background: var(--chirpui-sidebar-active-bg)` |

### Phase 3: Refine section title styling

- Add `display: block` if not already (for margin to apply)
- Consider `padding-inline-start: 0` or alignment tweak so section titles align with links
- Ensure collapsible `summary` inherits section-title styling

### Phase 4: Icon alignment (optional)

- `.chirpui-sidebar__icon`: add `display: inline-flex`, `min-width`, or `margin-inline-end` for consistent spacing when icons vary in width

### Phase 5: Dori / nvidia.css override (optional)

Add to nvidia.css if Dori wants the bolder active state:

```css
--chirpui-sidebar-active-bg: var(--chirpui-accent);
--chirpui-sidebar-active-color: var(--chirpui-text);
```

(Or white if desired for max contrast on green.)

### Phase 6: Documentation

- Add sidebar section to `docs/COMPONENT-OPTIONS.md`:
  - Macros: `sidebar`, `sidebar_section`, `sidebar_link`, `sidebar_toggle`
  - Params: `sidebar_section(title, collapsible, cls)`, `sidebar_link(href, label, icon, active, cls)`
  - Tokens: `--chirpui-sidebar-active-bg`, `--chirpui-sidebar-active-color`, `--chirpui-sidebar-section-gap`, `--chirpui-sidebar-link-gap`, `--chirpui-sidebar-collapsed-width`

---

## Collapsible Sidebar (Implemented)

Icon-only mode when collapsed. Opt-in via `app_shell(sidebar_collapsible=true)` or `{% block sidebar_collapsible %}true{% end %}` in `app_shell_layout`.

- **sidebar_link**: Label wrapped in `<span class="chirpui-sidebar__label">`; `title` attr for tooltip.
- **sidebar_toggle**: Macro for toggle button; `data-chirpui-sidebar-toggle` for script.
- **CSS**: `.chirpui-app-shell--sidebar-collapsed` narrows sidebar, hides labels/section titles.
- **Script**: Inline toggle + localStorage persistence; updates `aria-expanded` on button.
- **app_shell / app_shell_layout**: `sidebar_collapsible` param/block; topbar-start when enabled.

---

## File Changes

| File | Action |
|------|--------|
| `src/chirp_ui/templates/chirpui.css` | Add tokens; update sidebar selectors; collapsed state; toggle styles |
| `src/chirp_ui/templates/chirpui/sidebar.html` | Label wrapper; title attr; `sidebar_toggle` macro |
| `src/chirp_ui/templates/chirpui/app_shell.html` | `sidebar_collapsible` param; toggle; script |
| `src/chirp_ui/templates/chirpui/app_shell_layout.html` | `sidebar_collapsible` block; toggle; script |
| `docs/COMPONENT-OPTIONS.md` | Document sidebar macros and tokens |
| `dori/.../nvidia.css` (if desired) | Override sidebar tokens for bolder active state |

---

## Summary (Implemented)

| Step | Action | Status |
|------|--------|--------|
| 1 | Add `--chirpui-sidebar-*` tokens to chirpui.css `:root` | Done |
| 2 | Wire tokens into `.chirpui-sidebar__nav`, `__section-links`, `__link--active` | Done |
| 3 | Refine section title spacing and alignment | Done |
| 4 | Icon alignment in `__icon` | Done |
| 5 | Add `sidebar_toggle`, collapsed state, app_shell integration | Done |
| 6 | Document in COMPONENT-OPTIONS.md | Done |
