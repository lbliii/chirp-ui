"""Copyable filesystem-routed app chrome fixture."""

from __future__ import annotations

from html import escape
from pathlib import Path

from chirp import App, AppConfig
from chirp.ext.chirp_ui import use_chirp_ui
from chirp.http.request import Request
from chirp.http.response import Response
from chirp.pages import Section, TabItem

PAGES_DIR = Path(__file__).with_name("pages")


def create_app() -> App:
    app = App(
        AppConfig(
            template_dir=PAGES_DIR,
            debug=True,
            alpine=True,
            view_transitions=True,
            skip_contract_checks=True,
        )
    )
    use_chirp_ui(app)

    app.register_section(
        Section(
            id="fs_workspace",
            label="Workspace",
            tab_items=(
                TabItem("Overview", "/workspace", badge="3", match="exact"),
                TabItem("Runs", "/workspace/runs", badge="8", match="exact"),
            ),
            breadcrumb_prefix=({"label": "Filesystem App", "href": "/workspace"},),
            active_prefixes=("/workspace",),
        )
    )
    app.register_section(
        Section(
            id="fs_admin",
            label="Admin",
            tab_items=(
                TabItem("Access", "/admin", badge="2", match="exact"),
                TabItem("Audit", "/admin/audit", match="exact"),
            ),
            breadcrumb_prefix=({"label": "Filesystem App", "href": "/workspace"},),
            active_prefixes=("/admin",),
        )
    )

    @app.route("/fs-search")
    async def filesystem_search(request: Request):
        q = request.query.get("q", "")
        if not q:
            return Response('<div class="chirpui-command-palette__empty">No results</div>')
        result = escape(q, quote=True)
        return Response(f'<div class="chirpui-command-palette__item">Result for {result}</div>')

    app.mount_pages(str(PAGES_DIR))
    return app
