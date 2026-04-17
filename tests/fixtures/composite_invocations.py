"""Canonical "valid invocation" fixtures for chirp-ui composite macros.

Used by ``tests/test_composite_contracts.py`` to assert each composite renders
without ``ChirpUIValidationWarning``. New composites must be added here so the
contract test exercises them.

A composite is a macro that assembles multiple sub-macros into a complete
semantic structure (vs. a primitive that emits one element). The list is
hand-curated — see ``.context/composite-contracts-plan.md`` § Sprint 0 D1.

Each fixture provides:

- ``name``        — stable id for parametrized test ids
- ``template``    — source filename, for human-readable failure messages
- ``source``     — full template string (imports + macro invocation)
- ``context``    — variables passed to ``render(**context)``
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CompositeFixture:
    name: str
    template: str
    source: str
    context: dict[str, Any] = field(default_factory=dict)


def _tag_toggle(tag: str) -> str:
    return f"/tags/{tag}"


COMPOSITE_FIXTURES: list[CompositeFixture] = [
    CompositeFixture(
        name="card",
        template="chirpui/card.html",
        source=(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="My Card", subtitle="Subtitle", variant="feature") %}'
            "<p>Body content.</p>"
            "{% end %}"
        ),
    ),
    CompositeFixture(
        name="card_with_slots",
        template="chirpui/card.html",
        source=(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="Settings", icon="gear") %}'
            "{% slot header_actions %}<button>...</button>{% end %}"
            "<p>Body.</p>"
            "{% slot footer %}Tags here{% end %}"
            "{% end %}"
        ),
    ),
    CompositeFixture(
        name="modal",
        template="chirpui/modal.html",
        source=(
            '{% from "chirpui/modal.html" import modal %}'
            '{% call modal("settings-modal", title="Settings", size="md") %}'
            "<p>Modal body.</p>"
            "{% slot footer %}<button>Cancel</button>{% end %}"
            "{% end %}"
        ),
    ),
    CompositeFixture(
        name="panel",
        template="chirpui/panel.html",
        source=(
            '{% from "chirpui/panel.html" import panel %}'
            '{% call panel(title="Activity", subtitle="Recent events", surface_variant="muted") %}'
            "<div>Activity rows.</div>"
            "{% end %}"
        ),
    ),
    CompositeFixture(
        name="accordion",
        template="chirpui/accordion.html",
        source=(
            '{% from "chirpui/accordion.html" import accordion, accordion_item %}'
            '{% call accordion(name="faq") %}'
            '{% call accordion_item("How do I sign up?", open=true) %}'
            "Click Sign Up."
            "{% end %}"
            '{% call accordion_item("How do I reset?") %}'
            "Use Forgot Password."
            "{% end %}"
            "{% end %}"
        ),
    ),
    CompositeFixture(
        name="form",
        template="chirpui/forms.html",
        source=(
            '{% from "chirpui/forms.html" import form %}'
            '{% call form("/save", method="post") %}'
            '<input name="title">'
            "{% end %}"
        ),
    ),
    CompositeFixture(
        name="form_with_htmx",
        template="chirpui/forms.html",
        source=(
            '{% from "chirpui/forms.html" import form %}'
            '{% call form("/save", method="post", '
            'hx={"post": "/save", "target": "#result", "swap": "innerHTML"}) %}'
            '<input name="title">'
            "{% end %}"
        ),
    ),
    CompositeFixture(
        name="feature_section",
        template="chirpui/feature_section.html",
        source=(
            '{% from "chirpui/feature_section.html" import feature_section %}'
            '{% call feature_section(layout="split", variant="halo", reverse=true) %}'
            "{% slot eyebrow %}New{% end %}"
            "{% slot title %}Lightning fast builds{% end %}"
            "<p>Description.</p>"
            '{% slot media %}<img src="/x" alt="">{% end %}'
            "{% end %}"
        ),
    ),
    CompositeFixture(
        name="site_shell",
        template="chirpui/site_shell.html",
        source=(
            '{% from "chirpui/site_shell.html" import site_shell %}'
            "{% call site_shell(ambient=true) %}"
            "{% slot header %}<header>Top</header>{% end %}"
            "<main>Content</main>"
            "{% slot footer %}<footer>Bottom</footer>{% end %}"
            "{% end %}"
        ),
    ),
    CompositeFixture(
        name="site_header",
        template="chirpui/site_header.html",
        source=(
            '{% from "chirpui/site_header.html" import site_header %}'
            '{% call site_header(brand_url="/", layout="start", variant="glass") %}'
            "{% slot brand %}LOGO{% end %}"
            '{% slot nav %}<a href="/docs">Docs</a>{% end %}'
            "{% slot tools %}<button>Toggle</button>{% end %}"
            "{% end %}"
        ),
    ),
    CompositeFixture(
        name="site_footer",
        template="chirpui/site_footer.html",
        source=(
            '{% from "chirpui/site_footer.html" import site_footer, footer_column, footer_link %}'
            '{% call site_footer(layout="columns") %}'
            '{% slot brand %}<a href="/">Logo</a>{% end %}'
            '{% call footer_column(title="Product") %}'
            '{{ footer_link("/docs", "Docs") }}'
            "{% end %}"
            "{% slot colophon %}© 2026{% end %}"
            "{% end %}"
        ),
    ),
    CompositeFixture(
        name="filter_bar",
        template="chirpui/filter_bar.html",
        source=(
            '{% from "chirpui/filter_bar.html" import filter_bar %}'
            '{% call filter_bar("/skills", surface_variant="muted", density="sm") %}'
            '<div class="chirpui-action-strip__primary">Primary</div>'
            '<div class="chirpui-action-strip__controls">Controls</div>'
            '<div class="chirpui-action-strip__actions">Actions</div>'
            "{% end %}"
        ),
    ),
    CompositeFixture(
        name="command_bar",
        template="chirpui/command_bar.html",
        source=(
            '{% from "chirpui/command_bar.html" import command_bar %}'
            '{% from "chirpui/button.html" import btn %}'
            '{% call command_bar(surface_variant="default", density="sm") %}'
            '{{ btn("New", variant="primary") }}'
            '{{ btn("Export", variant="ghost") }}'
            "{% end %}"
        ),
    ),
    CompositeFixture(
        name="suspense_slot",
        template="chirpui/suspense.html",
        source=(
            '{% from "chirpui/suspense.html" import suspense_slot %}'
            '{{ suspense_slot("user-profile", skeleton_variant="card") }}'
        ),
    ),
    CompositeFixture(
        name="suspense_group",
        template="chirpui/suspense.html",
        source=(
            '{% from "chirpui/suspense.html" import suspense_slot, suspense_group %}'
            "{% call suspense_group() %}"
            '{{ suspense_slot("nav") }}'
            '{{ suspense_slot("footer") }}'
            "{% end %}"
        ),
    ),
    CompositeFixture(
        name="surface",
        template="chirpui/surface.html",
        source=(
            '{% from "chirpui/surface.html" import surface %}'
            '{% call surface(variant="muted", full_width=true) %}'
            "<p>Surface body.</p>"
            "{% end %}"
        ),
    ),
    CompositeFixture(
        name="resource_index",
        template="chirpui/resource_index.html",
        source=(
            '{% from "chirpui/resource_index.html" import resource_index %}'
            "{% call resource_index("
            'title="Skills", search_action="/search", query="",'
            ' results_layout="grid", results_cols=2, has_results=true) %}'
            '<article class="chirpui-card">Result row</article>'
            "{% end %}"
        ),
    ),
    CompositeFixture(
        name="tag_browse_tray",
        template="chirpui/tag_browse.html",
        source=(
            '{% from "chirpui/tag_browse.html" import tag_browse_tray %}'
            "{{ tag_browse_tray("
            '"my-filters", "Filter by tags", tags, selected_tags,'
            " tag_toggle_url, clear_url) }}"
        ),
        context={
            "tags": ["python", "rust", "go"],
            "selected_tags": ["python"],
            "tag_toggle_url": _tag_toggle,
            "clear_url": "/tags/clear",
        },
    ),
]
