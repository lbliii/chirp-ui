# Design System Research

**Status:** research note
**Date:** 2026-05-23
**Scope:** External design-system research, Chirp UI product opinion, Bengal shell implications, and maturity gates

## Goal

Use external design systems as requirements proxies because Chirp UI has no
userbase signal yet. The outcome is not a clone of shadcn, Material, Carbon,
Polaris, Atlassian, or USWDS. The outcome is a sharper Chirp UI opinion:
registry-owned contracts, Python-native ergonomics, recipe-first composition,
and evidence gates before public API expansion.

Related source docs:

- [VISION.md](../strategy/vision.md)
- [PRIMITIVES.md](../fundamentals/primitives.md)
- [DENSE-NAVIGATION-SYNTHESIS.md](../patterns/dense-navigation-synthesis.md)
- [DESIGN-layout-affinity.md](layout-affinity.md)
- [PUBLIC-SURFACE-STABILIZATION.md](../safety/public-surface-stabilization.md)

## Research Inputs

- [shadcn/ui components](https://ui.shadcn.com/docs/components)
- [shadcn/ui blocks](https://ui.shadcn.com/blocks)
- [shadcn/ui registry](https://ui.shadcn.com/docs/registry)
- [shadcn/ui CLI](https://ui.shadcn.com/docs/cli)
- [shadcn/ui namespaces](https://ui.shadcn.com/docs/registry/namespace)
- [shadcn/ui MCP server](https://ui.shadcn.com/docs/mcp)
- [shadcn/ui theming](https://ui.shadcn.com/docs/theming)
- [Material Design 3 components](https://m3.material.io/components)
- [Material Design 3 foundations](https://m3.material.io/foundations)
- [Material Design 3 tokens](https://m3.material.io/foundations/design-tokens/overview)
- [Carbon components overview](https://carbondesignsystem.com/components/overview/components/)
- [Carbon patterns](https://carbondesignsystem.com/patterns/overview/)
- [Carbon design tokens](https://carbondesignsystem.com/elements/tokens/overview/)
- [Shopify Polaris components](https://polaris.shopify.com/components)
- [Shopify Polaris foundations](https://polaris.shopify.com/foundations)
- [Atlassian components](https://atlassian.design/components)
- [Atlassian tokens](https://atlassian.design/foundations/tokens/)
- [USWDS components](https://designsystem.digital.gov/components/)
- [USWDS maturity model](https://designsystem.digital.gov/components/overview/)

## Benchmark Matrix

| System | Useful lesson | Avoid |
|---|---|---|
| shadcn/ui | Registry distribution, local install workflow, private namespaces, agent/MCP surface. | Tailwind utility authoring, copied source as the normal update model, React assumptions. |
| Material Design 3 | Complete foundation vocabulary and component guidance. | Platform-general visual orthodoxy over Python app contracts. |
| Carbon | Status, accessibility, pattern docs, tokens, enterprise component breadth. | Enterprise breadth without Chirp UI's registry-first projection discipline. |
| Shopify Polaris | Product-domain guidance and commerce patterns. | Domain lock-in and copying commerce-only primitives. |
| Atlassian Design System | App-shell/productivity surface, tokens, interaction guidance. | Product-suite specificity as public Chirp UI API. |
| USWDS | Maturity and performance documentation around shipped surfaces. | Utility-class scale. |

## Component/Feature/Primitive Parity Matrix

Research is a requirements proxy, not promotion evidence. Chirp UI should not
chase raw component count; do not chase raw component count as a strategy. The
copied-source/Tailwind model conflicts with the library-owned contract. The goal
is contract maturity, not more names:
components, docs, generated CSS, manifests, tests, and agents all agree.

| Surface | Chirp UI Today | shadcn/ui | Material Design 3 | Carbon | Shopify Polaris | Atlassian Design System | Chirp UI Strategy |
|---|---|---|---|---|---|---|---|
| Distribution and discovery | Python package, descriptors, manifest, `find`, Bengal package data. | Registry, CLI, namespaces, MCP, blocks. | Guidance plus platform implementations. | Packages, Storybook, status. | Packages, domain docs, tokens/icons. | Packages, tokens, components, product guidance. | Productize registry/manifest/find without copied source. |
| Layout primitives | Strong `stack`, `cluster`, `grid`, `frame`, `block`; no utility vocabulary. | Tailwind utilities and blocks. | Layout guidance. | Grid/layout guidance. | Layout guidance. | Page/product layout patterns. | Keep primitives as the authoring moat. |
| App/site shell | Existing app shell, tabs, navigation, Bengal pressure. | Blocks and templates. | App bars/nav guidance. | Shell patterns. | App shell/product shell. | Product navigation. | Mature shell contracts through recipes and reference proof first. |
| Navigation hierarchy | Sidebar, primary nav, route tabs, nav tree, breadcrumbs, command palette. | Nav blocks. | Navigation components. | UI shell/navigation. | Navigation. | Side/top navigation. | Keep layer model canonical; promote only repeated gaps. |
| Page header and actions | Page header, hero, share, dropdown, action bar, copy button. | Page blocks and actions. | Top app bar/actions. | Page headers. | Page/action patterns. | Page layout/actions. | Teach composition before `page_actions()`. |
| Dense data and object browsing | Resource index/card, table, params table, filters, badges. | Data table blocks. | Lists/data table guidance. | Data table strong. | Index/table strong. | Table/list strong. | Avoid data-grid engine until reference proof repeats. |
| Agent/readiness metadata | Registry labels, generated options, source maps, `find --details`. | MCP and registry metadata. | Not primary. | Status/docs metadata. | Component guidance. | Component docs. | Make agent discovery a first-class product surface. |

### Parity Takeaways

- shadcn is the best benchmark for distribution, blocks, and agent-facing
  installation, not for styling.
- Carbon, Atlassian, Polaris, Material, and USWDS show why maturity labels,
  accessibility guidance, and pattern boundaries matter.
- Chirp UI's differentiator is the registry contract: public classes, templates,
  CSS, manifest, docs, tests, and agents all project from the same truth.

## Core Findings

### 1. shadcn's moat is distribution, not styling

shadcn proves that installation, search, registry metadata, and local workflow
can be the product. Chirp UI should match that usefulness through a Python
package, `find`, generated options, package data, and source maps while keeping
components library-owned.

### 2. Behavior proof matters more than visual breadth

Mature systems document focus, keyboard, ARIA, motion, overflow, loading,
disabled, and error behavior. Chirp UI should invest in anatomy docs and
browser/server proof before expanding macro names.

### 3. Components, patterns, shells, and evidence are different

The docs IA now keeps contracts, recipes, evidence, research, and plans
separate. That distinction should also drive API decisions: a recipe can teach a
composition without becoming a component.

### 4. Shell APIs need layer discipline first

Application chrome is promising, but `application_chrome()`, `docs_shell`, and
`catalog_shell` should wait for repeated route-family proof. Until then,
`navigation.md`, dense recipes, and reference implementation evidence own the
guidance.

### 5. Differentiation is verification

The S-tier version of Chirp UI is not the biggest component list. It is the
system where app authors and agents can verify what exists, what is stable, what
is recipe-only, and what proof is required to promote it.

## Product Opinion

- **Python-native over copied source:** app authors import macros and registry
  contracts instead of copying React/Tailwind components.
- **Contracts over classes:** components expose named params, slots, emitted
  classes, tokens, and tests; utility-class strings are not the public language.
- **Recipes before composites:** if existing primitives compose cleanly, teach
  the recipe instead of freezing a shell.
- **Behavior where the platform cannot carry it:** Alpine/HTMX helpers belong
  in shared behavior files, not inline scripts in macros.
- **Evidence labels are product UX:** `stable`, `experimental`, `recipe-only`,
  `compatibility`, and `research` should be visible to humans and agents. See
  the evidence-label glossary in
  [PUBLIC-SURFACE-STABILIZATION.md](../safety/public-surface-stabilization.md).

## Bengal Shell Implications

Bengal proved Chirp UI can carry a bespoke docs/product shell, but also showed
where the library still depends on theme-local composition:

- persistent app shell regions,
- compact page identity and actions,
- linked navigation/catalog rails,
- dense reference/data surfaces,
- semantic icons and diagnostics,
- generated/source-map clarity for agents.

Those are inputs for reference implementations, not immediate APIs.

## Backlog

### Wave 1: Research Ledger And Evidence Labels

Done: this research note, public-surface labels, and source-only evidence
boundaries.

### Wave 2: Registry Product Surface

Keep improving `find`, generated options, manifest/package data, and agent
source maps so discovery feels as complete as shadcn's registry while staying
library-owned.

### Wave 3: Anatomy Contracts

Keep anatomy docs focused on rendered structure, focus/keyboard behavior,
runtime requirements, HTMX/Alpine boundaries, and proof commands.

### Wave 4: Accessibility And Performance Ledger

Add only when a component or pattern has concrete proof gaps. Do not invent
process around surfaces that are already covered by existing render/browser
tests.

### Evidence Model Without A Userbase

Chirp UI cannot plan around downstream adoption data it does not have. Use:

- Scenario-complete non-Bengal reference implementations,
- Browser, render, server, escaping, and generated-output tests,
- `docs/reference-implementations/PROOF-ANALYSIS.md` as the source-only ledger,
- recipe guidance, another independent reference, or a stop-and-ask public API
  plan as the only valid outcomes,
- `docs/reference-implementations/RECIPE-GUIDANCE.md` as the source-only
  authoring layer when proof says to keep current primitives and teach the
  recipe,
- Explicit stop-and-ask before any public macro/API, descriptor field, emitted
  class, CSS contract, manifest schema, extension protocol, or copied-source
  workflow.

### Wave 5: Bengal-Driven Primitive Maturation

Use Bengal pressure to choose reference scenarios. Do not count Bengal as the
second independent reference for promotion. It is an excellent stress case and
an insufficient promotion proof by itself.

## Composite Promotion Gate

Before promoting a composite, require:

1. two independent scenario-complete references,
2. a repeated missing contract after current primitives were tried,
3. accessibility, overflow, responsive, and behavior proof,
4. descriptor/template/CSS/manifest/generated-doc alignment,
5. docs and examples in the same PR,
6. explicit non-goals and migration notes.

## Not Now

- Python shadcn clone.
- Tailwind-style utility vocabulary.
- Copied-source component install workflow.
- Public app-shell macros without repeated reference proof.
- Data-grid or reference-page engine without repeated dense-reference proof.
- MCP/server tooling before installed package discovery proves insufficient.

## Steward Notes

- **Docs:** keep this in `docs/decisions/`, not the main reader path.
- **Registry:** no new descriptor or manifest fields are authorized here.
- **Bengal:** theme pressure informs reference scenarios, not public API by
  itself.
- **Verification:** proof for this slice is docs-only review, link coverage from
  [INDEX.md](../INDEX.md), and focused docs/evidence tests.
