# Chirp UI Agent Constitution

## North Star

Chirp UI exists to prove that a Python UI library can stay introspectable, safe, and beautiful without becoming a utility-class string vocabulary. The component registry is the source of truth; macros, CSS, docs, tests, the manifest, themes, and examples are projections of that registry. See `docs/VISION.md`.

## Non-Negotiables

- No utility-class vocabulary. Use `stack()`, `cluster()`, `grid()`, `frame()`, and `block()` composition primitives instead of `p-4`/`flex`/`text-center` equivalents.
- Every shipped `chirpui-*` class is registry-cited, template-emitted only when intentional, and defined in the generated CSS.
- Cascade order is public API: `chirpui.reset, chirpui.token, chirpui.base, chirpui.component, chirpui.utility, app.overrides`.
- Edit CSS partials, not generated `src/chirp_ui/templates/chirpui.css`; run the CSS build and commit both when CSS changes.
- No `<script>` tags in component macros. Alpine behavior lives in `chirpui-alpine.js`; tiny inline `x-data` attributes are the exception.
- Escape by default. Use `html_attrs`/`attrs_map`; `Markup` and `| safe` require trusted or already-escaped input.
- Python 3.14+ and free-threading compatibility are table stakes. Avoid mutable global state and non-free-threading-ready dependencies.

## Architecture Boundaries

- `src/chirp_ui/components.py` owns component descriptors, variants, sizes, emitted classes, slots, runtime requirements, and registry metadata.
- `src/chirp_ui/manifest.py` and `src/chirp_ui/manifest.json` project the registry for agents, docs, and downstream tooling.
- `src/chirp_ui/templates/chirpui/` owns Kida macro output and public HTML/HTMX/Alpine contracts.
- `src/chirp_ui/templates/css/partials/` owns author CSS; `chirpui.css` is deterministic generated output.
- `src/chirp_ui/validation.py`, `filters.py`, `tokens.py`, `alpine.py`, `route_tabs.py`, `icons.py`, and public exports in `__init__.py` are Python API surface.
- `src/bengal_themes/` is the packaged default Bengal theme surface.
- `scripts/` owns deterministic build projections. Keep them pure-Python/stdlib unless there is a checked-in reason not to.

## Stakes

- App developers inherit broken HTML, inaccessible controls, or XSS if macros bypass escaping or drift from Kida/HTMX contracts.
- Downstream overrides silently fail if layer order or specificity discipline changes.
- Coding agents hallucinate APIs when descriptors, manifest, docs, examples, and CSS disagree.
- Theme consumers lose a stable default UX when token names, assets, or theme package metadata drift.
- Free-threaded consumers can see races that local GIL-backed testing hides.

## Stop And Ask

- Public API changes: imports from `chirp_ui.__init__`, macro signatures, descriptor fields, manifest schema, theme entry points, `static_path()`, `register_filters()`.
- New runtime or build dependencies, especially anything not clearly pure-Python/free-threading-ready.
- New component, variant, size, color vocabulary, macro parameter, provide/consume key, config surface, or extension pattern.
- Cascade layer order, `app.overrides`, generated-output build order, release pipeline, or docs-site output contract changes.
- Security/auth/escaping changes, `Markup`/`| safe` use on new inputs, raw attribute escape hatches.
- Test/code disagreement, unreproduced bugs, irreversible migrations, or "dead" code that may still be load-bearing.

## Anti-Patterns

- Adding utility classes or raw CSS values instead of tokens.
- Hand-editing generated `chirpui.css`, `manifest.json`, or generated docs sections.
- Template classes without CSS and descriptor `emits` coverage.
- Defensive `try: ... except Exception: pass` around validation; use warnings that tell consumers what to do.
- Speculative macro params or "future flexibility" without a consumer.
- Refactoring during a bug fix unless the refactor is the fix or the touched CSS partial needs opportunistic envelope conversion.
- Re-triaging sharp edges already documented in `CLAUDE.md`; treat that table as institutional memory.

## Steward System

Read this root file plus the closest scoped `AGENTS.md`. Root is the constitution and routing guide; scoped files are domain stewards. Scoped stewards own local invariants, refusal patterns, docs, tests, examples, fixtures, and checks. Cross-boundary work needs `Steward Notes` in the PR description naming the consulted stewards, the contract touched, and the remaining risk.

Steward files use this operating model:

- Point Of View: who or what the domain represents.
- Protect: invariants, contracts, quality bars, and failure modes.
- Advocate: features, fixes, and investments the domain should push for.
- Serve Peers: upstream/downstream domains that need clearer contracts, diagnostics, docs, tests, or ergonomics.
- Do Not: local anti-patterns.
- Own: tests, docs, examples, fixtures, and maintenance checks.

## When To Consult

- Proactively consult stewards for cross-boundary, public-facing, hard-to-reverse, performance-sensitive, concurrency-sensitive, security-sensitive, or contract-affecting work.
- Use the nearest steward for local work.
- Use multiple stewards when ownership lines cross.
- Parallelize steward consultation only when questions are independent.
- Keep final synthesis with the implementing agent.

## Ask Stewards

Trigger phrase: `ask stewards`.

For implementation work, consult affected scoped stewards before editing. For backlog, roadmap, or prioritization work, consult all scoped stewards and produce a rollup with raw steward signals, confidence, dependencies, risks, convergence, minority reports, ranked backlog, and not-now items.

## Extension Routing

- New component descriptor: `src/chirp_ui/components.py`.
- New Kida component macro: `src/chirp_ui/templates/chirpui/<name>.html`.
- New component CSS: `src/chirp_ui/templates/css/partials/<nnn>_<name>.css`, then regenerate `chirpui.css`.
- New Alpine controller: `src/chirp_ui/templates/chirpui-alpine.js` and `src/chirp_ui/alpine.py` metadata when required.
- New token: `src/chirp_ui/tokens.py`, token CSS partials, docs, and manifest projection.
- New Bengal theme asset/template: `src/bengal_themes/chirp_theme/`.
- New docs page: `docs/` for reference, `docs/plans/` for active plans, `site/content/` for published docs site content.

## Done Criteria

- `uv run poe ci` is green, or you state exactly which narrower checks ran and why full CI was not run.
- Registry/template/CSS/manifest/docs projections are rebuilt and committed when affected.
- `test_template_css_contract.py`, `test_transition_tokens.py`, `test_registry_emits_parity.py`, manifest checks, and provide/consume checks pass for affected surfaces.
- Macro changes update descriptors, doc-blocks, `COMPONENT-OPTIONS.md`, examples, tests, and changelog fragments where user-facing.
- Public API changes include migration notes/deprecation path.
- Performance, concurrency, and security-sensitive changes include explicit notes in the PR.

## Review Notes

- Keep PRs to one component or one concern unless a rename genuinely crosses files.
- Commit style follows existing history: `feat(...)`, `fix:`, `refactor:`, `docs:`; imperative subject, body explains motivation.
- Flag surprises in the PR: stale classes, orphaned providers, inconsistent variants/sizes, tests that look wrong, dead-looking macros, or browser verification gaps.
- Diff explains what; PR description explains why.
