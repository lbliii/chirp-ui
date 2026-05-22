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
from tests.browser.gauntlet_detectors import (
    assert_direct_child_margins_trimmed,
    assert_direct_children_contained,
    assert_local_overflow_owner,
    assert_no_document_horizontal_overflow,
)

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
async def test_showcase_headers_own_title_action_relationships(
    showcase_page,
    showcase_base_url: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + "/layout")
    await wait_for_alpine(showcase_page)

    await expect(showcase_page.locator(".chirpui-page-header").first).to_be_visible()
    await expect(showcase_page.locator(".chirpui-entity-header").first).to_be_visible()
    await showcase_page.evaluate(
        """() => {
            const longTitle = "relationship-owner-title-" + "alpha".repeat(24);
            const longMeta = "release-note-" + "beta".repeat(18);
            const pageTitle = document.querySelector(".chirpui-page-header h1");
            const pageSubtitle = document.querySelector(".chirpui-page-header p");
            const pageActions = document.querySelector(".chirpui-page-header__actions");
            if (pageTitle) pageTitle.textContent = longTitle;
            if (pageSubtitle) pageSubtitle.textContent = longMeta;
            if (pageActions) {
                pageActions.innerHTML = `
                    <button class="chirpui-btn chirpui-btn--sm">Primary action</button>
                    <button class="chirpui-btn chirpui-btn--secondary chirpui-btn--sm">Secondary action</button>
                `;
            }

            const entity = document.querySelector(".chirpui-entity-header");
            const entityTitle = entity?.querySelector(".chirpui-entity-header__title");
            const entityMeta = entity?.querySelector(".chirpui-entity-header__meta");
            if (entityTitle) entityTitle.textContent = longTitle;
            if (entityMeta) entityMeta.textContent = longMeta;

            const host = document.querySelector(".chirpui-container");
            host?.insertAdjacentHTML("beforeend", `
                <div class="chirpui-section-header" data-testid="relationship-section-header">
                    <div class="chirpui-section-header__top">
                        <div class="chirpui-section-header__title-block">
                            <span class="chirpui-section-header__icon">*</span>
                            <div>
                                <h2>${longTitle}</h2>
                                <p class="chirpui-text-muted chirpui-font-sm">${longMeta}</p>
                            </div>
                        </div>
                        <div class="chirpui-section-header__actions">
                            <button class="chirpui-btn chirpui-btn--sm">Review</button>
                            <button class="chirpui-btn chirpui-btn--secondary chirpui-btn--sm">Export report</button>
                        </div>
                    </div>
                </div>
            `);
        }"""
    )

    await assert_no_document_horizontal_overflow(
        showcase_page, f"header-relationships-{width}x{height}"
    )
    metrics = await showcase_page.evaluate(
        """() => [
            [".chirpui-page-header", ".chirpui-page-header__actions"],
            ["[data-testid='relationship-section-header']", ".chirpui-section-header__actions"],
            [".chirpui-entity-header", ".chirpui-entity-header__actions"],
        ].map(([rootSelector, actionsSelector]) => {
            const root = document.querySelector(rootSelector);
            const title = root?.querySelector("h1, h2");
            const meta = root?.querySelector("p");
            const actions = root?.querySelector(actionsSelector);
            const rootRect = root.getBoundingClientRect();
            const titleRect = title.getBoundingClientRect();
            const actionsRect = actions.getBoundingClientRect();
            const titleStyle = getComputedStyle(title);
            const metaStyle = getComputedStyle(meta);
            return {
                rootSelector,
                overflow: Math.ceil(root.scrollWidth - root.clientWidth),
                titleMarginStart: titleStyle.marginBlockStart,
                titleMarginEnd: titleStyle.marginBlockEnd,
                metaMarginStart: metaStyle.marginBlockStart,
                metaMarginEnd: metaStyle.marginBlockEnd,
                titleContained: titleRect.right <= rootRect.right + 1,
                actionsContained: actionsRect.right <= rootRect.right + 1,
                actionsWidth: actionsRect.width,
                rootWidth: rootRect.width,
            };
        })"""
    )
    for metric in metrics:
        assert metric["overflow"] <= 1, metric
        assert metric["titleMarginStart"] == "0px", metric
        assert metric["titleMarginEnd"] == "0px", metric
        assert metric["metaMarginStart"] == "0px", metric
        assert metric["metaMarginEnd"] == "0px", metric
        assert metric["titleContained"], metric
        assert metric["actionsContained"], metric
        assert metric["actionsWidth"] <= metric["rootWidth"] + 1, metric


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
async def test_showcase_islands_own_fallback_and_mutation_region_rhythm(
    showcase_page,
    showcase_base_url: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + "/islands")
    await wait_for_alpine(showcase_page)

    await expect(
        showcase_page.locator("#counter-widget-root .chirpui-island-fallback")
    ).to_be_visible()
    await showcase_page.evaluate(
        """() => {
            const longText = "island-region-owner-" + "kappa".repeat(24);
            const fallback = document.querySelector("#counter-widget-root .chirpui-island-fallback");
            fallback?.querySelector("h3")?.replaceChildren(longText);
            fallback?.querySelector("p")?.replaceChildren(longText);
            document.querySelector("#relationship-island-proof")?.remove();
            document.querySelector("main")?.insertAdjacentHTML(
                "afterbegin",
                `<section id="relationship-island-proof" style="max-width: min(100%, 22rem);">
                    <div id="proof-fragment" class="chirpui-fragment-island" hx-disinherit="hx-select hx-target hx-swap">
                        <div id="proof-result" class="chirpui-fragment-island" aria-live="polite"></div>
                        <p>${longText}</p>
                        <p>${longText}</p>
                    </div>
                </section>`
            );
        }"""
    )

    await assert_no_document_horizontal_overflow(
        showcase_page, f"island-region-relationships-{width}x{height}"
    )
    await assert_direct_children_contained(
        showcase_page,
        "#counter-widget-root .chirpui-island-fallback",
        f"island-fallback-{width}x{height}",
    )
    await assert_direct_child_margins_trimmed(
        showcase_page,
        "#counter-widget-root .chirpui-island-fallback",
        f"island-fallback-{width}x{height}",
    )
    await assert_direct_children_contained(
        showcase_page,
        "#proof-fragment",
        f"island-fragment-{width}x{height}",
    )
    metrics = await showcase_page.evaluate(
        """() => {
            const fallback = document.querySelector("#counter-widget-root .chirpui-island-fallback");
            const fragment = document.querySelector("#proof-fragment");
            const emptyResult = document.querySelector("#proof-result");
            const paragraphs = [...fragment.querySelectorAll("p")];
            return {
                fallbackDisplay: getComputedStyle(fallback).display,
                fallbackGap: getComputedStyle(fallback).rowGap,
                fallbackOverflow: Math.ceil(fallback.scrollWidth - fallback.clientWidth),
                fragmentOverflow: Math.ceil(fragment.scrollWidth - fragment.clientWidth),
                emptyResultDisplay: getComputedStyle(emptyResult).display,
                secondParagraphMarginStart: getComputedStyle(paragraphs[1]).marginBlockStart,
            };
        }"""
    )
    assert metrics["fallbackDisplay"] == "grid", metrics
    assert metrics["fallbackGap"] != "normal", metrics
    assert metrics["fallbackOverflow"] <= 1, metrics
    assert metrics["fragmentOverflow"] <= 1, metrics
    assert metrics["emptyResultDisplay"] == "none", metrics
    assert metrics["secondParagraphMarginStart"] != "0px", metrics


@pytest.mark.parametrize(
    ("width", "height"),
    [(320, 640), (768, 1024), (1280, 900)],
)
async def test_showcase_form_control_internals_own_pressure(
    showcase_page,
    showcase_base_url: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + "/forms")
    await wait_for_alpine(showcase_page)

    await expect(showcase_page.locator("#field-price .chirpui-input-group")).to_be_visible()
    await expect(showcase_page.locator("#field-plan .chirpui-field__radio-group")).to_be_visible()
    await showcase_page.evaluate(
        """() => {
            const longText = "form-control-owner-" + "omega".repeat(24);
            const checkboxLabel = document.querySelector("#field-newsletter .chirpui-field__label--inline");
            checkboxLabel?.insertAdjacentHTML("beforeend", `<span>${longText}</span>`);
            document
                .querySelectorAll("#field-plan .chirpui-field__radio-label")
                .forEach((label) => { label.textContent = longText; });
            const rangeLabel = document.querySelector("#field-volume .chirpui-field__label");
            if (rangeLabel) rangeLabel.textContent = longText;
            const rangeValue = document.querySelector("#field-volume .chirpui-field__range-value");
            if (rangeValue) rangeValue.textContent = "100";
            const pricePrefix = document.querySelector("#field-price .chirpui-input-group__prefix");
            const priceSuffix = document.querySelector("#field-price .chirpui-input-group__suffix");
            if (pricePrefix) pricePrefix.textContent = longText;
            if (priceSuffix) priceSuffix.textContent = longText;
            const searchButton = document.querySelector("#field-q2 .chirpui-search-bar__btn .chirpui-btn__label");
            if (searchButton) searchButton.textContent = "Search form relationships";
        }"""
    )

    await assert_no_document_horizontal_overflow(
        showcase_page, f"form-control-internals-{width}x{height}"
    )
    metrics = await showcase_page.evaluate(
        """() => [
            ["#field-newsletter", ".chirpui-field__label--inline"],
            ["#field-plan", ".chirpui-field__radio-group"],
            ["#field-volume", ".chirpui-field__range-header"],
            ["#field-price", ".chirpui-input-group"],
            ["#field-q2", ".chirpui-search-bar__inner"],
        ].map(([rootSelector, childSelector]) => {
            const root = document.querySelector(rootSelector);
            const child = root?.querySelector(childSelector);
            const firstChild = root?.querySelector(":scope > :not(script, style, template)");
            const rootRect = root.getBoundingClientRect();
            const childRect = child.getBoundingClientRect();
            const firstChildStyle = getComputedStyle(firstChild);
            return {
                rootSelector,
                overflow: Math.ceil(root.scrollWidth - root.clientWidth),
                childContained: childRect.right <= rootRect.right + 1,
                childWidth: childRect.width,
                rootWidth: rootRect.width,
                firstChildMarginStart: firstChildStyle.marginBlockStart,
                firstChildMarginEnd: firstChildStyle.marginBlockEnd,
            };
        })"""
    )
    for metric in metrics:
        label = metric["rootSelector"]
        assert metric["overflow"] <= 1, {label: metric}
        assert metric["childContained"], {label: metric}
        assert metric["childWidth"] <= metric["rootWidth"] + 1, {label: metric}
        assert metric["firstChildMarginStart"] == "0px", {label: metric}
        assert metric["firstChildMarginEnd"] == "0px", {label: metric}


@pytest.mark.parametrize(
    ("width", "height"),
    [(320, 640), (768, 1024), (1280, 900)],
)
async def test_showcase_specialized_form_controls_own_pressure(
    showcase_page,
    showcase_base_url: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + "/forms")
    await wait_for_alpine(showcase_page)

    await showcase_page.evaluate(
        """() => {
            const longText = "specialized-control-owner-" + "sigma".repeat(24);
            const options = Array.from({ length: 8 }, (_, index) => {
                const id = `proof-star-${index}`;
                return `<input class="chirpui-star-rating__input" id="${id}" name="proof-star" type="radio">
                    <label class="chirpui-star-rating__label" for="${id}">&#9733;</label>`;
            }).join("");
            document.querySelector("#relationship-specialized-control-proof")?.remove();
            document.querySelector("main")?.insertAdjacentHTML(
                "afterbegin",
                `<section id="relationship-specialized-control-proof" style="max-width: min(100%, 20rem);">
                    <div class="chirpui-field">
                        <label class="chirpui-field__label" for="proof-file">${longText}</label>
                        <input id="proof-file" class="chirpui-field__file" type="file">
                    </div>
                    <fieldset id="proof-star" class="chirpui-star-rating" aria-label="Star pressure">
                        ${options}
                    </fieldset>
                    <fieldset id="proof-thumbs" class="chirpui-thumbs" aria-label="Thumb pressure">
                        <input class="chirpui-thumbs__input" id="proof-thumb-up" name="proof-thumb" type="radio">
                        <label class="chirpui-thumbs__label" for="proof-thumb-up">Up</label>
                        <input class="chirpui-thumbs__input" id="proof-thumb-down" name="proof-thumb" type="radio">
                        <label class="chirpui-thumbs__label" for="proof-thumb-down">Down</label>
                    </fieldset>
                    <div id="proof-form-segmented" class="chirpui-segmented" role="radiogroup">
                        <input id="proof-segment-1" class="chirpui-segmented__input" name="proof-segment" type="radio" checked>
                        <label class="chirpui-segmented__label" for="proof-segment-1">${longText}</label>
                        <input id="proof-segment-2" class="chirpui-segmented__input" name="proof-segment" type="radio">
                        <label class="chirpui-segmented__label" for="proof-segment-2">${longText}</label>
                    </div>
                    <div id="proof-number-scale" class="chirpui-number-scale">
                        ${Array.from({ length: 10 }, (_, index) => {
                            const value = index + 1;
                            return `<input class="chirpui-number-scale__input" id="proof-scale-${value}" name="proof-scale" type="radio">
                                <label class="chirpui-number-scale__label" for="proof-scale-${value}">${value}</label>`;
                        }).join("")}
                    </div>
                    <div id="proof-display-segmented" class="chirpui-segmented" role="radiogroup" aria-label="Display segmented pressure">
                        <label class="chirpui-segmented__option chirpui-segmented__option--active">
                            <input class="chirpui-visually-hidden" name="proof-display" type="radio" checked>
                            <span class="chirpui-segmented__label">${longText}</span>
                        </label>
                        <label class="chirpui-segmented__option">
                            <input class="chirpui-visually-hidden" name="proof-display" type="radio">
                            <span class="chirpui-segmented__label">${longText}</span>
                        </label>
                    </div>
                </section>`
            );
        }"""
    )

    await assert_no_document_horizontal_overflow(
        showcase_page, f"specialized-form-controls-{width}x{height}"
    )
    metrics = await showcase_page.evaluate(
        """() => {
            const proof = document.querySelector("#relationship-specialized-control-proof");
            const proofRect = proof.getBoundingClientRect();
            const entries = [
                ["#proof-file", null],
                ["#proof-star", ".chirpui-star-rating__label"],
                ["#proof-thumbs", ".chirpui-thumbs__label"],
                ["#proof-form-segmented", ".chirpui-segmented__label"],
                ["#proof-number-scale", ".chirpui-number-scale__label"],
                ["#proof-display-segmented", ".chirpui-segmented__option"],
            ];
            return entries.map(([selector, childSelector]) => {
                const root = document.querySelector(selector);
                const child = childSelector ? root.querySelector(childSelector) : root;
                const rootRect = root.getBoundingClientRect();
                const childRect = child.getBoundingClientRect();
                const rootStyle = getComputedStyle(root);
                const childStyle = getComputedStyle(child);
                return {
                    selector,
                    overflow: Math.ceil(root.scrollWidth - root.clientWidth),
                    rootContained: rootRect.right <= proofRect.right + 1,
                    childContained: childRect.right <= rootRect.right + 1,
                    flexWrap: rootStyle.flexWrap,
                    maxInlineSize: rootStyle.maxInlineSize,
                    childWhiteSpace: childStyle.whiteSpace,
                    childOverflowWrap: childStyle.overflowWrap,
                };
            });
        }"""
    )
    for metric in metrics:
        assert metric["overflow"] <= 1, {metric["selector"]: metric}
        assert metric["rootContained"], {metric["selector"]: metric}
        assert metric["childContained"], {metric["selector"]: metric}
        if metric["selector"] != "#proof-file":
            assert metric["flexWrap"] == "wrap", {metric["selector"]: metric}
        assert metric["maxInlineSize"] == "100%", {metric["selector"]: metric}
        if metric["selector"] == "#proof-display-segmented":
            assert metric["childWhiteSpace"] == "normal", metric
            assert metric["childOverflowWrap"] == "anywhere", metric


@pytest.mark.parametrize(
    ("width", "height"),
    [(320, 640), (768, 1024), (1280, 900)],
)
async def test_showcase_list_and_media_rows_own_relationship_pressure(
    showcase_page,
    showcase_base_url: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + "/layout")
    await wait_for_alpine(showcase_page)

    await showcase_page.evaluate(
        """() => {
            const longText = "row-relationship-owner-" + "theta".repeat(24);
            document.querySelector("#relationship-row-proof")?.remove();
            document.querySelector("main")?.insertAdjacentHTML(
                "afterbegin",
                `<section id="relationship-row-proof" style="max-width: min(100%, 28rem);">
                    <ul class="chirpui-list chirpui-list--bordered" aria-label="Row relationship proof">
                        <li class="chirpui-list__item"><p>${longText}</p></li>
                        <li class="chirpui-list__item"><p>${longText}</p></li>
                    </ul>
                    <div class="chirpui-media-object" style="margin-top: 1rem;">
                        <div class="chirpui-media-object__media">
                            <div style="inline-size: 3rem; block-size: 3rem; background: var(--chirpui-accent); border-radius: var(--chirpui-radius);"></div>
                        </div>
                        <div class="chirpui-media-object__body">
                            <strong>${longText}</strong>
                            <p>${longText}</p>
                        </div>
                        <div class="chirpui-media-object__actions">
                            <button class="chirpui-btn chirpui-btn--sm" type="button"><span class="chirpui-btn__label">${longText}</span></button>
                        </div>
                    </div>
                </section>`
            );
        }"""
    )

    await assert_no_document_horizontal_overflow(
        showcase_page, f"list-media-row-relationships-{width}x{height}"
    )
    metrics = await showcase_page.evaluate(
        """() => {
            const proof = document.querySelector("#relationship-row-proof");
            const list = proof.querySelector(".chirpui-list");
            const listItems = [...proof.querySelectorAll(".chirpui-list__item")];
            const mediaObject = proof.querySelector(".chirpui-media-object");
            const mediaBody = proof.querySelector(".chirpui-media-object__body");
            const mediaActions = proof.querySelector(".chirpui-media-object__actions");
            const mediaParagraph = mediaBody.querySelector("p");
            const listParagraph = listItems[0].querySelector("p");
            const containers = [list, ...listItems, mediaObject, mediaBody, mediaActions];
            return {
                containers: containers.map((el) => ({
                    className: el.className,
                    overflow: Math.ceil(el.scrollWidth - el.clientWidth),
                    width: el.getBoundingClientRect().width,
                })),
                listGap: getComputedStyle(list).rowGap,
                secondItemMarginTop: getComputedStyle(listItems[1]).marginTop,
                listParagraphMarginStart: getComputedStyle(listParagraph).marginBlockStart,
                listParagraphMarginEnd: getComputedStyle(listParagraph).marginBlockEnd,
                mediaParagraphMarginStart: getComputedStyle(mediaParagraph).marginBlockStart,
                mediaParagraphMarginEnd: getComputedStyle(mediaParagraph).marginBlockEnd,
                mediaBodyDisplay: getComputedStyle(mediaBody).display,
                mediaActionsDisplay: getComputedStyle(mediaActions).display,
                mediaActionsWidth: mediaActions.getBoundingClientRect().width,
                mediaObjectWidth: mediaObject.getBoundingClientRect().width,
            };
        }"""
    )
    for metric in metrics["containers"]:
        assert metric["overflow"] <= 1, {metric["className"]: metric}
    assert metrics["listGap"] != "normal", metrics
    assert metrics["secondItemMarginTop"] == "0px", metrics
    assert metrics["listParagraphMarginStart"] == "0px", metrics
    assert metrics["listParagraphMarginEnd"] == "0px", metrics
    assert metrics["mediaParagraphMarginStart"] == "0px", metrics
    assert metrics["mediaParagraphMarginEnd"] == "0px", metrics
    assert metrics["mediaBodyDisplay"] == "grid", metrics
    assert metrics["mediaActionsDisplay"] == "flex", metrics
    assert metrics["mediaActionsWidth"] <= metrics["mediaObjectWidth"] + 1, metrics


@pytest.mark.parametrize(
    ("width", "height"),
    [(320, 640), (768, 1024), (1280, 900)],
)
async def test_showcase_code_docs_rows_own_local_overflow(
    showcase_page,
    showcase_base_url: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + "/forms")
    await wait_for_alpine(showcase_page)

    await showcase_page.evaluate(
        """() => {
            const longToken = "code-doc-owner-" + "lambda".repeat(28);
            document.querySelector("#relationship-code-doc-proof")?.remove();
            document.querySelector("main")?.insertAdjacentHTML(
                "afterbegin",
                `<section id="relationship-code-doc-proof" style="max-width: min(100%, 24rem);">
                    <div class="chirpui-params-table">
                        <h3 class="chirpui-params-table__title">${longToken}</h3>
                        <div class="chirpui-params-table__wrap">
                            <table class="chirpui-params-table__table">
                                <thead class="chirpui-params-table__head">
                                    <tr>
                                        <th class="chirpui-params-table__th chirpui-params-table__th--name">Name</th>
                                        <th class="chirpui-params-table__th chirpui-params-table__th--type">Type</th>
                                        <th class="chirpui-params-table__th chirpui-params-table__th--default">Default</th>
                                        <th class="chirpui-params-table__th chirpui-params-table__th--description">Description</th>
                                    </tr>
                                </thead>
                                <tbody class="chirpui-params-table__body">
                                    <tr class="chirpui-params-table__row">
                                        <td class="chirpui-params-table__td chirpui-params-table__td--name"><code class="chirpui-params-table__code">${longToken}</code></td>
                                        <td class="chirpui-params-table__td chirpui-params-table__td--type"><code class="chirpui-params-table__code">${longToken}</code></td>
                                        <td class="chirpui-params-table__td chirpui-params-table__td--default"><code class="chirpui-params-table__code chirpui-params-table__code--muted">${longToken}</code></td>
                                        <td class="chirpui-params-table__td chirpui-params-table__td--description">${longToken}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <pre class="chirpui-signature" data-language="python"><code class="chirpui-signature__code">async def ${longToken}(very_long_argument_name: str = "${longToken}") -> ${longToken}:</code></pre>
                </section>`
            );
        }"""
    )

    await assert_no_document_horizontal_overflow(
        showcase_page, f"code-doc-relationships-{width}x{height}"
    )
    await assert_direct_child_margins_trimmed(
        showcase_page,
        "#relationship-code-doc-proof .chirpui-params-table",
        f"code-doc-params-table-{width}x{height}",
    )
    await assert_local_overflow_owner(
        showcase_page,
        "#relationship-code-doc-proof .chirpui-params-table__wrap",
        f"code-doc-params-wrap-{width}x{height}",
    )
    await assert_local_overflow_owner(
        showcase_page,
        "#relationship-code-doc-proof .chirpui-signature",
        f"code-doc-signature-{width}x{height}",
    )
    metrics = await showcase_page.evaluate(
        """() => {
            const proof = document.querySelector("#relationship-code-doc-proof");
            const params = proof.querySelector(".chirpui-params-table");
            const title = proof.querySelector(".chirpui-params-table__title");
            const wrap = proof.querySelector(".chirpui-params-table__wrap");
            const signature = proof.querySelector(".chirpui-signature");
            const code = proof.querySelector(".chirpui-signature__code");
            const firstParamsChild = params.querySelector(":scope > :not(script, style, template)");
            const titleStyle = getComputedStyle(title);
            const firstParamsStyle = getComputedStyle(firstParamsChild);
            const wrapStyle = getComputedStyle(wrap);
            const signatureStyle = getComputedStyle(signature);
            const codeStyle = getComputedStyle(code);
            const proofRect = proof.getBoundingClientRect();
            const paramsRect = params.getBoundingClientRect();
            const wrapRect = wrap.getBoundingClientRect();
            const signatureRect = signature.getBoundingClientRect();
            return {
                proofOverflow: Math.ceil(proof.scrollWidth - proof.clientWidth),
                paramsOverflow: Math.ceil(params.scrollWidth - params.clientWidth),
                wrapLocalOverflow: Math.ceil(wrap.scrollWidth - wrap.clientWidth),
                signatureLocalOverflow: Math.ceil(signature.scrollWidth - signature.clientWidth),
                wrapOverflowX: wrapStyle.overflowX,
                signatureOverflowX: signatureStyle.overflowX,
                codeWhiteSpace: codeStyle.whiteSpace,
                titleMarginStart: titleStyle.marginBlockStart,
                titleMarginEnd: titleStyle.marginBlockEnd,
                firstParamsMarginStart: firstParamsStyle.marginBlockStart,
                firstParamsMarginEnd: firstParamsStyle.marginBlockEnd,
                paramsContained: paramsRect.right <= proofRect.right + 1,
                wrapContained: wrapRect.right <= proofRect.right + 1,
                signatureContained: signatureRect.right <= proofRect.right + 1,
            };
        }"""
    )
    assert metrics["proofOverflow"] <= 1, metrics
    assert metrics["paramsOverflow"] <= 1, metrics
    assert metrics["wrapLocalOverflow"] > 1, metrics
    assert metrics["signatureLocalOverflow"] > 1, metrics
    assert metrics["wrapOverflowX"] == "auto", metrics
    assert metrics["signatureOverflowX"] == "auto", metrics
    assert metrics["codeWhiteSpace"] == "pre", metrics
    assert metrics["titleMarginStart"] == "0px", metrics
    assert metrics["titleMarginEnd"] == "0px", metrics
    assert metrics["firstParamsMarginStart"] == "0px", metrics
    assert metrics["firstParamsMarginEnd"] == "0px", metrics
    assert metrics["paramsContained"], metrics
    assert metrics["wrapContained"], metrics
    assert metrics["signatureContained"], metrics


@pytest.mark.parametrize(
    ("width", "height"),
    [(320, 640), (768, 1024), (1280, 900)],
)
async def test_showcase_drag_rows_own_pressure_and_board_overflow(
    showcase_page,
    showcase_base_url: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + "/forms")
    await wait_for_alpine(showcase_page)

    await showcase_page.evaluate(
        """() => {
            const longText = "drag-row-owner-" + "sigma".repeat(28);
            document.querySelector("#relationship-drag-proof")?.remove();
            document.querySelector("main")?.insertAdjacentHTML(
                "afterbegin",
                `<section id="relationship-drag-proof" style="max-width: min(100%, 24rem);">
                    <div class="chirpui-sortable" role="listbox">
                        <div class="chirpui-sortable__item" role="option">
                            <span class="chirpui-sortable__handle">☰</span>
                            <span class="chirpui-sortable__content"><p>${longText}</p></span>
                            <button class="chirpui-sortable__remove" type="button">x</button>
                        </div>
                    </div>
                    <div class="chirpui-dnd chirpui-dnd--row" role="listbox">
                        <div class="chirpui-dnd__item chirpui-dnd__item--row" role="option">
                            <span class="chirpui-dnd__handle">☰</span>
                            <span class="chirpui-dnd__drop-indicator"></span>
                            <p>${longText}</p>
                        </div>
                    </div>
                    <div class="chirpui-dnd chirpui-dnd--board" role="group" aria-label="Board proof">
                        ${["Planning", "Doing", "Done"].map((title) => `
                            <div class="chirpui-dnd__column" role="group">
                                <div class="chirpui-dnd__column-header">${title}-${longText}</div>
                                <div class="chirpui-dnd__column-body">
                                    <div class="chirpui-dnd__card" role="article"><p>${longText}</p></div>
                                </div>
                            </div>
                        `).join("")}
                    </div>
                </section>`
            );
        }"""
    )

    await assert_no_document_horizontal_overflow(
        showcase_page, f"drag-row-relationships-{width}x{height}"
    )
    metrics = await showcase_page.evaluate(
        """() => {
            const proof = document.querySelector("#relationship-drag-proof");
            const sortable = proof.querySelector(".chirpui-sortable");
            const sortableItem = proof.querySelector(".chirpui-sortable__item");
            const sortableContent = proof.querySelector(".chirpui-sortable__content");
            const sortableParagraph = sortableContent.querySelector("p");
            const dndRow = proof.querySelector(".chirpui-dnd--row");
            const dndItem = proof.querySelector(".chirpui-dnd__item");
            const dndParagraph = dndItem.querySelector("p");
            const board = proof.querySelector(".chirpui-dnd--board");
            const column = proof.querySelector(".chirpui-dnd__column");
            const columnHeader = proof.querySelector(".chirpui-dnd__column-header");
            const card = proof.querySelector(".chirpui-dnd__card");
            const cardParagraph = card.querySelector("p");
            const containers = [proof, sortable, sortableItem, sortableContent, dndRow, dndItem, column, card];
            return {
                containers: containers.map((el) => ({
                    className: el.className || el.id,
                    overflow: Math.ceil(el.scrollWidth - el.clientWidth),
                })),
                boardLocalOverflow: Math.ceil(board.scrollWidth - board.clientWidth),
                boardOverflowX: getComputedStyle(board).overflowX,
                sortableItemWrap: getComputedStyle(sortableItem).flexWrap,
                dndItemWrap: getComputedStyle(dndItem).flexWrap,
                sortableParagraphMargins: [
                    getComputedStyle(sortableParagraph).marginBlockStart,
                    getComputedStyle(sortableParagraph).marginBlockEnd,
                ],
                dndParagraphMargins: [
                    getComputedStyle(dndParagraph).marginBlockStart,
                    getComputedStyle(dndParagraph).marginBlockEnd,
                ],
                columnHeaderWrap: getComputedStyle(columnHeader).overflowWrap,
                cardParagraphMargins: [
                    getComputedStyle(cardParagraph).marginBlockStart,
                    getComputedStyle(cardParagraph).marginBlockEnd,
                ],
            };
        }"""
    )
    for metric in metrics["containers"]:
        assert metric["overflow"] <= 1, {metric["className"]: metric}
    assert metrics["boardLocalOverflow"] > 1, metrics
    assert metrics["boardOverflowX"] == "auto", metrics
    assert metrics["sortableItemWrap"] == "wrap", metrics
    assert metrics["dndItemWrap"] == "wrap", metrics
    assert metrics["sortableParagraphMargins"] == ["0px", "0px"], metrics
    assert metrics["dndParagraphMargins"] == ["0px", "0px"], metrics
    assert metrics["cardParagraphMargins"] == ["0px", "0px"], metrics
    assert metrics["columnHeaderWrap"] == "anywhere", metrics


@pytest.mark.parametrize(
    ("width", "height"),
    [(320, 640), (768, 1024), (1280, 900)],
)
async def test_showcase_table_rows_own_action_and_metadata_pressure(
    showcase_page,
    showcase_base_url: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + "/forms")
    await wait_for_alpine(showcase_page)

    await showcase_page.evaluate(
        """() => {
            const longText = "table-row-owner-" + "delta".repeat(24);
            document.querySelector("#relationship-table-proof")?.remove();
            document.querySelector("main")?.insertAdjacentHTML(
                "afterbegin",
                `<section id="relationship-table-proof" style="max-width: min(100%, 24rem);">
                    <div class="chirpui-table-wrap">
                        <table class="chirpui-table chirpui-table--compact">
                            <thead class="chirpui-table__head">
                                <tr class="chirpui-table__row">
                                    <th class="chirpui-table__th">Name</th>
                                    <th class="chirpui-table__th chirpui-table__th--actions">Actions</th>
                                </tr>
                            </thead>
                            <tbody class="chirpui-table__body">
                                <tr class="chirpui-table__row">
                                    <td class="chirpui-table__td">
                                        <p><a href="#">${longText}</a></p>
                                        <p>${longText}</p>
                                    </td>
                                    <td class="chirpui-table__td chirpui-table__td--actions">
                                        <button class="chirpui-btn chirpui-btn--sm">Open</button>
                                        <button class="chirpui-btn chirpui-btn--ghost chirpui-btn--sm chirpui-row-actions__trigger">...</button>
                                    </td>
                                </tr>
                                <tr class="chirpui-table__row">
                                    <td class="chirpui-table__td"><code>${longText}</code></td>
                                    <td class="chirpui-table__td">
                                        <button class="chirpui-btn chirpui-btn--ghost chirpui-btn--sm chirpui-row-actions__trigger">...</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </section>`
            );
        }"""
    )

    await assert_no_document_horizontal_overflow(
        showcase_page, f"table-row-relationships-{width}x{height}"
    )
    await assert_local_overflow_owner(
        showcase_page,
        "#relationship-table-proof .chirpui-table-wrap",
        f"table-row-wrap-{width}x{height}",
    )
    metrics = await showcase_page.evaluate(
        """() => {
            const proof = document.querySelector("#relationship-table-proof");
            const wrap = proof.querySelector(".chirpui-table-wrap");
            const firstCell = proof.querySelector(".chirpui-table__td");
            const paragraphs = [...firstCell.querySelectorAll("p")];
            const actionCell = proof.querySelector(".chirpui-table__td--actions");
            const inferredActionCell = proof.querySelector("tbody tr:nth-child(2) td:nth-child(2)");
            const actionButton = actionCell.querySelector(".chirpui-btn");
            const rowTrigger = inferredActionCell.querySelector(".chirpui-row-actions__trigger");
            const actionButtonRect = actionButton.getBoundingClientRect();
            const rowTriggerRect = rowTrigger.getBoundingClientRect();
            const proofRect = proof.getBoundingClientRect();
            const wrapRect = wrap.getBoundingClientRect();
            const actionRect = actionCell.getBoundingClientRect();
            const inferredRect = inferredActionCell.getBoundingClientRect();
            return {
                proofOverflow: Math.ceil(proof.scrollWidth - proof.clientWidth),
                wrapOverflow: Math.ceil(wrap.scrollWidth - wrap.clientWidth),
                wrapOverflowX: getComputedStyle(wrap).overflowX,
                wrapContained: wrapRect.right <= proofRect.right + 1,
                actionButtonContained: actionButtonRect.right <= actionRect.right + 1,
                rowTriggerContained: rowTriggerRect.right <= inferredRect.right + 1,
                paragraphMargins: paragraphs.map((node) => [
                    getComputedStyle(node).marginBlockStart,
                    getComputedStyle(node).marginBlockEnd,
                ]),
                secondParagraphMarginStart: getComputedStyle(paragraphs[1]).marginBlockStart,
                actionAlign: getComputedStyle(actionCell).textAlign,
                inferredActionAlign: getComputedStyle(inferredActionCell).textAlign,
                actionButtonDisplay: getComputedStyle(actionButton).display,
                rowTriggerDisplay: getComputedStyle(rowTrigger).display,
                rowTriggerMinInline: getComputedStyle(rowTrigger).minInlineSize,
                rowTriggerMinBlock: getComputedStyle(rowTrigger).minBlockSize,
            };
        }"""
    )
    assert metrics["proofOverflow"] <= 1, metrics
    assert metrics["wrapOverflow"] >= 0, metrics
    assert metrics["wrapOverflowX"] == "auto", metrics
    assert metrics["wrapContained"], metrics
    assert metrics["actionButtonContained"], metrics
    assert metrics["rowTriggerContained"], metrics
    assert metrics["paragraphMargins"][0] == ["0px", "0px"], metrics
    assert metrics["paragraphMargins"][1][1] == "0px", metrics
    assert metrics["secondParagraphMarginStart"] != "0px", metrics
    assert metrics["actionAlign"] == "right", metrics
    assert metrics["inferredActionAlign"] == "right", metrics
    assert metrics["actionButtonDisplay"] == "inline-flex", metrics
    assert metrics["rowTriggerDisplay"] == "inline-flex", metrics
    assert metrics["rowTriggerMinInline"] != "0px", metrics
    assert metrics["rowTriggerMinBlock"] != "0px", metrics


@pytest.mark.parametrize(
    ("width", "height"),
    [(320, 640), (768, 1024), (1280, 900)],
)
async def test_showcase_search_browse_composites_own_rhythm(
    showcase_page,
    showcase_base_url: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + "/forms")
    await wait_for_alpine(showcase_page)

    await expect(showcase_page.locator(".chirpui-search-header").first).to_be_visible()
    await expect(showcase_page.locator(".chirpui-resource-index").first).to_be_visible()
    await showcase_page.evaluate(
        """() => {
            const longText = "search-browse-owner-" + "gamma".repeat(24);
            const searchHeader = document.querySelector(".chirpui-search-header");
            const title = searchHeader?.querySelector(".chirpui-page-header h1");
            const subtitle = searchHeader?.querySelector(".chirpui-page-header p");
            const input = searchHeader?.querySelector(".chirpui-search-bar__input");
            const controls = searchHeader?.querySelector(".chirpui-action-strip__controls");
            if (title) title.textContent = longText;
            if (subtitle) subtitle.textContent = longText;
            if (input) input.setAttribute("placeholder", longText);
            if (controls) {
                controls.innerHTML = `
                    <button class="chirpui-btn chirpui-btn--sm">Sort by relationship</button>
                    <button class="chirpui-btn chirpui-btn--secondary chirpui-btn--sm">Switch view</button>
                    <button class="chirpui-btn chirpui-btn--primary chirpui-btn--sm">Create searchable record</button>
                `;
            }

            const resourceIndex = document.querySelector(".chirpui-resource-index");
            const results = resourceIndex?.querySelector(".chirpui-resource-index__results");
            if (results && !results.querySelector(".chirpui-fragment-island")) {
                results.insertAdjacentHTML(
                    "afterbegin",
                    `<div class="chirpui-fragment-island" aria-live="polite">${longText}</div>`
                );
            }
        }"""
    )

    await assert_no_document_horizontal_overflow(
        showcase_page, f"search-browse-composites-{width}x{height}"
    )
    metrics = await showcase_page.evaluate(
        """() => [
            [".chirpui-search-header", ".chirpui-search-header__strip"],
            [".chirpui-resource-index", ".chirpui-resource-index__results"],
        ].map(([rootSelector, childSelector]) => {
            const root = document.querySelector(rootSelector);
            const child = root?.querySelector(childSelector);
            const rootRect = root.getBoundingClientRect();
            const childRect = child.getBoundingClientRect();
            const firstChild = root?.querySelector(":scope > :not(script, style, template)");
            const firstChildStyle = getComputedStyle(firstChild);
            return {
                rootSelector,
                overflow: Math.ceil(root.scrollWidth - root.clientWidth),
                childContained: childRect.right <= rootRect.right + 1,
                childWidth: childRect.width,
                rootWidth: rootRect.width,
                firstChildMarginStart: firstChildStyle.marginBlockStart,
                firstChildMarginEnd: firstChildStyle.marginBlockEnd,
            };
        })"""
    )
    for metric in metrics:
        assert metric["overflow"] <= 1, metric
        assert metric["childContained"], metric
        assert metric["childWidth"] <= metric["rootWidth"] + 1, metric
        assert metric["firstChildMarginStart"] == "0px", metric
        assert metric["firstChildMarginEnd"] == "0px", metric


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


@pytest.mark.parametrize(
    ("width", "height"),
    [(320, 640), (768, 1024), (1280, 900)],
)
async def test_support_shell_result_cards_own_relationship_pressure(
    showcase_page,
    showcase_base_url: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + "/support-shell?queue=product")
    await wait_for_alpine(showcase_page)

    await expect(showcase_page.locator(".chirpui-result-card").first).to_be_visible()
    await showcase_page.evaluate(
        """() => {
            const longText = "support-result-owner-" + "kappa".repeat(24);
            const card = document.querySelector(".chirpui-result-card");
            card.querySelector(".chirpui-result-card__title").textContent = longText;
            card.querySelector(".chirpui-result-card__subtitle").textContent = longText;
            card.querySelector(".chirpui-result-card__actions").innerHTML =
                `<span class="chirpui-badge chirpui-badge--error">${longText}</span>`;
            card.querySelector(".chirpui-result-card__body").insertAdjacentHTML(
                "afterbegin",
                `<p>${longText}</p>`
            );
            card.querySelector(".chirpui-result-card__footer").insertAdjacentHTML(
                "afterbegin",
                `<span>${longText}</span>`
            );
            const inspector = document.querySelector(".chirpui-inspector-panel");
            inspector.querySelector(".chirpui-inspector-panel__subtitle").textContent = longText;
            inspector.querySelector(".chirpui-inspector-panel__body").insertAdjacentHTML(
                "afterbegin",
                `<p>${longText}</p>`
            );
            inspector.querySelector(".chirpui-inspector-panel__footer").insertAdjacentHTML(
                "afterbegin",
                `<span>${longText}</span>`
            );
        }"""
    )

    await assert_no_document_horizontal_overflow(
        showcase_page, f"support-result-card-relationships-{width}x{height}"
    )
    metrics = await showcase_page.evaluate(
        """() => [
            ".chirpui-result-card",
            ".chirpui-result-card__header",
            ".chirpui-result-card__copy",
            ".chirpui-result-card__actions",
            ".chirpui-result-card__body",
            ".chirpui-result-card__footer",
            ".chirpui-inspector-panel",
            ".chirpui-inspector-panel__body",
            ".chirpui-inspector-panel__footer",
        ].map((selector) => {
            const el = document.querySelector(selector);
            const firstChild = el.querySelector(":scope > :not(script, style, template)");
            const style = firstChild ? getComputedStyle(firstChild) : null;
            return {
                selector,
                overflow: Math.ceil(el.scrollWidth - el.clientWidth),
                marginStart: style?.marginBlockStart ?? null,
                marginEnd: style?.marginBlockEnd ?? null,
                width: el.getBoundingClientRect().width,
            };
        })"""
    )
    for metric in metrics:
        assert metric["overflow"] <= 1, {metric["selector"]: metric}
        if metric["marginStart"] is not None:
            assert metric["marginStart"] == "0px", {metric["selector"]: metric}
            assert metric["marginEnd"] == "0px", {metric["selector"]: metric}


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
