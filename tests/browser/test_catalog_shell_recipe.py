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
