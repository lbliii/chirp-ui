# Chirp UI Pre-1.0 Gap Roadmap

Status: active roadmap
Date: 2026-05-23

This roadmap turns the Skeleton-inspired review and current design-system
research into executable work. The goal is not to copy Skeleton, shadcn/ui,
Radix, Carbon, GOV.UK, or any other system. The goal is to make Chirp UI the
best system in its own category: a Python-native, registry-verified design
system for server-rendered apps.

## Current Position

Chirp UI already has the hard architectural pieces in place:

- a registry-backed component vocabulary,
- a shipped `chirpui-manifest@5` with params, slots, emitted classes, tokens,
  maturity, runtime requirements, and authoring hints,
- generated CSS partials with registry parity checks,
- public cascade layers and token-first app overrides,
- HTMX and Alpine interaction contracts,
- dense navigation recipes,
- a Bengal/chirp-theme integration path,
- broad render, JS, browser, and contract coverage.

The remaining work is mostly about making that quality obvious, reducing stale
planning noise, and stabilizing the public surface before 1.0.

## Categorical Strategy

Chirp UI should not win by having the most components or the largest ecosystem.
It should win by making UI contracts inspectable and verifiable from Python in a
way Tailwind, shadcn/ui, Radix, and enterprise React systems cannot.

The strategic bets are:

- **Registry as product:** the Python registry, manifest, CLI discovery, docs,
  and agent-facing source map become a coherent component catalog, not just
  internal metadata.
- **Contracts over classes:** public authoring stays centered on macros, slots,
  tokens, variants, runtime requirements, and relationship contracts, not
  utility class strings.
- **Evidence-labeled maturity:** every surface is clearly stable,
  experimental, recipe-only, compatibility, or research-backed-not-shipped.
- **Anatomy as executable contract:** complex components document parts,
  roles, state, focus, keyboard behavior, runtime requirements, and proof.
- **Shell layer discipline:** app shell, docs/catalog shell, rails, trays,
  page tools, and content flow mature through smaller contracts before any
  composite shell macro.
- **Bengal as proof path:** the packaged Bengal theme is a reference implementation for
  docs/catalog shell pressure, theme asset contracts, and reference-page
  primitives.
- **Screen catalog as taste floor:** complete product situations, profile
  pairings, realistic data, agent guidance, and visual proof make default mocks
  look designed before app authors write custom CSS.

See `docs/decisions/design-system-research.md` for the research ledger behind these
decisions.

## Workstreams

### 0. Productization Coordination

Goal: keep the pre-1.0 push focused on making existing quality visible,
teachable, and stable before expanding public surface area.

Tasks:

- Use `docs/plans/PLAN-pre-1.0-productization-saga.md` as the umbrella plan
  for sequencing visible showcase, public-surface stabilization, theme
  authoring, application chrome adoption, Bengal integration, and verification.
- Update child plans when implementation starts; do not let the umbrella plan
  become a second backlog with stale task detail.
- Treat visual proof, docs/source collateral, and generated-output checks as
  first-class acceptance criteria.

Acceptance:

- New work can point to one productization epic and one child plan.
- Public surface expansion is deferred unless the promotion gates in the
  productization saga are satisfied.
- Planning updates reduce ambiguity about what is active, shipped, deferred, or
  not-now.

### 0a. Registry Product Surface

Goal: make the registry and manifest feel like a first-class design-system
product, comparable in practical usefulness to shadcn's registry ecosystem but
grounded in Python contracts instead of copied source.

Tasks:

- Improve discovery output around component maturity, authoring status,
  runtime requirements, slots, and recipe-only boundaries.
- Make generated docs and agent-facing sources point to real registry data and
  proof, not hand-maintained claims.
- Evaluate a future agent query surface only after `build_manifest()`, `find`,
  and source inventory docs are strong enough locally.
- Keep app-local extension stories typed and registry-preserving; do not make
  copied component source the default ownership model.

Acceptance:

- A user or agent can discover the preferred component, its maturity, required
  runtime, and relevant docs/tests without reading implementation files first.
- Registry, manifest, generated docs, and source inventory agree.
- Any manifest or descriptor expansion has a migration/schema plan before code
  changes.

### 0b. Anatomy And Evidence Ledgers

Goal: raise complex component maturity by making accessibility, behavior,
performance, and responsive proof explicit.

Tasks:

- Add anatomy-contract expectations to high-risk surfaces: overlays, drawers,
  command palette, route tabs, shell navigation, page actions, and dense
  reference primitives.
- Track proof fields such as native semantics, keyboard, focus, overflow,
  reduced motion, runtime requirements, and browser coverage.
- Avoid claims of manual screen-reader proof unless manual verification was
  actually performed.
- Use evidence labels from `docs/safety/public-surface-stabilization.md` to keep
  research, recipes, and stable APIs distinct.

Acceptance:

- Promotion PRs for complex surfaces cite anatomy and proof, not only visual
  output.
- Browser proof covers stress widths and focus movement when relevant.
- Docs and tests name any residual accessibility or performance risk.

### 1. Verification Reliability

Goal: every maintainer and agent can regenerate and verify the system from a
fresh checkout.

Tasks:

- Fix local `uv run` / cache setup issues so `poe build-manifest-check`,
  `poe build-css-check`, `poe build-docs-check`, and release preflight are
  reliable.
- Add a short troubleshooting note for the Kida API mismatch failure mode:
  system `python -m chirp_ui.manifest --json` can import the wrong installed
  Kida, while `uv run` should use the locked environment.
- Keep `src/chirp_ui/manifest.json`, `src/chirp_ui/templates/chirpui.css`, and
  generated docs in the release-preflight drift gate.

Acceptance:

- `uv run poe build-manifest-check` passes from a clean checkout.
- `uv run poe build-css-check` passes from a clean checkout.
- `uv run poe build-docs-check` passes from a clean checkout.
- The docs name the preferred command path and the known failure mode.

### 2. Roadmap Hygiene

Goal: active plans describe real remaining work, not shipped history.

Tasks:

- Move plans that are fully shipped to `docs/plans/done/`.
- Rewrite partially shipped plans as residual backlogs.
- Keep this file as the current top-level planning map.
- Link every active plan to one of these workstreams.

Acceptance:

- `docs/INDEX.md` lists only genuinely active plans under in-flight work.
- Shipped plans do not contain unqualified `Status: active` or `Status: draft`
  language.
- Each remaining active plan has a "Residual Work" or "Next Slice" section.

### 3. Visible Design-System Showcase

Goal: make Chirp UI's quality visible, not just verifiable.

Tasks:

- Maintain a static visual audit page that can be opened without a server.
- Show token palettes, theme modes, component states, dense navigation,
  forms, feedback, marketing patterns, ASCII/TUI primitives, and responsive
  stress cases in one place.
- Add a screenshot checklist for desktop, tablet, and phone widths.
- Use the page as the first stop before promoting experimental components.

Acceptance:

- `examples/design-system-gap-showcase/index.html` renders with packaged CSS.
- The page exercises light/dark token contrast, dense chrome, long labels,
  loading/reserved badges, and nested surfaces.
- The page contains no inline copy explaining how to use the library; it is a
  visual audit surface, not a landing page.

### 3a. Screen Catalog And Taste Floor

Goal: raise the default mock quality with complete product situations rather
than isolated component examples.

Tasks:

- Use `docs/plans/PLAN-visual-taste-floor-saga.md` as the active plan for the
  composition taxonomy, taste laws, profile/screen pairings, golden screens,
  agent guidance, and proof ratchet.
- Build golden screens before adding public screen macros: Command Center,
  Review Queue, Agent Run Monitor, and Product/Docs Home.
- Treat every local visual workaround in those screens as evidence for a
  missing token, relationship, primitive, pattern, component, or recipe.
- Promote only repeated semantic moves; keep one-off polish in recipes.

Acceptance:

- A polished mock starts from a screen archetype and profile, not from a generic
  card grid.
- Golden screens survive realistic data, stress states, and desktop/tablet/phone
  widths.
- Agent guidance can cite curated screen entries without inventing classes or
  macros.

### 4. Theme Authoring UX

Goal: make token-driven theming feel obvious and powerful.

Tasks:

- Add a theme preset gallery covering default, app starter, holy-light, and
  chirp-theme token profiles.
- Add a token explorer that groups color, typography, radius, elevation,
  spacing, and motion tokens by job.
- Document which tokens app authors should override first.
- Keep theme customization token-first; component selectors belong in
  `@layer app.overrides` only when a token hook is insufficient.

Acceptance:

- A user can compare theme presets visually without reading token tables first.
- `docs/fundamentals/tokens.md` and `docs/theming/app-theme.md` link to the visual gallery.
- No new private `--chirp-theme-*` token vocabulary appears.

### 5. Dense Navigation Productization

Goal: turn the dense navigation study into a teachable product surface.

Tasks:

- Publish a focused dense navigation recipes guide.
- Keep product-specific shells as recipes until repeated reference implementation usage proves
  a macro should exist.
- Add browser proof for `scope_switcher` and `saved_view_strip` only if their
  overflow or layout behavior becomes more ambitious.
- Revisit `workspace_shell` after reference implementation usage, not from showcase examples
  alone.

Acceptance:

- The guide explains scope, command jump, broad nav, object context, local
  route views, page tools, and attention states as separate layers.
- Recipes cite existing components first.
- Any new macro proposal answers the acceptance rule in
  `docs/patterns/dense-navigation-synthesis.md`.

### 5a. Application Chrome System

Goal: make layered app shells, rails, trays, command surfaces, object context,
route rows, and page tools robust enough for modern applications without
shipping a premature mega-shell macro.

Tasks:

- Use `docs/plans/PLAN-application-chrome-system.md` as the live contract map
  for the five rocks: layer model, rail/tray contracts, visual rhythm,
  responsive gauntlet, and recipe-first composite gates.
- Add rail-to-tray recipes and browser proof before any application chrome
  composite proposal.
- Treat modern chrome rhythm as token/control-size/elevation proof, not
  utility spacing classes.
- Publish application chrome guidance through the navigation pattern docs
  without inventing site-only component facts.

Acceptance:

- Application chrome remains recipe-first until deliberately built reference
  implementations prove a stable missing API.
- Browser gauntlets cover 320px stress, phone, tablet, and desktop widths for
  rail/tray fallback, command focus, route-tab scroll, badges, and overflow.
- New public chrome API proposals include registry, CSS, manifest, generated
  docs, examples, browser proof, and changelog collateral.

Current promotion queue:

- Private evidence is complete for page actions, linked nav/sidebar semantics,
  shell response/OOB routing, and compact header/page hero comparison.
- Scenario-complete proof also exists for dense reference/data pages and agent
  discovery. The next work there is proof analysis: compare current primitives
  against the reference fixture outcomes before proposing a data-grid,
  reference-page macro, manifest schema change, or copied-source workflow.
- The next qualifying work is not waiting for a userbase or adding another
  artificial fixture. It is deliberately building or identifying a second
  scenario-complete non-Bengal reference implementation for page actions,
  linked branch navigation, or compact docs/reference/catalog headers, or a
  third scenario-complete hand-written route family for shell response/OOB
  branching.
- Use [REFERENCE-IMPLEMENTATION-PLAYBOOK.md](../reference-implementations/playbook.md)
  and [reference-implementations/README.md](../reference-implementations/README.md)
  as the queue for those reference scenarios before proposing public API. Use
  [reference-implementations/PROOF-ANALYSIS.md](../reference-implementations/PROOF-ANALYSIS.md)
  to decide whether existing proof routes to guidance, more reference evidence,
  or a stop-and-ask API plan. Use
  [reference-implementations/RECIPE-GUIDANCE.md](../reference-implementations/RECIPE-GUIDANCE.md)
  when the decision is to keep current primitives and teach the recipe.
- Until that reference-implementation evidence exists, keep these surfaces recipe-first
  and do not add `application_chrome()`, `docs_shell`, `catalog_shell`,
  `compact_page_header`, `page_actions`, or shell response helper APIs.

### 5b. Bengal-Driven Component Maturation

Goal: use the custom Bengal theme as a first-party docs/catalog proving ground
that exposes which Chirp UI primitives should mature next.

Tasks:

- Treat Bengal docs chrome as evidence for smaller contracts first:
  `page_hero` empty-slot behavior, compact headers, linked nav-tree/sidebar
  semantics, page actions, reference cards, semantic icons, and footer/content
  ownership.
- Use `docs/plans/PLAN-page-actions-primitive.md` as the active investigation
  gate before any registry-owned page-actions macro or runtime is proposed.
- Keep Bengal shell pressure separate from generic app-shell pressure.
- Promote recipes only after Bengal plus another independent reference
  implementation repeat the same structural gap.
- Treat private fixtures as proof of current composition, not as promotion
  evidence by themselves.
- Record accepted/deferred Bengal findings in the relevant child plan before
  implementation.

Acceptance:

- Bengal-driven changes name the exact theme pressure and existing primitives
  tried.
- Public API changes include descriptor, template, CSS, manifest, docs,
  examples, tests, generated-output, and changelog collateral.
- `docs_shell`, `catalog_shell`, or similar composites remain deferred until
  the composite promotion gate is satisfied.

### 6. CSS Scope Hardening

Goal: reduce style bleed as a normal maintenance practice.

Tasks:

- Continue converting touched component partials to the `@layer` + `@scope`
  envelope.
- Prioritize components that nest, hover, or use contextual selectors: forms,
  buttons, nav, lists, badges, tables, panels, and grouped controls.
- Add a browser or computed-style proof when a conversion changes behavior.

Acceptance:

- New components use scoped partials by default.
- Each conversion keeps registry emits parity green.
- Nested component bleed fixes are covered by targeted browser tests.

### 7. Public Surface Stabilization

Goal: make the pre-1.0 API feel intentional.

Tasks:

- Review experimental components and classify them as promote, keep
  experimental, recipe-only, or deprecate later.
- Record decisions in `docs/safety/public-surface-stabilization.md`.
- Review legacy helpers and prevent utility-class vocabulary growth.
- Keep the completed legacy-helper cleanup plan archived under
  `docs/plans/done/PLAN-legacy-helper-cleanup-pre-1.0.md`, and use its proof
  when deciding future keep/deprecate outcomes.
- Keep `find --authoring` and manifest authoring hints aligned with docs.

Acceptance:

- Every experimental public component has a 1.0 disposition.
- Every legacy helper has an explicit keep/deprecate-later decision.
- Generated docs and manifest agree about preferred versus compatibility
  authoring paths.

### 8. Bengal And chirp-theme Integration

Goal: make Chirp UI a first-class Bengal library without theme-local asset
plumbing.

Tasks:

- Finish Bengal library asset modes: `bundle`, `link`, and `none`.
- Register Chirp UI template/macros/runtime helpers from Bengal library
  declarations.
- Remove transitional filesystem-relative theme imports after Bengal owns the
  asset contract.
- Keep chirp-theme output parity moving through Chirp UI-native templates and
  tokens.

Acceptance:

- A Bengal theme with `libraries = ["chirp_ui"]` can import Chirp UI macros
  and emit required assets without manual path knowledge.
- Static and dev outputs resolve the same logical asset contract.
- `chirp-theme` CSS contains only theme tokens, content polish, and actively
  referenced vertical styles.

## Active Plan Mapping

Each active plan is mapped to this roadmap so planning docs do not drift into a
parallel backlog.

| Plan | Roadmap workstream |
|---|---|
| `PLAN-visual-taste-floor-saga.md` | Screen Catalog And Taste Floor |
| `PLAN-pre-1.0-productization-saga.md` | Productization Coordination |
| `PLAN-bengal-chirpui-library-contract.md` | Bengal And chirp-theme Integration |
| `PLAN-chirp-theme-content-parity.md` | Bengal And chirp-theme Integration |
| `PLAN-css-scope-and-layer.md` | CSS Scope Hardening |
| `PLAN-application-chrome-system.md` | Application Chrome System |

Archived planning inputs now live under `docs/plans/done/`. Notable archived
inputs for the current productization push are `PLAN-skeleton-equivalent-roadmap.md`,
`PLAN-ascii-maturity.md`, `PLAN-test-coverage-hardening.md`,
`PLAN-navigation-contract-application.md`, and
`PLAN-dense-object-chrome-next.md`, `PLAN-agent-grounding-depth.md`,
`PLAN-theme-tokens.md`, and `PLAN-primitive-vocabulary-hardening.md`.

## Sequencing

1. Lock the categorical story in docs: registry product surface, contract
   verification, no utility vocabulary, and recipe-first promotion.
2. Strengthen registry discovery and evidence labels before adding broad new
   public API.
3. Add anatomy/evidence ledgers for high-risk interactive and shell-adjacent
   surfaces.
4. Use Bengal and application chrome proof to mature smaller contracts before
   shell composites.
5. Publish and maintain visual/theme proof surfaces.
6. Continue CSS scope conversion and verification hardening throughout.

## Decision Rule

Before adding a new public component, ask:

- Does an existing primitive composition fail in a repeated, documented way?
- Is the missing behavior visible in the visual audit or a real consuming app?
- Can the registry, manifest, docs, CSS, and tests describe it together?
- Does it preserve Chirp UI as a Python vocabulary rather than a utility-class
  vocabulary?

If the answer is not concrete, keep the pattern as a recipe.
