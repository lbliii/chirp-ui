# chirp-theme parity matrix

This document records the current `chirp-theme` migration stance against Bengal
default. The long-term goal is full output parity with Bengal default's content
types, but not implementation parity with its copied templates and CSS. The goal
is a cleaner, installable theme package that translates useful default theme
ideas into `chirp-ui` macros and `--chirpui-*` tokens, with explicit deferrals
for niche or legacy-heavy verticals while they are redesigned.

## Classification labels

- `foundation`: required for the shell/docs/page experience and the first dogfood slice
- `core-parity`: retained high-value surfaces for content-heavy sites
- `future-parity`: required for eventual default-theme parity, but redesigned
  instead of copied forward
- `deferred`: intentionally not migrated in the current slice

## Theme surface

| Family | Bengal default references | chirp-theme status | Notes |
|---|---|---|---|
| Shell and shared runtime | `templates/base.html`, shared JS/CSS entrypoints | `foundation` | Keep Bengal metadata/runtime hooks, replace structural shell composition with theme-owned primitives. |
| Canonical pages | `home.html`, `page.html`, `doc/home.html`, `doc/list.html`, `doc/single.html` | `foundation` | These are the acceptance target for the dogfood docs site; new repeated UI should come from `chirpui/*` macros. |
| Markdown directives | `admonition`, `cards`, `card`, `child-cards` directive output | `foundation` | Bengal provides structured directive context; `chirp-theme` supplies Kida directive templates that emit Chirp UI callout/grid/card markup. |
| Shell partials | `partials/navigation-components.html`, `partials/docs-nav.html`, `partials/docs-toc-sidebar.html`, `partials/page-hero.html`, `partials/theme-controls.html`, `partials/search-modal.html` | `foundation` | Rewritten or re-scoped to use `chirp-ui` primitives before adding theme-specific markup. |
| Blog shell and posts | `blog/shell.html`, `blog/list.html`, `blog/single.html`, `post.html` | `core-parity` | Retained as the primary non-docs content vertical. |
| Search and errors | `search.html`, `404.html` | `core-parity` | Retained because they are part of the basic site UX contract. |
| Shared post/list components | `partials/components/post-card.html`, `article.html`, `related-posts-simple.html`, `tags.html`, `tiles.html` | `core-parity` | Reused by docs, generic pages, and blog surfaces. |
| Taxonomy, archive, authors | `tag.html`, `tags.html`, `archive*.html`, `author*.html`, `category-browser.html` | `core-parity` | Rebuilt on retained post/list/resource primitives and Chirp UI resource-index/card patterns instead of copied default-theme verticals. |
| Tracks, tutorial, notebook, changelog, resume | `tracks/`, `tutorial/`, `notebook/`, `changelog/`, `resume/` | `core-parity` | Re-expressed as Chirp UI learning/content systems using resource indexes, stepper progress, rendered content, and retained post/resource cards. |
| Autodoc and reference trees | `autodoc/`, `api-reference/`, `cli-reference/`, `openapi-reference/`, `api-hub/` | `future-parity` | Required long-term, but needs a dedicated reference-surface redesign with Chirp UI navigation, tables, signatures, and search patterns. |
| Shortcodes and embeds | `shortcodes/` | `core-parity` | Mapped onto Chirp UI callouts, accordion/details, card-backed media/figure embeds, code blocks, and safe link primitives. |
| Niche graph/data-table/experimental UI | graph/minimap/data-table/holo families | `deferred` | Keep only capabilities that still map to an actual output contract; redesign through Chirp UI when they are promoted. |

## Chirp UI Translation Rules

- Prefer `chirpui/*` macros for cards, buttons, layout primitives, page heroes,
  nav, footer, and repeated content structures.
- Tune visual identity through `--chirpui-*` tokens. Do not introduce new
  `--chirp-theme-*` tokens.
- Legacy `--color-*`, `--radius-*`, and `--font-family-*` aliases are
  temporary compatibility for copied Bengal CSS. New CSS should read from
  `--chirpui-*` directly.
- If a copied default-theme pattern needs component-specific CSS, first ask
  whether the missing hook belongs in the Chirp UI component registry.
- If a Markdown directive maps to an existing Chirp UI primitive, prefer a Kida
  directive template over CSS that restyles legacy directive classes.

## Asset graph decisions

### Keep

- the `chirp_ui` provider library declaration in `theme.toml`
- token overrides in `chirp-theme.css` using `--chirpui-*`
- token and reset layers only while copied default-theme CSS still needs them
- layout and component CSS needed by the retained shell/docs/page/blog/search/404 surfaces
- theme appearance/search/versioning/runtime JS under `assets/js/core/`
- docs navigation, TOC, mobile navigation, link previews, and selective lazy loaders

### Collapse

- overlapping layout families that only existed to preserve default-theme parity
- duplicated page-family CSS once the canonical templates are moved to the primitive layer
- shell markup embedded directly in `base.html`
- old Bengal CSS variables once their copied consumers are translated to
  `--chirpui-*`

### Remove from the copied baseline

- tracks/tutorial/notebook/resume/changelog-specific CSS imports
- reference/autodoc/API-hub CSS and JS
- unused graph minimap and data-table wiring
- experimental holographic/demo CSS

Removing copied baseline files does not remove these content types from the
long-term contract. It means `chirp-theme` should reintroduce them through
Chirp UI-native templates, directive contexts, registry-backed components, and
tokenized CSS when that vertical is actively rebuilt.

## Acceptance gates

The current retained contract is:

- packaged `chirp-theme` entry point and resource resolution
- `theme.toml` declares `libraries = ["chirp_ui"]`
- canonical templates: `base.html`, `home.html`, `page.html`, `doc/home.html`, `doc/list.html`, `doc/single.html`
- retained core templates: `blog/shell.html`, `blog/list.html`, `blog/single.html`, `post.html`, `search.html`, `404.html`
- taxonomy/archive/author templates: `tag.html`, `tags.html`, `archive.html`,
  `archive-year.html`, `author.html`, `authors/list.html`,
  `authors/single.html`, `category-browser.html`
- learning/content templates: `tracks/list.html`, `tracks/single.html`,
  `tutorial/list.html`, `tutorial/single.html`, `notebook/single.html`,
  `changelog/list.html`, `changelog/single.html`, `resume/list.html`,
  `resume/single.html`
- shortcode templates: `tip`, `warning`, `danger`, `details`, `figure`,
  `img`, `audio`, `gallery`, `highlight`, `blockquote`, `param`, `ref`,
  `relref`
- docs dogfood site builds using only emitted packaged assets
- Bengal can resolve `chirpui/*` templates through the theme library provider
- Bengal card directives render through `templates/directives/` into
  `chirpui-grid` and `chirpui-card` markup on the dogfood docs site
- Bengal admonition directives render through `templates/directives/` into
  `chirpui-callout` markup
- the old default-theme `components/cards.css` bundle is not part of the
  retained theme asset graph; card-shaped UI should come from Chirp UI macros
  or scoped retained vertical CSS
- every shipped CSS file under `assets/css/` is reachable from
  `assets/css/style.css`; future-parity CSS should not ship as dormant copied
  baseline baggage
- theme CSS contains no `--chirp-theme-*` private token vocabulary
- `chirp-theme.css` and `style.css` continue to parse cleanly

Anything not listed above is intentionally outside the current retained runtime
contract until a later migration slice expands the supported surface with a
Chirp UI-native design.
