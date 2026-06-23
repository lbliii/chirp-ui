"""Declarative registry for component-showcase pages.

Each entry describes one navigable or routable showcase destination. The registry
is the single source of truth for sidebar navigation, the home index card grid, and
(later) command-palette search.

Fields
------
path
    Route path as declared on ``@app.route`` (including ``{param}`` segments).
title
    Human label for nav and search.
section
    Sidebar group: Core, Golden screens, Shell recipes, Components, Data,
    Effects, ASCII, or Rich.
description
    Short blurb for index cards and search snippets. May contain safe HTML.
tags
    Extra search keywords (component names, archetypes, etc.).
nav_order
    Sort key within a sidebar section (lower first).
icon
    Optional sidebar icon id (``sources``, ``run``, …).
match
    Sidebar active-state mode: ``exact`` or ``prefix``.
golden_screen
    Golden-screen archetype reference page.
shell_recipe
    Catalog / operations / support shell recipe page.
interactive_demo
    Page with live HTMX/SSE/island interactions.
hidden
    Non-nav endpoint (POST handler, fragment, SSE). Still listed so route ratchets
    stay in sync with ``app.py``.
show_in_sidebar
    When ``False``, the page is registered but omitted from the sidebar (golden
    screens, island subpages, theme-pack previews).
index_card
    Include on the home page component card grid.
index_order
    Sort key for index cards (lower first).

POST, fragment, and SSE routes use ``hidden=True`` and ``show_in_sidebar=False``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

MatchMode = Literal["exact", "prefix"]

SHOWCASE_LIVE_URL = "https://chirp-ui-showcase-production.up.railway.app"

SECTION_ORDER: tuple[str, ...] = (
    "Core",
    "Golden screens",
    "Shell recipes",
    "Components",
    "Data",
    "Effects",
    "ASCII",
    "Rich",
)


@dataclass(frozen=True, slots=True)
class ShowcasePage:
    path: str
    title: str
    section: str = ""
    description: str = ""
    tags: tuple[str, ...] = ()
    nav_order: int = 0
    icon: str = ""
    match: MatchMode = "prefix"
    golden_screen: bool = False
    shell_recipe: bool = False
    interactive_demo: bool = False
    hidden: bool = False
    show_in_sidebar: bool = True
    index_card: bool = False
    index_order: int = 0


PAGES: tuple[ShowcasePage, ...] = (
    # --- Core ---
    ShowcasePage(
        path="/",
        title="Home",
        section="Core",
        nav_order=10,
        icon="sources",
        match="exact",
    ),
    ShowcasePage(
        path="/demo",
        title="Quick Demo",
        section="Core",
        nav_order=20,
        icon="run",
        match="prefix",
        interactive_demo=True,
        tags=("streaming", "sse", "model_card"),
    ),
    ShowcasePage(
        path="/demo/submit",
        title="Demo submit fragment",
        hidden=True,
        show_in_sidebar=False,
    ),
    ShowcasePage(
        path="/demo/stream",
        title="Demo SSE stream",
        hidden=True,
        show_in_sidebar=False,
        interactive_demo=True,
    ),
    ShowcasePage(
        path="/toast",
        title="Toast fragment",
        hidden=True,
        show_in_sidebar=False,
    ),
    ShowcasePage(
        path="/favicon.ico",
        title="Favicon redirect",
        hidden=True,
        show_in_sidebar=False,
    ),
    ShowcasePage(
        path="/showcase/pages.json",
        title="Showcase page index JSON",
        hidden=True,
        show_in_sidebar=False,
        tags=("search", "json"),
    ),
    # --- Components ---
    ShowcasePage(
        path="/htmx",
        title="HTMX Patterns",
        section="Components",
        nav_order=10,
        tags=("htmx", "boost", "fragments"),
    ),
    ShowcasePage(
        path="/navigation",
        title="Navigation",
        section="Components",
        description=(
            "navbar, sidebar, stepper, route_tabs, nav_tree, pagination, command_palette."
        ),
        nav_order=20,
        index_card=True,
        index_order=10,
        tags=("navbar", "sidebar", "command_palette"),
    ),
    ShowcasePage(
        path="/layout",
        title="Layout",
        section="Components",
        description=(
            "Grid, stack, surface, hero, split_panel, entity_header, search_header, "
            "filter_bar, filter_chips, label_overline, segmented_control, action_bar, "
            "tray, media_object."
        ),
        nav_order=30,
        index_card=True,
        index_order=20,
        tags=("grid", "stack", "split_panel"),
    ),
    ShowcasePage(
        path="/chrome",
        title="App chrome & regions",
        section="Components",
        description=(
            "workspace_shell, split_layout, file_tree, shell_region, safe_region — "
            "plus how <code>app_shell_layout</code> maps to Chirp's shell."
        ),
        nav_order=40,
        index_card=True,
        index_order=30,
        tags=("app_shell", "shell_region", "workspace_shell"),
    ),
    ShowcasePage(
        path="/shell-actions",
        title="Shell Actions",
        section="Components",
        description="Route-scoped topbar actions, overflow menus, and persistent app shell updates.",
        nav_order=50,
        index_card=True,
        index_order=40,
        tags=("shell_actions", "topbar"),
    ),
    ShowcasePage(
        path="/sections",
        title="Sections",
        section="Components",
        description="section — Surface + header with icon, actions, and surface variants.",
        nav_order=60,
        index_card=True,
        index_order=50,
        tags=("section",),
    ),
    ShowcasePage(
        path="/layout/dir",
        title="Layout directory fragment",
        hidden=True,
        show_in_sidebar=False,
    ),
    ShowcasePage(
        path="/blocks",
        title="Blocks Gallery",
        section="Components",
        description=(
            "Registry-generated copy-paste blocks — live preview and Kida macro call "
            "for every public component."
        ),
        nav_order=65,
        index_card=True,
        index_order=55,
        tags=("blocks", "gallery", "registry", "copy-paste"),
    ),
    ShowcasePage(
        path="/carousel",
        title="Carousel",
        section="Components",
        description="Compact and page variants. CSS scroll-snap, native touch swipe, zero-JS.",
        nav_order=70,
        index_card=True,
        index_order=60,
        tags=("carousel", "scroll-snap"),
    ),
    ShowcasePage(
        path="/cards",
        title="Cards & Alerts",
        section="Components",
        description=(
            "card, alert — Content containers, <code>attrs_map</code> for HTMX widget roots, "
            "metric/config cards."
        ),
        nav_order=80,
        index_card=True,
        index_order=70,
        tags=("card", "alert"),
    ),
    ShowcasePage(
        path="/forms",
        title="Forms",
        section="Components",
        description=(
            "Fields, validation, wizard_form, inline_edit, drag-and-drop, sortable_list, "
            "signature, params_table."
        ),
        nav_order=90,
        index_card=True,
        index_order=80,
        tags=("form", "validation", "wizard_form"),
    ),
    ShowcasePage(
        path="/forms/demo",
        title="Forms demo fragment",
        hidden=True,
        show_in_sidebar=False,
    ),
    ShowcasePage(
        path="/appearance-tone",
        title="Appearance & Tone",
        section="Components",
        description=(
            "Descriptor-backed appearance and tone axes for buttons, badges, alerts, "
            "surfaces, and fields."
        ),
        nav_order=100,
        index_card=True,
        index_order=90,
        tags=("appearance", "tone"),
    ),
    ShowcasePage(
        path="/theme-packs",
        title="Theme Packs",
        section="Components",
        description="Token-only Atlas, Ember, and Sage packs shown across light, dark, and system modes.",
        nav_order=110,
        index_card=True,
        index_order=100,
        tags=("theme_pack", "atlas", "ember", "sage"),
    ),
    ShowcasePage(
        path="/theme-explorer",
        title="Theme Explorer",
        section="Components",
        description=(
            "Live token explorer with preset switching, computed values, and WCAG contrast preview."
        ),
        nav_order=105,
        index_card=True,
        index_order=95,
        interactive_demo=True,
        tags=("theme", "tokens", "contrast", "preset"),
    ),
    ShowcasePage(
        path="/theme-packs/preview/{name}/{mode}",
        title="Theme pack preview",
        hidden=True,
        show_in_sidebar=False,
        tags=("theme_pack",),
    ),
    ShowcasePage(
        path="/ui",
        title="UI Components",
        section="Components",
        description=(
            "modal, dropdown, tabs, accordion, tooltip, toast, row_actions, share_menu, "
            "status, empty_state, infinite_scroll."
        ),
        nav_order=120,
        index_card=True,
        index_order=110,
        tags=("modal", "dropdown", "tabs"),
    ),
    ShowcasePage(
        path="/ui/tab/{name}",
        title="UI tab fragment",
        hidden=True,
        show_in_sidebar=False,
    ),
    # --- Data ---
    ShowcasePage(
        path="/data-display",
        title="Data Display",
        section="Data",
        description=(
            "description_list, timeline, tag_input, tree_view, calendar — Key-value pairs, "
            "activity feeds, tags, trees."
        ),
        nav_order=10,
        index_card=True,
        index_order=140,
        tags=("description_list", "timeline", "tree_view"),
    ),
    ShowcasePage(
        path="/data",
        title="Team Roster",
        section="Data",
        description=(
            "Search, filter, sort, pagination, bulk select, export CSV — HTML over the wire."
        ),
        nav_order=20,
        match="exact",
        index_card=True,
        index_order=150,
        interactive_demo=True,
        tags=("table", "pagination", "bulk_select"),
    ),
    ShowcasePage(
        path="/data/table",
        title="Data table fragment",
        hidden=True,
        show_in_sidebar=False,
    ),
    ShowcasePage(
        path="/data/bulk-bar",
        title="Data bulk bar fragment",
        hidden=True,
        show_in_sidebar=False,
    ),
    ShowcasePage(
        path="/data/export",
        title="Data export",
        hidden=True,
        show_in_sidebar=False,
    ),
    # --- Shell recipes ---
    ShowcasePage(
        path="/catalog-shell",
        title="Catalog Shell",
        section="Shell recipes",
        description=("Atlas search catalog — filters, results rail, and selected-object detail."),
        nav_order=10,
        shell_recipe=True,
        tags=("catalog", "search", "atlas"),
    ),
    ShowcasePage(
        path="/operations-shell",
        title="Operations Shell",
        section="Shell recipes",
        description=("Ops command surface — metrics, queues, incidents, and activity rail."),
        nav_order=20,
        match="exact",
        shell_recipe=True,
        tags=("operations", "ops", "compute", "atlas"),
    ),
    ShowcasePage(
        path="/operations-shell-workspace",
        title="Operations Shell WS",
        section="Shell recipes",
        description="Workspace variant of the operations shell with split layout.",
        nav_order=30,
        shell_recipe=True,
        tags=("operations", "workspace", "atlas"),
    ),
    ShowcasePage(
        path="/support-shell",
        title="Support Shell",
        section="Shell recipes",
        description="Sage inbox triage — filter rail, result collection, and inspector.",
        nav_order=40,
        shell_recipe=True,
        tags=("support", "sage", "inbox"),
    ),
    ShowcasePage(
        path="/calendar",
        title="Calendar",
        section="Data",
        nav_order=70,
        tags=("calendar",),
    ),
    ShowcasePage(
        path="/calendar/{year}/{month}",
        title="Calendar month view",
        hidden=True,
        show_in_sidebar=False,
        tags=("calendar",),
    ),
    ShowcasePage(
        path="/dashboard",
        title="Dashboard",
        section="Data",
        description=(
            "animated_stat_card, config_row, settings_row, bar_chart, donut — "
            "Dashboard building blocks."
        ),
        nav_order=80,
        index_card=True,
        index_order=200,
        tags=("dashboard", "stat_card", "chart"),
    ),
    # --- Golden screens ---
    ShowcasePage(
        path="/screen-command-center",
        title="Command Center",
        section="Golden screens",
        description=(
            "Atlas profile — metrics, queues, incidents, activity, and selected-object inspection."
        ),
        nav_order=10,
        golden_screen=True,
        shell_recipe=True,
        tags=("command-center", "golden-screen", "operations", "atlas"),
    ),
    ShowcasePage(
        path="/screen-review-queue",
        title="Review Queue",
        section="Golden screens",
        description=(
            "Sage profile — filter rail, result collection, inspector, and state-rich review items."
        ),
        nav_order=20,
        golden_screen=True,
        shell_recipe=True,
        tags=("review-queue", "golden-screen", "support", "sage"),
    ),
    ShowcasePage(
        path="/screen-agent-run-monitor",
        title="Agent Run Monitor",
        section="Golden screens",
        description=("Signal profile — live run state, artifacts, logs, and retry context."),
        nav_order=30,
        golden_screen=True,
        tags=("agent-run-monitor", "golden-screen", "signal"),
    ),
    ShowcasePage(
        path="/screen-product-docs-home",
        title="Product Docs Home",
        section="Golden screens",
        description=("Ember profile — identity, proof band, lifecycle, entry points, and CTA."),
        nav_order=40,
        golden_screen=True,
        tags=("product-docs", "golden-screen", "ember"),
    ),
    ShowcasePage(
        path="/screen-lucky-cat-market",
        title="Lucky Cat Market",
        section="Golden screens",
        description=(
            "Atlas profile — ticker search, movers grid, market catalog, and live activity feed."
        ),
        nav_order=50,
        golden_screen=True,
        tags=("data-dense", "market", "lucky-cat", "golden-screen", "atlas"),
    ),
    # --- Effects ---
    ShowcasePage(
        path="/effects",
        title="Visual Effects",
        section="Effects",
        description=(
            "aurora, meteor, particles, symbol rain, constellation, sparkle, confetti, orbit — "
            "Background and decorative effects."
        ),
        nav_order=10,
        index_card=True,
        index_order=160,
        tags=("aurora", "particles", "effects"),
    ),
    ShowcasePage(
        path="/typography",
        title="Typography",
        section="Effects",
        description=(
            "neon_text, glitch_text, gradient_text, typewriter, text_reveal, marquee, "
            "number_ticker."
        ),
        nav_order=20,
        index_card=True,
        index_order=170,
        tags=("typography", "neon_text", "typewriter"),
    ),
    ShowcasePage(
        path="/animation",
        title="Animation",
        section="Effects",
        description=(
            "Motion tokens, micro-feedback, skeleton, View Transitions — Polished interactions."
        ),
        nav_order=30,
        index_card=True,
        index_order=210,
        tags=("animation", "view_transitions", "skeleton"),
    ),
    ShowcasePage(
        path="/animation/swap-demo",
        title="Animation swap demo fragment",
        hidden=True,
        show_in_sidebar=False,
    ),
    # --- ASCII ---
    ShowcasePage(
        path="/ascii",
        title="ASCII Icons",
        section="ASCII",
        description=(
            "Unicode symbols as primary icons — blink, pulse, shrink, rotate, spin, bounce, throb."
        ),
        nav_order=10,
        match="exact",
        index_card=True,
        index_order=220,
        tags=("ascii", "icons"),
    ),
    ShowcasePage(
        path="/ascii-primitives",
        title="ASCII Primitives",
        section="ASCII",
        description=(
            "Knobs, faders, VU meters, 7-segment displays, split-flap boards, breaker panels, "
            "toggles, tables — Full retro control suite."
        ),
        nav_order=20,
        index_card=True,
        index_order=180,
        tags=("ascii", "knobs", "vu_meter"),
    ),
    # --- Rich ---
    ShowcasePage(
        path="/buttons",
        title="Buttons & Cards",
        section="Rich",
        description=(
            "ripple, shimmer, pulsing buttons, glow_card, spotlight_card, bento_grid, dock, "
            "notification_dot."
        ),
        nav_order=10,
        index_card=True,
        index_order=190,
        tags=("button", "glow_card", "bento_grid"),
    ),
    ShowcasePage(
        path="/streaming",
        title="Streaming & AI",
        section="Rich",
        description="EventStream, model_card — live SSE demo, no LLM required.",
        nav_order=20,
        index_card=True,
        index_order=130,
        interactive_demo=True,
        tags=("streaming", "sse", "model_card"),
    ),
    ShowcasePage(
        path="/message-turn",
        title="Message turn surface",
        section="Rich",
        description=(
            "Assistant-turn chrome: actions, meta, reasoning, tool calls, citations, shortcuts."
        ),
        nav_order=25,
        index_card=True,
        index_order=125,
        tags=("message_bubble", "citations", "shortcuts"),
    ),
    ShowcasePage(
        path="/composer",
        title="Real composer",
        section="Rich",
        description="IME-safe send, send/stop abort, OOB attachments, suggestion chips.",
        nav_order=26,
        index_card=True,
        index_order=128,
        interactive_demo=True,
        tags=("composer", "chat_input", "attachments"),
    ),
    ShowcasePage(
        path="/composer/send",
        title="Composer send fragment",
        hidden=True,
        show_in_sidebar=False,
    ),
    ShowcasePage(
        path="/composer/abort",
        title="Composer abort endpoint",
        hidden=True,
        show_in_sidebar=False,
    ),
    ShowcasePage(
        path="/composer/dismiss/{file_id}",
        title="Composer dismiss attachment",
        hidden=True,
        show_in_sidebar=False,
    ),
    ShowcasePage(
        path="/streaming/demo",
        title="Streaming demo fragment",
        hidden=True,
        show_in_sidebar=False,
        interactive_demo=True,
    ),
    ShowcasePage(
        path="/streaming/retry",
        title="Streaming retry fragment",
        hidden=True,
        show_in_sidebar=False,
    ),
    ShowcasePage(
        path="/islands",
        title="Islands",
        section="Rich",
        description="Framework-agnostic mount roots plus no-build state primitives (grid, wizard, upload).",
        nav_order=30,
        index_card=True,
        index_order=120,
        interactive_demo=True,
        tags=("islands", "alpine"),
    ),
    ShowcasePage(
        path="/islands/remount",
        title="Islands remount fragment",
        hidden=True,
        show_in_sidebar=False,
    ),
    ShowcasePage(
        path="/islands/grid-state",
        title="Islands grid state",
        show_in_sidebar=False,
        interactive_demo=True,
        tags=("islands", "grid"),
    ),
    ShowcasePage(
        path="/islands/wizard-state",
        title="Islands wizard state",
        show_in_sidebar=False,
        interactive_demo=True,
        tags=("islands", "wizard"),
    ),
    ShowcasePage(
        path="/islands/upload-state",
        title="Islands upload state",
        show_in_sidebar=False,
        interactive_demo=True,
        tags=("islands", "upload"),
    ),
    ShowcasePage(
        path="/messenger",
        title="Messenger",
        section="Rich",
        description=(
            "message_bubble, message_thread, typing_indicator, chat_input, conversation_list."
        ),
        nav_order=40,
        index_card=True,
        index_order=230,
        tags=("messenger", "chat"),
    ),
    ShowcasePage(
        path="/social",
        title="Social Media",
        section="Rich",
        description="post_card, comment, profile_header, avatar_stack, trending_tag, mention.",
        nav_order=50,
        index_card=True,
        index_order=240,
        tags=("social", "post_card"),
    ),
    ShowcasePage(
        path="/video",
        title="Video Platform",
        section="Rich",
        description="video_card, channel_card, video_thumbnail, live_badge, playlist, chapter_list.",
        nav_order=60,
        index_card=True,
        index_order=250,
        tags=("video", "playlist"),
    ),
)


def page_by_path() -> dict[str, ShowcasePage]:
    """Return registry entries keyed by route path."""
    return {page.path: page for page in PAGES}


def visible_pages() -> tuple[ShowcasePage, ...]:
    """Non-hidden pages (for search serialization in Epic 2)."""
    return tuple(page for page in PAGES if not page.hidden)


def nav_sections() -> tuple[tuple[str, tuple[ShowcasePage, ...]], ...]:
    """Sidebar sections in display order."""
    grouped: dict[str, list[ShowcasePage]] = {name: [] for name in SECTION_ORDER}
    for page in PAGES:
        if page.hidden or not page.show_in_sidebar or not page.section:
            continue
        grouped[page.section].append(page)
    return tuple(
        (section, tuple(sorted(pages, key=lambda item: item.nav_order)))
        for section in SECTION_ORDER
        for pages in [grouped[section]]
        if pages
    )


def index_cards() -> tuple[ShowcasePage, ...]:
    """Home page component gallery card grid entries in display order."""
    return tuple(
        sorted((page for page in PAGES if page.index_card), key=lambda item: item.index_order)
    )


def golden_screen_pages() -> tuple[ShowcasePage, ...]:
    """Golden-screen archetype fixtures for nav, search, and the home index."""
    return tuple(
        sorted(
            (page for page in PAGES if page.golden_screen and not page.hidden),
            key=lambda item: (item.nav_order, item.path),
        )
    )


def shell_recipe_pages() -> tuple[ShowcasePage, ...]:
    """Standalone shell recipe demos (excludes golden-screen fixtures)."""
    return tuple(
        sorted(
            (
                page
                for page in PAGES
                if page.shell_recipe
                and not page.golden_screen
                and not page.hidden
                and page.show_in_sidebar
            ),
            key=lambda item: (item.nav_order, item.path),
        )
    )
