"""Unit tests for chirp-ui icon registry and icon() resolution."""

import pytest

from chirp_ui.icons import ICON_REGISTRY, icon


class TestIconRegistry:
    """ICON_REGISTRY contains all expected entries and only str→str mappings."""

    def test_registry_is_nonempty(self) -> None:
        assert len(ICON_REGISTRY) > 0

    def test_all_values_are_strings(self) -> None:
        for name, glyph in ICON_REGISTRY.items():
            assert isinstance(name, str), f"key {name!r} is not str"
            assert isinstance(glyph, str), f"value for {name!r} is not str"

    def test_no_empty_keys(self) -> None:
        for name in ICON_REGISTRY:
            assert name.strip(), "registry contains an empty or whitespace-only key"

    def test_no_empty_values(self) -> None:
        for name, glyph in ICON_REGISTRY.items():
            assert glyph, f"icon {name!r} maps to empty string"

    def test_known_icons_present(self) -> None:
        expected = {
            "status",
            "add",
            "refresh",
            "search",
            "reply",
            "share",
            "up",
            "down",
            "watch",
            "follow",
            "report",
            "home",
            "gear",
            "star",
            "cloud",
            "bolt",
            "chat",
            "alert",
            "pencil",
        }
        missing = expected - set(ICON_REGISTRY)
        assert not missing, f"expected icons missing from registry: {missing}"

    def test_values_are_single_grapheme_cluster_or_short(self) -> None:
        for name, glyph in ICON_REGISTRY.items():
            assert len(glyph) <= 3, f"icon {name!r} maps to unexpectedly long value {glyph!r}"


class TestIconFunction:
    """icon() resolves names and passes through unknown names."""

    def test_resolves_known_name(self) -> None:
        assert icon("status") == "◎"
        assert icon("add") == "+"
        assert icon("gear") == "⚙"

    def test_unknown_name_passes_through(self) -> None:
        assert icon("nonexistent-icon") == "nonexistent-icon"

    def test_empty_string_passes_through(self) -> None:
        assert icon("") == ""

    def test_unicode_input_passes_through(self) -> None:
        assert icon("🔥") == "🔥"

    def test_whitespace_only_passes_through(self) -> None:
        assert icon("  ") == "  "

    @pytest.mark.parametrize(
        "name",
        sorted(ICON_REGISTRY.keys()),
        ids=sorted(ICON_REGISTRY.keys()),
    )
    def test_every_registered_icon_resolves(self, name: str) -> None:
        result = icon(name)
        assert result == ICON_REGISTRY[name]
        assert result != name or name == ICON_REGISTRY[name]
