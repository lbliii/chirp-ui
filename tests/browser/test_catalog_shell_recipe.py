"""Browser proof for the component-showcase catalog search shell recipe."""

import importlib.util
import socket
import sys
import threading
import time
from pathlib import Path

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine, wait_for_htmx
from tests.browser.gauntlet_detectors import assert_no_document_horizontal_overflow

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

_SHOWCASE_DIR = Path(__file__).resolve().parents[2] / "examples" / "component-showcase"
_SHOWCASE_APP = _SHOWCASE_DIR / "app.py"


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _load_showcase_app():
    if str(_SHOWCASE_DIR) not in sys.path:
        sys.path.insert(0, str(_SHOWCASE_DIR))
    spec = importlib.util.spec_from_file_location(
        "chirp_ui_component_showcase_browser", _SHOWCASE_APP
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.app


@pytest.fixture(scope="session")
def showcase_base_url():
    from pounce import ServerConfig
    from pounce.server import Server

    port = _find_free_port()
    app = _load_showcase_app()
    config = ServerConfig(
        host="127.0.0.1",
        port=port,
        log_level="warning",
        access_log=False,
    )
    server = Server(config, app)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    for _ in range(50):
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.1):
                break
        except OSError:
            time.sleep(0.1)
    else:
        raise RuntimeError(f"Showcase server did not start on port {port}")

    yield f"http://127.0.0.1:{port}"

    server.shutdown()
    thread.join(timeout=5)


@pytest.fixture
async def showcase_page():
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context()
        page = await ctx.new_page()
        yield page
        await ctx.close()
        await browser.close()


async def _assert_locator_has_no_horizontal_overflow(page, selector: str, label: str) -> None:
    result = await page.locator(selector).first.evaluate(
        """(el) => ({
            overflow: Math.ceil(el.scrollWidth - el.clientWidth),
            rect: (() => {
                const r = el.getBoundingClientRect();
                return { left: r.left, right: r.right, width: r.width };
            })(),
        })"""
    )

    assert result["overflow"] <= 1, {
        "label": label,
        "overflow": result["overflow"],
        "rect": result["rect"],
    }


async def _assert_children_contained(page, selector: str, label: str) -> None:
    failures = await page.locator(selector).first.evaluate(
        """(el) => {
            const parent = el.getBoundingClientRect();
            return [...el.children]
                .filter((child) => {
                    const style = getComputedStyle(child);
                    const rect = child.getBoundingClientRect();
                    return style.display !== "none"
                        && style.visibility !== "hidden"
                        && rect.width > 0
                        && rect.height > 0
                        && (rect.left < parent.left - 1 || rect.right > parent.right + 1);
                })
                .slice(0, 8)
                .map((child) => ({
                    className: child.className,
                    text: (child.textContent || "").trim().slice(0, 80),
                    rect: (() => {
                        const r = child.getBoundingClientRect();
                        return { left: r.left, right: r.right, width: r.width };
                    })(),
                    parent: { left: parent.left, right: parent.right, width: parent.width },
                }));
        }"""
    )

    assert not failures, {"label": label, "failures": failures}


@pytest.mark.parametrize(
    ("width", "height"),
    [(320, 640), (390, 844), (768, 1024), (1024, 768), (1280, 900)],
)
async def test_catalog_shell_responsive_command_surface_has_no_overflow(
    showcase_page,
    showcase_base_url: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + "/catalog-shell?version=latest")
    await wait_for_alpine(showcase_page)

    await expect(showcase_page.locator("#catalog-shell-query")).to_be_visible()
    await expect(showcase_page.locator(".catalog-shell-search .chirpui-btn")).to_be_visible()
    await expect(showcase_page.locator(".catalog-shell-hints")).to_be_visible()
    await assert_no_document_horizontal_overflow(showcase_page, f"catalog-shell-{width}x{height}")
    await _assert_locator_has_no_horizontal_overflow(
        showcase_page,
        ".catalog-shell-command-bar .chirpui-action-strip__inner",
        f"catalog-shell-command-inner-{width}x{height}",
    )
    await _assert_children_contained(
        showcase_page,
        ".catalog-shell-command-bar .chirpui-action-strip__inner",
        f"catalog-shell-command-children-{width}x{height}",
    )

    command_bounds = await showcase_page.locator(".catalog-shell-command-bar").bounding_box()
    assert command_bounds is not None
    assert command_bounds["x"] >= 0
    assert command_bounds["x"] + command_bounds["width"] <= width + 1


async def test_catalog_shell_facet_htmx_updates_url_results_and_boundary(
    showcase_page,
    showcase_base_url: str,
) -> None:
    await showcase_page.set_viewport_size({"width": 1024, "height": 768})
    await showcase_page.goto(
        showcase_base_url + "/catalog-shell?category=intelligence&version=latest"
    )
    await wait_for_alpine(showcase_page)

    await showcase_page.locator(".catalog-shell-category-link[aria-label='Data']").click()
    await wait_for_htmx(showcase_page)

    await expect(showcase_page).to_have_url(
        showcase_base_url + "/catalog-shell?category=data&version=latest"
    )
    await expect(showcase_page.locator("#catalog-shell-frame")).to_have_count(1)
    await expect(showcase_page.locator(".catalog-shell-workspace")).to_contain_text(
        "Data and analytics products"
    )
    await expect(showcase_page.locator(".catalog-shell-workspace")).to_contain_text("2 docs")
    await assert_no_document_horizontal_overflow(showcase_page, "catalog-shell-facet-data")


async def test_catalog_shell_hint_htmx_preserves_query_and_result_scope(
    showcase_page,
    showcase_base_url: str,
) -> None:
    await showcase_page.set_viewport_size({"width": 1024, "height": 768})
    await showcase_page.goto(
        showcase_base_url + "/catalog-shell?category=intelligence&version=latest"
    )
    await wait_for_alpine(showcase_page)

    await showcase_page.locator(".catalog-shell-hints a[data-query='rag']").click()
    await wait_for_htmx(showcase_page)

    await expect(showcase_page).to_have_url(
        showcase_base_url + "/catalog-shell?q=rag&category=intelligence"
    )
    await expect(showcase_page.locator("#catalog-shell-query")).to_have_value("rag")
    await expect(showcase_page.locator("#catalog-shell-frame")).to_have_count(1)
    await expect(showcase_page.locator(".catalog-shell-workspace")).to_contain_text("VectorLake")
    await expect(showcase_page.locator(".catalog-shell-workspace")).to_contain_text("1 doc")


@pytest.mark.parametrize(
    ("width", "height"),
    [(320, 640), (390, 844), (768, 1024), (1280, 900)],
)
async def test_data_filter_bar_layout_affinity_has_no_overflow(
    showcase_page,
    showcase_base_url: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + "/data")
    await wait_for_alpine(showcase_page)

    await expect(showcase_page.locator("#data_filters")).to_be_visible()
    await expect(showcase_page.locator('[data-chirpui-role="search"]')).to_be_visible()
    await expect(showcase_page.locator('[data-chirpui-role="filters"]')).to_be_visible()
    await expect(showcase_page.locator('[data-chirpui-role="actions"]')).to_be_visible()
    await assert_no_document_horizontal_overflow(showcase_page, f"data-filter-bar-{width}x{height}")
    await _assert_locator_has_no_horizontal_overflow(
        showcase_page,
        "#data_filters .chirpui-action-strip__inner",
        f"data-filter-inner-{width}x{height}",
    )
    await _assert_children_contained(
        showcase_page,
        "#data_filters .chirpui-action-strip__inner",
        f"data-filter-children-{width}x{height}",
    )


async def test_data_filter_bar_search_interaction_keeps_resolver_boundary(
    showcase_page,
    showcase_base_url: str,
) -> None:
    await showcase_page.set_viewport_size({"width": 390, "height": 844})
    await showcase_page.goto(showcase_base_url + "/data")
    await wait_for_alpine(showcase_page)

    search = showcase_page.locator('#data_filters input[name="q"]')
    await expect(search).to_be_visible()
    await search.fill("alice")
    await search.dispatch_event("keyup")
    await wait_for_htmx(showcase_page)

    await expect(showcase_page.locator("#data_table_content")).to_contain_text("Alice")
    await expect(showcase_page.locator("#data_table_content")).to_contain_text("Showing 1")
    await assert_no_document_horizontal_overflow(showcase_page, "data-filter-search-alice")
    await _assert_locator_has_no_horizontal_overflow(
        showcase_page,
        "#data_filters .chirpui-action-strip__inner",
        "data-filter-search-inner",
    )
    await _assert_children_contained(
        showcase_page,
        "#data_filters .chirpui-action-strip__inner",
        "data-filter-search-children",
    )


@pytest.mark.parametrize(
    ("width", "height"),
    [(320, 640), (390, 844), (768, 1024), (1280, 900)],
)
async def test_card_layout_affinity_has_no_overflow(
    showcase_page,
    showcase_base_url: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + "/cards")
    await wait_for_alpine(showcase_page)

    await expect(showcase_page.locator(".chirpui-card").first).to_be_visible()
    await expect(
        showcase_page.locator('.chirpui-card [data-chirpui-role="content"]').first
    ).to_be_visible()
    await expect(
        showcase_page.locator('.chirpui-resource-card [data-chirpui-role="metadata"]')
        .filter(has_text="builtin")
        .first
    ).to_be_visible()
    await expect(
        showcase_page.locator(
            '.chirpui-card__header-actions[data-chirpui-role="actions"]:has(.chirpui-btn)'
        ).first
    ).to_be_visible()
    await assert_no_document_horizontal_overflow(
        showcase_page, f"card-layout-affinity-{width}x{height}"
    )
    await _assert_locator_has_no_horizontal_overflow(
        showcase_page,
        ".chirpui-card",
        f"card-layout-affinity-card-{width}x{height}",
    )


@pytest.mark.parametrize(
    ("width", "height"),
    [(320, 640), (390, 844), (768, 1024), (1280, 900)],
)
async def test_layout_affinity_primitives_have_no_overflow(
    showcase_page,
    showcase_base_url: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + "/layout")
    await wait_for_alpine(showcase_page)

    await expect(showcase_page.locator(".layout-affinity-demo")).to_be_visible()
    await expect(showcase_page.locator('[data-chirpui-role~="rail"]')).to_be_visible()
    await expect(showcase_page.locator('[data-chirpui-role~="content"]').first).to_be_visible()
    await expect(
        showcase_page.locator('.layout-affinity-demo a[data-chirpui-role~="actions"]')
    ).to_be_visible()
    await assert_no_document_horizontal_overflow(
        showcase_page, f"layout-affinity-primitives-{width}x{height}"
    )
    await _assert_locator_has_no_horizontal_overflow(
        showcase_page,
        ".layout-affinity-demo",
        f"layout-affinity-demo-{width}x{height}",
    )
    await _assert_children_contained(
        showcase_page,
        ".layout-affinity-demo",
        f"layout-affinity-demo-children-{width}x{height}",
    )


@pytest.mark.parametrize(
    ("width", "height"),
    [(320, 640), (768, 1024), (1280, 900)],
)
async def test_showcase_forms_component_rhythm_has_no_overflow(
    showcase_page,
    showcase_base_url: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + "/forms")
    await wait_for_alpine(showcase_page)

    form = showcase_page.locator(
        ".chirpui-form:has(> .chirpui-field):has(> .chirpui-form-actions)"
    ).first
    await expect(form).to_be_visible()
    await expect(showcase_page.locator(".chirpui-form > .chirpui-field").first).to_be_visible()
    rhythm = await form.evaluate(
        """(form) => {
            const field = form.querySelector(":scope > .chirpui-field");
            const actions = form.querySelector(":scope > .chirpui-form-actions");
            const formStyle = getComputedStyle(form);
            return {
                display: formStyle.display,
                gap: formStyle.rowGap,
                fieldMargin: field ? getComputedStyle(field).marginBlockEnd : null,
                actionsMargin: actions ? getComputedStyle(actions).marginBlockStart : null,
            };
        }"""
    )
    assert rhythm["display"] == "flex"
    assert rhythm["gap"] != "normal"
    assert rhythm["fieldMargin"] == "0px"
    assert rhythm["actionsMargin"] == "0px"
    await assert_no_document_horizontal_overflow(
        showcase_page, f"showcase-forms-rhythm-{width}x{height}"
    )


@pytest.mark.parametrize(
    ("width", "height"),
    [(320, 640), (768, 1024), (1280, 900)],
)
async def test_showcase_fieldset_grouped_rhythm_has_no_overflow(
    showcase_page,
    showcase_base_url: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + "/forms")
    await wait_for_alpine(showcase_page)

    fieldset = showcase_page.locator(".chirpui-fieldset:has(> .chirpui-field)").first
    await expect(fieldset).to_be_visible()
    rhythm = await fieldset.evaluate(
        """(fieldset) => {
            const fields = [...fieldset.querySelectorAll(":scope > .chirpui-field")];
            return {
                firstMargin: fields[0] ? getComputedStyle(fields[0]).marginBlockEnd : null,
                secondStart: fields[1] ? getComputedStyle(fields[1]).marginBlockStart : null,
                minWidth: getComputedStyle(fieldset).minWidth,
            };
        }"""
    )
    assert rhythm["firstMargin"] == "0px"
    assert rhythm["secondStart"] != "0px"
    assert rhythm["minWidth"] == "0px"
    await assert_no_document_horizontal_overflow(
        showcase_page, f"showcase-fieldset-rhythm-{width}x{height}"
    )


@pytest.mark.parametrize(
    ("width", "height"),
    [(320, 640), (390, 844), (768, 1024), (1280, 900), (1440, 1000)],
)
async def test_workspace_shell_layout_affinity_has_no_overflow(
    showcase_page,
    showcase_base_url: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + "/chrome")
    await wait_for_alpine(showcase_page)

    await expect(showcase_page.locator(".chirpui-workspace-shell")).to_be_visible()
    await expect(showcase_page.locator(".chirpui-workspace-shell__inspector")).to_contain_text(
        "Inspector"
    )
    await expect(
        showcase_page.locator('.chirpui-workspace-shell [data-chirpui-role~="rail"]').first
    ).to_be_visible()
    await expect(
        showcase_page.locator('.chirpui-workspace-shell [data-chirpui-role~="content"]').first
    ).to_be_visible()
    await assert_no_document_horizontal_overflow(
        showcase_page, f"workspace-shell-layout-affinity-{width}x{height}"
    )
    await _assert_locator_has_no_horizontal_overflow(
        showcase_page,
        ".chirpui-workspace-shell",
        f"workspace-shell-{width}x{height}",
    )
    await _assert_children_contained(
        showcase_page,
        ".chirpui-workspace-shell__content-layout",
        f"workspace-shell-content-layout-{width}x{height}",
    )


@pytest.mark.parametrize(
    ("width", "height"),
    [(320, 640), (390, 844), (768, 1024), (1280, 900), (1440, 1000)],
)
async def test_operations_shell_payoff_experiment_has_no_overflow(
    showcase_page,
    showcase_base_url: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + "/operations-shell")
    await wait_for_alpine(showcase_page)

    await expect(showcase_page.locator("#operations-shell-surface")).to_be_visible()
    await expect(showcase_page.locator("#ops-shell-query")).to_be_visible()
    await expect(showcase_page.locator("#ops-shell-filter-form")).to_be_visible()
    await expect(showcase_page.locator("#operations-shell-frame")).to_be_visible()
    await expect(showcase_page.locator(".ops-shell-inspector")).to_contain_text("Inspector rail")
    await assert_no_document_horizontal_overflow(
        showcase_page, f"operations-shell-{width}x{height}"
    )
    await _assert_locator_has_no_horizontal_overflow(
        showcase_page,
        ".ops-shell-command-bar .chirpui-action-strip__inner",
        f"operations-shell-command-{width}x{height}",
    )
    await _assert_locator_has_no_horizontal_overflow(
        showcase_page,
        "#ops-shell-filter-form .chirpui-action-strip__inner",
        f"operations-shell-filter-{width}x{height}",
    )
    await _assert_locator_has_no_horizontal_overflow(
        showcase_page,
        "#operations-shell-frame",
        f"operations-shell-frame-{width}x{height}",
    )


async def test_operations_shell_search_updates_dense_workspace_boundary(
    showcase_page,
    showcase_base_url: str,
) -> None:
    await showcase_page.set_viewport_size({"width": 390, "height": 844})
    await showcase_page.goto(showcase_base_url + "/operations-shell")
    await wait_for_alpine(showcase_page)

    search = showcase_page.locator("#ops-shell-query")
    await expect(search).to_be_visible()
    await search.fill("queues")
    await search.dispatch_event("keyup")
    await wait_for_htmx(showcase_page)

    await expect(showcase_page.locator("#operations-shell-frame")).to_contain_text("Forge Runners")
    await expect(showcase_page.locator("#operations-shell-frame")).to_contain_text(
        "Queue depth above target"
    )
    await assert_no_document_horizontal_overflow(showcase_page, "operations-shell-search-queues")
    await _assert_locator_has_no_horizontal_overflow(
        showcase_page,
        "#operations-shell-frame",
        "operations-shell-search-frame",
    )


@pytest.mark.parametrize(
    ("width", "height"),
    [(320, 640), (390, 844), (768, 1024), (1280, 900), (1440, 1000)],
)
async def test_operations_workspace_shell_variant_has_no_overflow(
    showcase_page,
    showcase_base_url: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + "/operations-shell-workspace")
    await wait_for_alpine(showcase_page)

    await expect(showcase_page.locator("#operations-workspace-shell-surface")).to_be_visible()
    await expect(showcase_page.locator("#ops-workspace-shell-query")).to_be_visible()
    await expect(showcase_page.locator("#ops-workspace-shell-filter-form")).to_be_visible()
    await expect(showcase_page.locator("#operations-workspace-shell-frame")).to_be_visible()
    await expect(showcase_page.locator(".chirpui-workspace-shell")).to_be_visible()
    await expect(showcase_page.locator(".ops-shell-inspector")).to_contain_text("Inspector rail")
    await assert_no_document_horizontal_overflow(
        showcase_page, f"operations-workspace-shell-{width}x{height}"
    )
    await _assert_locator_has_no_horizontal_overflow(
        showcase_page,
        ".ops-shell-command-bar .chirpui-action-strip__inner",
        f"operations-workspace-shell-command-{width}x{height}",
    )
    await _assert_locator_has_no_horizontal_overflow(
        showcase_page,
        "#ops-workspace-shell-filter-form .chirpui-action-strip__inner",
        f"operations-workspace-shell-filter-{width}x{height}",
    )
    await _assert_locator_has_no_horizontal_overflow(
        showcase_page,
        "#operations-workspace-shell-frame",
        f"operations-workspace-shell-frame-{width}x{height}",
    )


async def test_operations_workspace_shell_search_updates_same_data_boundary(
    showcase_page,
    showcase_base_url: str,
) -> None:
    await showcase_page.set_viewport_size({"width": 390, "height": 844})
    await showcase_page.goto(showcase_base_url + "/operations-shell-workspace")
    await wait_for_alpine(showcase_page)

    search = showcase_page.locator("#ops-workspace-shell-query")
    await expect(search).to_be_visible()
    await search.fill("queues")
    await search.dispatch_event("keyup")
    await wait_for_htmx(showcase_page)

    await expect(showcase_page.locator("#operations-workspace-shell-frame")).to_contain_text(
        "Forge Runners"
    )
    await expect(showcase_page.locator("#operations-workspace-shell-frame")).to_contain_text(
        "Queue depth above target"
    )
    await assert_no_document_horizontal_overflow(
        showcase_page, "operations-workspace-shell-search-queues"
    )
    await _assert_locator_has_no_horizontal_overflow(
        showcase_page,
        "#operations-workspace-shell-frame",
        "operations-workspace-shell-search-frame",
    )


@pytest.mark.parametrize(
    ("width", "height"),
    [(320, 640), (390, 844), (768, 1024), (1280, 900), (1440, 1000)],
)
async def test_support_shell_second_domain_has_no_overflow(
    showcase_page,
    showcase_base_url: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + "/support-shell")
    await wait_for_alpine(showcase_page)

    await expect(showcase_page.locator("#support-shell-surface")).to_be_visible()
    await expect(showcase_page.locator("#support-shell-query")).to_be_visible()
    await expect(showcase_page.locator("#support-shell-filter-form")).to_be_visible()
    await expect(showcase_page.locator("#support-shell-frame")).to_be_visible()
    await expect(showcase_page.locator(".support-shell-inspector")).to_contain_text(
        "Inspector rail"
    )
    card_style = await showcase_page.locator(".chirpui-result-card").first.evaluate(
        """el => {
            const style = getComputedStyle(el);
            return {
                display: style.display,
                backgroundColor: style.backgroundColor,
                paddingTop: parseFloat(style.paddingTop),
            };
        }"""
    )
    assert card_style["display"] == "grid"
    assert card_style["backgroundColor"] != "rgba(0, 0, 0, 0)"
    assert card_style["paddingTop"] > 0
    await assert_no_document_horizontal_overflow(showcase_page, f"support-shell-{width}x{height}")
    await _assert_locator_has_no_horizontal_overflow(
        showcase_page,
        ".support-shell-command-bar .chirpui-action-strip__inner",
        f"support-shell-command-{width}x{height}",
    )
    await _assert_locator_has_no_horizontal_overflow(
        showcase_page,
        "#support-shell-filter-form .chirpui-action-strip__inner",
        f"support-shell-filter-{width}x{height}",
    )
    await _assert_locator_has_no_horizontal_overflow(
        showcase_page,
        "#support-shell-frame",
        f"support-shell-frame-{width}x{height}",
    )


async def test_support_shell_search_updates_dense_workspace_boundary(
    showcase_page,
    showcase_base_url: str,
) -> None:
    await showcase_page.set_viewport_size({"width": 390, "height": 844})
    await showcase_page.goto(showcase_base_url + "/support-shell")
    await wait_for_alpine(showcase_page)

    search = showcase_page.locator("#support-shell-query")
    await expect(search).to_be_visible()
    await search.fill("latency")
    await search.dispatch_event("keyup")
    await wait_for_htmx(showcase_page)

    await expect(showcase_page.locator("#support-shell-frame")).to_contain_text("VectorShop")
    await expect(showcase_page.locator("#support-shell-frame")).to_contain_text(
        "Latency alert fired"
    )
    await assert_no_document_horizontal_overflow(showcase_page, "support-shell-search-latency")
    await _assert_locator_has_no_horizontal_overflow(
        showcase_page,
        "#support-shell-frame",
        "support-shell-search-frame",
    )
