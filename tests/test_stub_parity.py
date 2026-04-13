"""Stub-vs-real parity tests.

Ensures test stubs in conftest.py produce identical output to the real
filter implementations in chirp_ui.filters. Prevents drift between test
and production behavior.
"""

from __future__ import annotations

import contextlib
import importlib.util
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any

import pytest

from chirp_ui.filters import (
    bem,
    field_errors,
    html_attrs,
    validate_size,
    validate_variant,
    validate_variant_block,
)
from chirp_ui.validation import ChirpUIValidationWarning

_conftest_path = Path(__file__).parent / "conftest.py"
_spec = importlib.util.spec_from_file_location("_conftest", _conftest_path)
_conftest = importlib.util.module_from_spec(_spec)
sys.modules["_conftest"] = _conftest
_spec.loader.exec_module(_conftest)

_bem_stub = _conftest._bem_stub
_field_errors_stub = _conftest._field_errors_stub
_html_attrs_stub = _conftest._html_attrs_stub
_validate_size_stub = _conftest._validate_size_stub
_validate_variant_block_stub = _conftest._validate_variant_block_stub
_validate_variant_stub = _conftest._validate_variant_stub


# ---------------------------------------------------------------------------
# html_attrs parity
# ---------------------------------------------------------------------------


class TestHtmlAttrsParity:
    """_html_attrs_stub must produce identical output to html_attrs."""

    @pytest.mark.parametrize(
        "value",
        [
            None,
            False,
            "",
            "  ",
            " data-x",
            ' id="foo"',
            {"class": "btn"},
            {"hx-post": "/save", "hx-target": "#out"},
            {"disabled": True},
            {"hidden": False},
            {"data-val": None},
            {"data-config": {"key": "val", "num": 42}},
            {"data-list": [1, 2, 3]},
            {"data-count": 7},
            {"data-name": "O'Reilly & Sons"},
            {"a": True, "b": "x", "c": None, "d": False},
            OrderedDict([("z", "1"), ("a", "2")]),
        ],
        ids=[
            "none",
            "false",
            "empty-str",
            "whitespace",
            "raw-leading-space",
            "raw-attr-str",
            "dict-simple",
            "dict-hx",
            "dict-bool-true",
            "dict-bool-false",
            "dict-none-value",
            "dict-nested-dict",
            "dict-list",
            "dict-int",
            "dict-special-chars",
            "dict-mixed",
            "ordered-dict",
        ],
    )
    def test_parity(self, value: Any) -> None:
        real = html_attrs(value)
        stub = _html_attrs_stub(value)
        assert str(real) == str(stub), f"Divergence for {value!r}: real={real!r}, stub={stub!r}"


# ---------------------------------------------------------------------------
# validate_variant parity
# ---------------------------------------------------------------------------

ALLOWED_VARIANTS = ("", "primary", "secondary", "danger")


class TestValidateVariantParity:
    """_validate_variant_stub must produce identical output to validate_variant."""

    @pytest.mark.parametrize(
        ("value", "default"),
        [
            ("primary", ""),
            ("", ""),
            ("unknown", ""),
            ("unknown", "primary"),
            ("danger", "primary"),
        ],
        ids=["valid", "empty", "invalid-no-default", "invalid-with-default", "valid-with-default"],
    )
    def test_parity(self, value: str, default: str) -> None:
        with (
            pytest.warns(match="chirp-ui")
            if value and value not in ALLOWED_VARIANTS
            else _no_warn()
        ):
            real = validate_variant(value, ALLOWED_VARIANTS, default)
        with (
            pytest.warns(match="chirp-ui")
            if value and value not in ALLOWED_VARIANTS
            else _no_warn()
        ):
            stub = _validate_variant_stub(value, ALLOWED_VARIANTS, default)
        assert real == stub, (
            f"Divergence for ({value!r}, {default!r}): real={real!r}, stub={stub!r}"
        )


# ---------------------------------------------------------------------------
# validate_variant_block parity
# ---------------------------------------------------------------------------


class TestValidateVariantBlockParity:
    """_validate_variant_block_stub must produce identical output to validate_variant_block."""

    @pytest.mark.parametrize(
        ("value", "block", "default"),
        [
            ("primary", "btn", ""),
            ("", "btn", ""),
            ("bogus", "btn", ""),
            ("default", "surface", "default"),
            ("muted", "surface", "default"),
        ],
        ids=["valid-btn", "empty-btn", "invalid-btn", "default-surface", "muted-surface"],
    )
    def test_parity(self, value: str, block: str, default: str) -> None:
        with (
            pytest.warns(match="chirp-ui")
            if value and value not in _get_allowed(block)
            else _no_warn()
        ):
            real = validate_variant_block(value, block, default)
        with (
            pytest.warns(match="chirp-ui")
            if value and value not in _get_allowed(block)
            else _no_warn()
        ):
            stub = _validate_variant_block_stub(value, block, default)
        assert real == stub, (
            f"Divergence for ({value!r}, {block!r}, {default!r}): real={real!r}, stub={stub!r}"
        )


# ---------------------------------------------------------------------------
# validate_size parity
# ---------------------------------------------------------------------------


class TestValidateSizeParity:
    """_validate_size_stub must produce identical output to validate_size."""

    @pytest.mark.parametrize(
        ("value", "block", "default"),
        [
            ("sm", "modal", "md"),
            ("", "modal", "md"),
            ("huge", "modal", "md"),
            ("", "btn", ""),
        ],
        ids=["valid-modal", "empty-modal", "invalid-modal", "empty-btn"],
    )
    def test_parity(self, value: str, block: str, default: str) -> None:
        from chirp_ui.validation import SIZE_REGISTRY

        allowed = SIZE_REGISTRY.get(block, ())
        should_warn = bool(value and allowed and value not in allowed)
        with pytest.warns(match="chirp-ui") if should_warn else _no_warn():
            real = validate_size(value, block, default)
        with pytest.warns(match="chirp-ui") if should_warn else _no_warn():
            stub = _validate_size_stub(value, block, default)
        assert real == stub, (
            f"Divergence for ({value!r}, {block!r}, {default!r}): real={real!r}, stub={stub!r}"
        )


# ---------------------------------------------------------------------------
# bem parity
# ---------------------------------------------------------------------------


class TestBemParity:
    """_bem_stub must produce identical class strings to bem."""

    @pytest.mark.parametrize(
        ("block", "kwargs"),
        [
            ("btn", {}),
            ("btn", {"variant": "primary"}),
            ("btn", {"variant": "primary", "size": "lg"}),
            ("btn", {"modifier": "loading"}),
            ("btn", {"modifier": ["loading"]}),
            ("btn", {"cls": "extra"}),
            ("surface", {"variant": "muted", "modifier": ["full", "no-padding"], "cls": "my-cls"}),
        ],
        ids=["bare", "variant", "variant+size", "modifier-str", "modifier-list", "cls", "complex"],
    )
    def test_parity(self, block: str, kwargs: dict[str, Any]) -> None:
        real = bem(block, **kwargs)
        stub = _bem_stub(block, **kwargs)
        assert real == stub, (
            f"Divergence for bem({block!r}, {kwargs}): real={real!r}, stub={stub!r}"
        )


# ---------------------------------------------------------------------------
# field_errors parity
# ---------------------------------------------------------------------------


class TestFieldErrorsParity:
    """_field_errors_stub must produce identical output to field_errors."""

    @pytest.mark.parametrize(
        ("errors", "field"),
        [
            (None, "name"),
            ({}, "name"),
            ({"name": ["required"]}, "name"),
            ({"name": ["required"]}, "email"),
            (OrderedDict([("name", ["err"])]), "name"),
            ({"name": {"nested": "err"}}, "name"),
            ({"name": "single"}, "name"),
            ({"name": 42}, "name"),
        ],
        ids=[
            "none",
            "empty-dict",
            "has-errors",
            "missing-field",
            "ordered-dict",
            "nested-dict",
            "bare-string",
            "int-value",
        ],
    )
    def test_parity(self, errors: Any, field: str) -> None:
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ChirpUIValidationWarning)
            real = field_errors(errors, field)
            stub = _field_errors_stub(errors, field)
        assert list(real) == list(stub), (
            f"Divergence for ({errors!r}, {field!r}): real={real!r}, stub={stub!r}"
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@contextlib.contextmanager
def _no_warn():
    """Context manager that does nothing — used as else-branch for pytest.warns."""
    yield


def _get_allowed(block: str) -> tuple[str, ...]:
    from chirp_ui.validation import VARIANT_REGISTRY

    return VARIANT_REGISTRY.get(block, ())
