"""Unit tests for chirp_ui.grid_state (issue #200).

No browser, no Chirp — the helper is stdlib + dataclasses only, mirroring
tests/test_route_tabs-style coverage. Locks the typed-projection contract the
data_grid macro renders from.
"""

from urllib.parse import parse_qs, urlsplit

import pytest

from chirp_ui.grid_state import (
    Column,
    ColumnSort,
    GridSort,
    column_aria_sort,
    parse_sort,
    selection_state,
    sort_columns,
    sort_query,
)

# ── parse_sort ─────────────────────────────────────────────────────────


def test_parse_sort_ascending() -> None:
    assert parse_sort("name") == GridSort("name", "asc")


def test_parse_sort_descending_dash_prefix() -> None:
    assert parse_sort("-name") == GridSort("name", "desc")


def test_parse_sort_empty_returns_default() -> None:
    assert parse_sort("", default_key="created") == GridSort("created", "asc")
    assert parse_sort(None, default_key="created") == GridSort("created", "asc")


def test_parse_sort_whitespace_returns_default() -> None:
    assert parse_sort("   ", default_key="created") == GridSort("created", "asc")


def test_parse_sort_unknown_key_clamps_to_default_when_allowed_given() -> None:
    got = parse_sort("evil", default_key="name", allowed=("name", "status"))
    assert got == GridSort("name", "asc")


def test_parse_sort_allowed_key_passes() -> None:
    got = parse_sort("-status", default_key="name", allowed=("name", "status"))
    assert got == GridSort("status", "desc")


def test_parse_sort_no_allowlist_accepts_any_key() -> None:
    assert parse_sort("arbitrary") == GridSort("arbitrary", "asc")


def test_parse_sort_default_direction_respected() -> None:
    assert parse_sort(None, default_key="created", default_direction="desc") == GridSort(
        "created", "desc"
    )


def test_parse_sort_bad_default_direction_clamped() -> None:
    assert parse_sort(None, default_key="x", default_direction="sideways").direction == "asc"


def test_parse_sort_bare_dash_returns_default() -> None:
    assert parse_sort("-", default_key="name") == GridSort("name", "asc")


# ── sort_columns ───────────────────────────────────────────────────────

COLS = [
    Column("name", "Name", sortable=True),
    Column("status", "Status", sortable=True, align="center"),
    Column("seats", "Seats", sortable=True, align="right"),
    Column("notes", "Notes", sortable=False),
]


def test_sort_columns_exactly_one_active() -> None:
    cols = sort_columns(COLS, GridSort("status", "asc"), "/users")
    active = [c for c in cols if c.is_active]
    assert len(active) == 1
    assert active[0].key == "status"


def test_sort_columns_single_aria_sort_invariant() -> None:
    cols = sort_columns(COLS, GridSort("status", "desc"), "/users")
    non_none = [c for c in cols if c.aria_sort != "none"]
    assert len(non_none) == 1
    assert non_none[0].key == "status"
    assert non_none[0].aria_sort == "descending"


def test_sort_columns_active_ascending_aria() -> None:
    cols = {c.key: c for c in sort_columns(COLS, GridSort("name", "asc"), "/users")}
    assert cols["name"].aria_sort == "ascending"


def test_sort_columns_inactive_columns_are_none() -> None:
    cols = {c.key: c for c in sort_columns(COLS, GridSort("name", "asc"), "/users")}
    assert cols["status"].aria_sort == "none"
    assert cols["seats"].aria_sort == "none"


def test_sort_columns_non_sortable_always_none_and_no_url() -> None:
    cols = {c.key: c for c in sort_columns(COLS, GridSort("notes", "asc"), "/users")}
    assert cols["notes"].aria_sort == "none"
    assert cols["notes"].is_active is False
    assert cols["notes"].next_url == ""


def test_sort_columns_toggle_active_ascending_requests_descending() -> None:
    cols = {c.key: c for c in sort_columns(COLS, GridSort("name", "asc"), "/users")}
    q = parse_qs(urlsplit(cols["name"].next_url).query)
    assert q["sort"] == ["-name"]


def test_sort_columns_toggle_active_descending_requests_ascending() -> None:
    cols = {c.key: c for c in sort_columns(COLS, GridSort("name", "desc"), "/users")}
    q = parse_qs(urlsplit(cols["name"].next_url).query)
    assert q["sort"] == ["name"]


def test_sort_columns_inactive_requests_ascending() -> None:
    cols = {c.key: c for c in sort_columns(COLS, GridSort("name", "asc"), "/users")}
    q = parse_qs(urlsplit(cols["status"].next_url).query)
    assert q["sort"] == ["status"]


def test_sort_columns_extra_params_survive_in_next_url() -> None:
    cols = {
        c.key: c
        for c in sort_columns(
            COLS, GridSort("name", "asc"), "/users", extra_params={"q": "ada", "page": "2"}
        )
    }
    q = parse_qs(urlsplit(cols["status"].next_url).query)
    assert q["q"] == ["ada"]
    assert q["page"] == ["2"]
    assert q["sort"] == ["status"]


def test_sort_columns_empty_extra_param_dropped() -> None:
    cols = {
        c.key: c
        for c in sort_columns(COLS, GridSort("name", "asc"), "/users", extra_params={"q": ""})
    }
    q = parse_qs(urlsplit(cols["status"].next_url).query)
    assert "q" not in q


def test_sort_columns_preserves_existing_query_and_replaces_sort() -> None:
    cols = {c.key: c for c in sort_columns(COLS, GridSort("name", "asc"), "/users?q=ada&sort=old")}
    q = parse_qs(urlsplit(cols["status"].next_url).query)
    assert q["q"] == ["ada"]
    assert q["sort"] == ["status"]  # old sort replaced, not duplicated


def test_sort_columns_custom_param_name() -> None:
    cols = {c.key: c for c in sort_columns(COLS, GridSort("name", "asc"), "/users", param="order")}
    q = parse_qs(urlsplit(cols["status"].next_url).query)
    assert q["order"] == ["status"]


def test_sort_columns_accepts_dict_columns() -> None:
    cols = sort_columns(
        [{"key": "name", "label": "Name", "sortable": True}],
        GridSort("name", "asc"),
        "/users",
    )
    assert isinstance(cols[0], ColumnSort)
    assert cols[0].aria_sort == "ascending"
    assert cols[0].label == "Name"


def test_sort_columns_carries_align() -> None:
    cols = {c.key: c for c in sort_columns(COLS, GridSort("name", "asc"), "/users")}
    assert cols["status"].align == "center"
    assert cols["seats"].align == "right"


# ── column_aria_sort / sort_query primitives ─────────────────────────────


def test_column_aria_sort_primitive() -> None:
    assert column_aria_sort("name", GridSort("name", "asc")) == "ascending"
    assert column_aria_sort("name", GridSort("name", "desc")) == "descending"
    assert column_aria_sort("status", GridSort("name", "asc")) == "none"
    assert column_aria_sort("", GridSort("", "asc")) == "none"


def test_sort_query_primitive() -> None:
    assert sort_query("name", GridSort("name", "asc")) == "sort=-name"
    assert sort_query("name", GridSort("name", "desc")) == "sort=name"
    assert sort_query("status", GridSort("name", "asc")) == "sort=status"
    assert sort_query("name", GridSort("name", "asc"), param="order") == "order=-name"


# ── selection_state ──────────────────────────────────────────────────────


def test_selection_state_count() -> None:
    sel = selection_state(["a", "b"], page_ids=["a", "b", "c"], total=10)
    assert sel.count == 2


def test_selection_state_all_selected_page_scoped() -> None:
    sel = selection_state(["a", "b", "c"], page_ids=["a", "b", "c"], total=99)
    # all page rows selected -> page-scoped all_selected True even though total=99
    assert sel.all_selected is True
    assert sel.partial is False
    assert sel.none_selected is False


def test_selection_state_partial() -> None:
    sel = selection_state(["a"], page_ids=["a", "b", "c"])
    assert sel.partial is True
    assert sel.all_selected is False
    assert sel.none_selected is False


def test_selection_state_none_selected() -> None:
    sel = selection_state([], page_ids=["a", "b", "c"])
    assert sel.none_selected is True
    assert sel.all_selected is False
    assert sel.partial is False


def test_selection_state_empty_page_is_not_all_selected() -> None:
    sel = selection_state(["a"], page_ids=[])
    assert sel.all_selected is False
    assert sel.none_selected is True


def test_selection_state_none_selected_ids_tolerated() -> None:
    sel = selection_state(None, page_ids=["a", "b"])
    assert sel.count == 0
    assert sel.none_selected is True


def test_selection_state_coerces_ids_to_str() -> None:
    sel = selection_state([1, 2], page_ids=[1, 2, 3])
    assert sel.is_selected("1") is True
    assert sel.is_selected(1) is True  # is_selected coerces too
    assert sel.is_selected("3") is False


def test_selection_state_selection_can_exceed_page() -> None:
    # ids selected on other pages are retained in the set but don't affect
    # page-scoped all_selected.
    sel = selection_state(["a", "b", "x", "y"], page_ids=["a", "b"], total=50)
    assert sel.count == 4
    assert sel.all_selected is True


def test_selection_state_is_frozen() -> None:
    sel = selection_state(["a"], page_ids=["a"])
    with pytest.raises((AttributeError, Exception)):
        sel.total = 5  # type: ignore[misc]
