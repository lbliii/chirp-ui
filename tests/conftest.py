"""Shared fixtures for chirp-ui tests."""

from pathlib import Path

import pytest
from kida import Environment, FileSystemLoader


TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "src" / "chirp_ui" / "templates"


@pytest.fixture
def env() -> Environment:
    """Kida environment with chirp-ui templates loaded via FileSystemLoader."""
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=True,
    )
