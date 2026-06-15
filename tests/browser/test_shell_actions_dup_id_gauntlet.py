"""Browser gauntlet for shell_actions_bar duplicate-id namespacing (#224).

When a consumer composes the bar in two regions (the canonical topbar plus a
mobile-drawer copy), the baked overflow id (`<target>-overflow`) and per-action
menu ids (`chirpui-shell-action-<id>`) would collide — invalid HTML that makes
getElementById ambiguous and lets one trigger cross-drive the other's panel.
id_suffix namespaces both fixed ids on the second instance. This is the test
that would have caught the bug: only a real-DOM scan can prove there are zero
duplicate ids — a TestClient string check passes on duplicate ids.

The drawer copy is rendered with id_suffix="-drawer"; the topbar copy uses the
default suffix. Both stubs carry an overflow zone AND a kind="menu" action.
"""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def _open(page, base_url):
    await page.goto(base_url + "/shell-actions-dup")
    await wait_for_alpine(page)
    await page.wait_for_timeout(100)


async def test_no_duplicate_ids_with_bar_in_two_regions(page, base_url):
    await _open(page, base_url)
    dups = await page.evaluate(
        """() => {
            const ids = [...document.querySelectorAll('[id]')]
                .map(e => e.id)
                .filter(Boolean);
            const seen = new Set();
            const dups = [];
            ids.forEach(i => { if (seen.has(i)) dups.push(i); else seen.add(i); });
            return dups;
        }"""
    )
    assert dups == [], f"duplicate ids in the rendered document: {dups}"


async def test_both_overflow_ids_present_and_distinct(page, base_url):
    await _open(page, base_url)
    # Exactly one canonical (topbar) overflow id and one suffixed (drawer) one.
    await expect(page.locator("#chirp-shell-actions-overflow")).to_have_count(1)
    await expect(page.locator("#chirp-shell-actions-overflow-drawer")).to_have_count(1)
    # The drawer-suffixed overflow lives inside the drawer copy; the canonical
    # one does not.
    drawer = page.get_by_test_id("drawer-actions")
    await expect(drawer.locator("#chirp-shell-actions-overflow-drawer")).to_have_count(1)
    await expect(drawer.locator("#chirp-shell-actions-overflow")).to_have_count(0)
    # Per-action menu ids are namespaced too.
    await expect(page.locator("#chirpui-shell-action-bulk")).to_have_count(1)
    await expect(page.locator("#chirpui-shell-action-bulk-drawer")).to_have_count(1)


async def test_drawer_more_drives_its_own_panel(page, base_url):
    await _open(page, base_url)
    drawer = page.get_by_test_id("drawer-actions")
    drawer_overflow = drawer.locator("#chirp-shell-actions-overflow-drawer")
    topbar_overflow = page.locator("#chirp-shell-actions-overflow")

    drawer_panel = drawer_overflow.locator(".chirpui-dropdown__menu")
    topbar_panel = topbar_overflow.locator(".chirpui-dropdown__menu")
    await expect(drawer_panel).to_be_hidden()
    await expect(topbar_panel).to_be_hidden()

    # Open the drawer copy's "More" trigger.
    await drawer_overflow.locator(".chirpui-dropdown__trigger").click()
    await expect(drawer_panel).to_be_visible()
    # The topbar overflow panel stays closed — Alpine $id wiring is
    # instance-scoped, so the duplicate-id cross-driving described in #224 is gone.
    await expect(topbar_panel).to_be_hidden()
