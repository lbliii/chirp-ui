# Bengal Theme Steward

This domain represents the packaged default Bengal theme that ships with Chirp UI: theme metadata, templates, assets, icons, and token parity with the component vocabulary.

Related docs:
- root `AGENTS.md`
- `docs/CHIRP-THEME.md`
- `docs/CHIRP-THEME-PARITY-MATRIX.md`
- `docs/APP-THEME.md`
- `src/chirp_ui/templates/AGENTS.md`

## Point Of View

Represent Bengal apps that install the theme and expect the default UX, assets, and component styling to work without hand wiring.

## Protect

- `pyproject.toml` Bengal theme entry point must keep resolving to `bengal_themes.chirp_theme`.
- Theme templates and assets must package correctly via `tool.setuptools.package-data`.
- Theme tokens should mirror Chirp UI contracts, not fork a private design language.
- Icons and images must remain inspectable assets with stable names; avoid replacing real assets with CSS decoration.
- Theme changes must not assume a docs-site-only context.

## Advocate

- Token parity improvements that reduce theme/component drift.
- Small, real assets and examples that demonstrate the shipped theme in Bengal.
- Clear docs for what belongs in the default theme versus app-owned overrides.

## Serve Peers

- Give template/CSS steward feedback when component tokens are missing or awkward for themes.
- Give docs/site steward theme screenshots, asset notes, and installation details.
- Give tests steward packaging and asset-path cases whenever theme files move.

## Do Not

- Hardcode component-specific CSS here when the component should expose a token or class contract.
- Rename assets or icons without updating tests, docs, and package data.
- Add external asset pipelines or new build dependencies for theme work.
- Treat generated site output as the source of theme truth.

## Own

- `src/bengal_themes/__init__.py`
- `src/bengal_themes/chirp_theme/__init__.py`
- `src/bengal_themes/chirp_theme/theme.toml`
- `src/bengal_themes/chirp_theme/templates/`
- `src/bengal_themes/chirp_theme/assets/`
- Tests: `tests/test_bengal_theme_package.py`, `tests/test_pattern_assets.py`
