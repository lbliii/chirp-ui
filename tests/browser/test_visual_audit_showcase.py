from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[2]
SHOWCASE = REPO_ROOT / "examples" / "design-system-gap-showcase" / "index.html"

VIEWPORTS = [
    pytest.param(320, 640, id="phone-320"),
    pytest.param(390, 844, id="phone-390"),
    pytest.param(768, 1024, id="tablet"),
    pytest.param(1440, 900, id="desktop"),
]


@pytest.fixture
def page():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context()
        page = ctx.new_page()
        yield page
        ctx.close()
        browser.close()


def open_visual_audit(page, width: int, height: int) -> None:
    page.set_viewport_size({"width": width, "height": height})
    page.goto(SHOWCASE.as_uri())
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(100)


def assert_no_document_horizontal_overflow(page, label: str) -> None:
    result = page.evaluate(
        """() => {
            const root = document.documentElement;
            const overflow = Math.ceil(root.scrollWidth - root.clientWidth);
            if (overflow <= 1) return { overflow, offenders: [] };

            const viewport = root.clientWidth;
            const offenders = [...document.body.querySelectorAll("*")]
                .filter((el) => {
                    const style = getComputedStyle(el);
                    const rect = el.getBoundingClientRect();
                    return style.display !== "none"
                        && style.visibility !== "hidden"
                        && rect.width > 0
                        && rect.height > 0
                        && (rect.right > viewport + 1 || rect.left < -1);
                })
                .slice(0, 8)
                .map((el) => ({
                    tag: el.tagName.toLowerCase(),
                    className: el.className,
                    text: (el.textContent || "").trim().slice(0, 80),
                    rect: (() => {
                        const r = el.getBoundingClientRect();
                        return { left: r.left, right: r.right, width: r.width };
                    })(),
                }));
            return { overflow, offenders };
        }"""
    )

    assert result["overflow"] <= 1, {label: result}


@pytest.mark.parametrize(("width", "height"), VIEWPORTS)
def test_visual_audit_has_no_document_horizontal_overflow(page, width, height):
    open_visual_audit(page, width, height)

    assert_no_document_horizontal_overflow(page, f"visual-audit-{width}x{height}")


@pytest.mark.parametrize(("width", "height"), VIEWPORTS)
def test_visual_audit_core_sections_are_visible(page, width, height):
    open_visual_audit(page, width, height)

    for selector in [
        "#tokens",
        "[data-audit-section='token-explorer']",
        "#navigation",
        "#components",
        "[data-audit-section='interaction-chrome']",
        "[data-audit-section='ascii-tui']",
        "[data-audit-section='proof-patterns']",
        "[data-audit-section='theme-gallery']",
    ]:
        box = page.locator(selector).bounding_box()
        assert box is not None, selector
        assert box["width"] > 0, selector
        assert box["height"] > 0, selector


def test_visual_audit_gap_families_render(page):
    open_visual_audit(page, 768, 1024)

    expectations = {
        "[data-audit-section='interaction-chrome'] .chirpui-command-palette__item": 2,
        "[data-audit-section='interaction-chrome'] .chirpui-modal__header": 1,
        "[data-audit-section='interaction-chrome'] .chirpui-drawer__header": 1,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-7seg": 1,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-badge": 1,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-border": 2,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-breaker-panel": 1,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-card": 1,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-checkbox": 2,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-divider": 1,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-empty": 1,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-error": 1,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-fader": 1,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-indicator": 2,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-knob": 1,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-modal": 1,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-progress": 1,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-radio": 2,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-radio-group": 1,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-skeleton": 1,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-sparkline": 1,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-spinner": 1,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-switch": 2,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-stepper": 1,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-tab": 2,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-tabs": 1,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-ticker": 1,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-tile-btn": 2,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-toggle": 2,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-table__row": 3,
        "[data-audit-section='ascii-tui'] .chirpui-ascii-vu": 1,
        "[data-audit-section='ascii-tui'] .chirpui-split-flap": 1,
        "[data-audit-section='proof-patterns'] .chirpui-logo-cloud__item": 3,
        "[data-audit-section='proof-patterns'] .chirpui-story-card": 1,
        "[data-audit-section='proof-patterns'] .chirpui-cta-band": 1,
    }

    for selector, count in expectations.items():
        assert page.locator(selector).count() == count, selector


def test_visual_audit_ascii_native_controls_change_checked_state(page):
    open_visual_audit(page, 768, 1024)

    section = page.locator("[data-audit-section='ascii-tui']")

    watch = section.locator(".chirpui-ascii-checkbox").nth(1)
    watch.click()
    assert section.locator("#audit-watch").is_checked()

    switch = section.locator(".chirpui-ascii-switch")
    switch.click()
    assert not section.locator(".chirpui-ascii-switch__input").is_checked()

    section.locator(".chirpui-ascii-radio").nth(1).click()
    assert section.locator("input[name='audit-channel'][value='stable']").is_checked()

    section.locator(".chirpui-ascii-knob__position").nth(2).click()
    assert section.locator("input[name='audit-traffic'][value='100']").is_checked()


def test_visual_audit_interaction_previews_use_scoped_component_roots(page):
    open_visual_audit(page, 768, 1024)

    assert page.locator(".audit-modal-preview dialog.chirpui-modal[open]").count() == 1
    assert page.locator(".audit-drawer-preview dialog.chirpui-drawer[open]").count() == 1

    command_item = page.locator(".audit-command-preview .chirpui-command-palette__item").nth(0)
    command_style = command_item.evaluate(
        """(el) => {
            const style = getComputedStyle(el);
            return {
                borderTopWidth: style.borderTopWidth,
                display: style.display,
                justifyContent: style.justifyContent,
            };
        }"""
    )
    assert command_style == {
        "borderTopWidth": "0px",
        "display": "flex",
        "justifyContent": "space-between",
    }

    modal_style = page.locator(".audit-modal-preview dialog.chirpui-modal").evaluate(
        """(el) => {
            const style = getComputedStyle(el);
            const close = getComputedStyle(el.querySelector(".chirpui-modal__close"));
            return {
                borderTopStyle: style.borderTopStyle,
                paddingTop: style.paddingTop,
                closeFontSize: close.fontSize,
            };
        }"""
    )
    assert modal_style["borderTopStyle"] == "solid"
    assert modal_style["paddingTop"] == "0px"
    assert float(modal_style["closeFontSize"].replace("px", "")) >= 20

    drawer_alignment = page.locator(".audit-drawer-preview").evaluate(
        """(el) => {
            const panel = el.querySelector(".chirpui-drawer__panel");
            const style = getComputedStyle(el);
            const outer = el.getBoundingClientRect();
            const inner = panel.getBoundingClientRect();
            const contentRight = outer.right - parseFloat(style.paddingRight || "0");
            return Math.abs(contentRight - inner.right);
        }"""
    )
    assert drawer_alignment <= 1


def test_visual_audit_logo_cloud_items_have_internal_gap(page):
    open_visual_audit(page, 768, 1024)

    gap = (
        page.locator(".chirpui-logo-cloud__item")
        .nth(0)
        .evaluate("(el) => getComputedStyle(el).gap")
    )

    assert gap != "0px"


def test_visual_audit_token_explorer_groups_first_override_jobs(page):
    open_visual_audit(page, 768, 1024)

    jobs = page.locator("[data-audit-section='token-explorer'] [data-token-job]").evaluate_all(
        "(els) => els.map((el) => el.getAttribute('data-token-job'))"
    )

    assert jobs == [
        "page",
        "surface",
        "text",
        "accent",
        "semantic",
        "focus",
        "radius",
        "elevation",
        "typography",
        "motion",
    ]

    assert page.locator("[data-audit-section='token-explorer'] .audit-token-row").count() >= 20


def test_visual_audit_theme_gallery_profiles_render(page):
    open_visual_audit(page, 768, 1024)

    gallery = page.locator("[data-audit-section='theme-gallery']")
    assert gallery.locator(".audit-profile--default").count() == 1
    assert gallery.locator(".audit-profile").count() == 1
    assert gallery.locator(".audit-dark").count() == 1
    assert gallery.locator(".audit-profile--holy").count() == 1
    assert gallery.locator(".audit-profile--chirp-theme").count() == 1

    for selector in [
        ".audit-profile--default .chirpui-btn--primary",
        ".audit-profile .chirpui-btn--primary",
        ".audit-dark .chirpui-btn--primary",
        ".audit-profile--holy .chirpui-btn--primary",
        ".audit-profile--chirp-theme .chirpui-btn--primary",
    ]:
        box = page.locator(selector).bounding_box()
        assert box is not None, selector
        assert box["width"] >= 40, selector
        assert box["height"] >= 30, selector


def test_visual_audit_theme_profiles_define_public_semantic_tokens(page):
    open_visual_audit(page, 768, 1024)

    profiles = page.locator("[data-theme-profile]").evaluate_all(
        """(els) => els.map((el) => {
            const style = getComputedStyle(el);
            const tokens = [
                "--chirpui-bg",
                "--chirpui-surface",
                "--chirpui-border",
                "--chirpui-text",
                "--chirpui-text-muted",
                "--chirpui-accent",
                "--chirpui-success",
                "--chirpui-warning",
                "--chirpui-error",
            ];
            return {
                profile: el.getAttribute("data-theme-profile"),
                missing: tokens.filter((token) => style.getPropertyValue(token).trim() === ""),
            };
        })"""
    )

    assert {profile["profile"] for profile in profiles} == {
        "default",
        "app-starter-light",
        "app-starter-dark",
        "holy-light",
        "chirp-theme",
    }
    assert all(profile["missing"] == [] for profile in profiles), profiles


def test_visual_audit_dark_profile_titles_inherit_dark_text(page):
    open_visual_audit(page, 768, 1024)

    dark_titles = page.locator(".audit-dark .audit-title").evaluate_all(
        """(els) => els.map((el) => {
            const style = getComputedStyle(el);
            return { color: style.color, backgroundColor: getComputedStyle(el.closest(".audit-dark")).backgroundColor };
        })"""
    )

    assert dark_titles
    for title in dark_titles:
        assert title["color"] != "rgb(0, 0, 0)", title
        assert title["color"] != title["backgroundColor"], title


def test_visual_audit_long_route_label_is_contained_by_scroll_strip(page):
    open_visual_audit(page, 320, 640)

    failure = page.locator(".chirpui-route-tabs").evaluate(
        """(el) => {
            const rect = el.getBoundingClientRect();
            const viewport = document.documentElement.clientWidth;
            const style = getComputedStyle(el);
            const contained = rect.left >= -1 && rect.right <= viewport + 1;
            const canScroll = el.scrollWidth > el.clientWidth;
            const scrollableOverflow = ["auto", "scroll"].includes(style.overflowX);
            if (contained && canScroll && scrollableOverflow) return null;
            return {
                overflowX: style.overflowX,
                rect: { left: rect.left, right: rect.right, width: rect.width },
                scrollWidth: el.scrollWidth,
                clientWidth: el.clientWidth,
                viewport,
            };
        }"""
    )
    assert failure is None, failure
