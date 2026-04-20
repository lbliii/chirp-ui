# chirp-ui: Migrate chirpui.js to Alpine.js

## Status

Historical migration plan. The broad migration described here is complete:

- `chirpui.js` is now pre-paint theme/style init only.
- interactive behavior lives in Alpine-powered templates
- the current contract for shared behavior lives in `ALPINE-MAGICS.md`

Use this file as background only. For the current runtime split and public
controller/store/event contract, see:

- `docs/ALPINE-MAGICS.md`
- `docs/ANTI-FOOTGUNS.md`
- Chirp's `site/content/docs/guides/alpine.md`

## Goal

Replace the custom vanilla JS in `chirpui.js` with Alpine.js for interactive components. Align chirp-ui with the HTMX + Alpine stack, reduce custom code to maintain, and use declarative patterns.

---

## Current State

- **chirpui.js** (~290 lines): Vanilla JS IIFEs for theme/style, dropdown, tray, modal, copy, tabs
- **Data attributes** drive behavior: `data-chirpui-dropdown`, `data-chirpui-tray-trigger`, etc.
- **HTMX integration**: `htmx:afterSettle` re-inits components after swaps
- **No framework dependency** today; apps include chirpui.js after chirpui.css

### Components and Templates

| Component | Template | Data Attributes | chirpui.js Logic |
|-----------|----------|-----------------|------------------|
| Dropdown | dropdown_menu.html | data-chirpui-dropdown, data-chirpui-dropdown-trigger | Open/close, outside click, Escape, arrow keys |
| Tray | tray.html | data-chirpui-tray-trigger, data-chirpui-tray, data-chirpui-tray-backdrop, data-chirpui-tray-close | Slide-in panel, body scroll lock, focus trap |
| Modal | modal_overlay.html | data-chirpui-modal-trigger, data-chirpui-modal, data-chirpui-modal-backdrop, data-chirpui-modal-close | Overlay, body scroll lock, Escape |
| Theme toggle | theme_toggle.html | data-chirpui-theme-toggle, data-chirpui-theme-icon | Cycle system/light/dark, localStorage |
| Style toggle | theme_toggle.html | data-chirpui-style-toggle, data-chirpui-style-select | Cycle default/neumorphic, localStorage |
| Copy button | (inline) | data-chirpui-copy, data-copy-text | Clipboard API, temporary "Copied!" state |
| Tabs | tabs_panels.html | data-chirpui-tabs, data-tab-trigger, data-tab-panel | Tab switching, aria-selected |

### Special Case: Theme/Style Init

Theme and style must be applied **before first paint** (FOUC prevention). Current chirpui.js runs an IIFE at parse time:

```js
var t = localStorage.getItem("chirpui-theme") || "system";
document.documentElement.setAttribute("data-theme", t);
```

Alpine evaluates after DOM ready. We need a tiny inline script (or Alpine's `x-init` with `$nextTick`) for pre-paint init. Options: keep a minimal ~5-line inline script, or use a blocking script in `<head>`.

---

## Dependencies

- **Alpine.js** v3.x (defer or standard)
- **@alpinejs/mask** — for phone_field, money_field, masked_field (load before Alpine core)
- **@alpinejs/intersect** — for reveal_on_scroll, x-intersect in app templates (load before Alpine core)
- **@alpinejs/focus** — for x-trap on tray and modal_overlay (focus containment, scroll lock)
- **HTMX** (already required)
- Apps using chirp-ui must include Alpine before chirp-ui components render

### Package / Docs Updates

- Add Alpine to chirp-ui README as a peer/required dependency
- Document in app_shell_layout and layout docs: "Include Alpine.js for dropdown, modal, tray, tabs, theme toggle"
- Mask plugin: app_shell_layout and app_layout include @alpinejs/mask before Alpine core for masked form fields
- Intersect plugin: same layouts include @alpinejs/intersect for reveal_on_scroll and x-intersect use cases
- Focus plugin: same layouts include @alpinejs/focus; tray and modal_overlay use x-trap.inert.noscroll for accessibility
- Consider: chirp-ui could bundle a minimal Alpine build or document CDN/install

---

## Alpine Patterns (Per Component)

### 1. Dropdown

```html
<div class="chirpui-dropdown" x-data="{ open: false }"
     @keydown.escape.window="open = false"
     @click.outside="open = false">
  <div class="chirpui-dropdown__trigger" @click="open = !open"
       :aria-expanded="open" role="button" tabindex="0">
    {{ trigger }}
  </div>
  <div class="chirpui-dropdown__menu" x-show="open" x-collapse
       @click="open = false">
    <!-- items -->
  </div>
</div>
```

- Use `x-collapse` (Alpine plugin) or `x-show` + CSS for animation
- Keyboard: Alpine's `@keydown.escape.window`; arrow-key focus can use `x-ref` + `$refs` or a small Alpine component

### 2. Tray

```html
<div x-data="tray()" x-init="init()">
  <button @click="open()" data-chirpui-tray-trigger>Open</button>
  <div id="tray-{{ id }}" x-show="isOpen" x-transition
       @keydown.escape.window="close()">
    <div @click="close()" data-chirpui-tray-backdrop></div>
    <button @click="close()" data-chirpui-tray-close>Close</button>
    <!-- content -->
  </div>
</div>
```

- `Alpine.data('tray', () => ({ isOpen: false, open(), close(), init() }))` for body scroll lock, focus
- Or use `x-effect` to toggle `document.body.style.overflow` when `isOpen` changes

### 3. Modal

Same pattern as tray; Alpine `x-data` with open/close, backdrop click, Escape.

### 4. Theme Toggle

```html
<button x-data="themeToggle()" @click="cycle()"
        :title="'Theme: ' + theme">
  <span x-text="icon"></span>
</button>
```

- `Alpine.data('themeToggle', () => ({ theme, icon, cycle() }))`
- Persist to localStorage; sync `document.documentElement.dataset.theme`
- **Pre-paint**: Inline script in `<head>` (before Alpine) to set `data-theme` from localStorage

### 5. Copy Button

```html
<button x-data="{ copied: false }"
        @click="navigator.clipboard.writeText(text).then(() => { copied = true; setTimeout(() => copied = false, 1500) })">
  <span x-show="!copied">Copy</span>
  <span x-show="copied">Copied!</span>
</button>
```

### 6. Tabs

```html
<div x-data="{ active: '{{ active }}' }">
  <button @click="active = 'tab1'" :aria-selected="active === 'tab1'">Tab 1</button>
  <div x-show="active === 'tab1'">Panel 1</div>
  <div x-show="active === 'tab2'">Panel 2</div>
</div>
```

---

## Migration Phases

### Phase 1: Add Alpine, Keep chirpui.js (Parallel)

1. Add Alpine.js to app_shell_layout, kanban_shell, pages_shell, etc.
2. Document Alpine as required for chirp-ui interactive components
3. Verify chirpui.js and Alpine coexist (no conflicts)
4. **Deliverable**: Alpine available; chirpui.js still drives behavior

### Phase 2: Migrate Components One-by-One

Order (by usage / risk):

1. **Dropdown** — highest usage (shell actions, overflow menu)
2. **Theme toggle** — keep pre-paint inline script; migrate cycle logic to Alpine
3. **Tabs** — straightforward
4. **Copy button** — simple
5. **Modal** — medium complexity
6. **Tray** — medium complexity

For each component:

- Add Alpine `x-data` / directives to template
- Remove corresponding IIFE from chirpui.js
- Test with HTMX swaps (htmx:afterSettle; Alpine auto-inits on new DOM)
- Update component docs

### Phase 3: Remove chirpui.js

1. Delete chirpui.js or reduce to a minimal stub (if any logic remains)
2. Extract pre-paint theme init to a small inline script or document it for apps to include
3. Update README, CHANGELOG
4. Bump major or minor per semver (new Alpine dependency is a breaking change for zero-JS users)

### Phase 4: Cleanup

- Remove `data-chirpui-dropdown` etc. if unused
- Ensure CSS still works (classes like `.chirpui-dropdown__menu` stay)
- Add Alpine version to pyproject or docs

---

## Rollback

- Keep chirpui.js in git history; tag before migration
- Feature flag or build variant: `CHIRPUI_ALPINE=1` to use Alpine templates (optional; adds complexity)
- Simpler: commit each phase; revert commits if needed

---

## Acceptance Criteria

- [x] All interactive components work with Alpine (dropdown, tray, modal, theme, style, copy, tabs)
- [x] No FOUC on theme (data-theme set before first paint)
- [x] HTMX swaps (OOB, partials) still work; Alpine inits on new content
- [x] Accessibility preserved (aria-expanded, focus management, Escape, arrow keys where applicable)
- [x] chirpui.js removed or reduced to &lt;20 lines (pre-paint only)
- [x] README documents Alpine as required
- [x] Chirp examples (kanban_shell, pages_shell) extend app_shell_layout and work

---

## Alpine Magics Adoption (Complete)

Alpine.js magics (`$refs`, `$id`, `$dispatch`, `$nextTick`) have been adopted across chirp-ui and Chirp:

- **$refs + $nextTick**: Dropdown focus management, Escape/click-outside with focus return, arrow-key navigation for dropdown_select
- **$id**: Unique IDs for dropdown and tabs (avoids collisions when multiple instances exist)
- **$dispatch**: `chirpui:dropdown-selected`, `chirpui:tab-changed`, `chirpui:tray-closed`, `chirpui:modal-closed` for app-level handling

See [ALPINE-MAGICS.md](ALPINE-MAGICS.md) for full documentation.

---

## Completed: App Shell Layout Refactor (2025-03)

- kanban_shell and pages_shell now extend `chirpui/app_shell_layout.html` instead of custom layouts
- Added `head_extra` block for layout-specific CSS/scripts
- Added `brand_link` block for custom brand href (override when default `/` is wrong)
- Kida note: avoid `{% block x %}/{% end %}` inside attribute values (causes k-par-001)

## Open Questions

1. **Alpine CDN vs package**: Document CDN, or add Alpine to chirp-ui's static assets / use_chirp_ui?
2. **x-collapse**: Use Alpine Collapse plugin for dropdown animation, or CSS-only?
3. **Zero-JS option**: Should chirp-ui support a "no Alpine" mode (e.g. native `<details>` for dropdown) for minimal apps? Out of scope for this plan.
