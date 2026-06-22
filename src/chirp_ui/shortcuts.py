"""Declarative keyboard-shortcut catalog for chirp-ui.

The catalog is the single source of truth: ``shortcuts_help.html`` renders the
help modal from it, and the ``chirpuiShortcuts`` Alpine factory dispatches from
the same data (serialized via :func:`shortcuts_json`). This makes the open-webui
#17015 class of bug structurally impossible — the modal cannot advertise a
binding the handler does not run, because both read one list.

Chirp-agnostic and stdlib-only, like ``route_tabs.py`` and ``grid_state.py``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

__all__ = [
    "DEFAULT_SHORTCUTS",
    "Shortcut",
    "shortcuts_by_category",
    "shortcuts_json",
]


@dataclass(frozen=True, slots=True)
class Shortcut:
    """One keyboard shortcut.

    ``keys`` are *display* tokens rendered via ``kbd()`` in the modal (e.g.
    ``("⌘", "K")``). The handler matches on ``mod`` (ctrlKey||metaKey, unified),
    ``shift``, and :meth:`event_key`. ``allow_in_input`` opts a shortcut past the
    input-context guard (Escape, focus-composer, composer send) — everything
    else early-returns when focus is in a text field.
    """

    id: str
    keys: tuple[str, ...]
    label: str
    action: str
    category: str = "General"
    mod: bool = False
    shift: bool = False
    key: str = ""
    allow_in_input: bool = False

    def event_key(self) -> str:
        """The ``event.key`` to match, lowercased. Defaults to the last display token."""
        return (self.key or self.keys[-1]).lower()


DEFAULT_SHORTCUTS: tuple[Shortcut, ...] = (
    Shortcut("help", ("?",), "Show keyboard shortcuts", "open-help", "General", key="?"),
    Shortcut(
        "palette", ("⌘", "K"), "Open command palette", "open-palette", "General", mod=True, key="k"
    ),
    Shortcut(
        "focus-composer", ("/",), "Focus the message composer", "focus-composer", "Chat", key="/"
    ),
    Shortcut(
        "send",
        ("⌘", "↵"),
        "Send message",
        "send",
        "Chat",
        mod=True,
        key="enter",
        allow_in_input=True,
    ),
    Shortcut(
        "escape", ("Esc",), "Close / cancel", "escape", "General", key="escape", allow_in_input=True
    ),
)


def shortcuts_by_category(
    shortcuts: tuple[Shortcut, ...] = DEFAULT_SHORTCUTS,
) -> dict[str, list[Shortcut]]:
    """Group shortcuts by category for the help modal, preserving insertion order."""
    grouped: dict[str, list[Shortcut]] = {}
    for sc in shortcuts:
        grouped.setdefault(sc.category, []).append(sc)
    return grouped


def shortcuts_json(shortcuts: tuple[Shortcut, ...] = DEFAULT_SHORTCUTS) -> str:
    """Serialize the catalog for the ``chirpuiShortcuts`` Alpine factory.

    Only the handler-relevant fields are emitted (display ``keys`` stay
    server-side for the modal). Embedded in a ``<script type="application/json">``
    so the handler reads the same data the modal rendered from.
    """
    return json.dumps(
        [
            {
                "id": s.id,
                "action": s.action,
                "mod": s.mod,
                "shift": s.shift,
                "key": s.event_key(),
                "allowInInput": s.allow_in_input,
            }
            for s in shortcuts
        ]
    )
