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
Dense chrome triggers can use a short visible placeholder while keeping a more
specific accessible name:

```html
{{ command_palette_trigger(
  target="project-palette",
  label="Search project",
  placeholder="Search or jump",
  shortcut="/",
  icon="search",
  density="sm"
) }}
```

## Counters And Badges

Counters in navigation should be stable:

- keep the label and count semantically separable
- avoid loading several counts one at a time if that causes repeated layout
  shifts
- reserve space when a count is expected and the surrounding navigation is dense
- include accessible count text when the visual badge is compact or hidden from
  assistive technologies

`route_tabs` and `primary_nav` support `badge_label`, `badge_expected`, and
`badge_loading` on items. Use `badge_label` when the visual count needs fuller
assistive text, `badge_expected` when a count is intentionally reserved but not
loaded yet, and `badge_loading` when a count is pending.

```html
{{ route_tabs(tabs=[
  {"href": "/issues", "label": "Issues", "badge": 12, "badge_label": "12 open issues"},
  {"href": "/runs", "label": "Runs", "badge_loading": true},
  {"href": "/audit", "label": "Audit", "badge_expected": true},
], current_path="/issues") }}
```

## Dense Object Navigation Recipe

For GitHub-like object pages, compose existing primitives in this order:

1. global row: brand/home, product menu, search/command trigger, utility actions,
   account slot
2. object row: breadcrumbs, title/meta, object-level actions
3. local row: `render_route_tabs` for route-backed object views
4. page row: filters, sort, bulk actions, and content-local tools

The component showcase includes two copyable dense object chrome recipes:
a repository/project page and an admin/settings page. Both keep global
navigation, object context, local routes, and page tools as separate layers.
It also includes a cloud/control-plane recipe for scope switching, service
menus, favorites quickbars, resource search, deployment tabs, and page-local
controls. The suite work hub recipe extends the same layer model to product
suites: top utilities, product modes, personal shortcuts, customizable sidebar
sections, project-local route tabs, and saved views stay distinct. The ops
console recipe applies it to observability: command-first dashboard search,
operational side navigation, time range controls, signal tabs, and stable alert
counts stay in separate layers. The tracker recipe treats shortcut hints as
navigation evidence, pairing command launch with visible favorites, team views,
route-backed issue tabs, and display controls. The knowledge workspace recipe
uses linked disclosure navigation for nested pages, collapsed breadcrumbs for
deep page location, and separate page-local routes for tasks, comments, and
history. The editor workbench recipe keeps file identity, tool navigation,
layer hierarchy, canvas context, comments/prototype routes, and inspector
properties in distinct regions without adding canvas-specific API. The business
object console recipe separates app/resource navigation, global object search,
object ID context, saved searches, and object-local event/invoice/log routes.
The collaboration inbox recipe separates unread navigation, jump-to-conversation
search, activity/later surfaces, and conversation-local message/thread/file
routes. The developer platform recipe combines project/group/profile scope,
search-or-go-to, workflow navigation, a context-sensitive project sidebar, and
project-local tabs without creating a product-specific header clone. The
reference docs recipe applies the same contract to workflow information
architecture, persistent left navigation, docs search, page-local controls, and
nearby-topic discovery.

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
