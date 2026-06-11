# PLAN: Content-Type Refinement (chirp-theme)

**Status:** proposed · **Scope:** `src/bengal_themes/chirp_theme/` content-type templates + CSS
**Sibling plans:** [PLAN-chirp-theme-content-parity](PLAN-chirp-theme-content-parity.md), [PLAN-application-chrome-system](PLAN-application-chrome-system.md), [PLAN-visual-taste-floor-saga](PLAN-visual-taste-floor-saga.md)

## The principle

> **Docs is the craft *floor*, not the layout *template*.**
> *"I really like how our docs pages render. But that doesn't mean everything should look like a techdocs website."* — project owner

What makes docs feel premium is a small, repeatable **type-and-accent system** — a mono accent eyebrow, a clamped display title, **one** left-accent device per surface (hero gutter / code rib / TOC guide-rail), quantified objects (count pills, kind glyphs, meta chips), calm aria-driven interactive states, and hairline-plus-whitespace rhythm. It is **not** the three-column reading-shell structure. Every content type inherits that craft and earns the same restraint, while choosing its **own** layout from the taxonomy.

**Divergence rules:**
1. Reserve the three-column reading shell (icon catalog-rail + section tree + right Page-map TOC) for **docs and api only**. No other type emits `chirp-theme-docs-layout` / `docs-nav` / `docs-toc-sidebar`.
2. Re-skin the **one** accent device per type — don't drop it, don't multiply it. Docs = flat left gutter bar; changelog/releases = vertical timeline rib; blog = warm rule + author avatar; resume = no accent (print-clean); authors = avatar ring.
3. Move **quantification** to each type's natural axis: TOC counts headings; a blog meta rail counts reading-time/tags; a release rail counts versions; a catalog header counts results. Same count-pill + mono-mark + soft-active-glow vocabulary, different axis.
4. Choose **prev/next scope** to match the content's mental model (`page_navigation` already supports this): blog → Older/Newer, releases → Previous/Next release, tracks → Previous/Next lesson.

**Anti-patterns:** don't reuse the docs 3-col grid for editorial/document types; don't hide the desktop topbar for a type that renders no rail; **don't ship per-type class hooks with zero matching CSS** (inert hooks are debt — wire or strip); don't copy the docs Page-map TOC literally onto editorial content.

## How this plan was produced (and what's *verified*)

- **Structural audit** (11 agents) — every content-type template, controls, shell wiring.
- **Design pass** (10 agents) — docs craft extraction + per-type identity system + build-ready specs.
- **Built the site** (`poe docs-build`, 126 pages, 0 health failures) and **captured 16 screenshots** (desktop + mobile) at `localhost:8847` → `.context/screenshots/` (gitignored).

The screenshots **corrected the code-only audit in three places** — see *Verified corrections* below. Where render reality and code analysis disagree, **render wins**.

## The shell model (topbar vs side rail), made explicit

`base.html` is the only shell: it always *renders* a topbar `<header>`, then `<main>{% block content %}`. There is **no left rail in the base** — each template composes its own rail inside the content block. The only automatic topbar→rail switch is `chirp-theme-shell--rail-only`, **hardcoded to URL prefixes `/docs/`, `/api/`, `/releases/`** (`base.html:412`); on desktop (≥769px) it sets `.chirp-theme-shell__header { display:none }` (`chirp-theme.css:445`) and on mobile the rail collapses and the topbar returns. So docs = **rail-only on desktop, topbar on mobile** (they swap).

Think in **three independent toggles**, not one fuzzy choice:

| Toggle | Options |
|---|---|
| Topbar | shown / hidden-on-desktop |
| Left rail | none / section-tree / lesson-stepper / meta-rail |
| Right TOC | yes / no / optional |

**Named layouts** (pick one per type):

- **Reading shell** — no topbar (desktop) · section-tree rail · right TOC → **docs, api**
- **Course shell** — topbar · lesson-stepper rail · right TOC → **tracks**; **tutorial** (lighter, no right TOC)
- **Editorial shell** — topbar · centered prose · optional right meta rail → **blog**
- **Register/Log shell** — topbar · centered · optional version/date jump-rail → **releases, changelog**
- **Document shell** — topbar · narrow centered, print-aware → **resume, notebook**
- **Catalog shell** — topbar · centered card grid → **all list/index pages**
- **Profile shell** — topbar · centered, avatar-led → **authors**

**Foundation fix that unlocks the rest:** replace the hardcoded URL-prefix `_page_is_catalog_shell` with a **declarative cascade/frontmatter flag** + a shared `{% block sidebar %}` in `base.html`. Then each type *declares* its layout instead of base guessing by URL — and the `/releases/` half-state goes away.

## The identity system (the dials)

Today every type shares **one** accent (teal), **one** hero skin, **one** width (72/68ch). Make identity systematic via per-surface dials set on the layout root (`[data-chirp-theme-surface="<type>"]` — the hook already ships on every type; tracks already proves it at `tracks.css:97`):

| Axis | Mechanism |
|---|---|
| **accent** | re-point `--chirpui-accent` (+ contrast-checked `--chirpui-on-accent`, light+dark) via a `--type-accent` alias inside the surface block — recolors links/badges/focus/hero-rule for free |
| **hero-skin** | named skins as CSS recompositions of the existing page_hero slots, scoped per surface (or a `skin=` param upstreamed to chirp-ui) |
| **width** | a `--type-measure-{prose,docs,wide,log,document,profile}` scale; generalize the lone api-72rem override |
| **density** | a `--type-rhythm` scalar scaling section/paragraph gaps |
| **typography** | `--type-heading-font/weight` per surface (the Instrument Serif display face ships but nothing routes it per type) |
| **texture** | per-surface background/pattern driven by `--type-accent` |
| **motion** | per-surface opt-in to animated hero (already reduced-motion-guarded globally) |

### Per-type identity matrix

| Type | One-line feel | Accent | Hero | Width | Density |
|---|---|---|---|---|---|
| **docs** | utilitarian reading instrument (the bar) | teal (keep) | compact label-led | 75ch | standard |
| **blog** | warm editorial magazine | warm clay/amber | serif masthead + byline | 68ch | airy |
| **tracks** | self-paced course | teal-tinted | left-rule course card | 75ch | compact-standard |
| **releases** | version register / git-tag ledger | cool slate/indigo | ledger header (mono version) | 60ch | compact |
| **changelog** | dated narrative log | cool slate/indigo (sibling) | quiet editorial masthead | 60ch | compact |
| **authors** | contributor profile + directory | muted violet | avatar-led profile | 64ch | standard |
| **notebook** | computational notebook | code-green | run-context/kernel header | 68ch (wide code) | airy |
| **resume** | printable CV | near-neutral ink | name-block, no hero | 48–52rem | tight-print |
| **tutorial** | guided lesson sequence | teal-secondary | lesson-progress header | 68ch | airy |

## Shared foundation work (do once, benefits all)

| # | Item | Effort | Files (primary) |
|---|---|---|---|
| F1 | **Per-surface accent token system** — new `components/type-identity.css`; map `--chirpui-accent`→`--type-accent` per surface; dark-mode + contrast pairs | M | `type-identity.css` (new), `style.css`, `tests/test_theme_token_parity.py` |
| F2 | **Declarative rail flag + shared `{% block sidebar %}`** — replace the URL-prefix hardcode; fixes the `/releases/` half-state | L | `base.html:412,486`, `chirp-theme.css:445` |
| F3 | **Width + density scale tokens** — `--type-measure-*`, `--type-rhythm`; fold the api-72rem special-case in | M | `chirp-theme.css`, `type-identity.css`, `reference.css` |
| F4 | **Hero-skin variants** — editorial-masthead / ledger / profile / run-context / lesson-progress / document-head | L | `page-hero.css` or `type-identity.css` (+ optional chirp-ui `skin=` param) |
| F5 | **Wire-or-strip inert hooks** — every `chirp-theme-{type}-*` / `-learning-*` hook gets real CSS or is removed; add a CI contract guard | L | `type-identity.css`, the type templates, `tests/` |
| F6 | **Per-type proof page + browser snapshots** — one route showing every surface; Playwright/axe incl. "releases keeps nav" | M | `site/` showcase route, `tests/browser/` |

## Per-type plans

> Full build-ready specs (controls, css_work, template_work, partials_to_wire/remove, content_contract, definition_of_done) live in the design workflow output (`wf_ec118e59-cef`). Below is the actionable essence.

### tracks — Course shell — effort **M** — *highest ROI, start here*
The CSS is done (772 lines, token-clean). It reads "broken" because the **dynamic layer is unwired**.
- **P0:** add `<script defer src="{{ asset_url('js/enhancements/tracks.js') }}">` to `base.html` script block (~L580). Revives scroll-spy current-lesson highlight, visited/completed ticks, localStorage progress, resume banner — and makes the existing `tests/browser/test_track_dogfood.py` pass.
- **P0:** fix the mobile rail toggle — `interactive.js:413` hardcodes `#docs-sidebar` but the rail is `#track-sidebar` (generalize to read `aria-controls`).
- **P1:** left-align the hero (override the centered chirpui editorial defaults *only* under `[data-chirp-theme-surface="track"]`) so the accent bar connects to text; make hero progress reflect real position instead of hardcoded `Step 1`.
- *Mobile note:* the pillar page is ~13,000px tall on mobile with the rail dumped inline above content — collapse the rail to a `<details>`/drawer.

### blog — Editorial shell — effort **L**
- **Stop borrowing the docs grid.** `blog/shell.html:6` uses `chirp-theme-docs-layout` + emits `docs-nav` → a blog post literally renders with the docs left rail. Replace with a centered editorial column, topbar at all breakpoints, no section-tree rail, optional sticky right meta-rail on wide single posts.
- **Flip the feature flags** — `content.author` + `content.excerpts` are OFF in `theme.yaml`, so post cards silently drop byline + excerpt though the data exists. Single biggest "data exists but hidden" fix.
- **Wire the orphaned partials** — `blog_post_meta`, `author_bio` (currently shadowed by a local var and never called), one share component, optional newsletter/comments. Remove the duplicate rich `related_posts`.
- **Re-skin the hero** — serif display title, warm accent wash, no left spine bar, no mono version pill (today it's a near-verbatim docs-hero clone).
- ⚠ **Verified bug:** the "More to Read" / related section renders **malformed** (raw text/code overflow) on single posts — diagnose during the wiring work.

### releases — Register/Log shell — effort **M** *(after a wiring decision)*
- ⚠ **Verified correction:** `/releases/` is `type: page` → renders via the **generic doc section-index** (rail + rail-only) and *looks like docs*; release detail pages are default `doc` → `doc/single.html`. The bespoke `releases/list.html` (timeline) + `releases/single.html` are **orphaned** (nothing sets `type: releases` or a `template:`).
- **Decision required:** (a) **wire the bespoke register** — set `type: releases`/cascade, adopt the declarative-rail foundation (F2) so it keeps the topbar — then ship the register design below; or (b) keep the doc-section treatment and **delete the orphans**. Recommended: **(a)** — releases shouldn't look like techdocs.
- If (a): semver grouping (0.9.x / 0.8.x), latest-release callout band, version jump-rail, **semver-correct sort** (today sorts by date string — breaks at 0.10.0), tier badges (non-color-only), drop or wire the decorative filter, releases RSS. Fence the work under `versioning.css:416+` (don't touch the unrelated version-selector subsystem).

### changelog — Register/Log shell — effort **M**
- Correctly wired (`type: changelog` cascade) — but **zero changelog CSS** (all hooks inert → monochrome) and it carries **release framing** (`v0.9`, "Released… stable", version/GitHub/Download) that collides with releases.
- Add `components/changelog.css`: month/year **date grouping** with sticky headers; **category chips** (Added/Changed/Fixed) on the *list* (today only on single, only with structured frontmatter — 2/3 sample entries use `## Added` markdown so the UI never fires); style the inert `--{category}` accent classes (non-color-only).
- Strip the semver/release vocabulary from `changelog/single.html`; drop the dead filter box.

### authors — Profile shell — effort **M**
- **Wire the avatar** — `profile_header`'s avatar slot is never filled, so the page has no portrait (the single reason it reads like a tag archive). Source from `avatar:` frontmatter, initials fallback.
- Replace the **degenerate metric** (`metric_card(value=author_name, label="Author")` pipes a name through a numeric KPI slot) with a `role` overline; keep only a real `Published N` stat.
- Social links → **icon buttons**, not muted text pills. Directory cards → avatar-led people cards (not `term_resource_card` borrowing `tags.css`).
- Resolve the two-template duplication (`author.html` real vs `authors/single.html` 1-line alias); wire-or-remove the dead `author-bio.html` (+ its orphaned CSS).

### notebook — Document shell (+ optional cell-navigator) — effort **L–XL**
- **Zero notebook CSS**; body is generic `content | safe` prose — no In[n]/Out[n] cells, exec counts, or cell chrome. The "first-class notebook layout" changelog claim overstates reality.
- Theme-side: `components/notebook.css`, kernel-status header (replace info-blue badge), code-green accent, faint grid texture, print-aware.
- **Framework dependency:** a real per-cell renderer needs Bengal to expose `params.notebook.cells` (`[{type, source, outputs, execution_count}]`). Until then, ship the chrome + a copy/Colab/download affordance and **soften the changelog claim**. Flag the cells API to Bengal.

### resume — Document shell — effort **M**
- **Zero resume CSS** (5 inert hooks); renders as a wide, airy generic profile. The template reads `headline/role/location/summary` params the sample doesn't supply, and **ignores the `bio` field the sample *does* set**.
- `components/resume.css`: narrow ~48rem column, dense rhythm, small-caps section rules, **real print block** (`@page` margins, page-break-inside:avoid, hide topbar+footer+Print-button). ⚠ Footer print-leak: the chirp-theme footer has no `role="contentinfo"` so it prints — fix theme-side.
- Reconcile the `bio`/`headline`/`summary` contract; add a Print/Download button; switch the index off the generic 3-col profile-card grid.

### tutorial — Course shell (lighter, no right TOC) — effort **L**
- ⚠ **Verified correction:** the code-audit predicted a leaf step page shows "0 steps + a spurious empty grid." **The render does not show that** — `/tutorial/01-…/` renders a stepper (2 steps, step 1 active), the body, and a bottom 2-step card grid. So it's **functional but unpolished/redundant**, not broken-empty. (The template resolves the step set on the leaf; the "page.children is empty" assumption is wrong for how it renders.)
- Real work: wire **prev/next pager** (`page_navigation` exists and already supports `type=tutorial` — just never imported); derive `current_step` from sibling position instead of hardcoded `1`; add a real **lesson-stepper left rail**; **dedupe** the redundant bottom step-card grid against the stepper; `components/tutorial.css` for the inert `-learning-*`/`-tutorial-*` hooks; document the tracks-vs-tutorial distinction; delete the dead `series-nav.html`.

## Verified corrections (render vs code-audit)

| Area | Code-audit claimed | Render/build reality |
|---|---|---|
| **releases** | `releases/list.html` renders `/releases/`; rail-only hides topbar with no rail (bug) | `/releases/` is `type: page` → **generic doc section-index** (has rail, looks like docs); bespoke release templates are **orphaned**; releases detail = `doc/single.html` |
| **tutorial** | leaf shows "0 steps" + spurious empty grid | leaf renders stepper(2) + body + **redundant** step-card grid; functional-but-unpolished, not empty |
| **blog** | techdocs rail + missing byline/excerpt | confirmed — **plus** the "More to Read" section renders malformed (raw text overflow) |
| **topbar nav** | no main menu → auto-nav | a **configured** main menu renders (Documentation, Tutorial, Learning tracks, Blog, Resume, Notebooks, Authors, Changelog, Dev, Releases) |
| **changelog** | wired but no CSS | confirmed wired (`type: changelog`); decent structure but monochrome (inert classes) + release-framed |

## Recommended Execution Order

1. **Tracks revival** (P0, M) — load `tracks.js` + fix mobile toggle. Verified, near-one-line, turns "broken" into "working." *Start here.*
2. **Shell foundation** (F2, L) — declarative rail flag + shared `{% block sidebar %}`; resolves the releases wiring question and de-risks every type shell.
3. **Identity foundation** (F1+F3+F5, M+M+L) — per-surface accent system, width/density scales, and wire-or-strip the inert hooks. This is the "make each feel distinct" engine; do it before per-type polish.
4. **Blog → a blog** (L) — flip flags, drop docs rail, editorial shell, wire byline/share/related, fix the "More to Read" bug.
5. **Releases + changelog** (M+M) — the register/log family + the identity split between them (depends on F2 for releases).
6. **Authors + resume** (M+M) — avatar/profile; narrow print-aware CV.
7. **Tracks hero polish + tutorial** (P1, L) — course-shell refinements.
8. **Notebook** (L–XL) — chrome now; real per-cell renderer when the Bengal `params.notebook.cells` API lands.
9. **Proof** (F6, M) — per-surface showcase route + browser/axe snapshots as the visual regression gate.

## Definition of done (cross-cutting)

- No content type (outside docs/api) emits `chirp-theme-docs-layout` / `docs-nav` / `docs-toc-sidebar`.
- No inert per-type class hooks ship (CI contract guard enforces it).
- Each type visibly diverges from the docs look in a side-by-side screenshot, while matching its craft (token-only CSS, visible focus, contrast pairs, reduced-motion).
- `poe ci` green; `poe test-browser-chrome` + the per-surface snapshot job green.
