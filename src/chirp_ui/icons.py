"""Icon registry: semantic names → Unicode glyphs for chirp-ui components.

Use the `icon` filter to resolve names in templates: `{{ "status" | icon }}` → ◎.
Unknown names pass through unchanged for backward compatibility.
"""

ICON_REGISTRY: dict[str, str] = {
    # Status / validation / run
    "status": "◎",
    "validate": "◎",
    "run": "◎",
    # Actions
    "add": "+",
    "refresh": "↻",
    "search": "⌕",
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
    # Alerts / flow
    "alert": "↑",
    "dots": "⋯",
    # Writing / authoring (Dingbats U+270E–U+2712, U+2709)
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
