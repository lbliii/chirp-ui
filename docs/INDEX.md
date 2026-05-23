# Documentation Index

Navigation guide for all chirp-ui documentation.

---

## Core Guides

- [LAYOUT.md](LAYOUT.md) — Horizontal overflow, vertical fill, grid vs frame primitives (consolidated)
- [PRIMITIVES.md](PRIMITIVES.md) — Blessed composition primitives vs legacy compatibility helpers
- [RELATIONSHIP-CONTRACTS.md](RELATIONSHIP-CONTRACTS.md) — Parent-owned inset, rhythm, attachment, grouping, pressure, and overflow contracts
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
- [DENSE-NAVIGATION-RECIPES.md](DENSE-NAVIGATION-RECIPES.md) — Copyable dense navigation recipes and layer model
- [VISUAL-AUDIT-SHOWCASE.md](VISUAL-AUDIT-SHOWCASE.md) — Static visual QA surface and responsive audit checklist
- [DESIGN-SYSTEM-RESEARCH.md](DESIGN-SYSTEM-RESEARCH.md) — External design-system research, Chirp UI product opinion, Bengal shell implications, and maturity gates
- [REFERENCE-IMPLEMENTATION-PLAYBOOK.md](REFERENCE-IMPLEMENTATION-PLAYBOOK.md) — Scenario-complete reference evidence rules for promotion candidates
- [reference-implementations/README.md](reference-implementations/README.md) — Reference implementation brief index for blocked promotion candidates

## Patterns

- [PRODUCT-PAGE-PATTERNS.md](PRODUCT-PAGE-PATTERNS.md) — Product-site composition recipes built from existing primitives
- [MEDIA-SITE-PATTERNS.md](MEDIA-SITE-PATTERNS.md) — Streaming, video, catalog, live-event, and media-plan composition recipes
- [FORUM-SITE-PATTERNS.md](FORUM-SITE-PATTERNS.md) — Forum, Q&A, threaded discussion, moderation, and community composition recipes
- [HTMX-PATTERNS.md](HTMX-PATTERNS.md) — `hx={}` dict, auto-injected attrs, app-shell HTMX boundaries, `build_hx_attrs()`
- [SEARCH-SHELL-RECIPES.md](SEARCH-SHELL-RECIPES.md) — Recipe-first dense catalog/search shells, scoped counts, responsive command surfaces, and HTMX/Alpine contracts
- [WORKSPACE-SHELL-RECIPES.md](WORKSPACE-SHELL-RECIPES.md) — Agent-facing dense search, operations, support, and admin workspace recipes
- [WORKSPACE-SHELL-PROOF.md](WORKSPACE-SHELL-PROOF.md) — Promotion proof comparing the operations baseline with the dense workspace variant
- [LAYOUT-AFFINITY-RESOLVER-AUTHORING.md](LAYOUT-AFFINITY-RESOLVER-AUTHORING.md) — Prototype resolver authoring contract for parent-scoped layout intent
- [HTMX-ADVANCEMENT.md](HTMX-ADVANCEMENT.md) — Design decisions for htmx integration
- [ALPINE-MAGICS.md](ALPINE-MAGICS.md) — Alpine.js store, `safeData`, shared controllers
- [DROPDOWN-ANATOMY.md](DROPDOWN-ANATOMY.md) — Dropdown menu, select, and split-menu rendered anatomy
- [MODAL-ANATOMY.md](MODAL-ANATOMY.md) — Native modal, overlay modal, and confirm dialog anatomy
- [TABS-ANATOMY.md](TABS-ANATOMY.md) — htmx tabs, tab panels, route tabs, and tabbed page layout anatomy
- [DRAWER-TRAY-ANATOMY.md](DRAWER-TRAY-ANATOMY.md) — Native drawer and store-backed tray anatomy
- [DND-FRAGMENT-ISLAND.md](DND-FRAGMENT-ISLAND.md) — Fragment islands, safe regions, drag-and-drop
- [PROVIDE-CONSUME-KEYS.md](PROVIDE-CONSUME-KEYS.md) — All provide/consume context keys and their contracts
- [SHELL-TABS-CONTRACT.md](SHELL-TABS-CONTRACT.md) — Route tabs, shell regions, and consumer app chrome recipe
- [WIZARD-FORM.md](WIZARD-FORM.md) — Multi-step wizard form pattern

## Safety and Migration

- [ANTI-FOOTGUNS.md](ANTI-FOOTGUNS.md) — Common pitfalls and how to avoid them
- [VERIFICATION.md](VERIFICATION.md) — Locked-environment verification, generated artifact checks, and Kida mismatch troubleshooting
- [PUBLIC-SURFACE-STABILIZATION.md](PUBLIC-SURFACE-STABILIZATION.md) — Pre-1.0 promotion, experimental, recipe-only, and compatibility decisions
- [STATIC-SHOWCASE-LEGACY-HELPER-TRIAGE.md](STATIC-SHOWCASE-LEGACY-HELPER-TRIAGE.md) — Static showcase legacy-helper inventory and decisions
- [DASHBOARD-MATURITY-CONTRACT.md](DASHBOARD-MATURITY-CONTRACT.md) — Dashboard component readiness checklist

## Reference

- [AGENT-SOURCE-INVENTORY.md](AGENT-SOURCE-INVENTORY.md) — Sprint 6 agent source provenance, snippet eligibility, and exclusion contract
- [AGENT-SOURCE-MAP.md](AGENT-SOURCE-MAP.md) — Sprint 6 generated-output ownership and agent source-input map
- [AGENT-CURATED-SNIPPETS.md](AGENT-CURATED-SNIPPETS.md) — Reviewed macro-first snippets for agent-facing examples
- [REGISTRY-DISCOVERY.md](REGISTRY-DISCOVERY.md) — CLI and Python discovery over the component registry and manifest labels
- [COMPONENT-OPTIONS.md](COMPONENT-OPTIONS.md) — Full parameter reference for all components
- [DOCS-IA-MIGRATION.md](DOCS-IA-MIGRATION.md) — Sprint 4 published-docs IA map and LLM endpoint source map
- [DEEP-DIVE-masked-field-use-cases.md](DEEP-DIVE-masked-field-use-cases.md) — Masked input field patterns and examples

## Theming

- [CHIRP-THEME.md](CHIRP-THEME.md) — Theme package architecture and token system
- [CHIRP-THEME-PARITY-MATRIX.md](CHIRP-THEME-PARITY-MATRIX.md) — Theme token coverage across components
- [BENGAL-THEME-ANATOMY.md](BENGAL-THEME-ANATOMY.md) — Packaged Bengal theme controls, search, mobile nav, TOC, and docs tab hooks

## Planning

Plans are triaged by status. In-flight work sits in [`plans/`](plans/); shipped work is archived under [`plans/done/`](plans/done/) so agents don't cite stale plans as live direction. (Sprint 6 of `PLAN-agent-grounding-depth.md`, 2026-04-20.)

- [ROADMAP-pre-1.0.md](ROADMAP-pre-1.0.md) — Current pre-1.0 gap roadmap

### In-flight plans (`docs/plans/`)

- [PLAN-pre-1.0-productization-saga.md](plans/PLAN-pre-1.0-productization-saga.md) — Umbrella productization saga for visible quality, public surface, themes, app chrome, Bengal, and verification
- [PLAN-css-scope-and-layer.md](plans/PLAN-css-scope-and-layer.md) — Ongoing `@scope` conversion policy and residual CSS hardening
- [PLAN-application-chrome-system.md](plans/PLAN-application-chrome-system.md) — Application chrome system contracts, rail/tray proof, rhythm audit, and composite gates
- [PLAN-page-actions-primitive.md](plans/PLAN-page-actions-primitive.md) — Page-local actions primitive investigation, promotion gate, and non-API boundary
- [PLAN-chirp-theme-content-parity.md](plans/PLAN-chirp-theme-content-parity.md) — Residual chirp-theme fixture parity backlog
- [PLAN-bengal-chirpui-library-contract.md](plans/PLAN-bengal-chirpui-library-contract.md) — First-class Bengal library asset/macro contract for Chirp UI

### Shipped plans (`docs/plans/done/`)

- [PLAN-alpine-focus-plugin.md](plans/done/PLAN-alpine-focus-plugin.md) — Alpine Focus plugin adoption
- [PLAN-layout-affinity-rollout.md](plans/done/PLAN-layout-affinity-rollout.md) — Layout-affinity resolver rollout, vocabulary gates, manifest@6 migration plan, and proof matrix
- [PLAN-relationship-contracts.md](plans/done/PLAN-relationship-contracts.md) — Relationship ownership rollout for inset, rhythm, attachment, region, pressure, and overflow contracts
- [PLAN-search-shell-contracts.md](plans/done/PLAN-search-shell-contracts.md) — Search shell contracts, scoped counts, responsive command surfaces, facets, pending state, and catalog-shell recipe tasks
- [PLAN-agent-grounding-depth.md](plans/done/PLAN-agent-grounding-depth.md) — Manifest grounding, package data, generated docs, find CLI, and plan triage
- [PLAN-ascii-maturity.md](plans/done/PLAN-ascii-maturity.md) — ASCII/TUI public template maturity proof
- [PLAN-sharp-edges.md](plans/done/PLAN-sharp-edges.md) — Sharp edges phases 1–2
- [PLAN-sharp-edges-phase3.md](plans/done/PLAN-sharp-edges-phase3.md) — Sharp edges phase 3
- [PLAN-sharp-edges-phase4.md](plans/done/PLAN-sharp-edges-phase4.md) — Sharp edges phase 4: API consistency
- [PLAN-base-layer-hardening.md](plans/done/PLAN-base-layer-hardening.md) — Base-layer hardening (Sprints 20–26)
- [PLAN-behavior-layer-hardening.md](plans/done/PLAN-behavior-layer-hardening.md) — Alpine/JS behavior layer audit
- [PLAN-chirpui-alpine-migration.md](plans/done/PLAN-chirpui-alpine-migration.md) — chirpui.js → Alpine migration
- [PLAN-color-system-hardening.md](plans/done/PLAN-color-system-hardening.md) — Color system validation and tokens
- [PLAN-context-aware-theming.md](plans/done/PLAN-context-aware-theming.md) — Context-aware theme switching
- [PLAN-descriptor-coverage.md](plans/done/PLAN-descriptor-coverage.md) — ComponentDescriptor coverage
- [PLAN-dense-navigation-reference-families.md](plans/done/PLAN-dense-navigation-reference-families.md) — Dense navigation reference family study
- [PLAN-dense-object-chrome-next.md](plans/done/PLAN-dense-object-chrome-next.md) — Dense object chrome recipe and composite-decision backlog after browser proof
- [PLAN-envelope-hardening-batch-1.md](plans/done/PLAN-envelope-hardening-batch-1.md) — Envelope hardening batch 1
- [PLAN-forum-site-patterns-from-communities.md](plans/done/PLAN-forum-site-patterns-from-communities.md) — Forum-site pattern recipes
- [PLAN-island-js-test-infrastructure.md](plans/done/PLAN-island-js-test-infrastructure.md) — JS island test infrastructure
- [PLAN-kida-0.4.0-adoption.md](plans/done/PLAN-kida-0.4.0-adoption.md) — Kida 0.4.0 feature adoption
- [PLAN-legacy-helper-cleanup-pre-1.0.md](plans/done/PLAN-legacy-helper-cleanup-pre-1.0.md) — First-party legacy helper cleanup before 1.0
- [PLAN-media-site-patterns-from-streaming.md](plans/done/PLAN-media-site-patterns-from-streaming.md) — Media-site pattern recipes
- [PLAN-modern-css-backgrounds.md](plans/done/PLAN-modern-css-backgrounds.md) — CSS background pattern system
- [PLAN-navigation-density-study.md](plans/done/PLAN-navigation-density-study.md) — Dense navigation study
- [PLAN-navigation-contract-application.md](plans/done/PLAN-navigation-contract-application.md) — Navigation contract application and dense object guidance
- [PLAN-product-page-patterns-from-langchain.md](plans/done/PLAN-product-page-patterns-from-langchain.md) — Product-page pattern recipes
- [PLAN-provide-consume-expansion.md](plans/done/PLAN-provide-consume-expansion.md) — Expand provide/consume usage
- [PLAN-primitive-vocabulary-hardening.md](plans/done/PLAN-primitive-vocabulary-hardening.md) — Primitive authoring hints and legacy-helper decisions
- [PLAN-route-tabs-and-tabbed-layout.md](plans/done/PLAN-route-tabs-and-tabbed-layout.md) — Route tabs architecture
- [PLAN-skeleton-equivalent-roadmap.md](plans/done/PLAN-skeleton-equivalent-roadmap.md) — Skeleton-inspired appearance, theme, docs, source, and anatomy roadmap
- [PLAN-sidebar-nav-refinements.md](plans/done/PLAN-sidebar-nav-refinements.md) — Sidebar nav refinements
- [PLAN-streaming-maturity.md](plans/done/PLAN-streaming-maturity.md) — SSE/streaming component maturity
- [PLAN-test-coverage-hardening.md](plans/done/PLAN-test-coverage-hardening.md) — Historical test coverage hardening plan, superseded by verification docs
- [PLAN-theme-tokens.md](plans/done/PLAN-theme-tokens.md) — Standardized theme token set and token-only theme examples
- [PLAN-verification-and-visual-showcase.md](plans/done/PLAN-verification-and-visual-showcase.md) — Verification repair, visual audit page, and roadmap cleanup

### Design & sprint-0 docs

- [DESIGN-css-registry-projection.md](DESIGN-css-registry-projection.md) — CSS epic S0 design lock-in
- [DESIGN-manifest-signature-extraction.md](DESIGN-manifest-signature-extraction.md) — Manifest signature-extraction RFC (Sprint 0 of agent-grounding)
- [DESIGN-appearance-tone.md](DESIGN-appearance-tone.md) — Descriptor-backed appearance and tone vocabulary
- [DESIGN-theme-pack-catalog.md](DESIGN-theme-pack-catalog.md) — Token-only curated theme pack catalog
- [DESIGN-llm-endpoints.md](DESIGN-llm-endpoints.md) — Generated LLM and agent-facing site artifacts
- [DESIGN-interactive-anatomy.md](DESIGN-interactive-anatomy.md) — Executable anatomy contracts for interactive components
- [DESIGN-layout-affinity.md](DESIGN-layout-affinity.md) — Proposed role/pressure/affinity contract for self-composing primitives and agentic developers
- [SPRINT-0-behavior-layer-design.md](SPRINT-0-behavior-layer-design.md) — Sprint 0 design for behavior layer

## Consolidated (redirects)

These files have been merged into [LAYOUT.md](LAYOUT.md) and are kept for existing links:

- [LAYOUT-OVERFLOW.md](LAYOUT-OVERFLOW.md) — Horizontal overflow (see LAYOUT.md)
- [LAYOUT-VERTICAL.md](LAYOUT-VERTICAL.md) — Vertical fill mode (see LAYOUT.md)
- [LAYOUT-GRIDS-AND-FRAMES.md](LAYOUT-GRIDS-AND-FRAMES.md) — Grid vs frame (see LAYOUT.md)
