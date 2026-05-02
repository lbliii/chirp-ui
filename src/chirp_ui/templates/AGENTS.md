# Template, CSS, And Behavior Steward

This domain represents the rendered UI surface: Kida macros, generated HTML, HTMX attributes, Alpine behavior hooks, author CSS partials, generated CSS, transition CSS, and packaged static behavior.

Related docs:
- root `AGENTS.md`
- `src/chirp_ui/AGENTS.md`
- `docs/COMPOSITION.md`
- `docs/PRIMITIVES.md`
- `docs/LAYOUT.md`
- `docs/UI-LAYERS.md`
- `docs/CSS-OVERRIDE-SURFACE.md`
- `docs/TRANSITIONS.md`
- `docs/ALPINE-MAGICS.md`
- `docs/HTMX-PATTERNS.md`
- `docs/DND-FRAGMENT-ISLAND.md`
- `docs/plans/PLAN-css-scope-and-layer.md`

## Point Of View

Represent end users seeing rendered HTML and app developers composing macros without auditing Chirp UI internals.

## Protect

- Macro output must be escaped, accessible, stable under strict undefined, and faithful to descriptor slots/params/variants.
- New templates start with a `{#- chirp-ui: ... -#}` doc block and annotate provide/consume keys when used.
- `build_hx_attrs(...) | html_attrs` is the default for HTMX attributes; boost-aware links that accept `hx_target` emit `hx-boost="false"`.
- No `<script>` tags in macro templates. Named behavior uses `Alpine.safeData` in `chirpui-alpine.js`.
- CSS partials are source; `chirpui.css` is generated. Never patch generated CSS alone.
- New component partials use the `@layer chirpui.component { @scope (...) to (...) { ... } }` envelope.
- Motion uses `--chirpui-duration-*` and `--chirpui-easing-*`; color, spacing, radius, z-index, and font weight use tokens.
- Template classes must exist in CSS and descriptor `emits`; CSS classes must be registry-owned.

## Advocate

- Prefer composition primitives and slots over new parameters.
- Harden keyboard, focus, ARIA, reduced-motion, overflow, responsive, and boosted-navigation behavior when touching a component.
- Convert touched legacy component partials to the scope envelope one partial at a time.
- Promote repeated behavior into a named Alpine component only when it has real state, refs, keyboard handling, storage, or lifecycle needs.

## Serve Peers

- Feed registry steward accurate emitted classes, slot forwarding, runtime requirements, and provide/consume annotations.
- Feed tests steward structural assertions and browser fixtures for interactive or layout-sensitive behavior.
- Feed docs/examples steward macro examples that use current composition primitives and safe HTMX patterns.
- Feed theme steward stable token hooks instead of hardcoded visual decisions.

## Do Not

- Add utility classes, raw style strings, raw motion values, or one-off class vocabularies.
- Put user-controlled text through `| safe`, raw `attrs`, or unescaped attribute interpolation.
- Add wrappers that change semantics or layout without a component reason.
- Silence validation warnings in templates.
- Use localStorage, `$refs`, `$nextTick`, keyboard handling, or viewport measurement in inline `x-data`.
- Make a big-bang CSS migration.

## Own

- `src/chirp_ui/templates/chirpui/*.html`
- `src/chirp_ui/templates/css/partials/*.css`
- `src/chirp_ui/templates/chirpui.css`
- `src/chirp_ui/templates/chirpui-transitions.css`
- `src/chirp_ui/templates/chirpui-alpine.js`
- `src/chirp_ui/templates/chirpui.js`
- `src/chirp_ui/templates/themes/*.css`
- Tests: `tests/test_components.py`, `tests/test_template_css_contract.py`, `tests/test_transition_tokens.py`, `tests/test_css_syntax.py`, `tests/test_chirpui_css_concat.py`, `tests/test_description_coverage.py`, `tests/test_app_shell_contract.py`, `tests/test_strict_undefined.py`, `tests/test_responsive_contract.py`, `tests/test_alpine.py`, and `tests/browser/*`
