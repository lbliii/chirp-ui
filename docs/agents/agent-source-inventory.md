# Agent Source Inventory

**Status:** active Sprint 6 source contract
**Created:** 2026-05-12
**Plan:** `docs/plans/done/PLAN-skeleton-equivalent-roadmap.md` Sprint 6

This inventory defines which Chirp UI sources may inform agent-facing content
and which sources must never be scraped for copyable snippets. It complements
`docs/decisions/llm-endpoints.md` and `docs/agents/agent-source-map.md`, keeping
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

No `candidate-review` source is approved for automatic snippet extraction.
Curated copyable snippets live in `docs/agents/agent-curated-snippets.md` and must pass
the review gate below.

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
| `manifest-derived` | `src/chirp_ui/find.py` | Human/agent registry discovery over the installed manifest through `python -m chirp_ui find --details`: component name, category, maturity, authoring, role, macro, template, runtime requirements, slots, and summary. | `source-only` |
| `manifest-derived` | `docs/COMPONENT-OPTIONS.md` | Generated macro/options reference that mirrors the manifest for humans and agents. | `source-only` |
| `docs-derived` | `docs/INDEX.md` | Durable documentation navigation and canonical source discovery. | `source-only` |
| `docs-derived` | `docs/decisions/design-system-research.md` | External design-system research, Chirp UI product opinion, Bengal shell implications, and maturity gates. | `source-only` |
| `docs-derived` | `docs/decisions/typography-rhythm-taste-floor.md` | Typography role, rhythm, measure, and screen-proof research for the visual taste-floor saga; planning input only, not public token vocabulary. | `source-only` |
| `docs-derived` | `docs/decisions/typography-role-matrix.md` | Recipe-only typography audit matrix for golden-screen role mapping; source-only until public token promotion is approved. | `source-only` |
| `docs-derived` | `docs/safety/public-surface-stabilization.md` | Evidence labels, promotion rules, recipe-only boundaries, compatibility policy, and maturity-discovery commands. | `source-only` |
| `docs-derived` | `docs/decisions/interactive-anatomy.md` | Interactive anatomy contract and evidence ledger fields for behavior-bearing promotions. | `source-only` |
| `docs-derived` | `docs/agents/docs-ia-migration.md` | Published docs IA, durable-source map, and SSG ownership boundary. | `source-only` |
| `docs-derived` | `docs/agents/agent-source-inventory.md` | Agent provenance policy and snippet source inventory. | `source-only` |
| `docs-derived` | `docs/agents/agent-source-map.md` | Generated-output ownership map and source-input map. | `source-only` |
| `docs-derived` | `docs/agents/agent-curated-snippets.md` | Hand-curated macro-first snippets that passed the review gate. | `copyable-curated` |
| `docs-derived` | `docs/agents/registry-discovery.md` | CLI and Python discovery workflows over manifest labels and component metadata. | `source-only` |
| `docs-derived` | `docs/screens/` | Screen archetype selection, profile pairing, fixture proof, promotion-ledger boundaries, and agent guidance for complete product situations. | `source-only` |
| `docs-derived` | `docs/reference-implementations/playbook.md` | Reference implementation evidence ladder, scenario-complete criteria, and promotion boundaries. | `source-only` |
| `docs-derived` | `docs/reference-implementations/README.md` | Index of reference implementation briefs for blocked promotion candidates. | `source-only` |
| `docs-derived` | `docs/reference-implementations/PROOF-ANALYSIS.md` | Source-only proof-analysis decisions for scenario-complete reference fixtures and public-API non-authorizations. | `source-only` |
| `docs-derived` | `docs/reference-implementations/RECIPE-GUIDANCE.md` | Source-only recipe guidance for reference candidates kept on current primitives. | `source-only` |
| `docs-derived` | `tests/browser/test_page_actions_candidate.py` | Browser proof for private page-action reference fixtures and public-API boundaries. | `source-only` |
| `docs-derived` | `tests/browser/test_linked_nav_candidate.py` | Browser proof for private linked-nav reference fixtures and public-API boundaries. | `source-only` |
| `docs-derived` | `tests/browser/test_compact_header_candidate.py` | Browser proof for private compact-header reference fixtures and public-API boundaries. | `source-only` |
| `docs-derived` | `tests/browser/test_dense_reference_data_reference.py` | Browser proof for private dense-reference fixtures and public-API boundaries. | `source-only` |
| `docs-derived` | `tests/test_shell_response_targets.py` | Server proof for shell response ownership reference contracts. | `source-only` |
| `docs-derived` | `tests/browser/test_consumer_shell_actions_oob.py` | Browser proof for consumer shell action response contracts. | `source-only` |
| `docs-derived` | `tests/test_find_cli.py` | CLI proof for agent discovery reference contracts. | `source-only` |
| `docs-derived` | `docs/components/appearance-tone.md` | Appearance/tone semantics and migration guidance. | `source-only` |
| `docs-derived` | `docs/components/context-menu-anatomy.md` | Shipped context-menu anatomy, proof ledger, and keyboard/focus contract. | `source-only` |
| `docs-derived` | `docs/components/menubar-anatomy.md` | Shipped menubar anatomy, proof ledger, and roving-focus contract. | `source-only` |
| `docs-derived` | `docs/components/input-otp-anatomy.md` | Shipped input OTP anatomy, proof ledger, and paste/backspace contract. | `source-only` |
| `docs-derived` | `docs/theming/app-theme.md` | App theme-pack load order, token-only rules, and ownership guidance. | `source-only` |
| `docs-derived` | `docs/components/dropdown-anatomy.md` | Dropdown rendered anatomy and tested behavior. | `source-only` |
| `docs-derived` | `docs/components/modal-anatomy.md` | Modal, overlay, and confirm rendered anatomy and tested behavior. | `source-only` |
| `docs-derived` | `docs/components/tabs-anatomy.md` | Tabs, tab panels, route tabs, and tabbed layout anatomy. | `source-only` |
| `docs-derived` | `docs/components/drawer-tray-anatomy.md` | Drawer and tray rendered anatomy and tested behavior. | `source-only` |
| `docs-derived` | `docs/theming/bengal-theme-anatomy.md` | Packaged Bengal theme controls, search, mobile nav, TOC, and docs tab hooks. | `source-only` |
| `docs-derived` | `site/content/docs/` | Published docs source front matter and concise mirrors consumed by Bengal. | `source-only` |
| `example-derived` | `examples/component-showcase/app.py` | Dynamic route map and server-side fragment context for runnable examples. | `source-only` |
| `example-derived` | `examples/component-showcase/templates/showcase/` | Dynamic showcase templates may inform agents only through candidate-review policy; they are not automatic snippets. | `candidate-review` |
| `example-derived` | `examples/component-showcase/templates/showcase/appearance-tone.html` | Runnable appearance/tone macro usage examples. | `candidate-review` |
| `example-derived` | `examples/component-showcase/templates/showcase/theme-packs.html` | Runnable theme-pack catalog examples. | `candidate-review` |
| `example-derived` | `examples/component-showcase/templates/showcase/htmx.html` | Runnable htmx pattern examples. | `candidate-review` |
| `example-derived` | `examples/component-showcase/templates/showcase/ui.html` | Runnable interactive component examples. | `candidate-review` |
| `example-derived` | `examples/component-showcase/templates/showcase/navigation.html` | Runnable navigation examples and dense navigation recipes. | `candidate-review` |
| `example-derived` | `examples/component-showcase/templates/showcase/operations_shell.html` | Source fixture for the Command Center golden screen; informs screen-level guidance only through `docs/screens/command-center.md`. | `candidate-review` |
| `example-derived` | `examples/component-showcase/templates/showcase/support_shell.html` | Source fixture for the Review Queue golden screen; informs screen-level guidance only through `docs/screens/review-queue.md`. | `candidate-review` |
| `example-derived` | `examples/component-showcase/templates/showcase/screen_agent_run_monitor.html` | Source fixture for the Agent Run Monitor golden screen; informs screen-level guidance only through `docs/screens/agent-run-monitor.md`. | `candidate-review` |
| `example-derived` | `examples/component-showcase/templates/showcase/screen_product_docs_home.html` | Source fixture for the Product/Docs Home golden screen; informs screen-level guidance only through `docs/screens/product-docs-home.md`. | `candidate-review` |

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
