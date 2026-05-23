# PLAN: Pre-1.0 Productization Saga

Status: active plan
Date: 2026-05-23
Trigger: The project has strong Skeleton-comparable architecture and current
design-system research now clarifies how Chirp UI can be categorically best
without imitating Tailwind, shadcn/ui, Radix, Carbon, or enterprise React
systems.

## Goal

Make Chirp UI feel ready for serious Python application authors before adding
more public surface area, and make the category unmistakable:

> a Python-native contract design system for server-rendered apps.

The next phase is not a component-count race. It is a productization pass over
the quality that already exists: registry discovery, executable contracts,
visual proof, theme authoring, public-surface decisions, application-chrome
adoption, Bengal integration, and reliable verification.

## Current Position

Chirp UI has crossed the architecture-risk threshold:

- `chirpui-manifest@5` projects registry metadata for components, params,
  slots, classes, tokens, runtime requirements, maturity, and authoring hints.
- Current component and maturity counts come from the generated manifest. Check
  them from source with `python -m chirp_ui.manifest --json` or
  `src/chirp_ui/manifest.json` instead of copying static counts into this plan.
- The preferred authoring surface is intentionally narrow: composition
  primitives such as `stack`, `cluster`, `grid`, `frame`, `block`, `layer`,
  and `prose`.
- Theme packs exist (`atlas`, `ember`, `sage`) with token-only proof, but remain
  experimental.
- Application chrome has reference implementation/browser proof and remains recipe-first.
- Anatomy docs and tests cover the major interactive families.
- CSS, manifest, docs, and examples are generated or checked as registry
  projections.

Compared to Skeleton and shadcn/ui, Chirp UI is competitive on architecture,
verification, and Python-native introspection. It is not yet at public product
parity on registry discovery, docs polish, theme tooling, live examples,
ecosystem affordances, anatomy/evidence ledgers, or first-run teaching.

## Productization Thesis

Chirp UI should win by being:

- Python-native and registry-grounded.
- Token-first instead of utility-class-first.
- HTMX/Alpine-aware without owning framework state.
- Agent-groundable through generated manifests and curated examples.
- Small enough to verify, but complete enough for application chrome, forms,
  overlays, navigation, and content surfaces.
- Evidence-labeled: stable, experimental, recipe-only, compatibility, or
  research-only surfaces are not blurred together.
- Contract-first: anatomy, slots, runtime requirements, emitted classes, focus,
  keyboard behavior, and proof are discoverable from source.

Do not chase Skeleton by copying Tailwind utilities, framework components, or
class aliases. Translate only the product strengths that match Chirp's category:
coherent themes, clear docs, strong examples, visible quality, and predictable
contracts.

Do not chase shadcn/ui by copying component source into apps. Translate its best
idea into Chirp's model: registry-backed discovery and agent workflows, but
with package upgrades and verification instead of perpetual local forks.

## Ranked Epics

### 1. Registry Product Surface

Goal: make the component registry and manifest as useful to humans and agents
as shadcn's registry is, while preserving Chirp UI's library-owned contract.

Next slices:

- Improve `python -m chirp_ui find` and manifest-backed docs around preferred
  authoring, maturity, runtime requirements, slots, and recipe-only boundaries.
- Ensure generated docs, source inventory, and curated snippets tell the same
  story as the registry.
- Add proof links or evidence references where descriptor data already supports
  them; defer descriptor/schema additions until a design RFC exists.
- Design an agent-facing "discover, apply, verify" workflow after local
  registry discovery is strong enough.

Acceptance:

- A user or agent can find the preferred primitive/component, understand when
  not to use it, and identify required runtime/proof without reading templates.
- Registry, manifest, generated docs, and source inventory agree.
- No copied-source component ownership model is introduced.

Proof:

- `uv run pytest tests/test_manifest.py tests/test_manifest_signatures.py -q`
- Focused `find`/inspect tests when CLI output changes.
- Generated docs freshness checks when generated output changes.

Collateral:

- `docs/DESIGN-SYSTEM-RESEARCH.md`
- `docs/AGENT-SOURCE-INVENTORY.md`
- `docs/AGENT-SOURCE-MAP.md`
- `docs/COMPONENT-OPTIONS.md` when generated output changes.
- Manifest schema notes before any schema change.

### 2. Anatomy And Evidence Ledgers

Goal: make high-risk component quality explicit: anatomy, accessibility,
behavior, responsive constraints, performance notes, and proof.

Next slices:

- Define a small evidence-ledger format for complex surfaces without changing
  descriptor schema yet.
- Apply it first to overlays, drawers/trays, command palette, route tabs, shell
  navigation, page actions, forms/validation, and Bengal docs chrome.
- Use Radix/Base/React Aria as behavior-proof inspiration and GOV.UK/Carbon as
  evidence-status inspiration.
- Record residual risk explicitly, especially when proof is automated browser
  proof rather than manual assistive-technology testing.

Acceptance:

- Promotion PRs for complex surfaces cite anatomy and proof.
- Docs do not imply manual screen-reader testing unless it happened.
- Browser proof covers focus, keyboard, overflow, reduced motion, or stress
  widths when those risks are relevant.

Proof:

- Existing anatomy tests plus focused additions for changed surfaces.
- Browser tests for focus/keyboard/overflow-sensitive changes.
- `uv run pytest tests/test_public_surface_stabilization.py -q` when maturity
  labels change.

Collateral:

- Existing anatomy docs under `docs/*-ANATOMY.md`
- `docs/PUBLIC-SURFACE-STABILIZATION.md`
- `docs/VISUAL-AUDIT-SHOWCASE.md`
- Relevant browser fixtures.

### 3. Visible Design-System Showcase

Goal: make quality obvious before readers inspect tests or plans.

Next slices:

- Promote `examples/design-system-gap-showcase/index.html` into the first QA
  stop for visual decisions.
- Ensure one pass covers tokens, theme modes, dense navigation, application
  chrome, forms, overlays, feedback, data tables, ASCII/TUI primitives, long
  labels, loading/reserved states, and responsive stress.
- Add a screenshot checklist for phone, tablet, desktop, light mode, dark mode,
  and at least one catalog theme pack.
- Treat missing showcase coverage as a blocker for promoting experimental
  visual components.

Acceptance:

- A new contributor can judge the design-system state from one local artifact.
- The showcase contains no invented APIs and no utility-class teaching.
- Visual audit docs name the component families and responsive widths covered.

Proof:

- `uv run pytest tests/test_visual_audit_showcase.py tests/test_pattern_assets.py -q`
- Browser proof for any changed interactive or layout-sensitive fixture.

Collateral:

- `docs/VISUAL-AUDIT-SHOWCASE.md`
- `examples/design-system-gap-showcase/index.html`
- Relevant pattern docs only when a pattern contract changes.

### 4. Public Surface Stabilization

Goal: make the pre-1.0 public vocabulary intentional.

Next slices:

- Drive the `93` experimental components toward explicit outcomes: stable,
  keep experimental, recipe-only, or deprecate later.
- Finish marketing-pattern classification after the ASCII/TUI promotion pass.
- Separate decorative effects from interaction-bearing effects and require
  reduced-motion proof before promotion.
- Keep recipe-only patterns out of preferred authoring until repeated app usage
  proves an API.
- Keep legacy helpers as compatibility unless a tested migration path exists.

Acceptance:

- Every experimental component has a named 1.0 disposition.
- Generated docs and manifest agree on maturity and authoring status.
- No recipe-only item is taught as a preferred component API.

Proof:

- `uv run pytest tests/test_public_surface_stabilization.py tests/test_manifest.py tests/test_component_options_ratchets.py -q`
- Browser proof when promotion depends on keyboard, focus, overflow, or motion.

Collateral:

- `docs/PUBLIC-SURFACE-STABILIZATION.md`
- `docs/COMPONENT-OPTIONS.md` when generated output changes.
- Changelog fragment for user-facing promotion, deprecation, or authoring
  guidance changes.

### 5. Theme Authoring UX

Goal: make token-driven theming feel obvious and powerful.

Next slices:

- Build a theme gallery that compares default, app starter, Bengal/chirp-theme,
  and catalog packs across the same component matrix.
- Add a token explorer organized by job: color, typography, radius, elevation,
  spacing, z-index, and motion.
- Document the first tokens app authors should override.
- Decide promotion criteria for `atlas`, `ember`, and `sage` from experimental
  to stable.
- Keep theme packs token-only; no component selector forks.

Acceptance:

- A user can compare themes visually before reading token tables.
- Theme-pack CSS remains token-only.
- Docs teach app overrides through tokens first and `@layer app.overrides`
  second.

Proof:

- `uv run pytest tests/test_theme_token_parity.py tests/test_bengal_theme_package.py tests/test_css_syntax.py -q`
- `uv run poe build-manifest-check`
- Theme browser proof for promoted packs across light, dark, and system modes.

Collateral:

- `docs/APP-THEME.md`
- `docs/TOKENS.md`
- `docs/CHIRP-THEME.md`
- `docs/CHIRP-THEME-PARITY-MATRIX.md`
- Site theming source pages when public docs change.

### 6. Application Chrome Adoption

Goal: make the recipe-first app-chrome system copyable for real Chirp apps.

Next slices:

- Treat filesystem-mounted app pages as the recommended adoption path.
- Publish a copyable app-chrome recipe around `_layout.html`, `_context.py`,
  `_meta.py`, route tabs, shell actions, command triggers, page tools, and local
  fragment endpoints.
- Teach shell, page-root, and inner-fragment target ownership with concrete
  HTMX examples.
- Keep browser fixtures as regression proof for shell/page-root ownership,
  OOB shell actions, command focus, and overflow.
- Revisit helpers only after independent reference implementations repeat route-handler boilerplate outside
  filesystem pages.

Acceptance:

- App authors can copy the filesystem recipe without adding a visual mega-shell
  macro.
- Shell navigation, route tabs, and local fragments have distinct response
  contracts.
- Application chrome remains recipe-first until repeated production evidence
  shows a missing public API.

Proof:

- `uv run pytest tests/test_shell_response_targets.py tests/test_filesystem_chrome_response_targets.py -q`
- Targeted browser tests under `tests/browser/test_*chrome*.py`.

Collateral:

- `docs/SHELL-TABS-CONTRACT.md`
- `docs/NAVIGATION.md`
- `docs/DENSE-NAVIGATION-RECIPES.md`
- `docs/plans/PLAN-application-chrome-system.md`
- Published navigation pattern source when site content changes.

Current application-chrome queue:

- Private fixtures now prove current composition for page actions, linked
  nav/sidebar, compact headers/page heroes, and shell response/OOB branching.
- Dense reference/data and agent-discovery proof now exist too. Their next
  slice is proof analysis against current primitives, not another brief and not
  an immediate data-grid, reference-page macro, manifest schema, or copied-source
  workflow.
- The next qualifying evidence is deliberately built reference implementation
  repetition: a second scenario-complete non-Bengal page-action, linked-branch,
  or compact docs/reference/catalog implementation, or a third
  scenario-complete hand-written route family outside `mount_pages()` for shell
  response/OOB helpers.
- Do not spend more productization slices creating artificial chrome fixtures
  unless they test a new failure mode; use new slices to build reference
  evidence, improve guidance, or stop and ask for an explicit public API/design
  plan.
- Use `docs/reference-implementations/PROOF-ANALYSIS.md` as the decision ledger
  for whether current proof routes to recipe guidance, more independent
  reference evidence, or a public API/design stop-and-ask.
- Use `docs/reference-implementations/RECIPE-GUIDANCE.md` when proof analysis
  keeps the surface on current primitives and the next productization work is
  author guidance.

### 7. Bengal And chirp-theme Integration

Goal: prove Chirp UI as a first-class Bengal library surface, not only a
standalone component catalog.

Next slices:

- Finish Bengal library asset modes: `bundle`, `link`, and `none`.
- Ensure Bengal library declarations register Chirp UI macros, CSS, and runtime
  helpers without filesystem-relative imports.
- Continue migrating chirp-theme output to Chirp UI-native templates and
  token vocabulary.
- Keep Bengal docs chrome separate from general Chirp app shell contracts.
- Use Bengal as evidence for smaller contracts first: compact headers,
  `page_hero` empty-slot behavior, linked branch navigation, page actions,
  reference cards, semantic icons, and footer/content ownership.

Acceptance:

- `libraries = ["chirp_ui"]` is enough for a Bengal app/theme to consume Chirp
  UI assets and macros through the documented contract.
- Static and dev outputs resolve the same logical assets.
- `chirp-theme` CSS contains only theme tokens, content polish, and actively
  referenced vertical styles.

Proof:

- `uv run pytest tests/test_bengal_theme_package.py tests/test_docs_site.py -q`
- Bengal browser proof when layout, focus, search, nav, or theme controls move.

Collateral:

- `docs/BENGAL-THEME-ANATOMY.md`
- `docs/CHIRP-THEME.md`
- `docs/CHIRP-THEME-PARITY-MATRIX.md`
- `docs/plans/PLAN-bengal-chirpui-library-contract.md`
- `docs/plans/PLAN-chirp-theme-content-parity.md`

### 8. Verification Reliability

Goal: make every productization slice reproducible from a clean checkout.

Next slices:

- Keep generated `manifest.json`, `chirpui.css`, generated component docs, and
  site artifacts inside drift gates.
- Keep the Kida mismatch troubleshooting path current.
- Run full CI for any slice that touches public macros, generated outputs, CSS,
  packaging, or multiple runtime surfaces.

Acceptance:

- Local maintainers and agents can run the documented commands without guessing
  which interpreter or generated outputs matter.
- Narrow proof is allowed only when the PR states why full CI was not run.

Proof:

- `uv run poe build-manifest-check`
- `uv run poe build-css-check`
- `uv run poe build-docs-check`
- `uv run poe ci` for cross-surface changes.

Collateral:

- `docs/VERIFICATION.md`
- `docs/plans/done/PLAN-test-coverage-hardening.md`
- `pyproject.toml` only when task definitions change.

## Recommended Execution Order

1. Make the registry product surface and evidence labels clear enough that
   humans and agents can choose the right contracts.
2. Add anatomy/evidence ledgers to high-risk surfaces before promoting more
   public API.
3. Stabilize the visual audit and theme gallery enough that they become default
   proof surfaces.
4. Use those proof surfaces to close public-surface decisions.
5. Productize application chrome through filesystem recipes and HTMX target
   contracts.
6. Finish Bengal integration as a reference implementation path and use Bengal pressure to
   mature smaller contracts before shell composites.
7. Continue opportunistic CSS scope conversion and verification hardening
   throughout.

## Promotion Gates

Before promoting any component, pattern, or theme pack:

- The registry, macro, CSS, manifest, docs, examples, and tests agree.
- The visual audit or a browser-tested recipe shows the surface in realistic
  context.
- Reduced-motion, focus, keyboard, overflow, and responsive behavior are proven
  when relevant.
- No utility-class vocabulary, Skeleton class alias, or component-local theme
  fork is introduced.
- Generated outputs are rebuilt by their scripts.

## Parity Matrix

| Contract | API/CLI | Programmatic | Protocol | Schema/Types | Docs | Examples | Tests |
|---|---|---|---|---|---|---|---|
| Registry product | Find/inspect only until designed | Registry and manifest queries | Local package data | No schema bump without RFC | Source inventory and generated docs | Curated snippets | Manifest/find/docs ratchets |
| Anatomy/evidence | No new API initially | Anatomy and proof records in docs/tests | Roles, states, focus, runtime | Descriptor fields deferred | Anatomy docs and stabilization ledgers | Browser fixtures | Render/browser/a11y-risk proof |
| Visual showcase | No new API | Existing macros only | Static/browser render | Existing manifest maturity | Visual audit docs | Design-system showcase | Visual audit and browser proof |
| Public surface | No removal before 1.0 gate | Descriptor maturity/authoring | Macro compatibility retained | Manifest maturity/authoring | Stabilization doc and generated options | Preferred examples only | Manifest/docs ratchets |
| Theme authoring | List/read only unless designed | Theme-pack catalog | Token CSS load order | Manifest theme packs | Theme docs and token explorer | Theme gallery | Token, package, browser tests |
| App chrome | No mega-shell macro | Filesystem recipe contracts | HTMX targets and OOB regions | Existing shell metadata | Shell/navigation docs | Filesystem chrome fixture | Server and browser chrome tests |
| Bengal integration | Library declaration path | Theme/library metadata | Asset modes | Package data contract | Bengal/theme docs | Packaged theme fixtures | Package/docs/browser tests |
| Verification | Poe commands | Build scripts | Generated artifact gates | Manifest schema stays explicit | Verification docs | N/A | CI and drift checks |

## Not Now

- `application_chrome()`, `workspace_shell()`, `chrome_frame()`, or
  `object_header()` without new real-app evidence.
- Tailwind-compatible utilities or Skeleton class aliases.
- Theme export/write workflows before source format, overwrite policy, and
  validation are designed.
- New framework-component ports.
- Figma kit work.
- New manifest schema fields for anatomy or chrome layers without a concrete
  generated-output consumer.
- Broad component expansion while experimental and legacy surfaces remain
  ambiguous.

## Steward Notes

Consulted stewards:

- Documentation steward
- Planning steward
- Existing Skeleton-equivalent, application-chrome, theme, public-surface, and
  verification plans

Accepted findings:

- New planning direction must be indexed and tied to active roadmap workstreams.
- Planning must not imply public APIs before registry, CSS, manifest, docs,
  examples, and proof are ready.
- Application chrome stays recipe-first after the first reference
  implementation wave.
- Productization work should reduce stale planning noise, not add a parallel
  backlog.

Deferred findings:

- Full multi-steward swarm. The user did not invoke `ask stewards`; consult
  domain stewards explicitly before implementation slices that touch public API,
  generated schema, theme contracts, or Bengal asset contracts.

Remaining risk:

- This umbrella plan can become a duplicate roadmap if not kept thin. Prefer
  updating the specific child plans when implementation starts.
