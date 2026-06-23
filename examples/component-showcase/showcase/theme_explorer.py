"""Theme explorer data for the live component-showcase page (#213)."""

from __future__ import annotations

import json
from dataclasses import dataclass

from chirp_ui.theme_packs import THEME_PACKS

__all__ = [
    "CONTRAST_PAIRS",
    "THEME_PRESETS",
    "TOKEN_JOBS",
    "ThemePreset",
    "TokenJob",
    "TokenRow",
    "list_theme_presets",
    "list_token_jobs",
]


@dataclass(frozen=True, slots=True)
class TokenRow:
    name: str
    meta: str
    kind: str = "color"


@dataclass(frozen=True, slots=True)
class TokenJob:
    id: str
    title: str
    tokens: tuple[TokenRow, ...]


@dataclass(frozen=True, slots=True)
class ThemePreset:
    id: str
    label: str
    badge: str = ""
    stylesheet: str | None = None
    theme_mode: str | None = None
    inline_tokens: tuple[tuple[str, str], ...] = ()


TOKEN_JOBS: tuple[TokenJob, ...] = (
    TokenJob(
        "page",
        "Page",
        (
            TokenRow("--chirpui-bg", "canvas"),
            TokenRow("--chirpui-bg-subtle", "bands"),
        ),
    ),
    TokenJob(
        "surface",
        "Surface",
        (
            TokenRow("--chirpui-surface", "panel"),
            TokenRow("--chirpui-border", "edge"),
        ),
    ),
    TokenJob(
        "text",
        "Text",
        (
            TokenRow("--chirpui-text", "primary"),
            TokenRow("--chirpui-text-muted", "secondary"),
        ),
    ),
    TokenJob(
        "accent",
        "Accent",
        (
            TokenRow("--chirpui-accent", "action"),
            TokenRow("--chirpui-accent-hover", "hover"),
            TokenRow("--chirpui-on-accent", "on-action"),
        ),
    ),
    TokenJob(
        "semantic",
        "Semantic",
        (
            TokenRow("--chirpui-success", "success"),
            TokenRow("--chirpui-warning", "warning"),
            TokenRow("--chirpui-error", "error"),
        ),
    ),
    TokenJob(
        "focus",
        "Focus",
        (
            TokenRow("--chirpui-focus-ring", "halo", kind="focus"),
            TokenRow("--chirpui-state-focus-outline", "keyboard", kind="outline"),
        ),
    ),
    TokenJob(
        "radius",
        "Radius",
        (
            TokenRow("--chirpui-radius-sm", "compact", kind="radius"),
            TokenRow("--chirpui-radius-lg", "panel", kind="radius"),
        ),
    ),
    TokenJob(
        "elevation",
        "Elevation",
        (
            TokenRow("--chirpui-elevation-card-rest", "rest", kind="shadow"),
            TokenRow("--chirpui-elevation-overlay", "float", kind="shadow"),
        ),
    ),
    TokenJob(
        "typography",
        "Typography",
        (
            TokenRow("--chirpui-ui-font-family", "ui", kind="type"),
            TokenRow("--chirpui-ui-lg", "scale", kind="type"),
        ),
    ),
    TokenJob(
        "motion",
        "Motion",
        (
            TokenRow("--chirpui-motion-base", "timing", kind="motion"),
            TokenRow("--chirpui-ease-standard", "curve", kind="motion"),
        ),
    ),
)

_CHIRP_THEME_INLINE: tuple[tuple[str, str], ...] = (
    ("--chirpui-bg", "#f4f1eb"),
    ("--chirpui-bg-subtle", "#fbf8f2"),
    ("--chirpui-surface", "#fffdf8"),
    ("--chirpui-surface-alt", "#f0ebe3"),
    ("--chirpui-border", "#ccd6d0"),
    ("--chirpui-text", "#111c24"),
    ("--chirpui-text-muted", "#475463"),
    ("--chirpui-accent", "#0e7490"),
    ("--chirpui-accent-hover", "#155e75"),
    ("--chirpui-success", "#0f766e"),
    ("--chirpui-warning", "#b45309"),
    ("--chirpui-error", "#be185d"),
)

THEME_PRESETS: tuple[ThemePreset, ...] = (
    ThemePreset("default", "Default tokens", badge="baseline"),
    ThemePreset("app-starter-light", "App starter light", badge="starter", theme_mode="light"),
    ThemePreset("app-starter-dark", "App starter dark", badge="starter", theme_mode="dark"),
    ThemePreset(
        "holy-light",
        "Holy light",
        badge="preset",
        stylesheet="themes/holy-light.css",
    ),
    ThemePreset(
        "chirp-theme",
        "chirp-theme",
        badge="Bengal",
        inline_tokens=_CHIRP_THEME_INLINE,
    ),
    *(
        ThemePreset(
            pack.name,
            pack.label,
            badge=pack.maturity,
            stylesheet=pack.path,
        )
        for pack in THEME_PACKS
    ),
)

CONTRAST_PAIRS: tuple[tuple[str, str, str], ...] = (
    ("accent", "--chirpui-on-accent", "--chirpui-accent"),
    ("text", "--chirpui-text", "--chirpui-bg"),
    ("muted", "--chirpui-text-muted", "--chirpui-bg-subtle"),
)


def list_token_jobs() -> tuple[TokenJob, ...]:
    return TOKEN_JOBS


def list_theme_presets() -> tuple[ThemePreset, ...]:
    return THEME_PRESETS


def theme_presets_json() -> str:
    payload = [
        {
            "id": preset.id,
            "label": preset.label,
            "stylesheet": preset.stylesheet,
            "theme_mode": preset.theme_mode,
            "inline_tokens": list(preset.inline_tokens),
        }
        for preset in THEME_PRESETS
    ]
    return json.dumps(payload)


def contrast_pairs_json() -> str:
    return json.dumps([list(pair) for pair in CONTRAST_PAIRS])
