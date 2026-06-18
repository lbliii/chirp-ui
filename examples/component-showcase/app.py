"""chirp-ui Component Showcase — spin up to see all components.

Requires: pip install -e ".[showcase]"
Run: python examples/component-showcase/app.py
"""

from __future__ import annotations

import os
from pathlib import Path

from chirp import App, AppConfig, Fragment, Request, Response, use_chirp_ui

from routes import components, demos, screens, shells
from showcase.search import search_index_json

TEMPLATES_DIR = Path(__file__).parent / "templates"

# Use source chirp-ui templates (many components not yet in installed package)
_CHIRPUI_SRC_TEMPLATES = Path(__file__).resolve().parents[2] / "src" / "chirp_ui" / "templates"

app = App(
    AppConfig(
        template_dir=TEMPLATES_DIR,
        debug=False,
        view_transitions=True,
        delegation=True,
        islands=True,
        component_dirs=(_CHIRPUI_SRC_TEMPLATES,) if _CHIRPUI_SRC_TEMPLATES.is_dir() else (),
    )
)
use_chirp_ui(app)


@app.route("/toast", methods=["POST"])
async def show_toast(request: Request) -> Fragment:
    return Fragment("_toast.html", "toast_demo")


@app.route("/showcase/pages.json")
async def showcase_pages_json(request: Request) -> Response:
    return Response(search_index_json(), media_type="application/json; charset=utf-8")


demos.register(app)
components.register(app)
shells.register(app)
screens.register(app)


if __name__ == "__main__":
    # Railway (and other PaaS) inject $PORT and route to a process bound on
    # 0.0.0.0. With no $PORT set we fall back to Chirp's defaults (127.0.0.1:8000)
    # so `python examples/component-showcase/app.py` keeps working locally.
    port = os.environ.get("PORT")
    if port:
        app.run(host="0.0.0.0", port=int(port))
    else:
        app.run()
