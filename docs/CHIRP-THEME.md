# chirp-theme

`chirp-theme` is the packaged Bengal theme that now ships from the `chirp-ui`
project. The theme is intentionally **static-first** and keeps v1 self-contained.

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

## Why v1 Is Self-Contained

Today Bengal's template integration builds a `FileSystemLoader` from theme
directories only. That means an installed Bengal theme can resolve templates
from:

- site `themes/<name>/templates/`
- installed theme package `templates/`
- bundled Bengal theme `templates/`

But it cannot yet import templates from another installed package such as
`chirp_ui`.

Because of that, `chirp-theme` v1:

- extends Bengal `default`
- ships its own theme templates
- keeps the override surface small
- avoids any special-case runtime coupling to `chirp_ui`

## Future Loader Bridge

The next architectural step is a Bengal loader bridge that would let a packaged
theme consume `chirp_ui` templates directly.

Desired end state:

1. Bengal theme templates can include or import package-provided templates.
2. `chirp-theme` becomes a thinner composition layer over `chirp_ui`.
3. Template duplication between the theme package and `chirp_ui` shrinks.

Expected Bengal work:

1. Extend template loader construction so a theme can register package template roots.
2. Preserve current theme precedence rules for site, installed theme, and bundled theme overrides.
3. Keep the fallback story deterministic so `extends` and `include` still resolve predictably.

Until that bridge exists, prefer adding theme behavior in:

- `assets/css/chirp-theme.css`
- a small number of theme-owned template overrides

Avoid copying large sections of `chirp_ui` templates unless there is no simpler
static-first option.
