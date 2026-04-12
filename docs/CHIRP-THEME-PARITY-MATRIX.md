# chirp-theme parity matrix

This document records the current `chirp-theme` migration stance against Bengal
default. The goal is not blanket parity with every historical template family.
The goal is a cleaner, installable theme package with a clearly retained core
surface and explicit deferrals for niche or legacy-heavy verticals.

## Classification labels

- `foundation`: required for the shell/docs/page experience and the first dogfood slice
- `core-parity`: retained high-value surfaces for content-heavy sites
- `deferred`: intentionally not migrated in the current slice
- `pruned`: omitted until there is a concrete need to restore them

## Theme surface

| Family | Bengal default references | chirp-theme status | Notes |
|---|---|---|---|
| Shell and shared runtime | `templates/base.html`, shared JS/CSS entrypoints | `foundation` | Keep Bengal metadata/runtime hooks, replace structural shell composition with theme-owned primitives. |
| Canonical pages | `home.html`, `page.html`, `doc/home.html`, `doc/list.html`, `doc/single.html` | `foundation` | These are the acceptance target for the dogfood docs site. |
| Shell partials | `partials/navigation-components.html`, `partials/docs-nav.html`, `partials/docs-toc-sidebar.html`, `partials/page-hero.html`, `partials/theme-controls.html`, `partials/search-modal.html` | `foundation` | Rewritten or re-scoped to use theme-owned primitives. |
| Blog shell and posts | `blog/shell.html`, `blog/list.html`, `blog/single.html`, `post.html` | `core-parity` | Retained as the primary non-docs content vertical. |
| Search and errors | `search.html`, `404.html` | `core-parity` | Retained because they are part of the basic site UX contract. |
| Shared post/list components | `partials/components/post-card.html`, `article.html`, `related-posts-simple.html`, `tags.html`, `tiles.html` | `core-parity` | Reused by docs, generic pages, and blog surfaces. |
| Taxonomy, archive, authors | `tag.html`, `tags.html`, `archive*.html`, `author*.html`, `category-browser.html` | `deferred` | Only restore if retained post/list primitives prove they are still worthwhile. |
| Tracks, tutorial, notebook, changelog, resume | `tracks/`, `tutorial/`, `notebook/`, `changelog/`, `resume/` | `deferred` | These depend on older bespoke shells and can stay out of the first migration slice. |
| Autodoc and reference trees | `autodoc/`, `api-reference/`, `cli-reference/`, `openapi-reference/`, `api-hub/` | `pruned` | Not migrated until a dedicated reference-surface redesign exists. |
| Niche graph/data-table/experimental UI | graph/minimap/data-table/holo families | `pruned` | Keep only the contextual graph needed by docs TOC; everything else is optional baggage for later. |

## Asset graph decisions

### Keep

- token and reset layers under `assets/css/tokens/` and `assets/css/base/`
- layout and component CSS needed by the retained shell/docs/page/blog/search/404 surfaces
- theme appearance/search/versioning/runtime JS under `assets/js/core/`
- docs navigation, TOC, mobile navigation, link previews, and selective lazy loaders

### Collapse

- overlapping layout families that only existed to preserve default-theme parity
- duplicated page-family CSS once the canonical templates are moved to the primitive layer
- shell markup embedded directly in `base.html`

### Remove or defer

- tracks/tutorial/notebook/resume/changelog-specific CSS imports
- reference/autodoc/API-hub CSS and JS
- unused graph minimap and data-table wiring
- experimental holographic/demo CSS

## Acceptance gates

The current retained contract is:

- packaged `chirp-theme` entry point and resource resolution
- canonical templates: `base.html`, `home.html`, `page.html`, `doc/home.html`, `doc/list.html`, `doc/single.html`
- retained core templates: `blog/shell.html`, `blog/list.html`, `blog/single.html`, `post.html`, `search.html`, `404.html`
- docs dogfood site builds using only emitted packaged assets
- `chirp-theme.css` and `style.css` continue to parse cleanly

Anything not listed above is intentionally deferred or pruned until a later
migration slice expands the supported surface.
