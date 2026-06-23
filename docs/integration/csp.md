# Content Security Policy — chirp-ui contract

chirp-ui ships **server-rendered HTML** with **inline Alpine expressions** on
interactive components (`x-data="chirpuiDropdown()"`, `@click`, `:class`, …).
That pattern is deliberate — factories live in `chirpui-alpine.js`, but Alpine
still **evaluates inline attribute expressions** at runtime.

This document is the missing contract called out in
[#221](https://github.com/lbliii/chirp-ui/issues/221). Without it, an app that
wires a secure-by-default CSP gets a **silently dead shell** (page renders,
components are inert, console may be clean).

See also:

- [standalone-core.md](standalone-core.md) — Alpine script order + safeData shim
- [capability-matrix.md](capability-matrix.md) — Chirp vs standalone CSP rows
- [../components/alpine-magics.md](../components/alpine-magics.md) — when inline
  `x-data` is acceptable vs a named factory

---

## Minimum CSP for standard Alpine (today)

With the **browser build** of Alpine 3.x (`/dist/cdn.min.js`), chirp-ui needs:

| Directive | Required value | Why |
|---|---|---|
| `script-src` | `'unsafe-eval'` | Alpine evaluates inline `x-data`, `@click`, `:class`, … |
| `script-src` | `'unsafe-inline'` **or** a per-request **nonce** on the safeData shim | The inline bootstrap that defines `Alpine.safeData` / `_chirpAlpineData` |
| `script-src` | Host allowlist for Alpine CDN **or** self-hosted `/dist/cdn.min.js` | Alpine core + optional plugins |
| `script-src` | Self (or static mount) for `chirpui.js`, `chirpui-alpine.js` | Library scripts |
| `style-src` | `'unsafe-inline'` **or** nonces | Some macros emit inline `style=` for one-off geometry; prefer tokens |
| `style-src` | Self for `chirpui.css`, `chirpui-transitions.css` | Component styles |

Example **development** header (adjust hostnames to your static mount):

```http
Content-Security-Policy:
  default-src 'self';
  script-src 'self' https://cdn.jsdelivr.net 'unsafe-eval' 'unsafe-inline';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  font-src 'self' data:;
  connect-src 'self';
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self';
```

**Production:** replace `'unsafe-inline'` on scripts with a **nonce** wired to
the safeData shim (Chirp does this via `csp_nonce()` — see below). Keep
`'unsafe-eval'` until you migrate to `@alpinejs/csp` or native primitives.

---

## Chirp integration (`use_chirp_ui`)

Chirp owns CSP injection when you call `use_chirp_ui(app)`:

| Concern | Chirp behavior |
|---|---|
| Alpine core + plugins | Injected once, deduped, correct `/dist/cdn.min.js` URL |
| safeData shim | Inline script with **`csp_nonce()`** global |
| `chirpui-alpine.js` | Injected before Alpine core |
| Dev warning | `check_alpine_runtime()` against rendered layout (framework-side) |

If your app **also** sets a strict CSP middleware, ensure it **merges** with
Chirp's policy rather than replacing it. A hand-rolled policy that omits
`'unsafe-eval'` while still using standard Alpine + chirp-ui macros will disable
every interactive component.

Chirp's optional **`alpine_csp=True`** mode (see
[Chirp Alpine guide](https://lbliii.github.io/chirp/docs/build-apps/ui-extensions/alpine/))
switches to the **`@alpinejs/csp` build**, which forbids inline expressions.
chirp-ui has **not** migrated its templates to that build yet — treat
`alpine_csp=True` as a **compatibility experiment**, not a drop-in for all macros.

---

## Standalone integration

Follow [standalone-core.md](standalone-core.md) for script order. For CSP:

1. **Allow `'unsafe-eval'`** in `script-src` while using standard Alpine.
2. Put a **nonce** on the safeData shim `<script nonce="…">` and add that nonce
   to `script-src` instead of `'unsafe-inline'`.
3. Serve `chirpui.js`, `chirpui-alpine.js`, and Alpine from `'self'` when possible
   (fewer third-party allowlist entries).
4. Call `check_alpine_runtime(html)` in dev/test — it detects missing
   `chirpui-alpine.js`, missing Alpine core, and the bare-`alpinejs@version` CDN
   footgun.

```python
from chirp_ui.alpine import check_alpine_runtime

result = check_alpine_runtime(response.text)
if result.factories_used and result.problems:
    raise RuntimeError("; ".join(result.problems))
```

---

## Bengal static docs (`chirp-theme`)

The packaged Bengal theme loads chirp-ui via `library_asset_tags()` and adds
Alpine core + the safeData shim in `base.html` so embedded component specimens
work. Static GitHub Pages builds typically **do not** set a restrictive CSP; if
you add one to a Bengal site, apply the same table above.

Shell chrome (mobile nav, search modal, theme menu) uses **native `<dialog>` /
`<popover>` + theme JS** — not Alpine. See
[../theming/bengal-alpine-policy.md](../theming/bengal-alpine-policy.md).

---

## Longer-term: eliminating `'unsafe-eval'`

Three viable paths (not mutually exclusive):

1. **`@alpinejs/csp` build** — register every factory with `Alpine.data()` and
   reference by name; no inline arg/handlers in templates. Large migration.
2. **Native platform primitives** — `<details>`, `<dialog>`, `popover`, CSS
   `:has()` / `@starting-style` where they cover the interaction.
3. **Data-attribute factories** — expand the pattern already used in some macros:
   escaped `data-*` attrs + a single `init()` reader (no inline JS literals).

Until a migration ships, **`'unsafe-eval'` is a documented requirement**, not a
silent footgun.

---

## Checklist

- [ ] `script-src` includes `'unsafe-eval'` (standard Alpine) **or** you have
      migrated the macros you use to `@alpinejs/csp` / native primitives
- [ ] safeData shim is nonce-safe (not `'unsafe-inline'` in production)
- [ ] Alpine core URL ends in `/dist/cdn.min.js`
- [ ] `check_alpine_runtime(html)` passes in dev when interactive macros render
- [ ] Styles allow `chirpui.css` + any inline geometry you rely on
