"""Golden screen reference routes."""

from __future__ import annotations

from chirp import App, Request, Template
from fixtures.market import market_context
from fixtures.ops import ops_context
from fixtures.support import support_context
from showcase.helpers import page


def register(app: App) -> None:
    @app.route("/screen-command-center", template="showcase/operations_shell.html")
    async def screen_command_center(request: Request) -> Template:
        return page(
            request,
            "showcase/operations_shell.html",
            **ops_context(request, base_path="/screen-command-center"),
            ops_screen_title="Golden screen: Command Center",
            ops_screen_subtitle=(
                "Atlas profile fixture for metrics, queues, incidents, activity, "
                "and selected-object inspection."
            ),
            ops_screen_archetype="command-center",
            ops_screen_profile="atlas",
        )

    @app.route("/screen-review-queue", template="showcase/support_shell.html")
    async def screen_review_queue(request: Request) -> Template:
        return page(
            request,
            "showcase/support_shell.html",
            **support_context(request, base_path="/screen-review-queue"),
            support_screen_title="Golden screen: Review Queue",
            support_screen_subtitle=(
                "Sage profile fixture for filter rail, result collection, inspector, "
                "stateful tickets, and batch-ready review work."
            ),
            support_screen_archetype="review-queue",
            support_screen_profile="sage",
        )

    @app.route("/screen-agent-run-monitor", template="showcase/screen_agent_run_monitor.html")
    async def screen_agent_run_monitor(request: Request) -> Template:
        return page(request, "showcase/screen_agent_run_monitor.html")

    @app.route("/screen-product-docs-home", template="showcase/screen_product_docs_home.html")
    async def screen_product_docs_home(request: Request) -> Template:
        return page(request, "showcase/screen_product_docs_home.html")

    @app.route("/screen-lucky-cat-market", template="showcase/screen_lucky_cat_market.html")
    async def screen_lucky_cat_market(request: Request) -> Template:
        return page(
            request,
            "showcase/screen_lucky_cat_market.html",
            **market_context(request, base_path="/screen-lucky-cat-market"),
            market_screen_title="Golden screen: Lucky Cat Market",
            market_screen_subtitle=(
                "Atlas profile fixture for ticker search, movers, market catalog, "
                "and live activity on a data-dense trading floor."
            ),
            market_screen_archetype="data-dense-market",
            market_screen_profile="atlas",
        )
