"""Minimal Chirp test app for browser integration tests.

This app mounts real chirp-ui components inside a real Chirp app shell with
hx-boost, Alpine.js, and all the runtime machinery that production apps use.
Each route exercises a specific nesting/interaction pattern.
"""

from __future__ import annotations

import os

from chirp import App, AppConfig
from chirp.ext.chirp_ui import use_chirp_ui
from chirp.http.request import Request
from chirp.http.response import Response
from chirp.templating.returns import Template


def create_app() -> App:
    """Create the test Chirp app with chirp-ui integration."""
    template_dir = os.path.join(os.path.dirname(__file__), "templates")

    app = App(
        AppConfig(
            template_dir=template_dir,
            debug=True,
            alpine=True,
            view_transitions=True,
        )
    )
    use_chirp_ui(app)

    # ── Navigation: boosted links between pages ──────────────────────

    @app.route("/")
    async def home(request: Request):
        return Template("home.html", page_title="Home")

    @app.route("/page-b")
    async def page_b(request: Request):
        return Template("page_b.html", page_title="Page B")

    # ── Fragment form: form inside boosted layout ────────────────────

    @app.route("/form")
    async def form_page(request: Request):
        return Template("form_page.html", page_title="Form Test")

    @app.route("/form/submit", methods=["POST"])
    async def form_submit(request: Request):
        return Response('<div id="form-result">Saved successfully</div>')

    # ── Tabs: server-driven htmx tabs ────────────────────────────────

    @app.route("/tabs")
    async def tabs_page(request: Request):
        return Template(
            "tabs_page.html",
            page_title="Tabs",
            active_tab="overview",
            tab_content="Overview content",
        )

    @app.route("/tabs/overview")
    async def tab_overview(request: Request):
        if request.is_fragment:
            return Response('<div id="tab-content-inner">Overview content</div>')
        return Template(
            "tabs_page.html",
            page_title="Tabs",
            active_tab="overview",
            tab_content="Overview content",
        )

    @app.route("/tabs/details")
    async def tab_details(request: Request):
        if request.is_fragment:
            return Response('<div id="tab-content-inner">Details content</div>')
        return Template(
            "tabs_page.html",
            page_title="Tabs",
            active_tab="details",
            tab_content="Details content",
        )

    # ── Modal: Alpine store-driven overlay ───────────────────────────

    @app.route("/modal")
    async def modal_page(request: Request):
        return Template("modal_page.html", page_title="Modal")

    # ── Dropdown: keyboard navigation ────────────────────────────────

    @app.route("/dropdown")
    async def dropdown_page(request: Request):
        return Template("dropdown_page.html", page_title="Dropdown")

    # ── Inline edit: display/edit/save cycle ─────────────────────────

    @app.route("/inline-edit")
    async def inline_edit_page(request: Request):
        return Template(
            "inline_edit_page.html",
            page_title="Inline Edit",
            current_value="Hello World",
        )

    @app.route("/inline-edit/edit")
    async def inline_edit_edit(request: Request):
        return Response(
            '<div id="edit-field">'
            '<form hx-post="/inline-edit/save" hx-target="#edit-field" hx-swap="innerHTML">'
            '<input name="value" value="Hello World" data-testid="edit-input">'
            '<button type="submit" data-testid="save-btn">Save</button>'
            '<button type="button" hx-get="/inline-edit/cancel" hx-target="#edit-field" '
            'hx-swap="innerHTML" data-testid="cancel-btn">Cancel</button>'
            "</form>"
            "</div>"
        )

    @app.route("/inline-edit/save", methods=["POST"])
    async def inline_edit_save(request: Request):
        return Response(
            '<div id="edit-field">'
            '<span data-testid="display-value">Saved Value</span>'
            '<button hx-get="/inline-edit/edit" hx-target="#edit-field" '
            'hx-swap="innerHTML" data-testid="edit-btn">Edit</button>'
            "</div>"
        )

    @app.route("/inline-edit/cancel")
    async def inline_edit_cancel(request: Request):
        return Response(
            '<div id="edit-field">'
            '<span data-testid="display-value">Hello World</span>'
            '<button hx-get="/inline-edit/edit" hx-target="#edit-field" '
            'hx-swap="innerHTML" data-testid="edit-btn">Edit</button>'
            "</div>"
        )

    # ── Client-side tabs: Alpine tabs_panels ─────────────────────────

    @app.route("/tabs-panels")
    async def tabs_panels_page(request: Request):
        return Template("tabs_panels_page.html", page_title="Client Tabs")

    # ── Fill mode: auto-toggle on htmx settle ────────────────────────

    @app.route("/fill")
    async def fill_page(request: Request):
        return Template("fill_page.html", page_title="Fill Mode")

    @app.route("/no-fill")
    async def no_fill_page(request: Request):
        return Template("no_fill_page.html", page_title="No Fill")

    return app
