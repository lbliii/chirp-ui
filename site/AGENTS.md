# Published Site Steward

This domain represents the Bengal-backed documentation site and published artifacts, including release pages, search/index output, public showcase assembly, and agent-facing site artifacts.

Related docs:
- root `AGENTS.md`
- `docs/AGENTS.md`
- `docs/INDEX.md`
- `README.md`
- `pyproject.toml` docs tasks

## Point Of View

Represent readers and agents consuming the published site rather than the source tree.

## Protect

- Source content lives under `site/content/` and `docs/`; generated `site/public/` is not the authoring source.
- Site build config should not fork component contracts from the registry or docs.
- `site/public/chirpui.manifest.json` is emitted from `python -m chirp_ui.manifest --json`, not hand-written.
- Release pages should match changelog/release reality.
- Search, `llms.txt`, `agent.json`, and index artifacts must be generated from the site pipeline.

## Advocate

- Published docs that expose manifest, component options, examples, and release notes cleanly.
- Build checks that catch broken links, missing showcase output, and stale public artifacts.
- Keeping local and production environment config differences explicit and small.

## Serve Peers

- Give docs steward feedback when source docs do not publish well.
- Give examples steward a reliable path into `site/public/showcase/`.
- Give build steward clear docs-site commands and generated artifact expectations.

## Do Not

- Edit `site/public/` as if it were source unless the task is explicitly about generated output verification.
- Add site-only component facts that contradict registry/docs.
- Add new docs dependencies casually; docs builds still need to fit the repo's Python-first toolchain.

## Own

- `site/config/`
- `site/content/`
- `site/assets/`
- Generated-site verification via `uv run poe docs-build-all`
- Tests: `tests/test_docs_site.py`
