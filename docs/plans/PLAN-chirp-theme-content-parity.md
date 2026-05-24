# chirp-theme bespoke rewrite waves

**Status:** active bespoke rewrite
**Owner:** chirp-theme  
**Scope:** Fully custom Bengal theme implemented with Chirp UI primitives

> Current note: this plan has been reframed. `chirp-theme` is not a Bengal
> default-theme parity project. It is a 100% bespoke theme whose implementation
> language is Chirp UI macros, `--chirpui-*` tokens, and narrowly scoped
> theme-owned CSS. Provider assets now come from Bengal `library_asset_tags()`;
> the old relative CSS import shim is gone.

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

| Area | Current Target |
|---|---|
| Shell | Chirp UI navbar/site footer, stable `chirp-theme-shell` hooks, Bengal-owned mobile nav/search/theme controls. |
| Docs frame | Direct Chirp UI `page_hero`, app-shell-contained docs/page/blog/listing content, docs rail, TOC rail, and page actions. |
| Catalog rail | Symbol-only primary `filter_rail`, contextual sidebar section tree, section identity, metadata, active branch styling. |
| TOC rail | Compact page map with page identity, heading count, progress stripe, heading marks, and rail back-to-top action. |
| Blog/card compatibility | Chirp UI card, surface, dropdown, button, and resource-card markup instead of old `.blog-post`, `.article-card`, `.card__*`, and share-button families. |

Required proof:
- `base.html` imports and uses `chirpui/navbar.html` and
  `chirpui/site_footer.html`;
- body output carries `data-chirp-theme-spine="bespoke"`;
- the theme stylesheet contains active `chirp-theme-shell` hooks;
- `base.html` emits Chirp UI provider assets through `library_asset_tags()`
  while `assets/css/style.css` stays theme-owned;
- built docs pages use `chirp-theme-doc-hero`, `chirp-theme-doc-toc`, and
  `chirpui-nav-tree` hooks instead of active legacy page-hero roots;
- built article pages use `chirp-theme-doc-catalog` and `chirpui-filter-rail`
  hooks for the full-page double-left-rail catalog shell;
- source contracts cover blog single pages and article-card compatibility
  surfaces with `chirp-theme-blog-article` and `chirpui-resource-card`
  without active `.blog-post` roots;
- built HTML references emitted assets only.

## Ranked Waves

| Wave | Status | Required Proof / Residual |
|---|---|---|
| 1. Taxonomy and Archive Listings | Shipped | Tag pages and dogfood docs prove `chirpui-resource-card`, `chirpui-badge`, and retained pagination/navigation. Dedicated author/category/archive fixtures are still residual before moving this plan to done. |
| 2. Learning Content | Shipped | Source contracts require Chirp UI resource indexes, rendered content, stepper progress, and retained post cards while forbidding copied inline scripts and legacy learning card shells. |
| 3. Python and CLI Autodoc | Shipped | Source contracts require resource indexes, parameter tables, accordions, code blocks, badges, shared reference classes, and no copied default autodoc table/card shells or inline scripts. |
| 4. OpenAPI and API Hubs | Shipped | Source contracts require resource indexes, nav trees, parameter tables, accordions, sticky request/response examples, code blocks, shared reference aliases, and contained large schemas/code samples. |
| 5. Shortcodes and Media Embeds | Shipped | Source contracts require Chirp UI callout, accordion, card, gallery, and code classes while preserving Bengal link semantics and escaping. |
| 6. Root Aliases and Utility Pages | Shipped | Generic section, blog shell, page heroes, surfaces, rendered content, badges, and cards replace copied blog about/contact classes and inline scripts. |

## Not Now

- Copying default-theme autodoc, OpenAPI, or shortcode templates as-is.
- Adding new Chirp UI components before proving existing primitives cannot
  express the output.
- Reintroducing private `--chirp-theme-*` tokens or dormant copied CSS for
  future verticals.
- Treating route-backed reference navigation as ARIA tabs.

## Steward Notes

- Documentation steward: this plan is active roadmap memory; shipped surfaces
  stay documented in `docs/theming/chirp-theme.md` and
  `docs/theming/chirp-theme-parity-matrix.md`.
- Planning steward: each wave should land as its own PR or commit series with
  fixture proof and updated parity matrix status.
- Theme steward: prefer Chirp UI macros and token hooks; if a missing primitive
  is discovered, record the component contract before adding theme CSS.
