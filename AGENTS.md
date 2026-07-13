# Chirp UI Agent Constitution

## North Star

We prove that a Python UI library can stay introspectable, safe, and beautiful
without becoming a utility-class string vocabulary. The component registry is
the source of truth; macros, CSS, docs, tests, the manifest, themes, examples,
and generated site artifacts are projections of that registry.

We optimize for Python-native contracts that app developers, tests, type
checkers, and coding agents can inspect. Public guidance is in `README.md` and
`docs/VISION.md`; implementation work must keep those claims true.

## Non-Negotiables

- No utility-class vocabulary. Use `stack()`, `cluster()`, `grid()`, `frame()`,
  and `block()` composition primitives instead of `p-4`/`flex`/`text-center`
  equivalents. Evidence: `docs/VISION.md:77`, `docs/PRIMITIVES.md:1`.
- The registry owns shipped component vocabulary. Evidence:
  `src/chirp_ui/components.py:1`, `README.md:101`.
- Every shipped `chirpui-*` class is registry-cited, template-emitted only when
  intentional, and defined in generated CSS. Evidence: `README.md:154`,
  `src/chirp_ui/components.py:210`.
- Cascade order is public API: `chirpui.reset, chirpui.token, chirpui.base,
  chirpui.component, chirpui.utility, app.overrides`. Evidence:
  `src/chirp_ui/templates/chirpui.css:11`, `README.md:158`.
- Edit CSS partials, not generated `src/chirp_ui/templates/chirpui.css`; run the
  CSS build and commit both when CSS changes. Evidence: `CLAUDE.md:92`,
  `scripts/build_chirpui_css.py:10`.
- Generated outputs are never hand-edited when a builder owns them:
  `manifest.json`, `chirpui.css`, generated `COMPONENT-OPTIONS.md` sections,
  and published site artifacts must come from their scripts. Evidence:
  `Makefile:80`, `docs/COMPONENT-OPTIONS.md:3677`.
- No arbitrary `<script>` tags in component macros. Alpine behavior lives in
  `chirpui-alpine.js`; small inline `x-data` attributes are the exception.
  Layout-level pre-paint/runtime scripts are allowed only in documented shell
  layout templates with focused tests. Evidence: `README.md:214`,
  `tests/test_app_shell_contract.py:47`.
- Escape by default. Use `html_attrs`/`attrs_map`; `Markup`, `| safe`, raw
  attribute strings, and `attrs_unsafe` require a named trust boundary.
  Evidence: `CLAUDE.md:83`, `tests/test_filters.py:424`.
- Python 3.14+ and free-threading compatibility are table stakes. Avoid mutable
  global state and non-free-threading-ready dependencies. Evidence:
  `pyproject.toml:10`, `src/chirp_ui/__init__.py:43`.
- Layout affinity and relationship ownership are HTML/CSS prototype contracts,
  not manifest schema, until a schema-bump plan lands. Evidence:
  `docs/LAYOUT-AFFINITY-RESOLVER-AUTHORING.md:8`,
  `docs/RELATIONSHIP-CONTRACTS.md:55`.

## Architecture Boundaries

| Path | Steward / Contract |
| --- | --- |
| `src/chirp_ui/` | Core registry, Python API, and manifest contracts. |
| `src/chirp_ui/templates/` | Kida macros, CSS, Alpine, and HTMX. |
| `src/bengal_themes/` | Installable `chirp-theme` package. Scoped steward: `src/bengal_themes/AGENTS.md`. |
| `docs/` | Durable docs, generated references, and source maps. |
| `docs/plans/` | Active plans, archives, roadmap, and not-now boundaries. |
| `site/` | Bengal site source and generated-site expectations. |
| `examples/` | Runnable demos, static showcase, and copyable patterns. |
| `tests/` | Executable parity, regression, browser, and fixture contracts. |
| `scripts/` | Deterministic builders and generated-output checks. |
| `.github/` | Hosted checks, Pages, changelog, and PyPI release. |
| `.claude/` | Advisory personas and review routing. |

## Governance Alignment

- No checked-in `CODEOWNERS`, `OWNERS`, or `MAINTAINERS` file exists in this
  repository as of this bootstrap. If one is added later, it is the source of
  truth for human review; stewards advise, CODEOWNERS approve.
- Canonical product and architecture knowledge lives in `README.md`,
  `docs/VISION.md`, `docs/INDEX.md`, and focused contract docs under `docs/`.
- The root constitution owns cross-cutting concerns; scoped `AGENTS.md` files own
  local invariants. Cross-boundary PRs include `Steward Notes`.
- Advisory personas under `.claude/agents/` do not own paths. They pressure-test
  cross-cutting concerns and route findings to scoped stewards.

## Stop And Ask

- Public API changes: imports from `chirp_ui.__init__`, macro signatures,
  descriptor fields, manifest schema, library contract, theme entry points,
  `static_path()`, `register_filters()`, `list_theme_packs()`.
- New runtime or build dependencies, especially anything not clearly
  pure-Python/free-threading-ready or not already represented in
  `pyproject.toml` dependency groups.
- New component, variant, size, appearance, tone, color vocabulary, macro
  parameter, provide/consume key, config surface, extension protocol, or
  theme-pack name.
- Data model, manifest schema, generated-output build order, release pipeline,
  docs-site output contract, or cascade layer order changes.
- Security/auth/escaping changes, `Markup`/`| safe` use on new inputs, raw
  attribute escape hatches, or unsafe HTML examples.
- Concurrency or lifecycle changes in Alpine registration, module caches,
  validation registries, static asset loading, or shared test fixtures.
- Layout-affinity promotion to descriptors or `chirpui-manifest@6`.
- Test/code disagreement, unreproduced bugs, irreversible migrations,
  destructive operations, or "dead" code that may still be load-bearing.

## Anti-Patterns

- Adding utility classes or raw CSS values instead of composition primitives and
  tokens.
- Hand-editing generated `chirpui.css`, `manifest.json`, generated docs
  sections, or site public artifacts.
- Template classes without CSS and descriptor `emits` coverage.
- Defensive `try: ... except Exception: pass` around validation; use warnings
  that tell consumers what to do.
- Speculative macro params, descriptor fields, manifest keys, or "future
  flexibility" without a real consumer.
- Refactoring during a bug fix unless the refactor is the fix or the touched CSS
  partial needs opportunistic envelope conversion.
- Re-triaging sharp edges already documented in `CLAUDE.md`; treat that table as
  institutional memory.
- Turning layout-affinity `data-chirpui-*` attributes into global utility
  selectors.

## Steward System

Read this root file plus the closest scoped `AGENTS.md`. Root is the
constitution, governance map, cross-cutting contract, and swarm protocol.
Scoped files are domain stewards with concrete local interests.

Every steward uses this operating model:

- Point Of View: who or what the domain represents.
- Protect: invariants, contracts, quality bars, and failure modes.
- Contract Checklist: concrete surfaces to inspect when this domain changes.
- Advocate: domain investments the steward should push for.
- Own: code, tests, docs, agent artifacts, and CODEOWNERS status.
- Do Not and Serve Peers appear only when they add non-obvious local guidance.

Cross-boundary work needs `Steward Notes` in the PR description naming consulted
stewards, the contract touched, accepted and deferred findings, proof run,
collateral updated, and remaining risk.

### Contract Checklist

- Identify every surface that should agree: CLI/API, programmatic use, protocol,
  schema/types, UI, docs, examples, scaffold/templates, tests, benchmarks,
  changelog, generated artifacts, and published site.
- Every accepted finding must name required proof and collateral updates, or
  explicitly say `no collateral: <reason>`.
- Docs/examples/scaffold move in the same PR as user-facing behavior unless
  synthesis records why they are unaffected.
- Contract-affecting PRs include a parity matrix when behavior spans multiple
  entrypoints.

### Steward Signal Format

Steward findings should be contract-oriented, evidence-backed, and
collateral-aware:

```text
Steward:
Area:
Severity: P0/P1/P2/P3
Invariant:
Evidence: <source-file:line> [-> <doc-file:line> for content audit]
User Impact:
Required Fix:
Required Proof:
Collateral:
Confidence:
Verification Status: machine-verified / manual-confirmation-needed / not-machine-verifiable
```

### Convergence Rule

Two or more independent stewards flagging the same accepted finding promotes it
to P0 for synthesis until the implementing agent proves the concerns are not the
same defect.

### Steward Swarms

Trigger phrases: `ask stewards`, `bugbash`, `review swarm`, and `steward
synthesis`.

For implementation review, consult affected scoped stewards and relevant
advisory agents. Return synthesis before or during the change. Include
accepted/deferred findings, merged duplicates, minority reports, required proof,
collateral updates, and not-now items.

For backlog, roadmap, or prioritization work, consult all scoped stewards and
produce raw steward signals, confidence, dependencies, risks, convergence,
minority reports, ranked backlog, and not-now items.

For content audit triggers such as `audit docs`, `content audit`, and `accuracy
pass`, verify every factual P0/P1 against source before recommending text
changes.

### Global Sweep On Accepted P0s

When a P0 is accepted, grep the full code/docs/site/examples tree for the same
wrong claim or pattern before closing it. Record the grep command, matching
scope, fixes made, and any explicit no-impact exclusions.

## Security And Escaping

This concern activates for templates, filters, docs snippets, examples,
Markdown/rendered content, HTMX attributes, Alpine data, and site/theme HTML.

- Prefer mapping APIs (`attrs_map`, `html_attrs`, `build_hx_attrs`) over raw
  attribute strings.
- `Markup`, `| safe`, `attrs_unsafe`, and raw HTML examples require a trust
  boundary and tests or docs explaining why the input is already safe.
- Public examples must not teach unsafe raw attributes unless the example is an
  explicit escape-hatch guide.
- Required evidence: render tests for escaping, audit output from
  `scripts/escape_audit.py` when relevant, and docs updates for trust-boundary
  changes.

## Accessibility

This concern activates for component markup, Alpine/HTMX behavior, browser
fixtures, examples, docs, site chrome, and theme controls.

- Prefer native HTML semantics before custom ARIA.
- Interactive controls need stable names, roles, states, keyboard operation,
  focus visibility, and no color-only state.
- Motion respects reduced-motion preferences and transition tokens.
- Browser proof is required when focus, dialogs, menus, overlays, responsive
  layout, or scroll locking are part of the behavior.

## Visual And Layout Quality

This concern activates for user-facing UI, theme tokens, examples, docs site
chrome, browser fixtures, and pattern recipes.

- Compose with named primitives and component slots before local CSS.
- Parent components own relationships between direct children: inset, rhythm,
  attachment, grouping, pressure, and local overflow.
- Layout-sensitive changes need browser or screenshot proof at phone, tablet,
  and desktop widths when unit render tests cannot prove the failure mode.
- New visual vocabulary goes through descriptors, tokens, docs, examples, tests,
  and generated projections.

## Agent Grounding

This concern activates for registry metadata, manifests, generated component
docs, source maps, snippets, examples, site outputs, and advisory agent files.

- Agents cite the manifest and durable docs instead of guessing macros, params,
  slots, classes, variants, sizes, or runtime requirements.
- Copyable snippets follow `docs/AGENT-SOURCE-INVENTORY.md`; candidate examples
  need explicit curation before becoming copyable guidance.
- Generated site artifacts remain Bengal-owned unless
  `docs/AGENT-SOURCE-MAP.md` names a Chirp UI-owned artifact.
- Required evidence: manifest/build-docs freshness checks, source-map parity
  tests, and grep-verifiable provenance for new agent guidance.

## Release Readiness

This concern activates before PRs, releases, generated-output updates, public
docs changes, or CI/workflow edits.

- Prefer `uv run poe ci`; when narrower checks run, state exactly which checks
  ran and why full CI did not.
- `poe ci` includes the blocking three-contract Playwright smoke. Local full-CI
  setup therefore needs `uv sync --group dev --group browser` and
  `uv run playwright install chromium`; broader browser proof remains in
  `poe ci-browser` and `poe test-browser-chrome`.
- **Template verification:** `uv run poe template-check` runs strict Kida
  verification over `src/chirp_ui/templates/chirpui` with production filter/global
  stubs (`scripts/template_check.py`). It is wired into `poe ci` and `poe check`
  after lint/format and before CSS checks. For local iteration on a single
  template directory, `kida check <dir> --strict` is the underlying engine — see
  [Kida `kida check` CLI docs](https://lbliii.github.io/kida/docs/reference/cli/#kida-check).
  Use `poe ci` (or at minimum `poe check` + `poe test`) before opening a PR;
  `template-check` alone is not sufficient.
- Generated projections must be rebuilt and committed when affected.
- Public behavior needs changelog fragments, migration notes, docs/examples, and
  steward notes when contracts change.
- Release workflows use GitHub release and trusted publishing surfaces; local
  publish shortcuts are not the default release story.

## Free-Threading And Concurrency

This concern activates for module globals, caches, validation state, static asset
loading, Alpine registration metadata, build scripts, tests, and dependencies.

- Python code targets 3.14 and `PYTHON_GIL=0` hosted checks.
- Use immutable dataclasses, tuples, mappings, `ContextVar`, and pure builders
  where shared state is needed.
- New dependencies need a free-threading readiness note.
- Avoid mutable module state unless tests prove safe reset and concurrent reads.

## Known Regression Patterns

- **Fabricated CLI / config fields.** Verification: every flag traces to
  `argparse`, task config, schema, or docs command. Grep source before filing.
- **Unverified finding regression.** Verification: every factual P0/P1 carries
  `machine-verified`, `manual-confirmation-needed`, or `not-machine-verifiable`.
- **Narrow-fix regression.** Verification: every accepted P0 closure runs the
  Global Sweep above.
- **Generated-output drift.** Shape: registry, CSS, manifest, or generated docs
  changed without the generated projection. Verification: `uv run poe
  verify-generated`; evidence in `pyproject.toml:217` and `Makefile:80`.
- **Strict-undefined optional-key regression.** Shape: dict/list templates use
  `item.key` guards that raise under Kida strict undefined. Verification:
  `tests/test_strict_undefined.py`; use `.get()` guards and `default("")`.
- **Unsafe attribute regression.** Shape: raw attr strings, `| safe`, or
  `attrs_unsafe` spread into public examples. Verification:
  `tests/test_filters.py`, `tests/test_kida_analysis_contracts.py`, and
  `scripts/escape_audit.py`.
- **Template/CSS/registry drift.** Shape: template emits a class that CSS or
  descriptors do not own. Verification: `tests/test_template_css_contract.py`
  and `tests/test_registry_emits_parity.py`.
- **Motion-token regression.** Shape: raw animation durations/easings in CSS.
  Verification: `tests/test_transition_tokens.py`.
- **Layout overflow regression.** Shape: long text, tables, actions, rails, or
  overlays widen the document. Verification: focused browser tests and
  `assert_no_document_horizontal_overflow` fixtures.
- **Plan-location drift.** Shape: `docs/INDEX.md` or tests point to
  `docs/plans/done/` while files remain active, or vice versa. Verification:
  planning ratchet tests and link/path grep; this appeared in PR #110 review
  comments.
- **Legacy helper growth.** Shape: new examples teach utility-like typography,
  spacing, or containment helpers as preferred authoring. Verification:
  `docs/PRIMITIVES.md`, `docs/PUBLIC-SURFACE-STABILIZATION.md`, and legacy
  helper tests.
- **Layout-affinity schema leak.** Shape: prototype `data-chirpui-*` resolver
  vocabulary appears as descriptor fields or manifest keys before a schema bump.
  Verification: `tests/docs_contracts/test_layout_affinity_docs.py`,
  `tests/docs_contracts/test_relationship_contract_docs.py`, and manifest tests.

## Done Criteria

- `uv run poe ci` is green, or the final response states exactly which narrower
  checks ran and why full CI was not run.
- Registry/template/CSS/manifest/docs projections are rebuilt and committed when
  affected.
- Affected generated checks pass, especially `test_template_css_contract.py`,
  `test_transition_tokens.py`, `test_registry_emits_parity.py`, manifest checks,
  and provide/consume checks.
- Macro changes update descriptors, doc-blocks, generated component options,
  examples, tests, and changelog fragments where user-facing.
- Public API changes include migration notes or a deprecation path.
- Performance, concurrency, security, accessibility, and browser-sensitive
  changes include explicit proof notes.
- Every accepted steward finding has test/docs/example/benchmark proof or an
  explicit no-impact note.
- Public-safe filter has run for new steward docs: no customer names, internal
  person names, private numbers, internal direction quotes, or private
  infrastructure names.

## Review Notes

- Keep PRs to one component or one concern unless a rename genuinely crosses
  files.
- Commit style follows existing history: `feat(...)`, `fix:`, `refactor:`,
  `docs:`; imperative subject, body explains motivation.
- Flag surprises in the PR: stale classes, orphaned providers, inconsistent
  variants/sizes, tests that look wrong, dead-looking macros, unused public
  names, suppressions, benchmark gaps, free-threading assumptions, browser
  verification gaps, steward disagreement, and deferred/not-now findings.
- Diff explains what; PR description explains why.
