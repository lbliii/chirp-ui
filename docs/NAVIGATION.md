# Navigation Contract

Navigation in ChirpUI is a layered contract, not a single topbar component.
Before choosing a component, identify the job the control performs. A route
link, a tab panel switch, a disclosure, a command menu, and a search launcher
can all look compact, but they have different semantics and different failure
modes.

See also:

- [SHELL-TABS-CONTRACT.md](SHELL-TABS-CONTRACT.md)
- [RESPONSIVE.md](RESPONSIVE.md)
- [UI-LAYERS.md](UI-LAYERS.md)
- [PLAN-navigation-density-study.md](plans/PLAN-navigation-density-study.md)

## Decision Matrix

| User need | Use | Do not use |
|-----------|-----|------------|
| Persistent app identity | `app_shell`, `navbar`, brand slots | a page header pretending to be global chrome |
| Broad product or section movement | `primary_nav`, `sidebar`, `nav_tree` | `dropdown_menu` command lists |
| Deep hierarchy | `nav_tree(branch_mode="linked")`, drawer/tray on phones | a three-tier topbar |
| Object or path context | `breadcrumbs`, page header metadata | route tabs |
| Local route-backed views | `render_route_tabs` / `route_tabs` | ARIA tabs |
| In-place panel switching | `tabs_panels`, `tabs` where tab semantics are satisfied | route links |
| Commands and actions | `command_bar`, `action_strip`, `dropdown_menu` | section navigation |
| Search, jump, and command launch | `command_palette`, `command_palette_trigger` | a normal text input in global chrome unless it owns search submission |
| Attention and status | badges, counters, notification actions | labels folded into route text |
| Overflow | scroll strip, drawer/tray, overflow menu, selective hide | wrapping until the header becomes a page section |

## Layer Model

| Layer | Responsibility | Typical ChirpUI surface |
|-------|----------------|-------------------------|
| Global shell | App identity, product switch, global utilities | `app_shell`, `navbar`, `command_palette_trigger`, icon actions |
| Product navigation | Major sections and frequent section switching | `sidebar`, `primary_nav`, `nav_tree` |
| Object context | Current object/path, title, metadata, object actions | `breadcrumbs`, `page_header`, `action_strip` |
| Local route navigation | Views of the current object/workspace | `render_route_tabs` |
| Surface chrome | Filters, sort, selection, page-local actions | `command_bar`, `filter_bar`, `selection_bar` |
| Command overlay | Search, jump, and command execution | `command_palette` |

Dense navigation works when these layers stay distinct even when they share the
same vertical space.

## ARIA And Semantics

Route navigation should stay link-native:

- use anchors with real `href` values
- wrap groups in a labelled `nav`
- mark the current destination with `aria-current="page"`
- use `match="exact"` or `match="prefix"` where ChirpUI supports path matching

True tab widgets are different:

- use `role="tablist"`, `role="tab"`, and `role="tabpanel"`
- manage `aria-selected`
- support the keyboard behavior required by the tab pattern
- use only when activating a tab changes an in-place panel, not the current URL

Disclosure navigation is not a command menu:

- use native `<details>` or disclosure buttons for expandable navigation groups
- preserve list semantics where the hierarchy matters
- do not add ARIA `menu`/`menuitem` roles to ordinary site or app navigation

Command menus are for actions and options:

- `dropdown_menu` is appropriate for commands, destructive actions, and option
  lists
- route links inside menus need a complete keyboard/focus story if they are
  exposed as menu items
- use `nav_tree` or documented disclosure patterns when the content is primarily
  navigation

## Overflow Policy

Use this priority order when a navigation surface becomes too dense:

1. Keep current context and the primary action reachable.
2. Keep local route tabs horizontally scrollable instead of wrapping into a tall
   block.
3. Move broad or deep navigation into `drawer`/`tray` on phones.
4. Collapse low-frequency utilities into an overflow action.
5. Hide only duplicate shortcuts whose destination remains reachable elsewhere.

Avoid wrapping dense global chrome until it reads like content. Wrapping can be
fine for chips, breadcrumbs, or metadata rows, but it usually fails for app
headers with mixed route links, utilities, search, and account controls.

Deep breadcrumb trails should use breadcrumb overflow instead of widening the
header:

```html
{{ breadcrumbs(items, overflow="collapse", max_items=4) }}
```

The collapsed middle crumbs remain navigation links in a disclosure-style
overflow list. This keeps the breadcrumb landmark and current-page state intact
without turning path navigation into an ARIA command menu.

## Search And Command Launchers

A compact search trigger in app chrome should open a larger command/search
surface. The trigger can be short, but it still needs a clear accessible name.
Keyboard hints are supplemental.

Use `command_palette_trigger` for the chrome control and `command_palette` for
the overlay. Keep search/jump behavior out of ordinary route navigation.

## Counters And Badges

Counters in navigation should be stable:

- keep the label and count semantically separable
- avoid loading several counts one at a time if that causes repeated layout
  shifts
- reserve space when a count is expected and the surrounding navigation is dense
- include accessible count text when the visual badge is compact or hidden from
  assistive technologies

This is guidance for existing badge-bearing surfaces (`route_tabs`,
`primary_nav`, `sidebar_link`, and `nav_tree`). New count-loading API should not
be added until an example or app proves the need.

## Dense Object Navigation Recipe

For GitHub-like object pages, compose existing primitives in this order:

1. global row: brand/home, product menu, search/command trigger, utility actions,
   account slot
2. object row: breadcrumbs, title/meta, object-level actions
3. local row: `render_route_tabs` for route-backed object views
4. page row: filters, sort, bulk actions, and content-local tools

On phones:

- move deep navigation into drawer/tray
- keep route tabs horizontally scrollable
- collapse low-frequency utilities into overflow
- keep the current object/path and primary action reachable

## Anti-Patterns

- Adding utility classes for dense padding, visibility, or text alignment.
- Modeling route links as ARIA tabs.
- Modeling ordinary navigation disclosure as ARIA menus.
- Building a public `github_header` or app-specific clone.
- Adding macro parameters before a concrete example proves the missing contract.
- Hand-editing generated CSS, manifest, or generated component docs.
