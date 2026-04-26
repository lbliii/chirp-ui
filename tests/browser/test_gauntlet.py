"""Responsive composition gauntlet.

This suite exercises ChirpUI as downstream apps compose it: many components
sharing one shell, dense controls in the same row, hostile labels, state
pressure, and viewport pressure from phone through desktop.
"""

import pytest

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
    "/gauntlet/navigation",
    "/gauntlet/forms",
    "/gauntlet/data",
    "/gauntlet/workflow",
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
    pytest.param("/gauntlet/forms", 375, 812, id="forms-phone"),
    pytest.param("/gauntlet/data", 375, 812, id="data-phone"),
    pytest.param("/gauntlet/workflow", 375, 812, id="workflow-phone"),
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


@pytest.mark.parametrize("path", ["/gauntlet/forms", "/gauntlet/hostile"])
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
