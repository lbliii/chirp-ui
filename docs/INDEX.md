# Documentation Index

Navigation guide for all chirp-ui documentation.

---

## Core Guides

- [LAYOUT.md](LAYOUT.md) — Horizontal overflow, vertical fill, grid vs frame primitives (consolidated)
- [PRIMITIVES.md](PRIMITIVES.md) — Blessed composition primitives vs legacy compatibility helpers
- [LAYOUT-PRESETS.md](LAYOUT-PRESETS.md) — Grid preset names, aliases, and breakpoint tokens
- [COMPOSITION.md](COMPOSITION.md) — Component composition patterns and slot mechanics
- [APPEARANCE-TONE.md](APPEARANCE-TONE.md) — Chirp-native visual preset axes for pilot components
- [TYPOGRAPHY.md](TYPOGRAPHY.md) — Type scale, font tokens, and text utilities
- [RESPONSIVE.md](RESPONSIVE.md) — Phone/tablet/desktop component behavior contract
- [TOKENS.md](TOKENS.md) — CSS custom property reference (spacing, color, radius, z-index)
- [APP-THEME.md](APP-THEME.md) — Token-only app theme starter and fresh-project ownership contract
- [TRANSITIONS.md](TRANSITIONS.md) — Motion tokens, duration/easing values, reduced-motion
- [UI-LAYERS.md](UI-LAYERS.md) — App shell vs page chrome vs surface chrome, shell regions
- [CSS-OVERRIDE-SURFACE.md](CSS-OVERRIDE-SURFACE.md) — Cascade order, `@layer app.overrides` contract, token vs layer vs unlayered paths
- [NAVIGATION.md](NAVIGATION.md) — Navigation layer model, component decision matrix, and dense chrome guidance
- [DENSE-NAVIGATION-SYNTHESIS.md](DENSE-NAVIGATION-SYNTHESIS.md) — Dense navigation recipe synthesis, primitive candidates, and anti-decisions

## Patterns

- [PRODUCT-PAGE-PATTERNS.md](PRODUCT-PAGE-PATTERNS.md) — Product-site composition recipes built from existing primitives
- [MEDIA-SITE-PATTERNS.md](MEDIA-SITE-PATTERNS.md) — Streaming, video, catalog, live-event, and media-plan composition recipes
- [FORUM-SITE-PATTERNS.md](FORUM-SITE-PATTERNS.md) — Forum, Q&A, threaded discussion, moderation, and community composition recipes
- [HTMX-PATTERNS.md](HTMX-PATTERNS.md) — `hx={}` dict, auto-injected attrs, `build_hx_attrs()`
- [HTMX-ADVANCEMENT.md](HTMX-ADVANCEMENT.md) — Design decisions for htmx integration
- [ALPINE-MAGICS.md](ALPINE-MAGICS.md) — Alpine.js store, `safeData`, shared controllers
- [DROPDOWN-ANATOMY.md](DROPDOWN-ANATOMY.md) — Dropdown menu, select, and split-menu rendered anatomy
- [MODAL-ANATOMY.md](MODAL-ANATOMY.md) — Native modal, overlay modal, and confirm dialog anatomy
- [TABS-ANATOMY.md](TABS-ANATOMY.md) — htmx tabs, tab panels, route tabs, and tabbed page layout anatomy
- [DRAWER-TRAY-ANATOMY.md](DRAWER-TRAY-ANATOMY.md) — Native drawer and store-backed tray anatomy
- [DND-FRAGMENT-ISLAND.md](DND-FRAGMENT-ISLAND.md) — Fragment islands, safe regions, drag-and-drop
- [PROVIDE-CONSUME-KEYS.md](PROVIDE-CONSUME-KEYS.md) — All provide/consume context keys and their contracts
- [SHELL-TABS-CONTRACT.md](SHELL-TABS-CONTRACT.md) — Route tabs and shell tab integration contract
- [WIZARD-FORM.md](WIZARD-FORM.md) — Multi-step wizard form pattern

## Safety and Migration

- [ANTI-FOOTGUNS.md](ANTI-FOOTGUNS.md) — Common pitfalls and how to avoid them
- [DASHBOARD-MATURITY-CONTRACT.md](DASHBOARD-MATURITY-CONTRACT.md) — Dashboard component readiness checklist

## Reference

- [AGENT-SOURCE-INVENTORY.md](AGENT-SOURCE-INVENTORY.md) — Sprint 6 agent source provenance, snippet eligibility, and exclusion contract
- [AGENT-SOURCE-MAP.md](AGENT-SOURCE-MAP.md) — Sprint 6 generated-output ownership and agent source-input map
- [COMPONENT-OPTIONS.md](COMPONENT-OPTIONS.md) — Full parameter reference for all components
- [DOCS-IA-MIGRATION.md](DOCS-IA-MIGRATION.md) — Sprint 4 published-docs IA map and LLM endpoint source map
- [DEEP-DIVE-masked-field-use-cases.md](DEEP-DIVE-masked-field-use-cases.md) — Masked input field patterns and examples

## Theming

- [CHIRP-THEME.md](CHIRP-THEME.md) — Theme package architecture and token system
- [CHIRP-THEME-PARITY-MATRIX.md](CHIRP-THEME-PARITY-MATRIX.md) — Theme token coverage across components
- [BENGAL-THEME-ANATOMY.md](BENGAL-THEME-ANATOMY.md) — Packaged Bengal theme controls, search, mobile nav, TOC, and docs tab hooks

## Planning

Plans are triaged by status. In-flight work sits in [`plans/`](plans/); shipped work is archived under [`plans/done/`](plans/done/) so agents don't cite stale plans as live direction. (Sprint 6 of `PLAN-agent-grounding-depth.md`, 2026-04-20.)

### In-flight plans (`docs/plans/`)

- [PLAN-agent-grounding-depth.md](plans/PLAN-agent-grounding-depth.md) — Manifest-as-full-registry-projection epic
- [PLAN-css-scope-and-layer.md](plans/PLAN-css-scope-and-layer.md) — CSS-as-registry-projection epic
- [PLAN-envelope-hardening-batch-1.md](plans/PLAN-envelope-hardening-batch-1.md) — Envelope-conversion batch 1
- [PLAN-alpine-focus-plugin.md](plans/PLAN-alpine-focus-plugin.md) — Alpine Focus plugin adoption
- [PLAN-ascii-maturity.md](plans/PLAN-ascii-maturity.md) — ASCII art component maturity (partial)
- [PLAN-test-coverage-hardening.md](plans/PLAN-test-coverage-hardening.md) — Test coverage expansion (partial)
- [PLAN-skeleton-equivalent-roadmap.md](plans/PLAN-skeleton-equivalent-roadmap.md) — Skeleton-inspired roadmap for Chirp-native appearance, themes, docs, LLM, and anatomy contracts
- [PLAN-theme-tokens.md](plans/PLAN-theme-tokens.md) — Theme token standardization
- [PLAN-primitive-vocabulary-hardening.md](plans/PLAN-primitive-vocabulary-hardening.md) — Primitive vs legacy helper vocabulary hardening
- [PLAN-sidebar-nav-refinements.md](plans/PLAN-sidebar-nav-refinements.md) — Sidebar nav refinements
- [PLAN-navigation-density-study.md](plans/PLAN-navigation-density-study.md) — Dense high-utility navigation study
- [PLAN-navigation-contract-application.md](plans/PLAN-navigation-contract-application.md) — Apply dense navigation guidance to ChirpUI
- [PLAN-dense-object-chrome-next.md](plans/PLAN-dense-object-chrome-next.md) — Next dense object chrome recipes, counters, command launcher, and composite decision
- [PLAN-dense-navigation-reference-families.md](plans/PLAN-dense-navigation-reference-families.md) — Roadmap for dense navigation recipe families beyond GitHub-style object pages
- [PLAN-route-tabs-and-tabbed-layout.md](plans/PLAN-route-tabs-and-tabbed-layout.md) — Route tabs architecture
- [PLAN-primitives-and-components.md](plans/PLAN-primitives-and-components.md) — Primitives vs components boundary
- [PLAN-layout-widget-brainstorm.md](plans/PLAN-layout-widget-brainstorm.md) — Layout widget ideas
- [PLAN-product-page-patterns-from-langchain.md](plans/PLAN-product-page-patterns-from-langchain.md) — Product-page composition recipes from LangChain design review
- [PLAN-media-site-patterns-from-streaming.md](plans/PLAN-media-site-patterns-from-streaming.md) — Media-site composition recipes from Netflix, YouTube, and Apple TV research
- [PLAN-forum-site-patterns-from-communities.md](plans/PLAN-forum-site-patterns-from-communities.md) — Forum-site composition recipes from Reddit, Discourse, Stack Overflow, and GitHub Discussions research
- [PLAN-chirp-theme-content-parity.md](plans/PLAN-chirp-theme-content-parity.md) — Bengal default content/output parity waves for chirp-theme
- [PLAN-bengal-chirpui-library-contract.md](plans/PLAN-bengal-chirpui-library-contract.md) — First-class Bengal library asset/macro contract for Chirp UI

### Shipped plans (`docs/plans/done/`)

- [PLAN-sharp-edges.md](plans/done/PLAN-sharp-edges.md) — Sharp edges phases 1–2
- [PLAN-sharp-edges-phase3.md](plans/done/PLAN-sharp-edges-phase3.md) — Sharp edges phase 3
- [PLAN-sharp-edges-phase4.md](plans/done/PLAN-sharp-edges-phase4.md) — Sharp edges phase 4: API consistency
- [PLAN-base-layer-hardening.md](plans/done/PLAN-base-layer-hardening.md) — Base-layer hardening (Sprints 20–26)
- [PLAN-behavior-layer-hardening.md](plans/done/PLAN-behavior-layer-hardening.md) — Alpine/JS behavior layer audit
- [PLAN-chirpui-alpine-migration.md](plans/done/PLAN-chirpui-alpine-migration.md) — chirpui.js → Alpine migration
- [PLAN-color-system-hardening.md](plans/done/PLAN-color-system-hardening.md) — Color system validation and tokens
- [PLAN-context-aware-theming.md](plans/done/PLAN-context-aware-theming.md) — Context-aware theme switching
- [PLAN-descriptor-coverage.md](plans/done/PLAN-descriptor-coverage.md) — ComponentDescriptor coverage
- [PLAN-island-js-test-infrastructure.md](plans/done/PLAN-island-js-test-infrastructure.md) — JS island test infrastructure
- [PLAN-kida-0.4.0-adoption.md](plans/done/PLAN-kida-0.4.0-adoption.md) — Kida 0.4.0 feature adoption
- [PLAN-modern-css-backgrounds.md](plans/done/PLAN-modern-css-backgrounds.md) — CSS background pattern system
- [PLAN-provide-consume-expansion.md](plans/done/PLAN-provide-consume-expansion.md) — Expand provide/consume usage
- [PLAN-streaming-maturity.md](plans/done/PLAN-streaming-maturity.md) — SSE/streaming component maturity

### Design & sprint-0 docs

- [DESIGN-css-registry-projection.md](DESIGN-css-registry-projection.md) — CSS epic S0 design lock-in
- [DESIGN-manifest-signature-extraction.md](DESIGN-manifest-signature-extraction.md) — Manifest signature-extraction RFC (Sprint 0 of agent-grounding)
- [DESIGN-appearance-tone.md](DESIGN-appearance-tone.md) — Descriptor-backed appearance and tone vocabulary
- [DESIGN-theme-pack-catalog.md](DESIGN-theme-pack-catalog.md) — Token-only curated theme pack catalog
- [DESIGN-llm-endpoints.md](DESIGN-llm-endpoints.md) — Generated LLM and agent-facing site artifacts
- [DESIGN-interactive-anatomy.md](DESIGN-interactive-anatomy.md) — Executable anatomy contracts for interactive components
- [SPRINT-0-behavior-layer-design.md](SPRINT-0-behavior-layer-design.md) — Sprint 0 design for behavior layer

## Consolidated (redirects)

These files have been merged into [LAYOUT.md](LAYOUT.md) and are kept for existing links:

- [LAYOUT-OVERFLOW.md](LAYOUT-OVERFLOW.md) — Horizontal overflow (see LAYOUT.md)
- [LAYOUT-VERTICAL.md](LAYOUT-VERTICAL.md) — Vertical fill mode (see LAYOUT.md)
- [LAYOUT-GRIDS-AND-FRAMES.md](LAYOUT-GRIDS-AND-FRAMES.md) — Grid vs frame (see LAYOUT.md)
