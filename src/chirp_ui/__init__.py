"""chirp-ui — Reusable Kida component library for Chirp.

Headless, htmx-native, zero JavaScript. Install and import::

    pip install chirp-ui

    {%% from "chirpui/card" import card %%}
    {%% from "chirpui/modal" import modal, modal_trigger %%}

When used with Chirp, components are auto-detected via ``PackageLoader``.
For standalone Kida usage, call :func:`get_loader`.
"""

from kida import PackageLoader

# Declare free-threading support (PEP 703)
_Py_mod_gil = 0

__version__ = "0.1.0"


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
