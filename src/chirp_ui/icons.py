"""Icon registry: semantic names → Unicode glyphs for chirp-ui components.

Use the `icon` filter to resolve names in templates: `{{ "status" | icon }}` → ◎.
Unknown names pass through unchanged for backward compatibility.
"""

ICON_REGISTRY: dict[str, str] = {
    # Status / validation / run
    "status": "◎",
    "validate": "◎",
    "run": "◎",
    "activity": "◎",
    "pause": "Ⅱ",
    # Actions
    "add": "+",
    "plus": "+",
    "refresh": "↻",
    "search": "⌕",
    "magnifying-glass": "⌕",
    "reply": "↩",
    "comment": "◉",
    "share": "↗",
    "send": "→",
    "stop": "■",
    "x": "×",  # noqa: RUF001
    "file": "▤",
    "up": "▲",
    "down": "▼",
    "arrow-up": "▲",
    "arrow-down": "▼",
    "arrow-left": "←",
    "arrow-right": "→",
    "vote-up": "▲",
    "vote-down": "▼",
    "check": "✓",
    "clock": "◷",
    "eye": "◉",
    "watch": "◉",
    "follow": "★",
    "report": "↑",
    "chevron-down": "▾",
    "arrow": "▸",
    "migrate": "▸",
    "config": "▸",
    # Shapes / symbols
    "wizard": "◇",
    "diamond": "◇",
    "settings": "◇",
    "gear": "⚙",
    "bullet": "●",
    "star": "★",
    "spark": "✦",
    "✧": "✧",
    # Domain / nav
    "home": "◉",
    "grid": "⊞",
    "user": "⊙",
    "shortcut": "⌘",
    "skills": "✦",
    "logs": "⟳",
    "cloud": "☁",
    "sources": "⊞",
    "chain": "⛓",
    "link": "⟶",
    "chart": "▤",
    "bolt": "⚡︎",
    "chat": "◉",
    "list": "≡",
    "compass": "❖",
    "graduation-cap": "◓",
    # Alerts / flow
    "alert": "↑",
    "info": "◎",
    "ℹ": "ℹ",  # noqa: RUF001
    "warning": "↑",
    "dots": "⋯",
    # Writing / authoring (Dingbats U+270E-U+2712, U+2709)
    "pencil": "✏",
    "pencil-lower": "✎",
    "pencil-upper": "✐",
    "nib": "✒",
    "nib-white": "✑",
    "envelope": "✉",
}


def icon(name: str) -> str:
    """Resolve icon name to glyph; unknown names pass through."""
    return ICON_REGISTRY.get(name, name)
