"""chirp-ui — Reusable Kida component library for Chirp.

Headless, htmx-native, zero JavaScript. Install and import::

    pip install chirp-ui

    {%% from "chirpui/card.html" import card %%}
    {%% from "chirpui/modal.html" import modal, modal_trigger %%}

When used with Chirp, components are auto-detected via ``PackageLoader``.
For standalone Kida usage, call :func:`get_loader`.
Call :func:`register_filters` to ensure bem/field_errors filters are available.
"""

from pathlib import Path

from kida import PackageLoader

# Declare free-threading support (PEP 703)
_Py_mod_gil = 0

__version__ = "0.2.0"

__all__ = ["get_loader", "register_filters", "static_path"]


def static_path() -> Path:
    """Path to chirp-ui templates (chirpui.css, themes/).

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


def register_filters(app: object) -> None:
    """Register chirp-ui filters (bem, field_errors) on a Chirp app.

    Call after App creation so chirp-ui components render correctly::

        from chirp import App
        import chirp_ui
        app = App(...)
        chirp_ui.register_filters(app)
    """
    from chirp_ui.filters import register_filters as _register

    _register(app)
