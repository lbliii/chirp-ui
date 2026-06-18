"""Minimal FastAPI + chirp-ui reference app (#287).

Run from repo root::

    pip install chirp-ui fastapi uvicorn python-multipart itsdangerous
    uvicorn examples.integrations.fastapi.app:app --reload --port 5002
"""

from __future__ import annotations

import secrets
import sys
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from kida.template import Markup
from starlette.middleware.sessions import SessionMiddleware

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "_shared"))

from chirpui_bootstrap import make_env, page_shell, render_template, static_root  # noqa: E402

app = FastAPI(title="chirp-ui FastAPI demo")
app.add_middleware(SessionMiddleware, secret_key="dev-only-change-me")
app.mount("/static", StaticFiles(directory=str(static_root())), name="static")


def _csrf_field(request: Request) -> Markup:
    token = request.session.get("_csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        request.session["_csrf_token"] = token
    return Markup(f'<input type="hidden" name="_csrf_token" value="{token}">')


def _env_for(request: Request):
    return make_env(
        template_dir=ROOT / "templates",
        csrf_field=lambda: _csrf_field(request),
    )


class Renderer:
    def __init__(self, request: Request) -> None:
        self._request = request
        self._env = _env_for(request)

    def page(self, template: str, **context: object) -> str:
        body = render_template(self._env, template, **context)
        return page_shell(title="FastAPI + chirp-ui", body=body, include_htmx=True)

    def fragment(self, template: str, **context: object) -> str:
        return render_template(self._env, template, **context)


def get_renderer(request: Request) -> Renderer:
    return Renderer(request)


@app.get("/", response_class=HTMLResponse)
async def index(renderer: Annotated[Renderer, Depends(get_renderer)]) -> HTMLResponse:
    return HTMLResponse(renderer.page("index.html", errors={}, name_value="", saved=False))


@app.post("/submit", response_class=HTMLResponse)
async def submit(
    request: Request,
    renderer: Annotated[Renderer, Depends(get_renderer)],
    name: str = Form(""),
    _csrf_token: str = Form(""),
) -> HTMLResponse:
    session_token = request.session.get("_csrf_token", "")
    if not session_token or _csrf_token != session_token:
        return HTMLResponse("Invalid CSRF token", status_code=403)

    cleaned = name.strip()
    errors: dict[str, list[str]] = {}
    if not cleaned:
        errors["name"] = ["Name is required."]
    saved = not errors
    return HTMLResponse(
        renderer.page("index.html", errors=errors, name_value=cleaned, saved=saved),
    )


@app.post("/htmx/greet", response_class=HTMLResponse)
async def htmx_greet(
    renderer: Annotated[Renderer, Depends(get_renderer)],
    name: str = Form(""),
) -> HTMLResponse:
    label = name.strip() or "stranger"
    return HTMLResponse(renderer.fragment("fragment.html", name=label))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=5002, reload=True)
