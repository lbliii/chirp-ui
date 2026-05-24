# DESIGN: LLM Source Enrichment

**Status:** scoped to SSG source enrichment; do not override Bengal outputs
**Created:** 2026-05-11
**Purpose:** make agent-facing docs current and registry-grounded through the
published docs sources that Bengal already turns into site artifacts.

## Decision

Chirp UI will not override Bengal/SSG-owned `llms.txt`, `agent.json`, search
indexes, page JSON, sitemap, or other site-wide generated artifacts.

Sprint 4 instead improves the source content and metadata those SSG artifacts
consume:

- `src/chirp_ui/manifest.json`
- generated `docs/COMPONENT-OPTIONS.md`
- durable docs listed in `docs/INDEX.md`
- `docs/agents/docs-ia-migration.md`
- `docs/agents/agent-source-inventory.md`
- `docs/agents/agent-source-map.md`
- `site/content/docs/**/*.md` front matter and prose
- vetted copyable snippets from dynamic examples

The static showcase is visual reference only. It is not a source for copyable
LLM snippets.

## Output Ownership

Bengal owns:

- `site/public/llms.txt`
- `site/public/agent.json`
- `site/public/index.json`
- page JSON/Markdown/LLM projections
- sitemap and robots output

Chirp UI owns:

- `src/chirp_ui/manifest.json`
- `site/public/chirpui.manifest.json` emitted from the manifest
- durable docs and site content that Bengal consumes

If Chirp UI later needs a richer agent-specific artifact, it must use a distinct
name and contract, such as `chirpui.agent.json`, and go through a separate
stop-and-ask decision. It must not replace SSG outputs.

## Input Rules

Manifest-derived content is authoritative for:

- component names
- macro names
- params
- slots
- variants, sizes, appearance, tone
- runtime requirements
- emitted classes
- tokens

Docs-derived content is authoritative for:

- concepts
- ownership rules
- migration notes
- safety guidance
- pattern recipes

Example-derived content is allowed only when explicitly vetted as copyable by
`docs/agents/agent-source-inventory.md`.

## Exclusions

Generated copyable snippets must reject:

- `sc-*` static showcase classes.
- `docs-*` fixture wrappers.
- inline fixture scripts.
- raw `chirpui-*` class-heavy markup when a macro example exists.
- appearance/tone classes instead of macro params.
- `attrs_unsafe` examples unless the snippet is explicitly about escape hatches.

## Source Contract

Source enrichment must:

- deterministic ordering
- canonical source links in published docs pages
- tests that every published docs page has a durable source mapping
- provenance labels in source maps for manifest/docs/example-derived content
- no static-showcase scraping as a source of public API
- a maintained source inventory that distinguishes `source-only`,
  `candidate-review`, `copyable-curated`, and `excluded` inputs
- a maintained source map that names generated-output ownership and source
  inputs without adding a replacement generator

## Required Proof

- Docs/source-map coverage tests.
- Tests that docs build tasks do not override SSG-owned LLM artifacts.
- Freshness tests against current manifest schema where source content cites it.
- Tests that published docs pages include canonical durable source links.
- Tests that copyable snippets exclude static showcase wrappers and raw utility-like classes.
- `uv run poe docs-build-all`.

## Stop-And-Ask Items

- Any repo-owned artifact that overlaps Bengal's SSG outputs.
- Adding new agent-facing artifact names such as `chirpui.agent.json`.
- Using static showcase content as an endpoint source.
- Adding generation dependencies or custom build steps for SSG-owned artifacts.

## Non-Goals

- Replacing the manifest.
- Hand-authored prompt packs.
- Scraping generated HTML as source of truth.
- Overriding Bengal `llms.txt` or `agent.json`.
