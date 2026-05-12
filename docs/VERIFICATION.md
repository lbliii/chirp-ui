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
