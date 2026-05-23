# chirp-theme bespoke rewrite waves

**Status:** active bespoke rewrite
**Owner:** chirp-theme  
**Scope:** Fully custom Bengal theme implemented with Chirp UI primitives

> Current note: this plan has been reframed. `chirp-theme` is not a Bengal
> default-theme parity project. It is a 100% bespoke theme whose implementation
> language is Chirp UI macros, `--chirpui-*` tokens, and narrowly scoped
> theme-owned CSS. The retained asset shim is temporary platform plumbing, not
> the theme architecture.

## Context

`chirp-theme` is no longer a thin clone of Bengal default. The retained shell,
docs, blog, card directives, docs navigation, and admonition directive route
through Chirp UI primitives or narrowly scoped integration CSS.

The next goal is not matching the original Bengal default theme. The goal is a
fully bespoke Bengal theme with its own shell, content hierarchy, navigation
model, page rhythm, and reference surfaces. When a default-theme surface is
still useful as input, treat it as product research, then rebuild the output
from first principles with current Kida templates, `chirpui/*` macros, and
`--chirpui-*` tokens.

Audit basis: compared
`b-stack/bengal/bengal/themes/default/templates/` with
`src/bengal_themes/chirp_theme/templates/` after the initial Chirp UI migration.
Excluding default-theme documentation files and `__pycache__`, 61 template paths
are shared and 83 default-theme output templates remain unported.

## Custom Theme Backlog

| Family | Legacy surface to retire | Bespoke Chirp UI target |
|---|---|---|
| Shell and navigation | copied header/menu/footer shape | Chirp UI navbar/footer shell with theme-owned identity, mobile dialog, search, and theme controls |
| Docs and prose | generic docs/page frames | bespoke article frame, docs rail, TOC rail, breadcrumbs, prose surface, action bar |
| Blog and editorial | post/list defaults | editorial hero, resource cards, tags, related content, archive rhythm |
| Autodoc and reference internals | default reference tables/cards | reference frame, route tabs, schema tables, code panels, badges, callouts |
| Shortcodes and embeds | copied shortcode wrappers | callout, figure/media embeds, disclosure/details, code/highlight, safe links |
| Taxonomy/archive/author/category | default listing cards | resource indexes, badges, list filters, author/category landing surfaces |
| API/OpenAPI hubs | default API hubs | endpoint cards, request/response panels, schema tables, reference nav |
| Tracks/tutorial/notebook/changelog/resume | learning/resume defaults | learning layout, progress/stepper, sidebar, resource cards, prose surfaces |

## Current Wave — Bespoke Shell And Content Spine

Status: in progress.

Build the theme's own visible spine before deeper verticals:

- desktop shell uses Chirp UI navbar and site footer macros;
- mobile navigation, search modal, theme controls, and the asset shim remain
  Bengal/theme-owned until platform support replaces them;
- body and main content expose stable `chirp-theme-shell` hooks;
- core page, docs, blog, listing, search, and error templates keep moving
  toward Chirp UI primitives and away from copied default-theme structure.
- docs list/single pages call Chirp UI `page_hero` directly, and the legacy
  page-hero compatibility macros now emit Chirp UI `page_hero` markup with
  theme-owned hooks;
- pagination, section navigation, and the docs TOC carry Chirp UI pagination,
  card, badge, grid, surface, and nav-tree classes while retaining the JS hooks
  Bengal still owns.
- docs, generic page, blog, and section index single/list pages now stay inside
  the app-shell frame and render only their owned content in the main panel.
- the catalog-browser shape uses a symbol-only primary `filter_rail` with
  hover/focus labels beside the existing Chirp UI sidebar section tree.
- the inner rail now behaves like a contextual workbench: it has a section
  identity card, article-set metadata, type-aware row icons, row metadata, and
  active branch card styling.
- the right TOC rail now follows the same rail language as a compact page map:
  page identity, heading count, progress stripe, heading-level marks, and
  active row/card styling.
- the old floating back-to-top button is now a rail action when the TOC rail is
  present, with the body-level control retained only as a fallback for pages
  without that rail.
- blog article, author, share, article-card, and card-base compatibility
  surfaces now emit Chirp UI card, surface, dropdown, button, and resource-card
  markup instead of the old `.blog-post`, `.article-card`, `.card__*`, and
  share-button families.

Required proof:
- `base.html` imports and uses `chirpui/navbar.html` and
  `chirpui/site_footer.html`;
- body output carries `data-chirp-theme-spine="bespoke"`;
- the theme stylesheet contains active `chirp-theme-shell` hooks;
- the current `assets/css/style.css` Chirp UI imports remain until Bengal
  library asset modes are released;
- built docs pages use `chirp-theme-doc-hero`, `chirp-theme-doc-toc`, and
  `chirpui-nav-tree` hooks instead of active legacy page-hero roots;
- built article pages use `chirp-theme-doc-catalog` and `chirpui-filter-rail`
  hooks for the full-page double-left-rail catalog shell;
- source contracts cover blog single pages and article-card compatibility
  surfaces with `chirp-theme-blog-article` and `chirpui-resource-card`
  without active `.blog-post` roots;
- built HTML references emitted assets only.

## Ranked Waves

### Wave 1 — Taxonomy and Archive Listings

Status: shipped in the current chirp-theme migration stack.

Rebuild `tag.html`, `tags.html`, `archive.html`, `archive-year.html`,
`author.html`, `authors/list.html`, `authors/single.html`, and
`category-browser.html` using retained post/resource card macros.

Required proof:
- Render a fixture site with tags, authors, categories, and archives.
- Assert output uses `chirpui-resource-card`, `chirpui-badge`, and retained
  pagination/navigation components.
- No dormant taxonomy-specific CSS unless an active template references it.

Implemented proof currently covers packaged template resolution plus the dogfood
docs site's generated tag index and tag pages. Authors, categories, and archive
fixtures still need dedicated content fixtures before this plan moves to done.

### Wave 2 — Learning Content

Status: shipped in the current chirp-theme migration stack.

Rebuild `tracks/`, `tutorial/`, `notebook/single.html`, and changelog/resume
views as learning/content systems rather than copied shells.

Required proof:
- Track and tutorial pages expose progress/navigation with Chirp UI primitives.
- Notebook pages keep prose, code, media, and outputs contained at mobile widths.
- Changelog/resume pages share the same resource/list primitives where possible.

Implemented proof currently covers packaged template resolution and source
contracts that require Chirp UI resource indexes, rendered content, stepper
progress, and retained post cards while forbidding copied inline scripts and
legacy learning card shells.

### Wave 3 — Python and CLI Autodoc

Status: shipped in the current chirp-theme migration stack.

Rebuild `autodoc/python/`, `autodoc/cli/`, and `autodoc/partials/` around a
single reference-page contract.

Required proof:
- Module, object, command, and section pages render from fixture autodoc data.
- Signatures, params, returns, raises, usage, examples, and member cards use
  Chirp UI code/table/card/badge primitives.
- Generated autodoc pages do not emit `/#/` placeholder links.

Implemented proof currently covers packaged template resolution and source
contracts requiring Chirp UI resource indexes, parameter tables, accordions,
code blocks, badges, and shared reference classes while forbidding copied
default autodoc table/card shells and inline scripts.

### Wave 4 — OpenAPI and API Hubs

Status: shipped in the current chirp-theme migration stack.

Rebuild `autodoc/openapi/`, `openapi-reference/`, `api-reference/`, `api-hub/`,
and `cli-reference/section-index.html`.

Required proof:
- Endpoint, schema, section, and hub fixtures render with Chirp UI navigation,
  code samples, request/response panels, and schema tables.
- Large schemas and code samples scroll within their containers without widening
  the page.

Implemented proof currently covers packaged template resolution and source
contracts requiring Chirp UI resource indexes, nav trees, parameter tables,
accordions, sticky request/response examples, code blocks, and shared reference
aliases while forbidding copied default OpenAPI/API hub shells and inline
scripts. REST endpoint pages should intentionally follow the familiar
Mintlify/Fern-style API reference convention rather than inventing a novel
navigation or reading model.

### Wave 5 — Shortcodes and Media Embeds

Status: shipped in the current chirp-theme migration stack.

Rebuild `shortcodes/` through safe, component-backed templates.

Required proof:
- `tip`, `warning`, and `danger` render through `callout`.
- `figure`, `img`, `audio`, and `gallery` use retained media/embed components.
- `ref` and `relref` preserve Bengal link semantics and escaping.
- `details`, `blockquote`, `highlight`, and `param` have render tests.

Implemented proof currently covers packaged template resolution plus source
contracts that require Chirp UI callout, accordion, card, gallery, and code
classes while forbidding copied default callout/gallery shells and inline
scripts.

### Wave 6 — Root Aliases and Utility Pages

Status: shipped in the current chirp-theme migration stack.

Rebuild `index.html`, `blog/about.html`, `blog/contact.html`, and any remaining
single-purpose aliases from retained page/blog primitives.

Required proof:
- No new one-off page shell CSS.
- Pages use `page_hero`, `surface`, `grid`, `stack`, and `resource_card` where
  appropriate.

Implemented proof currently covers packaged template resolution and source
contracts requiring the generic section resource index, retained blog shell,
Chirp UI page heroes, surfaces, rendered content, badges, and cards while
forbidding copied blog about/contact classes and inline scripts.

## Not Now

- Copying default-theme autodoc, OpenAPI, or shortcode templates as-is.
- Adding new Chirp UI components before proving existing primitives cannot
  express the output.
- Reintroducing private `--chirp-theme-*` tokens or dormant copied CSS for
  future verticals.
- Treating route-backed reference navigation as ARIA tabs.

## Steward Notes

- Documentation steward: this plan is active roadmap memory; shipped surfaces
  stay documented in `docs/CHIRP-THEME.md` and
  `docs/CHIRP-THEME-PARITY-MATRIX.md`.
- Planning steward: each wave should land as its own PR or commit series with
  fixture proof and updated parity matrix status.
- Theme steward: prefer Chirp UI macros and token hooks; if a missing primitive
  is discovered, record the component contract before adding theme CSS.
