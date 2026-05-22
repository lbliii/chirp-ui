# Verification

Status: active practice
Date: 2026-05-12

Use the locked `uv run` environment for Chirp UI verification. The generated
artifacts depend on the repo's pinned `kida-templates` API and registered Chirp
UI filters, so running the same Python module from a system interpreter can
import a different installed Kida package and fail in ways that do not represent
the checkout.

## Generated Artifacts

Run this before committing registry, CSS, or docs changes:

```text
uv run poe verify-generated
```

That task is the short path for:

- `uv run poe build-css-check`
- `uv run poe build-manifest-check`
- `uv run poe build-docs-check`

It verifies these committed generated files are fresh:

- `src/chirp_ui/templates/chirpui.css`
- `src/chirp_ui/manifest.json`
- `docs/COMPONENT-OPTIONS.md`

Hosted CI runs this check through `uv run poe ci`. If the GitHub check fails
here, regenerate the owned output locally and commit the generated file rather
than editing generated output by hand.

## JavaScript Island Helpers

The JavaScript island helper suite is part of the full CI gate:

```text
npm ci
uv run poe test-js
```

`uv run poe ci` also runs `test-js`, so local full-CI runs need the npm
dependencies installed first. These tests cover browser-adjacent state helpers
that Python render tests cannot exercise.

If one is stale, regenerate the exact artifact:

```text
uv run poe build-css
uv run poe build-manifest
uv run poe build-docs
```

## Gate Policy

`uv run poe ci` is the trusted default gate for normal PRs. It runs lint,
format, generated-artifact freshness, focused CSS/template checks, type checks,
the full non-browser pytest suite, and Vitest island-helper tests.

Coverage and browser proof are explicit gates, not hidden defaults:

```text
uv run poe test-cov
uv run poe ci-browser
uv run poe test-browser-chrome
```

`test-cov` enforces the configured coverage floor (`fail_under = 80`) when a PR
claims coverage movement or before a release hardening sweep. `ci-browser` is
required for changes whose failure mode depends on Playwright, actual layout,
dialog APIs, htmx lifecycle, or Alpine lifecycle. Browser tests stay outside
`poe ci` because they require the browser dependency group and installed browser
binaries.

For application chrome slices, use `uv run poe test-browser-chrome` as the
focused proof loop. It builds the published docs output first, then runs the
rail-to-drawer recipe and multi-family chrome gauntlet plus Bengal docs chrome
without executing every browser fixture in the suite.

## Proof Routing

Choose the narrowest proof that can observe the contract being changed, then run
`uv run poe ci` before broad merges or release-facing work.

| Change surface | Required proof |
|---|---|
| Registry, manifest schema, generated CSS, generated component docs | `uv run poe verify-generated` plus affected manifest or generated-doc tests |
| Kida macros, escaping, structured attrs, HTMX attributes | Targeted pytest render tests plus strict-undefined or template/CSS contract tests |
| Alpine controllers, JavaScript island helpers, runtime state helpers | `uv run poe test-js` plus focused Python metadata tests when applicable |
| Token, CSS partial, cascade layer, or scope behavior | CSS syntax/concat tests, template/CSS contract tests, and browser proof when computed layout or cascade interaction is the failure mode |
| Dialog, focus, overflow, htmx lifecycle, Alpine lifecycle, responsive layout | `uv run poe ci-browser` or the targeted browser test that exercises the changed behavior |
| Application chrome rail/tray, command focus, route-tab scroll, badge stability, and multi-family recipes | `uv run poe test-browser-chrome` |
| Search shells, facet rails, scoped counts, and responsive command surfaces | Targeted render tests for fallback and HTMX contracts plus browser proof at 320px, 390px, 768px, 1024px, and desktop width for no overflow and visible primary controls |
| Docs, examples, scaffold, or published site content | Relevant docs/site tests, `uv run poe docs-build-all` when published output changes, and examples proof when snippets are executable |
| Theme packages, Bengal templates, packaged assets | Bengal package tests plus generated/site proof when templates or emitted assets change |

## Release Preflight

Use the Make target when preparing a package build or release:

```text
make release-preflight
```

It regenerates CSS, manifest, and component reference docs, then fails if those
generated files changed and still need to be committed.

## Kida Mismatch Failure

Symptom:

```text
python -m chirp_ui.manifest --json
```

fails locally with a Kida import, parser, or analysis API error even though the
checkout should be valid.

Preferred command:

```text
uv run python -m chirp_ui.manifest --json
```

Reason: plain `python` may import a globally installed `kida` or
`kida-templates` version. `uv run` uses the locked project environment and keeps
manifest generation aligned with CI.

## Focused Proof Set

For pre-1.0 design-system work, the usual focused proof set is:

```text
uv run poe verify-generated
uv run pytest tests/test_manifest.py tests/test_chirpui_css_concat.py tests/test_visual_audit_showcase.py -q
uv run --group browser pytest tests/browser/test_visual_audit_showcase.py -q --timeout=30 --override-ini=addopts=
```

Run the full gate before release or broad refactors:

```text
npm ci
uv run poe ci
```
