#!/usr/bin/env python3
"""Build deterministic-scenario PDF proofs for the packaged Bengal theme."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
from contextlib import asynccontextmanager, contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from typing import TYPE_CHECKING

from playwright.async_api import async_playwright

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = "/tests/browser/templates/bengal_print_contract.html"
SCENARIOS = (
    {
        "name": "letter-color",
        "format": "Letter",
        "print_background": True,
        "grayscale": False,
    },
    {
        "name": "a4-background-off",
        "format": "A4",
        "print_background": False,
        "grayscale": False,
    },
    {
        "name": "letter-grayscale",
        "format": "Letter",
        "print_background": True,
        "grayscale": True,
    },
)


class QuietHandler(SimpleHTTPRequestHandler):
    """Serve fixture assets without polluting proof output with request logs."""

    def log_message(self, format: str, *args: object) -> None:
        return


@contextmanager
def static_repo_url() -> Iterator[str]:
    handler = partial(QuietHandler, directory=str(REPO_ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


@asynccontextmanager
async def async_static_repo_url() -> AsyncIterator[str]:
    """Adapt the threaded fixture server to the async Playwright lifecycle."""
    with static_repo_url() as base_url:
        yield base_url


async def build_proofs(output_dir: Path) -> list[dict[str, object]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, object]] = []

    async with async_static_repo_url() as base_url, async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        try:
            for scenario in SCENARIOS:
                page = await browser.new_page(viewport={"width": 1124, "height": 1000})
                print_events: list[str] = []
                await page.expose_function(
                    "recordPrintEvent", lambda event, events=print_events: events.append(event)
                )
                await page.add_init_script(
                    """
                    window.addEventListener('beforeprint', () => window.recordPrintEvent('beforeprint'));
                    window.addEventListener('afterprint', () => window.recordPrintEvent('afterprint'));
                    """
                )
                await page.goto(f"{base_url}{FIXTURE_PATH}", wait_until="networkidle")
                await page.wait_for_function("() => window.BengalMain")
                if scenario["grayscale"]:
                    await page.add_style_tag(
                        content="""
                        @media print {
                          *, *::before, *::after {
                            background: #fff !important;
                            border-color: #777 !important;
                            color: #111 !important;
                            outline-color: #777 !important;
                            text-decoration-color: #111 !important;
                          }
                        }
                        """
                    )

                output = output_dir / f"bengal-print-{scenario['name']}.pdf"
                await page.pdf(
                    path=str(output),
                    format=str(scenario["format"]),
                    print_background=bool(scenario["print_background"]),
                    display_header_footer=False,
                    tagged=True,
                    outline=True,
                )
                before_count = print_events.count("beforeprint")
                after_count = print_events.count("afterprint")
                if (
                    before_count < 1
                    or before_count != after_count
                    or print_events[0] != "beforeprint"
                    or print_events[-1] != "afterprint"
                ):
                    msg = f"unexpected print lifecycle for {scenario['name']}: {print_events}"
                    raise RuntimeError(msg)
                if await page.locator("[data-print-generated]").count() != 0:
                    msg = f"print metadata was not restored after {scenario['name']}"
                    raise RuntimeError(msg)

                payload = output.read_bytes()
                manifest.append(
                    {
                        **scenario,
                        "file": output.name,
                        "bytes": len(payload),
                        "sha256": hashlib.sha256(payload).hexdigest(),
                        "tagged": True,
                        "outline": True,
                    }
                )
                await page.close()
        finally:
            await browser.close()

    (output_dir / "manifest.json").write_text(
        json.dumps({"fixture": FIXTURE_PATH, "scenarios": manifest}, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "output" / "pdf",
        help="Directory for proof PDFs and manifest (default: output/pdf)",
    )
    args = parser.parse_args()
    manifest = asyncio.run(build_proofs(args.output_dir.resolve()))
    for item in manifest:
        print(f"built {item['file']} ({item['bytes']} bytes)")


if __name__ == "__main__":
    main()
