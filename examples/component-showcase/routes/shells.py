"""Shell recipe routes for catalog, operations, and support demos."""

from __future__ import annotations

from chirp import App, Request, Template

from fixtures.catalog import catalog_context
from fixtures.ops import ops_context
from fixtures.support import support_context
from showcase.helpers import page


def register(app: App) -> None:
    @app.route("/catalog-shell", template="showcase/catalog_shell.html")
    async def catalog_shell(request: Request) -> Template:
        return page(request, "showcase/catalog_shell.html", **catalog_context(request))

    @app.route("/operations-shell", template="showcase/operations_shell.html")
    async def operations_shell(request: Request) -> Template:
        return page(request, "showcase/operations_shell.html", **ops_context(request))

    @app.route("/operations-shell-workspace", template="showcase/operations_shell_workspace.html")
    async def operations_shell_workspace(request: Request) -> Template:
        return page(
            request,
            "showcase/operations_shell_workspace.html",
            **ops_context(request, base_path="/operations-shell-workspace"),
        )

    @app.route("/support-shell", template="showcase/support_shell.html")
    async def support_shell(request: Request) -> Template:
        return page(request, "showcase/support_shell.html", **support_context(request))
