# Chirp UI Pre-1.0 Gap Roadmap

Status: active roadmap
Date: 2026-05-12

This roadmap turns the Skeleton-inspired design-system review into executable
work. The goal is not to copy Skeleton's Tailwind/Svelte architecture. The goal
is to make Chirp UI feel as inspectable, themeable, and visually convincing
while preserving its Python-native registry contract.

## Current Position

Chirp UI already has the hard architectural pieces in place:

- a registry-backed component vocabulary,
- a shipped `chirpui-manifest@5` with params, slots, emitted classes, tokens,
  maturity, runtime requirements, and authoring hints,
- generated CSS partials with registry parity checks,
- public cascade layers and token-first app overrides,
- HTMX and Alpine interaction contracts,
- dense navigation recipes,
- a Bengal/chirp-theme integration path,
- broad render, JS, browser, and contract coverage.

The remaining work is mostly about making that quality obvious, reducing stale
planning noise, and stabilizing the public surface before 1.0.

## Workstreams

### 1. Verification Reliability

Goal: every maintainer and agent can regenerate and verify the system from a
fresh checkout.

Tasks:

- Fix local `uv run` / cache setup issues so `poe build-manifest-check`,
  `poe build-css-check`, `poe build-docs-check`, and release preflight are
  reliable.
- Add a short troubleshooting note for the Kida API mismatch failure mode:
  system `python -m chirp_ui.manifest --json` can import the wrong installed
  Kida, while `uv run` should use the locked environment.
- Keep `src/chirp_ui/manifest.json`, `src/chirp_ui/templates/chirpui.css`, and
  generated docs in the release-preflight drift gate.

Acceptance:

- `uv run poe build-manifest-check` passes from a clean checkout.
- `uv run poe build-css-check` passes from a clean checkout.
- `uv run poe build-docs-check` passes from a clean checkout.
- The docs name the preferred command path and the known failure mode.

### 2. Roadmap Hygiene

Goal: active plans describe real remaining work, not shipped history.

Tasks:

- Move plans that are fully shipped to `docs/plans/done/`.
- Rewrite partially shipped plans as residual backlogs.
- Keep this file as the current top-level planning map.
- Link every active plan to one of these workstreams.

Acceptance:

- `docs/INDEX.md` lists only genuinely active plans under in-flight work.
- Shipped plans do not contain unqualified `Status: active` or `Status: draft`
  language.
- Each remaining active plan has a "Residual Work" or "Next Slice" section.

### 3. Visible Design-System Showcase

Goal: make Chirp UI's quality visible, not just verifiable.

Tasks:

- Maintain a static visual audit page that can be opened without a server.
- Show token palettes, theme modes, component states, dense navigation,
  forms, feedback, marketing patterns, ASCII/TUI primitives, and responsive
  stress cases in one place.
- Add a screenshot checklist for desktop, tablet, and phone widths.
- Use the page as the first stop before promoting experimental components.

Acceptance:

- `examples/design-system-gap-showcase/index.html` renders with packaged CSS.
- The page exercises light/dark token contrast, dense chrome, long labels,
  loading/reserved badges, and nested surfaces.
- The page contains no inline copy explaining how to use the library; it is a
  visual audit surface, not a landing page.

### 4. Theme Authoring UX

Goal: make token-driven theming feel obvious and powerful.

Tasks:

- Add a theme preset gallery covering default, app starter, holy-light, and
  chirp-theme token profiles.
- Add a token explorer that groups color, typography, radius, elevation,
  spacing, and motion tokens by job.
- Document which tokens app authors should override first.
- Keep theme customization token-first; component selectors belong in
  `@layer app.overrides` only when a token hook is insufficient.

Acceptance:

- A user can compare theme presets visually without reading token tables first.
- `docs/TOKENS.md` and `docs/APP-THEME.md` link to the visual gallery.
- No new private `--chirp-theme-*` token vocabulary appears.

### 5. Dense Navigation Productization

Goal: turn the dense navigation study into a teachable product surface.

Tasks:

- Publish a focused dense navigation recipes guide.
- Keep product-specific shells as recipes until repeated real app usage proves
  a macro should exist.
- Add browser proof for `scope_switcher` and `saved_view_strip` only if their
  overflow or layout behavior becomes more ambitious.
- Revisit `workspace_shell` after real app usage, not from showcase examples
  alone.

Acceptance:

- The guide explains scope, command jump, broad nav, object context, local
  route views, page tools, and attention states as separate layers.
- Recipes cite existing components first.
- Any new macro proposal answers the acceptance rule in
  `docs/DENSE-NAVIGATION-SYNTHESIS.md`.

### 6. CSS Scope Hardening

Goal: reduce style bleed as a normal maintenance practice.

Tasks:

- Continue converting touched component partials to the `@layer` + `@scope`
  envelope.
- Prioritize components that nest, hover, or use contextual selectors: forms,
  buttons, nav, lists, badges, tables, panels, and grouped controls.
- Add a browser or computed-style proof when a conversion changes behavior.

Acceptance:

- New components use scoped partials by default.
- Each conversion keeps registry emits parity green.
- Nested component bleed fixes are covered by targeted browser tests.

### 7. Public Surface Stabilization

Goal: make the pre-1.0 API feel intentional.

Tasks:

- Review experimental components and classify them as promote, keep
  experimental, recipe-only, or deprecate later.
- Record decisions in `docs/PUBLIC-SURFACE-STABILIZATION.md`.
- Review legacy helpers and prevent utility-class vocabulary growth.
- Keep the completed legacy-helper cleanup plan archived under
  `docs/plans/done/PLAN-legacy-helper-cleanup-pre-1.0.md`, and use its proof
  when deciding future keep/deprecate outcomes.
- Keep `find --authoring` and manifest authoring hints aligned with docs.

Acceptance:

- Every experimental public component has a 1.0 disposition.
- Every legacy helper has an explicit keep/deprecate-later decision.
- Generated docs and manifest agree about preferred versus compatibility
  authoring paths.

### 8. Bengal And chirp-theme Integration

Goal: make Chirp UI a first-class Bengal library without theme-local asset
plumbing.

Tasks:

- Finish Bengal library asset modes: `bundle`, `link`, and `none`.
- Register Chirp UI template/macros/runtime helpers from Bengal library
  declarations.
- Remove transitional filesystem-relative theme imports after Bengal owns the
  asset contract.
- Keep chirp-theme output parity moving through Chirp UI-native templates and
  tokens.

Acceptance:

- A Bengal theme with `libraries = ["chirp_ui"]` can import Chirp UI macros
  and emit required assets without manual path knowledge.
- Static and dev outputs resolve the same logical asset contract.
- `chirp-theme` CSS contains only theme tokens, content polish, and actively
  referenced vertical styles.

## Sequencing

1. Keep verification reliability wired into local and hosted CI gates.
2. Publish and maintain the theme gallery.
3. Use dense navigation recipes and visual audit proof before promoting new
   composites.
4. Use the visual audit page to drive experimental component stabilization.
5. Continue CSS scope conversion and Bengal integration in parallel with
   feature work.

## Decision Rule

Before adding a new public component, ask:

- Does an existing primitive composition fail in a repeated, documented way?
- Is the missing behavior visible in the visual audit or a real consuming app?
- Can the registry, manifest, docs, CSS, and tests describe it together?
- Does it preserve Chirp UI as a Python vocabulary rather than a utility-class
  vocabulary?

If the answer is not concrete, keep the pattern as a recipe.
