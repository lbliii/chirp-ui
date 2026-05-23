# chirp-theme

`chirp-theme` is the packaged Bengal theme that ships from the `chirp-ui`
project. It is a fully bespoke Bengal theme, not a Bengal default-theme skin or
parity fork. Its implementation language is Chirp UI macros, `--chirpui-*`
tokens, current Kida patterns, and narrowly scoped theme CSS.

## Package Layout

Theme resources live under:

- `src/bengal_themes/chirp_theme/theme.toml`
- `src/bengal_themes/chirp_theme/templates/`
- `src/bengal_themes/chirp_theme/assets/`

`pyproject.toml` registers the package through the `bengal.themes`
entry-point group:

```toml
[project.entry-points."bengal.themes"]
chirp-theme = "bengal_themes.chirp_theme"
```

## Product Direction

`chirp-theme` is not meant to be a thin skin on Bengal default, and it should
not grow a private design system beside `chirp-ui`.

The long-term goal is:

1. A real standalone Bengal theme package fully supported by `chirp-ui`
2. A better-organized custom theme that can replace default-theme usage without
   copying default-theme architecture
3. A translation of useful default-theme ideas into `chirp-ui` components,
   slots, and `--chirpui-*` tokens, only when those ideas still serve the custom
   product direction
4. A theme that uses modern `chirp-ui`, Kida, and Alpine-friendly patterns as
   the foundation for a future Bengal default v2

The current standalone cutover started as an ownership cutover: the package
carried forward a large default-theme asset/partial surface so the docs site
could dogfood a packaged Bengal theme immediately. That is a transitional
blueprint, not the target architecture. Each migration slice should ask what
the copied default-theme pattern was trying to do, then re-express the useful
parts with `chirp-ui` primitives and tokens.

That means the package should own:

- its shell templates
- its partials/macros
- its stylesheet entrypoint
- its icons, JS, fonts, favicons, and other referenced assets

Current article surfaces use the app-shell frame as the persistent page model:
docs pages, generic pages, blog posts/lists, and section indexes keep the left
catalog chrome in place while only the route-owned article or list content
changes in the main panel. The outer catalog rail is symbol-first, with
hover/focus labels for titles, so the shell reads like application chrome
rather than another text navigation column. The inner rail is a contextual
workbench for the active article family: it carries a section identity card,
article-set metadata, typed navigation rows, and active branch styling. The
right TOC rail is the matching page map for the current article, preserving
scroll progress and in-page anchors while using the same compact card, mark,
and active-row language. Back-to-top is likewise treated as shell chrome: it
appears as a right-rail action when the TOC rail exists, with the old floating
control kept only as a fallback for pages without that rail.

## Supported Surface

The retained `chirp-theme` contract is intentionally explicit:

- canonical shell/docs/pages: `base.html`, `home.html`, `page.html`, `doc/home.html`, `doc/list.html`, `doc/single.html`
- retained core parity: `blog/shell.html`, `blog/list.html`, `blog/single.html`, `post.html`, `search.html`, and `404.html`
- taxonomy/archive/author pages, learning/content pages, autodoc/API reference
  pages, shortcodes, embeds, root aliases, and utility pages listed in the
  parity matrix acceptance gates
- shared shell partials and components that support those templates

The current parity and redesign decisions live in
[`docs/CHIRP-THEME-PARITY-MATRIX.md`](./CHIRP-THEME-PARITY-MATRIX.md).
The active implementation backlog for unported content families lives in
[`docs/plans/PLAN-chirp-theme-content-parity.md`](./plans/PLAN-chirp-theme-content-parity.md).
The visual token comparison for `chirp-theme` lives in
`examples/design-system-gap-showcase/index.html`; use it alongside
[`docs/VISUAL-AUDIT-SHOWCASE.md`](./VISUAL-AUDIT-SHOWCASE.md) before promoting
theme-level token changes.
Anything not listed there as retained is intentionally outside the current
runtime contract until a later redesign slice brings it back through Chirp
UI-native templates and tokens.

## Design Principles

`chirp-theme` should optimize for:

- docs sites
- product and marketing pages
- content-heavy static sites
- modern composable template patterns
- clearer separation between structure, behavior, and styling

It should avoid carrying forward historical baggage from Bengal default when a
cleaner `chirp-ui`-driven pattern exists.

## Relationship To `chirp-ui`

The theme is shipped inside the `chirp-ui` repo because it is part of the same
design-system effort. The docs site dogfoods the package directly, so the theme
is exercised on a real Bengal site rather than living as an isolated demo.

The theme should treat `chirp-ui` as a real library, not as an optional CSS file
to adapt after the fact. New templates should prefer `chirpui/*` macros for
cards, buttons, layout primitives, site chrome, navigation, and repeated
content patterns. Theme CSS should tune `--chirpui-*` tokens first. Bengal
legacy variables such as `--color-*` may remain temporarily only to support
copied default-theme CSS while that CSS is deleted or translated.

The curated app theme packs (`atlas`, `ember`, and `sage`) do not replace the
Bengal `chirp-theme` package. They are token-only Chirp UI resources exposed
from `chirp_ui.static_path()`. The Bengal `chirp-theme` menu no longer exposes
the old `data-palette` aliases or `data-theme-pack` metadata; it is an
appearance-only control while the bespoke theme rewrite owns its color identity
through shipped tokens. Future palette or theme-pack selection should use a new
Chirp UI-owned contract rather than resurrecting the old Bengal palette names.

The direction of dependency matters:

- preferred: `chirp-theme` sets `--chirpui-*` tokens and composes `chirpui/*`
  macros
- preferred for Markdown directives: Bengal handlers expose structured context
  and `chirp-theme` owns `templates/directives/*.html` so directive output is
  Chirp UI markup, not copied default-theme markup
- acceptable transitional step: copied Bengal CSS aliases old variables to
  `--chirpui-*` tokens while the owning template is converted
- not acceptable for new work: creating `--chirp-theme-*` or component-specific
  theme classes when a Chirp UI token, primitive, or macro should own the
  contract

The current CSS loading contract is a transitional boundary, not the theme
architecture. Until Bengal has first-class library asset modes with matching dev
and static-build behavior, `assets/css/style.css` is the single stylesheet
entrypoint and imports Chirp UI's generated CSS and transition CSS before theme
tokens and overrides. That shim must stay isolated while templates, layout, and
content surfaces continue moving to the bespoke Chirp UI implementation. Theme
templates should not add separate
`chirp_ui/chirpui.css` or `chirp_ui/chirpui-transitions.css` links. The desired
platform contract is for Bengal to expose `bundle`, `link`, and `none` modes
from the library declaration; that contract is tracked in
[`docs/plans/PLAN-bengal-chirpui-library-contract.md`](./plans/PLAN-bengal-chirpui-library-contract.md).

The JavaScript loading contract is similarly explicit. `chirp-theme` currently
loads individual packaged scripts from `assets/js/`; it does not advertise a
generated `js/bundle.js` path because no bundle artifact is produced by this
package. Share and LLM-copy controls depend on
`assets/js/enhancements/action-bar.js`, so templates that emit
`data-action="copy-url"` or `data-action="copy-llm-txt"` must keep that script
in the base script list.

The theme should eventually cover the same broad content/output families users
expect from Bengal: autodoc and reference pages, tutorials, tracks, notebooks,
changelog and resume views, taxonomy/archive/author pages, search, errors, and
content-heavy pages. The goal is not default-theme parity. Treat the default
theme as input when useful, then rebuild each promoted surface as a custom
Chirp UI-native contract.

## Near-Term Execution

The current wave focuses on making the theme visibly standalone while shrinking
the copied default-theme surface:

- route the desktop shell through Chirp UI navbar/footer macros
- keep mobile navigation, search modal, and theme controls theme-owned until
  they are deliberately promoted or replaced
- keep `chirp_ui` declared as a Bengal theme library dependency
- load Chirp UI JS through Bengal's provider asset system
- bundle Chirp UI CSS through the theme stylesheet until Bengal supports
  first-class library CSS inclusion modes
- replace default-theme partial dependencies with `chirpui/*` macros where a
  registry-backed component already exists
- render high-value Markdown directives through Kida directive templates when a
  Chirp UI component or primitive is the correct output contract
- ensure generated output only references assets shipped by the theme package

That standalone baseline is the platform for the bespoke rewrite. The next
phase is no longer “copy every legacy family forward”; it is “design and
implement each promoted theme surface using Chirp UI as the primitive layer.”
