# Steward: Template, CSS, And Behavior

You keep the rendered UI contract honest. This domain owns Kida macro output,
generated HTML, author CSS partials, generated CSS, HTMX attributes, Alpine
hooks, packaged static behavior, and token-only theme CSS.

Related: root `AGENTS.md`, `src/chirp_ui/AGENTS.md`,
`docs/fundamentals/composition.md`, `docs/fundamentals/primitives.md`,
`docs/fundamentals/layout.md`, `docs/fundamentals/ui-layers.md`,
`docs/fundamentals/css-override-surface.md`,
`docs/fundamentals/transitions.md`, `docs/components/alpine-magics.md`,
`docs/components/htmx-patterns.md`, `docs/components/dnd-fragment-island.md`.

Cross-cutting concerns active here: security and escaping, accessibility, visual
and layout quality, agent grounding, release readiness.

## Point Of View

You represent end users seeing rendered HTML and app developers composing macros
without auditing internals. You defend stable, escaped, accessible output
against hidden script behavior, cascade bleed, utility drift, and stale CSS.

## Protect

- **Macros are public contracts.** Macro params, slots, doc-blocks, and rendered
  attributes must agree with descriptors and generated docs. Evidence:
  `src/chirp_ui/manifest.py:45`, `tests/test_description_coverage.py:70`.
- **Escaped output by default.** `build_hx_attrs(...) | html_attrs` and
  `attrs_map` are the safe path; raw attrs and `| safe` need trust-boundary
  proof. Evidence: `CLAUDE.md:102`, `tests/test_filters.py:424`.
- **Scripts stay exceptional and named.** Named Alpine behavior lives in
  `chirpui-alpine.js`; component macros may emit small `x-data` hooks. Existing
  shell/layout pre-paint and runtime scripts are narrow exceptions that require
  focused shell tests. Evidence: `README.md:214`,
  `tests/test_app_shell_contract.py:47`.
- **Alpine factories are enumerable.** `ALPINE_REQUIRED_COMPONENTS` and
  `tests/test_alpine.py` must stay aligned with rendered `x-data` factories;
  `check_alpine_runtime()` detects missing runtime scripts, not every drift
  shape. Evidence: `src/chirp_ui/alpine.py:58`, `tests/test_alpine.py:55`.
- **CSS partials are source.** `chirpui.css` is generated from
  `src/chirp_ui/templates/css/partials/`. Evidence:
  `scripts/build_chirpui_css.py:10`, `src/chirp_ui/templates/chirpui.css:5`.
- **Layer order is public API.** Do not reorder cascade layers. Evidence:
  `src/chirp_ui/templates/chirpui.css:11`, `tests/test_chirpui_css_concat.py:74`.
- **Component CSS uses scoped envelopes when new or touched.** New component
  partials use `@layer chirpui.component` with an `@scope` boundary unless a
  documented exception applies. Evidence: `CLAUDE.md:94`,
  `docs/strategy/vision.md:70`.
- **Motion token checks are enforceable.** CSS transitions must use motion
  tokens; broader color, spacing, radius, z-index, and font-weight tokenization
  is a review expectation unless tests prove it. Evidence: `CLAUDE.md:90`,
  `tests/test_transition_tokens.py`.
- **Template classes have owners.** Classes emitted in templates must exist in
  CSS and descriptor `emits`; CSS classes must be registry-owned. Evidence:
  `tests/test_template_css_contract.py`, `tests/test_registry_emits_parity.py`.
- **Relationship resolvers stay parent-scoped.** Layout-affinity selectors must
  start from the owning parent and avoid arbitrary descendants. Evidence:
  `docs/patterns/layout-affinity-resolver-authoring.md:90`.

## Contract Checklist

When this domain changes, check:

- `src/chirp_ui/templates/chirpui/*.html` — params, slots, doc-blocks,
  `provide`/`consume`, escaped attrs, ARIA, strict undefined, HTMX/Alpine hooks.
- `src/chirp_ui/components.py` — descriptor params, slots, emits, runtime
  requirements, maturity, authoring, and composition metadata.
- `src/chirp_ui/templates/css/partials/*.css` — source CSS, layer/scope
  envelope, token use, selector boundaries, relationship ownership, responsive
  containment.
- `src/chirp_ui/templates/chirpui.css` — regenerated output only.
- `src/chirp_ui/templates/chirpui-alpine.js`, `chirpui.js`,
  `src/chirp_ui/alpine.py` — factory names, idempotency, lifecycle, runtime
  detection, htmx swap behavior.
- `src/chirp_ui/templates/islands/*.js`, `tests/js/*`, `package.json`,
  `vitest.config.js` — packaged island behavior, static asset paths, and
  Vitest proof.
- `docs/COMPONENT-OPTIONS.md`, anatomy docs, `docs/components/htmx-patterns.md`,
  `docs/components/alpine-magics.md`, `docs/fundamentals/responsive.md`,
  `docs/fundamentals/relationship-contracts.md` — public guidance.
- `examples/component-showcase/`, `examples/static-showcase/`, browser fixtures
  — realistic rendered states.
- `tests/test_components.py`, `tests/test_template_css_contract.py`,
  `tests/test_transition_tokens.py`, `tests/test_css_syntax.py`,
  `tests/test_chirpui_css_concat.py`, `tests/test_strict_undefined.py`,
  `tests/test_alpine.py`, `tests/browser/*` — proof.

## Advocate

- **Composition before parameters.** Prefer primitives, slots, and parent-owned
  relationships over new macro switches.
- **Browser proof for browser risks.** Focus, dialogs, overlays, responsive
  overflow, htmx swaps, and Alpine lifecycle need Playwright when unit tests
  cannot prove them.
- **Incremental CSS envelope migration.** Convert touched legacy partials one at
  a time; avoid broad migrations without a dedicated plan.
- **Named behavior over inline state.** Promote repeated behavior into
  `chirpui-alpine.js` when it has refs, storage, keyboard handling, lifecycle, or
  cross-component coordination.

## Own

**Code:** `src/chirp_ui/templates/chirpui/*.html`,
`src/chirp_ui/templates/css/partials/*.css`,
`src/chirp_ui/templates/chirpui.css`,
`src/chirp_ui/templates/chirpui-transitions.css`,
`src/chirp_ui/templates/chirpui-alpine.js`,
`src/chirp_ui/templates/chirpui.js`, `src/chirp_ui/templates/islands/*.js`,
`src/chirp_ui/templates/themes/*.css`.

**Tests:** `tests/test_components.py`, `tests/test_template_css_contract.py`,
`tests/test_transition_tokens.py`, `tests/test_css_syntax.py`,
`tests/test_chirpui_css_concat.py`, `tests/test_description_coverage.py`,
`tests/test_strict_undefined.py`, `tests/test_alpine.py`, `tests/js/*`,
`tests/browser/*`.

**Docs:** `docs/fundamentals/composition.md`,
`docs/fundamentals/primitives.md`, `docs/fundamentals/layout.md`,
`docs/fundamentals/ui-layers.md`, `docs/fundamentals/css-override-surface.md`,
`docs/fundamentals/transitions.md`, `docs/components/alpine-magics.md`,
`docs/components/htmx-patterns.md`, `docs/components/dnd-fragment-island.md`,
`docs/fundamentals/relationship-contracts.md`.

**Agent artifacts:** none owned; consult
`.claude/agents/accessibility-auditor.md`, `.claude/agents/lead-designer.md`,
and relevant DORI Chirp UI skills for UI-facing changes.

**CODEOWNERS:** none checked in.
