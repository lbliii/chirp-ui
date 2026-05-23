# PLAN: Skeleton-Equivalent Roadmap

**Status:** superseded and archived
**Created:** 2026-05-11
**Trigger:** User wants Chirp UI to become the Python-native equivalent of Skeleton's design-system quality.
**Reference:** Skeleton v4 design system, themes, presets, framework components, and LLM docs.

> Current note: this plan shipped the design lock-in, build/token guardrails,
> appearance/tone pilot, theme packs, docs IA/source ownership, interactive
> anatomy contracts, and agent-source mapping work. The forward productization
> direction now lives in
> [`PLAN-pre-1.0-productization-saga.md`](../PLAN-pre-1.0-productization-saga.md).

## Goal

Make Chirp UI feel as coherent, adaptive, and teachable as Skeleton while
preserving Chirp's category difference:

- Python-native component registry as source of truth.
- No utility-class vocabulary.
- Token-only theme packs.
- Generated CSS, manifest, docs, site artifacts, and LLM surfaces.
- HTMX/Alpine-native behavior instead of framework-owned state.

This is not a port of Skeleton. It is a translation of Skeleton's strongest
ideas into Chirp's registry, macro, token, and generated-artifact model.

## Steward Notes

Consulted stewards:

- Core Registry and Python API
- Templates/CSS/Behavior
- Docs and Site
- Examples and Showcase
- Tests and Build Scripts
- Bengal Theme

Convergence:

- Appearance/tone must be descriptor-backed metadata and validated macro params,
  not CSS-only preset classes.
- Sprint 2 will use dedicated `appearances` and `tones` descriptor fields, not a
  generic axes model.
- `danger` is the only shared destructive/action tone. Existing `error` values
  remain component-local legacy compatibility where already shipped and must not
  be added to the shared tone registry.
- Theme packs must be token-only and package-visible through a typed catalog.
- LLM docs endpoints must be generated from the manifest, durable docs, and
  vetted copyable examples.
- Interactive anatomy docs require executable unit/browser proof, not prose only.
- Bengal `chirp-theme` must map to the same theme vocabulary or label old
  palette controls as transitional aliases.

Minority reports:

- None on direction. The only sequencing tension is whether theme packs or
  appearance/tone should ship first. Accepted resolution: harden token/build
  contracts first, then ship a small pilot for each.

Deferred findings:

- No write/export workflow for themes until source format, destination policy,
  overwrite behavior, package-data contract, and token validation are designed.
- No global cross-component preset vocabulary until a pilot component set proves
  `appearance` and `tone`.
- No generic descriptor-axis model until at least a third repeated axis proves
  the abstraction and stable manifest field names remain possible.
- No prose-only interactive anatomy in LLM endpoints.
- No static showcase scraping for copyable snippets.

## Contract Matrix

| Contract | API/CLI | Programmatic | Protocol | Schema/Types | Docs | Examples | Tests |
|---|---|---|---|---|---|---|---|
| Appearance/tone | Optional later CLI docs only | Descriptor fields, validation filters | Macro params only | Manifest schema bump | Design-system and component docs | Dynamic showcase matrix | Manifest, validation, CSS parity |
| Theme packs | List API first; export deferred | Frozen catalog in library contract | Token CSS loaded after `chirpui.css` | Manifest theme catalog | Theming docs, README | Theme gallery | Package data, token-only scan, browser visuals |
| LLM endpoints | Site build tasks | Manifest/docs generator | Public `/llms*.txt`, `agent.json` | Endpoint schema/version | Generated endpoint docs | Vetted snippets only | Determinism and freshness checks |
| Interactive anatomy | No broad API until modeled | Anatomy metadata adjacent to descriptors | ARIA, Alpine, HTMX, focus contracts | Manifest anatomy fields later | Durable anatomy docs | Copyable dynamic fixtures | Unit plus browser keyboard/focus |
| Bengal theme parity | No new public entry point unless needed | Existing `chirp-theme` entry point retained | `data-theme`/palette aliases mapped | Theme-pack catalog cites Bengal surface | `CHIRP-THEME` docs updated | Docs theme showcase | Package/theme parity tests |

## Sprint 0: Design Lock-In

Goal: settle names and source-of-truth before changing public API.

Design docs:

- `docs/DESIGN-appearance-tone.md`
- `docs/DESIGN-theme-pack-catalog.md`
- `docs/DESIGN-llm-endpoints.md`
- `docs/DESIGN-interactive-anatomy.md`

Tasks:

1. Write a design RFC for `appearance` and `tone`.
   - Candidate `appearance`: `filled`, `tonal`, `outlined`, `ghost`.
   - Candidate `tone`: `neutral`, `primary`, `secondary`, `success`, `warning`, `danger`, `info`, `surface`.
   - Decision: `danger` is shared public vocabulary; `error` remains component-local legacy compatibility where already shipped.
2. Define descriptor fields and validation strategy.
   - Decision: dedicated `appearances` and `tones` fields for the Sprint 2 pilot.
   - Must not overload `variant`.
3. Define theme-pack catalog shape.
   - Frozen dataclass or tuple data.
   - Package resource path.
   - Load order.
   - Whether packs appear in `get_library_contract()`, manifest, or both.
4. Define LLM endpoint outputs.
   - Inputs: manifest, generated component options, selected durable docs, vetted dynamic showcase snippets.
   - Outputs: likely `site/public/llms.txt`, `site/public/llms-full.txt`, and `site/public/agent.json`.
5. Define interactive anatomy metadata shape.
   - Start with modal/dialog, dropdown/menu, tabs, tray/drawer.
   - Name required roles, state attributes, trigger/panel relationships, runtime requirements, focus behavior, and browser proof.

Acceptance:

- New RFC docs under `docs/`.
- `docs/INDEX.md` links active plan and RFCs.
- Stop-and-ask decisions recorded before implementation.
- No public macro or manifest changes yet.

## Sprint 1: Build And Token Guardrails

Goal: close existing projection gaps before adding new theme/appearance surface.

Progress:

- 2026-05-11: CSS build manifest coverage test added.
- 2026-05-11: `TOKEN_CATALOG` parity made bidirectional and missing CSS-defined tokens cataloged.
- 2026-05-11: token category guardrail added and obvious non-color category debt corrected.
- 2026-05-11: token-only scanner added for packaged app theme CSS, with `holy-light.css` documented as legacy selector-bearing theme CSS.
- 2026-05-11: `docs/VISION.md` manifest schema reference updated before the
  Sprint 2 schema bump; current shipped schema is `chirpui-manifest@5`.

Tasks:

1. Add a CSS build manifest coverage test.
   - Every `src/chirp_ui/templates/css/partials/*.css` file must be listed exactly once by `scripts/build_chirpui_css.py`, with explicit exclusions only.
2. Add reverse token parity.
   - Fail on CSS-defined `--chirpui-*` tokens missing from `TOKEN_CATALOG`.
   - Keep narrow documented exclusions only if required.
3. Audit token categories.
   - Correct non-color tokens currently classified as color.
   - Add category allowlist tests.
4. Add theme-pack token-only scanner before packs exist.
   - Scanner should reject `.chirpui-*` selectors and non-token component rules in theme-pack CSS.
5. Fix stale manifest-schema docs.
   - README and `docs/VISION.md` agree on the current shipped schema.

Proof:

- `uv run pytest tests/test_chirpui_css_concat.py tests/test_registry_emits_parity.py tests/test_template_css_contract.py tests/test_manifest.py tests/test_css_syntax.py -q`
- `uv run poe build-css-check`
- `uv run poe build-manifest-check`

Collateral:

- `docs/VISION.md`
- `docs/TOKENS.md` if token categories move
- Generated `src/chirp_ui/manifest.json` and `docs/COMPONENT-OPTIONS.md` if token metadata affects output

## Sprint 2: Appearance/Tone Pilot

Goal: prove Skeleton-style presets as Chirp-native macro vocabulary.

Progress:

- 2026-05-11: Descriptor fields `appearances` and `tones` added for the first
  pilot slice.
- 2026-05-11: `btn`, `badge`, `alert`, and `surface` accept optional
  `appearance`/`tone` params, with `danger` as the shared destructive tone and
  legacy `variant="error"` retained as component-local compatibility.
- 2026-05-11: Manifest schema bumped for appearance/tone and generated
  component options now project appearance/tone fields.
- 2026-05-11: CSS parity, validation, rendering, and generated-output checks
  cover the pilot classes and exclude shared `tone="error"`.
- 2026-05-11: `field` / `text_field` joined the pilot with appearance/tone
  params while preserving validation error as component state, not shared tone.
- 2026-05-11: `docs/APPEARANCE-TONE.md` and the component showcase
  `/appearance-tone` route added migration teaching and copyable macro examples.
- 2026-05-11: `card` joined the pilot as the surface-like container path,
  with token-backed treatment CSS and showcase examples.

Locked decisions:

- Use dedicated `appearances` and `tones` descriptor fields for the pilot.
- Use `danger` as the shared destructive/action tone.
- Do not add shared `tone="error"`.
- Keep existing component-local `variant="error"` compatibility where already
  shipped: `alert`, `badge`, `toast`, `status_indicator`, `notification_dot`,
  and `streaming_bubble`.
- Treat existing local `tone` parameters such as `aura(tone=...)` as
  component-local vocabularies unless explicitly migrated.

Pilot components:

- `btn`
- `badge`
- `alert`
- `card`
- `surface`
- one form control if the naming holds

Tasks:

1. Add descriptor fields for `appearance` and `tone`.
   - Extend descriptor emits so `appearances` and `tones` derive
     `chirpui-{block}--{value}` classes directly.
   - Do not hide normal axis classes in `extra_emits`.
2. Add validation helpers and filters.
   - Strict mode warns with actionable fallback.
   - Invalid values do not silently produce classes.
3. Project the new fields into the manifest.
   - Bump manifest schema if fields are public.
4. Update pilot macros to accept the new params.
   - Existing `variant` behavior must keep working or receive an explicit migration path.
   - Add per-pilot mapping tables for old `variant`, new `appearance`, new
     `tone`, compatibility status, and preferred examples.
5. Map appearance/tone to component-owned BEM modifiers and token aliases.
   - No standalone `chirpui-tone-*`, `chirpui-preset-*`, or utility-like classes.
   - New `tone="danger"` CSS uses `--chirpui-danger`; legacy `error` variants
     may keep `--chirpui-error` paths until migration.
6. Add dynamic showcase matrix.
   - Defaults, at least two non-default tones, disabled/error states where relevant, and invalid fallback coverage.

Proof:

- `uv run pytest tests/test_manifest.py tests/test_manifest_signatures.py tests/test_validation.py tests/test_filters.py tests/test_registry_emits_parity.py tests/test_template_css_contract.py -q`
- `uv run poe build-manifest-check`
- `uv run poe build-docs-check`
- Showcase route smoke with validation warnings treated as failures
- Manifest tests prove shared `tones` exclude `error`.
- Rendering/validation tests prove existing local `variant="error"` values still
  work where retained.

Closure synthesis:

- Accepted: the first public preset contract is component-owned
  `appearance` / `tone`, projected through descriptors, manifest, generated
  docs, CSS, examples, and validation.
- Accepted: `danger` is the shared destructive tone; `error` remains
  component-local legacy compatibility where already shipped.
- Accepted: the pilot surface is `btn`, `badge`, `alert`, `card`, `surface`,
  and `field` / `text_field`.
- Deferred: broad all-component rollout, generic arbitrary axis fields,
  `tone="error"`, theme-pack work, anatomy manifest fields, and LLM endpoints.
- Required proof: unit/contract CI, generated-output checks, docs-site build,
  and visual QA of `/appearance-tone` across desktop and mobile.

Collateral:

- `docs/COMPONENT-OPTIONS.md`
- `docs/COMPOSITION.md` or a new appearance/tone design-system doc
- `site/content/docs/components/`
- `examples/component-showcase/README.md`
- README quick examples if the new params become preferred
- Changelog or migration note if `variant` guidance changes

## Sprint 3: Curated Theme Packs

Goal: ship a small, typed, token-only theme catalog.

Progress:

- 2026-05-11: Added immutable `ThemePack` metadata and the first catalog
  packs: `atlas`, `ember`, and `sage`.
- 2026-05-11: Projected theme packs into `get_library_contract()` and the
  manifest schema `chirpui-manifest@5`.
- 2026-05-11: Added package-data/resource tests, deterministic ordering tests,
  token-only scanner coverage, and CSS mode checks for catalog packs.
- 2026-05-11: Added the component showcase `/theme-packs` matrix with isolated
  preview routes for each pack and mode.
- 2026-05-11: Bengal `chirp-theme` palette controls now expose transitional
  `data-theme-pack` mappings to `atlas`, `ember`, and `sage`; later bespoke
  theme work removed those transitional aliases.
- 2026-05-11: Added browser-contract coverage that loads each catalog pack in
  Chromium and verifies light, dark, and system-mode token resolution.
- 2026-05-11: Expanded theme-pack browser proof across desktop and mobile
  viewports for navigation, form controls, overlay layers, and compact data
  tables.

Closure:

- Status: Sprint 3 closed on 2026-05-11.
- Accepted proof: immutable catalog/API, library contract projection, manifest
  projection, package-data tests, token-only CSS scanner, syntax checks,
  deterministic ordering checks, Bengal transitional alias tests, data-route
  integration tests, showcase template analysis, targeted Playwright
  theme-pack proof, full `uv run poe ci`, and full `uv run poe ci-browser`.
- Collateral updated: `docs/APP-THEME.md`, `docs/CHIRP-THEME.md`,
  `docs/CHIRP-THEME-PARITY-MATRIX.md`, README, site theming docs, component
  showcase docs/routes/templates, changelog fragment, manifest, and package
  data tests.
- Deferred: theme export/write commands stay out of scope until source format,
  overwrite policy, destination policy, and validation workflow are designed.
- Remaining risk: Bengal palette names are transitional aliases, not stable
  theme-pack names. The docs and tests pin the mapping, but future UI should
  present `atlas`, `ember`, and `sage` as the forward vocabulary.

Initial packs:

- 3 to 5 curated packs only.
- Each pack must define light, dark, and system branches.
- Each pack authored in `--chirpui-*` tokens.
- Legacy Bengal `--color-*` aliases may be derived only where retained Bengal CSS still needs them.

Tasks:

1. Add immutable theme-pack metadata.
   - Name, label, description, resource path, supported modes, maturity.
2. Expose read-only list API.
   - Project into library contract and manifest if accepted in Sprint 0.
3. Package token-only CSS resources.
4. Add docs theme gallery and dynamic showcase theme matrix.
5. Map Bengal theme controls and palettes to the same vocabulary or document transitional aliases.
6. Defer export/write commands unless Sprint 0 explicitly approved the workflow.

Proof:

- Package-data/resource tests.
- Token-only scanner for every pack.
- CSS syntax checks.
- Theme list ordering determinism.
- Browser visual QA across light/dark/system, desktop/mobile, covering buttons, forms, alerts, surfaces, overlays, navigation, and dense data.
- `uv run pytest tests/test_install.py tests/test_css_syntax.py tests/test_bengal_theme_package.py -q`

Collateral:

- `docs/APP-THEME.md`
- `docs/TOKENS.md`
- `docs/CHIRP-THEME.md`
- `docs/CHIRP-THEME-PARITY-MATRIX.md`
- `site/content/docs/theming/`
- `examples/docs-theme-showcase/`
- README CSS/theming section

## Sprint 4: Docs IA And LLM Endpoints

Goal: make the system teachable like Skeleton without duplicating facts.

Progress:

- 2026-05-11: Added `docs/DOCS-IA-MIGRATION.md` as the Sprint 4
  source-of-truth map from current published docs pages to the target IA,
  durable canonical sources, and future agent-facing source provenance labels.
- 2026-05-12: Scoped Sprint 4 away from overriding Bengal/SSG-owned
  `llms.txt` and `agent.json`; accepted direction is source-content enrichment,
  canonical source links, and manifest publication under Chirp UI-owned names.

Docs IA target:

- Get Started
- Fundamentals
- Design System
- Components
- Patterns
- Integrations
- Agent Manifest
- Theming

Tasks:

1. Create a migration matrix from current docs to target IA.
   - Name canonical durable doc for each site page.
2. Refresh stale published examples.
   - Version snippets and class-heavy home cards need review.
3. Improve SSG source content instead of overriding SSG outputs.
   - Bengal owns `llms.txt`, `agent.json`, search indexes, sitemap, and page projections.
   - Chirp UI owns manifest publication, durable docs, site page front matter, and canonical source links.
4. Add regression checks for the ownership boundary.
   - Docs tasks must not call a custom generator for Bengal-owned LLM artifacts.
5. Add provenance labels in source maps and source content.
   - Manifest-derived, docs-derived, example-derived.
6. Reject non-public snippets.
   - No `sc-*`, `docs-*`, static-gallery wrappers, inline fixture scripts, or raw appearance/tone classes in copyable LLM snippets unless explicitly marked non-copyable.

Proof:

- `uv run pytest tests/test_docs_site.py -q`
- Docs IA coverage and SSG ownership-boundary tests
- `uv run poe docs-build-all`

Collateral:

- `docs/INDEX.md`
- `site/content/docs/**`
- `site/config/_default/menu.yaml` if nav changes
- `pyproject.toml`
- `site/AGENTS.md` only if generated artifact expectations change

## Sprint 5: Interactive Anatomy Contracts

**Status:** closed 2026-05-12

Goal: document and verify the actual rendered anatomy of interactive components.

Initial families:

- Modal/dialog and confirm dialog
- Dropdown/menu/split button
- Tabs/route tabs, with clear distinction between tab semantics and navigation semantics
- Drawer/tray
- Theme/search/mobile-nav hooks in packaged Bengal theme

Tasks:

1. Audit each family before publishing docs.
   - Classes, roles, state attributes, ids, trigger relationships, HTMX behavior, Alpine factory, keyboard/focus behavior.
2. Fix known safety gaps before docs bless them.
   - Dropdown menu payloads must stay out of Alpine object literals; use
     `data-*` payloads read by named Alpine code or add a proven JS-string-safe
     filter.
3. Add anatomy metadata if Sprint 0 approved projection.
   - Closure decision: not now. Sprint 5 shipped docs-plus-tests contracts;
     descriptor/manifest anatomy projection needs a later schema design and
     concrete consumer.
4. Add durable docs plus concise site mirrors.
5. Add copyable dynamic showcase fixtures.
   - Closure decision: existing browser fixtures and component showcase routes
     remain the executable examples for this sprint. A generated copyable
     snippet catalog belongs with the later agent-facing synthesis work, not
     inside anatomy docs.
6. Add Bengal static-first anatomy coverage for theme popover, search modal, mobile nav dialog, and tabs.

Proof:

- Unit render tests for structure and ARIA.
- Browser tests for open/close, keyboard navigation, focus return, and Alpine lifecycle.
- `uv run poe test-browser` for changed interactive families.
- `uv run poe ci` for non-browser contracts.

Progress:

- 2026-05-12: Started Sprint 5 dropdown/menu anatomy hardening by moving
  menu and split-menu selection payload assembly out of inline Alpine object
  literals and into `data-*` attributes read by `chirpuiDropdown().selectItem()`.
- 2026-05-12: Published the dropdown/menu anatomy contract in
  `docs/DROPDOWN-ANATOMY.md` with a site mirror, docs IA coverage, render
  tests, and browser proof for the menu family.
- 2026-05-12: Started the modal/dialog anatomy slice with native modal,
  confirm dialog, and modal overlay render/browser proof plus
  `docs/MODAL-ANATOMY.md` and a site mirror.
- 2026-05-12: Started the tabs/route-tabs anatomy slice, hardened
  `tabs_panels` payloads to escaped `data-*` attributes read by
  `chirpuiTabs()`, and published `docs/TABS-ANATOMY.md` with a site mirror.
- 2026-05-12: Published the drawer/tray anatomy slice in
  `docs/DRAWER-TRAY-ANATOMY.md` with render tests, drawer/tray browser proof,
  docs IA coverage, and a site mirror.
- 2026-05-12: Published the Bengal theme controls anatomy slice in
  `docs/BENGAL-THEME-ANATOMY.md` with a theming site mirror and package tests
  for theme popovers, search modal/inline hooks, mobile nav, docs TOC, and
  docs-site tab enhancement hooks.
- 2026-05-12: Closed Sprint 5 with descriptor/manifest anatomy metadata
  deferred, dynamic showcase snippet catalog deferred to agent-facing synthesis,
  and full CI proof at `uv run poe ci` with 1869 passing tests.

Closure synthesis:

- Accepted: five anatomy families now have durable docs or theme docs, site
  mirrors where published, and tests that pin rendered structure, ARIA/state
  hooks, Alpine/native runtime boundaries, and Bengal static hooks.
- Accepted: dropdown and tabs payload safety gaps were fixed before docs
  blessed those contracts.
- Deferred: descriptor/manifest anatomy metadata remains a not-now item.
  Required future proof: schema migration notes, descriptor/template/doc parity,
  generated endpoint parity, and a real consumer.
- Deferred: a copyable dynamic snippet catalog remains a not-now item. Required
  future proof: generated source provenance, non-public fixture filtering, and
  tests rejecting `sc-*`, `docs-*`, inline fixture scripts, and raw class-heavy
  examples.
- Remaining risk: browser proof exists across the changed interactive families,
  but Bengal theme controls currently rely on package/static hook tests plus
  docs build proof rather than a dedicated Bengal browser fixture.

Collateral:

- `docs/ALPINE-MAGICS.md`
- `docs/HTMX-PATTERNS.md`
- `docs/SHELL-TABS-CONTRACT.md`
- New anatomy docs under `docs/`
- `site/content/docs/components/`
- `site/content/docs/theming/`
- Existing browser fixtures and component showcase routes
- Generated LLM endpoints: no direct changes; Bengal-owned outputs remain SSG-owned

## Sprint 6 Candidate: Agent-Facing Synthesis

**Status:** residual source contract

Goal: turn the shipped docs, manifest, theme catalog, and showcase examples into
agent-safe source maps without overriding Bengal-owned SSG artifacts.

2026-05-13 status: the source inventory, generated-output map, no-new-artifact
decision, and snippet provenance gates are in place. Remaining work is only
candidate snippet curation after a concrete consumer asks for copyable examples.

Candidate tasks:

1. Define the vetted snippet source inventory.
   - Dynamic showcase routes and durable docs are allowed.
   - Static showcase scaffolding, browser test pages, and docs-site wrappers are
     excluded unless explicitly marked non-copyable.
   - 2026-05-12: Added `docs/AGENT-SOURCE-INVENTORY.md` with provenance labels,
     snippet eligibility states, candidate dynamic showcase sources, and
     explicit exclusions for generated/static/test surfaces.
2. Add snippet provenance tests.
   - Reject `sc-*`, `docs-*`, inline fixture scripts, raw appearance/tone
     modifier classes, and raw class-heavy snippets where a macro example
     exists.
   - 2026-05-12: Added docs-site provenance tests for source path existence,
     allowed eligibility values, forbidden snippet roots, and explicit
     exclusion-rule coverage.
3. Add an agent-facing source map that points to existing generated SSG outputs
   and Chirp-owned source inputs without replacing Bengal `llms.txt` or
   `agent.json`.
   - 2026-05-12: Added `docs/AGENT-SOURCE-MAP.md` to map Bengal-owned outputs,
     the Chirp-owned published manifest, source inputs, and forbidden output
     name overlaps.
4. Decide whether any Chirp-owned generated artifact is still needed after the
   Bengal SSG ownership decision.
   - 2026-05-12: Decision: no new Chirp-owned agent artifact is needed for this
     phase; continue enriching sources and keep `site/public/chirpui.manifest.json`
     as the only Chirp-owned published machine artifact.
5. Keep descriptor/manifest anatomy metadata deferred unless a concrete
   generated consumer requires it.

Proof:

- `uv run pytest tests/test_docs_site.py -q`
- Snippet provenance tests
- `uv run poe docs-build-all`
- `uv run poe ci`

Collateral:

- `docs/DOCS-IA-MIGRATION.md`
- `docs/DESIGN-llm-endpoints.md`
- `docs/DESIGN-interactive-anatomy.md` only if metadata projection is reopened
- `site/content/docs/**`
- `scripts/docs_site.py` only if source enrichment changes

## Ranked Backlog

1. Agent-facing synthesis and snippet provenance.
2. Bengal theme vocabulary/parity cleanup.
3. Descriptor/manifest anatomy metadata only after a concrete consumer appears.
4. Theme export/write workflow design.
5. Broader appearance/tone rollout beyond the pilot components.

## Risks

- `appearance`/`tone` becomes a disguised utility vocabulary.
- Theme packs fork component CSS instead of tuning tokens.
- LLM endpoints scrape static showcase scaffolding and teach non-public APIs.
- Anatomy docs describe desired behavior instead of tested behavior.
- Bengal theme palettes drift from app theme packs.
- Manifest schema grows without migration notes or stale-doc checks.

## Not Now

- Tailwind-compatible utility classes.
- Skeleton class-name aliases.
- Theme export/write commands before list/catalog proof.
- New runtime dependencies for behavior primitives.
- Big-bang CSS envelope migration.
- Figma kit work.
- Static showcase as a source for copyable snippets.
- Framework-component ports for React/Svelte/Vue.

## Definition Of Done

For any implementation PR under this plan:

- Accepted steward findings identify proof and collateral.
- Generated outputs are rebuilt by scripts, not hand-edited.
- Public macro/manifest/schema changes include docs and migration notes.
- Full `uv run poe ci` is green, or the PR states exactly which narrower checks ran and why full CI was not run.
- Browser proof is included for any interactive anatomy, theme visual, or layout-sensitive change.
