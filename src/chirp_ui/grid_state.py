"""Server-driven data-grid state helpers for chirp-ui (issue #200).

Deliberately modeled on :mod:`chirp_ui.route_tabs`: stdlib + dataclasses only,
no ``import chirp`` and no ``import kida``. The module is fully unit-testable
with plain pytest and ``ty``-checkable without a render or a Chirp app
("works without Chirp, better with Chirp").

Two concerns, two analogs of ``route_tabs.tab_is_active``:

* **Sort.** :func:`parse_sort` turns a raw ``?sort=`` query value into a typed
  :class:`GridSort`; :func:`sort_columns` projects a list of :class:`Column`
  declarations into :class:`ColumnSort` rows that carry the ``aria_sort`` value
  and the fully-built toggle ``next_url`` the macro renders **but never
  computes**. The same :class:`GridSort` the route uses to actually order rows
  produces the rendered ``aria-sort`` and next-request, so server data and
  advertised UI cannot drift.

* **Selection.** :func:`selection_state` normalizes request-derived ids into a
  :class:`SelectionState` whose props (``count``, ``all_selected``,
  ``none_selected``, ``partial``) seed the select-all checkbox server-side, so
  selection is correct on a full load even with JavaScript off. The Alpine
  factory owns live in-page toggling between requests.

Example (Chirp route)::

    from chirp_ui import Column, parse_sort, sort_columns, selection_state

    COLS = [
        Column("name", "Name", sortable=True),
        Column("status", "Status", sortable=True, align="center"),
        Column("seats", "Seats", sortable=True, align="right",
               width="1fr", mobile_width="80px", resizable=True),
    ]

``width``, ``mobile_width``, and ``resizable`` are layout hints for the future
opt-in ARIA-grid renderer (issue #261). Table mode ignores them today.

    sort = parse_sort(req.query.get("sort"), default_key="name",
                      allowed=tuple(c.key for c in COLS))
    rows = query_users(order_by=sort.key, desc=(sort.direction == "desc"))
    cols = sort_columns(COLS, sort, base_url="/users",
                        extra_params={"q": req.query.get("q", "")})
    sel = selection_state(req.query.getlist("ids"),
                          page_ids=[u.id for u in rows], total=count_users())
"""

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

__all__ = [
    "Column",
    "ColumnSort",
    "GridSort",
    "SelectionState",
    "column_aria_sort",
    "parse_sort",
    "selection_state",
    "sort_columns",
    "sort_query",
]

_ASC = "asc"
_DESC = "desc"
_DIRECTIONS = (_ASC, _DESC)


@dataclass(frozen=True, slots=True)
class Column:
    """A column declaration — the developer-authored input to the grid.

    ``key`` is the *stable* sort key sent to the server (never ``label|lower``);
    renaming ``label`` or shipping duplicate/i18n labels never breaks sorting.

    v1 does not expose per-column pinning: the grid pins the **first visual
    column** via ``sticky_first_col=true`` (a CSS ``:first-child`` rule), not an
    arbitrary column. A ``frozen`` flag was deliberately *not* shipped so the
    public surface advertises no pinning contract the renderer cannot honor.

    ``width``, ``mobile_width``, and ``resizable`` seed the ARIA-grid-over-div
    variant (issue #261). Real-``<table>`` mode ignores them — callers can set
    them now without changing table rendering.
    """

    key: str
    label: str
    sortable: bool = False
    align: str = ""
    width: str | None = None
    mobile_width: str | None = None
    resizable: bool = False


@dataclass(frozen=True, slots=True)
class GridSort:
    """The typed current-sort state. ``direction`` is ``"asc"`` or ``"desc"``."""

    key: str = ""
    direction: str = _ASC


@dataclass(frozen=True, slots=True)
class ColumnSort:
    """A projected column ready to render.

    The macro reads :attr:`aria_sort` and :attr:`next_url` directly; it never
    derives sort state. ``aria_sort`` is one of ``"ascending"``,
    ``"descending"``, ``"none"``; ``next_url`` is the fully-built toggle URL.
    """

    key: str
    label: str
    align: str
    sortable: bool
    aria_sort: str
    is_active: bool
    next_url: str


@dataclass(frozen=True, slots=True)
class SelectionState:
    """Server-authoritative selection snapshot for the current page.

    ``selected`` is the full cross-request selection; ``page_ids`` are the ids
    rendered on this page; ``total`` is the grand result-set size (or ``None``).
    The ``all_selected`` / ``partial`` props are **page-scoped** — they describe
    the visible page, not the entire result set (cross-page "select all N
    matching" is out of scope for v1).
    """

    selected: frozenset[str]
    page_ids: tuple[str, ...]
    total: int | None = None

    @property
    def count(self) -> int:
        """Number of selected ids across all requests."""
        return len(self.selected)

    @property
    def all_selected(self) -> bool:
        """True when every visible page id is selected (page has rows)."""
        return bool(self.page_ids) and all(pid in self.selected for pid in self.page_ids)

    @property
    def none_selected(self) -> bool:
        """True when no visible page id is selected."""
        return not any(pid in self.selected for pid in self.page_ids)

    @property
    def partial(self) -> bool:
        """True when some-but-not-all visible page ids are selected.

        Seeds the select-all checkbox's server-side indeterminate state.
        """
        return not self.none_selected and not self.all_selected

    def is_selected(self, row_id: str) -> bool:
        """True when ``row_id`` is in the selection (templates call this)."""
        return str(row_id) in self.selected


def _normalize_direction(direction: str | None) -> str:
    return direction if direction in _DIRECTIONS else _ASC


def parse_sort(
    raw: str | None,
    *,
    default_key: str = "",
    default_direction: str = _ASC,
    allowed: Sequence[str] = (),
) -> GridSort:
    """Turn a raw ``?sort=`` value into a typed :class:`GridSort`.

    ``"name"`` → ascending, ``"-name"`` → descending. Unknown or empty keys
    clamp to ``default_key`` — the :func:`route_tabs.tab_is_active` empty-href
    guard analog, defensive against arbitrary query input. When ``allowed`` is
    given, a key outside it also clamps to the default.
    """
    default_direction = _normalize_direction(default_direction)
    fallback = GridSort(default_key, default_direction)
    if not raw:
        return fallback
    value = raw.strip()
    if not value:
        return fallback
    if value.startswith("-"):
        key, direction = value[1:], _DESC
    else:
        key, direction = value, _ASC
    if not key:
        return fallback
    if allowed and key not in allowed:
        return fallback
    return GridSort(key, direction)


def _build_url(
    base_url: str, sort_value: str, param: str, extra_params: Mapping[str, str] | None
) -> str:
    """Return ``base_url`` with ``param`` set to ``sort_value``, preserving query.

    Existing query params on ``base_url`` are kept; ``extra_params`` (e.g. an
    active filter query) are merged in so a sort click does not drop a filter.
    Empty ``extra_params`` values are dropped.
    """
    split = urlsplit(base_url)
    pairs: list[tuple[str, str]] = [
        (k, v) for k, v in parse_qsl(split.query, keep_blank_values=False) if k != param
    ]
    if extra_params:
        for k, v in extra_params.items():
            if v is None or v == "":
                continue
            pairs = [(pk, pv) for pk, pv in pairs if pk != k]
            pairs.append((str(k), str(v)))
    pairs.append((param, sort_value))
    query = urlencode(pairs)
    return urlunsplit((split.scheme, split.netloc, split.path, query, split.fragment))


def column_aria_sort(column_key: str, sort: GridSort) -> str:
    """Return the ``aria-sort`` value for ``column_key`` given ``sort``.

    Standalone projection primitive for callers who hand-render a single
    ``<th>``. Returns ``"ascending"`` / ``"descending"`` when this column is the
    active sort, else ``"none"``.
    """
    if column_key and column_key == sort.key:
        return "ascending" if sort.direction == _ASC else "descending"
    return "none"


def sort_query(column_key: str, sort: GridSort, param: str = "sort") -> str:
    """Return the ``?param=value`` query string that toggles ``column_key``.

    Standalone projection primitive. An active ascending column requests
    ``-key`` (descending); an active descending column requests ``key``
    (ascending); an inactive column requests ``key`` (ascending).
    """
    value = f"-{column_key}" if column_key == sort.key and sort.direction == _ASC else column_key
    return urlencode({param: value})


def sort_columns(
    columns: Sequence[Column | Mapping[str, object]],
    sort: GridSort,
    base_url: str,
    *,
    param: str = "sort",
    extra_params: Mapping[str, str] | None = None,
) -> list[ColumnSort]:
    """Project ``columns`` into renderable :class:`ColumnSort` rows.

    The :func:`route_tabs.tab_is_active` analog for tables. For each column it
    computes ``is_active`` (``col.sortable and col.key == sort.key``),
    ``aria_sort`` (``ascending`` / ``descending`` when active+sortable, else
    ``none``) and the toggled ``next_url`` (active+asc → request ``-key``;
    active+desc → request ``key``; inactive → request ``key`` ascending),
    preserving ``extra_params`` so an active filter query survives a sort click.

    Exactly one column is marked active for a given :class:`GridSort`, so the
    single-sort + single ``aria-sort`` invariant is structural, not asserted in
    a template branch.
    """
    out: list[ColumnSort] = []
    for raw in columns:
        col = _coerce_column(raw)
        is_active = col.sortable and bool(col.key) and col.key == sort.key
        if not col.sortable or not col.key:
            aria_sort = "none"
        elif is_active:
            aria_sort = "ascending" if sort.direction == _ASC else "descending"
        else:
            aria_sort = "none"
        # Toggle: active ascending -> request descending; otherwise request ascending.
        next_value = f"-{col.key}" if is_active and sort.direction == _ASC else col.key
        next_url = (
            _build_url(base_url, next_value, param, extra_params)
            if col.sortable and col.key
            else ""
        )
        out.append(
            ColumnSort(
                key=col.key,
                label=col.label,
                align=col.align,
                sortable=col.sortable,
                aria_sort=aria_sort,
                is_active=is_active,
                next_url=next_url,
            )
        )
    return out


def _coerce_column(raw: Column | Mapping[str, object]) -> Column:
    """Accept a :class:`Column` or a plain dict (caller convenience)."""
    if isinstance(raw, Column):
        return raw
    width = raw.get("width")
    mobile_width = raw.get("mobile_width")
    return Column(
        key=str(raw.get("key", "")),
        label=str(raw.get("label", "")),
        sortable=bool(raw.get("sortable", False)),
        align=str(raw.get("align", "")),
        width=str(width) if width not in (None, "") else None,
        mobile_width=str(mobile_width) if mobile_width not in (None, "") else None,
        resizable=bool(raw.get("resizable", False)),
    )


def selection_state(
    selected_ids: Iterable[str] | None,
    page_ids: Iterable[str],
    total: int | None = None,
) -> SelectionState:
    """Normalize request-derived selection into a :class:`SelectionState`.

    ``selected_ids`` (e.g. ``req.query.getlist("ids")``) is coerced to a
    ``frozenset`` of strings; tolerant of ``None``. ``page_ids`` are the ids
    rendered on the current page. ``total`` is the grand result-set size.
    """
    selected = frozenset(str(s) for s in (selected_ids or ()))
    page = tuple(str(p) for p in page_ids)
    return SelectionState(selected=selected, page_ids=page, total=total)
