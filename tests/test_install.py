"""Smoke tests to verify chirp-ui works after pip install."""

from kida import Environment

import chirp_ui


def test_import_chirp_ui() -> None:
    """Import succeeds and package exposes public API."""
    assert hasattr(chirp_ui, "get_loader")
    assert hasattr(chirp_ui, "register_filters")
    assert hasattr(chirp_ui, "static_path")
    assert chirp_ui.__version__


def test_get_loader_loads_template() -> None:
    """get_loader() returns a loader that can resolve chirp-ui templates."""
    env = Environment(loader=chirp_ui.get_loader(), autoescape=True)
    html = env.from_string(
        '{% from "chirpui/card.html" import card %}{% call card() %}Body{% end %}'
    ).render()
    assert "chirpui-card" in html
    assert "Body" in html


def test_static_path_exists() -> None:
    """static_path() points to a directory with chirpui.css."""
    path = chirp_ui.static_path()
    assert path.exists()
    assert (path / "chirpui.css").exists()
