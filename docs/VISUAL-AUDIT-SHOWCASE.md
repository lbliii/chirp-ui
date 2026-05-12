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
