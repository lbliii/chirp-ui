# chirp-ui: Route Tabs and Tabbed Page Layout

> **See also:** [PLAN-primitives-and-components.md](PLAN-primitives-and-components.md) for full primitives inventory, component specs, and implementation details.

## Goal

Extract Dori's route-backed subsection tabs and tabbed page layout into ChirpUI primitives so any Chirp+ChirpUI app can use them without reimplementing. Layout order: **Tabs topmost** → Title → Actions → Content.

---

## Current State

### Dori (source of truth)

- **`_route_tabs.html`**: `render_route_tabs(tabs, current_path)` macro. Renders `<nav>` with `<a>` links. Each link has `hx-get`, `hx-target="#page-root"`, `hx-push-url`, `hx-swap="innerHTML"`. Tab items: `{label, href, icon?, badge?, match?}`.
- **`route_tabs.py`**: `RouteTab` dataclass, `tab_is_active(tab, current_path)` helper. Uses `match="exact"` or `match="prefix"`.
- **`template_global("tab_is_active")`**: Injected into templates for active-state logic.
- **`_page_layout.html`**: Structure: `container` → `stack` → `#page-root` → `#page-content` (route-tabs + page-content-inner) → page_header, page_toolbar, page_content blocks.
- **`nvidia.css`**: `.dori-route-tabs`, `.dori-route-tab`, `.dori-route-tab--active`, `.dori-route-tab__icon`, `.dori-route-tab__badge` (pill-style, border-bottom, active state).

### ChirpUI (existing)

- **`tabs_panels.html`**: Client-side tab switching (Alpine.js), `role="tab"`. Not for route navigation.
- **`nav_link.html`**: Single link with `hx-boost`, `hx-target="#main"`. No tab bar.
- **`chirpui.css`**: `#page-root`, `#page-content`, `#page-content-inner` flex + gap (already added).

---

## Proposed Primitives

### 1. `route_tabs` (component + CSS)

**File:** `chirpui/route_tabs.html`

**API:**
```python
# Tab item: dict with label, href, icon?, badge?, match?
# match: "exact" | "prefix" (default "exact")
# is_active: template global or passed-in callable
```

```html
{% from "chirpui/route_tabs.html" import route_tabs %}
{{ route_tabs(tabs, current_path, is_active=tab_is_active) }}
```

**Behavior:**
- Renders `<nav role="navigation" aria-label="Subsection navigation" class="chirpui-route-tabs">`
- Each tab: `<a href="..." class="chirpui-route-tab" hx-get="..." hx-target="#page-root" hx-push-url="true" hx-swap="innerHTML">`
- Active: `chirpui-route-tab--active`, `aria-current="page"`
- Uses `icon` filter if provided; supports optional badge slot.

**is_active contract:** `(tab, current_path) -> bool`. Default: `current_path == tab.href` for exact, `current_path.startswith(tab.href + "/") or current_path == tab.href` for prefix. ChirpUI can provide a built-in `tab_is_active` that apps register as template_global, or pass a custom callable.

**CSS:** Add to chirpui.css (port from Dori nvidia.css):
- `.chirpui-route-tabs`, `.chirpui-route-tab`, `.chirpui-route-tab--active`, `.chirpui-route-tab__icon`, `.chirpui-route-tab__badge`

**Target:** `#page-root` by default. Allow override via param (e.g. `target="#page-content"`) for flexibility.

---

### 2. `tabbed_page_layout` (layout template)

**File:** `chirpui/tabbed_page_layout.html` (or `chirpui/app_shell_tabbed.html`)

**API:**
```html
{% extends "chirpui/tabbed_page_layout.html" %}
{% block page_header %}{{ page_header("Section Title") }}{% end %}
{% block page_toolbar %}{% end %}
{% block page_content %}...{% end %}
```

**Structure:**
- Wraps `container` → `stack` → `#page-root` → `#page-content` (route-tabs + page-content-inner)
- `#page-content-inner`: `page_header`, `page_toolbar`, `page_content` blocks
- `route_tabs` rendered when `route_tabs` context variable exists

**Alternative:** Keep as macro `tabbed_page_layout()` that slots header, toolbar, content. Apps extend their own `_layout.html` and call `tabbed_page_layout()` with blocks. Or provide as a base template that apps extend.

**Recommendation:** Provide as a **macro** `tabbed_page_layout(route_tabs=route_tabs)` so apps can compose it into their layout without forcing a new base template. The macro renders the full structure; slots are `page_header`, `page_toolbar`, `page_content`.

---

### 3. `content_action_bar` (convenience macro)

**File:** `chirpui/action_strip.html` (extend) or `chirpui/layout.html`

**API:**
```html
{% from "chirpui/layout.html" import content_action_bar %}
{% call content_action_bar(surface_variant="muted", density="sm") %}
<div class="chirpui-action-strip__actions">
  <button class="chirpui-btn chirpui-btn--primary chirpui-btn--sm">＋ New</button>
</div>
{% end %}
```

**Behavior:**
- Wraps `surface(variant)` + `action_strip(...)` + `chirpui-mb-md`
- Reduces boilerplate for the common pattern: action bar in a muted surface with bottom margin.

**Priority:** Low. Nice-to-have.

---

### 4. `tab_is_active` (Python helper)

**File:** `chirp_ui/route_tabs.py` (new) or similar

**API:**
```python
def tab_is_active(tab: dict | object, current_path: str) -> bool:
    """Return True when tab matches current_path. Tab must have href and match (default 'exact')."""
```

**Contract:** Tab has `href` and optionally `match` ("exact" | "prefix"). Apps register as `app.template_global("tab_is_active")(tab_is_active)`.

**Usage:** ChirpUI can ship this; Chirp apps using `use_chirp_ui()` could auto-register it. Or Dori keeps its own. For ChirpUI to be self-contained, include a default implementation.

---

## Implementation Order

| Phase | Task | Effort |
|-------|------|--------|
| 1 | Add `route_tabs` template + CSS to ChirpUI | Medium |
| 2 | Add `tab_is_active` helper (or document that apps must provide it) | Low |
| 3 | Add `tabbed_page_layout` macro | Medium |
| 4 | Migrate Dori to use ChirpUI `route_tabs` and `tabbed_page_layout` | Medium |
| 5 | Add `content_action_bar` (optional) | Low |

---

## Migration: Dori

1. **ChirpUI** adds `route_tabs.html`, `chirpui-route-tabs` CSS, `tab_is_active` in `chirp_ui/route_tabs.py` (or similar).
2. **Dori** removes `_route_tabs.html`, `route_tabs.py` (or keeps only `RouteTab`/tab definitions and `tab_is_active` if ChirpUI's default doesn't match). Dori imports `route_tabs` from ChirpUI.
3. **Dori** removes `.dori-route-tabs` etc. from nvidia.css; uses ChirpUI classes.
4. **Dori** `_page_layout.html` either uses ChirpUI `tabbed_page_layout` macro or keeps current structure (already compatible).

---

## Open Questions

- **tab_is_active:** ChirpUI-provided vs app-provided? Dori's logic supports exact and prefix. ChirpUI could ship a default; apps override if needed.
- **Target:** Always `#page-root`? Or allow `#page-content` for narrow swaps? Default `#page-root` matches current fragment target registry.
- **Icon filter:** `tab.icon | icon` — ChirpUI has `icon` filter in `filters.py`. ✓
- **tabbed_page_layout:** Macro vs base template? Macro is more flexible; apps can wrap in their own layout.

---

## Files to Create/Modify

### ChirpUI (new)

- `src/chirp_ui/templates/chirpui/route_tabs.html`
- `src/chirp_ui/templates/chirpui.css` (add section for route-tabs)
- `src/chirp_ui/route_tabs.py` (optional, for `tab_is_active`)
- `src/chirp_ui/templates/chirpui/tabbed_page_layout.html` (macro)

### ChirpUI (modify)

- `src/chirp_ui/ext/chirp_ui.py` — register `tab_is_active` if ChirpUI provides it
- `site/content/docs/app-shell/_index.md` — document route_tabs, tabbed_page_layout

### Dori (after ChirpUI ships)

- Remove `_route_tabs.html`; use `chirpui/route_tabs.html`
- Remove route-tabs CSS from nvidia.css
- Optionally use `tabbed_page_layout` macro in `_page_layout.html`
- Keep `route_tabs.py` for tab definitions (RouteTab, DISCOVER_TABS, etc.) — or move tab data to ChirpUI if it makes sense (unlikely; tab definitions are app-specific)
