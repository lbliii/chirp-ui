# Relationship Contracts

Status: active design contract
Date: 2026-05-21
Plan: [PLAN-relationship-contracts.md](plans/PLAN-relationship-contracts.md)

ChirpUI components should not only look correct in isolation. They should also
know which relationships they own with neighboring pieces: inset, sibling
rhythm, attachment, separation, wrapping, pressure, and overflow.

The rule is simple: children own their internal shape; parents own the relationship.
More specifically, parent primitives and components own the relationship
between their direct children.

## Why This Exists

The recurring fresh-app failure was not a missing token or one ugly example.
It was relationship ambiguity:

- fields carried bottom margins, while forms did not own field rhythm;
- paragraphs and headings carried default margins inside stacks and framed
  surfaces;
- action rows needed local CSS to decide search width and hint wrapping;
- dense shells repeated rail/content/inspector spacing in each page.

Those are all the same class of bug. A component library cannot make app
authors and agents fix spacing relationship by relationship.

## Relationship Types

| Relationship | Owner | Contract |
|---|---|---|
| Inset | framed component | Content stays away from borders and backgrounds. Direct slot margins are trimmed. |
| Sibling rhythm | parent primitive | Gap controls spacing between siblings. Child outside margins are neutralized. |
| Attached | owning component | Related fragments stay close: label/input/hint/error, title/actions, metric/label. |
| Grouped | parent primitive or component | Related controls/chips/cards use medium rhythm and wrap without overflow. |
| Separated | page/workspace primitive | Sections, result cards, and major panels use larger rhythm. |
| Region | shell primitive | Rails, content, inspectors, toolbars, and sidebars get predictable placement and minimums. |
| Pressure | parent resolver | Flexible children expand, rigid children keep intrinsic size, compressible children wrap before overflow. |
| Local overflow | owning component | Wide content scrolls locally instead of widening the page. |

## Ownership Rules

1. A child component may define internal padding, typography, and attached
   subparts.
2. A parent primitive defines spacing between direct children.
3. Direct-child margin trimming belongs to the parent owner, not app CSS.
4. Standalone compatibility margins may remain, but parent owners must
   neutralize them when children are composed inside the owner.
5. Relationship contracts must be parent-scoped. Do not add global rules that
   make every `data-chirpui-*` element react everywhere.
6. New relationship behavior needs docs plus render/CSS/browser proof when
   computed layout matters.

## Current Contract Matrix

| Surface | Relationship Owned | Status | Proof |
|---|---|---|---|
| `stack()` | sibling vertical rhythm, child margin trim | shipped | `TestLayout`, `/layout` browser proof |
| `cluster()` | inline wrapping rhythm, child margin trim | shipped | `TestLayout`, `/layout` browser proof |
| `grid()` / `block()` | repeating cell minimums and spans | shipped | layout docs, grid CSS tests |
| `frame()` | structural region columns and rail/content shrink safety | prototype | layout-affinity matrix and browser proof |
| `card` | inset rhythm, header content/actions, metadata grouping | shipped/prototype mix | component CSS tests, card browser proof |
| `surface` | inset rhythm, framed content flow, long-word containment | shipped | surface CSS tests |
| `panel` | inset rhythm and slot flow | shipped | panel CSS tests |
| `callout` | inset rhythm and body flow | shipped | callout CSS tests |
| `form()` | field/action/error-summary sibling rhythm | shipped | `TestForms`, `/forms` browser proof |
| field wrappers and form control internals | label/control/hint/error attachment, option grouping, prefix/suffix/search pressure | shipped | form field render/CSS tests; `/forms` browser proof |
| `command_bar` / `filter_bar` | search, hints, filters, actions, visible-label rows | shipped/prototype mix | action-container tests, browser proof |
| `workspace_shell` | rail/content/inspector/toolbars | prototype | workspace recipe docs and browser proof |
| workspace primitives | rails, result collections, cards, metrics, inspector panels | shipped/prototype mix | data/support/operations browser proof; result cards own title/body/actions/footer pressure |
| `search_header` / `resource_index` | search-first header and browse surface rhythm | shipped | render/CSS/browser proof; search/header/filter/results rhythm owned by composites |
| `page_header` / `section_header` / `entity_header` | title/actions and title/subtitle attachment | shipped | render/CSS/browser proof; direct-child margins trimmed under header owners |
| `fieldset` | grouped form-control rhythm, child margin trim | shipped | `TestForms`, `/forms` browser proof |
| `list_group()` / `media_object()` | row separation, leading media/body/actions pressure, child margin trim | shipped | list/media CSS tests; `/layout` browser proof |
| `dnd` / `sortable` | drag row/board grouping | partial | visual structure tests; spacing/overflow proof needed |
| `modal` / `drawer` / `tray` / `panel` | header/body/footer region rhythm | shipped | CSS/browser proof; region margins, wrapping, and local overflow owned by containers |
| navigation primitives | item metadata, rails, trays, dense chrome | partial | dense navigation docs and browser proof |

## Known Gaps

### Form Subrelationships

`form()` owns field rhythm, and control internals now own common attachment
and pressure relationships: checkbox/toggle label rows, radio option groups,
range label/value rows, input-group prefix/input/suffix sizing, and search bar
button/input wrapping. Remaining form work should focus on specialized controls
that prove new relationship needs.

### Header And Section Relationships

Headers now own title/subtitle/meta attachment, action wrapping, title block
margin trimming, and overflow-safe long titles. Search-first `search_header`
and `resource_index` also own their composite rhythm, so app pages should not
add local margins between search, filters, selection state, and results.

### Overlay And Panel Regions

Modals, drawers, trays, and panels own header/body/footer separation, scroll
ownership, action row rhythm, direct child margin trimming, and long-token
containment inside their local region.

### Lists, Rows, And Dense Collections

`list_group()` owns row separation and trims direct item-child margins, so
bordered lists do not double-space rows with both `gap` and sibling margins.
`media_object()` owns the leading media/body/actions relationship: media stays
intrinsic, body content flexes and wraps, actions wrap as a trailing group, and
direct body/action child margins are neutralized. Dense workspace result cards
also own title/subtitle/action/body/footer pressure for long labels, owners,
status badges, and URLs.

Remaining row-like work should focus on specialized row systems that have
distinct interaction contracts:

- drag/drop and sortable rows;
- params/signature rows with code-heavy local overflow;
- table row action groups and dense metadata variants.

## Agent Checklist

When building or reviewing a UI, ask these before adding page-local CSS:

1. What parent owns this relationship?
2. Is the problem inset, sibling rhythm, attachment, separation, region
   placement, pressure, or overflow?
3. Does the parent trim direct child margins?
4. Does the parent define the gap?
5. Does standalone compatibility require child margins to remain outside this
   parent?
6. Does the relationship hold at phone, tablet, and desktop widths?
7. Is the fix documented and covered by render/CSS/browser proof?

If no owner exists, add one in the narrowest existing component or primitive.
Do not patch the app page unless the relationship is truly app-specific.
