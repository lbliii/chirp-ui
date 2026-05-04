# chirp-ui: Dense Navigation Reference Families

Status: active plan
Date: 2026-05-03
Depends on:

- [PLAN-navigation-density-study.md](PLAN-navigation-density-study.md)
- [PLAN-navigation-contract-application.md](PLAN-navigation-contract-application.md)
- [PLAN-dense-object-chrome-next.md](PLAN-dense-object-chrome-next.md)
- [../NAVIGATION.md](../NAVIGATION.md)

## Goal

Broaden ChirpUI's dense navigation guidance beyond GitHub-like repository
pages. GitHub is a useful daily reference, but the durable product opportunity
is a family of high-utility work surfaces:

- product-suite work hubs,
- cloud and deployment consoles,
- observability consoles,
- keyboard-first trackers,
- knowledge workspaces,
- design/editor workbenches,
- business object consoles,
- collaboration inboxes,
- developer platforms,
- dense reference/docs systems.

Each family should produce copyable ChirpUI recipes and only then justify new
component API. The goal is to teach ChirpUI how to build dense navigation
systems without cloning any specific product.

## Progress

- Family 1 accepted: the component showcase now includes a product-suite work
  hub recipe with top utilities, mode navigation, personal shortcuts,
  customizable sidebar sections, project-local route tabs, stable counts, and
  saved views.
- Family 2 accepted: the component showcase now includes a cloud/control-plane
  console recipe with scope switching, service menu, favorites quickbar,
  resource search, object-local route tabs, stable counts, and deployment tools.
- Family 3 accepted: the component showcase now includes an observability/ops
  console recipe with command-first dashboard search, operational side
  navigation, time range controls, signal tabs, saved investigations, and stable
  alert counts.
- Family 4 accepted: the component showcase now includes a keyboard-first
  tracker recipe with favorites, team pages, shortcut-labeled command launch,
  route-backed issue views, saved views, and compact display controls.
- Family 5 accepted: the component showcase now includes a knowledge workspace
  recipe with workspace switching, linked nested page navigation, team/private
  boundaries, collapsed breadcrumbs, page-local routes, and nearby-topic
  discovery.
- Family 6 accepted: the component showcase now includes an editor workbench
  recipe with compact file navigation, tool controls, linked layer hierarchy,
  canvas context, route-backed comments/prototype views, and an inspector panel.
- Family 7 accepted: the component showcase now includes a business object
  console recipe with app launching, global object search, resource navigation,
  saved searches, object ID context, and object-local event/invoice/log routes.
- Family 8 accepted: the component showcase now includes a collaboration inbox
  recipe with workspace switching, unread side navigation, jump-to-conversation
  search, activity/later surfaces, and conversation-local routes.

## Research Sources

These sources are reference inputs, not contracts to copy:

| Family | References | Navigation lesson |
|--------|------------|-------------------|
| Product-suite work hub | [Atlassian Jira navigation](https://support.atlassian.com/navigation/docs/what-is-the-new-navigation-in-jira/), [Atlassian navigation best practices](https://support.atlassian.com/navigation/docs/navigation-best-practices/), [Asana new navigation](https://help.asana.com/s/article/new-navigation-in-asana) | Top utilities plus customizable sidebar, recent/starred/for-you areas, project or mode navigation. |
| Cloud/control-plane console | [AWS Console services menu](https://docs.aws.amazon.com/en_us/awsconsolehelpdocs/latest/gsg/service-menu.html), [AWS favorites quickbar](https://docs.aws.amazon.com/awsconsolehelpdocs/latest/gsg/add-fave.html), [Vercel dashboard](https://vercel.com/docs/dashboard-features/overview), [Vercel command menu](https://vercel.com/docs/dashboard-features/command-menu) | Scope selectors, service/resource menus, favorites quickbars, project search, command shortcuts. |
| Observability/ops console | [Grafana search and command palette](https://grafana.com/docs/grafana/latest/search/), [Datadog quick nav](https://www.datadoghq.com/blog/datadog-quick-nav-menu/), [Datadog navigation redesign](https://www.datadoghq.com/blog/datadog-navigation-redesign/) | Command palette for pages/actions, product-area side nav, recent dashboards, high-density dashboard controls. |
| Keyboard-first tracker | [Linear concepts](https://linear.app/docs/conceptual-model), [Linear favorites](https://linear.app/docs/favorites), [Linear team pages](https://linear.app/docs/default-team-pages), [Linear display options](https://linear.app/docs/display-options) | Sidebar favorites, team views, shortcut families, command menu, compact display controls. |
| Knowledge workspace | [Notion sidebar](https://www.notion.com/help/navigate-with-the-sidebar), [Notion sidebar academy](https://www.notion.com/help/notion-academy/lesson/sidebar), [Notion pages and breadcrumbs](https://www.notion.com/help/notion-academy/lesson/pages-breadcrumbs-and-sidebar) | Nested hierarchy, workspace switcher, search, favorites, private/shared/teamspace sections, breadcrumbs. |
| Design/editor workbench | [Figma UI3 navigation](https://help.figma.com/hc/en-us/articles/23954856027159-Navigating-UI3-Figma-s-new-UI) | Canvas-first layout, collapsible panels, contextual file menu, tool relocation to preserve workspace. |
| Business object console | [Stripe Dashboard basics](https://docs.stripe.com/dashboard/basics?locale=en-GB), [Stripe Dashboard search](https://docs.stripe.com/dashboard/search?locale=en-GB), [Salesforce Lightning navigation items](https://help.salesforce.com/s/articleView?id=platform.customize_lex_nav_menus_create.htm&language=en_US&type=5) | Object/resource sidebar, global object search, app launcher, object tabs and saved searches. |
| Collaboration inbox | [Slack keyboard navigation](https://slack.com/help/articles/115003340723-Navigate-Slack-with-your-keyboard), [Slack shortcuts](https://slack.com/hc/en-us/articles/201374536-Slack-keyboard-shortcuts) | Conversation sidebar, unread navigation, region focus, jump-to-conversation, activity/later surfaces. |
| Developer platform | [GitLab interface navigation](https://docs.gitlab.com/tutorials/left_sidebar/), [GitLab search](https://docs.gitlab.com/user/search/), [GitLab navigation sidebar](https://archives.docs.gitlab.com/18.1/development/navigation_sidebar/) | Context-sensitive sidebar, top search-or-go-to, project/group scopes, workflow-based nav. |
| Reference/docs system | [GitLab docs global navigation](https://docs.gitlab.co.jp/ee/development/documentation/site_architecture/global_nav.html) | Workflow-based information architecture and persistent nearby-topic discovery. |

## Common Patterns

These patterns recur across the reference set and are worth turning into ChirpUI
recipes:

1. **Scope switcher before local controls.** Team, account, workspace, project,
   organization, environment, or file context should be visible before page
   actions.
2. **Search as navigation.** Search and command launchers jump across entities,
   not just filter the current table.
3. **Durable sidebar plus compact top utilities.** Broad navigation belongs in
   a sidebar or panel; top rows should hold identity, search, creation, account,
   and high-frequency utilities.
4. **Favorites, recent, starred, and saved views.** Personal shortcuts are not
   secondary in dense apps; they are a first-class way to make large systems
   usable.
5. **Object-local route views.** Once inside a project, dashboard, account,
   customer, issue, or page, route tabs or a local nav layer switch views of the
   current object.
6. **Stable counts and attention markers.** Badges, unread counts, alert counts,
   and issue counts must reserve space and carry accessible text.
7. **Keyboard paths are product paths.** Command menus, jump shortcuts, and
   region focus shortcuts are part of the navigation contract, not hidden power
   user extras.
8. **Responsive overflow is by layer.** Sidebars collapse, route tabs scroll,
   low-frequency utilities move into overflow, and object context remains
   reachable.

## Family Plans

### Family 1: Product-Suite Work Hub

Reference shape:

- Atlassian-style top bar for search/create/account,
- customizable sidebar for For you, Recent, Starred, Apps, Spaces or Projects,
- project or space-local navigation below the workspace level,
- mode-oriented organization as seen in Asana's Work/Strategy/Workflow/Company
  direction.

ChirpUI recipe:

- `workspace_shell` or `app_shell`,
- `primary_nav` for top-level product modes when horizontal space allows,
- `sidebar`, `nav_tree`, and `primary_nav` for recent/starred/project sections,
- `command_palette_trigger` for global search/create,
- `route_tabs` for project-local views.

Implementation candidate:

- `examples/component-showcase/templates/showcase/_suite_work_hub.html`
- Showcase section: "Suite Work Hub Navigation"
- Site docs: app-shell page or a future dense navigation recipes page.

Proof:

- render test checks sidebar sections, command trigger, route tabs, and stable
  badges,
- responsive browser proof if new CSS is needed,
- docs build checks.

Not now:

- draggable sidebar customization,
- persisted user personalization,
- product-specific app switcher API.

### Family 2: Cloud And Deployment Console

Reference shape:

- AWS-style services menu, recently visited services, favorites quickbar,
- Vercel-style scope selector, project list, Find/Command Menu, project
  dashboard tabs,
- environment/resource awareness.

ChirpUI recipe:

- global row with scope switcher, command launcher, create action, account slot,
- favorites quickbar using `primary_nav` or compact `chip_group`,
- project/resource cards or table below,
- object page with breadcrumbs, metadata counters, `route_tabs`, and page tools.

Implementation candidate:

- `examples/component-showcase/templates/showcase/_cloud_console_nav.html`
- Recipe states: empty favorites, populated favorites, loading deployment count.

Proof:

- render test for services/favorites/resource scope,
- badge reserved/loading tests reused from nav counters,
- browser check for quickbar horizontal scroll.

Not now:

- true service catalog search backend,
- drag-reorder favorites,
- cloud-vendor-specific vocabulary.

### Family 3: Observability And Ops Console

Reference shape:

- Grafana command palette for dashboards, folders, pages, and actions,
- Datadog product-area nav with dense flyout/subnav and recent troubleshooting
  resources,
- dashboard chrome with time range, refresh, filters, alert counts, and kiosk or
  focus modes.

ChirpUI recipe:

- command/search launcher as the primary cross-system jump path,
- sidebar or product rail grouped by operational domain,
- dashboard header with time range/action strip,
- `route_tabs` or segmented controls for Logs/Metrics/Traces/Alerts,
- stable alert/monitor badges.

Implementation candidate:

- `examples/component-showcase/templates/showcase/_ops_console_nav.html`
- Showcase section: "Ops Console Navigation"

Proof:

- render tests for alert-count reserved/loading states,
- command trigger accessibility test,
- browser check for toolbar overflow at phone and tablet widths.

Not now:

- realtime metrics,
- hover mega-menus,
- keyboard command execution beyond existing command palette behavior.

### Family 4: Keyboard-First Tracker

Reference shape:

- Linear-style sidebar favorites, team pages, cycles/projects/views,
- contextual command menu,
- view display controls,
- shortcut families for "go to" and "open" actions.

ChirpUI recipe:

- sidebar with favorites and team-scoped nav,
- `command_palette_trigger` with shortcut labels,
- `command_bar` for view display controls,
- `route_tabs` for team issue views,
- dense object row for issue/project metadata.

Implementation candidate:

- `examples/component-showcase/templates/showcase/_tracker_nav.html`
- Docs note: keyboard hints are supplemental; visible controls still need labels.

Proof:

- render tests for favorites/team sections,
- command trigger label/shortcut tests,
- no new JS unless command behavior itself changes.

Not now:

- full shortcut dispatcher,
- peek preview behavior,
- saved personal display preferences.

### Family 5: Knowledge Workspace

Reference shape:

- Notion-style workspace switcher,
- search and inbox at top of sidebar,
- Teamspaces, Shared, Private, Favorites,
- deeply nested pages,
- breadcrumbs for current page location.

ChirpUI recipe:

- `nav_tree(branch_mode="linked")` and disclosure nav for nested pages,
- `breadcrumbs(overflow="collapse")`,
- command launcher for search/jump,
- sidebar sections for workspace/team/private boundaries,
- page header with object actions and share/publish status.

Implementation candidate:

- `examples/component-showcase/templates/showcase/_knowledge_workspace_nav.html`

Proof:

- render test for nested pages and collapsed breadcrumbs,
- strict undefined test for minimal nested nav items if new dict shapes appear,
- responsive check for sidebar collapse if CSS changes.

Not now:

- drag-and-drop page nesting,
- access-control inheritance UI,
- infinite-depth virtualization.

### Family 6: Design Or Editor Workbench

Reference shape:

- Figma-style canvas-first workspace,
- collapsible navigation and properties panels,
- file name/location menu,
- contextual toolbar relocation to maximize canvas space.

ChirpUI recipe:

- `workspace_shell`, `split_layout`, `file_tree`, and inspector panel slots,
- compact document/object header,
- command launcher for file/actions,
- panel collapse affordances using existing shell behavior where possible.

Implementation candidate:

- extend `examples/component-showcase/templates/showcase/chrome.html`,
- or add `_editor_workbench_nav.html`.

Proof:

- browser layout proof because failures are visual: canvas area must stay
  usable at desktop/tablet widths,
- no generated CSS drift,
- no inline scripts.

Not now:

- freeform canvas engine,
- custom keyboard tool mode system,
- drag handles unless split panel already supports the need.

### Family 7: Business Object Console

Reference shape:

- Stripe-style sidebar resource areas, global resource search, object IDs,
  customers/payments/invoices/products,
- Salesforce-style app launcher and configurable navigation items,
- saved searches and object list filters.

ChirpUI recipe:

- business resource sidebar,
- top search/command launcher,
- object detail header with IDs, status, metadata counters,
- `route_tabs` for Overview/Events/Logs/Settings,
- `filter_bar` or `command_bar` for saved searches and list controls.

Implementation candidate:

- `examples/component-showcase/templates/showcase/_business_object_console.html`

Proof:

- render tests for object ID/search/status patterns,
- docs examples for search vs filter distinction,
- no new public API until repeated object header shape is proven.

Not now:

- SQL/search query language support,
- custom app-builder navigation model,
- permission-aware nav hiding.

### Family 8: Collaboration Inbox

Reference shape:

- Slack-style workspace/channel/DM sidebar,
- unread counts and attention states,
- jump-to-conversation,
- region focus shortcuts and conversation detail panel.

ChirpUI recipe:

- sidebar with channels, DMs, activity/later sections,
- stable unread badge states,
- command launcher for jump-to-conversation,
- local route tabs for thread/activity/files/canvas where applicable,
- `message_thread` or conversation components for content.

Implementation candidate:

- extend existing messenger/social examples,
- or add `examples/component-showcase/templates/showcase/_collaboration_inbox_nav.html`.

Proof:

- render tests for unread/reserved/loading badges,
- browser focus proof only if new keyboard/focus behavior is added,
- docs note separating unread navigation from command actions.

Not now:

- realtime unread synchronization,
- full Slack-like keyboard region manager,
- multi-workspace account switch persistence.

### Family 9: Developer Platform

Reference shape:

- GitLab-style context-sensitive sidebar,
- top "Search or go to",
- project/group/profile scopes,
- workflow-based project navigation,
- project search with filtering.

ChirpUI recipe:

- global search/go-to trigger,
- context sidebar that changes by project/group/profile,
- breadcrumbs for project/group hierarchy,
- route tabs for project-local views,
- command bar filters for search results and issue/MR lists.

Implementation candidate:

- build alongside existing project/repository object chrome rather than a
  separate GitHub clone,
- `examples/component-showcase/templates/showcase/_developer_platform_nav.html`.

Proof:

- render tests for context sidebar variants,
- search/filter route examples,
- responsive proof for sidebar plus route tabs.

Not now:

- code browser tree behavior,
- merge request review UI,
- project-specific command mode.

### Family 10: Reference And Documentation System

Reference shape:

- GitLab docs-style workflow-based global navigation,
- persistent nearby-topic discovery,
- breadcrumbs,
- search as the likely initial entrypoint,
- left nav that does not lose place.

ChirpUI recipe:

- workflow-based `nav_tree`,
- `breadcrumbs(overflow="collapse")`,
- search/command trigger,
- current section highlighting,
- page-local "on this page" or adjacent-topic surfaces.

Implementation candidate:

- site/docs recipe rather than core component API first,
- possible `examples/docs-theme-showcase/` update.

Proof:

- docs-site tests if site source changes,
- render test for workflow nav state,
- no generated site/public edits unless docs build output is explicitly part of
  the task.

Not now:

- search index implementation,
- automatic information architecture generation,
- analytics-driven nav ordering.

## Execution Order

Recommended order, from highest reuse to most specialized:

1. **Cloud/control-plane console**: builds directly on current dense object
   chrome and validates favorites/scope/resource patterns.
2. **Product-suite work hub**: validates customizable sidebar, recent/starred,
   and mode/project navigation.
3. **Observability/ops console**: stress-tests command launcher, toolbar
   density, alert counts, and dashboard controls.
4. **Knowledge workspace**: stress-tests deep hierarchy, breadcrumbs, and
   sidebar sections.
5. **Business object console**: validates object IDs, global resource search,
   and saved-search/list-control patterns.
6. **Keyboard-first tracker**: validates shortcut hinting and command-first
   navigation without requiring a shortcut engine.
7. **Collaboration inbox**: validates unread counts and jump-to-conversation
   patterns.
8. **Developer platform**: consolidates GitHub/GitLab-like lessons after the
   broader primitives are proven.
9. **Design/editor workbench**: requires browser layout proof and should wait
   until shell/panel contracts are stable.
10. **Reference/docs system**: can proceed in parallel when site/docs work is
    active, but should not drive core app-shell API alone.

## Shared Acceptance Checklist

Every accepted family recipe should include:

- one copyable showcase or site example,
- a short docs note explaining the navigation layer model used,
- render tests for non-default states,
- strict-undefined tests for any new dict-driven inputs,
- CSS/registry/manifest/generated-docs updates only when public macros or
  emitted classes change,
- browser proof when the success criterion depends on real layout, scroll,
  focus, dialog, or responsive behavior,
- a changelog fragment if user-facing behavior changes.

## Shared Not-Now List

- Product-branded clones.
- Utility classes for dense spacing, hiding, alignment, or overflow.
- Drag-and-drop personalization before static recipes prove the structure.
- Async counter loading protocols beyond reserved/loading visual states.
- JavaScript-managed responsive overflow.
- New composite macros before at least two recipes repeat the same shape.
- A shortcut engine; shortcut labels and command launcher behavior come first.
