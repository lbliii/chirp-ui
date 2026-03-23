# chirp-ui

An optional companion UI layer for the Chirp web framework — Kida template macros (cards, modals, forms, layouts) that render as HTML, styled with modern CSS.

## Stack

| Layer | Package |
|-------|---------|
| Template engine | [kida-templates](https://github.com/lbliii/kida) — Jinja2-like, `PackageLoader`, `{% slot %}` |
| Web framework | [bengal-chirp](https://github.com/lbliii/chirp) — optional; `chirp-ui` works standalone |
| Interactivity | Alpine.js (CDN, no build step) + htmx for swaps/SSE |
| CSS | `chirpui-*` CSS custom properties, `color-mix()`, `:has()`, container queries |
| Python | 3.14+ (free-threading ready, `_Py_mod_gil = 0`) |

## Project layout

```
src/chirp_ui/
  __init__.py          # get_loader(), register_filters(), static_path()
  filters.py           # bem, html_attrs, validate_*, register_colors, resolve_color, sanitize_color, contrast_text
  validation.py        # VARIANT_REGISTRY, SIZE_REGISTRY, set_strict()
  route_tabs.py        # route-aware tabs helper
  templates/chirpui/   # Kida macros — one file per component
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

## Dev commands

```bash
uv sync --group dev      # install deps
uv run pytest -q         # tests
uv run ruff check .      # lint
uv run ruff format .     # format
uv run ty check src/     # type check (Astral ty, Rust-based)
uv run poe ci            # full CI: lint + format + CSS + ty + tests
```

Or via Make: `make test`, `make lint`, `make ty`, `make ci` (see `Makefile`).

## Key conventions

- **BEM class names** — all CSS classes use `chirpui-<block>` and `chirpui-<block>--<modifier>`.
- **Kida macros** — components are `{% macro %}` / `{% call %}` pairs using `{% slot %}` for content injection. No wrapper divs without good reason.
- **No client JS in macros** — Alpine.js `x-data` attributes only; no `<script>` tags in component templates.
- **`| safe` usage** — only on outputs already escaped via `html_attrs` or `Markup`. See `SECURITY.md`.
- **Variants/sizes validated** — use `validate_variant` / `validate_size` filters against `VARIANT_REGISTRY` / `SIZE_REGISTRY`. Unknown values fall back to default, not an error (unless strict mode is on).
- **CSS motion tokens** — animations must use `--chirpui-duration-*` / `--chirpui-easing-*` tokens, not raw values. The `test_transition_tokens.py` test enforces this.
- **Template CSS contract** — every CSS class referenced in templates must exist in `chirpui.css`. The `test_template_css_contract.py` test enforces this.
- **Filter bar vs filter chips** — `filter_bar.html` = form + `action_strip` for list/table toolbars. `filter_chips.html` = `filter_group` + `filter_chip` for faceted pill rows (HTMX, `register_colors`). See `docs/COMPONENT-OPTIONS.md`.

## Adding a component

1. Add `src/chirp_ui/templates/chirpui/<name>.html` — Kida macro.
2. Add styles to `chirpui.css` under a `/* <name> */` section comment.
3. Add any new variants/sizes to `VARIANT_REGISTRY` / `SIZE_REGISTRY` in `validation.py`.
4. Add render tests to `tests/test_components.py`.
5. Run `uv run poe ci` before opening a PR.

## Testing without Chirp

`tests/conftest.py` provides a `env` fixture that loads templates via `FileSystemLoader` and stubs all Chirp-provided filters (`bem`, `field_errors`, `html_attrs`, `island_attrs`, etc.). Tests should use this fixture — no real Chirp app required.

## Relationship to the Bengal ecosystem

chirp-ui is one optional layer. Users bring their own Chirp app; chirp-ui adds the component library and default design language. The framework (`bengal-chirp`) and template engine (`kida-templates`) are separate packages maintained by the same author.
