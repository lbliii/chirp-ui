# Bengal Chirp UI library contract

**Status:** Active  
**Owner:** chirp-theme / Bengal integration  
**Scope:** First-class Chirp UI consumption from Bengal themes without theme-local asset plumbing

## Context

`chirp-theme` should declare `libraries = ["chirp_ui"]` and then use Chirp UI
macros, tokens, CSS, and runtime assets through Bengal's library contract. Theme
templates should not know package-relative asset paths, fingerprinting rules,
or dev/static serving details.

Current state:

- `theme.toml` declares `libraries = ["chirp_ui"]`.
- `base.html` calls Bengal 0.3.3's `library_asset_tags()` helper.
- `assets/css/style.css` contains only theme tokens, layout polish, and
  content-specific overrides.
- package tests require built HTML, emitted files, and `asset-manifest.json` to
  agree on Chirp UI provider assets and the theme stylesheet.

The linked-asset path is validated. Bundle and none modes still need explicit
fixture coverage before this plan can close.

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

### Waves 1-2 — Shipped Boundary And Package Metadata

| Wave | Status | Contract | Proof |
|---|---|---|---|
| 1. Stabilize theme boundary | Shipped | Theme uses Bengal-managed provider links plus one theme stylesheet; no filesystem-relative Chirp UI CSS imports. | Built HTML references emitted provider CSS/JS and theme CSS; package tests verify manifest entries and files. |
| 2. Define Chirp UI package metadata | Shipped | `chirp_ui.get_library_contract()` and `LIBRARY_CONTRACT` expose package name, template root, static root, ordered CSS/JS entries, optional Alpine/runtime assets, manifest path, and schema. | Tests assert declared assets exist under `static_path()` and no Bengal build behavior enters the Chirp UI package contract. |

### Wave 3 — Bengal Library Asset Modes

Bengal should consume library metadata and give themes explicit inclusion modes:

| Mode | Semantics |
|---|---|
| `bundle` | Fold required library CSS into the theme stylesheet output while preserving Chirp UI cascade order before theme overrides. |
| `link` | Emit separate library CSS/JS links, fingerprinted in static builds and stable in dev. |
| `none` | Make library assets available and register templates/helpers, but let the theme handle inclusion manually. |

Bengal owns this mode switch. The selected mode is not Chirp UI package metadata;
Chirp UI only declares assets, template roots, and runtime requirements. Bengal
uses that metadata to make dev server and static build behavior match.

Required proof:

- Dev server and static build resolve the same logical library asset paths.
- Static build rewrites linked library assets to fingerprinted outputs.
- Build diagnostics identify the template and asset when a referenced library
  asset is not emitted.

Fixture matrix:

| Mode | Fixture proves | Required checks |
|---|---|---|
| `bundle` | A theme with `libraries = ["chirp_ui"]` and `asset_mode = "bundle"` emits one theme CSS output containing Chirp UI CSS before theme overrides. | Built HTML references the theme stylesheet only; asset manifest contains the bundled output; cascade layer order remains `chirpui.*` before `app.overrides`. |
| `link` | The same theme with `asset_mode = "link"` emits separate logical library CSS/JS links in dev and fingerprinted library outputs in static builds. | Dev logical paths and static manifest outputs resolve; linked assets are copied and rewritten; missing linked assets are diagnostics. |
| `none` | The same theme with `asset_mode = "none"` registers macros/helpers and makes assets available without automatic CSS/JS inclusion. | Chirp UI macros import successfully; built HTML has no automatic library links; explicit theme-managed links still resolve when present. |

### Waves 4-5 — Registration And Theme Import Cleanup

| Wave | Status | Required Proof |
|---|---|---|
| 4. Macro and runtime registration | Open | A fixture theme using `libraries = ["chirp_ui"]` imports Chirp UI macros without manual loader setup; runtime-dependent components report required JS/Alpine assets before build output; missing runtime assets become diagnostics. |
| 5. Remove transitional theme imports | Shipped for linked mode | `style.css` no longer imports package CSS by relative filesystem path; built static HTML references fingerprinted provider CSS/JS plus theme CSS; bundle/none mode work remains separate fixtures. |

## Not Now

- Adding more theme-level adapter macros.
- Teaching `chirp-theme` more Bengal asset internals.
- Creating a Bengal-specific public API inside Chirp UI before the package
  metadata shape is reviewed.
- Copying generated `chirpui.css` into the theme package.
- Reintroducing filesystem-relative Chirp UI CSS imports as a theme
  convenience.

## Steward Notes

- Core registry/API steward: Wave 2 is a public metadata contract and must stay
  small, deterministic, and free-threading safe.
- Template/CSS steward: linked-provider Wave 5 proof is shipped; bundle/none
  fixtures still need cascade and dev/build parity coverage.
- Planning steward: this plan is active because it blocks reducing theme CSS
  plumbing without losing Chirp UI styling.
- Theme steward: continue converting page/content templates to Chirp UI
  primitives, but defer further asset plumbing to this contract.
