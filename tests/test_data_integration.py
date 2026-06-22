"""Integration tests for component-showcase data page.

Requires chirp (pip install chirp or uv sync --group showcase).
"""

import ast
import re
import sys
import warnings
from pathlib import Path

import pytest

from chirp_ui.theme_packs import THEME_PACKS
from chirp_ui.validation import ChirpUIDeprecationWarning, ChirpUIValidationWarning

pytest.importorskip("chirp")

from chirp.testing import TestClient

_SHOWCASE_DIR = Path(__file__).resolve().parent.parent / "examples" / "component-showcase"
_SHOWCASE_APP = _SHOWCASE_DIR / "app.py"

SHOWCASE_ROUTE_SMOKE_PATHS = (
    "/",
    "/demo",
    "/htmx",
    "/navigation",
    "/layout",
    "/chrome",
    "/shell-actions",
    "/sections",
    "/carousel",
    "/cards",
    "/forms",
    "/appearance-tone",
    "/theme-packs",
    "/theme-packs/preview/atlas/light",
    "/ui",
    "/islands",
    "/islands/grid-state",
    "/islands/wizard-state",
    "/islands/upload-state",
    "/streaming",
    "/message-turn",
    "/composer",
    "/data-display",
    "/catalog-shell",
    "/catalog-shell?q=rag&category=intelligence",
    "/operations-shell",
    "/operations-shell?q=queues&area=compute&status=warning",
    "/operations-shell-workspace",
    "/operations-shell-workspace?q=queues&area=compute&status=warning",
    "/support-shell",
    "/support-shell?q=latency&queue=priority&status=danger",
    "/screen-command-center",
    "/screen-command-center?q=queues&area=compute&status=warning",
    "/screen-review-queue",
    "/screen-review-queue?q=latency&queue=priority&status=danger",
    "/screen-agent-run-monitor",
    "/screen-product-docs-home",
    "/calendar",
    "/calendar/2026/5",
    "/calendar/2026/05",
    "/data",
    "/effects",
    "/typography",
    "/ascii-primitives",
    "/buttons",
    "/dashboard",
    "/animation",
    "/ascii",
    "/messenger",
    "/social",
    "/video",
    "/data/table?page=1&sort=name",
    "/data/bulk-bar",
    "/data/export",
    "/layout/dir?dir=rtl",
    "/animation/swap-demo",
    "/islands/remount",
)

SHOWCASE_FRAGMENT_OR_ACTION_ROUTES = {
    "/toast",
    "/showcase/pages.json",
    "/demo/submit",
    "/demo/stream",
    "/forms/demo",
    "/ui/tab/{name}",
    "/streaming/demo",
    "/streaming/retry",
    "/composer/send",
    "/composer/abort",
    "/composer/dismiss/{file_id}",
    "/data/table",
    "/data/bulk-bar",
    "/data/export",
    "/layout/dir",
    "/animation/swap-demo",
}


def _showcase_route_patterns() -> set[str]:
    patterns: set[str] = set()
    route_sources = (
        _SHOWCASE_APP,
        _SHOWCASE_DIR / "routes" / "components.py",
        _SHOWCASE_DIR / "routes" / "demos.py",
        _SHOWCASE_DIR / "routes" / "shells.py",
        _SHOWCASE_DIR / "routes" / "screens.py",
    )
    for source in route_sources:
        for line in source.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line.startswith("@app.route("):
                continue
            expr = ast.parse(line[1:]).body[0].value
            patterns.add(ast.literal_eval(expr.args[0]))
    return patterns


def _route_pattern_matches(pattern: str, path: str) -> bool:
    path = path.split("?", 1)[0]
    regex = re.escape(pattern)
    regex = re.sub(r"\\\{[^/]+\\\}", r"[^/]+", regex)
    return re.fullmatch(regex, path) is not None


ISLAND_ROUTE_SMOKE_PATHS = (
    "/islands",
    "/islands/grid-state",
    "/islands/wizard-state",
    "/islands/upload-state",
    "/islands/remount",
)

ISLAND_TEMPLATE_PATHS = (
    "showcase/islands.html",
    "showcase/islands_grid_state.html",
    "showcase/islands_wizard_state.html",
    "showcase/islands_upload_state.html",
)


@pytest.fixture
def showcase_app():
    """Load the component-showcase app."""
    if str(_SHOWCASE_DIR) not in sys.path:
        sys.path.insert(0, str(_SHOWCASE_DIR))
    from app import app

    return app


class TestDataPage:
    """Verify /data and /data/table routes return 200 and expected HTML."""

    def test_showcase_page_routes_have_smoke_representatives(self) -> None:
        missing = sorted(
            route
            for route in _showcase_route_patterns() - SHOWCASE_FRAGMENT_OR_ACTION_ROUTES
            if not any(_route_pattern_matches(route, path) for path in SHOWCASE_ROUTE_SMOKE_PATHS)
        )
        assert not missing, "Showcase page routes missing route-smoke coverage: " + ", ".join(
            missing
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("path", SHOWCASE_ROUTE_SMOKE_PATHS)
    async def test_showcase_routes_return_200(self, showcase_app, path: str) -> None:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", ChirpUIValidationWarning)
            warnings.simplefilter("always", ChirpUIDeprecationWarning)
            async with TestClient(showcase_app) as client:
                response = await client.get(path)
        assert response.status == 200
        chirp_warnings = [
            warning
            for warning in caught
            if issubclass(warning.category, (ChirpUIValidationWarning, ChirpUIDeprecationWarning))
        ]
        assert not chirp_warnings, f"{path} emitted chirp-ui warnings: " + "; ".join(
            str(warning.message) for warning in chirp_warnings
        )

    @pytest.mark.asyncio
    async def test_navigation_page_returns_dense_example(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/navigation")
            assert response.status == 200
            assert "Dense Object Navigation" in response.text
            assert "Project workspace navigation" in response.text
            assert "Settings workspace navigation" in response.text
            assert "Cloud Console Navigation" in response.text
            assert "Cloud console global navigation" in response.text
            assert "Cloud console favorites" in response.text
            assert "Suite Work Hub Navigation" in response.text
            assert "Suite work hub global navigation" in response.text
            assert "Suite work hub personal shortcuts" in response.text
            assert "Suite work hub saved views" in response.text
            assert "Ops Console Navigation" in response.text
            assert "Ops console global navigation" in response.text
            assert "Ops dashboard controls" in response.text
            assert "Jump to dashboard, log, trace" in response.text
            assert "Keyboard-First Tracker Navigation" in response.text
            assert "Tracker global navigation" in response.text
            assert "Tracker display controls" in response.text
            assert "Go to issue, project, view" in response.text
            assert "Knowledge Workspace Navigation" in response.text
            assert "Knowledge workspace global navigation" in response.text
            assert "Knowledge page controls" in response.text
            assert "Search or jump to page" in response.text
            assert "Editor Workbench Navigation" in response.text
            assert "Editor workbench global navigation" in response.text
            assert "Editor tool navigation" in response.text
            assert "Find file, frame, action" in response.text
            assert "Business Object Console Navigation" in response.text
            assert "Business object console global navigation" in response.text
            assert "Business object list controls" in response.text
            assert "Search customers, invoices, IDs" in response.text
            assert "Collaboration Inbox Navigation" in response.text
            assert "Collaboration inbox global navigation" in response.text
            assert "Collaboration inbox controls" in response.text
            assert "Jump to channel, DM, thread" in response.text
            assert "Developer Platform Navigation" in response.text
            assert "Developer platform global navigation" in response.text
            assert "Developer platform list controls" in response.text
            assert "Search or go to project, issue, MR" in response.text
            assert "Reference Docs Navigation" in response.text
            assert "Reference docs global navigation" in response.text
            assert "Reference docs page controls" in response.text
            assert "Search docs or jump to topic" in response.text
            assert "chirpui-breadcrumbs__overflow" in response.text
            assert "chirpui-route-tab__badge" in response.text
            assert "chirpui-route-tab__badge--reserved" in response.text
            assert "chirpui-sidebar__badge--loading" in response.text
            assert "chirpui-scope-switcher" in response.text
            assert "chirpui-saved-view-strip" in response.text
            assert "chirpui-command-palette-trigger--sm" in response.text
            assert "Find service, project, deployment" in response.text
            assert "Search work, people, projects" in response.text
            assert response.text.count("chirpui-frame--sidebar-start") >= 8
            assert "data-showcase-nav-shell-frame" not in response.text
            assert "data-showcase-nav-sidebar-viewport" not in response.text
            assert "/static/chirpui-logo.svg" in response.text
            logo_response = await client.get("/static/chirpui-logo.svg")
            assert logo_response.status == 200
            assert "<svg" in logo_response.text

    @pytest.mark.asyncio
    async def test_data_filter_bar_uses_layout_affinity_contract(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/data")

        assert response.status == 200
        text = response.text
        assert 'id="data_filters"' in text
        assert 'data-chirpui-role="search"' in text
        assert 'data-chirpui-pressure="flex"' in text
        assert 'data-chirpui-affinity="fill"' in text
        assert 'data-chirpui-role="filters"' in text
        assert 'data-chirpui-pressure="compress"' in text
        assert 'data-chirpui-role="actions"' in text
        assert 'data-chirpui-pressure="rigid"' in text
        assert 'data-chirpui-affinity="end"' in text

    @pytest.mark.asyncio
    async def test_layout_page_uses_layout_affinity_primitives_contract(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/layout")

        assert response.status == 200
        text = response.text
        assert "layout-affinity-demo" in text
        assert 'data-chirpui-role="rail nav"' in text
        assert 'data-chirpui-role="content"' in text
        assert 'data-chirpui-role="metadata"' in text
        assert 'data-chirpui-role="actions"' in text
        assert 'data-chirpui-pressure="compress"' in text
        assert 'data-chirpui-pressure="flex"' in text
        assert 'data-chirpui-pressure="rigid"' in text
        assert 'data-chirpui-affinity="fill"' in text
        assert 'data-chirpui-affinity="end"' in text

    @pytest.mark.asyncio
    async def test_catalog_shell_returns_layered_catalog_recipe(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/catalog-shell?q=rag&category=intelligence")

        assert response.status == 200
        assert "Catalog search shell" in response.text
        assert "Layered catalog browser" in response.text
        assert "Intelligence" in response.text
        assert "VectorLake" in response.text
        assert "Design a RAG workflow" in response.text
        assert "catalog-shell-product-card" in response.text
        assert "catalog-shell-doc-link" in response.text
        assert "catalog-shell-command-bar" in response.text
        assert "chirpui-action-strip--wrap" in response.text
        assert "chirpui-action-strip--scroll" not in response.text
        assert "1 doc" in response.text
        assert "1 records" not in response.text
        assert 'id="catalog-shell-surface"' in response.text
        assert 'id="catalog-shell-frame"' in response.text
        assert 'hx-get="/catalog-shell"' in response.text
        assert 'hx-trigger="input changed delay:120ms, search"' in response.text
        assert 'hx-select="#catalog-shell-frame"' in response.text
        assert 'hx-push-url="true"' in response.text
        assert "x-on:htmx:before-request.window" in response.text
        assert "catalog-shell-pending" in response.text

    @pytest.mark.asyncio
    async def test_catalog_shell_progressive_enhancement_contract(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get(
                "/catalog-shell?q=rag&category=intelligence&family=Assistants&version=latest"
            )

        assert response.status == 200
        text = response.text
        assert (
            '<form id="catalog-shell-controls" class="catalog-shell-search" action="/catalog-shell" method="get"'
            in text
        )
        assert (
            '<label class="chirpui-visually-hidden" for="catalog-shell-query">Search product documentation</label>'
            in text
        )
        assert 'name="category" value="intelligence"' in text
        assert 'name="family" value="Assistants"' in text
        assert 'name="version" value="latest"' in text
        assert 'id="catalog-shell-state" hidden' in text
        assert 'hx-target="#catalog-shell-surface"' in text
        assert 'hx-select="#catalog-shell-surface"' in text
        assert 'hx-target="#catalog-shell-frame"' in text
        assert 'hx-select="#catalog-shell-frame"' in text
        assert 'hx-include="#catalog-shell-query, #catalog-shell-state"' in text
        assert 'hx-sync="#catalog-shell-frame:replace"' in text
        assert 'role="status" aria-live="polite"' in text
        assert 'data-chirpui-role="search"' in text
        assert 'data-chirpui-pressure="flex"' in text
        assert 'data-chirpui-affinity="fill"' in text
        assert 'data-chirpui-role="hints"' in text
        assert 'data-chirpui-pressure="compress"' in text
        assert 'data-chirpui-affinity="end"' in text
        assert 'data-chirpui-role="status"' in text
        assert 'data-chirpui-pressure="rigid"' in text
        assert text.count('hx-indicator="#catalog-shell-pending"') >= 6
        assert re.search(
            r'<a class="catalog-shell-category-link[^"]*" href="/catalog-shell\?[^"]*category=data',
            text,
        )
        assert re.search(
            r'<a class="catalog-shell-family-link[^"]*" href="/catalog-shell\?[^"]*family=Assistants',
            text,
        )

    @pytest.mark.asyncio
    async def test_catalog_shell_scoped_counts_use_visible_doc_language(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            all_response = await client.get("/catalog-shell?version=latest")
            intelligence_response = await client.get(
                "/catalog-shell?category=intelligence&version=latest"
            )
            rag_response = await client.get(
                "/catalog-shell?q=rag&category=intelligence&version=latest"
            )
            data_response = await client.get("/catalog-shell?category=data&version=latest")

        assert all_response.status == 200
        assert intelligence_response.status == 200
        assert rag_response.status == 200
        assert data_response.status == 200
        assert "12 docs" in all_response.text
        assert "3 docs" in intelligence_response.text
        assert "1 doc" in rag_response.text
        assert "2 docs" in data_response.text
        assert "records" not in intelligence_response.text
        assert "records" not in rag_response.text
        assert "records" not in data_response.text

    @pytest.mark.asyncio
    async def test_catalog_shell_command_surface_wraps_instead_of_scrolling(
        self, showcase_app
    ) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/catalog-shell?version=latest")

        assert response.status == 200
        assert "catalog-shell-command-bar" in response.text
        assert "chirpui-action-strip--wrap" in response.text
        assert "chirpui-action-strip--scroll" not in response.text
        assert 'aria-label="Suggested catalog searches"' in response.text

    @pytest.mark.asyncio
    async def test_operations_shell_returns_payoff_experiment(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/operations-shell?q=queues&area=compute&status=warning")

        assert response.status == 200
        text = response.text
        assert "Operations workspace shell" in text
        assert "Layout-affinity payoff experiment" in text
        assert "Payoff readout" in text
        assert "Forge Runners" in text
        assert "Queue depth above target" in text
        assert "Current resolver gap: panel placement is page-owned CSS." in text
        assert 'id="operations-shell-surface"' in text
        assert 'id="operations-shell-frame"' in text
        assert "ops-shell-command-bar" in text
        assert "ops-shell-filter-bar" in text
        assert "chirpui-action-strip--wrap" in text
        assert "chirpui-action-strip--scroll" not in text
        assert 'data-chirpui-role="search"' in text
        assert 'data-chirpui-role="hints"' in text
        assert 'data-chirpui-role="status"' in text
        assert 'data-chirpui-role="filters"' in text
        assert 'data-chirpui-role="actions"' in text
        assert 'data-chirpui-role="rail nav"' in text
        assert 'data-chirpui-role="content"' in text
        assert 'data-chirpui-pressure="flex"' in text
        assert 'data-chirpui-pressure="compress"' in text
        assert 'data-chirpui-pressure="rigid"' in text
        assert 'data-chirpui-affinity="fill"' in text
        assert 'data-chirpui-affinity="end"' in text
        assert 'hx-target="#operations-shell-frame"' in text
        assert 'hx-select="#operations-shell-frame"' in text
        assert 'hx-indicator="#operations-shell-pending"' in text

    @pytest.mark.asyncio
    async def test_operations_shell_workspace_variant_preserves_baseline_comparison(
        self, showcase_app
    ) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get(
                "/operations-shell-workspace?q=queues&area=compute&status=warning"
            )

        assert response.status == 200
        text = response.text
        assert "Operations workspace shell: workspace_shell" in text
        assert "Workspace shell variant" in text
        assert "Forge Runners" in text
        assert "Queue depth above target" in text
        assert "inspector_panel owns the selected-object shape." in text
        assert "chirpui-workspace-shell" in text
        assert "chirpui-workspace-shell__sidebar" in text
        assert "chirpui-workspace-shell__inspector" in text
        assert "chirpui-filter-rail" in text
        assert "chirpui-result-collection" in text
        assert "chirpui-result-card" in text
        assert "chirpui-inspector-panel" in text
        assert "chirpui-metric-strip" in text
        assert 'id="operations-workspace-shell-surface"' in text
        assert 'id="operations-workspace-shell-frame"' in text
        assert "ops-shell-command-bar" in text
        assert "ops-shell-filter-bar" in text
        assert 'class="ops-shell-workspace"' not in text
        assert 'class="ops-shell-rail ops-shell-rail--areas"' not in text
        assert 'action="/operations-shell-workspace"' in text
        assert 'hx-get="/operations-shell-workspace"' in text
        assert 'hx-target="#operations-workspace-shell-frame"' in text
        assert 'hx-select="#operations-workspace-shell-frame"' in text
        assert 'hx-indicator="#operations-workspace-shell-pending"' in text

    @pytest.mark.asyncio
    async def test_support_shell_repeats_payoff_shape_in_second_domain(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/support-shell?q=latency&queue=priority&status=danger")

        assert response.status == 200
        text = response.text
        assert "Support queue shell" in text
        assert "Second layout-affinity payoff experiment" in text
        assert "Workspace shell readout" in text
        assert "VectorShop" in text
        assert "Latency alert fired" in text
        assert "inspector_panel owns the selected-ticket shape." in text
        assert "chirpui-workspace-shell" in text
        assert "chirpui-workspace-shell__sidebar" in text
        assert "chirpui-workspace-shell__inspector" in text
        assert "chirpui-filter-rail" in text
        assert "chirpui-result-collection" in text
        assert "chirpui-result-card" in text
        assert "chirpui-inspector-panel" in text
        assert "chirpui-metric-strip" in text
        assert 'class="support-shell-workspace"' not in text
        assert 'class="support-shell-rail support-shell-rail--queues"' not in text
        assert "support-shell-rail-link" not in text
        assert "support-shell-card-grid" not in text
        assert 'id="support-shell-surface"' in text
        assert 'id="support-shell-frame"' in text
        assert "support-shell-command-bar" in text
        assert "support-shell-filter-bar" in text
        assert "chirpui-action-strip--wrap" in text
        assert "chirpui-action-strip--scroll" not in text
        assert 'data-chirpui-role="search"' in text
        assert 'data-chirpui-role="hints"' in text
        assert 'data-chirpui-role="status"' in text
        assert 'data-chirpui-role="filters"' in text
        assert 'data-chirpui-role="actions"' in text
        assert 'data-chirpui-role="rail nav"' in text
        assert 'data-chirpui-role="content"' in text
        assert 'data-chirpui-pressure="flex"' in text
        assert 'data-chirpui-pressure="compress"' in text
        assert 'data-chirpui-pressure="rigid"' in text
        assert 'data-chirpui-affinity="fill"' in text
        assert 'data-chirpui-affinity="end"' in text
        assert 'hx-target="#support-shell-frame"' in text
        assert 'hx-select="#support-shell-frame"' in text
        assert 'hx-indicator="#support-shell-pending"' in text

    @pytest.mark.asyncio
    async def test_golden_screen_routes_expose_profile_and_archetype_metadata(
        self, showcase_app
    ) -> None:
        async with TestClient(showcase_app) as client:
            command = await client.get("/screen-command-center?q=queues&area=compute")
            review = await client.get("/screen-review-queue?q=latency&queue=priority")

        assert command.status == 200
        assert 'data-screen-archetype="command-center"' in command.text
        assert 'data-screen-profile="atlas"' in command.text
        assert 'action="/screen-command-center"' in command.text
        assert 'hx-get="/screen-command-center"' in command.text
        assert "Golden screen: Command Center" in command.text
        assert "Forge Runners" in command.text

        assert review.status == 200
        assert 'data-screen-archetype="review-queue"' in review.text
        assert 'data-screen-profile="sage"' in review.text
        assert 'action="/screen-review-queue"' in review.text
        assert 'hx-get="/screen-review-queue"' in review.text
        assert "Golden screen: Review Queue" in review.text
        assert "VectorShop" in review.text

    @pytest.mark.asyncio
    async def test_remaining_golden_screen_routes_expose_profile_and_archetype_metadata(
        self, showcase_app
    ) -> None:
        async with TestClient(showcase_app) as client:
            agent = await client.get("/screen-agent-run-monitor")
            product = await client.get("/screen-product-docs-home")

        assert agent.status == 200
        assert 'data-screen-archetype="agent-run-monitor"' in agent.text
        assert 'data-screen-profile="signal"' in agent.text
        assert "Golden screen: Agent Run Monitor" in agent.text
        assert "Run 8729: procurement policy review" in agent.text
        assert "chirpui-timeline" in agent.text
        assert "chirpui-result-collection" in agent.text

        assert product.status == 200
        assert 'data-screen-archetype="product-docs-home"' in product.text
        assert 'data-screen-profile="ember"' in product.text
        assert "Signal Loom" in product.text
        assert "Open screen catalog" in product.text
        assert "chirpui-logo-cloud" in product.text
        assert "chirpui-cta-band" in product.text

    def test_support_shell_uses_workspace_shell_instead_of_page_owned_shell_grid(self) -> None:
        support_template = (
            _SHOWCASE_DIR / "templates" / "showcase" / "support_shell.html"
        ).read_text(encoding="utf-8")
        operations_template = (
            _SHOWCASE_DIR / "templates" / "showcase" / "operations_shell.html"
        ).read_text(encoding="utf-8")
        operations_workspace_template = (
            _SHOWCASE_DIR / "templates" / "showcase" / "operations_shell_workspace.html"
        ).read_text(encoding="utf-8")
        base_template = (_SHOWCASE_DIR / "templates" / "base.html").read_text(encoding="utf-8")
        ops_shell_css = (
            _SHOWCASE_DIR / "templates" / "showcase" / "_css" / "ops_shell.css.html"
        ).read_text(encoding="utf-8")

        assert "workspace_shell(" in support_template
        assert "panel(title=support_metrics.tickets" in support_template
        assert 'block(cls="support-shell-spotlight")' not in support_template
        assert "support-shell-spotlight-head" not in support_template
        assert "frame(" not in support_template
        assert "frame(" in operations_template
        assert "workspace_shell(" in operations_workspace_template
        assert "panel(title=ops_metrics.workloads" in operations_workspace_template
        assert 'block(cls="ops-shell-spotlight")' not in operations_workspace_template
        assert "ops-shell-spotlight-head" not in operations_workspace_template
        assert "ops-shell-workload-measures" not in operations_workspace_template
        assert "frame(" not in operations_workspace_template
        assert ".support-shell-workspace {" not in base_template
        assert ".support-shell-frame {" not in base_template
        assert ".support-shell-rail {" not in base_template
        assert ".support-shell-ticket-measures {" not in base_template
        assert ".support-shell-spotlight-head" not in base_template
        assert ".support-shell-command-bar .chirpui-action-strip__inner" not in base_template
        assert ".ops-shell-command-bar .chirpui-action-strip__inner" not in base_template
        assert ".ops-shell-workspace {" in ops_shell_css
        assert ".ops-shell-frame {" in ops_shell_css

    @pytest.mark.asyncio
    async def test_htmx_page_does_not_emit_demo_toasts_on_load(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/htmx")
        assert response.status == 200
        toast_section = response.text.split("<h3>oob_toast</h3>", 1)[1].split(
            "<h3>counter_badge</h3>", 1
        )[0]
        assert "oob_toast(&quot;Item saved!&quot;" in toast_section
        assert 'hx-swap-oob="beforeend:#chirpui-toasts"' not in toast_section

    @pytest.mark.asyncio
    async def test_theme_pack_showcase_uses_pack_catalog(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/theme-packs")
        assert response.status == 200
        assert "Theme Packs" in response.text
        for pack in THEME_PACKS:
            assert pack.label in response.text
            assert f"/static/{pack.path}" in response.text
            for mode in pack.modes:
                assert f'/theme-packs/preview/{pack.name}/{mode}"' in response.text

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("pack_name", "mode"),
        [(pack.name, mode) for pack in THEME_PACKS for mode in pack.modes],
    )
    async def test_theme_pack_preview_routes_render_isolated_css(
        self, showcase_app, pack_name: str, mode: str
    ) -> None:
        pack = next(pack for pack in THEME_PACKS if pack.name == pack_name)
        async with TestClient(showcase_app) as client:
            response = await client.get(f"/theme-packs/preview/{pack_name}/{mode}")
        assert response.status == 200
        assert f'data-theme="{mode}"' in response.text
        assert f'href="/static/{pack.path}"' in response.text
        assert pack.label in response.text
        assert "chirpui-btn" in response.text
        assert "chirpui-card" in response.text
        assert "chirpui-alert" in response.text
        assert "chirpui-field" in response.text

    @pytest.mark.asyncio
    async def test_theme_pack_preview_rejects_unknown_pack_or_mode(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            missing_pack = await client.get("/theme-packs/preview/missing/light")
            missing_mode = await client.get("/theme-packs/preview/atlas/sepia")
        assert missing_pack.status == 404
        assert missing_mode.status == 404

    @pytest.mark.asyncio
    async def test_composer_send_returns_message_bubble_fragment(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.post("/composer/send", data={"message": "hello"})
        assert response.status == 200
        assert "chirpui-message-bubble--right" in response.text
        assert "<p>hello</p>" in response.text

    @pytest.mark.asyncio
    async def test_composer_abort_returns_no_content(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.post("/composer/abort")
        assert response.status == 204

    @pytest.mark.asyncio
    async def test_composer_dismiss_returns_ok(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.post("/composer/dismiss/demo")
        assert response.status == 200

    @pytest.mark.asyncio
    async def test_effects_page_wraps_background_macros_with_canvas_height(
        self, showcase_app
    ) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/effects")
        assert response.status == 200
        html = response.text

        for root_class in (
            "chirpui-aurora",
            "chirpui-meteor",
            "chirpui-particle-bg",
            "chirpui-symbol-rain",
            "chirpui-holy-light",
            "chirpui-rune-field",
            "chirpui-constellation",
            "chirpui-scanline",
            "chirpui-grain",
        ):
            assert re.search(
                rf'class="{root_class}(?:[" ]|--).*?data-showcase-effect-fill',
                html,
                re.S,
            ), f"{root_class} showcase demo must call the wrapper macro with height"

        for replayable_class in (
            "chirpui-hover-wobble",
            "chirpui-hover-jello",
            "chirpui-hover-rubber",
        ):
            assert replayable_class in html

    @pytest.mark.asyncio
    @pytest.mark.parametrize("path", ISLAND_ROUTE_SMOKE_PATHS)
    async def test_island_showcase_routes_return_200(self, showcase_app, path: str) -> None:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", ChirpUIValidationWarning)
            warnings.simplefilter("always", ChirpUIDeprecationWarning)
            async with TestClient(showcase_app) as client:
                response = await client.get(path)
        assert response.status == 200
        chirp_warnings = [
            warning
            for warning in caught
            if issubclass(warning.category, (ChirpUIValidationWarning, ChirpUIDeprecationWarning))
        ]
        assert not chirp_warnings, f"{path} emitted chirp-ui warnings: " + "; ".join(
            str(warning.message) for warning in chirp_warnings
        )

    def test_island_showcase_templates_use_composed_patterns(self) -> None:
        stale_patterns = {
            "inline style": r"\bstyle=",
            "direct card class": r'cls="chirpui-card"',
            "raw back link": r"<p><a href=",
            "missing field modifier": r"chirpui-field--file",
        }
        for rel_path in ISLAND_TEMPLATE_PATHS:
            template = (_SHOWCASE_DIR / "templates" / rel_path).read_text(encoding="utf-8")
            for label, pattern in stale_patterns.items():
                assert not re.search(pattern, template), (
                    f"{rel_path} still uses stale island showcase pattern: {label}"
                )

    @pytest.mark.asyncio
    async def test_data_page_returns_200(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/data")
            assert response.status == 200
            assert "Data Display" in response.text
            assert 'id="data_table_content"' in response.text
            assert "chirpui-spinner" in response.text
            assert "chirpui-field--dense" in response.text
            assert 'style="min-width' not in response.text

    @pytest.mark.asyncio
    async def test_maturity_primitives_render_in_showcase(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            forms_response = await client.get("/forms")
            ui_response = await client.get("/ui")
            data_response = await client.get("/data")

        assert forms_response.status == 200
        assert ui_response.status == 200
        assert data_response.status == 200

        assert "chirpui-toggle-group" in forms_response.text
        assert "chirpui-slider" in forms_response.text
        assert "chirpui-label" in forms_response.text

        assert "chirpui-kbd" in ui_response.text
        assert "chirpui-separator" in ui_response.text
        assert "chirpui-aspect-ratio" in ui_response.text
        assert "chirpui-scroll-area" in ui_response.text
        assert "chirpui-item" in ui_response.text

        assert "chirpui-data-table" in data_response.text

    @pytest.mark.asyncio
    async def test_data_table_fragment_returns_200(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/data/table?page=1&sort=name")
            assert response.status == 200
            assert "chirpui-table" in response.text
            assert "Alice" in response.text
            assert "chirpui-pagination" in response.text
            assert "Showing" in response.text

    @pytest.mark.asyncio
    async def test_data_table_search_returns_filtered(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/data/table?q=alice&role=")
            assert response.status == 200
            assert "Alice" in response.text
            assert "Bob" not in response.text

    @pytest.mark.asyncio
    async def test_data_table_empty_search_shows_empty_state(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/data/table?q=nonexistentxyz&role=")
            assert response.status == 200
            assert "chirpui-empty-state" in response.text
            assert "No results" in response.text

    @pytest.mark.asyncio
    async def test_data_bulk_bar_and_export_accept_selected_values(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            bulk_response = await client.get(
                "/data/bulk-bar?selected=alice@example.com&selected=bob@example.com"
            )
            assert bulk_response.status == 200
            assert "2 selected" in bulk_response.text

            export_response = await client.get(
                "/data/export?selected=alice@example.com,bob@example.com"
            )
            assert export_response.status == 200
            assert "Alice,alice@example.com" in export_response.text
            assert "Bob,bob@example.com" in export_response.text
            assert "Carol" not in export_response.text
