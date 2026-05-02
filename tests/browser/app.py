"""Minimal Chirp test app for browser integration tests.

This app mounts real chirp-ui components inside a real Chirp app shell with
hx-boost, Alpine.js, and all the runtime machinery that production apps use.
Each route exercises a specific nesting/interaction pattern.
"""

import os

from chirp import App, AppConfig
from chirp.ext.chirp_ui import use_chirp_ui
from chirp.http.request import Request
from chirp.http.response import Response
from chirp.templating.returns import Template

GAUNTLET_NAV_ITEMS = [
    {
        "title": "Workspace with a very long branch label",
        "href": "/gauntlet/workspace",
        "open": True,
        "active": True,
        "badge": 128,
        "children": [
            {"title": "Overview", "href": "/gauntlet/workspace/overview", "active": True},
            {"title": "Members", "href": "/gauntlet/workspace/members", "badge": 12},
            {
                "title": "Nested section with server-owned children",
                "href": "/gauntlet/workspace/nested",
                "open": True,
                "children": [
                    {"title": "Deep child", "href": "/gauntlet/workspace/nested/deep"},
                    {
                        "title": "Muted archived child with a long title",
                        "href": "/gauntlet/workspace/nested/archive",
                        "muted": True,
                    },
                ],
            },
        ],
    },
    {
        "title": "Closed branch still routes",
        "href": "/gauntlet/closed",
        "children": [
            {"title": "Hidden until open", "href": "/gauntlet/closed/hidden"},
        ],
    },
    {"title": "Plain leaf", "href": "/gauntlet/plain"},
]

GAUNTLET_DETAIL_NAV_ITEMS = [
    {
        "title": "Hinted route branch",
        "href": "/gauntlet/contextual/branch",
        "hint": "Branch parents stay route links while detail appears on hover and focus.",
        "hint_position": "right",
        "open": True,
        "badge": 3,
        "children": [
            {
                "title": "Hinted child link",
                "href": "/gauntlet/contextual/child",
                "hint": "Child entries inherit the same item hint contract.",
            },
            {"title": "Plain child", "href": "/gauntlet/contextual/plain"},
        ],
    },
    {
        "title": "Closed hinted branch",
        "href": "/gauntlet/contextual/closed",
        "hint": "Closed branches still expose their route and do not render hidden children.",
        "children": [{"title": "Hidden detail child", "href": "/gauntlet/contextual/hidden"}],
    },
]


GAUNTLET_ROUTE_TABS = [
    {"label": "Overview", "href": "/gauntlet", "match": "exact", "badge": 4},
    {"label": "Activity", "href": "/gauntlet/activity", "match": "prefix"},
    {"label": "Settings With A Long Label", "href": "/gauntlet/settings", "match": "prefix"},
    {"label": "Audit", "href": "/gauntlet/audit", "match": "prefix", "badge": 999},
]


GAUNTLET_TABLE_ROWS = [
    ("Alpha Corridor", "Active", "42", "Stable short cell"),
    ("Beta Intake", "Paused", "7", "Wrapped metadata with several short words"),
    (
        "Gamma Archive",
        "Needs review",
        "128",
        "unbroken-token-0123456789abcdefghijklmnopqrstuvwxyz",
    ),
]

PRODUCT_PATTERN_CUSTOMERS = [
    "Klarna",
    "Vanta",
    "Clay",
    "Rippling",
    "Lyft",
    "Gong",
    "Harvey",
    "Cloudflare",
]

PRODUCT_PATTERN_LOGOS = [{"name": name} for name in PRODUCT_PATTERN_CUSTOMERS]

PRODUCT_PATTERN_PRODUCTS = [
    {
        "href": "/product-page-patterns/observe",
        "name": "Observability",
        "summary": "Trace runs, inspect tool calls, and understand failures.",
        "kind": "Platform",
    },
    {
        "href": "/product-page-patterns/evaluate",
        "name": "Evaluation",
        "summary": "Score behavior with reusable test cases and human review.",
        "kind": "Workflow",
    },
    {
        "href": "/product-page-patterns/deploy",
        "name": "Deployment",
        "summary": "Ship durable agent services with memory and checkpoints.",
        "kind": "Runtime",
    },
]

PRODUCT_PATTERN_STORIES = [
    {
        "customer": "Klarna",
        "outcome": "Reduced support resolution time",
        "metric": "80%",
        "summary": "A shared tracing and evaluation loop helped support agents improve faster.",
        "href": "/product-page-patterns/stories/klarna",
    },
    {
        "customer": "Monday Service",
        "outcome": "Faster evaluation feedback",
        "metric": "8.7x",
        "summary": "Production traces became reusable eval cases for each agent iteration.",
        "href": "/product-page-patterns/stories/monday",
    },
    {
        "customer": "Podium",
        "outcome": "Fewer engineering escalations",
        "metric": "90%",
        "summary": "Observable agent runs gave operators enough context to resolve issues.",
        "href": "/product-page-patterns/stories/podium",
    },
]

GAUNTLET_ROOMS = {
    "all": "All rooms",
    "primitives": "Primitive room",
    "rhythm": "Control rhythm room",
    "navigation": "Navigation room",
    "forms": "Forms room",
    "data": "Data room",
    "workflow": "Workflow room",
    "linkability": "Linkability room",
    "contextual": "Contextual detail room",
    "actions": "Actions in entries room",
    "swaps": "HTMX swap room",
    "content": "Hostile content room",
    "density": "Dense records room",
    "states": "State matrix room",
    "edges": "Viewport edge room",
    "hostile": "Hostile room",
}


def _gauntlet_context(active_room: str = "all") -> dict[str, object]:
    room = active_room if active_room in GAUNTLET_ROOMS else "all"
    return {
        "page_title": f"Gauntlet: {GAUNTLET_ROOMS[room]}",
        "active_room": room,
        "rooms": GAUNTLET_ROOMS,
        "nav_items": GAUNTLET_NAV_ITEMS,
        "detail_nav_items": GAUNTLET_DETAIL_NAV_ITEMS,
        "gauntlet_route_tabs": GAUNTLET_ROUTE_TABS,
        "table_rows": GAUNTLET_TABLE_ROWS,
    }


def create_app() -> App:
    """Create the test Chirp app with chirp-ui integration."""
    template_dir = os.path.join(os.path.dirname(__file__), "templates")

    app = App(
        AppConfig(
            template_dir=template_dir,
            debug=True,
            alpine=True,
            view_transitions=True,
            skip_contract_checks=True,
        )
    )
    use_chirp_ui(app)

    # ── Navigation: boosted links between pages ──────────────────────

    @app.route("/")
    async def home(request: Request):
        return Template("home.html", page_title="Home")

    @app.route("/gauntlet")
    async def gauntlet_page(request: Request):
        return Template("gauntlet_page.html", **_gauntlet_context())

    @app.route("/gauntlet/fragments/actions/{state}")
    async def gauntlet_actions_fragment(request: Request, state: str):
        return Template(
            "gauntlet_swap_fragment.html",
            swap_state=state if state in {"stable", "urgent"} else "stable",
        )

    @app.route("/gauntlet/fragments/action-result/{label}")
    async def gauntlet_action_result(request: Request, label: str):
        safe_label = label if label in {"pinned", "configured", "refreshed"} else "updated"
        return Response(f'<span class="chirpui-text-muted">Action: {safe_label}</span>')

    @app.route("/gauntlet/{room}")
    async def gauntlet_room(request: Request, room: str):
        return Template("gauntlet_page.html", **_gauntlet_context(room))

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

    # ── Command palette ──────────────────────────────────────────────

    @app.route("/command-palette")
    async def command_palette_page(request: Request):
        return Template("command_palette_page.html", page_title="Command Palette")

    @app.route("/search")
    async def search(request: Request):
        q = request.query.get("q", "")
        items = [f"Result for '{q}' #{i}" for i in range(1, 4)] if q else []
        html = "".join(f'<div class="chirpui-command-palette__item">{item}</div>' for item in items)
        return Response(html or '<div class="chirpui-command-palette__empty">No results</div>')

    # ── Drawer ────────────────────────────────────────────────────────

    @app.route("/drawer")
    async def drawer_page(request: Request):
        return Template("drawer_page.html", page_title="Drawer")

    # ── Tray ──────────────────────────────────────────────────────────

    @app.route("/tray")
    async def tray_page(request: Request):
        return Template("tray_page.html", page_title="Tray")

    # ── Toast ─────────────────────────────────────────────────────────

    @app.route("/toast")
    async def toast_page(request: Request):
        return Template("toast_page.html", page_title="Toast")

    @app.route("/toast/send")
    async def toast_send(request: Request):
        return Response(
            '<div class="chirpui-toast chirpui-toast--success" role="alert"'
            ' data-testid="toast-item">'
            '<span class="chirpui-toast__message">Operation successful</span>'
            '<button class="chirpui-toast__close" x-data'
            ' @click="$el.parentElement.remove()" aria-label="Dismiss">&times;</button>'
            "</div>"
        )

    # ── Copy button ───────────────────────────────────────────────────

    @app.route("/copy-button")
    async def copy_button_page(request: Request):
        return Template("copy_button_page.html", page_title="Copy Button")

    # ── Theme toggle ──────────────────────────────────────────────────

    @app.route("/theme-toggle")
    async def theme_toggle_page(request: Request):
        return Template("theme_toggle_page.html", page_title="Theme Toggle")

    # ── Split panel ───────────────────────────────────────────────────

    @app.route("/split-panel")
    async def split_panel_page(request: Request):
        return Template("split_panel_page.html", page_title="Split Panel")

    # ── Streaming bubble ──────────────────────────────────────────────

    @app.route("/streaming")
    async def streaming_page(request: Request):
        return Template("streaming_page.html", page_title="Streaming")

    # ── Card variants (Sprint 5 @scope pilot) ─────────────────────────

    @app.route("/card-variants")
    async def card_variants_page(request: Request):
        return Template("card_variants_page.html", page_title="Card Variants")

    # ── Surface variants (envelope hardening batch 1, S4) ─────────────

    @app.route("/surface-variants")
    async def surface_variants_page(request: Request):
        return Template("surface_variants_page.html", page_title="Surface Variants")

    # ── Callout variants (envelope hardening batch 1, S5) ─────────────

    @app.route("/callout-variants")
    async def callout_variants_page(request: Request):
        return Template("callout_variants_page.html", page_title="Callout Variants")

    # ── Video / Channel cards (envelope hardening batch 1, S6) ────────

    @app.route("/video-channel-cards")
    async def video_channel_cards_page(request: Request):
        return Template("video_channel_cards_page.html", page_title="Video / Channel Cards")

    # ── Product page patterns (LangChain design review, Phase 2) ─────

    @app.route("/product-page-patterns")
    async def product_page_patterns(request: Request):
        return Template(
            "product_page_patterns.html",
            page_title="Product Page Patterns",
            current_path="/product-page-patterns",
            customer_names=PRODUCT_PATTERN_CUSTOMERS,
            customer_logos=PRODUCT_PATTERN_LOGOS,
            products=PRODUCT_PATTERN_PRODUCTS,
            stories=PRODUCT_PATTERN_STORIES,
        )

    return app
