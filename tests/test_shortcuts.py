"""Unit tests for chirp_ui.shortcuts (keyboard shortcut catalog)."""

import json

from kida import Environment

from chirp_ui.shortcuts import DEFAULT_SHORTCUTS, Shortcut, shortcuts_by_category, shortcuts_json


def test_shortcuts_by_category_covers_every_entry() -> None:
    grouped = shortcuts_by_category(DEFAULT_SHORTCUTS)
    assert sum(len(items) for items in grouped.values()) == len(DEFAULT_SHORTCUTS)


def test_shortcut_event_key_defaults_to_last_display_token() -> None:
    sc = Shortcut("palette", ("⌘", "K"), "Open palette", "open-palette", mod=True, key="k")
    assert sc.event_key() == "k"


def test_shortcuts_json_round_trip_fields() -> None:
    payload = json.loads(shortcuts_json())
    assert len(payload) == len(DEFAULT_SHORTCUTS)
    allowlisted = {entry["id"] for entry in payload if entry["allowInInput"]}
    assert allowlisted == {"escape", "send"}


def test_shortcuts_help_renders_catalog_rows(env: Environment) -> None:
    html = env.from_string(
        '{% from "chirpui/shortcuts_help.html" import shortcuts_help %}{{ shortcuts_help() }}'
    ).render()
    for sc in DEFAULT_SHORTCUTS:
        assert f'data-shortcut-id="{sc.id}"' in html
    assert html.count("data-shortcut-id=") == len(DEFAULT_SHORTCUTS)
    assert "chirpuiShortcuts" in html
