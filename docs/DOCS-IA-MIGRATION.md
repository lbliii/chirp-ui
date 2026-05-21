# Docs IA Migration Matrix

**Status:** active Sprint 4 source map
**Created:** 2026-05-11
**Plan:** `docs/plans/done/PLAN-skeleton-equivalent-roadmap.md` Sprint 4

This matrix maps the current published docs site to the target information
architecture for Chirp UI's Skeleton-equivalent documentation work. The goal is
to make published pages and future LLM endpoints cite the same durable sources
instead of duplicating component facts.

## Target IA

| Target section | Job | Canonical durable sources |
|---|---|---|
| Get Started | Install and wire Chirp UI into an app | `README.md`, `docs/ANTI-FOOTGUNS.md`, `docs/VISION.md` |
| Fundamentals | Explain layout, composition, tokens, responsive behavior, layers, and safe overrides | `docs/LAYOUT.md`, `docs/PRIMITIVES.md`, `docs/COMPOSITION.md`, `docs/RESPONSIVE.md`, `docs/TYPOGRAPHY.md`, `docs/TOKENS.md`, `docs/UI-LAYERS.md`, `docs/CSS-OVERRIDE-SURFACE.md` |
| Design System | Teach visual presets, themes, tokens, and motion as registry-backed contracts | `docs/APPEARANCE-TONE.md`, `docs/APP-THEME.md`, `docs/TOKENS.md`, `docs/TRANSITIONS.md`, `docs/DESIGN-appearance-tone.md`, `docs/DESIGN-theme-pack-catalog.md` |
| Components | Publish macro usage, params, runtime requirements, slots, and examples | `docs/COMPONENT-OPTIONS.md`, `src/chirp_ui/components.py`, `src/chirp_ui/templates/chirpui/` |
| Patterns | Compose components into product, media, forum, navigation, search, HTMX, Alpine, layout-affinity, and shell workflows | `docs/NAVIGATION.md`, `docs/DENSE-NAVIGATION-SYNTHESIS.md`, `docs/DENSE-NAVIGATION-RECIPES.md`, `docs/plans/PLAN-application-chrome-system.md`, `docs/SEARCH-SHELL-RECIPES.md`, `docs/DESIGN-layout-affinity.md`, `docs/LAYOUT-AFFINITY-RESOLVER-AUTHORING.md`, `docs/plans/PLAN-layout-affinity-rollout.md`, `docs/plans/PLAN-search-shell-contracts.md`, `docs/PRODUCT-PAGE-PATTERNS.md`, `docs/MEDIA-SITE-PATTERNS.md`, `docs/FORUM-SITE-PATTERNS.md`, `docs/HTMX-PATTERNS.md`, `docs/ALPINE-MAGICS.md`, `docs/DND-FRAGMENT-ISLAND.md`, `docs/WIZARD-FORM.md` |
| Integrations | Explain Chirp, htmx, Alpine, Bengal theme, and app shell integration boundaries | `README.md`, `docs/UI-LAYERS.md`, `docs/CHIRP-THEME.md`, `docs/CHIRP-THEME-PARITY-MATRIX.md`, `docs/proposals/CHIRP-FRAMEWORK-SUPPORT.md` |
| Agent Manifest | Publish generated agent-facing artifacts and provenance | `docs/DESIGN-llm-endpoints.md`, `docs/VISION.md`, `src/chirp_ui/manifest.py`, `src/chirp_ui/manifest.json`, `docs/COMPONENT-OPTIONS.md` |
| Theming | Explain app theme packs, Bengal docs theme, CSS variables, and override ownership | `docs/APP-THEME.md`, `docs/CHIRP-THEME.md`, `docs/CHIRP-THEME-PARITY-MATRIX.md`, `docs/TOKENS.md`, `docs/CSS-OVERRIDE-SURFACE.md` |

## Published Page Map

Every published docs page must name a durable source. Pages may summarize for
the site, but component facts, macro parameters, slots, tokens, generated
manifest fields, and migration rules should come from the canonical source.

| Published source | Target section | Canonical durable source | Migration action |
|---|---|---|---|
| `site/content/docs/_index.md` | Get Started | `docs/INDEX.md` | Uses Bengal `cards`/`card` directives; keep links aligned with published reference surfaces. |
| `site/content/docs/about/_index.md` | Integrations | `docs/VISION.md`, `README.md` | Keep as a short philosophy and integration overview; avoid new component facts. |
| `site/content/docs/app-shell/_index.md` | Integrations | `docs/UI-LAYERS.md`, `docs/SHELL-TABS-CONTRACT.md`, `docs/NAVIGATION.md`, `docs/COMPONENT-OPTIONS.md` | Keep quick-start snippet; mirror shell target-boundary and filesystem recipe guidance without adding site-only component facts. |
| `site/content/docs/app-shell/ui-layers.md` | Fundamentals | `docs/UI-LAYERS.md`, `docs/SHELL-TABS-CONTRACT.md` | Keep aligned with Chirp shell vocabulary and avoid site-only terminology. |
| `site/content/docs/components/_index.md` | Components | `docs/COMPONENT-OPTIONS.md`, `src/chirp_ui/manifest.json` | Prefer generated category summaries once LLM/docs generator lands. |
| `site/content/docs/components/appearance-tone.md` | Design System | `docs/APPEARANCE-TONE.md` | Keep as published mirror and cite the durable guide. |
| `site/content/docs/components/ascii.md` | Components | `docs/COMPONENT-OPTIONS.md`, `src/chirp_ui/templates/chirpui/ascii_*.html` | Either add a durable ASCII guide later or keep this as a generated/component-reference summary. |
| `site/content/docs/components/dropdowns.md` | Components | `docs/DROPDOWN-ANATOMY.md`, `docs/ALPINE-MAGICS.md` | Keep as published mirror and cite the tested anatomy guide. |
| `site/content/docs/components/drawers-trays.md` | Components | `docs/DRAWER-TRAY-ANATOMY.md`, `docs/ALPINE-MAGICS.md` | Keep as published mirror and cite the tested anatomy guide. |
| `site/content/docs/components/islands.md` | Patterns | `docs/DND-FRAGMENT-ISLAND.md`, `docs/ALPINE-MAGICS.md` | Align terminology with fragment islands and Alpine controller guidance. |
| `site/content/docs/components/modals.md` | Components | `docs/MODAL-ANATOMY.md`, `docs/ALPINE-MAGICS.md`, `docs/HTMX-PATTERNS.md` | Keep as published mirror and cite the tested anatomy guide. |
| `site/content/docs/components/tabs.md` | Components | `docs/TABS-ANATOMY.md`, `docs/SHELL-TABS-CONTRACT.md`, `docs/NAVIGATION.md` | Keep as published mirror and preserve route-tab vs ARIA-tab distinction. |
| `site/content/docs/components/type-aware-rendering.md` | Components | `docs/COMPONENT-OPTIONS.md` | Keep facts tied to `description_list` generated reference. |
| `site/content/docs/get-started/_index.md` | Get Started | `README.md`, `docs/ANTI-FOOTGUNS.md` | Keep short; point deeper architecture to durable docs. |
| `site/content/docs/get-started/installation.md` | Get Started | `README.md`, `pyproject.toml` | Keep install commands and version examples in sync with package metadata. |
| `site/content/docs/patterns/_index.md` | Patterns | `docs/NAVIGATION.md`, `docs/SEARCH-SHELL-RECIPES.md`, `docs/DESIGN-layout-affinity.md`, `docs/PRODUCT-PAGE-PATTERNS.md`, `docs/MEDIA-SITE-PATTERNS.md`, `docs/FORUM-SITE-PATTERNS.md` | Keep as index; avoid inventing pattern contracts. |
| `site/content/docs/patterns/forums.md` | Patterns | `docs/FORUM-SITE-PATTERNS.md` | Keep published summary with canonical guide link. |
| `site/content/docs/patterns/media-sites.md` | Patterns | `docs/MEDIA-SITE-PATTERNS.md` | Keep published summary with canonical guide link. |
| `site/content/docs/patterns/navigation.md` | Patterns | `docs/NAVIGATION.md`, `docs/DENSE-NAVIGATION-SYNTHESIS.md`, `docs/DENSE-NAVIGATION-RECIPES.md`, `docs/plans/PLAN-application-chrome-system.md` | Keep published summary with canonical guide links and recipe-first application chrome status. |
| `site/content/docs/patterns/layout-affinity.md` | Patterns | `docs/DESIGN-layout-affinity.md`, `docs/LAYOUT-AFFINITY-RESOLVER-AUTHORING.md`, `docs/plans/PLAN-layout-affinity-rollout.md`, `docs/SEARCH-SHELL-RECIPES.md`, `docs/PRIMITIVES.md` | Keep published summary with prototype status; do not promote descriptor or manifest fields here. |
| `site/content/docs/patterns/product-pages.md` | Patterns | `docs/PRODUCT-PAGE-PATTERNS.md` | Keep published summary with canonical guide link. |
| `site/content/docs/patterns/search-shells.md` | Patterns | `docs/SEARCH-SHELL-RECIPES.md`, `docs/DESIGN-layout-affinity.md`, `docs/HTMX-PATTERNS.md`, `docs/RESPONSIVE.md`, `docs/VERIFICATION.md`, `docs/plans/PLAN-search-shell-contracts.md` | Keep published summary with canonical guide links and recipe-first search-shell status. |
| `site/content/docs/theming/_index.md` | Theming | `docs/APP-THEME.md`, `docs/TOKENS.md`, `docs/CSS-OVERRIDE-SURFACE.md` | Keep theme-pack names and load order in sync with catalog docs. |
| `site/content/docs/theming/bengal-theme-controls.md` | Theming | `docs/BENGAL-THEME-ANATOMY.md`, `docs/CHIRP-THEME.md` | Keep as a published mirror for packaged theme controls; do not describe them as registry-owned Chirp UI component APIs. |
| `site/content/docs/theming/chirp-theme.md` | Theming | `docs/CHIRP-THEME.md`, `docs/CHIRP-THEME-PARITY-MATRIX.md` | Keep Bengal theme package guidance aligned with transitional alias mapping. |

## SSG Source Enrichment Map

Bengal owns site-wide generated artifacts such as `llms.txt`, `agent.json`,
search indexes, page JSON, sitemap, and robots output. Chirp UI should not
override those files. This source map defines what Chirp UI-owned content should
feed into the SSG pipeline and any future Chirp UI-owned agent artifact with a
distinct name.

| Source section | Provenance label | Allowed source |
|---|---|---|
| Library summary | docs-derived | `docs/VISION.md`, `README.md` |
| Current manifest schema and stats | manifest-derived | `src/chirp_ui/manifest.json` from `scripts/build_manifest.py` |
| Component inventory | manifest-derived | `src/chirp_ui/manifest.json` |
| Macro signatures and options | manifest-derived | `docs/COMPONENT-OPTIONS.md`, generated from manifest |
| Theme packs | manifest-derived | `src/chirp_ui/manifest.json`, `docs/APP-THEME.md` |
| Public docs map | docs-derived | `docs/INDEX.md`, this matrix, `site/content/docs/**/*.md` front matter |
| Agent source inventory | docs-derived | `docs/AGENT-SOURCE-INVENTORY.md` |
| Agent source map | docs-derived | `docs/AGENT-SOURCE-MAP.md` |
| Copyable examples | example-derived | Vetted dynamic showcase snippets listed in `docs/AGENT-SOURCE-INVENTORY.md` only |

## Exclusion Rules

Agent-facing copyable snippets must reject:

- `sc-*` static showcase classes.
- `docs-*` site fixture wrappers.
- inline fixture scripts.
- raw `chirpui-*` class-heavy markup when a macro example exists.
- raw appearance/tone modifier classes instead of macro params.
- `attrs_unsafe` examples unless the snippet is explicitly about escape hatches.

## First Implementation Slices

1. Decide whether Chirp UI needs a repo-owned endpoint generator or should
   rely on Bengal's site-wide `llms.txt`/`agent.json` output. Decision:
   rely on Bengal for SSG-owned outputs.
2. Improve the source docs and front matter that Bengal consumes.
3. Add a regression check that docs build tasks do not override SSG-owned
   `llms.txt` or `agent.json`.
4. Add tests that this matrix covers all published docs pages and that generated
   snippets honor the exclusion rules.
5. Sprint 6 source inventory added in `docs/AGENT-SOURCE-INVENTORY.md`; keep
   snippet eligibility there rather than inferring from generated site output.
6. Sprint 6 source map added in `docs/AGENT-SOURCE-MAP.md`; keep generated
   output ownership there and do not add replacement tasks for Bengal-owned
   artifacts.
