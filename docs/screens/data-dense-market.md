# Screen: Data-Dense Market

Status: golden screen fixture
Profile: `atlas`
Fixture route: `/screen-lucky-cat-market`
Live demo: https://chirp-ui-showcase-production.up.railway.app/screen-lucky-cat-market
Source template: `examples/component-showcase/templates/showcase/screen_lucky_cat_market.html`
Proof: `tests/test_data_integration.py`,
`tests/browser/test_golden_screen_fixtures.py`

## Use When

Use Data-Dense Market when an application needs a trading-floor or finance
operations surface with:

- portfolio or account snapshot metrics,
- ticker/symbol search and sector filters,
- movers grids and watchlist/catalog cards,
- selected-symbol inspection,
- live activity or tape-style updates.

Good fits include trading dashboards, market monitors, portfolio workspaces,
and any number-heavy operational UI where tabular numerics and dense cards
must feel composed rather than spreadsheet-like.

## Do Not Use When

Do not use this screen for editorial product pages, low-density onboarding,
marketing-first pages, or simple settings forms. Those need a product/docs home,
onboarding flow, or settings surface instead.

## Composition Map

| Job | Current Surface |
|---|---|
| Profile | `atlas` token mood through screen metadata. |
| Command surface | `command_bar`, search form, hint actions, HTMX update boundary. |
| Portfolio snapshot | `metric_strip`, tabular `metric_item` values. |
| Scope and filtering | `filter_bar`, dense fields, sector/state selectors. |
| Movers | `result_collection`, `result_card`, gain/loss badges. |
| Selected symbol | `inspector_panel` with quote metadata and summary. |
| Market catalog | `result_collection` with selected row state. |
| Live activity | compact `table`, `role=status` live-region note. |
| Empty state | `empty_state` when filters remove all symbols. |

## Typography Role Map

Use the recipe-only role names from
`docs/decisions/typography-role-matrix.md`. These names do not authorize public
tokens or utility classes.

| Role | Screen Surface | Intent |
|---|---|---|
| `page-title` | Page header | Establish market context without hero/display scale. |
| `panel-title` | Movers, catalog, and activity headings | Make scoped regions readable before card-level content. |
| `object-title` | Symbol card title and selected symbol title | Keep ticker symbols prominent in dense cards. |
| `dense-body` | Symbol summaries and inspector explanation | Support short market copy without cramped rhythm. |
| `metadata` | Sector labels, volume, and footer copy | Keep provenance visible without making it disabled-looking. |
| `metric` | Portfolio snapshot, prices, P/L, and tape values | Make operational numbers scannable with tabular numerics. |
| `status-label` | Gainer/loser/watch badges | Pair state color with readable labels so state is not color-only. |

## Data Shape

The fixture expects market records with:

- `symbol`, `name`, `sector`, `price`, `change`, `change_pct`, `volume`,
- `status`, `summary`, `tags`,
- portfolio snapshot values,
- recent activity rows with time/side/size/price.

Use realistic long labels and mixed gain/loss states. A market screen that only
contains short placeholder cards does not prove the taste floor.

## Required States

- Gainer symbol.
- Loser symbol.
- Watch / warning symbol.
- Selected symbol in catalog.
- Filtered-empty catalog.
- Populated live-activity table.

## Agent Guidance

- Start from this screen when the product situation is number-heavy and
  time-sensitive: trading floors, portfolio monitors, market catalogs.
- Prefer `metric_strip`, tabular numerics, and dense `result_card` rows before
  inventing custom stat markup.
- Keep search + filter + catalog + inspector relationships explicit; do not
  collapse the whole surface into one generic card grid.
- If the requested product situation is close but not market-specific, start
  from Command Center or Review Queue and record the gap instead of inventing
  utility classes.

## Proof Checklist

- Server route renders and exposes `data-screen-archetype="data-dense-market"`
  when fixture-backed.
- Browser proof covers 320, 390, 768, and 1280 widths with no document
  horizontal overflow when fixture-backed.
- Portfolio metrics, movers, catalog, inspector, and activity surfaces are all
  visible in the populated fixture.
- Tabular numerics are used on prices, P/L, and tape values.

## Extraction Candidates

Do not promote a pattern because the current Chirp UI path produces too much
local workaround or premature public API work.

- `market_ticker_strip` — repeated only on this screen so far.
- `quote_card` — currently composed from `result_card`.
- `live_tape_panel` — currently composed from `table` + status note.

Stop and ask before adding public vocabulary for any of the above.
