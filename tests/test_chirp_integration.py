"""Contract tests between chirp and chirp-ui.

Requires bengal-chirp installed (skip if not available).
Verifies that use_chirp_ui() correctly registers filters and loaders.
"""

import pytest

chirp = pytest.importorskip("chirp")

from chirp import App, AppConfig  # noqa: E402
from chirp.ext.chirp_ui import use_chirp_ui  # noqa: E402


@pytest.fixture
def app() -> App:
    """Minimal Chirp app with chirp-ui integration."""
    app = App(AppConfig(debug=True))
    use_chirp_ui(app)
    return app


class TestUseCHIRPUI:
    def test_registers_expected_filters(self, app: App) -> None:
        """use_chirp_ui registers all chirp-ui filters on the app."""
        registered = set(app._template_filters.keys())
        expected = {
            "validate_variant",
            "validate_variant_block",
            "validate_size",
            "resolve_color",
            "sanitize_color",
            "contrast_text",
        }
        missing = expected - registered
        assert not missing, f"Missing filters: {missing}"

    def test_registers_standard_chirp_filters(self, app: App) -> None:
        """use_chirp_ui also registers standard Chirp filters (bem, html_attrs, etc.)."""
        registered = set(app._template_filters.keys())
        for name in ("bem", "html_attrs", "field_errors", "icon"):
            assert name in registered, f"Missing standard filter: {name}"

    def test_static_files_path_exists(self) -> None:
        """chirp-ui static files path contains chirpui.css."""
        from chirp_ui import static_path

        static = static_path()
        assert static.is_dir()
        assert (static / "chirpui.css").exists()
