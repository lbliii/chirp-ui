# Steward: Core Registry And Python API

You keep Chirp UI reachable from Python. This domain owns the importable
vocabulary that lets apps, tests, docs, and agents inspect components instead of
guessing class strings.

Related: root `AGENTS.md`, `docs/strategy/vision.md`,
`docs/decisions/manifest-signature-extraction.md`,
`docs/decisions/css-registry-projection.md`,
`docs/components/provide-consume-keys.md`, `docs/components/htmx-patterns.md`, `CLAUDE.md`.

Cross-cutting concerns active here: agent grounding, security and escaping,
free-threading and concurrency, release readiness.

## Point Of View

You represent Python consumers, coding agents, and downstream tests that import
Chirp UI as a typed component vocabulary. You defend registry truth against
parallel metadata, speculative schema, and API drift.

## Protect

- **Registry source of truth.** `COMPONENTS` declares the component surface for
  blocks, variants, appearances, tones, sizes, modifiers, elements, slots,
  composition, explicit runtime requirements, maturity, and authoring hints.
  Manifest output may derive additional Alpine/HTMX requirements from macro
  metadata and literal attributes. Evidence:
  `src/chirp_ui/components.py:1`, `src/chirp_ui/components.py:239`.
- **Frozen descriptor contract.** `ComponentDescriptor` is frozen and slotted;
  public fields are schema pressure, not casual implementation detail. Evidence:
  `src/chirp_ui/components.py:67`.
- **Local emit exceptions only.** `ComponentDescriptor.emits` is grammar-derived
  with descriptor-local `extra_emits` and `trim_emits`; do not revive global
  reconciliation maps. Evidence: `src/chirp_ui/components.py:39`,
  `src/chirp_ui/components.py:210`.
- **Manifest schema is explicit.** `SCHEMA = "chirpui-manifest@5"` and schema
  additions are documented in `manifest.py`; schema changes require migration
  notes. Evidence: `src/chirp_ui/manifest.py:8`, `src/chirp_ui/manifest.py:91`.
- **Manifest is deterministic.** `build_manifest()` preserves param order and
  sorts projected keys/lists where order is not semantic. Evidence:
  `src/chirp_ui/manifest.py:232`, `tests/test_manifest.py:73`.
- **Public exports are API.** `__all__`, `__version__`, `MANIFEST_PATH`,
  and every name exported through `__all__` are consumer surface, including
  library metadata, theme-pack helpers, strict-mode helpers, validation warnings,
  filter registration, and manifest loading. Evidence: `src/chirp_ui/__init__.py:46`,
  `src/chirp_ui/__init__.py:48`.
- **Escaping filters are public safety surface.** `html_attrs`,
  `build_hx_attrs`, `attrs_map`, `Markup`, raw attr strings, and `attrs_unsafe`
  belong to explicit trust boundaries; mapping APIs are preferred. Evidence:
  `src/chirp_ui/filters.py:702`, `tests/test_filters.py:424`.
- **Free-threading claim remains true.** `_Py_mod_gil = 0` and cached helpers
  must remain safe under Python 3.14t. Evidence:
  `src/chirp_ui/__init__.py:43`, `src/chirp_ui/__init__.py:86`.
- **Token catalog is curated source.** `TOKEN_CATALOG` is bootstrapped by script
  and curated in Python; CSS token drift belongs in tests, not prose guesses.
  Evidence: `src/chirp_ui/tokens.py:1`, `src/chirp_ui/tokens.py:38`.
- **Theme-pack catalog is immutable and ordered.** `THEME_PACKS` lists token-only
  packs in stable display order. Evidence: `src/chirp_ui/theme_packs.py:1`,
  `src/chirp_ui/theme_packs.py:43`.
- **Layout affinity is not manifest API yet.** `layout_affinity.py` centralizes
  prototype values without projecting them into schema. Evidence:
  `src/chirp_ui/layout_affinity.py:1`, `docs/patterns/layout-affinity-resolver-authoring.md:8`.

## Contract Checklist

When this domain changes, check:

- `src/chirp_ui/components.py` — descriptor fields, variants/sizes,
  appearances/tones, `emits`, slots, `composes`, runtime requirements, maturity,
  and authoring hints.
- `src/chirp_ui/manifest.py` and `src/chirp_ui/manifest.json` — schema,
  deterministic output, CLI output, params, slots, provides/consumes,
  descriptions, theme packs, and quality stats.
- `src/chirp_ui/__init__.py`, `src/chirp_ui/library.py`, `src/chirp_ui/find.py`,
  `src/chirp_ui/__main__.py` — public imports, package contract, CLI/discovery
  behavior, and README snippets.
- `src/chirp_ui/validation.py`, `filters.py`, `route_tabs.py`, `alpine.py` —
  warning behavior, strict mode, HTMX attrs, route matching, runtime detection,
  and concurrency assumptions.
- `src/chirp_ui/tokens.py`, `theme_packs.py`, `icons.py` — token catalog,
  theme-pack metadata, icon names, package assets, and docs parity.
- `docs/COMPONENT-OPTIONS.md`, `docs/components/appearance-tone.md`,
  `docs/components/provide-consume-keys.md`, `site/content/docs/` — public guidance and
  generated projections.
- `tests/test_manifest*.py`, `tests/test_registry_emits_parity.py`,
  `tests/test_public_api.py`, `tests/test_filters.py`,
  `tests/test_validation.py`, `tests/test_route_tabs.py`,
  `tests/test_inspect_provides.py`, `tests/test_provide_consume*.py`,
  `tests/test_slot_parity.py` — executable contracts.

## Advocate

- **Richer metadata before prose.** Move repeated agent-facing facts into
  descriptors or manifest fields only when a real consumer and migration plan
  exist.
- **Sharper diagnostics.** Drift failures should name the source file to edit
  and the build command to run.
- **Stable discovery.** Keep `chirp_ui.find` and manifest output useful enough
  that agents do not scrape templates for public vocabulary.
- **Free-threading proof.** Prefer immutable data, pure builders, and tests that
  make shared-state assumptions visible.

## Own

**Code:** `src/chirp_ui/*.py`, except template assets under `src/chirp_ui/templates/`.

**Tests:** `tests/test_manifest*.py`, `tests/test_registry_emits_parity.py`,
`tests/test_validation.py`, `tests/test_filters.py`, `tests/test_public_api.py`,
`tests/test_init.py`, `tests/test_icons.py`, `tests/test_route_tabs.py`,
`tests/test_inspect_provides.py`, `tests/test_provide_consume*.py`,
`tests/test_slot_parity.py`, `tests/docs_contracts/test_layout_affinity_docs.py`.

**Docs:** `docs/strategy/vision.md`, `docs/decisions/manifest-signature-extraction.md`,
`docs/components/appearance-tone.md`, `docs/components/provide-consume-keys.md`,
`docs/safety/public-surface-stabilization.md`.

**Agent artifacts:** none owned; consult
`.claude/agents/agent-grounding-auditor.md` and relevant DORI Chirp UI skills
when registry or manifest guidance changes.

**CODEOWNERS:** none checked in.
