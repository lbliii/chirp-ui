# Agent Source Inventory

**Status:** active Sprint 6 source contract
**Created:** 2026-05-12
**Plan:** `docs/plans/PLAN-skeleton-equivalent-roadmap.md` Sprint 6

This inventory defines which Chirp UI sources may inform agent-facing content
and which sources must never be scraped for copyable snippets. It complements
`docs/DESIGN-llm-endpoints.md` and `docs/AGENT-SOURCE-MAP.md`, keeping
Chirp-owned source enrichment separate from Bengal-owned generated site
artifacts.

## Policy

Chirp UI agent-facing synthesis uses three provenance labels:

- `manifest-derived`: generated from the component registry or manifest.
- `docs-derived`: durable source docs and published docs source content.
- `example-derived`: runnable examples that still require snippet-specific
  vetting before they become copyable agent examples.

Snippet eligibility uses these values:

- `source-only`: may inform summaries or source maps, but must not be emitted as
  a copyable snippet.
- `candidate-review`: may contain useful examples, but each snippet must be
  explicitly extracted, filtered, and tested before publication.
- `copyable-curated`: approved for copyable snippets after provenance tests.
- `excluded`: must never be used as an agent-facing source.

No current source is approved for automatic snippet extraction. Sprint 6 starts
with the inventory and provenance tests so later generation work has a safe
allowlist to build from.

## Snippet Review Gate

A `candidate-review` source can move to `copyable-curated` only in a PR that
adds all of the following:

| Gate | Required proof |
|---|---|
| Exact source path | The snippet cites the original durable doc or dynamic showcase template line of ownership. |
| Macro-first shape | The snippet uses public macros, params, slots, `attrs_map`, and `hx={}` before raw classes. |
| Exclusion scan | The snippet contains no static showcase classes, docs wrappers, inline scripts, browser-test selectors, or raw appearance/tone modifier classes. |
| Runnable proof | A render, docs, example, or browser test exercises the snippet's public contract. |
| Provenance note | The snippet declares `example-derived` or `docs-derived` provenance and links back to this inventory. |

## Source Inventory

| Provenance | Source | Agent use | Snippet eligibility |
|---|---|---|---|
| `manifest-derived` | `src/chirp_ui/manifest.json` | Component inventory, macro names, params, slots, variants, sizes, appearance, tone, emitted classes, runtime requirements, theme-pack catalog. | `source-only` |
| `manifest-derived` | `docs/COMPONENT-OPTIONS.md` | Generated macro/options reference that mirrors the manifest for humans and agents. | `source-only` |
| `docs-derived` | `docs/INDEX.md` | Durable documentation navigation and canonical source discovery. | `source-only` |
| `docs-derived` | `docs/DOCS-IA-MIGRATION.md` | Published docs IA, durable-source map, and SSG ownership boundary. | `source-only` |
| `docs-derived` | `docs/AGENT-SOURCE-INVENTORY.md` | Agent provenance policy and snippet source inventory. | `source-only` |
| `docs-derived` | `docs/AGENT-SOURCE-MAP.md` | Generated-output ownership map and source-input map. | `source-only` |
| `docs-derived` | `docs/APPEARANCE-TONE.md` | Appearance/tone semantics and migration guidance. | `source-only` |
| `docs-derived` | `docs/APP-THEME.md` | App theme-pack load order, token-only rules, and ownership guidance. | `source-only` |
| `docs-derived` | `docs/DROPDOWN-ANATOMY.md` | Dropdown rendered anatomy and tested behavior. | `source-only` |
| `docs-derived` | `docs/MODAL-ANATOMY.md` | Modal, overlay, and confirm rendered anatomy and tested behavior. | `source-only` |
| `docs-derived` | `docs/TABS-ANATOMY.md` | Tabs, tab panels, route tabs, and tabbed layout anatomy. | `source-only` |
| `docs-derived` | `docs/DRAWER-TRAY-ANATOMY.md` | Drawer and tray rendered anatomy and tested behavior. | `source-only` |
| `docs-derived` | `docs/BENGAL-THEME-ANATOMY.md` | Packaged Bengal theme controls, search, mobile nav, TOC, and docs tab hooks. | `source-only` |
| `docs-derived` | `site/content/docs/` | Published docs source front matter and concise mirrors consumed by Bengal. | `source-only` |
| `example-derived` | `examples/component-showcase/app.py` | Dynamic route map and server-side fragment context for runnable examples. | `source-only` |
| `example-derived` | `examples/component-showcase/templates/showcase/appearance-tone.html` | Runnable appearance/tone macro usage examples. | `candidate-review` |
| `example-derived` | `examples/component-showcase/templates/showcase/theme-packs.html` | Runnable theme-pack catalog examples. | `candidate-review` |
| `example-derived` | `examples/component-showcase/templates/showcase/htmx.html` | Runnable htmx pattern examples. | `candidate-review` |
| `example-derived` | `examples/component-showcase/templates/showcase/ui.html` | Runnable interactive component examples. | `candidate-review` |
| `example-derived` | `examples/component-showcase/templates/showcase/navigation.html` | Runnable navigation examples and dense navigation recipes. | `candidate-review` |

## Snippet Exclusions

| Source or pattern | Reason |
|---|---|
| `examples/static-showcase/` | Visual static gallery output is not source truth and contains showcase scaffolding. |
| `site/public/` | Generated Bengal output; never hand-authored source. |
| `tests/browser/` | Browser fixtures are proof surfaces, not public examples. |
| `examples/component-showcase/templates/base.html` | Showcase shell chrome; not a copyable component recipe. |
| `examples/component-showcase/templates/index.html` | Showcase navigation page; contains index chrome and raw class-heavy summaries. |
| `site/content/showcase/_index.md` | Published placeholder for generated showcase output. |
| `site/content/docs/` as snippets | Published docs mirrors may summarize sources, but snippets must cite durable docs or curated examples directly. |
| `sc-*` | Static showcase implementation classes are not public API. |
| `docs-*` | Docs-site fixture wrappers are not public API. |
| inline `<script>` | Copyable snippets must not teach inline behavior scripts. |
| `attrs_unsafe` | Allowed only in an explicit escape-hatch guide, never in general component snippets. |
| raw `chirpui-*` class-heavy markup | Prefer public macros and params when a macro exists. |
| raw appearance/tone modifier classes | Use `appearance=` and `tone=` macro params instead. |

## Curating Candidate Examples

Before any `candidate-review` source becomes `copyable-curated`, the extracting
slice must prove:

1. The source uses public macros, params, slots, and safe `attrs_map`/`hx={}`
   patterns where available.
2. The snippet does not include static showcase classes, docs wrappers, inline
   scripts, or browser-test-only selectors.
3. Raw `chirpui-*` classes appear only when the snippet is explicitly about
   CSS override surfaces or a component has no macro representation.
4. Appearance and tone use macro parameters, not hand-authored modifier classes.
5. `attrs_unsafe` appears only in a dedicated escape-hatch snippet that explains
   the trust boundary.
6. The snippet names its provenance as `example-derived` and points to this
   inventory plus the original source file.

## Output Boundary

Bengal continues to own `llms.txt`, `agent.json`, page JSON, page Markdown,
search indexes, sitemap, and robots output. This inventory may enrich sources
that Bengal consumes, but it does not authorize a replacement generator or a new
repo-owned agent artifact.
