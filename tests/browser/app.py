"""Minimal Chirp test app for browser integration tests.

This app mounts real chirp-ui components inside a real Chirp app shell with
hx-boost, Alpine.js, and all the runtime machinery that production apps use.
Each route exercises a specific nesting/interaction pattern.
"""

import asyncio
import os

from chirp import App, AppConfig, ShellAction, ShellActions, ShellActionZone
from chirp.ext.chirp_ui import use_chirp_ui
from chirp.http.request import Request
from chirp.http.response import Response
from chirp.pages.shell_actions import ShellMenuItem
from chirp.templating.returns import Template

from chirp_ui import Column, parse_sort, selection_state, sort_columns
from chirp_ui.theme_packs import get_theme_pack

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

# Data grid gauntlet (#200) — sortable + selectable + sticky + load-more.
DATA_GRID_COLUMNS = [
    Column("name", "Name", sortable=True),
    Column("status", "Status", sortable=True, align="center"),
    Column("seats", "Seats", sortable=True, align="right"),
    Column("notes", "Notes", sortable=False),
]

# (id, name, status, seats, notes) — id is the stable selection value.
DATA_GRID_RECORDS = [
    ("u-1", "Alpha Corridor", "Active", 42, "Stable short cell"),
    ("u-2", "Beta Intake", "Paused", 7, "Some wrapped metadata"),
    ("u-3", "Gamma Archive", "Needs review", 128, "Longer note here"),
    ("u-4", "Delta Relay", "Active", 19, "Relay note"),
    ("u-5", "Epsilon Vault", "Paused", 64, "Vault note"),
    ("u-6", "Zeta Mesh", "Active", 3, "Mesh note"),
]

_DATA_GRID_PAGE_SIZE = 3
_DATA_GRID_ALLOWED = tuple(c.key for c in DATA_GRID_COLUMNS if c.sortable)


def _data_grid_sorted_records(sort) -> list[tuple]:
    if not sort.key:
        return list(DATA_GRID_RECORDS)
    key_index = {"name": 1, "status": 2, "seats": 3}.get(sort.key)
    if key_index is None:
        return list(DATA_GRID_RECORDS)
    return sorted(
        DATA_GRID_RECORDS,
        key=lambda rec: rec[key_index],
        reverse=(sort.direction == "desc"),
    )


def _data_grid_context(request: Request, *, offset: int = 0) -> dict[str, object]:
    sort = parse_sort(
        _hx_header(request, "HX-Sort") or request.query.get("sort"),
        default_key="name",
        allowed=_DATA_GRID_ALLOWED,
    )
    ordered = _data_grid_sorted_records(sort)
    page = ordered[offset : offset + _DATA_GRID_PAGE_SIZE]
    has_more = (offset + _DATA_GRID_PAGE_SIZE) < len(ordered)
    next_offset = offset + _DATA_GRID_PAGE_SIZE
    columns = sort_columns(DATA_GRID_COLUMNS, sort, base_url="/data-grid")
    selected = request.query.getlist("ids") if hasattr(request.query, "getlist") else []
    selection = selection_state(
        selected,
        page_ids=[rec[0] for rec in page],
        total=len(DATA_GRID_RECORDS),
    )
    return {
        "page_title": "Data Grid",
        "columns": columns,
        "rows": [[rec[1], rec[2], str(rec[3]), rec[4]] for rec in page],
        "row_ids": [rec[0] for rec in page],
        "row_labels": [rec[1] for rec in page],
        "selection": selection,
        "has_more": has_more,
        "load_more_url": f"/data-grid/rows?offset={next_offset}&sort={sort.key if sort.direction == 'asc' else '-' + sort.key}",
    }


CONSUMER_WORKSPACE_TABS = [
    {"label": "Overview", "href": "/consumer-workspace", "match": "exact", "badge": 4},
    {
        "label": "Runs",
        "href": "/consumer-workspace/runs",
        "match": "exact",
        "badge_loading": True,
    },
    {
        "label": "Settings",
        "href": "/consumer-workspace/settings",
        "match": "exact",
        "badge_expected": True,
    },
]

CONSUMER_WORKSPACE_VIEWS = {
    "/consumer-workspace": (
        "Workspace overview",
        "Overview content proves persistent shell, route tabs, command launch, and page tools.",
    ),
    "/consumer-workspace/runs": (
        "Workspace runs",
        "Runs content arrived through the page-root route-tab boundary.",
    ),
    "/consumer-workspace/settings": (
        "Workspace settings",
        "Settings content keeps the same app shell and page chrome.",
    ),
}

CONSUMER_ADMIN_TABS = [
    {"label": "Access", "href": "/consumer-admin", "match": "exact", "badge": 2},
    {"label": "Jobs", "href": "/consumer-admin/jobs", "match": "exact", "badge": 12},
    {"label": "Audit", "href": "/consumer-admin/audit", "match": "exact"},
]

CONSUMER_ADMIN_VIEWS = {
    "/consumer-admin": (
        "Access controls",
        "Access content proves a second app chrome consumer can own a distinct route family.",
    ),
    "/consumer-admin/jobs": (
        "Background jobs",
        "Jobs content arrived through the admin page-root boundary.",
    ),
    "/consumer-admin/audit": (
        "Audit trail",
        "Audit content keeps the admin shell, route tabs, and page tools stable.",
    ),
}

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

FORUM_PATTERN_TABS = [
    {"label": "Home", "href": "/forum-site-patterns", "match": "exact", "icon": "home"},
    {
        "label": "Threads",
        "href": "/forum-site-patterns/threads",
        "match": "prefix",
        "badge": 12,
        "icon": "sources",
    },
    {"label": "Q&A", "href": "/forum-site-patterns/questions", "match": "prefix", "icon": "status"},
    {
        "label": "Moderation",
        "href": "/forum-site-patterns/moderation",
        "match": "prefix",
        "badge": 3,
        "icon": "alert",
    },
]

FORUM_PATTERN_CAST = [
    {"label": "Rogue", "initials": "R", "href": "/forum-site-patterns/characters/rogue"},
    {"label": "Gambit", "initials": "G", "href": "/forum-site-patterns/characters/gambit"},
    {"label": "Storm", "initials": "S", "href": "/forum-site-patterns/characters/storm"},
    {"label": "Forge", "initials": "F", "href": "/forum-site-patterns/characters/forge"},
    {"label": "Jubilee", "initials": "J", "href": "/forum-site-patterns/characters/jubilee"},
]

FORUM_PATTERN_TOPICS = [
    {
        "href": "/forum-site-patterns/threads/med-bay-after-the-blackout",
        "title": "Med Bay after the blackout: who saw the east generator fail?",
        "description": "Open investigation scene with a rotating cast, two unread replies, and one director note.",
        "category": "Scene",
        "state": "needs reply",
        "state_variant": "warning",
        "top_meta": "Xavier Institute / Med Bay",
        "replies": 18,
        "views": 142,
        "latest_href": "/forum-site-patterns/threads/med-bay-after-the-blackout#post-18",
        "latest_title": "New generator clue",
        "actor": "Rogue",
        "meta": "12 min ago",
    },
    {
        "href": "/forum-site-patterns/threads/quiet-hours-in-the-boathouse-with-a-long-scene-title",
        "title": "Quiet hours in the boathouse with a long scene title that should wrap without pushing controls sideways",
        "description": "Low-pressure character scene; watch state and cast do the work instead of repeated labels.",
        "category": "Slice of life",
        "state": "watched",
        "state_variant": "info",
        "top_meta": "Lake / Boathouse",
        "replies": 7,
        "views": 64,
        "latest_href": "/forum-site-patterns/threads/quiet-hours#post-7",
        "latest_title": "Tea on the dock",
        "actor": "Gambit",
        "meta": "Yesterday",
    },
    {
        "href": "/forum-site-patterns/threads/founders-office-closed-canon-review",
        "title": "Founder office canon review",
        "description": "Locked staff thread that still exposes state, latest activity, and a clear route to context.",
        "category": "Canon",
        "state": "locked",
        "state_variant": "muted",
        "top_meta": "Guidebook / Director notes",
        "replies": 4,
        "views": 35,
        "latest_href": "/forum-site-patterns/threads/founders-office#post-4",
        "latest_title": "Revision summary",
        "actor": "Director",
        "meta": "2 days ago",
    },
]

FORUM_PATTERN_MODERATION = [
    {
        "href": "/forum-site-patterns/moderation/reports/42",
        "title": "Report on Med Bay after the blackout",
        "description": "Potential continuity conflict with current event timing.",
        "state": "needs review",
        "variant": "warning",
        "meta": "Rule: continuity / Scene",
    },
    {
        "href": "/forum-site-patterns/moderation/reports/43",
        "title": "Application needs director response",
        "description": "Prospective writer answered the requested revision.",
        "state": "waiting",
        "variant": "info",
        "meta": "Applications / 1 hour ago",
    },
]

MEDIA_PATTERN_THUMB = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
    "viewBox='0 0 640 360'%3E%3Crect width='640' height='360' fill='%23242b3d'/%3E"
    "%3Crect x='42' y='42' width='556' height='276' rx='24' fill='%2337475f'/%3E"
    "%3Ccircle cx='320' cy='180' r='52' fill='%23ffffff' fill-opacity='.82'/%3E"
    "%3Cpath d='M304 146l56 34-56 34z' fill='%23242b3d'/%3E%3C/svg%3E"
)

MEDIA_PATTERN_DEVICES = [
    {"name": "Smart TVs"},
    {"name": "Mobile"},
    {"name": "Game consoles"},
    {"name": "Web"},
    {"name": "Tablets"},
]

MEDIA_PATTERN_FEATURED = [
    {
        "name": "The Long Night Relay",
        "summary": "A live citywide race with alternate camera feeds and replay markers.",
        "state": "Live",
        "state_variant": "error",
        "meta": "Sports / 8 feeds / Included",
        "href": "/media-site-patterns/watch/relay",
    },
    {
        "name": "North Pier",
        "summary": "A premium mystery series with weekly episodes and downloadable extras.",
        "state": "New episodes",
        "state_variant": "info",
        "meta": "Series / 4K / Downloadable",
        "href": "/media-site-patterns/watch/north-pier",
    },
]

MEDIA_PATTERN_TITLES = [
    {
        "href": "/media-site-patterns/watch/relay-final",
        "title": "Relay Final: Market Street Sprint",
        "duration": "1:42:00",
        "channel": "Acme Sports",
        "views": "Live",
        "date": "Starts 8:00 PM",
    },
    {
        "href": "/media-site-patterns/watch/tide-archive",
        "title": "Tide Archive: Director Commentary",
        "duration": "42:18",
        "channel": "Acme Originals",
        "views": "24K",
        "date": "Yesterday",
    },
    {
        "href": "/media-site-patterns/watch/field-notes",
        "title": "Field Notes: How the city rail scene was built",
        "duration": "13:05",
        "channel": "Behind the Frame",
        "views": "8.4K",
        "date": "2 days ago",
    },
]

MEDIA_PATTERN_LIVE_EVENTS = [
    {
        "name": "Bay City vs. Harbor United",
        "state": "Live",
        "variant": "error",
        "time": "Q3 / 08:12 remaining",
        "restriction": "Available in home market and replay after midnight.",
    },
    {
        "name": "Creator Premiere: Studio Walkthrough",
        "state": "Upcoming",
        "variant": "info",
        "time": "Tomorrow, 7:30 PM",
        "restriction": "Reminder and trailer available now.",
    },
]

MEDIA_PATTERN_PLANS = [
    {
        "name": "Starter",
        "price": "$8/mo",
        "fit": "Mobile and web",
        "badge": "Core",
        "summary": "HD streaming, one profile, and offline downloads on one device.",
    },
    {
        "name": "Household",
        "price": "$15/mo",
        "fit": "Families",
        "badge": "Popular",
        "summary": "4K catalog, four profiles, kids mode, and two simultaneous streams.",
    },
    {
        "name": "Live Plus",
        "price": "$24/mo",
        "fit": "Sports and live events",
        "badge": "Live",
        "summary": "Live channels, DVR, regional sports, and event replay windows.",
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


def _consumer_shell_actions(label: str = "New run") -> ShellActions:
    return ShellActions(
        primary=ShellActionZone(
            items=(
                ShellAction(
                    id="consumer-primary",
                    label=label,
                    href="/consumer-workspace/new",
                    variant="primary",
                ),
            )
        ),
        controls=ShellActionZone(
            items=(
                ShellAction(
                    id="consumer-refresh",
                    label="Refresh",
                    action="refresh-consumer",
                    variant="secondary",
                ),
            )
        ),
    )


def _hx_header(request: Request, name: str) -> str:
    headers = getattr(request, "headers", {})
    get = getattr(headers, "get", None)
    if not get:
        return ""
    return get(name) or ""


def _is_hx_target(request: Request, target: str) -> bool:
    return bool(_hx_header(request, "HX-Request")) and _hx_header(request, "HX-Target") == target


def _include_shell_actions_oob(request: Request) -> bool:
    return _is_hx_target(request, "main")


def _ctx_rail_context(
    request: Request, path: str, main_label: str, rail_html: str
) -> dict[str, object]:
    """Context for the route-context rail gauntlet fixture (#195).

    On a boosted #main request the fixture emits a context_rail_oob() fragment
    (when rail_html is non-empty); on initial load the same content renders via
    the context_rail block.
    """
    return {
        "page_title": "Context Rail",
        "context_rail": True,
        "current_path": path,
        "main_label": main_label,
        "rail_html": rail_html,
        "boosted": _is_hx_target(request, "main"),
    }


def _workspace_context(path: str, *, include_shell_actions_oob: bool = False) -> dict[str, object]:
    title, copy = CONSUMER_WORKSPACE_VIEWS.get(
        path, CONSUMER_WORKSPACE_VIEWS["/consumer-workspace"]
    )
    return {
        "page_title": title,
        "current_path": path,
        "tab_items": CONSUMER_WORKSPACE_TABS,
        "view_title": title,
        "view_copy": copy,
        "shell_actions": _consumer_shell_actions(),
        "include_shell_actions_oob": include_shell_actions_oob,
    }


def _workspace_page_root_fragment(path: str) -> str:
    title, copy = CONSUMER_WORKSPACE_VIEWS.get(
        path, CONSUMER_WORKSPACE_VIEWS["/consumer-workspace"]
    )
    active = {
        tab["href"]: " chirpui-route-tab--active" if tab["href"] == path else ""
        for tab in CONSUMER_WORKSPACE_TABS
    }
    current = {
        tab["href"]: ' aria-current="page"' if tab["href"] == path else ""
        for tab in CONSUMER_WORKSPACE_TABS
    }
    return f"""
<div id="route-tabs">
  <nav role="navigation" aria-label="Subsection navigation" class="chirpui-route-tabs">
    <a href="/consumer-workspace" class="chirpui-route-tab{active["/consumer-workspace"]}"{current["/consumer-workspace"]} hx-boost="false" hx-select="unset" hx-get="/consumer-workspace" hx-target="#page-root" hx-push-url="true" hx-swap="innerHTML"><span class="chirpui-route-tab__label">Overview</span><span class="chirpui-route-tab__badge">4</span></a>
    <a href="/consumer-workspace/runs" class="chirpui-route-tab{active["/consumer-workspace/runs"]}"{current["/consumer-workspace/runs"]} hx-boost="false" hx-select="unset" hx-get="/consumer-workspace/runs" hx-target="#page-root" hx-push-url="true" hx-swap="innerHTML"><span class="chirpui-route-tab__label">Runs</span><span class="chirpui-route-tab__badge chirpui-route-tab__badge--reserved chirpui-route-tab__badge--loading" aria-hidden="true"></span></a>
    <a href="/consumer-workspace/settings" class="chirpui-route-tab{active["/consumer-workspace/settings"]}"{current["/consumer-workspace/settings"]} hx-boost="false" hx-select="unset" hx-get="/consumer-workspace/settings" hx-target="#page-root" hx-push-url="true" hx-swap="innerHTML"><span class="chirpui-route-tab__label">Settings</span><span class="chirpui-route-tab__badge chirpui-route-tab__badge--reserved" aria-hidden="true"></span></a>
  </nav>
</div>
<div class="chirpui-stack chirpui-stack--sm">
  <nav class="chirpui-breadcrumbs" aria-label="Breadcrumb">
    <ol class="chirpui-breadcrumbs__list">
      <li class="chirpui-breadcrumbs__item"><a href="/consumer-workspace" class="chirpui-breadcrumbs__link">Consumers</a></li>
      <li class="chirpui-breadcrumbs__item"><span class="chirpui-breadcrumbs__current" aria-current="page">Workspace</span></li>
    </ol>
  </nav>
  <div class="chirpui-cluster chirpui-cluster--sm">
    <h1 data-testid="consumer-heading">Workspace consumer</h1>
    <button type="button" class="chirpui-command-palette__trigger chirpui-command-palette-trigger chirpui-command-palette-trigger--sm" aria-label="Search workspace" x-data="chirpuiDialogTarget()" data-dialog-target="workspace-consumer-palette" @click="open()">
      <span class="chirpui-command-palette__trigger-label">Search or jump</span>
      <kbd class="chirpui-command-palette__kbd">/</kbd>
    </button>
  </div>
</div>
<div class="chirpui-action-strip chirpui-action-strip--muted chirpui-action-strip--sm chirpui-action-strip--scroll" role="toolbar" aria-label="Workspace page tools">
  <div class="chirpui-action-strip__inner">
    <button class="chirpui-btn chirpui-btn--ghost chirpui-btn--sm" hx-get="/consumer-workspace/filter-fragment" hx-target="#page-content-inner" hx-swap="innerHTML" hx-select="unset" hx-disinherit="hx-select">Filter</button>
    <button class="chirpui-btn chirpui-btn--ghost chirpui-btn--sm">Refresh</button>
    <button class="chirpui-btn chirpui-btn--ghost chirpui-btn--sm">Export</button>
  </div>
</div>
<div id="page-content-inner">
  <section class="chirpui-block">
    <h2 data-testid="consumer-view-title">{title}</h2>
    <p data-testid="consumer-view-copy">{copy}</p>
  </section>
</div>
"""


def _consumer_admin_shell_actions(label: str = "Invite member") -> ShellActions:
    return ShellActions(
        primary=ShellActionZone(
            items=(
                ShellAction(
                    id="consumer-admin-primary",
                    label=label,
                    href="/consumer-admin/invite",
                    variant="primary",
                ),
            )
        ),
        controls=ShellActionZone(
            items=(
                ShellAction(
                    id="consumer-admin-audit",
                    label="Audit",
                    href="/consumer-admin/audit",
                    variant="secondary",
                ),
            )
        ),
    )


def _admin_context(path: str, *, include_shell_actions_oob: bool = False) -> dict[str, object]:
    title, copy = CONSUMER_ADMIN_VIEWS.get(path, CONSUMER_ADMIN_VIEWS["/consumer-admin"])
    return {
        "page_title": title,
        "current_path": path,
        "tab_items": CONSUMER_ADMIN_TABS,
        "view_title": title,
        "view_copy": copy,
        "shell_actions": _consumer_admin_shell_actions(),
        "include_shell_actions_oob": include_shell_actions_oob,
    }


def _admin_page_root_fragment(path: str) -> str:
    title, copy = CONSUMER_ADMIN_VIEWS.get(path, CONSUMER_ADMIN_VIEWS["/consumer-admin"])
    active = {
        tab["href"]: " chirpui-route-tab--active" if tab["href"] == path else ""
        for tab in CONSUMER_ADMIN_TABS
    }
    current = {
        tab["href"]: ' aria-current="page"' if tab["href"] == path else ""
        for tab in CONSUMER_ADMIN_TABS
    }
    return f"""
<div id="route-tabs">
  <nav role="navigation" aria-label="Subsection navigation" class="chirpui-route-tabs">
    <a href="/consumer-admin" class="chirpui-route-tab{active["/consumer-admin"]}"{current["/consumer-admin"]} hx-boost="false" hx-select="unset" hx-get="/consumer-admin" hx-target="#page-root" hx-push-url="true" hx-swap="innerHTML"><span class="chirpui-route-tab__label">Access</span><span class="chirpui-route-tab__badge">2</span></a>
    <a href="/consumer-admin/jobs" class="chirpui-route-tab{active["/consumer-admin/jobs"]}"{current["/consumer-admin/jobs"]} hx-boost="false" hx-select="unset" hx-get="/consumer-admin/jobs" hx-target="#page-root" hx-push-url="true" hx-swap="innerHTML"><span class="chirpui-route-tab__label">Jobs</span><span class="chirpui-route-tab__badge">12</span></a>
    <a href="/consumer-admin/audit" class="chirpui-route-tab{active["/consumer-admin/audit"]}"{current["/consumer-admin/audit"]} hx-boost="false" hx-select="unset" hx-get="/consumer-admin/audit" hx-target="#page-root" hx-push-url="true" hx-swap="innerHTML"><span class="chirpui-route-tab__label">Audit</span></a>
  </nav>
</div>
<div class="chirpui-stack chirpui-stack--sm">
  <nav class="chirpui-breadcrumbs" aria-label="Breadcrumb">
    <ol class="chirpui-breadcrumbs__list">
      <li class="chirpui-breadcrumbs__item"><a href="/consumer-workspace" class="chirpui-breadcrumbs__link">Consumers</a></li>
      <li class="chirpui-breadcrumbs__item"><span class="chirpui-breadcrumbs__current" aria-current="page">Admin console</span></li>
    </ol>
  </nav>
  <div class="chirpui-cluster chirpui-cluster--sm">
    <h1 data-testid="consumer-admin-heading">Admin console</h1>
    <button type="button" class="chirpui-command-palette__trigger chirpui-command-palette-trigger chirpui-command-palette-trigger--sm" aria-label="Search admin" x-data="chirpuiDialogTarget()" data-dialog-target="admin-consumer-palette" @click="open()">
      <span class="chirpui-command-palette__trigger-label">Search admin</span>
      <kbd class="chirpui-command-palette__kbd">/</kbd>
    </button>
  </div>
</div>
<div class="chirpui-action-strip chirpui-action-strip--muted chirpui-action-strip--sm chirpui-action-strip--scroll" role="toolbar" aria-label="Admin console tools">
  <div class="chirpui-action-strip__inner">
    <button class="chirpui-btn chirpui-btn--ghost chirpui-btn--sm">Review</button>
    <button class="chirpui-btn chirpui-btn--ghost chirpui-btn--sm">Suspend</button>
    <button class="chirpui-btn chirpui-btn--ghost chirpui-btn--sm">Export</button>
  </div>
</div>
<div id="page-content-inner">
  <section class="chirpui-block">
    <h2 data-testid="consumer-admin-view-title">{title}</h2>
    <p data-testid="consumer-admin-view-copy">{copy}</p>
  </section>
</div>
"""


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

    @app.route("/dense-object-chrome")
    async def dense_object_chrome_page(request: Request):
        return Template("dense_object_chrome_page.html", page_title="Dense Object Chrome")

    @app.route("/rail-to-tray")
    async def rail_to_tray_page(request: Request):
        return Template("rail_to_tray_page.html", page_title="Rail To Drawer Chrome")

    # Mobile shell nav drawer gauntlet (#196): the built-in app_shell affordance
    # (nav_drawer=True + context_rail=True) through the layout entry point. Two
    # routes so the drawer-link-close path also exercises a real boosted nav.
    def _shell_drawer_ctx(path: str, label: str) -> dict[str, object]:
        return {
            "page_title": "Shell Nav Drawer",
            "nav_drawer": True,
            "context_rail": True,
            "current_path": path,
            "main_label": label,
        }

    @app.route("/shell-drawer")
    async def shell_drawer_page(request: Request):
        return Template(
            "shell_drawer_page.html", **_shell_drawer_ctx("/shell-drawer", "Drawer shell")
        )

    # Shell-actions duplicate-id gauntlet (#224): a consumer renders the bar in
    # two regions (canonical topbar + a drawer copy with id_suffix="-drawer"). The
    # stub carries an overflow zone AND a kind="menu" action so BOTH fixed ids
    # appear in both instances — the duplicate-id condition the suffix fixes.
    def _dup_id_shell_actions() -> ShellActions:
        return ShellActions(
            primary=ShellActionZone(
                items=(
                    ShellAction(
                        id="bulk",
                        label="Bulk",
                        kind="menu",
                        menu_items=(
                            ShellMenuItem(label="Delete", action="delete"),
                            ShellMenuItem(label="Move", action="move"),
                        ),
                    ),
                )
            ),
            overflow=ShellActionZone(
                items=(ShellAction(id="archive", label="Archive", action="archive"),)
            ),
            target="chirp-shell-actions",
        )

    @app.route("/shell-actions-dup")
    async def shell_actions_dup_page(request: Request):
        return Template(
            "shell_actions_dup_id_page.html",
            page_title="Shell Actions Dup Id",
            current_path="/shell-actions-dup",
            shell_actions=_dup_id_shell_actions(),
        )

    @app.route("/shell-drawer/deploys")
    async def shell_drawer_deploys_page(request: Request):
        return Template(
            "shell_drawer_page.html", **_shell_drawer_ctx("/shell-drawer/deploys", "Deployments")
        )

    # Route-context rail gauntlet (#195): /ctx and /ctx/b carry rail content,
    # /ctx/none ships none so the shell-runtime stale-clear must empty the rail.
    @app.route("/ctx")
    async def ctx_a(request: Request):
        return Template(
            "context_rail_page.html",
            **_ctx_rail_context(
                request, "/ctx", "Context A", '<h2 data-testid="rail-content">Context A</h2>'
            ),
        )

    @app.route("/ctx/b")
    async def ctx_b(request: Request):
        return Template(
            "context_rail_page.html",
            **_ctx_rail_context(
                request, "/ctx/b", "Context B", '<h2 data-testid="rail-content">Context B</h2>'
            ),
        )

    @app.route("/ctx/none")
    async def ctx_none(request: Request):
        return Template(
            "context_rail_page.html",
            **_ctx_rail_context(request, "/ctx/none", "No context", ""),
        )

    @app.route("/consumer-workspace")
    async def consumer_workspace_page(request: Request):
        if _is_hx_target(request, "page-root"):
            return Response(_workspace_page_root_fragment("/consumer-workspace"))
        return Template(
            "consumer_workspace_page.html",
            **_workspace_context(
                "/consumer-workspace",
                include_shell_actions_oob=_include_shell_actions_oob(request),
            ),
        )

    @app.route("/consumer-workspace/runs")
    async def consumer_workspace_runs_page(request: Request):
        if _is_hx_target(request, "page-root"):
            return Response(_workspace_page_root_fragment("/consumer-workspace/runs"))
        return Template(
            "consumer_workspace_page.html",
            **_workspace_context(
                "/consumer-workspace/runs",
                include_shell_actions_oob=_include_shell_actions_oob(request),
            ),
        )

    @app.route("/consumer-workspace/settings")
    async def consumer_workspace_settings_page(request: Request):
        if _is_hx_target(request, "page-root"):
            return Response(_workspace_page_root_fragment("/consumer-workspace/settings"))
        return Template(
            "consumer_workspace_page.html",
            **_workspace_context(
                "/consumer-workspace/settings",
                include_shell_actions_oob=_include_shell_actions_oob(request),
            ),
        )

    @app.route("/consumer-workspace/filter-fragment")
    async def consumer_workspace_filter_fragment(request: Request):
        return Response(
            '<section class="chirpui-block" data-testid="consumer-filter-result">'
            "<h2>Filtered workspace</h2>"
            "<p>Filter content arrived through the page-content-inner boundary.</p>"
            "</section>"
        )

    @app.route("/consumer-admin")
    async def consumer_admin_page(request: Request):
        if _is_hx_target(request, "page-root"):
            return Response(_admin_page_root_fragment("/consumer-admin"))
        return Template(
            "consumer_admin_page.html",
            **_admin_context(
                "/consumer-admin",
                include_shell_actions_oob=_include_shell_actions_oob(request),
            ),
        )

    @app.route("/consumer-admin/jobs")
    async def consumer_admin_jobs_page(request: Request):
        if _is_hx_target(request, "page-root"):
            return Response(_admin_page_root_fragment("/consumer-admin/jobs"))
        return Template(
            "consumer_admin_page.html",
            **_admin_context(
                "/consumer-admin/jobs",
                include_shell_actions_oob=_include_shell_actions_oob(request),
            ),
        )

    @app.route("/consumer-admin/audit")
    async def consumer_admin_audit_page(request: Request):
        if _is_hx_target(request, "page-root"):
            return Response(_admin_page_root_fragment("/consumer-admin/audit"))
        return Template(
            "consumer_admin_page.html",
            **_admin_context(
                "/consumer-admin/audit",
                include_shell_actions_oob=_include_shell_actions_oob(request),
            ),
        )

    # Data grid gauntlet (#200): full load renders data_grid; the load-more
    # hx-get returns the data_grid_rows fragment (sort + offset preserved in the
    # sentinel URL the macro emitted on the previous render).
    @app.route("/data-grid")
    async def data_grid_page(request: Request):
        return Template("data_grid_page.html", **_data_grid_context(request))

    @app.route("/data-grid/rows")
    async def data_grid_rows_route(request: Request):
        try:
            offset = int(request.query.get("offset", "0"))
        except TypeError, ValueError:
            offset = 0
        ctx = _data_grid_context(request, offset=offset)
        return Template(
            "data_grid_rows_fragment.html",
            columns=ctx["columns"],
            rows=ctx["rows"],
            row_ids=ctx["row_ids"],
            row_labels=ctx["row_labels"],
            selection=ctx["selection"],
            has_more=ctx["has_more"],
            load_more_url=ctx["load_more_url"],
        )

    @app.route("/application-chrome-gauntlet")
    async def application_chrome_gauntlet_page(request: Request):
        return Template(
            "application_chrome_gauntlet_page.html",
            page_title="Application Chrome Gauntlet",
        )

    @app.route("/page-b")
    async def page_b(request: Request):
        return Template("page_b.html", page_title="Page B")

    @app.route("/rapid-nav")
    async def rapid_nav(request: Request):
        return Template("rapid_page.html", page_title="Rapid Nav", rapid_label="Start")

    @app.route("/rapid-a")
    async def rapid_a(request: Request):
        await asyncio.sleep(0.3)
        return Template("rapid_page.html", page_title="Rapid A", rapid_label="Slow A")

    @app.route("/rapid-b")
    async def rapid_b(request: Request):
        await asyncio.sleep(0.05)
        return Template("rapid_page.html", page_title="Rapid B", rapid_label="Fast B")

    @app.route("/theme-pack-preview/{name}/{mode}")
    async def theme_pack_preview(request: Request, name: str, mode: str):
        if mode not in {"light", "dark", "system"}:
            return Response("Unknown theme mode", status=404)

        pack = get_theme_pack(name)
        if pack is None:
            return Response("Unknown theme pack", status=404)

        return Template(
            "theme_pack_preview_page.html",
            page_title=f"{pack.label} theme pack",
            mode=mode,
            pack=pack,
        )

    # ── Fragment form: form inside boosted layout ────────────────────

    @app.route("/form")
    async def form_page(request: Request):
        return Template("form_page.html", page_title="Form Test")

    @app.route("/form/submit", methods=["POST"])
    async def form_submit(request: Request):
        return Response('<div id="form-result">Saved successfully</div>')

    slow_form_submits = {"count": 0}

    @app.route("/form/slow")
    async def slow_form_page(request: Request):
        slow_form_submits["count"] = 0
        return Template("slow_form_page.html", page_title="Slow Form")

    @app.route("/form/slow-submit", methods=["POST"])
    async def slow_form_submit(request: Request):
        slow_form_submits["count"] += 1
        await asyncio.sleep(0.25)
        count = slow_form_submits["count"]
        return Response(f'<div id="slow-form-result" data-count="{count}">Saved {count}</div>')

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

    @app.route("/search-sync")
    async def search_sync_page(request: Request):
        return Template("search_sync_page.html", page_title="Search Sync")

    @app.route("/search/slow")
    async def slow_search(request: Request):
        q = request.query.get("q", "")
        if q == "a":
            await asyncio.sleep(0.3)
        elif q == "ab":
            await asyncio.sleep(0.05)
        return Response(f'<div data-testid="search-result">Result for {q}</div>')

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

    @app.route("/app-layout-theme")
    async def app_layout_theme_page(request: Request):
        return Template("app_layout_theme_page.html", page_title="App Layout Theme")

    @app.route("/ascii-controls")
    async def ascii_controls_page(request: Request):
        return Template("ascii_controls_page.html", page_title="ASCII Controls")

    @app.route("/ascii-composites")
    async def ascii_composites_page(request: Request):
        return Template("ascii_composites_page.html", page_title="ASCII Composites")

    @app.route("/ascii-displays")
    async def ascii_displays_page(request: Request):
        return Template("ascii_displays_page.html", page_title="ASCII Displays")

    # ── Split panel ───────────────────────────────────────────────────

    @app.route("/split-panel")
    async def split_panel_page(request: Request):
        return Template("split_panel_page.html", page_title="Split Panel")

    # ── Streaming bubble ──────────────────────────────────────────────

    @app.route("/streaming")
    async def streaming_page(request: Request):
        return Template("streaming_page.html", page_title="Streaming")

    @app.route("/page-actions-candidate")
    async def page_actions_candidate_page(request: Request):
        return Template(
            "page_actions_candidate_page.html",
            page_title="Page Actions Candidate",
            candidate_url="/page-actions-candidate",
            prompt_text="Summarize the streaming transcript and identify the model handoff.",
            page_tool_items=[
                {
                    "label": "Open current fixture",
                    "href": "/page-actions-candidate",
                    "icon": "link",
                },
                {"label": "Open prompt text", "href": "/page-actions-candidate/prompt.txt"},
                {"label": "Copy sample text", "action": "copy-sample-text"},
                {
                    "label": "Ask external assistant about this prompt",
                    "href": "https://chat.openai.com/",
                    "icon": "share",
                },
                {
                    "label": (
                        "Open prompt text with a deliberately long label that should stay "
                        "inside the existing dropdown menu"
                    ),
                    "href": "/page-actions-candidate/prompt.txt?variant=long-label",
                },
                {"divider": True},
                {
                    "label": "Review existing primitives",
                    "href": "/page-actions-candidate#primitive-review",
                },
            ],
        )

    @app.route("/page-actions-candidate/prompt.txt")
    async def page_actions_candidate_prompt(request: Request):
        return Response(
            "Summarize the streaming transcript and identify the model handoff.",
            content_type="text/plain; charset=utf-8",
        )

    @app.route("/linked-nav-candidate")
    async def linked_nav_candidate_page(request: Request):
        return Template(
            "linked_nav_candidate_page.html",
            page_title="Linked Nav Candidate",
            current_path="/linked-nav-candidate/guide/install",
            linked_nav_items=[
                {
                    "title": "Guide",
                    "href": "/linked-nav-candidate/guide",
                    "open": True,
                    "badge": 4,
                    "children": [
                        {
                            "title": "Install",
                            "href": "/linked-nav-candidate/guide/install",
                            "active": True,
                        },
                        {
                            "title": (
                                "Configuration with a deliberately long child label "
                                "that must wrap inside the sidebar"
                            ),
                            "href": "/linked-nav-candidate/guide/configuration",
                        },
                    ],
                },
                {
                    "title": "Reference",
                    "href": "/linked-nav-candidate/reference",
                    "children": [
                        {
                            "title": "Hidden child until server marks branch open",
                            "href": "/linked-nav-candidate/reference/hidden",
                        },
                    ],
                },
                {
                    "title": "No-href group",
                    "open": True,
                    "children": [
                        {
                            "title": "Grouped child",
                            "href": "/linked-nav-candidate/grouped-child",
                        },
                    ],
                },
            ],
        )

    @app.route("/compact-header-candidate")
    async def compact_header_candidate_page(request: Request):
        return Template(
            "compact_header_candidate_page.html",
            page_title="Compact Header Candidate",
            long_title=(
                "Compact header candidate with a deliberately long title that must wrap "
                "without pushing actions or page chrome outside the viewport"
            ),
        )

    @app.route("/dense-reference-data-reference")
    async def dense_reference_data_reference_page(request: Request):
        return Template(
            "dense_reference_data_reference_page.html",
            page_title="Dense Reference Data Reference",
            modules=[
                {
                    "href": "/dense-reference-data-reference/modules/chirp_ui.components",
                    "title": "chirp_ui.components",
                    "kind": "Registry",
                    "summary": "Component descriptors, emitted classes, slots, and maturity metadata.",
                    "status": "Stable",
                },
                {
                    "href": "/dense-reference-data-reference/modules/chirp_ui.templates.reference_browser_with_exceptionally_long_slug",
                    "title": "chirp_ui.templates.reference_browser_with_exceptionally_long_slug",
                    "kind": "Templates",
                    "summary": "Macro output contracts for dense docs and generated component pages.",
                    "status": "Candidate",
                },
                {
                    "href": "/dense-reference-data-reference/modules/chirp_ui.validation",
                    "title": "chirp_ui.validation",
                    "kind": "Runtime",
                    "summary": "Validation helpers that keep variants, sizes, and appearances registry-bound.",
                    "status": "Stable",
                },
            ],
            member_rows=[
                (
                    "resource_index",
                    "macro",
                    "stable",
                    "Search, filter, selection, empty state, and result layout wrapper.",
                ),
                (
                    "params_table_with_extremely_long_generated_member_name",
                    "macro",
                    "candidate",
                    "Reference table pressure case with a long generated identifier.",
                ),
                (
                    "validate_variant_block",
                    "filter",
                    "stable",
                    "Registry-aligned validation path for bounded option sets.",
                ),
            ],
            params=[
                {
                    "name": "filter_state_name",
                    "type": "str | None",
                    "default": "None",
                    "description": "Hidden field name that preserves server-owned filter context.",
                },
                {
                    "name": "module_reference_identifier_with_deliberately_long_unbroken_name",
                    "type": "Mapping[str, Sequence[ComponentDescriptor]]",
                    "default": "",
                    "description": "Pressure case for generated reference identifiers.",
                },
                {
                    "name": "results_layout",
                    "type": '"stack" | "grid"',
                    "default": '"stack"',
                    "description": "Existing bounded layout option, not a data-grid engine.",
                },
            ],
        )

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

    # ── Visual effect render contracts ──────────────────────────────

    @app.route("/effects-visual")
    async def effects_visual_page(request: Request):
        return Template("effects_visual_page.html", page_title="Effects Visual Contracts")

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

    # ── Forum site patterns (community/PBP design review, Phase 2) ───

    @app.route("/forum-site-patterns")
    async def forum_site_patterns(request: Request):
        return Template(
            "forum_site_patterns.html",
            page_title="Forum Site Patterns",
            current_path="/forum-site-patterns",
            forum_tabs=FORUM_PATTERN_TABS,
            cast=FORUM_PATTERN_CAST,
            topics=FORUM_PATTERN_TOPICS,
            moderation_items=FORUM_PATTERN_MODERATION,
        )

    # ── Media site patterns (streaming/media design review, Phase 2) ─

    @app.route("/media-site-patterns")
    async def media_site_patterns(request: Request):
        return Template(
            "media_site_patterns.html",
            page_title="Media Site Patterns",
            current_path="/media-site-patterns",
            devices=MEDIA_PATTERN_DEVICES,
            featured=MEDIA_PATTERN_FEATURED,
            titles=MEDIA_PATTERN_TITLES,
            live_events=MEDIA_PATTERN_LIVE_EVENTS,
            plans=MEDIA_PATTERN_PLANS,
            thumbnail=MEDIA_PATTERN_THUMB,
        )

    return app
