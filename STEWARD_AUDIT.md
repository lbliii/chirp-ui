# Steward Audit

Status: bootstrap audit for the first AGENTS.md steward network.

This file records Phase 4 self-audit findings, their verification status, and
the action taken before this steward-network update was finalized.

## Summary

Completed audit agents returned findings for Core Registry, Template/CSS/Behavior,
Bengal Theme, Planning, Examples and Showcase, Test Contract, and Advisory Agent
Artifacts.

Docs, Published Site, Build Projection, and CI/Release audit agents were spawned
but did not return after repeated waits. Their scoped files were still checked
locally through grep, generated-output rebuilds, public-safe filtering, and
targeted tests.

No convergence rule escalation was triggered by two independent completed
stewards reporting the same P0 finding. Several P2/P3 findings were accepted and
fixed because they were low-risk evidence or generated-output drift.

## Findings

Steward: Core Registry and Python API
Area: Runtime requirement and manifest-source accuracy
Severity: P2
Invariant: Component runtime requirements and public API guidance must match the
registry, manifest builder, and public exports.
Evidence: Core audit reported descriptor-local runtime requirements, manifest
runtime derivation from macro metadata/literal attributes, `__all__` public
exports, escaping APIs, and stale provide/consume design-doc wording.
User Impact: Agents can misstate how Alpine/HTMX requirements, exports, or
provide/consume metadata are owned.
Required Fix: Tighten `src/chirp_ui/AGENTS.md` and update
`docs/DESIGN-manifest-signature-extraction.md`.
Required Proof: `rg -n 'list_provides|list_consumes|depends_on'
docs/DESIGN-manifest-signature-extraction.md src/chirp_ui/manifest.py`.
Collateral: `src/chirp_ui/AGENTS.md`,
`docs/DESIGN-manifest-signature-extraction.md`.
Confidence: High
Verification Status: machine-verified
Action: Applied.

Steward: Template, CSS, and Behavior
Area: Script, token, island, and Alpine proof precision
Severity: P2
Invariant: Template guidance must not overstate script bans, token coverage, or
Alpine drift tests.
Evidence: Template audit cited app shell script tests, transition-token tests,
island JS files/tests, and `check_alpine_runtime()` limits.
User Impact: Agents could reject valid shell scripts or assume tests prove drift
shapes they do not prove.
Required Fix: Narrow script guidance to component macros, clarify motion-token
scope, add island JS ownership, and describe Alpine checks precisely.
Required Proof: `tests/test_app_shell_contract.py`, `tests/test_alpine.py`,
`tests/js/`, `src/chirp_ui/templates/islands/`.
Collateral: `AGENTS.md`, `src/chirp_ui/templates/AGENTS.md`.
Confidence: High
Verification Status: machine-verified
Action: Applied.

Steward: Bengal Theme
Area: Theme package contract
Severity: P2
Invariant: The theme steward must match installed package metadata, retained
asset entrypoints, and current parity docs.
Evidence: Bengal audit reported nonexistent `tests/test_pattern_assets.py`,
missing standalone `theme.toml` invariants, missing CSS entrypoint invariants,
and stale retained-surface docs.
User Impact: Agents can audit the theme against nonexistent tests or understate
the retained Bengal output surface.
Required Fix: Replace nonexistent test references, add `theme.toml` and
`assets/css/style.css` invariants, and align theme docs with the parity matrix.
Required Proof: `docs/CHIRP-THEME-PARITY-MATRIX.md`,
`src/bengal_themes/chirp_theme/theme.toml`,
`src/bengal_themes/chirp_theme/assets/css/style.css`.
Collateral: `src/bengal_themes/AGENTS.md`, `docs/CHIRP-THEME.md`,
`site/content/docs/theming/chirp-theme.md`.
Confidence: High
Verification Status: machine-verified
Action: Applied.

Steward: Planning
Area: Active and archived plan drift
Severity: P2
Invariant: Active plans must not carry stale counts or shipped-problem
statements; archived plans must not read like live backlog.
Evidence: Planning audit cited stale manifest counts in
`docs/plans/PLAN-pre-1.0-productization-saga.md`, stale CSS-layer/emits claims
in `docs/plans/PLAN-css-scope-and-layer.md`, missing Steward Notes, archived
ASCII `Next Slice` language, and a wrong roadmap citation in
`docs/plans/AGENTS.md`.
User Impact: Agents can reopen solved work or route future work through old
proof trails.
Required Fix: Remove static manifest counts, rewrite the CSS plan around
residual scope work, add Steward Notes, historicalize archived ASCII language,
and fix the citation.
Required Proof: Manifest count check, `rg -n '## Steward Notes'
docs/plans/PLAN-css-scope-and-layer.md`, and grep for stale claims.
Collateral: `docs/plans/AGENTS.md`,
`docs/plans/PLAN-css-scope-and-layer.md`,
`docs/plans/PLAN-pre-1.0-productization-saga.md`,
`docs/plans/done/PLAN-ascii-maturity.md`.
Confidence: High
Verification Status: machine-verified
Action: Applied.

Steward: Examples and Showcase
Area: Generated showcase, source inventory, snippets, citations, public-safe data
Severity: P1/P2/P3
Invariant: Examples must stay generated, public-safe, and explicit about what is
copyable.
Evidence: Examples audit reported static showcase CSS drift after assembly,
partial source-inventory coverage for showcase templates, `attrs_unsafe` in a
general forms showcase, weak curated-snippet metadata, stale browser-proof
citation, and a real person name in examples/browser fixtures.
User Impact: Published showcase output can drift, agents can over-trust example
templates, and public examples can leak person names.
Required Fix: Reassemble showcase output, add wildcard inventory policy, improve
curated snippet metadata, retarget browser citation, replace the name, and keep
the deeper `attrs_unsafe` ratchet as follow-up.
Required Proof: `bash scripts/assemble-static-showcase.sh site/public/showcase`,
public-safe grep, and source-inventory grep.
Collateral: `examples/AGENTS.md`, `docs/AGENT-SOURCE-INVENTORY.md`,
`docs/AGENT-CURATED-SNIPPETS.md`, `site/public/showcase/css/chirpui.css`,
example/browser fixture templates.
Confidence: High
Verification Status: machine-verified, except the person-name intent was
manual-confirmation-needed before replacement.
Action: Applied generated-output, inventory, metadata, citation, and public-safe
fixes. Deferred a dedicated `attrs_unsafe` example-template ratchet.

Steward: Test Contract
Area: Packaging claims, moved-plan references, CSS design-doc paths, private
memory references, citation precision
Severity: P2/P3
Invariant: Test steward guidance and cited docs must match what tests and source
actually prove.
Evidence: Test audit reported overbroad installed-package proof wording, stale
moved top-level plan references, obsolete CSS path diagrams, private memory-path
references, and imprecise citations in `tests/AGENTS.md`.
User Impact: Reviewers can follow dead proof trails or think CI proves wheel
install smoke that it does not prove.
Required Fix: Scope packaging proof to in-tree package-data checks, update moved
plan references, update CSS design-doc path model, remove private memory
references, and retarget citations.
Required Proof: grep for moved top-level plan references, private memory-path
references, and private person names across source, tests, docs, scripts, and
agent files.
Collateral: `tests/AGENTS.md`, source/test comments, CSS partial comments,
generated CSS, `docs/DESIGN-css-registry-projection.md`, plan docs.
Confidence: High
Verification Status: machine-verified
Action: Applied.

Steward: Advisory Agent Artifacts
Area: Persona output format, utility checks, missing audit file, citation
precision
Severity: P2/P3
Invariant: Advisory personas must use the root Steward Signal Format and scoped
utility checks must include markdown/public-safe proof.
Evidence: Advisory audit reported bullet-prefixed output fields,
missing markdown/public-safe utility checks, references to missing
`STEWARD_AUDIT.md`, and stale `.claude/AGENTS.md` citations.
User Impact: Steward swarm output can drift from the parser/readback contract,
and advisory files can point at missing bootstrap artifacts.
Required Fix: Remove bullet prefixes from persona output examples, add utility
checks, create `STEWARD_AUDIT.md`, and retarget citations.
Required Proof: `rg -n '^Steward:|^- Steward:' AGENTS.md .claude/agents/*.md`
and `rg --files | rg '^STEWARD_(AUDIT|QUESTIONS)\\.md$'`.
Collateral: `.claude/AGENTS.md`, `.claude/agents/*.md`, `STEWARD_AUDIT.md`.
Confidence: High
Verification Status: machine-verified
Action: Applied.

Steward: Documentation
Area: Audit completion
Severity: P3
Invariant: Scoped steward self-audits should return findings before finalizing.
Evidence: Documentation audit agent was spawned and waited on repeatedly but did
not return before final local verification.
User Impact: Documentation steward did not provide an independent completed
finding set for this bootstrap.
Required Fix: Treat this as residual risk for first reviewer; rerun `ask
stewards` on documentation if the docs steward file changes again.
Required Proof: Local checks over docs-facing files and targeted docs tests.
Collateral: None.
Confidence: Medium
Verification Status: manual-confirmation-needed
Action: Local verification substituted for subagent result.

Steward: Published Site
Area: Audit completion
Severity: P3
Invariant: Scoped steward self-audits should return findings before finalizing.
Evidence: Published Site audit agent was spawned and waited on repeatedly but did
not return before final local verification.
User Impact: Site steward did not provide an independent completed finding set
for this bootstrap.
Required Fix: Treat this as residual risk for first reviewer; rerun `ask
stewards` on site if published docs/source-map behavior changes again.
Required Proof: Local checks over `site/`, generated showcase assembly, and
targeted docs/site tests.
Collateral: None.
Confidence: Medium
Verification Status: manual-confirmation-needed
Action: Local verification substituted for subagent result.

Steward: Build Projection
Area: Audit completion
Severity: P3
Invariant: Scoped steward self-audits should return findings before finalizing.
Evidence: Build Projection audit agent was spawned and waited on repeatedly but
did not return before final local verification.
User Impact: Build steward did not provide an independent completed finding set
for this bootstrap.
Required Fix: Treat this as residual risk for first reviewer; rerun build
projection audit if generated-output scripts change again.
Required Proof: `uv run poe build-css`, generated CSS diff review, and generated
freshness tests.
Collateral: None.
Confidence: Medium
Verification Status: manual-confirmation-needed
Action: Local verification substituted for subagent result.

Steward: CI and Release
Area: Audit completion
Severity: P3
Invariant: Scoped steward self-audits should return findings before finalizing.
Evidence: CI/Release audit agent was spawned and waited on repeatedly but did
not return before final local verification.
User Impact: CI steward did not provide an independent completed finding set for
this bootstrap.
Required Fix: Treat this as residual risk for first reviewer; rerun CI/release
audit if workflows, release gates, or package-smoke work changes again.
Required Proof: `.github/workflows/`, `pyproject.toml` Poe tasks, and targeted
verification commands.
Collateral: None.
Confidence: Medium
Verification Status: manual-confirmation-needed
Action: Local verification substituted for subagent result.

## Deferred Follow-Up

- Add a focused ratchet for `attrs_unsafe` in candidate/general example
  templates or move the drag-and-drop behavior to a supported runtime pattern.
- Decide whether CI should gain a true wheel/sdist install smoke. This bootstrap
  narrowed test-steward wording instead of adding a new release gate.
- Add a source-inventory ratchet proving every showcase template is covered by
  wildcard policy, explicit listing, or exclusion.
- Add rendered proof for curated snippets if they grow beyond the current small
  docs-derived example.
