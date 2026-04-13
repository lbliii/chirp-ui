# chirp-ui

An optional companion UI layer for the Chirp web framework — Kida template macros (cards, modals, forms, layouts) that render as HTML, styled with modern CSS.

## Stack

| Layer | Package |
|-------|---------|
| Template engine | [kida-templates](https://github.com/lbliii/kida) — Jinja2-like, `PackageLoader`, `{% slot %}` |
| Web framework | [bengal-chirp](https://github.com/lbliii/chirp) — optional; `chirp-ui` works standalone |
| Interactivity | Alpine.js (injected by Chirp, no build step) + htmx for swaps/SSE |
| CSS | `chirpui-*` CSS custom properties, `color-mix()`, `:has()`, container queries |
| Python | 3.14+ (free-threading ready, `_Py_mod_gil = 0`) |

## Project layout

```
src/chirp_ui/
  __init__.py          # get_loader(), register_filters(), static_path()
  filters.py           # bem, html_attrs, build_hx_attrs, validate_*, register_colors, resolve_color, sanitize_color, contrast_text
  validation.py        # VARIANT_REGISTRY, SIZE_REGISTRY, set_strict()
  route_tabs.py        # route-aware tabs helper
  templates/chirpui/   # Kida macros — one file per component (e.g. aura.html, label_overline.html)
  templates/patterns/  # SVG tiles for --chirpui-pattern-* + .chirpui-texture--* (serve with static_path())
  # CSS-only: --chirpui-bg-pattern-* tokens, .chirpui-bg-pattern--*, .chirpui-band--pattern-*, .chirpui-ambient, surface--noise-overlay / --static-overlay
  templates/chirpui.css
  templates/chirpui.js
  templates/themes/
tests/
  conftest.py          # Kida Environment fixture with filter stubs (no Chirp required)
  test_components.py
  test_css_syntax.py
  test_template_css_contract.py
  test_transition_tokens.py
  test_filters.py
  test_validation.py
docs/
```

**UI vocabulary:** `docs/UI-LAYERS.md` — app shell vs **marketing site shell** vs page chrome vs **surface chrome** (component frames), shell regions, page fragment target IDs, and links to Chirp’s `chirp.shell_regions` constants.

## Dev commands

```bash
uv sync --group dev      # install deps
uv run pytest -q         # tests
uv run ruff check .      # lint
uv run ruff format .     # format
uv run ty check src/     # type check (Astral ty, Rust-based)
uv run poe ci            # full CI: lint + format + CSS + ty + tests
```

Or via Make: `make test`, `make lint`, `make ty`, `make ci`, `make test-browser` (see `Makefile`).

**Documentation site (Bengal)** — lives under `site/`; published to GitHub Pages like other b-stack repos. **`site/public/` is not committed** (generated output; matches chirp/kida).

```bash
uv sync --group docs
uv run poe docs-build-all   # bengal site build + static showcase → site/public/showcase/
# or: uv run poe docs-build && make showcase-public
uv run poe docs-serve       # local preview (rebuild first for /showcase/)
```

Standalone showcase preview (no Bengal): `make showcase` → `_site/index.html`.

## Key conventions

- **BEM class names** — all CSS classes use `chirpui-<block>` and `chirpui-<block>--<modifier>`.
- **Kida macros** — components are `{% macro %}` / `{% call %}` pairs using `{% slot %}` for content injection. No wrapper divs without good reason.
- **No client JS in macros** — Alpine.js `x-data` attributes only; no `<script>` tags in component templates.
- **`| safe` usage** — only on outputs already escaped via `html_attrs` or `Markup`. See `SECURITY.md`.
- **Variants/sizes validated** — use `validate_variant` / `validate_size` filters against `VARIANT_REGISTRY` / `SIZE_REGISTRY`. Unknown values fall back to default, not an error (unless strict mode is on).
- **Provided context keys** — use `{% provide _component_key = value %}` with underscore prefix for parent-to-child state flow across slot boundaries (requires kida ≥ 0.3.4). In child macros: `{% set _variant = (variant if variant else consume("_component_key", "")) | validate_variant(...) %}`. Explicit params always win over provided values. Avoid `{% set variant = ... %}` when `variant` is also a macro parameter — kida has a scoping issue; use a different variable name like `_variant`.
- **Error boundaries (kida 0.4.0)** — use `{% try %}...{% fallback [error] %}...{% end %}` to catch render-time exceptions and show fallback content. `suspense_slot` uses this automatically. The optional `error` variable exposes `message`, `type`, `template`, `line`.
- **Scoped slots (kida 0.4.0)** — `{% slot name let:var=expr %}` in defs exposes variables to the caller's slot body (caller uses `{% slot name let:var %}`). Use for inversion-of-control patterns where the parent templates child-provided data. Provide/consume remains correct for deep cross-macro context propagation.
- **List comprehensions (kida 0.4.0)** — `[expr for var in iterable if condition]` supported in template expressions.
- **CSS motion tokens** — animations must use `--chirpui-duration-*` / `--chirpui-easing-*` tokens, not raw values. The `test_transition_tokens.py` test enforces this.
- **Template CSS contract** — every CSS class referenced in templates must exist in `chirpui.css`. The `test_template_css_contract.py` test enforces this.
- **Filter bar vs filter chips vs filter row** — `filter_bar.html` = form + `action_strip` for list/table toolbars; `filter_row` (same file) = lightweight cluster form for 2-3 inline controls with HTMX. `filter_chips.html` = `filter_group` + `filter_chip` for faceted pill rows (HTMX, `register_colors`). See `docs/COMPONENT-OPTIONS.md`.
- **Install snippet** — `code.html` provides `install_snippet(command)` for pre-formatted shell commands with a copy button. Uses `x-data="chirpuiCopy()"`.
- **Tag browse composite** — `tag_browse.html` provides `tag_browse_tray`, `tag_selection_badges`, `tag_filter_actions` for tag-filtered listings. Plugs into `resource_index` slots.
- **Settings row** — `settings_row.html` provides `settings_row_list` (container with hoverable/divided/relaxed modifiers) and `settings_row` (label + auto-inferred status badge + monospace detail).
- **Layout overflow** — App shell main clips horizontal bleed; `grid()` applies **`min-width: 0`** to direct children in CSS; use `block()` for **`span=`** / bento cells. Pair with `cluster()` and wrapping `indicator_row()` so content does not widen the page. Use `frame()` for explicit hero/sidebar columns. Page/section/entity headers harden flex title columns; for other flex rows use **`chirpui-min-w-0`**. Custom grids need `min-width: 0` / `minmax(0, 1fr)` on tracks. For fixed bento-style column ratios, use `grid(..., preset=…)` (canonical names and aliases: `docs/LAYOUT-PRESETS.md`); use `items="start"` when row cells have unequal heights; use `preset="detail-two-single"` or `detail-two` + `detail_single=true` for a one-column detail row (see `docs/LAYOUT-OVERFLOW.md`). See also `docs/LAYOUT-GRIDS-AND-FRAMES.md`.
- **Card overline labels** — use `label_overline()` from `chirpui/label_overline.html` for small-caps section labels inside cards (optional `section=true`, `tag="h3"`).
- **HTMX attribute helper** — use `build_hx_attrs(hx_post=..., hx_target=...) | html_attrs` in templates instead of individual `{% if hx_* %}` blocks. `build_hx_attrs` converts underscores to hyphens; `html_attrs` skips `None` values and escapes output. Registered as a template global.
- **Boost-aware components** — components that accept `hx_target` must emit `hx-boost="false"` on `<a>` elements to prevent boost from hijacking the click. This is enforced by tabs, route_tabs, and button.
- **Safe-by-default forms** — the `form()` macro auto-adds `hx-select="unset"` and `hx-disinherit="hx-select"` when htmx is detected. Explicit `hx_select` overrides the default. No manual `hx-select="unset"` needed.
- **Fragment form pattern** — forms with `hx-post` inside boosted layouts get `hx-select="unset"` automatically (see above). Use `hx-swap="innerHTML transition:false"` (preserves wrapper, suppresses VT flash). See `docs/DND-FRAGMENT-ISLAND.md § Forms inside boosted layouts`.
- **OOB composition helpers** — `oob.html` provides `oob_fragment(id, swap)` for wrapping any content as an OOB swap, `oob_toast(message, variant)` as a shorthand for toast OOB, and `counter_badge(id, count, variant, oob)` for server-driven numeric indicators. See `docs/COMPONENT-OPTIONS.md § OOB Helpers`.
- **Form field a11y** — every field has `id="field-{name}"` (OOB target), `aria-describedby="errors-{name}"` on controls, and a `<div id="errors-{name}" role="alert" aria-live="polite">` error container (always in DOM, empty when no errors). Use `form_error_summary(errors)` at form top for an alert-style error count with anchor links to fields. Fields support `oob=true` on `field_wrapper` for per-field OOB swap.
- **Suspense slots** — `suspense.html` provides `suspense_slot(id)` and `suspense_group()` for skeleton-to-content swap patterns. Pairs with Chirp's `Suspense(defer_map={})` — the server renders the shell with skeleton placeholders, then sends deferred content as OOB swaps targeting each slot's `id`. Use `suspense_group` to mark a region `aria-busy="true"` until all child slots resolve. `suspense_slot` wraps content in a kida `{% try %}` error boundary — if the skeleton or caller content fails to render, a default skeleton is shown instead of crashing the page. See `docs/COMPONENT-OPTIONS.md § Suspense`.
- **Marketing site shell** — `site_shell.html`, `site_header.html`, `site_footer.html` provide a full-page scroll layout alternative to `app_shell`. Use for marketing sites, landing pages, and docs homes. `site_shell` manages z-index stacking context so sticky headers always stay on top. `site_header` has layout variants (`start`, `center-brand`, `center-nav`, `split`) and surface variants (`glass`, `solid`, `transparent`). `site_footer` has layout variants (`columns`, `centered`, `simple`). See `docs/COMPONENT-OPTIONS.md § Marketing Kit`.
- **Marketing content sections** — `band.html` provides full-bleed section panels with width variants (`inset`, `bleed`, `contained`) and pattern integration. `feature_section.html` provides two-column copy+media layouts with layout variants (`split`, `balanced`, `media-dominant`, `stacked`), surface variants (`default`, `muted`, `halo`), and a `reverse` modifier for zigzag patterns. `feature_stack` wraps multiple feature sections with consistent spacing.
- **Bento extensions** — `chirpui-surface--bento` adds hover lift + flex height equalization to surfaces. `chirpui-frame--bento` applies consistent gap and min-height to bento frames. `chirpui-block--wide` / `chirpui-block--tall` span 2 grid columns/rows. Surface typography elements: `chirpui-surface__eyebrow`, `__title`, `__lede`, `__body`.
- **Navigation progress** — `nav_progress.html` provides a CSS-only fixed progress bar at the viewport top. Animates automatically via `body.htmx-request`. Use outside `app_shell` (which has its own built-in bar). Place once in base layout: `{{ nav_progress() }}`.
- **SSE connection status** — `sse_status.html` provides `sse_status(state)` (connected/disconnected/error indicator with dot + label) and `sse_retry(url)` (htmx-powered retry button for reconnecting to an SSE endpoint). Pair with `streaming_bubble`/`streaming_block` from `streaming.html`. See `docs/COMPONENT-OPTIONS.md § SSE Status`.

## Warning system

chirp-ui uses Python's `warnings` module (not `logging`) for developer feedback. Three warning classes in `chirp_ui.validation`:

- **`ChirpUIValidationWarning`** — invalid variant/size/input silently corrected. In strict mode (`set_strict(True)`), escalates to `ValueError`.
- **`ChirpUIDeprecationWarning`** — deprecated feature. Always warns (never raises, even in strict mode).
- **`ChirpUIWarning`** — base class for all chirp-ui warnings.

Developers filter with standard `-W` flags: `python -W ignore::ChirpUIValidationWarning` to silence, or `-W error::ChirpUIValidationWarning` to crash on invalid input.

## `hx={}` dict pattern

Macros with many htmx parameters (`btn`, `icon_btn`, `form`) accept an `hx=none` dict as shorthand. Keys are short htmx names without the `hx-` prefix:

```html
{{ btn("Save", hx={"post": "/save", "target": "#result", "swap": "innerHTML"}) }}
```

Individual `hx_*` kwargs still work and override keys from the `hx` dict. `build_hx_attrs(hx=dict, **kwargs)` merges both, drops `None` values.

## Deprecation policy

- **`channel_card(use_slots=...)`** — always use named slots (`body`, `actions`). The `use_slots` parameter will be removed in a future release.
- **`section_header_inline`** — use `section_header(variant="inline")` instead.

## Adding a component

1. Add `src/chirp_ui/templates/chirpui/<name>.html` — Kida macro (e.g. `label_overline.html`).
2. Add styles to `chirpui.css` under a `/* <name> */` section comment.
3. Add any new variants/sizes to `VARIANT_REGISTRY` / `SIZE_REGISTRY` in `validation.py`.
4. For htmx-enabled components, use `build_hx_attrs(...) | html_attrs` instead of individual `{% if hx_* %}` blocks.
5. Add render tests to `tests/test_components.py`.
6. Run `uv run poe ci` before opening a PR.

## Testing without Chirp

`tests/conftest.py` provides a `env` fixture that loads templates via `FileSystemLoader` and stubs all Chirp-provided filters (`bem`, `field_errors`, `html_attrs`, `island_attrs`, etc.). Tests should use this fixture — no real Chirp app required.

## Relationship to the Bengal ecosystem

chirp-ui is one optional layer. Users bring their own Chirp app; chirp-ui adds the component library and default design language. The framework (`bengal-chirp`) and template engine (`kida-templates`) are separate packages maintained by the same author.

**Alpine.js ownership:** Chirp is the single authority for Alpine injection. `use_chirp_ui(app)` auto-enables `alpine=True` on the app config; `app_shell_layout.html` does **not** include Alpine scripts. Named components should register with `Alpine.safeData(name, factory)` (injected by Chirp) for htmx-safe registration that works on both full page loads and boosted navigation swaps.

**JSON in `x-data`:** Prefer Chirp’s `{{ alpine_json_config("my-id", config) }}` (registered when `alpine=True`) to emit the JSON `<script>` tag with a safe id; or hand-write `<script type="application/json">` with `{{ config | tojson }}`. For JSON directly in a double-quoted attribute, use `{{ config | tojson(attr=true) }}` (or single-quoted attributes with default `tojson`). See Kida’s filter reference and Chirp’s Alpine guide.

**`page_scripts` block:** `app_shell_layout.html` defines an empty `{% block page_scripts %}{% end %}` near `</body>`. This block is only overridable by templates that `{% extends %}` the layout directly (e.g. inner `_layout.html` files). **Filesystem page templates** (`page.html`) are composed into the layout via `render_with_blocks` — they cannot override `page_scripts` or any other sibling block in the layout. If a page needs an inline `<script>` (e.g. for `Alpine.safeData` registration), put it inside the content block (`page_root` or `page_content`), not in a separate `page_scripts` block. See Chirp's filesystem-routing docs for details.

## Troubleshooting: "all interactive components are dead"

If theme toggles, style toggles, command palette, sidebar collapse, dropdowns,
and modals all stop working at once, Alpine.js is not loading. Diagnosis:

1. **Open browser DevTools → Elements** — look for `<script data-chirp="alpine">` near `</body>`.
   - **Missing entirely?** `AlpineInject` is being skipped. Check if the string
     `data-chirp="alpine"` appears elsewhere in the HTML (false-positive dedup).
   - **Present but `window.Alpine` is undefined?** The CDN URL is wrong. Check
     the `src` attribute — it must end with `/dist/cdn.min.js`, not a bare
     `@version`. A bare jsDelivr path resolves to CommonJS (`dist/module.cjs.js`)
     which silently fails in browsers. See Chirp's `CLAUDE.md § Alpine.js Injection`.
2. **Check Console** — "Script error." at line 0 = cross-origin script failure
   (CORS masks the real error). This confirms the CDN script didn't execute.
3. **`poe dev-sync` not picking up fix?** If Chirp's workspace source has the fix
   but the installed package doesn't, `uv` may cache the old wheel when the version
   number is unchanged. Fix: `rm -rf .venv && poe dev-sync` to force a clean rebuild.
