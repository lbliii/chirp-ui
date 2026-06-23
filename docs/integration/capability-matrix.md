# Capability matrix — Chirp vs standalone

Honest comparison of what you get with **`use_chirp_ui(app)`** (Chirp) vs wiring
chirp-ui yourself in Flask, FastAPI, Django, or bare kida.

Shared bootstrap details: [standalone-core.md](standalone-core.md).

Legend:

| Symbol | Meaning |
|---|---|
| **Free** | Provided by Chirp integration; no glue |
| **Hand-roll** | You wire it; chirp-ui ships the pieces |
| **Degraded** | Possible but lossy, stubbed, or intentionally out of scope |
| **Lost** | Not available without Chirp (or requires reimplementing Chirp features) |

---

## Core seams

| Capability | Chirp (`use_chirp_ui`) | Standalone | Notes |
|---|---|---|---|
| Kida template loader | **Free** — `get_loader()` auto-composed | **Hand-roll** — `ChoiceLoader` + `get_loader()` | Do not mix with Jinja/Django templates in the same file |
| Filters & globals (`bem`, `html_attrs`, `field_errors`, `validate_*`, `build_hx_attrs`, …) | **Free** — `register_filters()` via extension | **Hand-roll** — `register_filters()` on kida adapter | Filters ship in `chirp-ui`; Chirp also adds route-aware helpers |
| Semantic colors (`resolve_color`, `badge(color=…)`) | **Free** | **Hand-roll** — `register_colors()` once | Optional unless you use named colors |
| Static assets (`chirpui.css`, JS, patterns, themes) | **Free** — mounted at configured prefix | **Hand-roll** — serve `static_path()` | Framework-specific mount (see per-framework guides) |
| Manifest / agent contract | **Free** | **Free** — `load_manifest()`, `get_library_contract()` | No Chirp required |

---

## Runtime & interactivity

| Capability | Chirp | Standalone | Notes |
|---|---|---|---|
| Alpine core + plugins (Mask, Intersect, Focus) | **Free** — injected, deduped | **Hand-roll** — CDN `<script defer>` tags | Must use `/dist/cdn.min.js` browser build |
| `Alpine.safeData` shim | **Free** — inline bootstrap injected | **Hand-roll** — copy shim from [standalone-core.md](standalone-core.md) | **#1 footgun** — missing shim kills all interactive components |
| `chirpui-alpine.js` controllers | **Free** | **Hand-roll** — serve + load before Alpine core | Same file in both paths |
| `chirpui.js` pre-paint theme/style | **Free** | **Hand-roll** | Prevents flash of wrong theme |
| htmx script injection | **Free** | **Hand-roll** | Add CDN script yourself |
| Route-aware link attrs (`route_link_attrs`, boosted nav) | **Free** — Chirp router integration | **Degraded** — `make_route_link_attrs()` returns plain `href` | Internal links won't auto-get shell swap attrs |
| Dev-time Alpine manifest check | **Free** — startup/freeze warning | **Hand-roll** — call `check_alpine_runtime(html)` | Pure function in `chirp_ui.alpine` |
| Strict validation (`CHIRP_UI_DEV`) | **Free** | **Free** — `set_strict(True)` | Same library behavior |
| CSP contract documented | **Free** — Chirp merges policy via `use_chirp_ui` | **Hand-roll** — see [csp.md](csp.md) | Standard Alpine + inline macros need `'unsafe-eval'` |
| Manifest-driven CSS subset | **Hand-roll** — `build_chirpui_css.py --components` | **Hand-roll** — same CLI / `css_subset` module | Full `chirpui.css` always available |

---

## Forms & security

| Capability | Chirp | Standalone | Notes |
|---|---|---|---|
| `csrf_field` global for `form()` | **Free** — wired to Chirp CSRF | **Hand-roll** — bridge to framework token | Middleware still enforces |
| Server-side form validation display (`field_errors`) | **Free** — Chirp validation shape | **Hand-roll** — map framework errors to `{name: [str, …]}` | Filter ships in chirp-ui |
| File upload / wizard state helpers | **Free** — Chirp form runtime | **Hand-roll** — reimplement or simplify | Depends on feature depth |

---

## Islands, streaming, shell

| Capability | Chirp | Standalone | Notes |
|---|---|---|---|
| Island / primitive runtime (`island_attrs`, `primitive_attrs`) | **Free** — Chirp island loader | **Degraded** — stub globals or avoid components | High-state islands need Chirp |
| OOB swap fragments (shell chrome updates) | **Free** — helpers + shell contract | **Lost** — write fragment routes yourself | Macros render targets; server emits swaps |
| SSE / streaming HTML / Suspense | **Free** — native Chirp responses | **Lost** — reimplement per route | chirp-ui macros render markup only |
| App shell scroll/fill contract | **Free** — `shell_runtime_script()` + Chirp nav | **Degraded** — partial without shell helpers | Layout macros work; response plumbing is yours |
| CSP nonces on inline scripts | **Free** — `csp_nonce()` global | **Hand-roll** — add nonce attr to shim script | Required under strict CSP |

---

## Tooling & DX

| Capability | Chirp | Standalone | Notes |
|---|---|---|---|
| Component showcase reference | **Free** — `examples/component-showcase` | **Free** — run with `pip install -e ".[showcase]"` | Showcase uses Chirp; proves full stack |
| Bengal theme (`chirp-theme`) | **Free** — entry point in package | **Free** — no Chirp required | Static/docs sites |
| Framework integration guides | N/A | **Hand-roll** — Flask / FastAPI / Django docs | This saga (#284) |

---

## Upgrade pitch (why Chirp)

Standalone is the **on-ramp**, not the destination. The rows marked **Hand-roll**
or **Lost** above are exactly what `use_chirp_ui(app)` deletes:

1. Alpine + safeData + htmx injection and deduplication
2. CSRF and route-aware HTMX attrs
3. OOB shell updates, SSE, and Suspense response helpers
4. Island runtime for high-state components

Once you are hand-wiring the safeData shim, CSRF bridges, and OOB fragment
routes, Chirp stops looking like a new framework and starts looking like the
thing that removes your glue code.

---

## Related

- [standalone-core.md](standalone-core.md) — copy-paste bootstrap
- [anti-footguns.md](../safety/anti-footguns.md) — Alpine and registration pitfalls
- [alpine-magics.md](../components/alpine-magics.md) — controller API contract
- Saga: [#284](https://github.com/lbliii/chirp-ui/issues/284) Framework-Agnostic Adoption On-Ramp
