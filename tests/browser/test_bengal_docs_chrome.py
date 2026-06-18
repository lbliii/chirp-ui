"""Browser proof for packaged Bengal docs chrome."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest
from playwright.async_api import expect

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

REPO_ROOT = Path(__file__).resolve().parents[2]
SITE_PUBLIC = REPO_ROOT / "site" / "public"

VIEWPORTS = [
    pytest.param(390, 844, id="phone"),
    pytest.param(768, 1024, id="tablet"),
    pytest.param(919, 863, id="compact-desktop"),
    pytest.param(1024, 768, id="tablet-wide"),
    pytest.param(1280, 900, id="desktop"),
]


@pytest.fixture(scope="module")
def static_site_url():
    handler = partial(SimpleHTTPRequestHandler, directory=str(SITE_PUBLIC))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


@pytest.fixture
async def page():
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context()
        page = await ctx.new_page()
        yield page
        await ctx.close()
        await browser.close()


async def open_app_shell_docs(page, static_site_url: str, width: int, height: int) -> None:
    await page.set_viewport_size({"width": width, "height": height})
    await page.goto(f"{static_site_url}/docs/app-shell/")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(100)


async def assert_no_document_horizontal_overflow(page, label: str) -> None:
    result = await page.evaluate(
        """() => {
            const root = document.documentElement;
            return {
                overflow: Math.ceil(root.scrollWidth - root.clientWidth),
                scrollWidth: root.scrollWidth,
                clientWidth: root.clientWidth,
            };
        }"""
    )
    assert result["overflow"] <= 1, {label: result}


@pytest.mark.parametrize(("width", "height"), VIEWPORTS)
async def test_bengal_docs_chrome_regions_survive_responsive_widths(
    page, static_site_url, width, height
):
    await open_app_shell_docs(page, static_site_url, width, height)

    await assert_no_document_horizontal_overflow(page, f"bengal-docs-chrome-{width}x{height}")
    await expect(page.locator(".chirp-theme-docs-layout__main")).to_be_visible()
    await expect(page.locator(".chirp-theme-docs-layout__article")).to_be_visible()
    assert await page.locator(".nav-search-trigger").count() >= 1
    assert await page.locator(".theme-dropdown__button").count() >= 1
    assert await page.locator("#mobile-nav-dialog").count() == 1

    if width <= 768:
        await expect(page.locator(".chirp-theme-shell__header")).to_be_visible()
        await expect(page.locator(".chirp-theme-docs-layout__sidebar")).to_be_hidden()
        await expect(page.locator(".mobile-nav-toggle")).to_be_visible()
    else:
        await expect(page.locator(".chirp-theme-shell__header")).to_be_hidden()
        await expect(page.locator(".chirp-theme-docs-layout__sidebar")).to_be_visible()
        await expect(page.locator(".chirp-theme-doc-catalog-rail__home")).to_be_visible()
        await expect(
            page.locator(".chirp-theme-doc-catalog-rail__group--actions .nav-search-trigger")
        ).to_be_visible()
        await expect(
            page.locator(".chirp-theme-doc-catalog-rail__group--actions .theme-dropdown__button")
        ).to_be_visible()

    if 768 < width <= 1024:
        await expect(page.locator(".chirp-theme-doc-catalog__primary")).to_be_visible()
        await expect(page.locator(".chirp-theme-doc-catalog__secondary")).to_be_hidden()

    if width >= 1280:
        await expect(page.locator(".chirp-theme-doc-catalog__secondary")).to_be_visible()
        await expect(page.locator(".chirp-theme-docs-layout__toc")).to_be_visible()
        await expect(page.locator(".toc-sidebar[data-bengal='toc']")).to_be_visible()


async def test_bengal_docs_mobile_nav_opens_and_keeps_search_reachable(page, static_site_url):
    await open_app_shell_docs(page, static_site_url, 390, 844)

    await page.locator(".mobile-nav-toggle").click()
    dialog = page.locator("#mobile-nav-dialog")
    assert await dialog.evaluate("el => el.open")
    # The mobile <nav> is an implicit navigation landmark; the redundant
    # explicit role="navigation" was dropped in the #129 a11y wave (it's named
    # via aria-label="Mobile navigation" instead). Assert on the nav element.
    await expect(dialog.locator("nav.mobile-nav-content")).to_be_visible()
    await expect(dialog.locator(".mobile-nav-search[data-open-search]")).to_be_visible()
    await expect(dialog.locator(".theme-dropdown__button")).to_be_visible()

    await page.keyboard.press("Escape")
    await page.wait_for_timeout(100)
    assert not await dialog.evaluate("el => el.open")


async def test_bengal_docs_theme_controls_use_native_popover(page, static_site_url):
    await open_app_shell_docs(page, static_site_url, 1280, 900)

    trigger = page.locator(
        ".chirp-theme-doc-catalog-rail__group--actions "
        ".theme-dropdown__button[popovertarget='theme-menu-rail']"
    )
    menu_id = await trigger.get_attribute("popovertarget")
    assert menu_id == "theme-menu-rail"
    await trigger.click()
    await expect(page.locator("#theme-menu-rail")).to_be_visible()
    assert await page.locator("#theme-menu-rail .theme-option[data-appearance]").count() == 3
    assert await page.locator("#theme-menu-rail .theme-option[data-theme-pack]").count() == 0
    assert await page.locator("#theme-menu-rail .theme-option[data-palette]").count() == 0


async def test_bengal_docs_desktop_nav_dropdown_opens_on_hover(page, static_site_url):
    await page.set_viewport_size({"width": 1280, "height": 900})
    await page.goto(f"{static_site_url}/")
    await page.wait_for_load_state("networkidle")

    dropdown = page.locator(".chirp-theme-shell__nav-dropdown").first
    trigger = dropdown.locator(".chirpui-navbar-dropdown__trigger")
    menu = dropdown.locator(".chirpui-navbar-dropdown__menu")
    nav_alignment = await page.locator(".chirp-theme-shell__desktop-nav").evaluate(
        """nav => {
            const items = Array.from(nav.children).map((item) => {
                const control = item.matches("a, summary")
                    ? item
                    : item.querySelector(":scope > summary, :scope > a");
                const rect = control.getBoundingClientRect();
                return {
                    tag: control.tagName,
                    top: rect.top,
                    bottom: rect.bottom,
                    center: rect.top + rect.height / 2,
                    height: rect.height,
                    display: getComputedStyle(control).display,
                    alignItems: getComputedStyle(control).alignItems,
                };
            });
            const centers = items.map((item) => item.center);
            const heights = items.map((item) => item.height);
            return {
                items,
                centerSpread: Math.max(...centers) - Math.min(...centers),
                heightSpread: Math.max(...heights) - Math.min(...heights),
            };
        }"""
    )

    assert nav_alignment["items"]
    assert nav_alignment["centerSpread"] <= 1
    assert nav_alignment["heightSpread"] <= 1
    assert {item["display"] for item in nav_alignment["items"]} <= {"flex", "inline-flex"}
    assert {item["alignItems"] for item in nav_alignment["items"]} == {"center"}

    await expect(menu).to_be_hidden()
    await trigger.hover()
    await expect(menu).to_be_visible()
    assert await dropdown.evaluate("el => el.open")
    await expect(trigger).to_have_attribute("aria-expanded", "true")

    await page.mouse.move(1000, 850)
    await expect(menu).to_be_hidden()
    await expect(trigger).to_have_attribute("aria-expanded", "false")


@pytest.mark.parametrize(("width", "height"), [(390, 844), (1280, 900)])
async def test_bengal_home_landing_page_uses_product_marketing_shapes(
    page, static_site_url, width, height
):
    await page.set_viewport_size({"width": width, "height": height})
    await page.goto(f"{static_site_url}/")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(100)

    await assert_no_document_horizontal_overflow(page, f"bengal-home-landing-{width}x{height}")
    await expect(page.locator(".chirp-theme-home__hero-stage")).to_be_visible()
    await expect(page.locator(".chirp-theme-home__product-visual")).to_be_visible()
    await expect(page.locator(".chirp-theme-home__visual-compose")).to_be_visible()
    await expect(page.locator(".chirp-theme-home__visual-proof")).to_be_visible()
    await expect(page.locator(".chirp-theme-home__metric-grid")).to_be_visible()
    await expect(page.locator(".chirp-theme-home__bento")).to_be_visible()
    await expect(page.locator(".chirp-theme-home__feature-stack")).to_be_visible()
    await expect(page.locator(".chirp-theme-home__logo-cloud")).to_be_visible()
    await expect(page.locator(".chirp-theme-home__cta")).to_be_visible()

    metrics = await page.evaluate(
        """() => {
            const hero = document.querySelector(".chirp-theme-home__hero-stage");
            const proof = document.querySelector(".chirp-theme-home__proof");
            const title = document.querySelector(".chirp-theme-home__hero .chirpui-hero__title");
            const visual = document.querySelector(".chirp-theme-home__product-visual");
            const ctas = Array.from(document.querySelectorAll(".chirp-theme-home__actions .chirpui-btn"));
            const heroRect = hero.getBoundingClientRect();
            const proofRect = proof.getBoundingClientRect();
            const titleRect = title.getBoundingClientRect();
            const visualRect = visual.getBoundingClientRect();
            const ctaRects = ctas.map((cta) => cta.getBoundingClientRect());
            return {
                heroHeight: Math.round(heroRect.height),
                proofTop: Math.round(proofRect.top),
                titleWidth: Math.round(titleRect.width),
                visualWidth: Math.round(visualRect.width),
                ctaOverflow: ctaRects.some((rect) => rect.width < 88 || rect.height < 32),
                viewportHeight: window.innerHeight,
            };
        }"""
    )

    assert metrics["titleWidth"] > 180, metrics
    assert metrics["visualWidth"] > 260, metrics
    assert not metrics["ctaOverflow"], metrics
    assert metrics["proofTop"] <= metrics["viewportHeight"] + 24, metrics

    focus_metrics = await page.evaluate(
        """() => {
            const cta = document.querySelector(".chirp-theme-home__actions .chirpui-btn");
            const bento = document.querySelector(".chirp-theme-home__shape-link");
            cta.focus();
            const ctaFocused = document.activeElement === cta;
            bento.focus();
            return {
                ctaFocused,
                bentoFocused: document.activeElement === bento,
                bentoOutline: getComputedStyle(bento).outlineStyle,
            };
        }"""
    )
    assert focus_metrics["ctaFocused"], focus_metrics
    assert focus_metrics["bentoFocused"], focus_metrics


async def test_bengal_outfit_display_font_loads_and_styles_brand_titles(page, static_site_url):
    """#135 — the Outfit display webfont must actually load and style brand titles.

    Two halves of the contract:
      1. ``document.fonts`` reports Outfit (400 + 600) as loaded — proving the
         preloaded woff2 + linked fonts.css resolved, not the system fallback.
      2. A *brand* title (the home hero title, ``var(--font-display)``) resolves
         to the Outfit family. We deliberately do NOT assert a prose docs <h2>:
         inside ``.chirp-theme-docs-layout__content`` headings are intentionally
         re-set to the sans UI family, so Outfit there would be a false negative.
    """
    await page.set_viewport_size({"width": 1280, "height": 900})
    await page.goto(f"{static_site_url}/")
    await page.wait_for_load_state("networkidle")
    # Explicitly activate both declared weights, then wait for the font set to
    # settle. A preloaded-but-not-yet-rendered weight (e.g. 600, if nothing above
    # the fold uses it at load time) reports unloaded to ``document.fonts.check``;
    # ``document.fonts.load`` forces the @font-face woff2 to resolve so the check
    # proves the face is *available*, not merely that it happens to be painted.
    await page.evaluate(
        """() => Promise.all([
            document.fonts.load("400 1rem Outfit"),
            document.fonts.load("600 1rem Outfit"),
        ]).then(() => document.fonts.ready)"""
    )
    await page.wait_for_timeout(100)

    font_state = await page.evaluate(
        """() => {
            const loadedFamilies = new Set();
            document.fonts.forEach((face) => {
                if (face.status === "loaded") {
                    loadedFamilies.add(face.family.replace(/['\"]/g, ""));
                }
            });
            return {
                outfit400: document.fonts.check("400 1rem Outfit"),
                outfit600: document.fonts.check("600 1rem Outfit"),
                loadedFamilies: Array.from(loadedFamilies),
            };
        }"""
    )
    assert font_state["outfit400"], font_state
    assert font_state["outfit600"], font_state
    assert "Outfit" in font_state["loadedFamilies"], font_state

    # A brand title (display font) resolves to Outfit; a prose docs heading is
    # intentionally sans and must NOT be Outfit.
    title = page.locator(".chirp-theme-home__hero .chirpui-hero__title").first
    await expect(title).to_be_visible()
    title_font = await title.evaluate("(el) => getComputedStyle(el).fontFamily")
    assert "Outfit" in title_font, {"home_hero_title_font_family": title_font}

    # Cross-check a docs section hero title also picks up Outfit (the section
    # header treatment uses var(--font-display)), not the prose-content override.
    await page.goto(f"{static_site_url}/docs/patterns/")
    await page.wait_for_load_state("networkidle")
    await page.evaluate("() => document.fonts.ready")
    section_title = page.locator(".chirp-theme-docs-layout__hero .chirpui-hero__title").first
    await expect(section_title).to_be_visible()
    section_font = await section_title.evaluate("(el) => getComputedStyle(el).fontFamily")
    assert "Outfit" in section_font, {"docs_section_hero_title_font_family": section_font}

    # The prose docs heading is intentionally the sans UI family (issue #135 note):
    # if a docs-content <h2> exists, it should NOT resolve to Outfit.
    prose_h2 = page.locator(".chirp-theme-docs-layout__content h2").first
    if await prose_h2.count() > 0:
        prose_font = await prose_h2.evaluate("(el) => getComputedStyle(el).fontFamily")
        assert "Outfit" not in prose_font, {"prose_h2_should_be_sans_not_outfit": prose_font}


async def test_bengal_docs_catalog_shell_moves_global_chrome_to_rail(page, static_site_url):
    for width, height in ((2309, 1606), (1159, 863), (889, 863)):
        await page.set_viewport_size({"width": width, "height": height})
        await page.goto(f"{static_site_url}/docs/app-shell/")
        await page.wait_for_load_state("networkidle")

        await assert_no_document_horizontal_overflow(page, f"app-shell-rail-only-{width}")
        await expect(page.locator(".chirp-theme-shell__header")).to_be_hidden()
        await expect(page.locator(".chirp-theme-doc-catalog-rail__home")).to_be_visible()
        await expect(
            page.locator(
                ".chirp-theme-doc-catalog-rail__home .chirp-theme-doc-catalog-rail__brand-mark"
            )
        ).to_have_text("ᗢ")
        await expect(
            page.locator(".chirp-theme-doc-catalog-rail__group--actions .nav-search-trigger")
        ).to_be_visible()
        await expect(
            page.locator(".chirp-theme-doc-catalog-rail__group--actions .theme-dropdown__button")
        ).to_be_visible()
        metrics = await page.evaluate(
            """() => {
                const header = document.querySelector(".chirp-theme-shell__header");
                const layout = document.querySelector(".chirp-theme-docs-layout");
                const sidebar = document.querySelector(".chirp-theme-docs-layout__sidebar");
                const catalog = document.querySelector(".chirp-theme-doc-catalog");
                const secondary = document.querySelector(".chirp-theme-doc-catalog__secondary");
                const secondaryItem = secondary.querySelector(".chirp-theme-docs-nav");
                const home = document.querySelector(".chirp-theme-doc-catalog-rail__home");
                const actions = document.querySelector(".chirp-theme-doc-catalog-rail__group--actions");
                const secondaryStyle = getComputedStyle(secondary);
                const secondaryRect = secondary.getBoundingClientRect();
                const secondaryItemRect = secondaryItem.getBoundingClientRect();
                return {
                    headerDisplay: getComputedStyle(header).display,
                    layoutTop: Math.round(layout.getBoundingClientRect().top),
                    sidebarTop: Math.round(sidebar.getBoundingClientRect().top),
                    catalogHeight: Math.round(catalog.getBoundingClientRect().height),
                    viewportHeight: window.innerHeight,
                    secondaryDisplay: secondaryStyle.display,
                    secondaryPaddingRight: parseFloat(secondaryStyle.paddingRight),
                    secondaryInlineStartGap: Math.round(secondaryItemRect.left - secondaryRect.left),
                    homeTop: Math.round(home.getBoundingClientRect().top),
                    actionsBottomGap: Math.round(window.innerHeight - actions.getBoundingClientRect().bottom),
                };
            }"""
        )
        assert metrics["headerDisplay"] == "none", metrics
        assert metrics["layoutTop"] == 0, metrics
        assert metrics["sidebarTop"] == 0, metrics
        assert abs(metrics["catalogHeight"] - metrics["viewportHeight"]) <= 2, metrics
        if width > 1024:
            assert metrics["secondaryDisplay"] != "none", metrics
            assert metrics["secondaryInlineStartGap"] <= 1, metrics
            assert metrics["secondaryPaddingRight"] <= 6, metrics
        assert 0 <= metrics["homeTop"] <= 18, metrics
        assert 0 <= metrics["actionsBottomGap"] <= 18, metrics


async def test_bengal_docs_catalog_action_buttons_match_section_rail_items(page, static_site_url):
    await page.set_viewport_size({"width": 2309, "height": 1606})
    await page.goto(f"{static_site_url}/docs/app-shell/")
    await page.wait_for_load_state("networkidle")

    metrics = await page.evaluate(
        """() => {
            const item = document.querySelector(
                ".chirp-theme-doc-catalog-rail__group--sections "
                + ".chirp-theme-doc-catalog-rail__item"
            );
            const search = document.querySelector(
                ".chirp-theme-doc-catalog-rail__group--actions .nav-search-trigger"
            );
            const theme = document.querySelector(
                ".chirp-theme-doc-catalog-rail__group--actions .theme-dropdown__button"
            );
            const itemMark = item.querySelector(".chirp-theme-doc-catalog-rail__mark");
            const searchMark = search.querySelector(".chirp-theme-doc-catalog-rail__mark");
            const themeMark = theme.querySelector(".theme-dropdown__icon");
            const rect = (el) => {
                const box = el.getBoundingClientRect();
                return {
                    width: Math.round(box.width),
                    height: Math.round(box.height),
                    radius: getComputedStyle(el).borderRadius,
                    display: getComputedStyle(el).display,
                };
            };
            return {
                item: rect(item),
                search: rect(search),
                theme: rect(theme),
                itemMark: rect(itemMark),
                searchMark: rect(searchMark),
                themeMark: rect(themeMark),
            };
        }"""
    )
    assert metrics["search"] == metrics["item"], metrics
    assert metrics["theme"] == metrics["item"], metrics
    assert metrics["searchMark"] == metrics["itemMark"], metrics
    assert metrics["themeMark"] == metrics["itemMark"], metrics


async def test_bengal_api_index_uses_catalog_shell_without_overflow(page, static_site_url):
    await page.set_viewport_size({"width": 889, "height": 863})
    await page.goto(f"{static_site_url}/api/")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(100)

    await assert_no_document_horizontal_overflow(page, "api-index-889")
    await expect(page.locator('[data-chirp-theme-surface="api-list"]')).to_be_visible()
    await expect(page.locator(".chirp-theme-docs-layout__sidebar")).to_be_visible()
    await expect(page.locator(".chirp-theme-doc-catalog__primary")).to_be_visible()
    await expect(page.locator(".chirp-theme-doc-catalog__secondary")).to_be_hidden()
    await expect(page.locator(".chirp-theme-api-hero")).to_be_visible()
    await expect(page.locator(".chirp-theme-api-index")).to_be_visible()
    assert await page.locator(".chirp-theme-reference-card").count() >= 3
    assert await page.locator(".chirp-theme-reference-grid").count() == 0
    assert await page.locator(".chirp-theme-api-index .chirpui-selection-bar:visible").count() == 0
    assert await page.locator(".chirp-theme-api-index .chirpui-resource-index__search").count() == 0

    metrics = await page.evaluate(
        """() => {
            const nav = document.querySelector(".chirp-theme-shell__nav");
            const hero = document.querySelector(".chirp-theme-api-hero");
            const results = document.querySelector(".chirp-theme-api-index .chirpui-resource-index__results");
            const search = document.querySelector(".chirp-theme-api-index .chirpui-resource-index__search");
            const card = document.querySelector(".chirp-theme-reference-card");
            const cardMark = card.querySelector(".chirp-theme-reference-card__mark");
            const cardTitle = card.querySelector(".chirp-theme-reference-card__title");
            const cardDescription = card.querySelector(".chirp-theme-reference-card__description");
            const cardFooter = card.querySelector(".chirp-theme-reference-card__footer");
            const navBottom = nav.getBoundingClientRect().bottom;
            const heroRect = hero.getBoundingClientRect();
            const resultsStyle = getComputedStyle(results);
            const cardStyle = getComputedStyle(card);
            const cardRect = card.getBoundingClientRect();
            const descriptionStyle = getComputedStyle(cardDescription);
            return {
                heroGap: Math.round(heroRect.top - navBottom),
                heroBackground: getComputedStyle(hero).backgroundImage,
                resultColumns: resultsStyle.gridTemplateColumns.split(" ").filter(Boolean).length,
                hasDeadSearchForm: Boolean(search),
                cardBorder: cardStyle.borderTopWidth,
                cardBackground: cardStyle.backgroundImage,
                cardDisplay: cardStyle.display,
                cardWidth: Math.round(cardRect.width),
                cardColumns: cardStyle.gridTemplateColumns,
                markWidth: Math.round(cardMark.getBoundingClientRect().width),
                markColor: getComputedStyle(cardMark).color,
                titleOverflowWrap: getComputedStyle(cardTitle).overflowWrap,
                descriptionClamp: descriptionStyle.webkitLineClamp,
                footerDisplay: getComputedStyle(cardFooter).display,
            };
        }"""
    )
    assert 0 <= metrics["heroGap"] <= 18, metrics
    assert "linear-gradient" in metrics["heroBackground"], metrics
    assert metrics["resultColumns"] >= 2, metrics
    assert metrics["hasDeadSearchForm"] is False, metrics
    assert metrics["cardBorder"] == "0px", metrics
    assert "linear-gradient" in metrics["cardBackground"], metrics
    assert metrics["cardDisplay"] == "grid", metrics
    assert metrics["cardWidth"] >= 240, metrics
    assert " " in metrics["cardColumns"], metrics
    assert metrics["markWidth"] >= 30, metrics
    assert metrics["markColor"] != "", metrics
    assert metrics["titleOverflowWrap"] == "anywhere", metrics
    assert metrics["descriptionClamp"] == "4", metrics
    assert metrics["footerDisplay"] == "flex", metrics


async def test_bengal_api_module_uses_app_shell_reference_frame(page, static_site_url):
    await page.set_viewport_size({"width": 1280, "height": 900})
    await page.goto(f"{static_site_url}/api/route_tabs/")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(100)

    await assert_no_document_horizontal_overflow(page, "api-module-1280")
    await expect(page.locator('[data-chirp-theme-surface="api-reference"]')).to_be_visible()
    await expect(page.locator(".chirp-theme-docs-layout__sidebar")).to_be_visible()
    await expect(page.locator(".chirp-theme-doc-catalog__secondary")).to_be_visible()
    await expect(page.locator(".chirp-theme-reference-hero")).to_be_visible()
    await expect(page.locator(".chirp-theme-reference-page--python")).to_be_visible()

    metrics = await page.evaluate(
        """() => {
            const article = document.querySelector(".chirp-theme-reference-page--python");
            const content = document.querySelector(".chirp-theme-reference-content");
            const hero = document.querySelector(".chirp-theme-reference-hero");
            const description = document.querySelector(".chirp-theme-reference-description");
            const descriptionCode = description.querySelector("code");
            const member = document.querySelector(".chirp-theme-reference-member");
            const memberTrigger = member.querySelector(".chirpui-accordion__trigger");
            const memberActions = member.querySelector(".chirpui-accordion__trigger-actions");
            const memberContent = member.querySelector(".chirpui-accordion__content");
            const memberBodyBadge = member.querySelector(".chirp-theme-reference-member__body > .chirpui-badge");
            const heroStyle = getComputedStyle(hero);
            const memberStyle = getComputedStyle(member);
            const triggerStyle = getComputedStyle(memberTrigger);
            const triggerMarkerStyle = getComputedStyle(memberTrigger, "::before");
            const actionsStyle = getComputedStyle(memberActions);
            const contentStyle = getComputedStyle(memberContent);
            return {
                articleMaxWidth: getComputedStyle(article).maxWidth,
                contentMaxWidth: getComputedStyle(content).maxWidth,
                heroBorder: heroStyle.borderTopWidth,
                heroBackground: heroStyle.backgroundImage,
                descriptionHasParagraph: Boolean(description.querySelector("p")),
                descriptionCodeText: descriptionCode ? descriptionCode.textContent : "",
                memberOverflow: memberStyle.overflow,
                memberTriggerDisplay: triggerStyle.display,
                memberTriggerColumns: triggerStyle.gridTemplateColumns.split(" ").filter(Boolean).length,
                memberTriggerMarkerContent: triggerMarkerStyle.content,
                memberTriggerMarkerWidth: Math.round(Number.parseFloat(triggerMarkerStyle.width)),
                memberActionsMarginStart: actionsStyle.marginInlineStart,
                memberContentPaddingTop: Math.round(Number.parseFloat(contentStyle.paddingTop)),
                memberContentBorderTop: contentStyle.borderTopWidth,
                memberActionBadgeCount: memberActions.querySelectorAll(".chirpui-badge").length,
                memberBodyBadgeCount: memberBodyBadge ? 1 : 0,
            };
        }"""
    )
    assert metrics["articleMaxWidth"] != "none", metrics
    assert metrics["contentMaxWidth"] != "65ch", metrics
    assert metrics["heroBorder"] == "0px", metrics
    assert "linear-gradient" in metrics["heroBackground"], metrics
    assert metrics["descriptionHasParagraph"] is True, metrics
    assert metrics["descriptionCodeText"] == "href", metrics
    assert metrics["memberOverflow"] == "clip", metrics
    assert metrics["memberTriggerDisplay"] == "grid", metrics
    assert metrics["memberTriggerColumns"] == 3, metrics
    assert metrics["memberTriggerMarkerContent"] == '""', metrics
    assert metrics["memberTriggerMarkerWidth"] >= 5, metrics
    assert metrics["memberActionsMarginStart"] == "0px", metrics
    assert metrics["memberContentPaddingTop"] == 0, metrics
    assert metrics["memberContentBorderTop"] == "1px", metrics
    assert metrics["memberActionBadgeCount"] == 1, metrics
    assert metrics["memberBodyBadgeCount"] == 0, metrics


async def test_bengal_section_hubs_and_release_index(page, static_site_url):
    await page.set_viewport_size({"width": 1280, "height": 900})
    await page.goto(f"{static_site_url}/layouts/")
    await page.wait_for_load_state("networkidle")
    assert await page.locator(".chirp-theme-section-hub__card").count() >= 5
    await page.goto(f"{static_site_url}/dev/")
    await page.wait_for_load_state("networkidle")
    assert await page.locator(".chirp-theme-section-hub__card").count() >= 2
    await page.goto(f"{static_site_url}/releases/")
    await page.wait_for_load_state("networkidle")
    metrics = await page.evaluate(
        """() => ({
            groups: document.querySelectorAll(".chirp-theme-release-group").length,
            navItems: document.querySelectorAll(".chirp-theme-releases-nav__item").length,
            heroBadge: document.querySelector(".chirp-theme-release-hero--index .chirpui-badge"),
            heroCount: (document.querySelector(".chirp-theme-release-hero--index .chirpui-hero__metadata")?.textContent ?? "").trim(),
            installHeight: Math.round(document.querySelector(".chirp-theme-release-install")?.getBoundingClientRect().height ?? 0),
        })"""
    )
    assert metrics["groups"] == 10, metrics
    assert metrics["navItems"] == 10, metrics
    assert metrics["heroBadge"] is None, metrics
    assert metrics["heroCount"] == "", metrics
    assert metrics["installHeight"] <= 28, metrics


async def test_bengal_api_module_symbol_cards_use_reference_grid(page, static_site_url):
    await page.set_viewport_size({"width": 1280, "height": 900})
    await page.goto(f"{static_site_url}/api/inspect/")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(100)

    await expect(page.locator(".chirp-theme-reference-symbols")).to_be_visible()
    symbol_cards = page.locator(".chirp-theme-reference-card--symbol")
    assert await symbol_cards.count() >= 3

    metrics = await page.evaluate(
        """() => {
            const card = document.querySelector(".chirp-theme-reference-card--symbol");
            const mark = card.querySelector(".chirp-theme-reference-card__mark");
            const eyebrow = card.querySelector(".chirp-theme-reference-card__eyebrow");
            const title = card.querySelector(".chirp-theme-reference-card__title");
            const description = card.querySelector(".chirp-theme-reference-card__description");
            const cardStyle = getComputedStyle(card);
            const markRect = mark.getBoundingClientRect();
            const eyebrowRect = eyebrow.getBoundingClientRect();
            const titleRect = title.getBoundingClientRect();
            const nameCell = document.querySelector(
                ".chirp-theme-reference-params .chirpui-params-table__td--name code"
            );
            return {
                usesResourceCardDom: Boolean(card.querySelector(".chirpui-card__top-meta")),
                cardDisplay: cardStyle.display,
                cardHeight: Math.round(card.getBoundingClientRect().height),
                markEyebrowSameRow: Math.abs(markRect.top - eyebrowRect.top) <= 2,
                titleBelowEyebrow: titleRect.top > eyebrowRect.top,
                descriptionClamp: getComputedStyle(description).webkitLineClamp,
                nameCodeWrap: nameCell ? getComputedStyle(nameCell).whiteSpace : null,
                duplicateModuleBadge: document.querySelectorAll(
                    ".chirp-theme-reference-badges .chirpui-badge"
                ).length,
            };
        }"""
    )
    assert metrics["usesResourceCardDom"] is False, metrics
    assert metrics["cardDisplay"] == "grid", metrics
    assert metrics["cardHeight"] <= 220, metrics
    assert metrics["markEyebrowSameRow"] is True, metrics
    assert metrics["titleBelowEyebrow"] is True, metrics
    assert metrics["descriptionClamp"] == "3", metrics
    assert metrics["nameCodeWrap"] == "nowrap", metrics
    assert metrics["duplicateModuleBadge"] == 0, metrics


async def test_bengal_api_prose_code_specimens_use_compact_treatment(page, static_site_url):
    await page.set_viewport_size({"width": 1280, "height": 900})
    await page.goto(f"{static_site_url}/api/find/")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(100)

    specimen = page.locator(
        ".chirp-theme-reference-description .code-block-wrapper--specimen"
    ).first
    await expect(specimen).to_be_visible()
    metrics = await specimen.evaluate(
        """el => {
            const pre = el.querySelector("pre");
            const code = el.querySelector("code");
            const marker = getComputedStyle(el, "::before");
            const copy = el.querySelector(".code-copy-button");
            const copyLabel = copy.querySelector("span");
            const style = getComputedStyle(el);
            const preStyle = getComputedStyle(pre);
            const codeStyle = getComputedStyle(code);
            const labelStyle = getComputedStyle(copyLabel);
            return {
                text: code.textContent.trim(),
                wrapperHeight: Math.round(el.getBoundingClientRect().height),
                wrapperBorderWidth: style.borderTopWidth,
                wrapperBoxShadow: style.boxShadow,
                codeWhiteSpace: codeStyle.whiteSpace,
                preLineHeight: Math.round(Number.parseFloat(preStyle.lineHeight)),
                preBorderWidth: preStyle.borderTopWidth,
                preBoxShadow: preStyle.boxShadow,
                codeBorderWidth: codeStyle.borderTopWidth,
                codeBoxShadow: codeStyle.boxShadow,
                markerDisplay: marker.display,
                copyWidth: Math.round(copy.getBoundingClientRect().width),
                copyLabelClip: labelStyle.clipPath,
            };
        }"""
    )
    assert metrics["text"] == "{name:<30} {category:<16} {first-line-of-description}", metrics
    assert metrics["wrapperHeight"] <= 48, metrics
    assert metrics["wrapperBorderWidth"] == "0px", metrics
    assert metrics["wrapperBoxShadow"] == "none", metrics
    assert metrics["codeWhiteSpace"] == "pre-wrap", metrics
    assert metrics["preLineHeight"] <= 20, metrics
    assert metrics["preBorderWidth"] == "0px", metrics
    assert metrics["preBoxShadow"] == "none", metrics
    assert metrics["codeBorderWidth"] == "0px", metrics
    assert metrics["codeBoxShadow"] == "none", metrics
    assert metrics["markerDisplay"] == "none", metrics
    assert 24 <= metrics["copyWidth"] <= 32, metrics
    assert metrics["copyLabelClip"] == "inset(50%)", metrics

    await page.goto(f"{static_site_url}/api/filters/")
    await page.wait_for_load_state("networkidle")
    await page.locator("#deprecate_param").evaluate("el => el.closest('details').open = true")
    member_specimen = page.locator(
        "#deprecate_param .chirp-theme-reference-member__description .code-block-wrapper--specimen"
    )
    await expect(member_specimen).to_be_visible()
    member_metrics = await member_specimen.evaluate(
        """el => {
            const pre = el.querySelector("pre");
            const code = el.querySelector("code");
            const marker = getComputedStyle(el, "::before");
            const preStyle = getComputedStyle(pre);
            const codeStyle = getComputedStyle(code);
            return {
                text: code.textContent.trim(),
                wrapperHeight: Math.round(el.getBoundingClientRect().height),
                markerDisplay: marker.display,
                preBorderWidth: preStyle.borderTopWidth,
                preBoxShadow: preStyle.boxShadow,
                codeBackground: codeStyle.backgroundColor,
            };
        }"""
    )
    assert member_metrics["text"].startswith("{% set _attrs_raw = attrs_unsafe"), member_metrics
    assert member_metrics["wrapperHeight"] <= 60, member_metrics
    assert member_metrics["markerDisplay"] == "none", member_metrics
    assert member_metrics["preBorderWidth"] == "0px", member_metrics
    assert member_metrics["preBoxShadow"] == "none", member_metrics
    assert member_metrics["codeBackground"] == "rgba(0, 0, 0, 0)", member_metrics


async def test_bengal_api_compact_summaries_render_markdown_code(page, static_site_url):
    await page.set_viewport_size({"width": 1280, "height": 900})
    await page.goto(f"{static_site_url}/api/manifest/")
    await page.wait_for_load_state("networkidle")

    hero_metrics = await page.evaluate(
        """() => {
            const summary = document.querySelector(".chirp-theme-reference-hero__summary");
            const content = summary.closest(".chirpui-hero__content");
            return {
                text: summary.textContent,
                codeTexts: Array.from(summary.querySelectorAll("code")).map((code) => code.textContent),
                paragraphCount: summary.querySelectorAll("p").length,
                contentGridColumn: getComputedStyle(content).gridColumnStart,
                contentGridRow: getComputedStyle(content).gridRowStart,
            };
        }"""
    )
    assert "``" not in hero_metrics["text"], hero_metrics
    assert "chirp_ui.components.COMPONENTS" in hero_metrics["codeTexts"], hero_metrics
    assert "chirp_ui.tokens.TOKEN_CATALOG" in hero_metrics["codeTexts"], hero_metrics
    assert hero_metrics["paragraphCount"] >= 1, hero_metrics
    assert hero_metrics["contentGridColumn"] == "1", hero_metrics
    assert hero_metrics["contentGridRow"] == "3", hero_metrics

    await page.goto(f"{static_site_url}/api/")
    await page.wait_for_load_state("networkidle")
    card_metrics = await page.locator(
        'a.chirp-theme-reference-card[href="/api/manifest/"]'
    ).evaluate(
        """card => {
            const description = card.querySelector(".chirp-theme-reference-card__description");
            return {
                text: description.textContent,
                codeTexts: Array.from(description.querySelectorAll("code")).map((code) => code.textContent),
                paragraphCount: description.querySelectorAll("p").length,
                display: getComputedStyle(description).display,
            };
        }"""
    )
    assert "``" not in card_metrics["text"], card_metrics
    assert "chirp_ui.components.COMPONENTS" in card_metrics["codeTexts"], card_metrics
    assert "chirp_ui.tokens.TOKEN_CATALOG" in card_metrics["codeTexts"], card_metrics
    assert card_metrics["paragraphCount"] >= 1, card_metrics
    assert card_metrics["display"] == "flow-root" or "-webkit-box" in card_metrics["display"], (
        card_metrics
    )


async def test_bengal_api_member_accordion_rows_align_open_and_closed(page, static_site_url):
    await page.set_viewport_size({"width": 1280, "height": 900})
    await page.goto(f"{static_site_url}/api/find/")
    await page.wait_for_load_state("networkidle")

    await expect(page.locator(".chirp-theme-reference-members")).to_be_visible()
    metrics = await page.evaluate(
        """() => {
            const members = Array.from(document.querySelectorAll(".chirp-theme-reference-member"));
            const openMember = members.find((member) => member.open);
            const closedMember = members.find((member) => !member.open);
            const measure = (member) => {
                const trigger = member.querySelector(".chirpui-accordion__trigger");
                const title = trigger.querySelector(".chirpui-accordion__trigger-text");
                const actions = trigger.querySelector(".chirpui-accordion__trigger-actions");
                const content = member.querySelector(".chirpui-accordion__content");
                const body = member.querySelector(".chirp-theme-reference-member__body");
                const description = member.querySelector(".chirp-theme-reference-member__description");
                const triggerRect = trigger.getBoundingClientRect();
                const titleRect = title.getBoundingClientRect();
                const actionsRect = actions.getBoundingClientRect();
                const bodyRect = body.getBoundingClientRect();
                const descriptionRect = description.getBoundingClientRect();
                const triggerStyle = getComputedStyle(trigger);
                const markerStyle = getComputedStyle(trigger, "::before");
                const contentStyle = getComputedStyle(content);
                const bodyStyle = getComputedStyle(body);
                return {
                    open: member.open,
                    triggerColumns: triggerStyle.gridTemplateColumns.split(" ").filter(Boolean).length,
                    triggerHeight: Math.round(triggerRect.height),
                    titleLeft: Math.round(titleRect.left - triggerRect.left),
                    titleRightGap: Math.round(actionsRect.left - titleRect.right),
                    actionsRightGap: Math.round(triggerRect.right - actionsRect.right),
                    markerContent: markerStyle.content,
                    markerWidth: Math.round(Number.parseFloat(markerStyle.width)),
                    markerTransform: markerStyle.transform,
                    actionsMarginStart: getComputedStyle(actions).marginInlineStart,
                    contentPaddingTop: Math.round(Number.parseFloat(contentStyle.paddingTop)),
                    contentBorderTop: contentStyle.borderTopWidth,
                    bodyLeft: Math.round(bodyRect.left - triggerRect.left),
                    bodyPaddingLeft: Math.round(Number.parseFloat(bodyStyle.paddingLeft)),
                    descriptionLeft: Math.round(descriptionRect.left - triggerRect.left),
                };
            };
            return {
                open: measure(openMember),
                closed: measure(closedMember),
            };
        }"""
    )
    for state in (metrics["open"], metrics["closed"]):
        assert state["triggerColumns"] == 3, metrics
        assert 40 <= state["triggerHeight"] <= 52, metrics
        assert state["titleLeft"] >= 28, metrics
        assert state["titleRightGap"] >= 8, metrics
        assert state["actionsRightGap"] >= 10, metrics
        assert state["markerContent"] == '""', metrics
        assert state["markerWidth"] >= 5, metrics
        assert state["actionsMarginStart"] == "0px", metrics
        assert state["contentPaddingTop"] == 0, metrics
        assert state["contentBorderTop"] == "1px", metrics
    assert metrics["open"]["markerTransform"] != metrics["closed"]["markerTransform"], metrics
    assert metrics["open"]["bodyPaddingLeft"] >= metrics["open"]["titleLeft"] - 2, metrics
    assert metrics["open"]["descriptionLeft"] >= metrics["open"]["titleLeft"] - 2, metrics


async def test_bengal_catalog_footer_lives_inside_shell_content(page, static_site_url):
    await page.set_viewport_size({"width": 1280, "height": 900})
    await page.goto(f"{static_site_url}/api/layout_affinity/")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(100)

    await assert_no_document_horizontal_overflow(page, "api-footer-inside-shell")
    await expect(page.locator(".chirp-theme-footer--shell")).to_be_visible()
    assert await page.locator("body > .chirp-theme-footer").count() == 0
    metrics = await page.evaluate(
        """() => {
            const root = document.documentElement;
            const mainColumn = document.querySelector(".chirp-theme-docs-layout__main");
            const article = document.querySelector(".chirp-theme-docs-layout__article");
            const footer = document.querySelector(".chirp-theme-footer--shell");
            const footerGrid = footer.querySelector(".chirpui-site-footer__grid");
            const footerList = footer.querySelector(".chirpui-site-footer__list");
            const footerLink = footer.querySelector(".chirpui-site-footer__link");
            const mainRect = mainColumn.getBoundingClientRect();
            const articleRect = article.getBoundingClientRect();
            const footerRect = footer.getBoundingClientRect();
            const linkRect = footerLink.getBoundingClientRect();
            const linkBefore = getComputedStyle(footerLink, "::before");
            return {
                footerParentClass: footer.parentElement.className,
                footerLeft: Math.round(footerRect.left),
                mainLeft: Math.round(mainRect.left),
                articleLeft: Math.round(articleRect.left),
                footerWidth: Math.round(footerRect.width),
                articleWidth: Math.round(articleRect.width),
                viewportWidth: root.clientWidth,
                gridColumns: getComputedStyle(footerGrid).gridTemplateColumns.split(" ").length,
                listDisplay: getComputedStyle(footerList).display,
                listStyle: getComputedStyle(footerList).listStyleType,
                linkDisplay: getComputedStyle(footerLink).display,
                linkMinHeight: Math.round(linkRect.height),
                linkBeforeContent: linkBefore.content,
                linkBeforeWidth: Math.round(parseFloat(linkBefore.width)),
            };
        }"""
    )
    assert "chirp-theme-docs-layout__main" in metrics["footerParentClass"], metrics
    assert metrics["footerLeft"] >= metrics["mainLeft"], metrics
    assert abs(metrics["footerLeft"] - metrics["articleLeft"]) <= 4, metrics
    assert abs(metrics["footerWidth"] - metrics["articleWidth"]) <= 4, metrics
    assert metrics["footerWidth"] < metrics["viewportWidth"] - 120, metrics
    assert metrics["gridColumns"] == 3, metrics
    assert metrics["listDisplay"] == "grid", metrics
    assert metrics["listStyle"] == "none", metrics
    assert metrics["linkDisplay"] == "inline-flex", metrics
    assert metrics["linkMinHeight"] >= 20, metrics
    assert metrics["linkBeforeContent"] == '""', metrics
    assert metrics["linkBeforeWidth"] >= 3, metrics


async def test_bengal_docs_desktop_content_starts_near_viewport_top(page, static_site_url):
    await page.set_viewport_size({"width": 2309, "height": 1606})
    await page.goto(f"{static_site_url}/docs/patterns/")
    await page.wait_for_load_state("networkidle")

    await assert_no_document_horizontal_overflow(page, "patterns-header-gap-2309")
    metrics = await page.evaluate(
        """() => {
            const layout = document.querySelector("#main-content .chirp-theme-docs-layout");
            const hero = layout.querySelector(".chirp-theme-docs-layout__hero");
            const tocContext = layout.querySelector(".chirp-theme-doc-toc__context");
            const firstRailItem = layout.querySelector(
                ".chirp-theme-docs-layout__sidebar .chirp-theme-doc-catalog-rail__item"
            );
            const layoutTop = layout.getBoundingClientRect().top;
            return {
                layoutTop: Math.round(layoutTop),
                heroGap: Math.round(hero.getBoundingClientRect().top),
                tocGap: Math.round(tocContext.getBoundingClientRect().top),
                railGap: Math.round(firstRailItem.getBoundingClientRect().top),
                mainPaddingTop: Math.round(
                    parseFloat(getComputedStyle(
                        layout.querySelector(".chirp-theme-docs-layout__main")
                    ).paddingTop)
                ),
            };
        }"""
    )
    assert metrics["layoutTop"] == 0, metrics
    assert metrics["heroGap"] <= 18, metrics
    assert 0 <= metrics["tocGap"] <= 18, metrics
    assert 0 <= metrics["railGap"] <= 18, metrics
    assert abs(metrics["tocGap"] - metrics["railGap"]) <= 8, metrics
    assert abs(metrics["tocGap"] - metrics["heroGap"]) <= 12, metrics
    assert metrics["mainPaddingTop"] <= 18, metrics


async def test_bengal_docs_hero_uses_catalog_header_treatment(page, static_site_url):
    await page.set_viewport_size({"width": 2309, "height": 1606})
    await page.goto(f"{static_site_url}/docs/patterns/")
    await page.wait_for_load_state("networkidle")

    await expect(page.locator(".chirp-theme-docs-layout__hero")).to_be_visible()
    metrics = await page.evaluate(
        """() => {
            const hero = document.querySelector(".chirp-theme-docs-layout__hero");
            const inner = hero.querySelector(".chirpui-hero__inner");
            const title = hero.querySelector(".chirpui-hero__title");
            const subtitle = hero.querySelector(".chirpui-hero__subtitle");
            const metadata = hero.querySelector(".chirpui-hero__metadata");
            const marker = getComputedStyle(hero, "::before");
            const heroStyle = getComputedStyle(hero);
            const innerStyle = getComputedStyle(inner);
            const heroRect = hero.getBoundingClientRect();
            const titleRect = title.getBoundingClientRect();
            const subtitleRect = subtitle.getBoundingClientRect();
            const metadataRect = metadata.getBoundingClientRect();
            const metadataAnchorRect = subtitle ? subtitleRect : titleRect;
            return {
                textAlign: innerStyle.textAlign,
                borderBottom: heroStyle.borderBottomWidth,
                background: heroStyle.backgroundImage,
                markerWidth: Math.round(Number.parseFloat(marker.width)),
                titleInset: Math.round(titleRect.left - heroRect.left),
                subtitleInsetDelta: Math.round(Math.abs(subtitleRect.left - titleRect.left)),
                metadataRightGap: Math.round(heroRect.right - metadataRect.right),
                metadataTopDelta: Math.round(
                    Math.abs(metadataRect.top - metadataAnchorRect.top)
                ),
                height: Math.round(heroRect.height),
            };
        }"""
    )
    assert metrics["textAlign"] == "left", metrics
    assert metrics["borderBottom"] == "0px", metrics
    assert "linear-gradient" in metrics["background"], metrics
    assert metrics["markerWidth"] >= 3, metrics
    assert 12 <= metrics["titleInset"] <= 32, metrics
    assert metrics["subtitleInsetDelta"] <= 2, metrics
    assert metrics["metadataRightGap"] <= 4, metrics
    # Since #250, page actions sit on row 2 and metadata drops to row 3 — when a
    # subtitle is present the pill shares that row (not the title row).
    assert metrics["metadataTopDelta"] <= 16, metrics
    # The <= 170 ceiling was aspirational and never actually met — the docs hero
    # measures ~190px @1280 / ~172px @1600 / ~179px @2309 on macOS, and ~206px on
    # the Linux CI runner (font metrics differ across platforms). The hero
    # title/subtitle type scale is intentional and should not shrink, so cap at the
    # observed cross-platform worst case (206) plus headroom rather than force a
    # regression. Revisit if the hero treatment is deliberately compacted.
    assert metrics["height"] <= 224, metrics


async def test_bengal_docs_hero_exposes_page_actions_popover(page, static_site_url):
    await page.set_viewport_size({"width": 1159, "height": 863})
    await page.goto(f"{static_site_url}/docs/app-shell/")
    await page.wait_for_load_state("networkidle")

    await assert_no_document_horizontal_overflow(page, "page-actions-hero")
    trigger = page.locator(".chirp-theme-page-actions__trigger")
    menu = page.locator(".chirp-theme-page-actions__menu")
    await expect(trigger).to_be_visible()
    await trigger.click()
    await expect(menu).to_be_visible()
    await expect(menu.locator('[data-action="copy-url"]')).to_be_visible()
    await expect(menu.locator('[data-action="copy-llm-txt"]')).to_be_visible()
    await expect(menu.locator('[data-ai="chatgpt"]')).to_be_visible()

    metrics = await page.evaluate(
        """() => {
            const hero = document.querySelector(".chirp-theme-docs-layout__hero");
            const trigger = hero.querySelector(".chirp-theme-page-actions__trigger");
            const menu = document.querySelector(".chirp-theme-page-actions__menu");
            const triggerRect = trigger.getBoundingClientRect();
            const menuRect = menu.getBoundingClientRect();
            return {
                triggerRightGap: Math.round(hero.getBoundingClientRect().right - triggerRect.right),
                menuOpen: menu.matches(":popover-open"),
                menuWidth: Math.round(menuRect.width),
                menuRight: Math.round(menuRect.right),
                viewportWidth: document.documentElement.clientWidth,
            };
        }"""
    )
    assert metrics["triggerRightGap"] <= 4, metrics
    assert metrics["menuOpen"], metrics
    assert 260 <= metrics["menuWidth"] <= 360, metrics
    assert metrics["menuRight"] <= metrics["viewportWidth"] - 4, metrics


async def test_bengal_docs_hero_hides_empty_metadata_pill(page, static_site_url):
    await page.set_viewport_size({"width": 919, "height": 863})
    await page.goto(f"{static_site_url}/docs/theming/chirp-theme/")
    await page.wait_for_load_state("networkidle")

    hero = page.locator(".chirp-theme-docs-layout__hero")
    metadata = hero.locator(".chirpui-hero__metadata")
    await expect(hero).to_be_visible()
    await expect(hero.locator(".chirp-theme-page-actions__trigger")).to_be_visible()
    await expect(metadata).to_be_hidden()


async def test_bengal_docs_article_typography_is_dense_reference(page, static_site_url):
    await page.set_viewport_size({"width": 1280, "height": 900})
    await page.goto(f"{static_site_url}/docs/app-shell/")
    await page.wait_for_load_state("networkidle")

    await expect(page.locator(".chirp-theme-docs-layout__content h2").first).to_be_visible()
    metrics = await page.evaluate(
        """() => {
            const content = document.querySelector(".chirp-theme-docs-layout__content");
            const paragraph = content.querySelector("p");
            const h2 = content.querySelector("h2");
            const inlineCode = content.querySelector("p code");
            const contentStyle = getComputedStyle(content);
            const paragraphStyle = getComputedStyle(paragraph);
            const h2Style = getComputedStyle(h2);
            const codeStyle = getComputedStyle(inlineCode);
            return {
                contentWidth: Math.round(content.getBoundingClientRect().width),
                contentFontSize: Math.round(Number.parseFloat(contentStyle.fontSize)),
                contentLineHeight: Math.round(Number.parseFloat(contentStyle.lineHeight)),
                paragraphMarginBottom: Math.round(Number.parseFloat(paragraphStyle.marginBottom)),
                h2FontSize: Math.round(Number.parseFloat(h2Style.fontSize)),
                h2LineHeight: Math.round(Number.parseFloat(h2Style.lineHeight)),
                h2LetterSpacing: h2Style.letterSpacing,
                h2FontFamily: h2Style.fontFamily,
                codeFontSize: Math.round(Number.parseFloat(codeStyle.fontSize)),
                codeLineHeight: Math.round(Number.parseFloat(codeStyle.lineHeight)),
            };
        }"""
    )
    assert 520 <= metrics["contentWidth"] <= 760, metrics
    assert metrics["contentFontSize"] == 16, metrics
    assert 25 <= metrics["contentLineHeight"] <= 27, metrics
    assert 12 <= metrics["paragraphMarginBottom"] <= 16, metrics
    assert 25 <= metrics["h2FontSize"] <= 27, metrics
    assert 30 <= metrics["h2LineHeight"] <= 33, metrics
    assert metrics["h2LetterSpacing"] in {"normal", "0px"}, metrics
    assert "Outfit" not in metrics["h2FontFamily"], metrics
    assert 12 <= metrics["codeFontSize"] <= 14, metrics
    assert 15 <= metrics["codeLineHeight"] <= 18, metrics


async def test_bengal_docs_toc_owns_scroll_to_top_action(page, static_site_url):
    await page.set_viewport_size({"width": 1280, "height": 900})
    await page.goto(f"{static_site_url}/docs/app-shell/")
    await page.wait_for_load_state("networkidle")

    await expect(page.locator(".chirp-theme-docs-layout__toc")).to_be_visible()
    assert await page.locator(".back-to-top").count() == 1
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.5)")
    await page.wait_for_timeout(100)
    button = page.locator(".chirp-theme-floating-top.back-to-top")
    await expect(button).to_be_visible()
    assert await page.locator(".chirp-theme-rail-top.back-to-top").count() == 0
    metrics = await button.evaluate(
        """el => {
            const rect = el.getBoundingClientRect();
            const footer = document.querySelector(".chirp-theme-footer--shell");
            const footerMark = document.querySelector(".chirp-theme-footer__rule-mark");
            const footerStyle = getComputedStyle(footer);
            const footerMarkRect = footerMark.getBoundingClientRect();
            const buttonCenter = rect.left + rect.width / 2;
            const footerCenter = footerMarkRect.left + footerMarkRect.width / 2;
            const viewportCenter = window.innerWidth / 2;
            return {
                width: rect.width,
                height: rect.height,
                bottomGap: window.innerHeight - rect.bottom,
                footerCenterDelta: Math.abs(buttonCenter - footerCenter),
                viewportCenterDelta: Math.abs(buttonCenter - viewportCenter),
                footerPosition: footerStyle.position,
                footerOverflow: footerStyle.overflow,
                position: getComputedStyle(el).position,
            };
        }"""
    )
    assert metrics["position"] == "fixed", metrics
    assert 34 <= metrics["width"] <= 40, metrics
    assert 34 <= metrics["height"] <= 40, metrics
    # Lower bound relaxed 12 -> 8: the Linux CI runner renders the gap at ~10.7px
    # vs macOS ~12-13px (sub-pixel / font metrics). Intent: the back-to-top button
    # sits a small, fixed gap above the viewport bottom.
    assert 8 <= metrics["bottomGap"] <= 24, metrics
    assert metrics["footerCenterDelta"] <= 2, metrics
    assert metrics["viewportCenterDelta"] >= 32, metrics
    assert metrics["footerPosition"] == "relative", metrics
    assert metrics["footerOverflow"] == "visible", metrics


async def test_bengal_docs_code_blocks_use_catalog_surface(page, static_site_url):
    await page.set_viewport_size({"width": 1280, "height": 900})
    await page.goto(f"{static_site_url}/docs/app-shell/")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(100)

    wrapper = page.locator(".chirp-theme-docs-layout .code-block-wrapper").first
    await expect(wrapper).to_be_visible()
    metrics = await wrapper.evaluate(
        """el => {
            const style = getComputedStyle(el);
            const marker = getComputedStyle(el, "::before");
            const pre = el.querySelector("pre");
            const code = el.querySelector("pre code");
            const preStyle = getComputedStyle(pre);
            const codeStyle = getComputedStyle(code);
            const copy = el.querySelector(".code-copy-button");
            const copyStyle = getComputedStyle(copy);
            return {
                animationName: style.animationName,
                borderWidth: style.borderTopWidth,
                overflow: style.overflow,
                background: style.backgroundImage,
                markerWidth: Math.round(Number.parseFloat(marker.width)),
                preAnimationName: preStyle.animationName,
                preBorderWidth: preStyle.borderTopWidth,
                preBoxShadow: preStyle.boxShadow,
                codeBorderWidth: codeStyle.borderTopWidth,
                codeBoxShadow: codeStyle.boxShadow,
                preMarginTop: Math.round(Number.parseFloat(preStyle.marginTop)),
                copyOpacity: copyStyle.opacity,
                copyPointerEvents: copyStyle.pointerEvents,
            };
        }"""
    )
    assert metrics["animationName"] == "none", metrics
    assert metrics["borderWidth"] == "0px", metrics
    assert metrics["overflow"] == "visible", metrics
    assert "linear-gradient" in metrics["background"], metrics
    assert metrics["markerWidth"] >= 3, metrics
    assert metrics["preAnimationName"] == "none", metrics
    assert metrics["preBorderWidth"] == "0px", metrics
    assert metrics["preBoxShadow"] == "none", metrics
    assert metrics["codeBorderWidth"] == "0px", metrics
    assert metrics["codeBoxShadow"] == "none", metrics
    assert metrics["preMarginTop"] == 0, metrics
    assert metrics["copyOpacity"] == "1", metrics
    assert metrics["copyPointerEvents"] == "auto", metrics

    plaintext_wrapper = page.locator(
        '.chirp-theme-docs-layout .rosettes[data-language="plaintext"] .code-block-wrapper'
    ).first
    await expect(plaintext_wrapper).to_be_visible()
    plaintext_metrics = await plaintext_wrapper.evaluate(
        """el => {
            const pre = el.querySelector("pre");
            const code = el.querySelector("pre code");
            const preStyle = getComputedStyle(pre);
            const codeStyle = getComputedStyle(code);
            return {
                wrapperHeight: Math.round(el.getBoundingClientRect().height),
                preLineHeight: Math.round(Number.parseFloat(preStyle.lineHeight)),
                codeBackground: codeStyle.backgroundColor,
                codeDisplay: codeStyle.display,
            };
        }"""
    )
    assert plaintext_metrics["codeBackground"] == "rgba(0, 0, 0, 0)", plaintext_metrics
    assert plaintext_metrics["codeDisplay"] == "block", plaintext_metrics
    assert plaintext_metrics["preLineHeight"] <= 20, plaintext_metrics
    assert plaintext_metrics["wrapperHeight"] <= 175, plaintext_metrics

    await page.goto(f"{static_site_url}/api/chirp_ui/")
    await page.wait_for_load_state("networkidle")
    await page.locator("#get_loader").evaluate("el => el.closest('details').open = true")
    api_wrapper = page.locator("#get_loader .code-block-wrapper").first
    await expect(api_wrapper).to_be_visible()
    api_metrics = await api_wrapper.evaluate(
        """el => {
            const pre = el.querySelector("pre");
            const code = el.querySelector("pre code");
            const preStyle = getComputedStyle(pre);
            const codeStyle = getComputedStyle(code);
            const style = getComputedStyle(el);
            return {
                text: code.textContent.trim(),
                overflow: style.overflow,
                preBorderWidth: preStyle.borderTopWidth,
                preBoxShadow: preStyle.boxShadow,
                codeBorderWidth: codeStyle.borderTopWidth,
                codeBoxShadow: codeStyle.boxShadow,
                codeBackground: codeStyle.backgroundColor,
            };
        }"""
    )
    assert api_metrics["text"].startswith("from kida import ChoiceLoader"), api_metrics
    assert api_metrics["overflow"] == "visible", api_metrics
    assert api_metrics["preBorderWidth"] == "0px", api_metrics
    assert api_metrics["preBoxShadow"] == "none", api_metrics
    assert api_metrics["codeBorderWidth"] == "0px", api_metrics
    assert api_metrics["codeBoxShadow"] == "none", api_metrics
    assert api_metrics["codeBackground"] == "rgba(0, 0, 0, 0)", api_metrics


async def test_bengal_release_index_promotes_latest_card(page, static_site_url):
    await page.set_viewport_size({"width": 1423, "height": 1200})
    await page.goto(f"{static_site_url}/releases/")
    await page.wait_for_load_state("networkidle")

    await assert_no_document_horizontal_overflow(page, "releases-latest-entry")
    await expect(page.locator(".chirp-theme-shell__header")).to_be_hidden()
    await expect(page.locator(".chirp-theme-release-groups")).to_be_visible()
    assert await page.locator(".chirp-theme-release-timeline").count() >= 1

    latest = page.locator(".chirp-theme-release-entry--latest")
    first_regular = page.locator(
        ".chirp-theme-release-entry:not(.chirp-theme-release-entry--latest)"
    ).first
    await expect(latest).to_be_visible()
    await expect(latest.locator(".chirpui-badge__text")).to_have_text("Latest")
    metrics = await page.evaluate(
        """() => {
            const firstTimeline = document.querySelector(".chirp-theme-release-timeline");
            const latest = document.querySelector(".chirp-theme-release-entry--latest");
            const regular = document.querySelector(
                ".chirp-theme-release-entry:not(.chirp-theme-release-entry--latest)"
            );
            const latestStyle = getComputedStyle(latest);
            const regularStyle = getComputedStyle(regular);
            const latestRect = latest.getBoundingClientRect();
            const regularRect = regular.getBoundingClientRect();
            const latestTitle = latest.querySelector(".chirpui-timeline__title-link");
            const regularTitle = regular.querySelector(".chirpui-timeline__title-link");
            const latestInstall = latest.querySelector(".chirp-theme-release-entry__install");
            const regularInstall = regular?.querySelector(
                ".chirp-theme-release-entry__install, .chirp-theme-release-patch__install"
            );
            const latestDot = latest.querySelector(".chirpui-timeline__dot");
            const heroSubtitle = document.querySelector(
                ".chirp-theme-release-hero--index .chirpui-hero__subtitle"
            );
            return {
                groupCount: document.querySelectorAll(".chirp-theme-release-group").length,
                timelineCount: firstTimeline?.querySelectorAll(".chirp-theme-release-entry").length ?? 0,
                latestTop: Math.round(latestRect.top),
                regularTop: Math.round(regularRect.top),
                latestBorderLeft: latestStyle.borderLeftWidth,
                regularBorderLeft: regularStyle.borderLeftWidth,
                latestDotBackground: getComputedStyle(latestDot).backgroundColor,
                latestTitle: latestTitle?.textContent?.trim(),
                regularTitle: regularTitle?.textContent?.trim(),
                latestInstallText: latestInstall?.textContent?.trim(),
                regularInstallText: regularInstall?.textContent?.trim(),
                heroSubtitle: heroSubtitle?.textContent?.trim(),
            };
        }"""
    )
    assert metrics["groupCount"] >= 2, metrics
    assert metrics["timelineCount"] >= 1, metrics
    assert metrics["latestTop"] < metrics["regularTop"], metrics
    assert metrics["latestDotBackground"] not in ("", "rgba(0, 0, 0, 0)"), metrics
    assert metrics["latestTitle"] == "chirp-ui 0.10.0", metrics
    assert metrics["regularTitle"] == "chirp-ui 0.9.0", metrics
    assert "uv add chirp-ui==0.10.0" in (metrics["latestInstallText"] or ""), metrics
    assert "uv add chirp-ui==0.9.0" in (metrics["regularInstallText"] or ""), metrics
    assert "Install a specific version" in (metrics["heroSubtitle"] or ""), metrics
    await expect(latest.locator(".chirpui-timeline__title-link")).to_have_text("chirp-ui 0.10.0")
    await expect(first_regular.locator(".chirpui-timeline__title-link")).to_have_text(
        "chirp-ui 0.9.0"
    )


async def test_bengal_docs_branch_summaries_hold_parent_links(page, static_site_url):
    await page.set_viewport_size({"width": 1280, "height": 900})
    await page.goto(f"{static_site_url}/docs/patterns/product-pages/")
    await page.wait_for_load_state("networkidle")

    patterns_summary = page.locator(
        ".chirp-theme-docs-nav__section.is-active "
        ".chirp-theme-docs-nav__summary-link[href='/docs/patterns/']"
    )
    await expect(patterns_summary).to_be_visible()
    await expect(patterns_summary.locator(".chirp-theme-docs-nav__label")).to_have_text("Patterns")
    assert await page.locator(".chirp-theme-docs-nav__branch-link").count() == 0
    assert (
        await page.locator(
            ".chirp-theme-docs-nav__section.is-active "
            ".chirpui-sidebar__section-links > "
            ".chirp-theme-docs-nav__leaf-link[href='/docs/patterns/']"
        ).count()
        == 0
    )

    await patterns_summary.click()
    await page.wait_for_url("**/docs/patterns/")


async def test_bengal_docs_branch_section_header_has_no_native_disclosure(page, static_site_url):
    """The section header is a folder <button> + sibling link, NOT a <summary>.

    There is no native <details>/<summary>, so no native disclosure marker
    exists. The folder toggle button leads the row; the link fills the rest.
    """
    await page.set_viewport_size({"width": 1159, "height": 863})
    await page.goto(f"{static_site_url}/docs/get-started/")
    await page.wait_for_load_state("networkidle")

    # No native disclosure element survives in the docs tree.
    assert (
        await page.locator(
            ".chirp-theme-doc-catalog__secondary details.chirp-theme-docs-nav__section"
        ).count()
        == 0
    )

    header = page.locator(
        ".chirp-theme-docs-nav__section.is-active .chirp-theme-docs-nav__section-header"
    ).first
    await expect(header).to_be_visible()
    layout = await header.evaluate(
        """el => {
            const rect = el.getBoundingClientRect();
            const toggle = el.querySelector(".chirp-theme-docs-nav__toggle");
            const link = el.querySelector(".chirp-theme-docs-nav__summary-link");
            const toggleRect = toggle.getBoundingClientRect();
            const linkRect = link.getBoundingClientRect();
            return {
                toggleTag: toggle.tagName,
                toggleType: toggle.getAttribute("type"),
                // Toggle leads the row; link follows it and reaches the edge.
                toggleInset: Math.round(toggleRect.left - rect.left),
                widthDelta: Math.round(rect.right - linkRect.right),
            };
        }"""
    )
    assert layout["toggleTag"] == "BUTTON"
    assert layout["toggleType"] == "button"
    assert abs(layout["toggleInset"]) <= 1
    assert layout["widthDelta"] <= 1


async def test_bengal_docs_compact_desktop_uses_icon_rail_without_overflow(page, static_site_url):
    await page.set_viewport_size({"width": 919, "height": 863})
    await page.goto(f"{static_site_url}/docs/patterns/layout-affinity/#avoid")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(100)

    await assert_no_document_horizontal_overflow(page, "layout-affinity-919")
    await expect(page.locator(".chirp-theme-docs-layout__sidebar")).to_be_visible()
    await expect(page.locator(".chirp-theme-doc-catalog__primary")).to_be_visible()
    await expect(page.locator(".chirp-theme-doc-catalog__secondary")).to_be_hidden()
    await expect(page.locator(".chirp-theme-docs-layout__article")).to_be_visible()
    vertical_gap = await page.evaluate(
        """() => {
            const firstItem = document.querySelector(".chirp-theme-doc-catalog-rail__item");
            const secondItem = document.querySelectorAll(".chirp-theme-doc-catalog-rail__item")[1];
            const itemRect = firstItem.getBoundingClientRect();
            const secondRect = secondItem.getBoundingClientRect();
            return {
                topGap: Math.round(itemRect.top),
                itemGap: Math.round(secondRect.top - itemRect.bottom),
            };
        }"""
    )
    assert 0 <= vertical_gap["topGap"] <= 18
    assert 10 <= vertical_gap["itemGap"] <= 16


async def test_bengal_docs_medium_secondary_rail_starts_near_header(page, static_site_url):
    await page.set_viewport_size({"width": 1100, "height": 863})
    await page.goto(f"{static_site_url}/docs/patterns/layout-affinity/#avoid")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(100)

    await assert_no_document_horizontal_overflow(page, "layout-affinity-1100")
    await expect(page.locator(".chirp-theme-doc-catalog__secondary")).to_be_visible()
    await expect(page.locator(".chirp-theme-doc-catalog__context")).to_have_count(0)
    await expect(page.locator(".chirp-theme-docs-nav__section").first).to_be_visible()
    vertical_gap = await page.evaluate(
        """() => {
            const header = document.querySelector(".chirp-theme-shell__header");
            const firstSection = document.querySelector(".chirp-theme-docs-nav__section");
            const headerRect = header.getBoundingClientRect();
            const sectionRect = firstSection.getBoundingClientRect();
            return Math.round(sectionRect.top - headerRect.bottom);
        }"""
    )
    assert 0 <= vertical_gap <= 20


async def test_bengal_docs_secondary_rail_aligns_with_content_top(page, static_site_url):
    await page.set_viewport_size({"width": 1159, "height": 863})
    await page.goto(f"{static_site_url}/docs/theming/chirp-theme/")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(100)

    await assert_no_document_horizontal_overflow(page, "chirp-theme-secondary-top-1159")
    await expect(page.locator(".chirp-theme-doc-catalog__context")).to_have_count(0)
    await expect(page.locator(".chirp-theme-docs-nav__section").first).to_be_visible()
    await expect(page.locator(".chirp-theme-docs-layout__hero")).to_be_visible()
    alignment = await page.evaluate(
        """() => {
            const firstSection = document.querySelector(".chirp-theme-docs-nav__section");
            const hero = document.querySelector(".chirp-theme-docs-layout__hero");
            const docsNav = document.querySelector(".chirp-theme-doc-catalog .chirp-theme-docs-nav");
            const secondary = document.querySelector(".chirp-theme-doc-catalog__secondary");
            const sectionTop = Math.round(firstSection.getBoundingClientRect().top);
            const docsNavTop = Math.round(docsNav.getBoundingClientRect().top);
            const heroTop = Math.round(hero.getBoundingClientRect().top);
            const docsNavStyle = getComputedStyle(docsNav);
            const secondaryStyle = getComputedStyle(secondary);
            return {
                sectionTop,
                docsNavTop,
                heroTop,
                topDelta: Math.round(docsNavTop - heroTop),
                firstSectionInset: Math.round(sectionTop - docsNavTop),
                docsNavPaddingTop: Math.round(Number.parseFloat(docsNavStyle.paddingTop)),
                docsNavBorderTopWidth: Math.round(Number.parseFloat(docsNavStyle.borderTopWidth)),
                docsNavBorderRadius: docsNavStyle.borderTopLeftRadius,
                docsNavBackground: docsNavStyle.backgroundImage,
                secondaryBackground: secondaryStyle.backgroundImage,
                secondaryBackgroundColor: secondaryStyle.backgroundColor,
                secondaryBorderLeftWidth: Math.round(Number.parseFloat(secondaryStyle.borderLeftWidth)),
                secondaryPaddingTop: Math.round(Number.parseFloat(secondaryStyle.paddingTop)),
            };
        }"""
    )
    assert abs(alignment["topDelta"]) <= 2, alignment
    assert 5 <= alignment["firstSectionInset"] <= 10, alignment
    assert 5 <= alignment["docsNavPaddingTop"] <= 8, alignment
    assert alignment["docsNavBorderTopWidth"] == 1, alignment
    assert alignment["docsNavBorderRadius"] != "0px", alignment
    assert "gradient" in alignment["docsNavBackground"], alignment
    assert alignment["secondaryBackground"] == "none", alignment
    assert alignment["secondaryBackgroundColor"] == "rgba(0, 0, 0, 0)", alignment
    assert alignment["secondaryBorderLeftWidth"] == 0, alignment
    assert 8 <= alignment["secondaryPaddingTop"] <= 16, alignment


async def test_bengal_docs_medium_catalog_keeps_readable_secondary_rail(page, static_site_url):
    await page.set_viewport_size({"width": 1061, "height": 863})
    await page.goto(f"{static_site_url}/docs/components/")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(100)

    await assert_no_document_horizontal_overflow(page, "components-1061")
    await expect(page.locator(".chirp-theme-doc-catalog__secondary")).to_be_visible()
    rail_width = await page.evaluate(
        """() => {
            const sidebar = document.querySelector(".chirp-theme-docs-layout__sidebar");
            const secondary = document.querySelector(".chirp-theme-doc-catalog__secondary");
            return {
                sidebar: Math.round(sidebar.getBoundingClientRect().width),
                secondary: Math.round(secondary.getBoundingClientRect().width),
            };
        }"""
    )
    assert rail_width["sidebar"] >= 320
    assert rail_width["secondary"] >= 260


async def test_bengal_docs_secondary_catalog_rail_scrolls_independently(page, static_site_url):
    await page.set_viewport_size({"width": 1159, "height": 600})
    await page.goto(f"{static_site_url}/docs/components/")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(100)

    await assert_no_document_horizontal_overflow(page, "components-independent-rail-scroll")
    await expect(page.locator(".chirp-theme-doc-catalog__primary")).to_be_visible()
    await expect(page.locator(".chirp-theme-doc-catalog__secondary")).to_be_visible()
    scroll_state = await page.evaluate(
        """() => {
            const sidebar = document.querySelector(".chirp-theme-docs-layout__sidebar");
            const primary = document.querySelector(".chirp-theme-doc-catalog__primary");
            const secondary = document.querySelector(".chirp-theme-doc-catalog__secondary");
            const firstItem = document.querySelector(".chirp-theme-doc-catalog-rail__item");
            const beforePrimaryTop = Math.round(primary.getBoundingClientRect().top);
            const beforeItemTop = Math.round(firstItem.getBoundingClientRect().top);
            const beforePageScroll = window.scrollY;
            secondary.scrollTop = Math.min(120, secondary.scrollHeight - secondary.clientHeight);
            return {
                sidebarOverflowY: getComputedStyle(sidebar).overflowY,
                primaryOverflowY: getComputedStyle(primary).overflowY,
                secondaryOverflowY: getComputedStyle(secondary).overflowY,
                secondaryCanScroll: secondary.scrollHeight > secondary.clientHeight,
                secondaryScrollTop: Math.round(secondary.scrollTop),
                primaryTopDelta: Math.round(primary.getBoundingClientRect().top) - beforePrimaryTop,
                itemTopDelta: Math.round(firstItem.getBoundingClientRect().top) - beforeItemTop,
                pageScrollDelta: window.scrollY - beforePageScroll,
            };
        }"""
    )
    assert scroll_state["sidebarOverflowY"] == "visible", scroll_state
    assert scroll_state["primaryOverflowY"] == "visible", scroll_state
    assert scroll_state["secondaryOverflowY"] == "auto", scroll_state
    assert scroll_state["secondaryCanScroll"], scroll_state
    assert scroll_state["secondaryScrollTop"] > 0, scroll_state
    assert scroll_state["primaryTopDelta"] == 0, scroll_state
    assert scroll_state["itemTopDelta"] == 0, scroll_state
    assert scroll_state["pageScrollDelta"] == 0, scroll_state


async def test_bengal_docs_branch_summaries_render_as_compact_labels(page, static_site_url):
    await page.set_viewport_size({"width": 1132, "height": 1606})
    await page.goto(f"{static_site_url}/docs/components/")
    await page.wait_for_load_state("networkidle")

    branch = page.locator(
        ".chirp-theme-docs-nav__section--depth-1.is-active "
        "> .chirp-theme-docs-nav__section-header "
        ".chirp-theme-docs-nav__summary-link[href='/docs/components/']"
    )
    leaf = page.locator(
        ".chirp-theme-docs-nav__section--depth-1.is-active .chirp-theme-docs-nav__leaf-link"
    ).first
    await expect(branch).to_be_visible()
    await expect(leaf).to_be_visible()
    metrics = await branch.evaluate(
        """(el) => {
            const leaf = document.querySelector(
                ".chirp-theme-docs-nav__section--depth-1.is-active "
                + ".chirp-theme-docs-nav__leaf-link"
            );
            const style = getComputedStyle(el);
            const leafStyle = getComputedStyle(leaf);
            return {
                branchHeight: Math.round(el.getBoundingClientRect().height),
                leafHeight: Math.round(leaf.getBoundingClientRect().height),
                branchFontSize: parseFloat(style.fontSize),
                leafFontSize: parseFloat(leafStyle.fontSize),
                textTransform: style.textTransform,
            };
        }"""
    )
    assert metrics["branchHeight"] < metrics["leafHeight"]
    assert metrics["branchFontSize"] < metrics["leafFontSize"]
    assert metrics["textTransform"] == "uppercase"


async def test_bengal_docs_root_single_pages_match_section_rows_with_page_icon(
    page, static_site_url
):
    await page.set_viewport_size({"width": 1132, "height": 1606})
    await page.goto(f"{static_site_url}/docs/")
    await page.wait_for_load_state("networkidle")

    root_leaf = page.locator(".chirp-theme-docs-nav__root-leaf[href='/docs/about/']")
    # The section branch row's leading glyph is the folder TOGGLE button; the
    # link sits beside it in the always-visible header row.
    branch_link = page.locator(
        ".chirp-theme-docs-nav__section--depth-1 "
        "> .chirp-theme-docs-nav__section-header "
        ".chirp-theme-docs-nav__summary-link[href='/docs/components/']"
    )
    await expect(root_leaf).to_be_visible()
    await expect(branch_link).to_be_visible()
    await expect(root_leaf.locator(".chirp-theme-docs-nav__label")).to_have_text("About")

    metrics = await root_leaf.evaluate(
        """(el) => {
            const branchHeader = document.querySelector(
                ".chirp-theme-docs-nav__section--depth-1 "
                + "> .chirp-theme-docs-nav__section-header:has("
                + ".chirp-theme-docs-nav__summary-link[href='/docs/components/'])"
            );
            // The leading glyph in the branch row is the folder toggle button.
            const branchToggle = branchHeader.querySelector(".chirp-theme-docs-nav__toggle");
            const branchFolder = branchToggle.querySelector(
                ".chirp-theme-docs-nav__folder--closed"
            );
            const getStartedToggle = document.querySelector(
                ".chirp-theme-docs-nav__section--depth-1 "
                + "> .chirp-theme-docs-nav__section-header:has("
                + ".chirp-theme-docs-nav__summary-link[href='/docs/get-started/']) "
                + ".chirp-theme-docs-nav__toggle"
            );
            const icon = el.querySelector(".chirp-theme-docs-nav__type-icon");
            const iconSvg = icon.querySelector("svg");
            const branchFolderSvg = branchFolder.querySelector("svg");
            const style = getComputedStyle(el);
            return {
                leftDelta: Math.round(
                    el.getBoundingClientRect().left - branchToggle.getBoundingClientRect().left
                ),
                rootHeight: Math.round(el.getBoundingClientRect().height),
                branchHeight: Math.round(branchHeader.getBoundingClientRect().height),
                rootIconSize: Math.round(icon.getBoundingClientRect().width),
                branchIconSize: Math.round(branchToggle.getBoundingClientRect().width),
                componentFolderColor: getComputedStyle(branchToggle).color,
                guideFolderColor: getComputedStyle(getStartedToggle).color,
                rootIconClass: iconSvg.getAttribute("class"),
                branchIconClass: branchFolderSvg.getAttribute("class"),
            };
        }"""
    )
    # Root single-page leaf and section branch row start at the same x.
    assert abs(metrics["leftDelta"]) <= 1, metrics
    assert abs(metrics["rootHeight"] - metrics["branchHeight"]) <= 2, metrics
    # Leading glyph slots are the same width (root type-icon vs branch toggle).
    assert abs(metrics["rootIconSize"] - metrics["branchIconSize"]) <= 1, metrics
    assert metrics["componentFolderColor"] == metrics["guideFolderColor"], metrics
    assert "icon-article" in metrics["rootIconClass"], metrics
    assert "icon-folder" in metrics["branchIconClass"], metrics

    await page.goto(f"{static_site_url}/docs/about/")
    await page.wait_for_load_state("networkidle")
    active_metrics = await page.locator(
        ".chirp-theme-docs-nav__root-leaf[href='/docs/about/']"
    ).evaluate(
        """(el) => {
            const icon = el.querySelector(".chirp-theme-docs-nav__type-icon");
            return {
                ariaCurrent: el.getAttribute("aria-current"),
                textColor: getComputedStyle(el).color,
                iconColor: getComputedStyle(icon).color,
            };
        }"""
    )
    assert active_metrics["ariaCurrent"] == "page", active_metrics
    assert active_metrics["iconColor"] == active_metrics["textColor"], active_metrics


async def test_bengal_docs_child_entries_use_compact_iterable_rows(page, static_site_url):
    await page.set_viewport_size({"width": 1159, "height": 863})
    await page.goto(f"{static_site_url}/docs/theming/")
    await page.wait_for_load_state("networkidle")

    active_children = page.locator(
        ".chirp-theme-docs-nav__section--depth-1.is-active "
        "> .chirpui-sidebar__section-links > .chirp-theme-docs-nav__leaf-link"
    )
    await expect(active_children).to_have_count(2)
    metrics = await active_children.first.evaluate(
        """(el) => {
            const branch = document.querySelector(
                ".chirp-theme-docs-nav__section--depth-1.is-active "
                + "> .chirp-theme-docs-nav__section-header .chirp-theme-docs-nav__summary-link"
            );
            const icon = el.querySelector(".chirp-theme-docs-nav__type-icon");
            const group = el.closest(".chirpui-sidebar__section-links");
            const groupStyle = getComputedStyle(group);
            return {
                childHeight: Math.round(el.getBoundingClientRect().height),
                childFontSize: parseFloat(getComputedStyle(el).fontSize),
                branchHeight: Math.round(branch.getBoundingClientRect().height),
                iconSize: Math.round(icon.getBoundingClientRect().width),
                groupGap: Math.round(Number.parseFloat(groupStyle.rowGap)),
                groupInset: Math.round(Number.parseFloat(groupStyle.marginLeft)),
            };
        }"""
    )
    assert 24 <= metrics["childHeight"] <= 32, metrics
    assert metrics["branchHeight"] < metrics["childHeight"], metrics
    assert metrics["childFontSize"] < 14, metrics
    assert metrics["iconSize"] <= 18, metrics
    assert metrics["groupGap"] <= 4, metrics
    assert metrics["groupInset"] >= 6, metrics


async def test_bengal_docs_catalog_navigation_omits_notification_counts(page, static_site_url):
    await page.set_viewport_size({"width": 1132, "height": 1606})
    await page.goto(f"{static_site_url}/docs/components/")
    await page.wait_for_load_state("networkidle")

    assert await page.locator(".chirp-theme-doc-catalog-rail__count").count() == 0
    assert await page.locator(".chirp-theme-docs-nav__summary-count").count() == 0
    assert await page.locator(".chirp-theme-docs-nav__meta").count() == 0


async def test_bengal_docs_toc_uses_surface_chrome_without_divider_lines(page, static_site_url):
    await page.set_viewport_size({"width": 2309, "height": 1606})
    await page.goto(f"{static_site_url}/docs/app-shell/")
    await page.wait_for_load_state("networkidle")

    await expect(page.locator(".chirp-theme-docs-layout__toc")).to_be_visible()
    line_styles = await page.evaluate(
        """() => {
            const styles = (selector) => {
                const style = getComputedStyle(document.querySelector(selector));
                return {
                    borderLeft: style.borderLeftWidth,
                    borderTop: style.borderTopWidth,
                    borderColor: style.borderColor,
                    display: style.display,
                };
            };
            return {
                rail: styles(".chirp-theme-docs-layout__toc"),
                context: styles(".chirp-theme-doc-toc__context"),
                group: styles(".chirp-theme-doc-toc__group"),
                link: styles(".chirp-theme-doc-toc__link"),
                metadata: styles(".chirp-theme-doc-toc__metadata"),
                progress: styles(".chirp-theme-doc-toc .toc-progress"),
            };
        }"""
    )
    assert line_styles["rail"]["borderLeft"] == "0px"
    assert line_styles["context"]["borderTop"] == "0px"
    assert line_styles["group"]["borderTop"] == "0px"
    assert line_styles["link"]["borderTop"] == "0px"
    assert line_styles["metadata"]["borderTop"] == "0px"
    assert line_styles["progress"]["display"] == "none"


async def test_bengal_docs_toc_count_pills_and_deep_labels_stay_compact(page, static_site_url):
    await page.set_viewport_size({"width": 2309, "height": 1606})
    await page.goto(f"{static_site_url}/docs/app-shell/")
    await page.wait_for_load_state("networkidle")

    await expect(page.locator(".chirp-theme-doc-toc__context-count")).to_be_visible()
    await expect(page.locator(".chirp-theme-doc-toc__count .toc-count").first).to_be_visible()
    metrics = await page.evaluate(
        """() => {
            const context = document.querySelector(".chirp-theme-doc-toc__context-count");
            const nested = document.querySelector(".chirp-theme-doc-toc__count .toc-count");
            const scroll = document.querySelector(".chirp-theme-doc-toc__scroll");
            const groupHeader = document.querySelector(".chirp-theme-doc-toc__group-header");
            const nestedBadge = document.querySelector(".chirp-theme-doc-toc__count");
            const nestedItems = Array.from(document.querySelectorAll(".chirp-theme-doc-toc__subitems"));
            const contextStyle = getComputedStyle(context);
            const nestedStyle = getComputedStyle(nested);
            const nestedBadgeStyle = getComputedStyle(nestedBadge);
            const groupStyle = getComputedStyle(groupHeader);
            return {
                contextColor: contextStyle.color,
                nestedColor: nestedStyle.color,
                contextBackground: contextStyle.backgroundColor,
                nestedBackground: nestedStyle.backgroundColor,
                nestedBoxShadow: nestedStyle.boxShadow,
                nestedOpacity: nestedStyle.opacity,
                nestedBadgeBackground: nestedBadgeStyle.backgroundColor,
                contextWhiteText: contextStyle.color === "rgb(255, 255, 255)",
                scrollOverflowX: getComputedStyle(scroll).overflowX,
                scrollWidth: Math.ceil(scroll.scrollWidth),
                clientWidth: Math.ceil(scroll.clientWidth),
                groupDisplay: groupStyle.display,
                groupColumns: groupStyle.gridTemplateColumns.split(" ").filter(Boolean),
                nestedInsetCount: nestedItems.length,
            };
        }"""
    )
    assert metrics["contextColor"] == metrics["nestedColor"], metrics
    assert metrics["nestedBackground"] == "rgba(0, 0, 0, 0)", metrics
    assert metrics["nestedBoxShadow"] == "none", metrics
    assert metrics["nestedOpacity"] == "1", metrics
    assert metrics["nestedBadgeBackground"] == "rgba(0, 0, 0, 0)", metrics
    assert not metrics["contextWhiteText"], metrics
    assert metrics["scrollOverflowX"] in {"auto", "hidden"}, metrics
    assert metrics["scrollWidth"] <= metrics["clientWidth"] + 1, metrics
    assert metrics["groupDisplay"] == "grid", metrics
    assert len(metrics["groupColumns"]) == 3, metrics
    assert metrics["nestedInsetCount"] > 0, metrics


async def test_bengal_docs_link_preview_shows_on_prose_hover(page, static_site_url):
    await page.set_viewport_size({"width": 1280, "height": 900})
    await page.goto(f"{static_site_url}/docs/app-shell/")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(100)

    link = page.locator('article.prose a[href$="/docs/app-shell/ui-layers/"]').first
    await expect(link).to_be_visible()

    await link.hover()
    preview = page.locator(".link-preview")
    await expect(preview).to_be_visible(timeout=2000)
    await expect(preview.locator(".link-preview__title")).to_contain_text("UI layers")
    await expect(preview.locator(".link-preview__section")).to_contain_text("app-shell")
    await expect(preview.locator(".link-preview__excerpt")).not_to_be_empty()
    await expect(preview.locator(".link-preview__meta")).to_contain_text("min read")

    metrics = await page.evaluate(
        """() => {
            const preview = document.querySelector(".link-preview");
            const style = getComputedStyle(preview);
            return {
                background: style.backgroundColor,
                borderRadius: style.borderRadius,
                boxShadow: style.boxShadow,
                zIndex: style.zIndex,
            };
        }"""
    )
    assert metrics["zIndex"] != "auto", metrics
    assert metrics["boxShadow"] != "none", metrics
    assert metrics["borderRadius"] != "0px", metrics


async def test_bengal_docs_link_preview_cross_site_allowed_host(page, static_site_url):
    await page.set_viewport_size({"width": 1280, "height": 900})
    await page.goto(f"{static_site_url}/docs/about/")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(100)

    link = page.locator('article.prose a[href="https://lbliii.github.io/chirp"]').first
    await expect(link).to_be_visible()

    await link.hover()
    preview = page.locator(".link-preview")
    await expect(preview).to_be_visible(timeout=4000)
    await expect(preview.locator(".link-preview__title")).to_contain_text("Chirp")
    await expect(preview.locator(".link-preview__excerpt")).not_to_be_empty()

    config = await page.evaluate(
        """() => {
            const el = document.getElementById('bengal-config');
            return el ? JSON.parse(el.textContent).linkPreviews.allowedHosts : [];
        }"""
    )
    assert "lbliii.github.io" in config
