"""Composite contract test — every documented composite renders cleanly.

Each fixture in ``tests/fixtures/composite_invocations.py`` is rendered with
``warnings.catch_warnings(record=True)``. The test fails if any
``ChirpUIValidationWarning`` was emitted. ``ChirpUIDeprecationWarning`` is
allowed (those are intentional and predate the deprecation timeline).

The shared ``env`` fixture in ``conftest.py`` registers minimal stubs for
filters that bypass validation (e.g. ``bem``). This test overrides those
stubs with the real :mod:`chirp_ui.filters` implementations so the
contract exercises the same validation paths apps see in production.

See ``.context/composite-contracts-plan.md`` for design rationale.
"""

import warnings

import pytest
from kida import Environment

from chirp_ui.filters import bem, validate_variant, validate_variant_block
from chirp_ui.validation import ChirpUIDeprecationWarning, ChirpUIValidationWarning, set_strict
from tests.fixtures.composite_invocations import COMPOSITE_FIXTURES, CompositeFixture


@pytest.fixture
def contract_env(env: Environment) -> Environment:
    """Env with real validating filters swapped in over conftest's stubs."""
    env.update_filters(
        {
            "bem": bem,
            "validate_variant": validate_variant,
            "validate_variant_block": validate_variant_block,
        }
    )
    return env


@pytest.fixture(autouse=True)
def _disable_strict_mode():
    """Composite tests rely on warnings being captured, not raised."""
    set_strict(False)
    yield
    set_strict(False)


def _format_failure(fixture: CompositeFixture, offenders: list[warnings.WarningMessage]) -> str:
    lines = [
        f"composite fixture {fixture.name!r} ({fixture.template}) emitted "
        f"{len(offenders)} validation warning(s):",
    ]
    lines.extend(f"  - {w.category.__name__}: {w.message}" for w in offenders)
    lines.append("")
    lines.append("Source:")
    lines.append(f"  {fixture.source}")
    return "\n".join(lines)


@pytest.mark.parametrize("fixture", COMPOSITE_FIXTURES, ids=lambda f: f.name)
def test_composite_renders_without_validation_warnings(
    contract_env: Environment, fixture: CompositeFixture
) -> None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        template = contract_env.from_string(fixture.source, name=f"contract:{fixture.name}")
        html = template.render(**fixture.context)

    offenders = [
        w
        for w in caught
        if isinstance(w.category, type)
        and issubclass(w.category, ChirpUIValidationWarning)
        and not issubclass(w.category, ChirpUIDeprecationWarning)
    ]
    assert not offenders, _format_failure(fixture, offenders)
    assert html, f"composite fixture {fixture.name!r} produced no output"
