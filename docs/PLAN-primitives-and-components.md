# ChirpUI: Primitives and Components Plan

Plan for ChirpUI primitives and components derived from Dori usage. Layout order: **Tabs topmost** → Title → Actions → Content.

---

## 1. Primitives Inventory

### 1.1 Layout Primitives (existing)

| Primitive | File | Purpose |
|-----------|------|---------|
| `container` | layout.html | Max-width wrapper, padding |
| `stack` | layout.html | Vertical stack with gap |
| `grid` | layout.html | Responsive grid (2/3/4 cols) |
| `cluster` | layout.html | Inline wrapping cluster |
| `block` | layout.html | Grid item with span |
| `page_header` | layout.html | H1 + subtitle + meta + actions slot |
| `section_header` | layout.html | H2 + subtitle + icon + actions |
| `section` | layout.html | surface + section_header + content |
| `section_collapsible` | layout.html | details/summary with section_header |

### 1.2 Surface Primitives (existing)

| Primitive | File | Purpose |
|-----------|------|---------|
| `surface` | surface.html | Background container (muted, elevated, etc.) |

### 1.3 Action Primitives (existing)

| Primitive | File | Purpose |
|-----------|------|---------|
| `action_strip` | action_strip.html | Search/filter/action row (includes surface + inner strip) |

### 1.4 Tabbed Layout Primitives (new)

| Primitive | File | Purpose |
|-----------|------|---------|
| `route_tabs` | route_tabs.html | Route-backed subsection nav (HTMX swap) |
| `tabbed_page_layout` | tabbed_page_layout.html | Macro: page-root → route-tabs + page-content-inner |
| `content_action_bar` | layout.html | Action strip + bottom margin (convenience) |

### 1.5 Python Helpers (new)

| Helper | File | Purpose |
|--------|------|---------|
| `tab_is_active` | route_tabs.py | `(tab, current_path) -> bool` for exact/prefix match |

---

## 2. Component Specifications

### 2.1 `route_tabs` (component + CSS)

**File:** `chirpui/route_tabs.html`

**Tab item structure:**
```python
# dict or object with:
#   label: str
#   href: str
#   icon?: str       # ChirpUI icon name (e.g. "grid", "chain")
#   badge?: str      # Optional pill text
#   match?: str      # "exact" | "prefix" (default "exact")
```

**API:**
```html
{% from "chirpui/route_tabs.html" import route_tabs %}
{{ route_tabs(tabs, current_path, target="#page-root", is_active=tab_is_active) }}
```

**Behavior:**
- Renders `<nav role="navigation" aria-label="Subsection navigation" class="chirpui-route-tabs">`
- Each tab: `<a href="..." class="chirpui-route-tab" hx-get="..." hx-target="#page-root" hx-push-url="true" hx-swap="innerHTML">`
- Active: `chirpui-route-tab--active`, `aria-current="page"`
- Uses `icon` filter if `tab.icon` provided
- Supports optional badge via `tab.badge`

**Params:**
- `tabs`: list of tab dicts/objects
- `current_path`: str (e.g. request.path)
- `target`: str, default `"#page-root"` — HTMX swap target
- `is_active`: callable `(tab, current_path) -> bool`, default `tab_is_active` (template global)

**CSS:**
- `.chirpui-route-tabs`, `.chirpui-route-tab`, `.chirpui-route-tab--active`, `.chirpui-route-tab__icon`, `.chirpui-route-tab__badge`
- Port from Dori `nvidia.css` lines 739–792 (replace `dori-` with `chirpui-`)

---

### 2.2 `tabbed_page_layout` (layout macro)

**File:** `chirpui/tabbed_page_layout.html`

**API:**
```html
{% from "chirpui/tabbed_page_layout.html" import tabbed_page_layout %}
{% call tabbed_page_layout(route_tabs=route_tabs, current_path=current_path) %}
  {% slot page_header %}{{ page_header("Section Title") }}{% end %}
  {% slot page_toolbar %}{% end %}
  {% slot page_content %}...{% end %}
{% end %}
```

**Structure:**
```
container
  stack(gap="lg")
    #page-root
      #page-content (flex column, gap)
        #route-tabs (when route_tabs)
          {{ route_tabs(...) }}
        #page-content-inner (flex column, gap)
          page_header
          page_toolbar
          page_content
```

**Context:**
- `route_tabs`: optional list; when present, renders route_tabs
- `current_path`: optional; passed to route_tabs

---

### 2.3 `content_action_bar` (convenience macro)

**File:** `chirpui/layout.html`

**Note:** `action_strip` already includes surface. Dori uses `action_strip` wrapped in `<div class="chirpui-surface chirpui-surface--muted chirpui-mb-md">` — that is redundant. The only extra is `chirpui-mb-md`.

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
- Wraps `action_strip(...)` in a div with `chirpui-mb-md`
- Reduces boilerplate for the pattern: action bar + bottom margin before content

**Implementation:** Either `action_strip(...)` with `cls="chirpui-mb-md"` on the outer wrapper (but action_strip's cls goes on inner div), or a new macro that wraps action_strip in `<div class="chirpui-mb-md">` — but action_strip already has a surface wrapper. So we need a wrapper that adds margin. Simplest: `content_action_bar` = `<div class="chirpui-mb-md">{% call action_strip(...) %}...{% end %}</div>`.

**Priority:** Low. Nice-to-have.

---

### 2.4 `tab_is_active` (Python helper)

**File:** `chirp_ui/route_tabs.py`

**API:**
```python
def tab_is_active(tab: dict | object, current_path: str) -> bool:
    """Return True when tab matches current_path. Tab must have href and match (default 'exact')."""
```

**Contract:**
- Tab has `href` (str) and optionally `match` ("exact" | "prefix")
- `exact`: `current_path == tab.href`
- `prefix`: `current_path == tab.href or current_path.startswith(tab.href + "/")`
- Support both dict (`tab["href"]`) and object (`tab.href`)

**Registration:** ChirpUI registers as `app.template_global("tab_is_active")(tab_is_active)` when `use_chirp_ui(app)` is called.

---

## 3. Icon Registry (ChirpUI)

**Verified:** `icon` filter exists in `chirp_ui/filters.py`. `tab.icon | icon` works.

**Dori tab icons used:** grid, chart, bolt, chat, list, cloud, arrow, skills, shortcut, chain, settings, sources, status, gear.

**ChirpUI ICON_REGISTRY has:** grid, logs, cloud, arrow, shortcut, skills, chain, settings, gear, status, sources (⊞). Missing: chart, bolt, chat, list (as distinct). Consider adding:
- `chart` → e.g. "▤" or "▥"
- `bolt` → e.g. "⚡"
- `chat` → e.g. "💬" or "◉"
- `list` → e.g. "≡" or reuse "⟳" (logs)

**Action:** Add missing icons to ChirpUI `icons.py` before or during migration.

---

## 4. Implementation Order

| Phase | Task | Effort |
|-------|------|--------|
| 1 | Add `route_tabs.html` template + CSS to ChirpUI | Medium |
| 2 | Add `route_tabs.py` with `tab_is_active`, register as template_global | Low |
| 3 | Add `tabbed_page_layout` macro | Medium |
| 4 | Add missing icons (chart, bolt, chat, list) if needed | Low |
| 5 | Migrate Dori to use ChirpUI `route_tabs` and `tabbed_page_layout` | Medium |
| 6 | Add `content_action_bar` (optional) | Low |

---

## 5. Files to Create/Modify

### ChirpUI (new)

- `src/chirp_ui/templates/chirpui/route_tabs.html`
- `src/chirp_ui/templates/chirpui/tabbed_page_layout.html`
- `src/chirp_ui/route_tabs.py`

### ChirpUI (modify)

- `src/chirp_ui/templates/chirpui.css` — add `.chirpui-route-tabs` section
- `src/chirp_ui/templates/chirpui/layout.html` — add `content_action_bar` (optional)
- `src/chirp_ui/icons.py` — add chart, bolt, chat, list if missing
- Chirp registration (e.g. `chirp_ui/ext.py` or similar) — register `tab_is_active`
- `site/content/docs/app-shell/_index.md` — document route_tabs, tabbed_page_layout

### Dori (after ChirpUI ships)

- Remove `_route_tabs.html`; use `chirpui/route_tabs.html`
- Remove route-tabs CSS from nvidia.css
- Optionally use `tabbed_page_layout` macro in `_page_layout.html`
- Keep `route_tabs.py` for tab definitions (RouteTab, DISCOVER_TABS, etc.) — app-specific data
- Remove redundant `surface` wrapper around `action_strip` in chains/shortcuts pages (or use `content_action_bar` if added)

---

## 6. Resolved Questions

- **tab_is_active:** ChirpUI-provided; apps can override via template_global if needed.
- **Target:** Default `#page-root`; allow override via `target` param.
- **Icon filter:** Exists; `tab.icon | icon` works.
- **tabbed_page_layout:** Macro (recommended) for flexibility.
- **content_action_bar:** Optional; Dori can keep using `action_strip` + `chirpui-mb-md` wrapper until added.

---

## 7. Route Tabs CSS (port from Dori)

```css
/* Route-family subsection tabs (Workspace, Settings, etc.) */
.chirpui-route-tabs {
    display: flex;
    flex-wrap: wrap;
    gap: var(--chirpui-spacing-sm);
    border-bottom: 1px solid var(--chirpui-border);
    padding-bottom: 0;
}
.chirpui-route-tab {
    display: inline-flex;
    align-items: center;
    gap: var(--chirpui-spacing-sm);
    padding: var(--chirpui-spacing-sm) var(--chirpui-spacing);
    color: var(--chirpui-text-muted);
    text-decoration: none;
    font-size: var(--chirpui-font-sm);
    font-weight: 500;
    border-radius: var(--chirpui-radius-sm) var(--chirpui-radius-sm) 0 0;
    border: 1px solid transparent;
    border-bottom: none;
    margin-bottom: -1px;
    background: transparent;
    transition: color var(--chirpui-transition), background var(--chirpui-transition),
        border-color var(--chirpui-transition);
}
.chirpui-route-tab:hover {
    color: var(--chirpui-text);
    background: var(--chirpui-surface-alt);
}
.chirpui-route-tab--active,
.chirpui-route-tab[aria-current="page"] {
    color: var(--chirpui-accent);
    background: var(--chirpui-primary-muted);
    border-color: var(--chirpui-border);
    border-bottom-color: var(--chirpui-bg);
    box-shadow: 0 -1px 0 0 var(--chirpui-accent);
}
.chirpui-route-tab__icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1em;
    height: 1em;
    opacity: 0.85;
}
.chirpui-route-tab--active .chirpui-route-tab__icon,
.chirpui-route-tab[aria-current="page"] .chirpui-route-tab__icon {
    opacity: 1;
}
.chirpui-route-tab__badge {
    font-size: var(--chirpui-font-xs);
    padding: 0.125rem 0.375rem;
    background: var(--chirpui-surface-alt);
    border-radius: 9999px;
}
```
