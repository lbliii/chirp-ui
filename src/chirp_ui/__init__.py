"""chirp-ui — Reusable Kida component library for Chirp.

Headless, htmx-native, zero JavaScript. Install and import::

    pip install chirp-ui

    {%% from "chirpui/card.html" import card %%}
    {%% from "chirpui/modal.html" import modal, modal_trigger %%}

When used with Chirp, components are auto-detected via ``PackageLoader``.
For standalone Kida usage, call :func:`get_loader`.
Call :func:`register_filters` to ensure bem/field_errors/html_attrs filters are available.
Call :func:`register_colors` once per app if you use semantic color names with
``resolve_color`` / ``badge(..., color=...)`` / ``filter_chips`` (see ``docs/COMPONENT-OPTIONS.md``).
"""

import json
from functools import cache
from importlib.resources import files
from pathlib import Path
from typing import Any

from kida import PackageLoader

from chirp_ui.alpine import (
    ALPINE_REQUIRED_COMPONENTS,
    AlpineRequirement,
    AlpineRuntimeCheck,
    check_alpine_runtime,
)
from chirp_ui.components import DesignSystemReport, DesignSystemStats, design_system_report
from chirp_ui.filters import TemplateFilterApp, register_colors, reset_colors
from chirp_ui.validation import (
    ChirpUIDeprecationWarning,
    ChirpUIValidationWarning,
    ChirpUIWarning,
    is_strict,
    set_strict,
)

# Declare free-threading support (PEP 703)
_Py_mod_gil = 0

__version__ = "0.5.0"

__all__ = [
    "ALPINE_REQUIRED_COMPONENTS",
    "MANIFEST_PATH",
    "AlpineRequirement",
    "AlpineRuntimeCheck",
    "ChirpUIDeprecationWarning",
    "ChirpUIValidationWarning",
    "ChirpUIWarning",
    "DesignSystemReport",
    "DesignSystemStats",
    "check_alpine_runtime",
    "design_system_report",
    "get_loader",
    "is_strict",
    "load_manifest",
    "register_colors",
    "register_filters",
    "reset_colors",
    "set_strict",
    "static_path",
]

# Path to the shipped ``chirpui-manifest@3`` JSON. Populated at build time by
# ``scripts/build_manifest.py`` and committed as package data; CI's
# ``build-manifest-check`` task guards against drift. Agents and tooling can
# ground against this file after a clean ``pip install chirp-ui`` with no
# build step.
MANIFEST_PATH: Path = Path(str(files("chirp_ui").joinpath("manifest.json")))


@cache
def load_manifest() -> dict[str, Any]:
    """Return the shipped component/token manifest as a dict.

    Cached for the life of the process. Uses :class:`importlib.resources` so
    it works both in-tree and after ``pip install chirp-ui``. Free-threading
    safe: ``functools.cache`` on a no-arg function is sound under 3.14t
    because :func:`json.loads` is pure and the first-reader wins the race
    without observable state drift.

    Example::

        from chirp_ui import load_manifest
        manifest = load_manifest()
        metric_card = manifest["components"]["metric-card"]
        print([p["name"] for p in metric_card["params"]])
    """
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def static_path() -> Path:
    """Path to chirp-ui templates (chirpui.css, chirpui.js, chirpui-alpine.js, patterns/*.svg, themes/).

    Use with StaticFiles to serve CSS and themes from the package::

        from chirp.middleware.static import StaticFiles
        import chirp_ui
        app.add_middleware(StaticFiles(
            directory=str(chirp_ui.static_path()),
            prefix="/static"
        ))
    """
    return Path(__file__).parent / "templates"


def get_loader() -> PackageLoader:
    """Return a PackageLoader for chirp-ui templates.

    Usage (manual registration without Chirp)::

        from kida import ChoiceLoader, Environment, FileSystemLoader
        from chirp_ui import get_loader

        env = Environment(
            loader=ChoiceLoader([
                FileSystemLoader("templates"),
                get_loader(),
            ])
        )
    """
    return PackageLoader("chirp_ui", "templates")


def register_filters(app: TemplateFilterApp) -> None:
    """Register chirp-ui filters (bem, field_errors, html_attrs) on a Chirp app.

    Call after App creation so chirp-ui components render correctly::

        from chirp import App
        import chirp_ui
        app = App(...)
        chirp_ui.register_filters(app)
    """
    from chirp_ui.filters import register_filters as _register

    _register(app)
