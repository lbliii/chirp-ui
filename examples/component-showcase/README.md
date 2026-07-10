# chirp-ui Component Showcase

Spin up a Chirp app to browse all chirp-ui components.

**Live deploy:** https://chirp-ui-showcase-production.up.railway.app

## Run locally

**Option A — pip (standalone):**

```bash
cd /path/to/chirp-ui
pip install -e ".[showcase]"   # installs chirp-ui + chirp + kida-templates
python examples/component-showcase/app.py
```

**Option B — uv (from b-stack workspace root):**

```bash
cd /path/to/b-stack
uv sync
uv run python chirp-ui/examples/component-showcase/app.py
```

Then open http://localhost:8000.

The appearance/tone pilot lives at `/appearance-tone` and shows the shared
macro-parameter vocabulary across buttons, badges, alerts, cards, surfaces, and
fields.

The curated theme-pack gallery lives at `/theme-packs` and renders the packaged
Atlas, Ember, and Sage token packs across light, dark, and system modes.

> **Note:** The showcase extra installs `bengal-chirp>=0.10.0` (CSP nonce
> auto-wiring via `use_chirp_ui`), `kida-templates>=0.9.0`, and
> `itsdangerous>=2.2.0` for Chirp's session middleware import. If you see
> `ModuleNotFoundError`, ensure you're using the same Python environment where
> the showcase extra was installed.
>
> **CI parity:** `uv sync --group dev` installs the same Chirp + pytest-asyncio
> deps CI uses for showcase HTTP integration (`tests/test_data_integration.py`).
> No hidden `--group browser` requirement for route smoke.

## Optional: Holy Light theme

Add to your base template's `{% block head %}`:

```html
<link rel="stylesheet" href="/static/themes/holy-light.css">
```

## Page registry

Every navigable showcase route is declared once in
`examples/component-showcase/showcase/registry.py`. The registry drives:

- sidebar sections in `templates/base.html`,
- the home index hierarchy (`/`),
- command-palette search (⌘K / Ctrl+K),
- and route ratchets in `tests/test_showcase_registry.py`.

Route handlers live in thin modules under `examples/component-showcase/routes/`;
fixture data lives in `examples/component-showcase/fixtures/`. The entrypoint
`app.py` only wires config, CSP, and `register()` calls.

## Add a showcase page

1. **Registry entry** — add a `ShowcasePage(...)` to `showcase/registry.py`
   (`path`, `title`, `section`, optional `description`, `tags`, flags).
2. **Template** — add `templates/showcase/your_page.html` (extend `base.html`,
   fill `{% block main %}`).
3. **Route** — add a one-liner in the matching `routes/*.py` module using
   `page(request, "showcase/your_page.html", ...)`.
4. **Ratchet** — run `uv run pytest tests/test_showcase_registry.py -q` so the
   new path is covered by the registry ↔ route sync test.
5. **Smoke** — open the page locally and confirm sidebar highlight + palette
   search find it.

POST handlers, HTMX fragments, and SSE streams use `hidden=True` and
`show_in_sidebar=False` in the registry.

**Fragment routes:** `Fragment("template.html", "block_name", ...)` requires a
matching `{% block block_name %}` in that template. Kida does not implement
`{{ super() }}` — use `{% include "partial.html" %}` for shared head/body markup.
See [`docs/fundamentals/composition.md`](../../docs/fundamentals/composition.md#kida-block-inheritance--override-only-no-super).
Ratchets: `tests/test_kida_template_contracts.py`.

## Railway smoke checklist

After deploying to https://chirp-ui-showcase-production.up.railway.app:

1. **Home** — `/` loads; golden screens, shell recipes, and component gallery
   sections render.
2. **Search** — ⌘K / Ctrl+K opens the palette; filter `catalog` → navigate to
   `/catalog-shell`; filter `command` → navigate to `/screen-command-center`.
3. **Shell recipes** — each returns **200** (not 500) with no CSP console errors:
   - `/catalog-shell`
   - `/support-shell`
   - `/operations-shell`
4. **Composer page** — `/composer` loads; browser console has no
   `chirpuiComposer is not defined` (hard-refresh if `chirpui-alpine.js` is stale
   after deploy).
5. **Composer POST** — `POST /composer/send` with `message=hello` returns **200**
   and HTML containing `chirpui-message-bubble--right` (not 500 / missing block).
6. **Interactive demo** — `/demo` loads and submits without CSP console errors.
7. **Golden screen** — `/screen-command-center` loads with shell CSS scoped to
   the page (no missing-style flash).

**Automated curl gate** (copy-paste after deploy):

```bash
./scripts/showcase_deploy_smoke.sh
# local: SHOWCASE_URL=http://127.0.0.1:8000 ./scripts/showcase_deploy_smoke.sh
```

If any step fails, check the browser console for CSP nonce violations and confirm
the deploy image installed `bengal-chirp>=0.10.0` via `pip install ".[showcase]"`.
Browser proof for composer Enter-to-send:
`uv sync --group browser && playwright install chromium && pytest tests/browser/test_composer_gauntlet.py -q`.
