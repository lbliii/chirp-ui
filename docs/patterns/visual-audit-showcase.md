# Visual Audit Showcase

Status: active practice
Date: 2026-05-12

The visual audit showcase is the answer to "can we see the impact?" It gives
the project a single static page for judging whether Chirp UI feels like a
coherent design system rather than a pile of correct components.

Open:

```text
examples/design-system-gap-showcase/index.html
```

For interactive golden screens and shell recipes on a live Chirp app, use the
Railway component showcase:

```text
https://chirp-ui-showcase-production.up.railway.app
```

Golden-screen fixtures:

- [Command Center](https://chirp-ui-showcase-production.up.railway.app/screen-command-center)
- [Review Queue](https://chirp-ui-showcase-production.up.railway.app/screen-review-queue)
- [Agent Run Monitor](https://chirp-ui-showcase-production.up.railway.app/screen-agent-run-monitor)
- [Product/Docs Home](https://chirp-ui-showcase-production.up.railway.app/screen-product-docs-home)

See also `docs/screens/README.md` for archetype selection guidance.

The page is intentionally static. It should work by opening the HTML file in a
browser, with no dev server and no app backend.

## What It Proves

The page should make these qualities visible:

- token contrast in light, dark, and app-owned theme contexts,
- theme profile comparison for app starter, holy-light, and chirp-theme,
- token explorer coverage for first app-owned overrides,
- command palette, modal, and drawer visual chrome,
- ASCII/TUI controls and data-table density,
- proof patterns for logo clouds, story cards, and CTA bands,
- component state consistency across default, hoverable, active, loading,
  reserved, success, warning, and error treatments,
- dense navigation layer discipline,
- application chrome rhythm: app shell, rails, route rows, command surfaces,
  tray/drawer overlays, and page tools should feel related without merging
  their semantics,
- form density and validation state polish,
- surface nesting and scoped CSS behavior,
- long-label and narrow-viewport resilience,
- whether experimental patterns are visually mature enough to promote.

## Audit Checklist

Run the page at these widths:

| Width | What to check |
|---:|---|
| 1440 | Dense chrome, token boards, and component grids should feel balanced and not sparse. |
| 1024 | Sidebar-like and dashboard sections should keep readable hierarchy. |
| 768 | Cards and controls should wrap without overlapping or truncating important text. |
| 390 | Buttons, badges, inputs, and dense navigation should remain tappable and legible. |
| 320 | Long labels and counts should wrap or reserve space without escaping containers. |

Check both default and dark/system theme modes when the browser or page supports
them.

For application chrome, inspect these rhythm checks before adding new API:

- mixed controls share coherent block size and touch targets,
- rails do not starve the primary content pane at tablet widths,
- route tabs scroll instead of wrapping into a tall block,
- tray/drawer overlays have clear elevation and reachable close controls,
- reserved/loading badges keep layout stable without announcing incorrect
  counts,
- token-backed spacing and borders do the work instead of utility-style helper
  classes.

Use this rhythm matrix for application chrome slices:

| Surface | Rhythm contract | Proof |
|---|---|---|
| Global shell and command row | Brand, search, utilities, and primary actions share a coherent control height without merging route and command semantics. | Browser-visible command trigger, primary action, and no overlap at 320, 390, 768, and desktop widths. |
| Product rail | Persistent broad navigation stays useful on tablet and desktop without starving the main pane. | Rail width leaves the main pane readable at 768 and 1024; phone fallback uses drawer or tray. |
| Object context | Breadcrumbs, title, metadata, and object actions wrap or collapse before widening the page. | Breadcrumb overflow remains navigable and object action controls stay reachable. |
| Local route row | URL-backed route links stay horizontally scrollable under dense labels and badges. | Route tabs keep `nowrap`, bounded height, and intended horizontal overflow. |
| Page tools | Filters, sort, export, refresh, and bulk actions read as page-local controls rather than product navigation. | Page toolbar has a labelled command/action surface and does not duplicate global actions. |
| Overlay chrome | Drawer, tray, command palette, and modal surfaces show clear elevation, focus behavior, and close affordances. | Open/focus/close proof covers click and keyboard behavior for the overlay used by the recipe. |
| Attention states | Reserved/loading badges hold space without announcing false counts. | Badge placeholders are dimensioned, hidden from assistive tech when empty, and visible counts have accessible labels. |

Browser proof lives in `tests/browser/test_visual_audit_showcase.py`. It opens
the page through `file://` so the test preserves the no-server contract while
checking horizontal overflow and required audit sections at phone, tablet, and
desktop widths.

## Promotion Rule

Before promoting an experimental component, add it to the visual audit page or
to an equivalent browser-tested recipe. If it cannot survive the audit page with
realistic content, keep it experimental or recipe-only.

## Maintenance

- Keep the page focused on visual inspection, not product marketing.
- Prefer real Chirp UI classes and emitted component markup over fake mockups.
- Do not add explanatory in-app copy; use this document for instructions.
- When a component receives a major visual change, update the page if it is one
  of the core audited surfaces.
