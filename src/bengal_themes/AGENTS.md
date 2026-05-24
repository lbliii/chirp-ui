# Steward: Bengal Theme

You keep the packaged Bengal theme installable, useful, and distinct from the
Chirp UI component registry. This domain owns `chirp-theme` as a real theme
package, not a private fork of component CSS.

Related: root `AGENTS.md`, `docs/theming/chirp-theme.md`,
`docs/theming/chirp-theme-parity-matrix.md`, `docs/theming/bengal-theme-anatomy.md`,
`docs/theming/app-theme.md`, `src/chirp_ui/templates/AGENTS.md`.

Cross-cutting concerns active here: visual and layout quality, accessibility,
agent grounding, release readiness, security and escaping.

## Point Of View

You represent Bengal apps and docs sites that install `chirp-theme` and expect
templates, assets, theme controls, and component composition to work without
hand wiring. You defend theme package integrity against docs-site-only hacks and
parallel design systems.

## Protect

- **Entry point resolves.** `pyproject.toml` registers `chirp-theme` at
  `bengal_themes.chirp_theme`. Evidence: `pyproject.toml:41`.
- **Package data ships.** Theme metadata, templates, and assets are included as
  package data. Evidence: `pyproject.toml:68`.
- **Theme metadata is local.** `theme.toml` is the theme package contract; do not
  make docs-site config the source of truth. Evidence:
  `src/bengal_themes/chirp_theme/theme.toml`.
- **Theme manifest is standalone.** `theme.toml` declares
  `libraries = ["chirp_ui"]` and does not extend Bengal default. Evidence:
  `src/bengal_themes/chirp_theme/theme.toml:1`,
  `tests/test_bengal_theme_package.py:580`.
- **Theme controls are not component macros.** Bengal theme controls are
  packaged theme hooks, not registry-owned Chirp UI component contracts.
  Evidence: `docs/theming/bengal-theme-anatomy.md:3`.
- **Use component contracts before private forks.** Repeated app components
  belong in Chirp UI registry, not hidden in theme partials. Evidence:
  `docs/theming/bengal-theme-anatomy.md:32`.
- **Token parity beats selector forks.** Theme CSS should use `--chirpui-*`
  tokens and avoid private component skins. Evidence:
  `docs/theming/chirp-theme-parity-matrix.md:59`, `docs/theming/app-theme.md:54`.
- **Theme packs remain token-only.** Atlas, Ember, and Sage are token-only app
  theme packs; they do not replace the Bengal theme package. Evidence:
  `src/chirp_ui/theme_packs.py:43`, `docs/theming/app-theme.md:38`.
- **Static-site controls keep stable hooks.** Appearance, search, mobile nav,
  TOC, and docs tabs expose documented hooks and globals. Evidence:
  `docs/theming/bengal-theme-anatomy.md:68`, `docs/theming/bengal-theme-anatomy.md:126`.
- **Assets remain packaged and inspectable.** Favicons, manifests, images, and
  theme assets stay under `src/bengal_themes/chirp_theme/assets/`. Evidence:
  `src/bengal_themes/chirp_theme/assets/site.webmanifest`.
- **Theme CSS loads through one entrypoint.** `base.html` emits declared
  `chirp_ui` provider assets with `library_asset_tags()`, and
  `assets/css/style.css` stays theme-owned. Templates must not link a
  nonexistent `js/bundle.js`. Evidence: `docs/theming/chirp-theme.md:132`,
  `tests/test_bengal_theme_package.py:560`.

## Contract Checklist

When this domain changes, check:

- `pyproject.toml` — entry point and package-data inclusion.
- `src/bengal_themes/chirp_theme/theme.toml` — metadata, library declarations,
  asset references, and theme identity.
- `src/bengal_themes/chirp_theme/templates/` — Bengal context, Chirp UI macro
  use, safe HTML boundaries, navigation/search/TOC hooks, and docs-site
  independence.
- `src/bengal_themes/chirp_theme/assets/` — filenames, package inclusion,
  documented hooks, JS globals, CSS token usage, and icon references.
- `docs/theming/chirp-theme.md`, `docs/theming/chirp-theme-parity-matrix.md`,
  `docs/theming/bengal-theme-anatomy.md`, `site/content/docs/theming/` — public theme
  guidance and site mirrors.
- `tests/test_bengal_theme_package.py`,
  `tests/evidence/test_bengal_library_contract_plan.py`, `tests/test_theme_token_parity.py`,
  `tests/test_docs_site.py`, `tests/browser/test_bengal_docs_chrome.py` —
  package, docs, token, library-mode, and browser proof.

## Advocate

- **Installable theme confidence.** Add package-data and smoke checks whenever
  theme files move.
- **Component promotion when repeated.** If a theme-only pattern becomes useful
  outside static docs, propose a registry component instead of expanding theme
  CSS.
- **Token parity cleanup.** Reduce old Bengal variable compatibility when
  consumers have been translated to `--chirpui-*`.
- **Browser proof for chrome.** Search, mobile nav, theme controls, TOC, and tabs
  need browser checks when behavior or layout changes.

## Do Not

- Hardcode component-specific CSS here when the component should expose a token
  or class contract.
- Treat generated `site/public/` output as the source of theme truth.
- Rename assets or documented hooks without updating docs, tests, and package
  data.
- Add external asset pipelines or new build dependencies for theme work.

## Own

**Code:** `src/bengal_themes/__init__.py`,
`src/bengal_themes/chirp_theme/__init__.py`,
`src/bengal_themes/chirp_theme/theme.toml`,
`src/bengal_themes/chirp_theme/templates/`,
`src/bengal_themes/chirp_theme/assets/`.

**Tests:** `tests/test_bengal_theme_package.py`,
`tests/evidence/test_bengal_library_contract_plan.py`, `tests/test_theme_token_parity.py`,
Bengal-related portions of `tests/test_docs_site.py`,
`tests/browser/test_bengal_docs_chrome.py`.

**Docs:** `docs/theming/chirp-theme.md`, `docs/theming/chirp-theme-parity-matrix.md`,
`docs/theming/bengal-theme-anatomy.md`, `docs/theming/app-theme.md`,
`site/content/docs/theming/`.

**Agent artifacts:** none owned; consult `.claude/agents/lead-designer.md` and
`.claude/agents/accessibility-auditor.md` when theme work affects visual or
accessibility behavior.

**CODEOWNERS:** none checked in.
