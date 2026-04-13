"""Shared test helpers for chirp-ui structural assertions."""

import re
from collections.abc import Sequence


def assert_element(
    html_str: str,
    tag: str,
    attrs: dict[str, str | None] | None = None,
    contains: str | None = None,
    *,
    absent_attrs: Sequence[str] | None = None,
) -> None:
    """Assert that *html_str* contains an element matching *tag* + *attrs*.

    Uses simple regex matching — no lxml/html.parser dependency.

    Parameters
    ----------
    html_str:
        The rendered HTML to search.
    tag:
        The HTML tag name (e.g. ``"button"``, ``"nav"``).
    attrs:
        Dict of attribute name -> expected value.  Value ``None`` means the
        attribute must be present (any value).
    contains:
        Optional text that must appear *somewhere* in *html_str* (not
        necessarily inside the matched element — keeps the helper simple).
    absent_attrs:
        Attribute names that must **not** appear on any ``<tag`` element.
    """
    attrs = attrs or {}
    # Check the tag exists at all
    tag_pattern = re.compile(rf"<{re.escape(tag)}[\s>/]", re.IGNORECASE)
    assert tag_pattern.search(html_str), f"Expected <{tag}> element not found in HTML"

    # Check each attr exists on *some* element of that tag type
    for attr_name, attr_val in attrs.items():
        if attr_val is None:
            assert re.search(
                rf"<{re.escape(tag)}\b[^>]*\b{re.escape(attr_name)}=",
                html_str,
                re.IGNORECASE,
            ), f'Expected attribute "{attr_name}" on <{tag}> not found'
        else:
            assert re.search(
                rf'<{re.escape(tag)}\b[^>]*\b{re.escape(attr_name)}="{re.escape(attr_val)}"',
                html_str,
                re.IGNORECASE,
            ), f'Expected {attr_name}="{attr_val}" on <{tag}> not found'

    # Check absent attrs
    for attr_name in absent_attrs or []:
        assert not re.search(
            rf"<{re.escape(tag)}\b[^>]*\b{re.escape(attr_name)}=",
            html_str,
            re.IGNORECASE,
        ), f'Attribute "{attr_name}" should not appear on <{tag}>'

    if contains is not None:
        assert contains in html_str, f"Expected text {contains!r} not found in HTML"
