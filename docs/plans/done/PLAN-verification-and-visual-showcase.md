# Verification And Visual Showcase Plan

Status: complete
Date: 2026-05-12
Depends on:

- [../ROADMAP-pre-1.0.md](../ROADMAP-pre-1.0.md)
- [../VISUAL-AUDIT-SHOWCASE.md](../VISUAL-AUDIT-SHOWCASE.md)
- [../DENSE-NAVIGATION-RECIPES.md](../DENSE-NAVIGATION-RECIPES.md)

## Goal

Tie release-quality verification to visible design-system proof. Chirp UI
already has the registry, generated CSS, manifest, tests, and theme contracts;
this plan makes those qualities inspectable before 1.0.

## Current Slice

Shipped in this slice:

- `docs/ROADMAP-pre-1.0.md` as the current gap-filling roadmap.
- `docs/VISUAL-AUDIT-SHOWCASE.md` as the operating instructions for visual QA.
- `docs/DENSE-NAVIGATION-RECIPES.md` as the focused dense navigation guide.
- `examples/design-system-gap-showcase/index.html` as a static visual audit
  page with token explorer, interaction chrome, ASCII/TUI controls, proof
  patterns, and theme profile gallery.
- `tests/test_visual_audit_showcase.py` and
  `tests/browser/test_visual_audit_showcase.py` as structural and browser proof
  for the no-server visual audit page.
- `uv run poe verify-generated` as the short generated-artifact verification
  task for CSS, manifest, and component reference docs.
- `docs/VERIFICATION.md` as the locked-environment verification and Kida
  mismatch troubleshooting note.
- Documentation index cleanup that moves shipped plans out of the active list.

## Sprint 1: Verification Repair

Tasks:

- Ensure the locked environment can run manifest, CSS, docs, and release
  preflight checks.
- Document the system-Python Kida mismatch failure mode and the preferred
  `uv run` path.
- Keep generated artifact drift checks fast enough for agents to run before
  publishing changes.

Acceptance:

- `uv run poe build-manifest-check` passes.
- `uv run poe build-css-check` passes.
- `uv run poe build-docs-check` passes.
- `uv run poe verify-generated` passes.
- The troubleshooting note names the failure and fix.

## Sprint 2: Visual Audit Proof

Tasks:

- Validate the static visual audit page at desktop, tablet, and phone widths.
- Add screenshots or browser tests only after the page stabilizes enough that
  image churn is low.
- Add any missing surfaces needed to judge the pre-1.0 public API: overlays,
  command palette, ASCII controls, marketing proof bands, and dense forms.

Acceptance:

- The page renders without missing CSS.
- Text does not escape controls at 320px.
- Dense navigation badges reserve space for visible, loading, and expected
  counts.
- Nested surfaces/cards preserve their own visual treatment.
- `tests/browser/test_visual_audit_showcase.py` proves the no-server page has
  no document-level horizontal overflow at phone, tablet, and desktop widths.
- The page includes command palette, modal, drawer, ASCII/TUI, logo cloud,
  story card, and CTA-band coverage.

## Sprint 3: Theme Gallery

Tasks:

- Add visual profiles for default, app-theme-starter, holy-light, and
  chirp-theme token sets.
- Group token samples by job: page, surface, text, accent, semantic state,
  focus, radius, elevation, and typography.
- Link the gallery from `TOKENS.md`, `APP-THEME.md`, and `CHIRP-THEME.md`.

Acceptance:

- A user can compare theme presets without reading the full token reference.
- Theme examples stay token-first.
- No new private theme token namespace is introduced.

## Sprint 4: Roadmap Cleanup

Tasks:

- Rewrite residual active plans around current remaining work.
- Keep shipped research and recipe studies in `docs/plans/done/`.
- Keep `ROADMAP-pre-1.0.md` as the one-page current map.

Acceptance:

- Active plans have concrete next slices.
- Shipped plans are not listed as active in `docs/INDEX.md`.
- Dense navigation residual work is represented by implementation plans, not
  broad research docs.

## Not Now

- Adding a new public shell macro from showcase evidence alone.
- Screenshot baselines before the visual audit page content stabilizes.
- Replacing component contract tests with screenshots.
- Adding Tailwind-style utility classes for showcase-only layout needs.

## Changelog

- 2026-05-12: Archived to `docs/plans/done/` after the verification docs,
  generated-artifact gate, visual audit page, dense navigation recipes, and
  roadmap cleanup landed. Remaining verification work is tracked by residual
  test/CI plans, not this shipped slice.
