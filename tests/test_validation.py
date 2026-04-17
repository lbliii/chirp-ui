"""Unit tests for chirp-ui validation module (set_strict, _is_strict, registries)."""

import threading

import pytest

from chirp_ui.validation import (
    CHIRP_UI_DEV_ENV,
    SIZE_REGISTRY,
    VARIANT_REGISTRY,
    _is_strict,
    set_strict,
)


class TestSetStrict:
    """set_strict / _is_strict ContextVar behavior."""

    def setup_method(self) -> None:
        set_strict(False)

    def teardown_method(self) -> None:
        set_strict(False)

    def test_default_is_not_strict(self) -> None:
        assert _is_strict() is False

    def test_set_strict_true(self) -> None:
        set_strict(True)
        assert _is_strict() is True

    def test_set_strict_false_after_true(self) -> None:
        set_strict(True)
        assert _is_strict() is True
        set_strict(False)
        assert _is_strict() is False

    def test_toggle_repeatedly(self) -> None:
        for _ in range(5):
            set_strict(True)
            assert _is_strict() is True
            set_strict(False)
            assert _is_strict() is False


class TestSetStrictAuto:
    """set_strict("auto") resolves CHIRP_UI_DEV at call time."""

    def setup_method(self) -> None:
        set_strict(False)

    def teardown_method(self) -> None:
        set_strict(False)

    def test_auto_with_env_set_enables_strict(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv(CHIRP_UI_DEV_ENV, "1")
        set_strict("auto")
        assert _is_strict() is True

    def test_auto_without_env_stays_off(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv(CHIRP_UI_DEV_ENV, raising=False)
        set_strict("auto")
        assert _is_strict() is False

    @pytest.mark.parametrize("value", ["1", "true", "TRUE", "yes", "on", " On "])
    def test_auto_truthy_values(self, monkeypatch: pytest.MonkeyPatch, value: str) -> None:
        monkeypatch.setenv(CHIRP_UI_DEV_ENV, value)
        set_strict("auto")
        assert _is_strict() is True, f"{value!r} should enable strict"

    @pytest.mark.parametrize("value", ["", "0", "false", "no", "off", "  ", "dev"])
    def test_auto_falsy_values(self, monkeypatch: pytest.MonkeyPatch, value: str) -> None:
        monkeypatch.setenv(CHIRP_UI_DEV_ENV, value)
        set_strict("auto")
        assert _is_strict() is False, f"{value!r} should not enable strict"

    def test_auto_reads_env_at_call_time(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv(CHIRP_UI_DEV_ENV, raising=False)
        set_strict("auto")
        assert _is_strict() is False

        monkeypatch.setenv(CHIRP_UI_DEV_ENV, "1")
        set_strict("auto")
        assert _is_strict() is True

    def test_bool_argument_still_works(self) -> None:
        set_strict(True)
        assert _is_strict() is True
        set_strict(False)
        assert _is_strict() is False


class TestStrictEscalatesEveryValidationSite:
    """Every ChirpUIValidationWarning site raises ValueError under strict mode.

    Covers the 8 ``_warn()`` call sites in ``filters.py`` so the contract
    ``strict mode escalates every validation warning to ValueError`` is
    enforced, not just assumed.
    """

    def setup_method(self) -> None:
        set_strict(True)

    def teardown_method(self) -> None:
        set_strict(False)

    def test_invalid_variant_raises(self) -> None:
        from chirp_ui.filters import validate_variant

        with pytest.raises(ValueError, match="variant"):
            validate_variant("gold", ("primary", "secondary"))

    def test_invalid_block_variant_raises(self) -> None:
        from chirp_ui.filters import validate_variant_block

        with pytest.raises(ValueError, match="variant"):
            validate_variant_block("gold", "badge")

    def test_invalid_size_raises(self) -> None:
        from chirp_ui.filters import validate_size

        with pytest.raises(ValueError, match="size"):
            validate_size("xxxl", "btn")

    def test_bem_invalid_variant_raises(self) -> None:
        from chirp_ui.filters import bem

        with pytest.raises(ValueError, match="variant"):
            bem("btn", variant="gold")

    def test_bem_invalid_size_raises(self) -> None:
        from chirp_ui.filters import bem

        with pytest.raises(ValueError, match="size"):
            bem("btn", size="xxxl")

    def test_bem_invalid_modifier_raises(self) -> None:
        from chirp_ui.components import COMPONENTS
        from chirp_ui.filters import bem

        block_with_modifiers = next(
            (name for name, desc in COMPONENTS.items() if desc.modifiers),
            None,
        )
        assert block_with_modifiers, "need a component with registered modifiers for this test"
        with pytest.raises(ValueError, match="modifier"):
            bem(block_with_modifiers, modifier="__definitely_not_a_real_modifier__")

    def test_unknown_icon_raises(self) -> None:
        from chirp_ui.filters import icon

        with pytest.raises(ValueError, match="icon"):
            icon("arrow-left")

    def test_contrast_text_unparseable_raises(self) -> None:
        from chirp_ui.filters import contrast_text

        with pytest.raises(ValueError, match="contrast_text"):
            contrast_text("not-a-real-color")

    def test_deprecation_warnings_do_not_escalate(self) -> None:
        """ChirpUIDeprecationWarning always warns, never raises."""
        import warnings

        from chirp_ui.filters import deprecate_param

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            deprecate_param("some-value", "old_param", "new_param")
        assert caught, "deprecate_param should still emit a warning in strict mode"


class TestStrictContextVarIsolation:
    """ContextVar isolation across threads."""

    def setup_method(self) -> None:
        set_strict(False)

    def teardown_method(self) -> None:
        set_strict(False)

    def test_child_set_does_not_leak_to_parent(self) -> None:
        set_strict(False)

        def child_fn() -> None:
            set_strict(True)
            assert _is_strict() is True

        t = threading.Thread(target=child_fn)
        t.start()
        t.join()

        assert _is_strict() is False, "child's set_strict should not leak to parent"


class TestVariantRegistry:
    """VARIANT_REGISTRY structure and content checks."""

    def test_registry_is_nonempty(self) -> None:
        assert len(VARIANT_REGISTRY) > 0

    def test_all_keys_are_strings(self) -> None:
        for block in VARIANT_REGISTRY:
            assert isinstance(block, str)

    def test_all_values_are_tuples_of_strings(self) -> None:
        for block, variants in VARIANT_REGISTRY.items():
            assert isinstance(variants, tuple), f"{block} value is not a tuple"
            for v in variants:
                assert isinstance(v, str), f"{block} variant {v!r} is not str"

    def test_known_blocks_present(self) -> None:
        expected = {"alert", "badge", "btn", "surface", "toast"}
        missing = expected - set(VARIANT_REGISTRY)
        assert not missing, f"expected blocks missing: {missing}"

    def test_alert_variants(self) -> None:
        assert "info" in VARIANT_REGISTRY["alert"]
        assert "success" in VARIANT_REGISTRY["alert"]
        assert "warning" in VARIANT_REGISTRY["alert"]
        assert "error" in VARIANT_REGISTRY["alert"]

    def test_no_duplicate_variants(self) -> None:
        for block, variants in VARIANT_REGISTRY.items():
            assert len(variants) == len(set(variants)), f"{block} has duplicate variants"


class TestSizeRegistry:
    """SIZE_REGISTRY structure and content checks."""

    def test_registry_is_nonempty(self) -> None:
        assert len(SIZE_REGISTRY) > 0

    def test_all_values_are_tuples_of_strings(self) -> None:
        for block, sizes in SIZE_REGISTRY.items():
            assert isinstance(sizes, tuple), f"{block} value is not a tuple"
            for s in sizes:
                assert isinstance(s, str), f"{block} size {s!r} is not str"

    def test_known_blocks_present(self) -> None:
        expected = {"btn", "modal"}
        missing = expected - set(SIZE_REGISTRY)
        assert not missing, f"expected blocks missing: {missing}"

    def test_btn_sizes(self) -> None:
        assert "sm" in SIZE_REGISTRY["btn"]
        assert "md" in SIZE_REGISTRY["btn"]
        assert "lg" in SIZE_REGISTRY["btn"]

    def test_no_duplicate_sizes(self) -> None:
        for block, sizes in SIZE_REGISTRY.items():
            assert len(sizes) == len(set(sizes)), f"{block} has duplicate sizes"


class TestDescriptorCoverage:
    """Every template in chirpui/ must have a ComponentDescriptor (or be excluded)."""

    # Composition-only templates with no chirpui-* CSS blocks of their own.
    EXCLUDED = frozenset(
        {
            "app_layout",
            "app_shell_layout",
            "ascii_icon",
            "auth",
            "bento_grid",
            "command_bar",
            "config_card",
            "config_dashboard",
            "islands",
            "layout",
            "modal_overlay",
            "nav_link",
            "oob",
            "search_header",
            "share_menu",
            "shell_frame",
            "state_primitives",
            "status_with_hint",
            "tabbed_page_layout",
            "tabs_panels",
        }
    )

    def test_descriptor_coverage(self) -> None:
        """All non-excluded templates must have at least one COMPONENTS entry."""
        from pathlib import Path

        from chirp_ui.components import COMPONENTS

        templates = {p.stem for p in Path("src/chirp_ui/templates/chirpui").glob("*.html")}
        registered = {c.template.replace(".html", "") for c in COMPONENTS.values() if c.template}
        unregistered = sorted(templates - registered - self.EXCLUDED)
        assert not unregistered, (
            f"Templates without ComponentDescriptor (add descriptor or exclude): {unregistered}"
        )

    def test_excluded_templates_exist(self) -> None:
        """Every excluded template must actually exist (stale exclusions are bugs)."""
        from pathlib import Path

        templates = {p.stem for p in Path("src/chirp_ui/templates/chirpui").glob("*.html")}
        stale = sorted(self.EXCLUDED - templates)
        assert not stale, f"Excluded templates no longer exist: {stale}"
