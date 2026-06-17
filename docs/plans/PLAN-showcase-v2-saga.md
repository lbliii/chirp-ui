# PLAN: Component Showcase v2 Saga

Status: proposed (issues filed 2026-06-17)
Date: 2026-06-17
Trigger: The live Railway showcase (`examples/component-showcase/`) has grown into a
monolith — ~55 routes, ~1,550 lines in `app.py`, ~63 templates, and ~1,075 lines of
showcase-only CSS in `base.html`. Navigation is duplicated (sidebar + home card grid),
there is no global search, and fixture data for shell recipes dominates the backend.
Recent CSP nonce work surfaced how many moving parts share one file. The showcase still
does its job as a component gallery, but discoverability and maintainability are now the
bottleneck — not coverage.

Deploy target: `chirp-ui-showcase-production.up.railway.app` (unchanged — v2 is an
in-repo refactor, not a new service).

## Mission

Make the component showcase **easy to navigate**, **cheap to extend**, and **safe to
deploy** — without reducing what it proves. v2 introduces a single page registry,
global search (command palette), and a modular app layout; it does **not** require a
rewrite of every demo page on day one.

## Problem Statement

The showcase currently mixes four audiences in one app:

| Audience | Examples | Pain today |
|---|---|---|
| Component gallery | `/ui`, `/forms`, `/cards` | Hard to find among 55 routes |
| Shell recipes | `/catalog-shell`, `/operations-shell`, `/support-shell` | ~950 lines of inline fixture data in `app.py` |
| Golden screens | `/screen-command-center`, `/screen-review-queue` | Same nav/search surface as low-level demos |
| Interactive demos | `/streaming`, `/data`, `/islands` | Route handlers interleaved with fixtures |

Symptoms:

- **No global search** — sidebar scroll is the only discovery path.
- **Triple navigation** — `base.html` sidebar, `index.html` card grid, and per-page
  copy all drift independently.
- **`app.py` is a junk drawer** — imports, fixtures, helpers, and 55 route handlers
  share one file.
- **`base.html` is a stylesheet** — catalog/ops/support shell CSS loads on every page.
- **Adding a page** touches 3–4 places (route, template, sidebar link, index card).

## Non-Goals

- Do **not** split the showcase into multiple Railway services or repos.
- Do **not** build server-side full-text search over `manifest.json` (200+ components) —
  showcase **pages** (~55 entries) are the search domain; component macro names can be
  tags, not a separate index.
- Do **not** rewrite every showcase template in v2 — migrate structure first, pages
  incrementally.
- Do **not** replace the static visual audit page (`examples/design-system-gap-showcase/`)
  — it keeps the no-server contract; this saga is about the **live Chirp app**.
- Do **not** introduce a non-pure-Python CSS build step for the showcase.
- Do **not** block v2 on filesystem routing — optional follow-up epic only.

## Success Criteria

v2 is done when:

1. Every showcase page is declared **once** in a registry and drives sidebar, home
   cards (or a generated index), and search.
2. **Command palette search** (⌘K / Ctrl+K) jumps to any registered page from any route.
3. `app.py` is a thin entrypoint (<200 lines) that mounts route modules and loads fixtures
   from `fixtures/`.
4. Shell-recipe CSS is **scoped** — gallery pages no longer download catalog/ops/support
   shell styles unless they need them.
5. Adding a new showcase page is a **single registry entry + template + route module
   one-liner** (documented in the epic acceptance).
6. Existing browser/evidence tests pass; new registry + search tests ratchet the contract.

---

## GitHub Saga Structure

Suggested GitHub labels: `saga:showcase-v2`, `epic:showcase-v2-*`, `area:showcase`.

Create one **tracking issue** (saga umbrella) linking the epics below. File epics as
GitHub issues when execution starts; task IDs here (`S2-E*-*`) map 1:1 to checklist items
in those issues.

---

## Epic 1 — Page Registry (source of truth)

**Goal:** One declarative list drives navigation, metadata, and (later) search.

**GitHub epic title:** `Epic: Showcase v2 — page registry`

| Task ID | Title | Description | Acceptance |
|---|---|---|---|
| S2-E1-1 | Define registry schema | Add `examples/component-showcase/registry.py` (or `showcase/registry.py`) with typed entries: `path`, `title`, `section`, `description`, `tags`, `nav_order`, optional `icon`, `match` (`exact`/`prefix`), flags (`golden_screen`, `shell_recipe`, `interactive_demo`). | Schema documented in module docstring; no runtime imports from templates yet. |
| S2-E1-2 | Migrate sidebar from registry | Replace hand-maintained `sidebar_link` lists in `base.html` with a Jinja loop over registry sections (Core, Components, Data, Effects, ASCII, Rich). | Sidebar links match pre-v2 URLs; order preserved. |
| S2-E1-3 | Migrate home index from registry | Replace `index.html` card grid with registry-driven cards (or a `{% for page in showcase_pages %}` partial). | Home page lists same destinations; no duplicate copy of paths. |
| S2-E1-4 | Registry context injection | Expose registry to all templates via a `_page()` helper or `Template(..., showcase_pages=...)`. | Any template can iterate pages; `current_path` highlighting unchanged. |
| S2-E1-5 | Registry ratchet test | `tests/test_showcase_registry.py`: every `@app.route` page template (except POST/fragment/SSE endpoints) has a registry entry; no orphan registry paths. | `uv run pytest tests/test_showcase_registry.py -q` |

**Proof:** `uv run pytest tests/test_showcase_registry.py tests/test_app_shell_contract.py -q`

---

## Epic 2 — Global Search (command palette)

**Goal:** Jump to any showcase page from anywhere; dogfood `command_palette`.

**GitHub epic title:** `Epic: Showcase v2 — command palette search`

Depends on: Epic 1 (registry).

| Task ID | Title | Description | Acceptance |
|---|---|---|---|
| S2-E2-1 | Serialize registry for client search | Emit registry as JSON in a `<script type="application/json" id="showcase-page-index">` or `GET /showcase/pages.json` (static, cacheable per deploy). | Payload ≤55 entries; includes path, title, section, tags, description. |
| S2-E2-2 | Wire `command_palette` in topbar | Add palette trigger to `base.html` `topbar_end` (alongside theme toggle). Items built from registry. | ⌘K / Ctrl+K opens palette on all shell pages. |
| S2-E2-3 | Client-side fuzzy filter | Filter by title, section, tags, description (simple substring or small fuzzy helper — no new deps). Arrow keys + Enter navigate; Esc closes. | Typing "catalog" surfaces `/catalog-shell`; "stream" surfaces `/streaming`. |
| S2-E2-4 | CSP-safe palette script | Any inline palette bootstrap uses `nonce="{{ csp_nonce() }}"` (same contract as shell runtime). | No CSP violations on palette open/select. |
| S2-E2-5 | Optional HTMX search fragment | `GET /search?q=` returns a fragment for future typeahead/mobile — **stretch**, not blocking. | Fragment renders matching registry rows; boosted nav works. |
| S2-E2-6 | Browser gauntlet | Playwright: open palette, filter, navigate, assert URL + `#page-content` swap. | `uv run pytest tests/browser/test_showcase_search.py -q` |

**Proof:** `uv run pytest tests/test_showcase_registry.py tests/browser/test_showcase_search.py -q`

**Non-goal reminder:** Search indexes **showcase pages**, not every chirp-ui macro in
`manifest.json`.

---

## Epic 3 — App Modularization

**Goal:** Split the monolith `app.py` into maintainable modules without changing URLs.

**GitHub epic title:** `Epic: Showcase v2 — modular app layout`

| Task ID | Title | Description | Acceptance |
|---|---|---|---|
| S2-E3-1 | Extract fixtures | Move `CATALOG_*`, `OPS_*`, `SUPPORT_*`, `TABLE_DATA` into `fixtures/catalog.py`, `fixtures/ops.py`, `fixtures/support.py`, `fixtures/roster.py`. | `app.py` imports fixtures; behavior unchanged. |
| S2-E3-2 | Split route modules | `routes/components.py`, `routes/shells.py`, `routes/screens.py`, `routes/demos.py` — each exports a `register(app)` function. | All 55 routes still resolve; no URL changes. |
| S2-E3-3 | Thin `app.py` | Entrypoint: `AppConfig`, `use_chirp_ui`, template dir, `register_*` calls, `app.run`. | `app.py` ≤200 lines. |
| S2-E3-4 | Shared `_page()` helper | Keep route context (`current_path`, screen titles) in `showcase/helpers.py`. | Shell pages still receive catalog/ops/support context dicts. |
| S2-E3-5 | Import-cycle guard test | Lightweight test that route modules import without circular deps. | `uv run pytest tests/test_showcase_app_structure.py -q` |

**Proof:** `uv run pytest tests/test_showcase_app_structure.py tests/test_data_integration.py -q` (or existing integration tests that hit `/data`, `/catalog-shell`).

---

## Epic 4 — Template & CSS Hygiene

**Goal:** Stop paying for every shell's CSS on every page; shrink `base.html`.

**GitHub epic title:** `Epic: Showcase v2 — scoped showcase CSS`

| Task ID | Title | Description | Acceptance |
|---|---|---|---|
| S2-E4-1 | Audit `base.html` CSS blocks | Inventory `.catalog-shell-*`, `.ops-shell-*`, `.support-shell-*` rules; map each to the routes that need them. | Written inventory in PR description or comment. |
| S2-E4-2 | Extract shell CSS partials | `templates/showcase/_css/catalog_shell.css.html`, `_ops_shell.css.html`, `_support_shell.css.html` included only from those templates (or a `{% block head_extra %}` per recipe). | Gallery pages (`/ui`, `/forms`) do not emit shell CSS in HTML source. |
| S2-E4-3 | Move shared showcase copy styles | Keep only truly global `.showcase-copy*` rules in `base.html`; page-specific layout in page templates. | `base.html` `<style>` block reduced measurably (target: <400 lines). |
| S2-E4-4 | CSS contract test | Assert shell CSS classes appear only on routes flagged `shell_recipe` in registry. | Ratchet prevents re-bloating `base.html`. |

**Proof:** `uv run pytest tests/test_template_css_contract.py tests/test_showcase_registry.py -q`

---

## Epic 5 — Golden Screens & Recipe Clarity

**Goal:** Make high-value reference pages discoverable as a first-class section.

**GitHub epic title:** `Epic: Showcase v2 — golden screens & recipes`

Depends on: Epic 1, Epic 2.

| Task ID | Title | Description | Acceptance |
|---|---|---|---|
| S2-E5-1 | Registry section: Golden screens | Group `/screen-*` entries with archetype tags (`command-center`, `review-queue`, …). | Sidebar section or palette group "Golden screens". |
| S2-E5-2 | Registry section: Shell recipes | Group catalog/ops/support shells with profile tags (`atlas`, `sage`, …). | Search "ops" finds operations shell routes. |
| S2-E5-3 | Landing page hierarchy | Rework `index.html`: Quick demo → Golden screens → Shell recipes → Component gallery (registry-driven). | New visitors see reference implementations before the long tail. |
| S2-E5-4 | Cross-link from docs | Link `docs/patterns/visual-audit-showcase.md` and archetype docs to live golden-screen URLs. | Docs cite Railway URLs where appropriate. |

**Proof:** Manual + `tests/docs_contracts/test_onsite_component_coverage.py` if doc links are ratcheted.

---

## Epic 6 — Deploy & Docs Contract

**Goal:** Keep Railway deploys predictable; document how to add a page post-v2.

**GitHub epic title:** `Epic: Showcase v2 — deploy & contributor docs`

| Task ID | Title | Description | Acceptance |
|---|---|---|---|
| S2-E6-1 | Update `examples/component-showcase/README.md` | Document registry + "add a page" checklist (registry entry → template → route module). | New contributor path is ≤5 steps. |
| S2-E6-2 | Pin Chirp floor in showcase extra | Keep `bengal-chirp>=0.8.0` (CSP nonce auto-wiring); note in README. | `uv lock` + Dockerfile `pip install ".[showcase]"` agree. |
| S2-E6-3 | Railway smoke checklist | Post-deploy: home loads, palette search works, `/catalog-shell` + `/demo` + one golden screen load without CSP errors. | Checklist in README or `docs/plans/` proof section. |
| S2-E6-4 | Changelog entry | Towncrier fragment under `changelog.d/` when saga ships. | CHANGELOG mentions showcase v2 discovery + structure. |

**Proof:** Deploy to Railway staging/production; manual smoke per checklist.

---

## Epic 7 — Optional: Filesystem routing for gallery pages (stretch)

**Goal:** Reduce boilerplate for simple static gallery pages.

**GitHub epic title:** `Epic: Showcase v2 — filesystem gallery routes (optional)`

**Status:** defer until Epics 1–4 land.

| Task ID | Title | Description | Acceptance |
|---|---|---|---|
| S2-E7-1 | Spike: Chirp `pages/` for showcase | Evaluate mounting `examples/component-showcase/pages/` for read-only gallery templates. | Spike doc with go/no-go. |
| S2-E7-2 | Migrate 5 gallery pages | Move low-interaction pages (e.g. `/typography`, `/effects`) to filesystem routes. | URLs unchanged; registry still lists them. |
| S2-E7-3 | Registry sync from filesystem | Auto-register `pages/*.html` or require explicit `_meta.py` per page. | No duplicate route definitions. |

---

## Recommended Execution Order

Phases are dependency-ordered. Recommended PR sequence (max value, lowest risk):

1. **Epic 1** (registry + sidebar/index migration) — unlocks everything else.
2. **Epic 2** (command palette search) — immediate UX win; dogfoods chirp-ui.
3. **Epic 3** (split `app.py`) — parallel-friendly once registry exists.
4. **Epic 4** (CSS scoping) — can overlap with Epic 3.
5. **Epic 5** (landing hierarchy + golden screen grouping) — polish after search works.
6. **Epic 6** (docs + deploy) — ship gate.
7. **Epic 7** (filesystem routing) — only if gallery page count keeps growing.

Each epic is "done" only when its **Proof** commands pass and Railway smoke checklist
(Epic 6) is green.

---

## Proof Loop

| Layer | What it guards |
|---|---|
| Registry ratchet | Every page route ↔ registry entry (`test_showcase_registry.py`) |
| App structure | Thin entrypoint, fixture modules, no import cycles |
| Template CSS contract | Shell CSS not leaked to gallery pages |
| Browser gauntlet | Command palette open → filter → navigate |
| CSP | Inline scripts nonced (`test_app_shell_contract.py`) |
| Railway smoke | Live deploy: search + shells + demo + golden screen |

---

## Mapping to GitHub Issues

Filed as GitHub issues (saga umbrella + seven epics):

| Epic | Issue | Title |
|---|---|---|
| Saga | [#273](https://github.com/lbliii/chirp-ui/issues/273) | `[Saga] Component Showcase v2 — registry, search, modular app` |
| 1 | [#266](https://github.com/lbliii/chirp-ui/issues/266) | `Epic: Showcase v2 — page registry` |
| 2 | [#267](https://github.com/lbliii/chirp-ui/issues/267) | `Epic: Showcase v2 — command palette search` |
| 3 | [#268](https://github.com/lbliii/chirp-ui/issues/268) | `Epic: Showcase v2 — modular app layout` |
| 4 | [#269](https://github.com/lbliii/chirp-ui/issues/269) | `Epic: Showcase v2 — scoped showcase CSS` |
| 5 | [#270](https://github.com/lbliii/chirp-ui/issues/270) | `Epic: Showcase v2 — golden screens & recipes` |
| 6 | [#271](https://github.com/lbliii/chirp-ui/issues/271) | `Epic: Showcase v2 — deploy & contributor docs` |
| 7 | [#272](https://github.com/lbliii/chirp-ui/issues/272) | `Epic: Showcase v2 — filesystem gallery routes (optional)` |

Task IDs (`S2-E1-1`, …) are checklist items inside the epic issues.

---

## Constraints & Risks

| Risk | Mitigation |
|---|---|
| Registry drift vs routes | Ratchet test fails CI if route and registry diverge |
| CSP breaks palette/runtime scripts | Keep `csp_nonce()` on all inline scripts; browser smoke post-deploy |
| Big-bang refactor breaks Railway | Land epics incrementally; URLs must not change in v2 |
| Search scope creep | Explicit non-goal: pages only, not full manifest search |
| `base.html` CSS extraction regressions | Visual spot-check catalog/ops/support shells at 768 + 1440 |

---

## Related Plans & Docs

| Doc | Relationship |
|---|---|
| `docs/patterns/visual-audit-showcase.md` | Static audit page — complementary, not replaced |
| `docs/plans/PLAN-application-chrome-system.md` | Shell recipes in showcase prove this system |
| `docs/plans/PLAN-pre-1.0-productization-saga.md` | Epic 3 "Visible Design-System Showcase" — v2 improves the **live** app half |
| `docs/patterns/navigation.md` | Command palette + shell nav patterns to dogfood |
| `examples/component-showcase/app.py` | Current monolith — refactor target |
| Railway deploy (`railway.json`, `Dockerfile`) | Unchanged target; redeploy after each epic |

---

## Open Questions (resolve at Epic 1 kickoff)

1. **Registry location** — `examples/component-showcase/registry.py` vs package subfolder
   `showcase/` (prefer subfolder if Epic 3 splits land together).
2. **Index page** — keep card grid visual or switch to compact list grouped by section?
3. **Palette placement** — topbar only vs also a home-page hero affordance?
4. **POST/fragment routes** — exclude from registry entirely vs register with `hidden: true`?

Default recommendations: subfolder `showcase/`, grouped card index, topbar palette only,
`hidden: true` for non-nav endpoints.
