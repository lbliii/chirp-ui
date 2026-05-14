"""Browser regression for route-scoped shell actions OOB updates."""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine, wait_for_htmx

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def open_workspace_consumer(page, base_url: str):
    await page.set_viewport_size({"width": 1024, "height": 768})
    await page.goto(base_url + "/consumer-workspace")
    await wait_for_alpine(page)
    await page.wait_for_timeout(100)


async def test_shell_actions_oob_replace_on_boosted_shell_navigation(page, base_url):
    await open_workspace_consumer(page, base_url)

    shell_actions = page.locator("#chirp-shell-actions")
    await expect(shell_actions).to_contain_text("New run")
    await expect(shell_actions).not_to_contain_text("Invite member")

    await page.locator('a[href="/consumer-admin"]').click()
    await wait_for_htmx(page)

    await expect(page).to_have_url(base_url + "/consumer-admin")
    await expect(shell_actions).to_contain_text("Invite member")
    await expect(shell_actions).not_to_contain_text("New run")
    await expect(shell_actions.get_by_role("link", name="Invite member")).to_have_count(1)

    await page.get_by_role("link", name="Workspace").click()
    await wait_for_htmx(page)

    await expect(page).to_have_url(base_url + "/consumer-workspace")
    await expect(shell_actions).to_contain_text("New run")
    await expect(shell_actions).not_to_contain_text("Invite member")
    await expect(shell_actions.get_by_role("link", name="New run")).to_have_count(1)
