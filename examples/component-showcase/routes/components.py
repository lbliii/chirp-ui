"""Component gallery and static showcase page routes."""

from __future__ import annotations

import calendar as cal_mod
from datetime import date

from chirp import (
    App,
    Fragment,
    Request,
    Response,
    ShellAction,
    ShellActions,
    ShellActionZone,
    Template,
)
from showcase.blocks_data import load_blocks_gallery
from showcase.helpers import page

from chirp_ui.theme_packs import get_theme_pack, list_theme_packs


def register(app: App) -> None:
    @app.route("/htmx", template="showcase/htmx.html")
    async def htmx_patterns(request: Request) -> Template:
        return page(request, "showcase/htmx.html")

    @app.route("/navigation", template="showcase/navigation.html")
    async def navigation(request: Request) -> Template:
        return page(request, "showcase/navigation.html")

    @app.route("/layout", template="showcase/layout.html")
    async def layout(request: Request) -> Template:
        direction = request.query.get("dir", "ltr")
        if direction not in {"ltr", "rtl"}:
            direction = "ltr"
        return page(request, "showcase/layout.html", direction=direction)

    @app.route("/chrome", template="showcase/chrome.html")
    async def chrome(request: Request) -> Template:
        return page(request, "showcase/chrome.html")

    @app.route("/shell-actions", template="showcase/shell_actions.html")
    async def shell_actions(request: Request) -> Template:
        actions = ShellActions(
            primary=ShellActionZone(
                items=(
                    ShellAction(
                        id="new-thread",
                        label="New thread",
                        href="/forms",
                        variant="primary",
                    ),
                )
            ),
            controls=ShellActionZone(
                items=(
                    ShellAction(id="sort", label="Latest", href="/data", variant="default"),
                    ShellAction(
                        id="watch", label="Watch", action="watch-thread", variant="secondary"
                    ),
                )
            ),
            overflow=ShellActionZone(
                items=(
                    ShellAction(id="share", label="Share", href="/social"),
                    ShellAction(id="archive", label="Archive", action="archive-thread"),
                )
            ),
        )
        return page(request, "showcase/shell_actions.html", shell_actions=actions)

    @app.route("/sections", template="showcase/sections.html")
    async def sections(request: Request) -> Template:
        return page(request, "showcase/sections.html")

    @app.route("/layout/dir", methods=["GET"])
    async def layout_dir(request: Request) -> Fragment:
        """Return Fragment with dir block for RTL/LTR toggle."""
        direction = request.query.get("dir", "ltr")
        return Fragment("showcase/_layout_dir.html", "dir_block", direction=direction)

    @app.route("/carousel", template="showcase/carousel.html")
    async def carousel_page(request: Request) -> Template:
        return page(request, "showcase/carousel.html")

    @app.route("/cards", template="showcase/cards.html")
    async def cards(request: Request) -> Template:
        return page(request, "showcase/cards.html")

    @app.route("/forms", template="showcase/forms.html")
    async def forms(request: Request) -> Template:
        return page(request, "showcase/forms.html")

    @app.route("/appearance-tone", template="showcase/appearance-tone.html")
    async def appearance_tone(request: Request) -> Template:
        return page(request, "showcase/appearance-tone.html")

    @app.route("/theme-packs", template="showcase/theme-packs.html")
    async def theme_packs(request: Request) -> Template:
        return page(request, "showcase/theme-packs.html", theme_packs=list_theme_packs())

    @app.route("/theme-packs/preview/{name}/{mode}", template="showcase/theme_pack_preview.html")
    async def theme_pack_preview(request: Request, name: str, mode: str) -> Template | Response:
        pack = get_theme_pack(name)
        if pack is None or mode not in pack.modes:
            return Response("Theme pack preview not found", status=404)
        return page(request, "showcase/theme_pack_preview.html", pack=pack, mode=mode)

    @app.route("/blocks", template="showcase/blocks.html")
    async def blocks_gallery(request: Request) -> Template:
        gallery = load_blocks_gallery()
        return page(
            request,
            "showcase/blocks.html",
            blocks_items=gallery.get("blocks", []),
            blocks_categories=gallery.get("categories", []),
            blocks_stats=gallery.get("stats", {}),
        )

    @app.route("/ui", template="showcase/ui.html")
    async def ui(request: Request) -> Template:
        return page(request, "showcase/ui.html")

    @app.route("/ui/tab/{name}", methods=["GET"])
    async def ui_tab(request: Request, name: str) -> Fragment:
        return Fragment("showcase/_tab_content.html", "tab_content", active_tab=name)

    @app.route("/data-display", template="showcase/data-display.html")
    async def data_display(request: Request) -> Template:
        return page(request, "showcase/data-display.html")

    @app.route("/calendar", template="showcase/calendar.html")
    @app.route("/calendar/{year}/{month}", template="showcase/calendar.html")
    async def calendar_view(
        request: Request,
        year: int | str | None = None,
        month: int | str | None = None,
    ) -> Template:
        today = date.today()
        year = int(year) if year is not None else today.year
        month = int(month) if month is not None else today.month
        cal = cal_mod.Calendar(firstweekday=cal_mod.SUNDAY)
        weeks = cal.monthdayscalendar(year, month)
        month_name = cal_mod.month_name[month]
        month_label = f"{month_name} {year}"
        prev_month = month - 1 or 12
        prev_year = year if month > 1 else year - 1
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1
        prev_url = f"/calendar/{prev_year}/{prev_month}"
        next_url = f"/calendar/{next_year}/{next_month}"
        return page(
            request,
            "showcase/calendar.html",
            weeks=weeks,
            month_label=month_label,
            prev_url=prev_url,
            next_url=next_url,
        )

    @app.route("/effects", template="showcase/effects.html")
    async def effects(request: Request) -> Template:
        return page(request, "showcase/effects.html")

    @app.route("/typography", template="showcase/typography.html")
    async def typography(request: Request) -> Template:
        return page(request, "showcase/typography.html")

    @app.route("/ascii-primitives", template="showcase/ascii_primitives.html")
    async def ascii_primitives(request: Request) -> Template:
        return page(request, "showcase/ascii_primitives.html")

    @app.route("/buttons", template="showcase/buttons.html")
    async def buttons(request: Request) -> Template:
        return page(request, "showcase/buttons.html")

    @app.route("/dashboard", template="showcase/dashboard.html")
    async def dashboard(request: Request) -> Template:
        return page(request, "showcase/dashboard.html")

    @app.route("/animation", template="showcase/animation.html")
    async def animation(request: Request) -> Template:
        return page(request, "showcase/animation.html")

    @app.route("/ascii", template="showcase/ascii.html")
    async def ascii_icons(request: Request) -> Template:
        return page(request, "showcase/ascii.html")

    @app.route("/animation/swap-demo", methods=["GET"])
    async def animation_swap_demo(request: Request) -> Fragment:
        return Fragment("showcase/_swap_content.html", "swap_demo")

    @app.route("/messenger", template="showcase/messenger.html")
    async def messenger(request: Request) -> Template:
        return page(request, "showcase/messenger.html")

    @app.route("/social", template="showcase/social.html")
    async def social(request: Request) -> Template:
        return page(request, "showcase/social.html")

    @app.route("/video", template="showcase/video.html")
    async def video(request: Request) -> Template:
        return page(request, "showcase/video.html")
