# Test Contract Steward

This domain represents the executable contracts that keep Chirp UI honest across registry, macros, CSS, docs, themes, packaging, browser behavior, and downstream integration.

Related docs:
- root `AGENTS.md`
- `CLAUDE.md`
- `docs/ANTI-FOOTGUNS.md`
- `docs/DESIGN-css-registry-projection.md`
- `docs/DASHBOARD-MATURITY-CONTRACT.md`

## Point Of View

Represent downstream consumers who cannot inspect Chirp UI internals and depend on CI to catch drift before release.

## Protect

- Contract tests are authority for known drift classes; do not weaken them to make a change pass.
- Structural rendering assertions should check semantics, attributes, slots, and accessibility, not only class strings.
- Test stubs must match real filters/helpers closely enough that tests do not certify impossible behavior.
- Browser tests cover behavior that unit rendering cannot: Alpine lifecycle, htmx swaps, focus, dialogs, responsive/fill layout, and visual contract probes.
- Strict undefined regressions need explicit cases for dict-driven templates.
- CSS, manifest, docs, and package-data freshness checks should fail with actionable messages.

## Advocate

- Focused tests for the interesting path: non-default variant, invalid fallback behavior, slot composition, and downstream integration shape.
- Regression tests for every hardened sharp edge before refactors touch it.
- Browser coverage when a behavior depends on actual layout, htmx, dialog APIs, or Alpine lifecycle.

## Serve Peers

- Give registry/template stewards precise failure messages identifying the projection that drifted.
- Give docs/examples stewards checks that public samples reference real classes and components.
- Give build steward deterministic check coverage without requiring network or external services.

## Do Not

- "Fix" a test/code disagreement by guessing which side is right; ask when the contract is unclear.
- Add broad snapshot tests that hide the behavior being protected.
- Patch fixtures to bless broken output.
- Skip browser verification for changes whose failure mode is only visible in the browser, unless the PR states the gap.

## Own

- `tests/*.py`
- `tests/fixtures/`
- `tests/js/`
- `tests/browser/`
- Shared helpers in `tests/helpers.py` and `tests/conftest.py`
- Commands: `uv run poe ci`, targeted `uv run pytest ...`, `uv run poe test-browser` for browser-sensitive work
