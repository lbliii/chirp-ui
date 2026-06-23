# Bengal docs theme — Alpine policy

**Status:** accepted (issue [#192](https://github.com/lbliii/chirp-ui/issues/192))  
**Scope:** `chirp-theme` (`src/bengal_themes/chirp_theme/`)

---

## Decision

The Bengal docs theme uses a **split interactivity model**:

| Surface | Runtime | Examples |
|---|---|---|
| **Theme shell chrome** | Vanilla JS + platform APIs | Mobile nav (`<dialog>`), search modal, theme appearance menu (`<popover>` + `theme.js`), mega-menu (`nav-dropdown.js`) |
| **Embedded chirp-ui macros** | Alpine 3.x + `chirpui-alpine.js` | Component specimens, autodoc demos, any page that imports `dropdown_menu`, `modal`, `data_grid`, … |

Theme chrome **does not** use Alpine. That keeps the docs shell lightweight and
 avoids coupling Bengal's static build to Alpine's CSP/`unsafe-eval` contract for
 navigation that already works with native APIs.

Embedded chirp-ui macros **do** require Alpine. `library_asset_tags()` emits
`chirpui.css`, `chirpui.js`, and `chirpui-alpine.js`, but **not** Alpine core.
The theme therefore loads Alpine core and the safeData shim in `base.html`
immediately after `library_asset_tags()`.

---

## What `base.html` ships

1. `{{ library_asset_tags() }}` — chirp-ui library bundle (Bengal >= 0.3.3).
2. Inline **safeData shim** — same bootstrap as
   [standalone-core.md](../integration/standalone-core.md) (queues factory
   registration until `alpine:init`).
3. **Alpine core** — deferred CDN script, URL ending in `/dist/cdn.min.js`.

Script order matches the standalone contract: `chirpui.js` → shim →
`chirpui-alpine.js` → Alpine core.

---

## Diagnostics (fail loud, not silent)

| Failure | Signal |
|---|---|
| Bengal < 0.3.3 / missing `library_asset_tags` | HTML comment in `<head>` — `--chirpui-*` tokens undefined, layout collapses |
| Alpine core blocked (CSP, ad blocker, wrong CDN URL) | `chirpui-alpine.js` dev self-check warns in the console; `check_alpine_runtime(html)` reports `result.problems` |
| Missing `chirpui-alpine.js` with interactive macros | `check_alpine_runtime` → `"chirpui-alpine.js runtime script is not in the HTML"` |

The missing-CSS guard predates this policy (#154). The Alpine stack completes
the same philosophy for interactive macros.

---

## CSP note

Alpine inline expressions require `script-src 'unsafe-eval'` with the standard
build. See [integration/csp.md](../integration/csp.md). The chirp-ui docs site
(GitHub Pages) does not ship a restrictive CSP today; if you add one to a Bengal
consumer, merge the chirp-ui contract.

---

## Non-goals

- Do **not** rewrite theme shell chrome to Alpine macros (`theme_toggle`,
  `dropdown_menu` in the header) — the bespoke shell is intentional.
- Do **not** load Alpine plugins (Mask, Intersect, Focus) on static Bengal builds
  unless a page needs them; the docs theme does not require them for shell chrome.

---

## Related

- [chirp-theme.md](chirp-theme.md) — package layout and product direction
- [bengal-theme-anatomy.md](bengal-theme-anatomy.md) — which controls are theme-owned
- [../integration/csp.md](../integration/csp.md) — CSP contract for interactive macros
