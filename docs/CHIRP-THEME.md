# chirp-theme

`chirp-theme` is the packaged Bengal theme that ships from the `chirp-ui`
project. It is intended to become a fully owned, comprehensive alternative to
Bengal's original default theme: a cleaner, more modern static-site shell built
with current Kida patterns, stronger component discipline, and a design system
that can eventually reach parity with Bengal default v1 and then move past it.

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
2. A better-organized replacement for the original Bengal default theme
3. A translation of the original default-theme ideas into `chirp-ui` components,
   slots, and `--chirpui-*` tokens
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

## Supported Surface

The retained `chirp-theme` contract is intentionally explicit:

- canonical shell/docs/pages: `base.html`, `home.html`, `page.html`, `doc/home.html`, `doc/list.html`, `doc/single.html`
- retained core parity: `blog/shell.html`, `blog/list.html`, `blog/single.html`, `post.html`, `search.html`, and `404.html`
- shared shell partials and components that support those templates

The current parity and redesign decisions live in
[`docs/CHIRP-THEME-PARITY-MATRIX.md`](./CHIRP-THEME-PARITY-MATRIX.md).
The active implementation backlog for unported content families lives in
[`docs/plans/PLAN-chirp-theme-content-parity.md`](./plans/PLAN-chirp-theme-content-parity.md).
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
from `chirp_ui.static_path()`. Bengal palette controls should either map to
those pack names or be documented as transitional aliases until the retained
default-theme palette surface is removed.

Current Bengal palette controls are transitional `data-palette` aliases. The
menu exposes `data-theme-pack` metadata so tools and future UI can line them up
with the curated pack vocabulary without treating the old names as new Chirp UI
theme packs:

| Bengal palette | Forward theme-pack family | Status |
|---|---|---|
| Default | `ember` | Transitional alias for the current warm editorial package identity |
| `snow-lynx` | `sage` | Transitional alias; soft low-glare palette |
| `brown-bengal` | `ember` | Transitional alias; warm editorial palette |
| `silver-bengal` | `atlas` | Transitional alias; cool operational neutral palette |
| `charcoal-bengal` | `ember` | Transitional alias; warm dark editorial palette |
| `blue-bengal` | `atlas` | Transitional alias; cool operational blue palette |

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

The current CSS loading contract is a transitional boundary, not the final
architecture. Until Bengal has first-class library asset modes with matching dev
and static-build behavior, `assets/css/style.css` is the single stylesheet
entrypoint and imports Chirp UI's generated CSS and transition CSS before theme
tokens and overrides. Theme templates should not add separate
`chirp_ui/chirpui.css` or `chirp_ui/chirpui-transitions.css` links. The desired
platform contract is tracked in
[`docs/plans/PLAN-bengal-chirpui-library-contract.md`](./plans/PLAN-bengal-chirpui-library-contract.md).

The theme should eventually cover the same broad content/output families as the
original Bengal default theme: autodoc and reference pages, tutorials, tracks,
notebooks, changelog and resume views, taxonomy/archive/author pages, search,
errors, and content-heavy pages. The migration should not copy those verticals
forward as-is. It should rebuild them as Chirp UI-native contracts when each
surface is promoted.

## Near-Term Execution

The current cutover work focuses on making the theme truly standalone while
shrinking the copied default-theme surface:

- remove implicit dependence on Bengal default theme inheritance
- declare `chirp_ui` as a Bengal theme library dependency
- load Chirp UI JS through Bengal's provider asset system
- bundle Chirp UI CSS through the theme stylesheet until Bengal supports
  first-class library CSS inclusion modes
- replace default-theme partial dependencies with `chirpui/*` macros where a
  registry-backed component already exists
- render high-value Markdown directives through Kida directive templates when a
  Chirp UI component or primitive is the correct output contract
- ensure generated output only references assets shipped by the theme package

That standalone baseline is the platform for future parity and beyond. The next
phase is no longer “copy every legacy family forward”; it is “translate and
improve every original theme output using Chirp UI as the primitive layer.”
