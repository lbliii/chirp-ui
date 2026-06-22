"""Unit tests for chirp_ui.text_fragment (citation deep links)."""

from chirp_ui.text_fragment import build_text_fragment_url


def test_no_chunk_returns_href_unchanged() -> None:
    assert build_text_fragment_url("https://x.test/doc", None) == "https://x.test/doc"
    assert build_text_fragment_url("https://x.test/doc", "") == "https://x.test/doc"


def test_simple_text_fragment() -> None:
    assert (
        build_text_fragment_url("https://x.test/doc", "exact quote")
        == "https://x.test/doc#:~:text=exact%20quote"
    )


def test_encodes_hyphen_in_chunk() -> None:
    url = build_text_fragment_url("https://x.test/doc", "a-b")
    assert "%2D" in url


def test_existing_hash_appends_text_directive() -> None:
    assert (
        build_text_fragment_url("https://x.test/doc#section", "quote")
        == "https://x.test/doc#section:~:text=quote"
    )


def test_existing_text_directive_appends_with_ampersand() -> None:
    href = "https://x.test/doc#:~:text=first"
    result = build_text_fragment_url(href, "second")
    assert result.startswith(href)
    assert "&text=" in result
