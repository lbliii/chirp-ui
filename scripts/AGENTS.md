# Build Projection Steward

This domain represents deterministic build scripts that project registry, template, CSS, docs, and site state into committed artifacts.

Related docs:
- root `AGENTS.md`
- `docs/DESIGN-css-registry-projection.md`
- `docs/DESIGN-manifest-signature-extraction.md`
- `docs/plans/PLAN-css-scope-and-layer.md`
- `pyproject.toml`

## Point Of View

Represent CI, release prep, and contributors who need stale generated output to fail loudly and reproducibly.

## Protect

- Build scripts stay deterministic and produce byte-identical output for the same inputs.
- CSS and manifest builders keep `--check` modes with actionable failure messages.
- Scripts should remain pure-Python and stdlib-only unless a human approves a dependency.
- Build order and layer declarations are public contracts when they affect shipped output.
- Generated files should clearly say they are generated and name the source/build command.

## Contract Checklist

- Builder changes: inspect normal and `--check` modes, deterministic ordering, generated header text, failure messages, and stale-output tests.
- CSS builder changes: inspect partial ordering, layer declarations, generated `chirpui.css`, CSS concat/syntax tests, and release-preflight tasks.
- Manifest/docs builder changes: inspect AST/parser assumptions, schema output, generated `manifest.json`, generated `COMPONENT-OPTIONS.md` sections, site manifest task, and docs freshness tests.
- Site/showcase assembly changes: inspect `docs-build-all`, `site/public` generation expectations, Make/Poe task wiring, and docs-site tests.
- Task changes in `pyproject.toml`: inspect CI/check/release task order, README command docs, Makefile parity, and changelog/release notes when behavior changes.

## Advocate

- More projection checks that catch drift before release.
- Better failure messages that name the file to edit and the command to run.
- Shared parsing helpers only when they reduce real duplicated build logic.

## Serve Peers

- Give registry/template/docs stewards reliable regenerate and check commands.
- Give tests steward in-memory builders for deterministic assertions.
- Give release reviewers a small set of build artifacts to inspect.

## Do Not

- Shell out to heavyweight toolchains for work Python can do deterministically.
- Hide stale-output failures behind best-effort warnings.
- Mutate unrelated files during a builder run.
- Change the CSS partial manifest order casually.

## Own

- `scripts/build_chirpui_css.py`
- `scripts/build_manifest.py`
- `scripts/build_component_options.py`
- `scripts/docs_site.py`
- `scripts/extract_tokens.py`
- `scripts/assemble-static-showcase.sh`
- Poe tasks in `pyproject.toml` that call these scripts
- Tests: `tests/test_chirpui_css_concat.py`, `tests/test_manifest.py`, `tests/test_docs_site.py`
