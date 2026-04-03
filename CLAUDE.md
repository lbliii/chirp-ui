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
  filters.py           # bem, html_attrs, validate_*, register_colors, resolve_color, sanitize_color, contrast_text
  validation.py        # VARIANT_REGISTRY, SIZE_REGISTRY, set_strict()
  route_tabs.py        # route-aware tabs helper
  templates/chirpui/   # Kida macros — one file per component (e.g. label_overline.html)
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

**UI vocabulary:** `docs/UI-LAYERS.md` — app shell vs page chrome vs **surface chrome** (component frames), shell regions, page fragment target IDs, and links to Chirp’s `chirp.shell_regions` constants.

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
- **CSS motion tokens** — animations must use `--chirpui-duration-*` / `--chirpui-easing-*` tokens, not raw values. The `test_transition_tokens.py` test enforces this.
- **Template CSS contract** — every CSS class referenced in templates must exist in `chirpui.css`. The `test_template_css_contract.py` test enforces this.
- **Filter bar vs filter chips** — `filter_bar.html` = form + `action_strip` for list/table toolbars. `filter_chips.html` = `filter_group` + `filter_chip` for faceted pill rows (HTMX, `register_colors`). See `docs/COMPONENT-OPTIONS.md`.
- **Layout overflow** — App shell main clips horizontal bleed; `grid()` applies **`min-width: 0`** to direct children in CSS; use `block()` for **`span=`** / bento cells. Pair with `cluster()` and wrapping `indicator_row()` so content does not widen the page. Use `frame()` for explicit hero/sidebar columns. Page/section/entity headers harden flex title columns; for other flex rows use **`chirpui-min-w-0`**. Custom grids need `min-width: 0` / `minmax(0, 1fr)` on tracks. For fixed bento-style column ratios, use `grid(..., preset=…)` (canonical names and aliases: `docs/LAYOUT-PRESETS.md`); use `items="start"` when row cells have unequal heights; use `preset="detail-two-single"` or `detail-two` + `detail_single=true` for a one-column detail row (see `docs/LAYOUT-OVERFLOW.md`). See also `docs/LAYOUT-GRIDS-AND-FRAMES.md`.
- **Card overline labels** — use `label_overline()` from `chirpui/label_overline.html` for small-caps section labels inside cards (optional `section=true`, `tag="h3"`).
- **Boost-aware components** — components that accept `hx_target` must emit `hx-boost="false"` on `<a>` elements to prevent boost from hijacking the click. This is enforced by tabs, route_tabs, and button.
- **Safe-by-default forms** — the `form()` macro auto-adds `hx-select="unset"` and `hx-disinherit="hx-select"` when htmx is detected. Explicit `hx_select` overrides the default. No manual `hx-select="unset"` needed.
- **Fragment form pattern** — forms with `hx-post` inside boosted layouts get `hx-select="unset"` automatically (see above). Use `hx-swap="innerHTML transition:false"` (preserves wrapper, suppresses VT flash). See `docs/DND-FRAGMENT-ISLAND.md § Forms inside boosted layouts`.

## Adding a component

1. Add `src/chirp_ui/templates/chirpui/<name>.html` — Kida macro (e.g. `label_overline.html`).
2. Add styles to `chirpui.css` under a `/* <name> */` section comment.
3. Add any new variants/sizes to `VARIANT_REGISTRY` / `SIZE_REGISTRY` in `validation.py`.
4. Add render tests to `tests/test_components.py`.
5. Run `uv run poe ci` before opening a PR.

## Testing without Chirp

`tests/conftest.py` provides a `env` fixture that loads templates via `FileSystemLoader` and stubs all Chirp-provided filters (`bem`, `field_errors`, `html_attrs`, `island_attrs`, etc.). Tests should use this fixture — no real Chirp app required.

## Relationship to the Bengal ecosystem

chirp-ui is one optional layer. Users bring their own Chirp app; chirp-ui adds the component library and default design language. The framework (`bengal-chirp`) and template engine (`kida-templates`) are separate packages maintained by the same author.

**Alpine.js ownership:** Chirp is the single authority for Alpine injection. `use_chirp_ui(app)` auto-enables `alpine=True` on the app config; `app_shell_layout.html` does **not** include Alpine scripts. Named components should register with `Alpine.safeData(name, factory)` (injected by Chirp) for htmx-safe registration that works on both full page loads and boosted navigation swaps.

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
