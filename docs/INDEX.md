# Documentation Index

Navigation guide for Chirp UI source documentation.

This index is intentionally broader than the published docs site. It includes
durable contracts, generated references, recipes, source maps, research,
evidence, proposals, and plan archives. When documents overlap, use this rule:
canonical docs own shipped facts, recipe docs own copyable composition patterns,
evidence docs own proof and decision history, and plans own remaining work.

---

## Orientation

- [VISION.md](strategy/vision.md) — Product philosophy, registry-first thesis, and decision lens
- [ROADMAP-pre-1.0.md](strategy/roadmap-pre-1.0.md) — Current pre-1.0 gap roadmap
- [DOCS-IA-MIGRATION.md](agents/docs-ia-migration.md) — Published-docs IA map and LLM endpoint source map

## Fundamentals

Canonical docs for shipped authoring contracts and low-level primitives.

- [LAYOUT.md](fundamentals/layout.md) — Horizontal overflow, vertical fill, grid vs frame primitives (consolidated)
- [PRIMITIVES.md](fundamentals/primitives.md) — Blessed composition primitives vs legacy compatibility helpers
- [RELATIONSHIP-CONTRACTS.md](fundamentals/relationship-contracts.md) — Parent-owned inset, rhythm, attachment, grouping, pressure, and overflow contracts
- [LAYOUT-PRESETS.md](fundamentals/layout-presets.md) — Grid preset names, aliases, and breakpoint tokens
- [COMPOSITION.md](fundamentals/composition.md) — Component composition patterns and slot mechanics
- [TYPOGRAPHY.md](fundamentals/typography.md) — Type scale, font tokens, and text utilities
- [RESPONSIVE.md](fundamentals/responsive.md) — Phone/tablet/desktop component behavior contract
- [TOKENS.md](fundamentals/tokens.md) — CSS custom property reference (spacing, color, radius, z-index)
- [TRANSITIONS.md](fundamentals/transitions.md) — Motion tokens, duration/easing values, reduced-motion
- [UI-LAYERS.md](fundamentals/ui-layers.md) — App shell vs page chrome vs surface chrome, shell regions
- [CSS-OVERRIDE-SURFACE.md](fundamentals/css-override-surface.md) — Cascade order, `@layer app.overrides` contract, token vs layer vs unlayered paths

## Component Contracts

Canonical component, behavior, and macro-contract references.

- [COMPONENT-OPTIONS.md](COMPONENT-OPTIONS.md) — Full generated parameter reference for all components
- [APPEARANCE-TONE.md](components/appearance-tone.md) — Chirp-native visual preset axes for pilot components
- [PROVIDE-CONSUME-KEYS.md](components/provide-consume-keys.md) — All provide/consume context keys and their contracts
- [ALPINE-MAGICS.md](components/alpine-magics.md) — Alpine.js store, `safeData`, shared controllers
- [HTMX-PATTERNS.md](components/htmx-patterns.md) — `hx={}` dict, auto-injected attrs, app-shell HTMX boundaries, `build_hx_attrs()`
- [DROPDOWN-ANATOMY.md](components/dropdown-anatomy.md) — Dropdown menu, select, and split-menu rendered anatomy
- [MODAL-ANATOMY.md](components/modal-anatomy.md) — Native modal, overlay modal, and confirm dialog anatomy
- [TABS-ANATOMY.md](components/tabs-anatomy.md) — htmx tabs, tab panels, route tabs, and tabbed page layout anatomy
- [DRAWER-TRAY-ANATOMY.md](components/drawer-tray-anatomy.md) — Native drawer and store-backed tray anatomy
- [DND-FRAGMENT-ISLAND.md](components/dnd-fragment-island.md) — Fragment islands, safe regions, drag-and-drop
- [SHELL-TABS-CONTRACT.md](components/shell-tabs-contract.md) — Route tabs, shell regions, and consumer app chrome recipe
- [WIZARD-FORM.md](components/wizard-form.md) — Multi-step wizard form pattern

## App Shell, Navigation, And Recipes

Recipe and pattern docs compose existing primitives. They should not introduce
new public APIs unless a linked plan or design record says so.

- [NAVIGATION.md](patterns/navigation.md) — Navigation layer model, component decision matrix, and dense chrome guidance
- [DENSE-NAVIGATION-RECIPES.md](patterns/dense-navigation-recipes.md) — Copyable dense navigation recipes and layer model
- [DENSE-NAVIGATION-SYNTHESIS.md](patterns/dense-navigation-synthesis.md) — Dense navigation recipe synthesis, primitive candidates, and anti-decisions
- [SEARCH-SHELL-RECIPES.md](patterns/search-shell-recipes.md) — Dense catalog/search shells, scoped counts, responsive command surfaces, and HTMX/Alpine contracts
- [WORKSPACE-SHELL-RECIPES.md](patterns/workspace-shell-recipes.md) — Agent-facing dense search, operations, support, and admin workspace recipes
- [WORKSPACE-SHELL-PROOF.md](evidence/workspace-shell-proof.md) — Promotion proof comparing the operations baseline with the dense workspace variant
- [LAYOUT-AFFINITY-RESOLVER-AUTHORING.md](patterns/layout-affinity-resolver-authoring.md) — Prototype resolver authoring contract for parent-scoped layout intent
- [PRODUCT-PAGE-PATTERNS.md](patterns/product-page-patterns.md) — Product-site composition recipes built from existing primitives
- [MEDIA-SITE-PATTERNS.md](patterns/media-site-patterns.md) — Streaming, video, catalog, live-event, and media-plan composition recipes
- [FORUM-SITE-PATTERNS.md](patterns/forum-site-patterns.md) — Forum, Q&A, threaded discussion, moderation, and community composition recipes
- [VISUAL-AUDIT-SHOWCASE.md](patterns/visual-audit-showcase.md) — Static visual QA surface and responsive audit checklist

## Screen Catalog

Screen catalog entries are complete product-situation recipes with profile
pairings, fixture routes, realistic state coverage, proof, and agent guidance.
They are not public macros.

- [README.md](screens/README.md) — Screen catalog overview, selection rule, and promotion boundary
- [COMMAND-CENTER.md](screens/command-center.md) — Atlas operational dashboard fixture for metrics, queues, incidents, activity, and selected-object inspection
- [REVIEW-QUEUE.md](screens/review-queue.md) — Sage review/triage fixture for filter rails, result collections, inspectors, and stateful records
- [AGENT-RUN-MONITOR.md](screens/agent-run-monitor.md) — Signal-candidate live run fixture for timelines, streaming output, artifacts, retries, and selected-step inspection
- [PRODUCT-DOCS-HOME.md](screens/product-docs-home.md) — Ember product/docs home fixture for identity, proof, lifecycle explanation, entry points, and CTA

## Theming And Bengal

- [APP-THEME.md](theming/app-theme.md) — Token-only app theme starter and fresh-project ownership contract
- [CHIRP-THEME.md](theming/chirp-theme.md) — Theme package architecture and token system
- [CHIRP-THEME-PARITY-MATRIX.md](theming/chirp-theme-parity-matrix.md) — Theme token coverage across components
- [BENGAL-THEME-ANATOMY.md](theming/bengal-theme-anatomy.md) — Packaged Bengal theme controls, search, mobile nav, TOC, and docs tab hooks

## Agent And Generated Sources

Source maps and generated-reference inputs. These docs ground coding agents and
site generation; they are not general reader tutorials.

- [AGENT-SOURCE-INVENTORY.md](agents/agent-source-inventory.md) — Agent source provenance, snippet eligibility, and exclusion contract
- [AGENT-SOURCE-MAP.md](agents/agent-source-map.md) — Generated-output ownership and agent source-input map
- [AGENT-CURATED-SNIPPETS.md](agents/agent-curated-snippets.md) — Reviewed macro-first snippets for agent-facing examples
- [REGISTRY-DISCOVERY.md](agents/registry-discovery.md) — CLI and Python discovery over the component registry and manifest labels

## Reference Implementation Evidence

Reference implementation briefs are source-only evidence for promotion
decisions. They do not authorize public APIs by themselves.

- [REFERENCE-IMPLEMENTATION-PLAYBOOK.md](reference-implementations/playbook.md) — Scenario-complete reference evidence rules for promotion candidates
- [reference-implementations/README.md](reference-implementations/README.md) — Reference implementation brief index for blocked promotion candidates
- [reference-implementations/PROOF-ANALYSIS.md](reference-implementations/PROOF-ANALYSIS.md) — Source-only proof-analysis ledger for reference fixture decisions
- [reference-implementations/RECIPE-GUIDANCE.md](reference-implementations/RECIPE-GUIDANCE.md) — Recipe-first guidance for reference candidates kept on current primitives

Briefs indexed by the reference implementation README:

- [PAGE-ACTIONS-AI-REFERENCE.md](reference-implementations/PAGE-ACTIONS-AI-REFERENCE.md)
- [LINKED-NAV-CATALOG-REFERENCE.md](reference-implementations/LINKED-NAV-CATALOG-REFERENCE.md)
- [COMPACT-HEADER-REFERENCE.md](reference-implementations/COMPACT-HEADER-REFERENCE.md)
- [SHELL-RESPONSE-REFERENCE.md](reference-implementations/SHELL-RESPONSE-REFERENCE.md)
- [DENSE-REFERENCE-DATA-REFERENCE.md](reference-implementations/DENSE-REFERENCE-DATA-REFERENCE.md)
- [AGENT-DISCOVERY-REFERENCE.md](reference-implementations/AGENT-DISCOVERY-REFERENCE.md)

## Safety, Verification, And Stabilization

- [ANTI-FOOTGUNS.md](safety/anti-footguns.md) — Common pitfalls and how to avoid them
- [VERIFICATION.md](safety/verification.md) — Locked-environment verification, generated artifact checks, and Kida mismatch troubleshooting
- [PUBLIC-SURFACE-STABILIZATION.md](safety/public-surface-stabilization.md) — Pre-1.0 promotion, experimental, recipe-only, and compatibility decisions
- [STATIC-SHOWCASE-LEGACY-HELPER-TRIAGE.md](safety/static-showcase-legacy-helper-triage.md) — Static showcase legacy-helper inventory and decisions
- [DASHBOARD-MATURITY-CONTRACT.md](components/dashboard-maturity-contract.md) — Dashboard component readiness checklist

## Design Records And Research

Design and research docs explain how decisions were reached. Promote stable
contracts into the canonical docs above instead of making these the only source
for shipped behavior.

- [DESIGN-SYSTEM-RESEARCH.md](decisions/design-system-research.md) — External design-system research, Chirp UI product opinion, Bengal shell implications, and maturity gates
- [DESIGN-css-registry-projection.md](decisions/css-registry-projection.md) — CSS epic S0 design lock-in
- [DESIGN-manifest-signature-extraction.md](decisions/manifest-signature-extraction.md) — Manifest signature-extraction RFC
- [DESIGN-appearance-tone.md](decisions/appearance-tone.md) — Descriptor-backed appearance and tone vocabulary
- [DESIGN-theme-pack-catalog.md](decisions/theme-pack-catalog.md) — Token-only curated theme pack catalog
- [DESIGN-composition-taxonomy-inventory.md](decisions/composition-taxonomy-inventory.md) — Taste-floor taxonomy inventory and golden-screen readiness map
- [DESIGN-llm-endpoints.md](decisions/llm-endpoints.md) — Generated LLM and agent-facing site artifacts
- [DESIGN-interactive-anatomy.md](decisions/interactive-anatomy.md) — Executable anatomy contracts for interactive components
- [DESIGN-layout-affinity.md](decisions/layout-affinity.md) — Proposed role/pressure/affinity contract for self-composing primitives and agentic developers
- [SPRINT-0-behavior-layer-design.md](decisions/behavior-layer-design.md) — Sprint 0 design for behavior layer
- [HTMX-ADVANCEMENT.md](decisions/htmx-advancement.md) — Design decisions for htmx integration
- [DEEP-DIVE-masked-field-use-cases.md](decisions/masked-field-use-cases.md) — Masked input field patterns and examples

## Proposals

Proposals are not shipped contracts until promoted by an implementation plan and
matching tests/docs collateral.

- [CHIRP-FRAMEWORK-SUPPORT.md](proposals/CHIRP-FRAMEWORK-SUPPORT.md) — Framework support for safer showcase and fragment workflows
- [click-to-edit-styling.md](proposals/click-to-edit-styling.md) — Click-to-edit styling improvements

## Planning

Plans are triaged by status. In-flight work sits in [`plans/`](plans/); shipped
work is archived under [`plans/done/`](plans/done/) so agents don't cite stale
plans as live direction. (Sprint 6 of `PLAN-agent-grounding-depth.md`,
2026-04-20.)

### In-flight plans (`docs/plans/`)

- [PLAN-visual-taste-floor-saga.md](plans/PLAN-visual-taste-floor-saga.md) — Screen catalog, profile, golden-screen, agent-guidance, and visual-proof saga for raising default visual quality
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
- [PLAN-sharp-edges.md](plans/done/PLAN-sharp-edges.md) — Sharp edges phases 1-2
- [PLAN-sharp-edges-phase3.md](plans/done/PLAN-sharp-edges-phase3.md) — Sharp edges phase 3
- [PLAN-sharp-edges-phase4.md](plans/done/PLAN-sharp-edges-phase4.md) — Sharp edges phase 4: API consistency
- [PLAN-base-layer-hardening.md](plans/done/PLAN-base-layer-hardening.md) — Base-layer hardening (Sprints 20-26)
- [PLAN-behavior-layer-hardening.md](plans/done/PLAN-behavior-layer-hardening.md) — Alpine/JS behavior layer audit
- [PLAN-chirpui-alpine-migration.md](plans/done/PLAN-chirpui-alpine-migration.md) — chirpui.js to Alpine migration
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

## Consolidated Redirects

These files have been merged into [LAYOUT.md](fundamentals/layout.md) and are kept for
existing links:

- [LAYOUT-OVERFLOW.md](fundamentals/layout-overflow.md) — Horizontal overflow (see LAYOUT.md)
- [LAYOUT-VERTICAL.md](fundamentals/layout-vertical.md) — Vertical fill mode (see LAYOUT.md)
- [LAYOUT-GRIDS-AND-FRAMES.md](fundamentals/layout-grids-and-frames.md) — Grid vs frame (see LAYOUT.md)
