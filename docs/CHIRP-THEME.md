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

`chirp-theme` is not meant to be a thin skin on Bengal default.

The long-term goal is:

1. A real standalone Bengal theme package fully supported by `chirp-ui`
2. A better-organized replacement for the original Bengal default theme
3. A theme that uses modern `chirp-ui`, Kida, and Alpine-friendly patterns as
   the foundation for a future Bengal default v2

That means the package should own:

- its shell templates
- its partials/macros
- its stylesheet entrypoint
- its icons, JS, fonts, favicons, and other referenced assets

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

The goal is not runtime indirection through `chirp_ui` template imports. The
goal is a strong, installable Bengal theme package whose implementation happens
to be owned and evolved by the `chirp-ui` project.

## Near-Term Execution

The current cutover work focuses on making the theme truly standalone:

- remove implicit dependence on Bengal default theme inheritance
- give the theme a real Bengal-supported `assets/css/style.css` entrypoint
- replace hidden default-theme partial dependencies with theme-owned resources
- ensure generated output only references assets shipped by the theme package

That standalone baseline is the platform for future parity and beyond.
