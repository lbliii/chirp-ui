# chirp-theme content parity waves

**Status:** Active  
**Owner:** chirp-theme  
**Scope:** Bengal default output parity through Chirp UI-native templates

## Context

`chirp-theme` is no longer a thin clone of Bengal default. The retained shell,
docs, blog, card directives, docs navigation, and admonition directive now route
through Chirp UI primitives or narrowly scoped integration CSS.

The next goal is full content/output parity with the original Bengal default
theme without copying its bespoke template and CSS architecture forward. Each
wave should translate the default-theme idea into current Kida templates,
`chirpui/*` macros, and `--chirpui-*` tokens.

Audit basis: compared
`b-stack/bengal/bengal/themes/default/templates/` with
`src/bengal_themes/chirp_theme/templates/` after the initial Chirp UI migration.
Excluding default-theme documentation files and `__pycache__`, 61 template paths
are shared and 83 default-theme output templates remain unported.

## Parity Gap

| Family | Missing templates | Primary Chirp UI translation |
|---|---:|---|
| Autodoc and reference internals | 41 | docs frame, sidebar, breadcrumbs, cards, tables, badges, code blocks, callouts |
| Shortcodes | 13 | callout, figure/media embeds, disclosure/details, code/highlight, safe links |
| Taxonomy/archive/author/category | 8 | resource cards, resource indexes, badges, list filters |
| API/OpenAPI hubs | 8 | route tabs, endpoint cards, schema tables, code samples, request/response panels |
| Tracks/tutorial/notebook/changelog/resume | 9 | learning layout, progress/stepper, sidebar, resource cards, prose surfaces |
| Blog utility pages and root aliases | 3 | page templates composed from retained blog/page primitives |
| CLI reference section index | 1 | reference index card/grid pattern |

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

Rebuild `autodoc/python/`, `autodoc/cli/`, and `autodoc/partials/` around a
single reference-page contract.

Required proof:
- Module, object, command, and section pages render from fixture autodoc data.
- Signatures, params, returns, raises, usage, examples, and member cards use
  Chirp UI code/table/card/badge primitives.
- Generated autodoc pages do not emit `/#/` placeholder links.

### Wave 4 — OpenAPI and API Hubs

Rebuild `autodoc/openapi/`, `openapi-reference/`, `api-reference/`, `api-hub/`,
and `cli-reference/section-index.html`.

Required proof:
- Endpoint, schema, section, and hub fixtures render with Chirp UI navigation,
  code samples, request/response panels, and schema tables.
- Large schemas and code samples scroll within their containers without widening
  the page.

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

Rebuild `index.html`, `blog/about.html`, `blog/contact.html`, and any remaining
single-purpose aliases from retained page/blog primitives.

Required proof:
- No new one-off page shell CSS.
- Pages use `page_hero`, `surface`, `grid`, `stack`, and `resource_card` where
  appropriate.

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
