# Chirp UI — Next-Version Roadmap (proposal)

Status: **proposed** — supersedes the recipe-first posture in `roadmap-pre-1.0.md` pending sign-off
Date: 2026-06-12
Source: 7-agent audit/synthesis/critique pass (app-shell family, Alpine ownership, competitive
analysis vs Tailwind/shadcn/Radix/Mantine/Catalyst, polish/perf/breadth, plan reconciliation).
Every load-bearing claim below was independently re-verified against the source.

---

## TL;DR

The left-rail app shell, server-side route-awareness, the OOB shell-action contract, and the
base-layer hardening are genuinely **competitive or ahead**. But all four of the stated goals hit
the same structural wall, and one footgun silently breaks everything:

| Goal | Wall |
|---|---|
| Nail app-shells + route-context drawers | No right rail (`grid: "topbar topbar" "sidebar main"`); `drawer.html`/`tray.html` are route-unaware static overlays. |
| Alpine ownership / silent-disable fix | `check_alpine_runtime()` is dormant with a literal `TODO(chirp)` and only substring-matches `chirpui-alpine.js`, never Alpine core; the one execution proof (`test_alpine_lifecycle.py`) runs in **no required gate**. |
| Competitive with shadcn/Radix | No data grid, combobox, date picker, context menu, OTP, menubar; `<details>`-based popovers; 35-line toast. |
| Comprehensive + polished + performant | Default theme reads generic; CSS ships as one **669 KB / 87.8 KB-gzip un-minified, un-subsettable** file (use 5 components, ship all 352). |

**The posture decision is the spine of this roadmap** (next section). The work is organized into
**5 sagas**, sequenced so the things that *silently break everything* (Alpine reliability) and the
*contracts that unblock everything else* (shell-region + route-context protocol) ship first.

---

## The posture decision: adopt the MIDDLE PATH

`roadmap-pre-1.0.md` is deliberately recipe-first — it **forbids** shipping `application_chrome()`,
`docs_shell`, `catalog_shell`, `page_actions`, and shell-response helpers until *"a second
non-Bengal scenario-complete reference implementation"* exists. That gate directly blocks the #1
stated goal ("nail app-shells with route-context drawers").

**Decision: ship the route-context shell-region _contracts_ + ONE blessed composite (a route-aware
contextual rail/drawer wired into `app_shell`). Keep the generic mega-shell recipe-first.**

Justification, grounded in the evidence:

1. **The recipe-first gate is load-bearing for identity.** The no-utility-vocabulary,
   registry-as-source-of-truth thesis is exactly what makes chirp-ui uncopyable vs Tailwind
   (`vision.md`). Abandoning it wholesale re-enters Tailwind's category at a disadvantage. Keep it
   as the **default**.
2. **But the gate was designed to block a generic whole-frame macro.** The plan's own Wave-1
   evidence (`PLAN-application-chrome-system.md:864-940`) already records that two independent
   reference implementations composed app chrome from primitives and that the repeated hard part
   was **response/OOB ownership, not a missing visual macro**. The evidence bar is *already met* for
   shell-region + route-context **contracts**, and explicitly *not* met for a mega-shell.
3. **The "two non-Bengal reference implementations" bar is effectively unsatisfiable for a solo
   author with no userbase.** The plan admits this and then keeps rejecting its own fixtures — a
   doom loop that permanently blocks the headline goal behind a gate aimed at a different artifact.
   **Re-scope the gate so the author's own Playwright-tested fixtures count as qualifying
   evidence.**
4. **The missing piece is a contract, not a vocabulary.** Sidebar nav + breadcrumbs are *already*
   OOB targets (`app_shell.html:50,61`); `route_link_attrs` auto-applies under Chirp. The gap is a
   right-rail region + a documented route→drawer-content update protocol.

**Hard boundary the ADR must draw:** blessed shell-**region** contracts are authorized; whole-frame
macros stay forbidden. This matters because the drift is already real — `workspace_shell` ships
`maturity=stable` while the plan *defers* it. The ADR must retroactively bless (or demote)
`workspace_shell` so the boundary is drawn against shipped reality, not the stale plan.

---

## Proposed new labels

Two new labels (the rest of the work reuses the existing taxonomy: `saga`/`epic`/`flagship` +
`P0–P3` + category labels):

- **`shell`** — app-shell / shell-region / route-context chrome work. `navigation`/`architecture`/
  `components` don't capture "shell-region contract" specifically; keeps the flagship rail/drawer
  body filterable.
- **`mcp`** — the agent-native registry distribution work (MCP server over the manifest).
  `tooling`/`autodoc` are too broad to isolate it.

---

## Sequencing (re-cut along the OWNERSHIP axis, not just priority)

The single most important correction from the critique: **the cross-repo dependency is a sequencing
trap.** Several of the highest-value Alpine fixes live in the Chirp framework repo, which the
chirp-ui issues cannot merge into. If filed as plain P0 chirp-ui issues they stall indefinitely.
So each phase separates **chirp-ui-unilateral** (commit here, unblockable) from **Chirp-coordination**
(must not gate the chirp-ui issues).

- **Phase 0 — stop the silent breakage (chirp-ui-unilateral).** Saga 1 client-side self-check +
  wire `test_alpine_lifecycle` into the browser-chrome gate + extend the detector as a pure helper.
  Nothing else lands before this class of regression fails red.
- **Phase 1 — unblock the headline.** Posture ADR (write *before* building) → Saga 2 flagship
  route-context rail region + content-swap protocol (standalone-OOB convention first; Chirp
  auto-resolver is a Phase-2 enhancement) → reconcile the two shell entry points (carries the
  syncNav active-match fix) → **co-schedule mobile slide-over** (a route-context right rail is
  incomplete without defined mobile collapse). Chirp-side Alpine work + Bengal Alpine policy run in
  parallel on a coordination track that does *not* block the chirp-ui issues.
- **Phase 2 — competitive breadth that supports the shell.** Saga 3 data grid (parallelizable —
  independent of the shell) + form/overlay wave 1; co-schedule menubar/navigation_menu/context_menu/
  resizable (they support shell nav + the resizable rail).
- **Phase 3 — polish + perf (lands best on a complete surface).** Saga 4 premium default identity +
  role-based type; CSS subset emitter (can start earlier — it's independent and the only concrete
  perf liability); sonner-grade feedback; motion-token + vocabulary enforcement; Saga 2 a11y +
  persistence parity.
- **Phase 4 — lean into the moat.** Saga 5 registry-generated blocks gallery (composes everything
  earlier) → console_scripts + MCP server → theme explorer.

---

## Saga 1 — Alpine Ownership & Runtime Reliability
`saga, robustness, javascript, ci, architecture, shell`

**Goal:** make the Chirp↔chirp-ui Alpine contract fail **loud** — at dev runtime, in CI, and on the
Bengal docs surface — so "all interactive components are silently dead" becomes structurally
impossible to ship green. Sequenced FIRST: a disabled Alpine silently breaks every interactive
component added in Sagas 2–4, the page renders, and the console is clean — strictly worse DX than
shadcn (build error) or Tailwind (no JS to break).

> **Ownership split (critical):** the items below are tagged **[chirp-ui]** (commit here,
> unblockable) or **[Chirp]** (coordination track — must NOT block the chirp-ui issues).

### Epic [P0] Client-side Alpine runtime self-check — `epic, P0: ship-blocker, javascript, robustness`
- **[P0]** Add `window.Alpine`-absence self-check to `chirpui-alpine.js` **[chirp-ui]** — `register()`
  currently queues factories forever on an `alpine:init` that never fires when Alpine is absent, with
  no self-check. Add a deferred check: if chirp-ui `x-data` components are in the DOM but
  `window.Alpine` is undefined, `console.warn` loudly with a diagnostic + doc link. *Acceptance:* a
  page with chirpui components and no Alpine logs one clear warning; a healthy page is silent.
- **[P3]** ~~Optional visible dev-only health banner~~ — *cut/deferred* per critique: a `role=alert`
  banner rendering into the user's page contradicts the "no client JS in macros / minimal footprint"
  selling point. The `console.warn` + CI gate fully solve "failure is invisible."

### Epic [P0] Promote Alpine-execution proof into a required gate — `epic, P0: ship-blocker, ci, javascript`
- **[P0]** Wire `test_alpine_lifecycle.py` into `test-browser-chrome-check` **[chirp-ui]** — the only
  end-to-end proof that Alpine *executes* against a real `use_chirp_ui` app runs in no required job
  (`pyproject.toml:210`). **Open decision to resolve in the issue:** does this single fast
  Alpine-liveness assertion become a new required job, or is `browser-smoke.yml` promoted to required
  for just this check? (Resolve the tension with the documented "Playwright stays out of required
  gates" stance explicitly.) *Acceptance:* a regression that disables Alpine fails CI red.

### Epic [P1] Wire `check_alpine_runtime()` + harden the dedup contract — `epic, P1: flagship+adoption, robustness, architecture`
- **[P1]** Extend the detector to Alpine **core** + CDN-URL assertion **[chirp-ui]** — today it only
  substring-matches `chirpui-alpine.js`, never Alpine core, so the exact CLAUDE.md failure (AlpineInject
  skipped / wrong CDN URL resolving to CommonJS) is undetectable. Ship as a pure helper with a unit test.
- **[P1]** Wire `check_alpine_runtime()` into a freeze-time check **[Chirp coordination]** — it's
  dormant with `TODO(chirp)` (`alpine.py:179-182`), not called by `use_chirp_ui`.
- **[P1]** Harden `AlpineInject` dedup against content false-positives **[Chirp coordination]** —
  the string `data-chirp="alpine"` appearing in page content trips the dedup; anchor the match.

### Epic [P1] Bengal docs theme Alpine policy — `epic, P1: flagship+adoption, theme, robustness`
- **[P1]** Decide + implement the Bengal Alpine policy + loud guard **[chirp-ui/theme]** — the static
  docs theme loads `chirpui-alpine.js` via `library_asset_tags()` but never loads Alpine core (no Chirp
  middleware in that path), so `theme_toggle`/`dropdown_menu`/`modal`/`command_palette` are
  **dead-by-construction** on every Bengal page, with zero diagnostic — while the theme already
  pioneered a *loud* missing-CSS guard. Mirror that guard for Alpine.

---

## Saga 2 — App Shell & Route-Context Chrome  *(the flagship)*
`saga, shell, components, navigation, architecture, accessibility`

**Goal:** best-in-class server-rendered, route-aware application shells: a first-class left-OR-right
context rail whose drawer content swaps per route, a competitive mobile slide-over, reconciled shell
entry points, and accessible resize. This is goal #4 and the clearest competitive win — a
route-driven contextual rail is something Tailwind UI and shadcn's Sidebar *cannot* do without the
app author hand-wiring it, because they have no server routing layer.

### Epic [P1] Posture ADR + plan reconciliation — `epic, P1: flagship+adoption, documentation, architecture, cleanup`
*(Write this FIRST — it authorizes the rail work and re-scopes the gate.)*
- **[P1]** Write the posture ADR + re-scope the evidence gate — bake in the middle-path decision;
  **hard acceptance:** retroactively bless or demote `workspace_shell` (ships `stable`, plan defers
  it) so the blessed-region vs forbidden-mega-shell boundary is drawn against shipped reality.
- **[P3]** Collapse redundant umbrella plans; archive completed/downstream plans.

### Epic [P0] FLAGSHIP: Route-context rail region + content-swap protocol — `epic, flagship, P0: ship-blocker, feature, shell, components, navigation, architecture`
- **[P0]** Add an optional context-rail region to `app_shell` with a stable outlet id — extend the
  grid beyond `"topbar topbar" "sidebar main"` (`083_app-shell.css:18`) with an optional right (and
  optional left-secondary) region as a peer shell region, OOB-targetable like `shell_actions`.
- **[P0]** Define + document the route→rail-content update protocol — **standalone-OOB convention
  first** (chirp-ui-only, unblockable); Chirp `swap_resolver` auto-wiring is a Phase-2 enhancement.
  *Acceptance:* "works without Chirp, better with Chirp"; a Playwright gauntlet proves the rail swaps
  content per route at 320px → desktop.
- **[P1]** One blessed golden reference screen using the context rail (the qualifying evidence).

### Epic [P1] Mobile hamburger → slide-over nav drawer — `epic, P1: flagship+adoption, feature, shell, responsive, accessibility`
*(Co-scheduled with the rail region — a route-context right rail needs defined mobile collapse at
first ship, or the flagship is desktop-only.)*
- **[P1]** Ship the rail-to-tray/drawer responsive recipe + thin `app_shell` affordance — replace the
  weak horizontal-scroll sidebar strip with the Catalyst/Tailwind-standard slide-over. The pieces
  (drawer, tray, sidebar) exist; wire them.

### Epic [P1] Reconcile the two divergent shell entry points — `epic, P1: flagship+adoption, shell, architecture, navigation, bug`
- **[P1]** Unify the region contract across both entry points — `app_shell()` gives
  `#chirpui-sidebar-nav` / `#chirpui-topbar-breadcrumbs` aria-live OOB hooks; `app_shell_layout.html:96`
  (the path filesystem `mount_pages` apps actually extend) gives the `<aside>` no id, no OOB hook.
  One path has a dangling OOB target with no consumer.
- **[P1]** Single canonical active-match helper (server + JS parity) — *promoted from P2*: `syncNav()`
  uses `p===h || p.startsWith(h+'/')` for all links, ignoring per-item `match=exact`, so post-boost
  JS re-marks links active that the server intentionally left inactive (visible flicker/wrong active
  state on every boosted nav). Same files + logic as entry-point reconciliation — co-schedule.

### Epic [P2] Drawer/tray/split-panel a11y + persistence parity — `epic, P2: taste-floor, accessibility, keyboard, components`
- **[P2]** Pointer-event + keyboard resize for `split_panel` + collapsible sidebar — the drag handle
  is mouse-only (`mousedown/mousemove`), inaccessible to keyboard/touch despite `role=separator` +
  `aria-valuenow`.
- **[P2]** Swipe-to-dismiss + opt-in open-state persistence for drawer/tray (a tray open before a
  boosted swap is lost today).

---

## Saga 3 — Comprehensive Interactive Primitives
`saga, components, feature, accessibility, keyboard`

**Goal:** close the "serious library" interactive tier shadcn/Radix ship by default — built
Python/HTMX/Alpine-native, each with a registry descriptor and a keyboard/anatomy proof (not just a
render test). Verified absent: `context_menu`, `combobox`, `autocomplete`, `otp`, `hover_card`,
`menubar`, `navigation_menu`; `multi_select_field` is native `<select multiple>`; `date_field` is
native `<input type=date>`; `command_palette` has cmd+K but no arrow-key result navigation.

> **Scope-inflation risk:** this is the largest body of work. Ship wave 1 fully-hardened over wave 2
> half-done. Per-primitive, decide server-driven (HTMX) vs Alpine-client and keep heavy logic in
> `chirpui-alpine.js` factories, not fat inline `x-data`.

### Epic [P1] Server-driven data grid — `epic, P1: flagship+adoption, feature, components, performance, accessibility`
*(Parallelizable — independent of the shell saga; a top-3 competitive item.)*
- **[P1]** Sortable columns with `aria-sort` + server sort state.
- **[P1]** Row selection bound to `selection_bar` + sticky header/first column. *Acceptance:* the
  59-line `data_table.html` wrapper is a real grid — and is no longer labeled `stable` while thin
  (see the maturity-honesty task).

### Epic [P1] Form/overlay primitive parity — wave 1 — `epic, P1: flagship+adoption, feature, components, accessibility, keyboard`
- **[P1]** Combobox/autocomplete with roving-tabindex keyboard nav.
- **[P1]** Token-pill multi-select + calendar-backed date/range picker.
- **[P1]** Arrow-key result navigation + active-descendant for `command_palette`.

### Epic [P2] Form/overlay parity — wave 2 + focus-managed overlays — `epic, P2: taste-floor, feature, components, accessibility, keyboard`
- **[P2]** `context_menu`, OTP/PIN input, `hover_card`, `menubar`/`navigation_menu` (the last two
  support shell nav — co-schedule with Saga 2 Phase-2 work).
- **[P2]** Anchor-positioned, focus-managed popover/dropdown (currently `<details>`-based, no anchor
  positioning, no focus/Escape/click-outside contract).

### Epic [P1] Registry maturity honesty — `epic, P1: flagship+adoption, library-contract, robustness, tech-debt`
*(Folded in from the critique — a contract-integrity bug, not cosmetics.)*
- **[P1]** Make the `maturity` field honest — `data_table`/`table`/`calendar`/`bar_chart`/`donut`
  ship `stable` while being thin wrappers, and 27 ASCII novelty components are also `stable`, so the
  label can't distinguish a hardened core from a thin one. Either harden-before-stable or introduce a
  "thin-but-shipped" tier, enforced by a registry test. The manifest **is** the product (it grounds
  the MCP + blocks-gallery work in Saga 5); a dishonest field poisons that surface.

---

## Saga 4 — Polish, Performance & Premium Defaults
`saga, design, performance, css, tech-debt`

**Goal:** raise the taste floor and fix the one concrete perf liability so chirp-ui looks premium
out of the box and ships only what consumers use.

### Epic [P1] CSS payload: manifest-driven subset (minify optional) — `epic, P1: flagship+adoption, performance, css, packaging, render-blocking`
- **[P1]** Manifest-driven CSS subset emitter + standalone async-load docs — the registry already
  maps emitted-classes→partials, so a "ship only the components you use" emitter is the **genuine
  payload win** and the in-identity one. *Acceptance:* a consumer using 5 components ships a fraction
  of the 352-component CSS.
- **[P2]** ~~`chirpui.min.css` via a free-threading-safe minifier~~ — *demoted from P1* per critique:
  Lightning CSS bindings are out (free-threading constraint), so a pure-Python/subprocess minifier
  yields a modest gzip delta on top of the already-87.8 KB-gzipped file, for added build-artifact +
  freshness-gate friction. The subset emitter is the real win; the minifier is optional polish.

### Epic [P1] FLAGSHIP: Premium default identity + role-based type — `epic, flagship, P1: flagship+adoption, design, fonts, contrast, dark-mode`
- **[P1]** Distinctive default token profile — the default accent is Tailwind sky; the project's own
  taste plan admits a contract floor but no taste floor. Pure-token, in-identity, carries most of the
  premium-perception weight.
- **[P1]** Role-based rem type ramp for dense app contexts — UI type uses viewport `clamp()` causing
  dense-app hierarchy drift.
- **[P3]** *Decoupled:* optional bundled variable font — pulled OUT of the flagship epic into a
  separate, explicitly-gated stop-and-ask decision (shipping a font file conflicts with the
  zero-runtime-dependency ethos). The flagship taste work is not blocked on the font question.

### Epic [P2] sonner-grade feedback — `epic, P2: taste-floor, components, javascript, reduced-motion, accessibility`
- **[P2]** Stacking, swipe-dismiss, server-driven loading→success/error toasts (the HTMX-native
  answer to sonner's promise API; default in shadcn) — upgrades the 35-line single-OOB-div toast.

### Epic [P2] Motion-token enforcement + vocabulary unification — `epic, P2: taste-floor, tech-debt, css, library-contract`
- **[P2]** Extend the motion-token test to `animation`/`animation-duration` — the test currently only
  covers `transition`; there are 167 raw-second declarations the "motion tokens enforced" claim
  misses.
- **[P2]** Unify the `error` vs `danger` destructive vocabulary with aliasing — the two have **zero**
  variant overlap. **Broaden** the registry invariant test to "no semantic concept has two disjoint
  variant names" so it catches the class, not just this instance.

### Epic [P3] Container-query responsiveness (narrowed) — `epic, P3: tech-debt, css, responsive`
- **[P3]** Add container-query breakpoints to **card + surface only** (the components that sit in the
  new context rail — pairs with Saga 2). Container queries are advertised as a stack pillar but barely
  used (4 `@container` vs 77 `@media`). Narrowed from the broad component list to avoid a P3 quietly
  consuming a sprint.

---

## Saga 5 — Registry as Distribution Product
`saga, autodoc, showcase, tooling, library-contract, mcp`

**Goal:** lean into the one uncopyable advantage — the machine-inspectable registry/manifest (352
entries) — by turning it into an agent-native distribution surface. shadcn's registry is a code-copy
distributor that *erases* the contract on paste; chirp-ui's registry **preserves** it. Sequenced
last: it composes the components + golden screens from earlier sagas.

### Epic [P1] FLAGSHIP: Registry-generated copy-paste blocks gallery — `epic, flagship, P1: flagship+adoption, showcase, autodoc, content, ia`
- **[P1]** Build a browsable blocks gallery generated from the manifest — Tailwind Plus's 500+ blocks
  and shadcn's Blocks are the dominant "comprehensive + premium" perception driver; chirp-ui has a
  QA-oriented audit page, not a shoppable gallery. Each entry renders live HTML + the copyable Kida
  macro call. **Hard acceptance (folded in from critique):** gallery generation is wired into the
  existing `release-preflight`/`build-css-check`-style freshness gate from its FIRST commit, like
  `manifest.json`/`chirpui.css` already are — or it becomes the exact contract-erosion the registry
  exists to prevent.

### Epic [P1/P2] Agent-native registry: CLI entry points + MCP server — `epic, tooling, autodoc, library-contract, mcp`
- **[P1]** `chirp-ui` console_scripts entry point — *quick-win, split out from MCP*: the documented
  `python -m chirp_ui find` has no installed `chirp-ui` command. A near-trivial `[project.scripts]`
  addition that should ship immediately.
- **[P2]** MCP server over the manifest — the most defensible expansion of the Python/agent angle.
  **Acceptance:** the MCP surface is freshness-gated like the gallery.

### Epic [P3] Interactive theme explorer — `epic, P3: tech-debt, showcase, design, dark-mode`
- **[P3]** Live token explorer with preset switching + contrast/dark preview (Radix Themes, Mantine,
  daisyUI all ship live theming — a strong "shine" signal the existing roadmap already plans).

---

## Risks (carry into the issues)

1. **Cross-repo dependency (top risk).** The root dedup/injection Alpine fixes are Chirp-owned.
   chirp-ui ships the loud client guard + CI proof unilaterally so failure is at least *visible* even
   if the Chirp-side fix lags — but do not file Chirp-owned work as blocking chirp-ui P0/P1 issues.
2. **Posture overreach.** "One blessed composite" can drift into the mega-shell the gate exists to
   prevent (`workspace_shell` already drifted). The ADR must enforce the region-vs-frame boundary.
3. **Saga 3 under-resourcing.** A data grid + 7 primitives to Radix/shadcn a11y parity is the easiest
   work to ship thin. Resist labeling thin primitives `stable` (the current `data_table`/`calendar`
   dishonesty is precisely this failure).
4. **"No client JS in macros" tension.** Combobox/command-nav/swipe/resizer push Alpine into
   templates (allowed: `x-data` only) — keep heavy logic in `chirpui-alpine.js` factories.
5. **Font vs zero-dependency ethos** — decoupled to a stop-and-ask (see Saga 4).
6. **Gallery/MCP drift** — solved by the freshness-gate acceptance criteria above.

---

## Mapping to existing plans

| Existing plan | Disposition |
|---|---|
| `PLAN-application-chrome-system.md` | Re-scoped by Saga 2 ADR; evidence gate relaxed to count author fixtures. |
| `PLAN-visual-taste-floor-saga.md` | Feeds Saga 4 (premium identity + type). |
| `PLAN-component-maturity-gap-sweep.md` | Feeds Saga 3 (primitives + maturity honesty). |
| `PLAN-page-actions-primitive.md` | Stays recipe-first (mega-shell side of the boundary). |
| `PLAN-css-scope-and-layer.md` | Continues as opportunistic; not a saga. |
| `PLAN-pre-1.0-productization-saga.md` | Collapse into this roadmap (Saga 2 ADR cleanup task). |
| `roadmap-pre-1.0.md` | Superseded by this doc on the posture point; verification/CSS-scope workstreams remain valid. |
