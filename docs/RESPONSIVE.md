# Responsive Contract

ChirpUI components must work at phone, tablet, and desktop widths without
consumer apps replacing the component vocabulary. Apps can still choose denser
or looser compositions, but the stock components should not force a desktop
layout onto small screens.

## Viewport Tiers

| Tier | Width | Contract |
|------|-------|----------|
| Phone | 360-430px | No page-level horizontal overflow from shell, nav, action rows, rendered content, or tables. Navigation that cannot fit must scroll horizontally or move into an overlay. |
| Tablet | 768-1024px | Two-column layouts may remain when content fits; sidebars and secondary panes must not starve the primary reading/writing surface. |
| Desktop | 1280px+ | Dense layouts may use persistent sidebars, multi-column grids, sticky panels, and richer hover affordances. |

## Current Guarantees

- `app_shell` collapses from a sidebar/main grid to a single-column shell below
  `48rem`. The sidebar becomes a horizontally scrollable nav strip so persistent
  navigation remains reachable without squeezing main content. Nested sidebar
  wrappers flatten inside that strip; use a drawer/tray for navigation that must
  preserve a full hierarchy on phones. Tall custom sidebar content is contained
  by `--chirpui-sidebar-mobile-max-block-size` and scrolls inside the shell
  sidebar rather than pushing the main surface down the page.
- `route_tabs` and `primary_nav` become horizontally scrollable strips below
  `40rem` instead of wrapping into tall blocks.
- Deep `breadcrumbs` trails can opt into `overflow="collapse"` so the first
  crumb, current crumb, and configured tail stay visible while middle crumbs
  move into a disclosure-style overflow list.
- Buttons, single-line form controls, dropdown triggers, pagination links,
  theme toggles, and ASCII toggles share `--chirpui-control-block-size` so
  mixed controls line up in topbars/toolbars. At phone widths or on coarse
  pointers they use `--chirpui-control-touch-target`.
- `action_strip` stacks its primary, controls, and actions zones below `48rem`;
  use `wrap="scroll"` for dense toolbars that should stay one line.
- `table` keeps its wrapper scrollable, uses touch momentum scrolling, and
  constrains long cell content at phone widths.
- `rendered_content` constrains media and allows long links/code to wrap.

## Guidance

- Prefer `stack`, `cluster`, `grid`, and `frame` over app-defined utility
  classes. The primitives already encode responsive behavior.
- Use `drawer` or `tray` for dense secondary controls on phones.
- Use `route_tabs` only for local object/workspace views. Use `primary_nav`,
  `sidebar`, or `nav_tree(branch_mode="linked")` for broad navigation.
- For forum/PBP surfaces, wrap post bodies in `rendered_content`, counts in
  `inline_counter`, cast faces in `linked_avatar_stack`, and authoring surfaces
  in `composer_shell`.
- Browser QA for responsive changes should cover at least 390px, 768px, 1024px,
  and desktop widths.
