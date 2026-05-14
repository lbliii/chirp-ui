# PLAN: Pre-1.0 Productization Saga

Status: active plan
Date: 2026-05-14
Trigger: The project has strong Skeleton-comparable architecture, but needs a
clear pre-1.0 push that makes the quality visible, teachable, and stable.

## Goal

Make Chirp UI feel ready for serious Python application authors before adding
more public surface area.

The next phase is not a component-count race. It is a productization pass over
the quality that already exists: visual proof, theme authoring, public-surface
decisions, application-chrome adoption, Bengal integration, and reliable
verification.

## Current Position

Chirp UI has crossed the architecture-risk threshold:

- `chirpui-manifest@5` projects registry metadata for components, params,
  slots, classes, tokens, runtime requirements, maturity, and authoring hints.
- `336` components are manifest-visible.
- `202` components are stable, `93` are experimental, `39` are legacy, and
  `2` are internal.
- The preferred authoring surface is intentionally narrow: composition
  primitives such as `stack`, `cluster`, `grid`, `frame`, `block`, `layer`,
  and `prose`.
- Theme packs exist (`atlas`, `ember`, `sage`) with token-only proof, but remain
  experimental.
- Application chrome has real consumer/browser proof and remains recipe-first.
- Anatomy docs and tests cover the major interactive families.
- CSS, manifest, docs, and examples are generated or checked as registry
  projections.

Compared to Skeleton, Chirp UI is competitive on architecture, verification,
and Python-native introspection. It is not yet at public product parity on
docs polish, theme tooling, live examples, ecosystem affordances, or first-run
teaching.

## Productization Thesis

Chirp UI should win by being:

- Python-native and registry-grounded.
- Token-first instead of utility-class-first.
- HTMX/Alpine-aware without owning framework state.
- Agent-groundable through generated manifests and curated examples.
- Small enough to verify, but complete enough for real app chrome, forms,
  overlays, navigation, and content surfaces.

Do not chase Skeleton by copying Tailwind utilities, framework components, or
class aliases. Translate only the product strengths that match Chirp's category:
coherent themes, clear docs, strong examples, visible quality, and predictable
contracts.

## Ranked Epics

### 1. Visible Design-System Showcase

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

### 2. Public Surface Stabilization

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

### 3. Theme Authoring UX

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

### 4. Application Chrome Adoption

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
- Revisit helpers only after real apps repeat route-handler boilerplate outside
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

### 5. Bengal And chirp-theme Integration

Goal: prove Chirp UI as a first-class Bengal library surface, not only a
standalone component catalog.

Next slices:

- Finish Bengal library asset modes: `bundle`, `link`, and `none`.
- Ensure Bengal library declarations register Chirp UI macros, CSS, and runtime
  helpers without filesystem-relative imports.
- Continue migrating chirp-theme output to Chirp UI-native templates and
  token vocabulary.
- Keep Bengal docs chrome separate from general Chirp app shell contracts.

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

### 6. Verification Reliability

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

1. Stabilize the visual audit and theme gallery enough that they become the
   default proof surface.
2. Use the proof surface to close public-surface decisions.
3. Productize application chrome through filesystem recipes and HTMX target
   contracts.
4. Finish Bengal integration as a real consumer path.
5. Continue opportunistic CSS scope conversion and verification hardening
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
  generated consumer.
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
- Application chrome stays recipe-first after the first consumer adoption wave.
- Productization work should reduce stale planning noise, not add a parallel
  backlog.

Deferred findings:

- Full multi-steward swarm. The user did not invoke `ask stewards`; consult
  domain stewards explicitly before implementation slices that touch public API,
  generated schema, theme contracts, or Bengal asset contracts.

Remaining risk:

- This umbrella plan can become a duplicate roadmap if not kept thin. Prefer
  updating the specific child plans when implementation starts.
