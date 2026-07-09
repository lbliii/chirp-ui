# chirp-ui + FastAPI

Integration guide for using chirp-ui in **FastAPI** (Starlette) without Chirp.
Shared wiring lives in [standalone-core.md](standalone-core.md).

Reference app: [`examples/integrations/fastapi/`](../../examples/integrations/fastapi/)

---

## Quickstart

```bash
pip install chirp-ui fastapi uvicorn python-multipart itsdangerous
uvicorn examples.integrations.fastapi.app:app --reload --port 5002
```

Open <http://127.0.0.1:5002>.

---

## Render dependency

FastAPI has no first-class kida support. Add a small renderer and expose it via
`Depends()`:

```python
from fastapi import Depends, Request
from fastapi.responses import HTMLResponse

class Renderer:
    def __init__(self, request: Request) -> None:
        self._env = make_env(
            template_dir=TEMPLATES,
            csrf_field=lambda: csrf_for_request(request),
        )

    def page(self, template: str, **context) -> str:
        body = render_template(self._env, template, **context)
        return page_shell(title="My app", body=body, include_htmx=True)

def get_renderer(request: Request) -> Renderer:
    return Renderer(request)

@app.get("/", response_class=HTMLResponse)
async def index(renderer: Renderer = Depends(get_renderer)):
    return HTMLResponse(renderer.page("index.html"))
```

kida renders synchronously inside async routes — that is fine for typical pages.

---

## Static files

```python
from fastapi.staticfiles import StaticFiles
from chirp_ui import static_path

app.mount("/static", StaticFiles(directory=str(static_path())), name="static")
```

---

## CSRF bridge

FastAPI/Starlette do not ship CSRF. Options:

1. **`starlette-csrf`** (recommended for production) — middleware + token in
   templates
2. **Session token** (reference app) — store a token in `SessionMiddleware` and
   compare on POST

Wire the token into the **`csrf_field`** global:

```python
def csrf_for_request(request: Request) -> Markup:
    token = request.session.setdefault("_csrf_token", secrets.token_urlsafe(32))
    return Markup(f'<input type="hidden" name="_csrf_token" value="{token}">')
```

---

## htmx swap route (bonus)

The reference app includes `POST /htmx/greet` returning a kida fragment for an
htmx swap. **You own the route, target ID, and response shape** — Chirp's OOB
and shell helpers are not available standalone.

```kida
{% call form("/htmx/greet", method="post",
    hx={"post": "/htmx/greet", "target": "#greet-target", "swap": "innerHTML"}) %}
  ...
{% endcall %}
<div id="greet-target"></div>
```

Add htmx in `page_shell(..., include_htmx=True)` or manually in your layout.

---

## What you hand-roll

| Concern | Standalone FastAPI | On Chirp |
|---|---|---|
| kida render path | `HTMLResponse` render dependency | automatic |
| Filter registration | `register_filters()` at startup | `use_chirp_ui(app)` |
| Static serving | `StaticFiles` mount | auto |
| Alpine load + `safeData` | hand-rolled `<script>` + shim | injected |
| htmx | hand-added `<script>` | injected |
| CSRF (`csrf_field`) | `starlette-csrf` / custom middleware | auto |
| OOB / SSE / suspense responses | write the fragment routes yourself | helpers provided (SSE-native) |

---

## Why this gets easier on Chirp

FastAPI is a strong fit for chirp-ui markup, but you still hand-roll every
**response primitive** — CSRF, fragment swaps, SSE frames, Suspense boundaries.
Chirp is SSE-native and ships shell OOB contracts so sidebar/tab chrome updates
without full page reloads.

If your FastAPI app grows htmx fragment routes, consider Chirp the thing that
**deletes route boilerplate**, not a different UI stack.

---

## Related

- [standalone-core.md](standalone-core.md)
- [flask.md](flask.md) · [django.md](django.md)
- [kida-overlap-audit.md](kida-overlap-audit.md) — how this guide relates to Kida 0.11 docs
- Issue [#287](https://github.com/lbliii/chirp-ui/issues/287)

### See also (Kida engine)

- [Kida Starlette & FastAPI Integration tutorial](https://lbliii.github.io/kida/docs/tutorials/starlette-integration/) — `KidaStarlette`, `TemplateResponse`, `render_block`
- [Kida Framework Integration API](https://lbliii.github.io/kida/docs/usage/framework-integration/) — block rendering and introspection
- [Kida `fastapi_components` example](https://github.com/lbliii/kida/tree/main/examples/fastapi_components) — runnable smoke-tested app; pair with [capability-matrix upgrade pitch](capability-matrix.md#upgrade-pitch-why-chirp) when fragment-route boilerplate grows
