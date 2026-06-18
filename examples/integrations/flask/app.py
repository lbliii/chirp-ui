"""Minimal Flask + chirp-ui reference app (#286).

Run from repo root::

    pip install chirp-ui flask flask-wtf
    python examples/integrations/flask/app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from flask import Flask, Response, request, send_from_directory
from flask_wtf.csrf import CSRFProtect, generate_csrf
from kida.template import Markup

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "_shared"))

from chirpui_bootstrap import make_env, page_shell, render_template, static_root  # noqa: E402

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-only-change-me"
CSRFProtect(app)


def _csrf_field() -> Markup:
    return Markup(f'<input type="hidden" name="csrf_token" value="{generate_csrf()}">')


env = make_env(template_dir=ROOT / "templates", csrf_field=_csrf_field)


def _render_page(template: str, **context: object) -> str:
    body = render_template(env, template, **context)
    return page_shell(title="Flask + chirp-ui", body=body)


@app.get("/")
def index() -> Response:
    return Response(
        _render_page("index.html", errors={}, name_value="", saved=False), mimetype="text/html"
    )


@app.post("/submit")
def submit() -> Response:
    name = (request.form.get("name") or "").strip()
    errors: dict[str, list[str]] = {}
    if not name:
        errors["name"] = ["Name is required."]
    saved = not errors
    return Response(
        _render_page("index.html", errors=errors, name_value=name, saved=saved),
        mimetype="text/html",
    )


@app.get("/static/<path:filename>")
def chirpui_static(filename: str) -> Response:
    directory = static_root()
    target = (directory / filename).resolve()
    if not str(target).startswith(str(directory.resolve())) or not target.is_file():
        return Response("Not Found", status=404)
    return send_from_directory(directory, filename)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
