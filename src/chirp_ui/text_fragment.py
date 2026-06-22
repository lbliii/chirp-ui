"""Text-fragment deep-link helper for chirp-ui citation UI.

Pure-URL, stdlib-only (Chirp-agnostic, like route_tabs / grid_state).
Builds ``#:~:text=`` scroll-to-text-fragment links.
"""

from urllib.parse import quote

__all__ = ["build_text_fragment_url"]


def build_text_fragment_url(href: str, chunk: str | None = None) -> str:
    """Return ``href`` with a text-fragment so the browser scrolls to/highlights ``chunk``.

    >>> build_text_fragment_url("https://x.test/doc", "exact quote")
    'https://x.test/doc#:~:text=exact%20quote'

    No chunk -> href unchanged. An existing ``#fragment`` is preserved and the
    text directive is appended with the ``:~:`` delimiter per the spec.
    Percent-encodes ``-`` , ``,`` and ``&`` because they are text-directive
    syntax characters.
    """
    if not chunk:
        return href
    encoded = quote(chunk, safe="").replace("-", "%2D")
    directive = f"text={encoded}"
    if "#" in href:
        base, frag = href.split("#", 1)
        if ":~:" in frag:
            return f"{href}&{directive}"
        return f"{base}#{frag}:~:{directive}"
    return f"{href}#:~:{directive}"
