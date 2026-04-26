"""Responsive composition gauntlet.

This suite exercises ChirpUI as downstream apps compose it: many components
sharing one shell, dense controls in the same row, hostile labels, state
pressure, and viewport pressure from phone through desktop.
"""

import pytest

from tests.browser.conftest import wait_for_htmx
from tests.browser.gauntlet_detectors import (
    assert_common_compositions_do_not_overlap,
    assert_control_rows_keep_coherent_heights,
    assert_focused_element_has_visible_ring,
    assert_no_document_horizontal_overflow,
    assert_no_failures,
    assert_touch_critical_controls_not_tiny,
    open_gauntlet,
)

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

VIEWPORT_SPECS = [
    (320, 640, "phone-320"),
    (375, 812, "phone-375"),
    (430, 932, "phone-430"),
    (768, 1024, "tablet-portrait"),
    (1024, 768, "tablet-landscape"),
    (1280, 800, "desktop-1280"),
    (1440, 900, "desktop-1440"),
]

ROOM_PATHS = [
    "/gauntlet/primitives",
    "/gauntlet/rhythm",
    "/gauntlet/navigation",
    "/gauntlet/forms",
    "/gauntlet/data",
    "/gauntlet/workflow",
    "/gauntlet/linkability",
    "/gauntlet/contextual",
    "/gauntlet/actions",
    "/gauntlet/swaps",
    "/gauntlet/content",
    "/gauntlet/density",
    "/gauntlet/states",
    "/gauntlet/edges",
    "/gauntlet/hostile",
]

ROOM_VIEWPORTS = [
    (375, 812, "phone"),
    (1024, 768, "tablet-landscape"),
]

SCENARIOS = [
    *[
        pytest.param("/gauntlet", width, height, id=f"all-{label}")
        for width, height, label in VIEWPORT_SPECS
    ],
    *[
        pytest.param(path, width, height, id=f"{path.rsplit('/', 1)[-1]}-{name}")
        for path in ROOM_PATHS
        for width, height, name in ROOM_VIEWPORTS
    ],
]

TOUCH_SCENARIOS = [
    pytest.param("/gauntlet", 320, 640, id="all-phone-320"),
    pytest.param("/gauntlet", 375, 812, id="all-phone-375"),
    pytest.param("/gauntlet/rhythm", 375, 812, id="rhythm-phone"),
    pytest.param("/gauntlet/forms", 375, 812, id="forms-phone"),
    pytest.param("/gauntlet/data", 375, 812, id="data-phone"),
    pytest.param("/gauntlet/workflow", 375, 812, id="workflow-phone"),
    pytest.param("/gauntlet/contextual", 375, 812, id="contextual-phone"),
    pytest.param("/gauntlet/actions", 375, 812, id="actions-phone"),
    pytest.param("/gauntlet/swaps", 375, 812, id="swaps-phone"),
    pytest.param("/gauntlet/content", 375, 812, id="content-phone"),
    pytest.param("/gauntlet/density", 375, 812, id="density-phone"),
    pytest.param("/gauntlet/states", 375, 812, id="states-phone"),
    pytest.param("/gauntlet/edges", 375, 812, id="edges-phone"),
    pytest.param("/gauntlet", 768, 1024, id="all-tablet"),
]

STATE_SCENARIOS = [
    pytest.param("dark", "default", id="dark-default"),
    pytest.param("light", "default", id="light-default"),
    pytest.param("system", "plain", id="system-plain"),
]


@pytest.mark.parametrize("path", ROOM_PATHS)
async def test_gauntlet_room_routes_render_surgical_rooms(page, base_url, path):
    await open_gauntlet(page, base_url, path, width=768, height=1024)

    assert await page.locator("[data-gauntlet-room]").count() == 1
    expected_room = path.rsplit("/", 1)[-1]
    assert await page.locator(f"[data-gauntlet-room='{expected_room}']").count() == 1


@pytest.mark.parametrize(("path", "width", "height"), SCENARIOS)
async def test_gauntlet_scenarios_have_no_document_horizontal_overflow(
    page, base_url, path, width, height
):
    await open_gauntlet(page, base_url, path, width=width, height=height)

    await assert_no_document_horizontal_overflow(page, f"{path}-{width}x{height}")


@pytest.mark.parametrize(("path", "width", "height"), SCENARIOS)
async def test_gauntlet_scenarios_do_not_overlap(page, base_url, path, width, height):
    await open_gauntlet(page, base_url, path, width=width, height=height)

    await assert_common_compositions_do_not_overlap(page, f"{path}-{width}x{height}")


@pytest.mark.parametrize(("path", "width", "height"), SCENARIOS)
async def test_gauntlet_control_rows_keep_coherent_heights(page, base_url, path, width, height):
    await open_gauntlet(page, base_url, path, width=width, height=height)

    await assert_control_rows_keep_coherent_heights(page, f"{path}-{width}x{height}")


@pytest.mark.parametrize(("path", "width", "height"), TOUCH_SCENARIOS)
async def test_gauntlet_touch_critical_controls_are_not_tiny(page, base_url, path, width, height):
    await open_gauntlet(page, base_url, path, width=width, height=height)

    await assert_touch_critical_controls_not_tiny(page, f"{path}-{width}x{height}")


@pytest.mark.parametrize(("theme", "style"), STATE_SCENARIOS)
async def test_gauntlet_state_matrix_keeps_layout_contracts(page, base_url, theme, style):
    await open_gauntlet(page, base_url, "/gauntlet", width=375, height=812)
    await page.evaluate(
        """([theme, style]) => {
            document.documentElement.setAttribute("data-theme", theme);
            document.documentElement.setAttribute("data-style", style);
        }""",
        [theme, style],
    )
    await page.wait_for_timeout(100)

    label = f"state-{theme}-{style}"
    await assert_no_document_horizontal_overflow(page, label)
    await assert_common_compositions_do_not_overlap(page, label)
    await assert_control_rows_keep_coherent_heights(page, label)


@pytest.mark.parametrize("path", ["/gauntlet/forms", "/gauntlet/content", "/gauntlet/hostile"])
async def test_gauntlet_room_survives_large_text_pressure(page, base_url, path):
    await open_gauntlet(page, base_url, path, width=375, height=812)
    await page.add_style_tag(content="html { font-size: 20px !important; }")
    await page.wait_for_timeout(100)

    await assert_no_document_horizontal_overflow(page, f"{path}-large-text")


async def test_gauntlet_linked_nav_branches_route_without_disclosure_conflict(page, base_url):
    await open_gauntlet(page, base_url, "/gauntlet/navigation", width=768, height=1024)

    assert await page.locator(".chirpui-nav-tree--linked-branches summary").count() == 0
    branch = page.locator(
        ".chirpui-nav-tree--linked-branches .chirpui-nav-tree__item--branch"
        " > .chirpui-nav-tree__link"
    ).first
    href = await branch.get_attribute("href")
    assert href == "/gauntlet/workspace"
    assert await page.get_by_text("Hidden until open").count() == 0


async def test_gauntlet_file_tree_forwards_linked_branch_contract(page, base_url):
    await open_gauntlet(page, base_url, "/gauntlet/linkability", width=768, height=1024)

    tree = page.locator(".chirpui-file-tree")
    assert await tree.locator(".chirpui-nav-tree--linked-branches").count() == 1
    assert await tree.locator("summary").count() == 0
    assert (
        await tree.locator(
            ".chirpui-nav-tree__item--branch > .chirpui-nav-tree__link"
        ).first.get_attribute("href")
        == "/gauntlet/workspace"
    )
    assert await tree.get_by_text("Hidden until open").count() == 0


async def test_gauntlet_default_controls_share_height_contract(page, base_url):
    await open_gauntlet(page, base_url, "/gauntlet/rhythm", width=375, height=812)

    heights = await page.locator("[data-gauntlet-control-group='rhythm-default']").evaluate(
        """(group) => {
            const selector = [
                ":scope > .chirpui-btn",
                ":scope > .chirpui-dropdown",
                ":scope > .chirpui-ascii-toggle",
                ":scope > .chirpui-icon-btn",
                ":scope > .chirpui-segmented",
                ":scope > .chirpui-pagination",
            ].join(",");
            return [...group.querySelectorAll(selector)].map((el) => ({
                className: el.className,
                text: (el.textContent || el.getAttribute("aria-label") || "").trim().slice(0, 40),
                height: Math.round(el.getBoundingClientRect().height),
            }));
        }"""
    )
    values = [item["height"] for item in heights]
    failures = []
    if min(values) < 39 or max(values) > 41 or max(values) - min(values) > 1:
        failures.append(heights)
    await assert_no_failures(page, failures, "rhythm-default-height-contract")


@pytest.mark.parametrize(
    ("width", "height", "expected"),
    [
        pytest.param(1024, 768, 32, id="desktop-small"),
        pytest.param(375, 812, 40, id="phone-touch-small"),
    ],
)
async def test_gauntlet_small_controls_follow_context_height_contract(
    page, base_url, width, height, expected
):
    await open_gauntlet(page, base_url, "/gauntlet/rhythm", width=width, height=height)

    heights = await page.locator("[data-gauntlet-control-group='rhythm-small']").evaluate(
        """(group) => {
            const selector = [
                ":scope > .chirpui-btn",
                ":scope > .chirpui-icon-btn",
                ":scope > .chirpui-ascii-toggle",
                ":scope > .chirpui-segmented",
            ].join(",");
            return [...group.querySelectorAll(selector)].map((el) => ({
                className: el.className,
                text: (el.textContent || el.getAttribute("aria-label") || "").trim().slice(0, 40),
                height: Math.round(el.getBoundingClientRect().height),
            }));
        }"""
    )
    failures = [item for item in heights if abs(item["height"] - expected) > 1]
    await assert_no_failures(
        page,
        failures,
        f"rhythm-small-height-contract-{width}x{height}",
    )


async def test_gauntlet_timeline_title_link_mode_avoids_overlay_contract(page, base_url):
    await open_gauntlet(page, base_url, "/gauntlet/linkability", width=768, height=1024)

    data_timeline = page.locator("[data-testid='title-link-timeline']")
    slot_timeline = page.locator("[data-testid='slot-title-link-timeline']")

    assert await data_timeline.locator(".chirpui-timeline__title-link").count() == 2
    assert await data_timeline.locator(".chirpui-timeline__link-overlay").count() == 0
    assert await slot_timeline.locator(".chirpui-timeline__title-link").count() == 1
    assert await slot_timeline.locator(".chirpui-timeline__link-overlay").count() == 0


async def test_gauntlet_contextual_nav_hints_keep_route_link_focus_contract(page, base_url):
    await open_gauntlet(page, base_url, "/gauntlet/contextual", width=768, height=1024)

    nav = page.locator("[data-testid='contextual-nav']")
    hinted = nav.locator(".chirpui-nav-tree__hint").first
    link = hinted.locator(".chirpui-nav-tree__link").first
    bubble = hinted.locator(".chirpui-tooltip__bubble")

    assert await link.get_attribute("href") == "/gauntlet/contextual/branch"
    assert await nav.locator("summary").count() == 0

    await link.focus()
    await bubble.wait_for(state="visible")
    await page.wait_for_function(
        """(el) => {
            const rect = el.getBoundingClientRect();
            return parseFloat(getComputedStyle(el).opacity) > 0.9
                && rect.width > 0
                && rect.height > 0;
        }""",
        arg=await bubble.element_handle(),
    )


async def test_gauntlet_contextual_timeline_hints_do_not_use_link_overlay(page, base_url):
    await open_gauntlet(page, base_url, "/gauntlet/contextual", width=768, height=1024)

    timeline = page.locator("[data-testid='contextual-timeline']")
    assert await timeline.locator(".chirpui-timeline__hint").count() == 2
    assert await timeline.locator(".chirpui-timeline__title-link").count() == 1
    assert await timeline.locator(".chirpui-timeline__link-overlay").count() == 0

    first_title = timeline.locator(".chirpui-timeline__title-link").first
    await first_title.focus()
    bubble = timeline.locator(".chirpui-tooltip__bubble").first
    await bubble.wait_for(state="visible")
    await page.wait_for_function(
        """(el) => parseFloat(getComputedStyle(el).opacity) > 0.9""",
        arg=await bubble.element_handle(),
    )
    assert await bubble.inner_text() == "Visible from hover or keyboard focus."


async def test_gauntlet_contextual_popover_is_click_reachable_on_phone(page, base_url):
    await open_gauntlet(page, base_url, "/gauntlet/contextual", width=375, height=812)

    popover = page.locator("[data-testid='contextual-popover'] .chirpui-popover")
    trigger = popover.locator(".chirpui-popover__trigger")
    await trigger.click()

    assert await popover.evaluate("el => el.open")
    panel = popover.locator(".chirpui-popover__panel")
    await panel.wait_for(state="visible")
    failure = await panel.evaluate(
        """(el) => {
            const rect = el.getBoundingClientRect();
            const viewport = document.documentElement.clientWidth;
            if (rect.left >= -1 && rect.right <= viewport + 1) return null;
            return {
                left: Math.round(rect.left),
                right: Math.round(rect.right),
                viewport,
            };
        }"""
    )
    await assert_no_failures(page, [failure] if failure else [], "contextual-popover-phone")


async def test_gauntlet_entry_actions_remain_independent_from_main_link(page, base_url):
    await open_gauntlet(page, base_url, "/gauntlet/actions", width=768, height=1024)

    card = page.locator("[data-testid='action-resource-card']")
    main_link = card.locator(".chirpui-card__main-link")
    assert await main_link.get_attribute("href") == "/gauntlet/actions/resource"

    footer_controls_inside_main_link = await card.locator(
        ".chirpui-card__footer-wrap :is(a, button, [role='button'])"
    ).evaluate_all(
        """(els) => els.filter((el) => Boolean(el.closest(".chirpui-card__main-link"))).length"""
    )
    assert footer_controls_inside_main_link == 0

    await card.get_by_role("button", name="Pin").click()
    await wait_for_htmx(page)
    assert "pinned" in await page.locator("#entry-action-result").inner_text()
    assert page.url.endswith("/gauntlet/actions")


async def test_gauntlet_entry_action_menus_open_without_navigation_or_viewport_escape(
    page, base_url
):
    await open_gauntlet(page, base_url, "/gauntlet/actions", width=375, height=812)

    before_url = page.url
    menu_root = page.locator("#gauntlet-entry-card-menu")
    await menu_root.locator(".chirpui-dropdown__trigger").click()
    menu = menu_root.locator(".chirpui-dropdown__menu")
    await menu.wait_for(state="visible")

    assert page.url == before_url
    assert await menu.get_by_role("menuitem", name="Archive").count() == 1
    failure = await menu.evaluate(
        """(el) => {
            const rect = el.getBoundingClientRect();
            const viewport = document.documentElement.clientWidth;
            if (rect.left >= -1 && rect.right <= viewport + 1) return null;
            return {
                left: Math.round(rect.left),
                right: Math.round(rect.right),
                viewport,
            };
        }"""
    )
    await assert_no_failures(page, [failure] if failure else [], "entry-action-menu-phone")


async def test_gauntlet_timeline_header_actions_do_not_require_overlay_links(page, base_url):
    await open_gauntlet(page, base_url, "/gauntlet/actions", width=768, height=1024)

    timeline = page.locator("[data-testid='action-timeline']")
    assert await timeline.locator(".chirpui-timeline__title-link").count() == 1
    assert (
        await timeline.locator(".chirpui-timeline__header-actions .chirpui-dropdown").count() == 1
    )
    assert await timeline.locator(".chirpui-timeline__link-overlay").count() == 0

    await timeline.locator("#gauntlet-timeline-menu .chirpui-dropdown__trigger").click()
    await timeline.locator("#gauntlet-timeline-menu .chirpui-dropdown__menu").wait_for(
        state="visible"
    )


async def test_gauntlet_htmx_swap_preserves_layout_and_reinitializes_components(page, base_url):
    await open_gauntlet(page, base_url, "/gauntlet/swaps", width=375, height=812)

    trigger = page.get_by_role("button", name="Load urgent")
    await trigger.click()
    await wait_for_htmx(page)

    region = page.locator("[data-testid='gauntlet-swap-region']")
    assert await region.get_attribute("data-state") == "urgent"
    assert "Swapped urgent entry" in await region.inner_text()

    await assert_no_document_horizontal_overflow(page, "htmx-swap-urgent-phone")
    await assert_common_compositions_do_not_overlap(page, "htmx-swap-urgent-phone")
    await assert_control_rows_keep_coherent_heights(page, "htmx-swap-urgent-phone")
    await assert_touch_critical_controls_not_tiny(page, "htmx-swap-urgent-phone")

    swapped_menu = page.locator("#gauntlet-swapped-menu")
    await swapped_menu.locator(".chirpui-dropdown__trigger").click()
    await swapped_menu.locator(".chirpui-dropdown__menu").wait_for(state="visible")
    assert await swapped_menu.get_by_role("menuitem", name="Mark reviewed").count() == 1


async def test_gauntlet_htmx_swap_keeps_trigger_focus_and_allows_second_swap(page, base_url):
    await open_gauntlet(page, base_url, "/gauntlet/swaps", width=768, height=1024)

    urgent = page.get_by_role("button", name="Load urgent")
    await urgent.focus()
    await urgent.press("Enter")
    await wait_for_htmx(page)
    assert (
        await page.locator("[data-testid='gauntlet-swap-region']").get_attribute("data-state")
        == "urgent"
    )
    assert await urgent.evaluate("el => document.activeElement === el")

    await page.get_by_role("button", name="Refresh fragment").click()
    await wait_for_htmx(page)
    assert (
        await page.locator("[data-testid='gauntlet-swap-region']").get_attribute("data-state")
        == "stable"
    )


async def test_gauntlet_content_pressure_keeps_text_inside_viewport(page, base_url):
    await open_gauntlet(page, base_url, "/gauntlet/content", width=320, height=640)

    await assert_no_document_horizontal_overflow(page, "content-pressure-phone-320")
    failure = await page.locator("[data-testid='content-pressure']").evaluate(
        """(root) => {
            const viewport = document.documentElement.clientWidth;
            const offenders = [...root.querySelectorAll(
                ".chirpui-card__title, .chirpui-resource-card__description, .chirpui-badge, .chirpui-chip"
            )].filter((el) => {
                const rect = el.getBoundingClientRect();
                return rect.left < -1 || rect.right > viewport + 1;
            }).map((el) => ({
                className: el.className,
                text: (el.textContent || "").trim().slice(0, 80),
                rect: (() => {
                    const rect = el.getBoundingClientRect();
                    return { left: Math.round(rect.left), right: Math.round(rect.right) };
                })(),
                viewport,
            }));
            return offenders.length ? offenders : null;
        }"""
    )
    await assert_no_failures(page, failure or [], "content-pressure-contained")


async def test_gauntlet_content_long_menu_stays_inside_phone_viewport(page, base_url):
    await open_gauntlet(page, base_url, "/gauntlet/content", width=320, height=640)

    await page.locator("#gauntlet-content-menu .chirpui-dropdown__trigger").click()
    menu = page.locator("#gauntlet-content-menu .chirpui-dropdown__menu")
    await menu.wait_for(state="visible")
    failure = await menu.evaluate(
        """(el) => {
            const rect = el.getBoundingClientRect();
            const viewport = document.documentElement.clientWidth;
            if (rect.left >= -1 && rect.right <= viewport + 1) return null;
            return {
                left: Math.round(rect.left),
                right: Math.round(rect.right),
                viewport,
                text: (el.textContent || "").trim().slice(0, 120),
            };
        }"""
    )
    await assert_no_failures(page, [failure] if failure else [], "content-long-menu-phone")


async def test_gauntlet_dense_record_actions_remain_separate_from_record_links(page, base_url):
    await open_gauntlet(page, base_url, "/gauntlet/density", width=375, height=812)

    table = page.locator("[data-testid='dense-record-table']")
    assert await table.get_by_role("link", name="Alpha intake with a long but spaced title").count()
    row_actions = table.locator("[data-gauntlet-control-group='dense-row-actions']")
    assert await row_actions.get_by_role("link", name="Open").get_attribute("href") == (
        "/gauntlet/density/alpha"
    )

    await row_actions.locator("#gauntlet-dense-row-menu .chirpui-dropdown__trigger").click()
    await row_actions.locator("#gauntlet-dense-row-menu .chirpui-dropdown__menu").wait_for(
        state="visible"
    )
    assert page.url.endswith("/gauntlet/density")
    await assert_no_document_horizontal_overflow(page, "density-row-actions-phone")


async def test_gauntlet_state_matrix_preserves_state_semantics(page, base_url):
    await open_gauntlet(page, base_url, "/gauntlet/states", width=375, height=812)

    assert await page.get_by_role("button", name="Saving").get_attribute("aria-busy") == "true"
    assert await page.get_by_role("button", name="Disabled", exact=True).is_disabled()
    assert await page.get_by_label("Disabled settings").is_disabled()
    assert await page.locator(".chirpui-chip--selected").count() == 1
    assert await page.locator(".chirpui-chip--muted").count() == 1

    dismiss = page.get_by_label("Dismiss")
    assert await dismiss.count() == 1
    await dismiss.click()
    assert await page.get_by_text("Failed").count() == 0


async def test_gauntlet_edge_layers_stay_inside_phone_viewport(page, base_url):
    await open_gauntlet(page, base_url, "/gauntlet/edges", width=320, height=640)

    failures = []
    for selector in [
        "#gauntlet-edge-top-menu",
        "#gauntlet-edge-right-menu",
        "#gauntlet-edge-scroll-menu",
    ]:
        root = page.locator(selector)
        await root.locator(".chirpui-dropdown__trigger").click()
        menu = root.locator(".chirpui-dropdown__menu")
        await menu.wait_for(state="visible")
        failure = await menu.evaluate(
            """(el) => {
                const rect = el.getBoundingClientRect();
                const viewport = document.documentElement.clientWidth;
                if (rect.left >= -1 && rect.right <= viewport + 1) return null;
                return {
                    id: el.closest(".chirpui-dropdown")?.id,
                    left: Math.round(rect.left),
                    right: Math.round(rect.right),
                    viewport,
                };
            }"""
        )
        if failure:
            failures.append(failure)
        await page.keyboard.press("Escape")

    popover = page.locator("[data-testid='edge-popover'] .chirpui-popover")
    await popover.locator(".chirpui-popover__trigger").click()
    panel = popover.locator(".chirpui-popover__panel")
    await panel.wait_for(state="visible")
    popover_failure = await panel.evaluate(
        """(el) => {
            const rect = el.getBoundingClientRect();
            const viewport = document.documentElement.clientWidth;
            if (rect.left >= -1 && rect.right <= viewport + 1) return null;
            return {
                panel: "edge-popover",
                left: Math.round(rect.left),
                right: Math.round(rect.right),
                viewport,
            };
        }"""
    )
    if popover_failure:
        failures.append(popover_failure)
    await assert_no_failures(page, failures, "edge-layers-phone")


async def test_gauntlet_dropdown_select_interaction_does_not_shift_toolbar(page, base_url):
    await open_gauntlet(page, base_url, "/gauntlet/forms", width=375, height=812)

    group = page.locator("[data-gauntlet-control-group='toolbar']")
    before = await group.bounding_box()
    await page.locator("#gauntlet-view .chirpui-dropdown__trigger--select").click()
    await page.get_by_role("option", name="Table").click()
    after = await group.bounding_box()

    assert await page.locator("#gauntlet-view .chirpui-dropdown__selected").inner_text() == "Table"
    failures = []
    if before and after and abs(before["height"] - after["height"]) > 1:
        failures.append({"before": before["height"], "after": after["height"]})
    await assert_no_failures(page, failures, "dropdown-select-toolbar-shift")


async def test_gauntlet_split_dropdown_menu_stays_inside_viewport(page, base_url):
    await open_gauntlet(page, base_url, "/gauntlet/data", width=375, height=812)

    await page.locator(
        "[data-gauntlet-control-group='pagination'] .chirpui-dropdown__trigger--split"
    ).click()
    menu = page.locator("[data-gauntlet-control-group='pagination'] .chirpui-dropdown__menu")
    await menu.wait_for(state="visible")
    failure = await menu.evaluate(
        """(el) => {
            const rect = el.getBoundingClientRect();
            const viewport = document.documentElement.clientWidth;
            if (rect.left >= -1 && rect.right <= viewport + 1) return null;
            return {
                left: Math.round(rect.left),
                right: Math.round(rect.right),
                viewport,
            };
        }"""
    )
    await assert_no_failures(page, [failure] if failure else [], "split-dropdown-in-viewport")


async def test_gauntlet_focus_indicators_are_visible_for_mixed_controls(page, base_url):
    await open_gauntlet(page, base_url, "/gauntlet/forms", width=375, height=812)

    await assert_focused_element_has_visible_ring(
        page,
        "[data-gauntlet-control-group='toolbar'] .chirpui-btn",
        "gauntlet-button",
    )
    await assert_focused_element_has_visible_ring(
        page,
        "[data-gauntlet-control-group='toolbar'] .chirpui-dropdown__trigger--select",
        "gauntlet-select",
    )
