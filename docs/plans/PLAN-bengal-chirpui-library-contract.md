# Bengal Chirp UI library contract

**Status:** Active  
**Owner:** chirp-theme / Bengal integration  
**Scope:** First-class Chirp UI consumption from Bengal themes without theme-local asset plumbing

## Context

`chirp-theme` is proving the right product direction: Bengal themes should be
able to think in Chirp UI components, tokens, macros, and runtime requirements
instead of adapting a copied default theme after the fact.

The migration also exposed the wrong kind of work. The theme has repeatedly had
to understand provider asset paths, fingerprinting, live reload behavior, and
whether Bengal serves library CSS at stable logical URLs. Those details are
platform responsibilities. A theme should declare that it uses `chirp_ui`; Bengal
should discover the package contract, make assets available consistently in dev
and static builds, register Kida/macros/filters, and fail before the browser sees
missing CSS or JS.

The immediate theme posture is intentionally conservative:

- `theme.toml` declares `libraries = ["chirp_ui"]`.
- `assets/css/style.css` is the single CSS entrypoint and imports Chirp UI CSS.
- `base.html` links the theme stylesheet and Chirp UI JS, not standalone provider
  CSS files.
- package tests reject HTML that references stale logical provider CSS paths.

That is a safe local contract, not the final Bengal abstraction.

## Target Contract

A Bengal theme should be able to declare library usage without knowing package
internals:

```toml
name = "chirp-theme"
libraries = ["chirp_ui"]
```

Bengal should then discover a library contract equivalent to:

| Contract | Expected behavior |
|---|---|
| Macro/templates | Add the package loader so `{% from "chirpui/card.html" import card %}` works. |
| CSS assets | Know the ordered CSS entries: `chirpui.css`, `chirpui-transitions.css`. |
| JS assets | Know the ordered JS entries: `chirpui.js`, optionally `chirpui-alpine.js` when required. |
| Asset mode | Support `bundle`, `link`, and `none` as explicit theme choices. |
| Dev server | Serve library assets at the same logical paths static builds understand. |
| Static build | Copy, fingerprint, and rewrite every referenced library asset. |
| Diagnostics | Error or warn when HTML references a library asset Bengal did not emit. |
| Runtime metadata | Surface Alpine/runtime requirements from Chirp UI metadata when templates need them. |

## Design Principles

- The component registry remains the source of truth for Chirp UI components.
- Chirp UI package metadata should describe assets and runtime requirements; it
  should not know about Bengal build internals.
- Bengal should own asset inclusion, copying, serving, fingerprinting, and
  diagnostics.
- `chirp-theme` should own composition, page semantics, and token choices.
- Theme templates should not hardcode package filesystem climbs, copied asset
  paths, or provider CSS link policy once Bengal supports the target contract.

## Ranked Waves

### Wave 1 — Stabilize The Current Theme Boundary

Status: shipped in the current migration stack.

Keep the theme on one CSS entrypoint and one JS provider link so dev/live reload
and static builds use the same visible contract. Document the reason in
`theme.toml`, `docs/CHIRP-THEME.md`, and package tests.

Required proof:

- Built HTML references `assets/css/style.*.css` or `/assets/css/style.css`, not
  `/assets/chirp_ui/chirpui.css`.
- The theme stylesheet contains the Chirp UI CSS imports.
- Package tests reject stale standalone provider CSS links.

### Wave 2 — Define Chirp UI Package Metadata

Status: shipped in the current migration stack.

Add a small, importable package contract for library consumers. This is
intentionally minimal and evidence-backed:

- package name: `chirp_ui`
- template loader root
- static root
- ordered CSS entries
- ordered JS entries
- optional Alpine/runtime entries
- manifest path and schema version

Required proof:

- Tests assert every declared asset exists under `static_path()`.
- Docs explain how frameworks should consume the metadata.
- No Bengal-specific behavior enters the Chirp UI package contract.

Implemented proof currently covers `chirp_ui.get_library_contract()`, the frozen
`LIBRARY_CONTRACT`, ordered CSS/JS asset entries, optional Alpine runtime assets,
manifest schema parity, and asset existence checks under the package static
root.

### Wave 3 — Bengal Library Asset Modes

Bengal should consume library metadata and give themes explicit inclusion modes:

- `bundle`: fold library CSS into the theme stylesheet output.
- `link`: emit separate library CSS/JS links, fingerprinted in static builds and
  stable in dev.
- `none`: make assets available but let the theme handle inclusion manually.

Required proof:

- Dev server and static build resolve the same logical library asset paths.
- Static build rewrites linked library assets to fingerprinted outputs.
- Build diagnostics identify the template and asset when a referenced library
  asset is not emitted.

### Wave 4 — Macro And Runtime Registration

Bengal should register Chirp UI's template loader and runtime helpers from the
same library declaration.

Required proof:

- A fixture theme using `libraries = ["chirp_ui"]` can import Chirp UI macros
  without manual loader setup.
- Runtime-dependent components can report required JS/Alpine assets before build
  output is written.
- Missing runtime assets are build diagnostics, not browser console surprises.

### Wave 5 — Remove Transitional Theme Imports

Once Bengal owns library CSS inclusion, remove filesystem-relative Chirp UI CSS
imports from `chirp-theme` and make `style.css` pure theme tokens, layout polish,
and content-specific overrides.

Required proof:

- `style.css` no longer imports package CSS by relative filesystem path.
- Theme output remains visually equivalent under `bundle` mode.
- Tests cover both dev logical paths and static fingerprinted paths.

## Not Now

- Adding more theme-level adapter macros.
- Teaching `chirp-theme` more Bengal asset internals.
- Creating a Bengal-specific public API inside Chirp UI before the package
  metadata shape is reviewed.
- Copying generated `chirpui.css` into the theme package.
- Treating current `@import "../../../../chirp_ui/..."` lines as the final
  architecture.

## Steward Notes

- Core registry/API steward: Wave 2 is a public metadata contract and must stay
  small, deterministic, and free-threading safe.
- Template/CSS steward: Wave 5 removes transitional imports only after Bengal
  can preserve cascade order and dev/build parity.
- Planning steward: this plan is active because it blocks reducing theme CSS
  plumbing without losing Chirp UI styling.
- Theme steward: continue converting page/content templates to Chirp UI
  primitives, but defer further asset plumbing to this contract.
