"""Shared fixtures for chirp-ui tests."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any

import pytest
from kida import Environment, FileSystemLoader


TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "src" / "chirp_ui" / "templates"


def _field_errors_stub(errors: Any, field_name: str) -> Sequence[str]:
    """Stub for Chirp's ``field_errors`` filter.

    In production, this filter is provided by ``chirp.templating.filters``.
    For testing chirp-ui without Chirp, return an empty list so templates
    render without errors.
    """
    if errors is None:
        return []
    if isinstance(errors, dict):
        return errors.get(field_name, [])
    return []


@pytest.fixture
def env() -> Environment:
    """Kida environment with chirp-ui templates loaded via FileSystemLoader."""
    e = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=True,
    )
    # Register stub for Chirp's field_errors filter (used by forms.html)
    e.update_filters({"field_errors": _field_errors_stub})
    return e
