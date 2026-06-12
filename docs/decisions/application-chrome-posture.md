# Application Chrome Posture — Middle Path

**Status**: Accepted
**Date**: 2026-06-12
**Supersedes**: the pure recipe-first stance of `strategy/roadmap-pre-1.0.md` and
`plans/PLAN-application-chrome-system.md` on the app-shell question (only).
**Related**: `strategy/roadmap-next.md`, `strategy/vision.md`,
`plans/PLAN-application-chrome-system.md`, GitHub saga #199 / flagship #195.

---

## Context

chirp-ui's headline next-version goal is to **nail application shells — especially
rails with slide-out drawers (left or right) whose content updates with context
based on routing.** Today that pattern does not exist as a first-class contract:
the app-shell grid is literally `"topbar topbar" / "sidebar main"` (no right/
secondary region), and `drawer.html` / `tray.html` are route-unaware static
overlays.

The existing planning corpus is deliberately **recipe-first**. It records an
*accepted boundary* — "Recipe First, Composite Later" — that forbids shipping a
generic application-frame macro (`application_chrome()`, `object_chrome()`,
`workspace_header()`, `dense_nav_frame()`, `docs_shell()`, `catalog_shell()`,
`page_actions()`) until **"at least two independent reference implementations
repeat the same contract"** (`PLAN-application-chrome-system.md:72,83,846`).

Two facts put that gate in tension with the goal:

1. **The evidence bar is effectively unsatisfiable as written.** A
   "second non-Bengal scenario-complete reference implementation" presumes a
   userbase that does not yet exist. The plan repeatedly rejects its own
   browser-tested fixtures as insufficient, creating a loop where the headline
   goal is permanently blocked by a gate aimed at a *different* artifact (a
   generic whole-frame macro), not at the rail/region contract the goal needs.
2. **The plan's own Wave-1 evidence already met the bar for the smaller
   contract.** It records (`PLAN-application-chrome-system.md:106,124`) that two
   independent reference implementations *already* composed app chrome from
   primitives, and that the repeated hard part was **response/OOB ownership** —
   not a missing visual macro. The contract evidence exists; the mega-shell
   evidence does not.

## Decision — adopt the MIDDLE PATH

**Ship the route-context shell-_region_ contracts plus exactly ONE blessed
composite — a route-aware contextual rail/drawer wired into `app_shell`. Keep the
generic mega-shell recipe-first.**

Concretely, this ADR **authorizes**:

- A first-class **context-rail region** in `app_shell` (optional right and/or
  left-secondary), as a peer region with a stable, OOB-targetable outlet id —
  the same response/OOB contract `shell_actions` already uses.
- A **context-drawer** that is route-aware (not just a static overlay).
- A documented **route → region/drawer content-update protocol**, with a
  standalone-OOB convention as the baseline and Chirp's `swap_resolver`
  auto-wiring as a progressive enhancement ("works without Chirp, better with
  Chirp").

It **keeps forbidden** (recipe-first, unchanged): `application_chrome()`,
`docs_shell()`, `catalog_shell()`, `compact_page_header()`/`docs_header()`,
`page_actions()`, `workspace_header()`, and any other generic whole-frame or
product-IA-owning macro.

### The hard boundary

The distinction this ADR draws and enforces:

| Blessed (may become stable public API) | Forbidden (stays recipe-first) |
|---|---|
| Shell **region** contracts: a context-rail region, a route-context drawer, and the route→content update protocol, each wired to the existing OOB/response contract and proven by a Playwright gauntlet. | Generic whole-**frame** macros that own page composition or product information architecture (`application_chrome`, `docs_shell`, `catalog_shell`, `page_actions`, `workspace_header`). |

A region contract adds *one named outlet + a swap convention* to a shell the app
author still composes. A frame macro tries to *own the whole layout*. The first
is a contract; the second encodes one product's IA. We bless the first, defer the
second.

### Re-scoped evidence gate

For **shell-region contracts only**, the qualifying evidence is relaxed: the
author's own scenario-complete, browser-tested fixtures (Playwright gauntlets
across 320 px → desktop, exercising the rail/drawer fallback, route-context swap,
focus, and overflow) **count as qualifying evidence**. The mega-shell gate is
unchanged — those still require independent reference-implementation evidence
that does not yet exist.

## `workspace_shell` reconciliation

`workspace_shell` shipped `maturity="stable"` while `PLAN-application-chrome-system.md:846`
keeps it **deferred** (promotable only when two reference implementations need the
same workspace/sidebar/tab/page-tool contract). That is real plan-vs-reality
drift, and it is precisely the precedent that proves the gate was being walked
past silently.

**Decision: demote `workspace_shell` to `maturity="experimental"`** (done in this
change; manifest regenerated). It is a broad workbench *frame*, not the blessed
*region* contract — so under the boundary above it belongs on the experimental
track until it earns promotion on its own evidence. This aligns it with its
siblings `composer_shell` and `dock`, which are already `experimental`. No
template or API change accompanies the demotion; it is a stability-signal
correction only.

## Consequences

- The flagship **route-context rail region + content-swap protocol** (#195) is
  now authorized to proceed — region contract first, standalone-OOB before the
  Chirp auto-resolver.
- chirp-ui's identity is preserved: this adds *contracts*, not a utility
  vocabulary and not a mega-shell. The registry-as-source-of-truth thesis
  (`vision.md`) stays intact, which is exactly what differentiates chirp-ui from
  Tailwind's category.
- Anyone promoting a *frame* macro must still clear the original gate. This ADR
  does not open that door.
- Consumers relying on `workspace_shell` see an `experimental` signal; the macro
  itself is unchanged and continues to render.
