# Typography And Rhythm Taste Floor

Status: research-backed planning input
Date: 2026-05-24
Plan: `docs/plans/PLAN-visual-taste-floor-saga.md`

This record captures the typography research behind the next visual taste-floor
slice. It does not add public tokens, macro parameters, theme packs, descriptor
fields, generated artifacts, or utility classes. It is evidence for the next
recipe and proof pass.

## Research Finding

The screen catalog raises the visual floor by giving agents and app authors a
complete product situation before they assemble components. Typography is the
next pressure point because a screen can have the right components and still
look like a wireframe when type hierarchy, rhythm, measure, weight, and muted
emphasis are left to ad hoc choices.

The strongest design systems do not treat typography as size utilities. They
ship role-based type decisions:

| Source | Relevant Evidence | Chirp UI Takeaway |
|---|---|---|
| Material 3 typography: `https://developer.android.com/develop/ui/compose/designsystems/material3` | Type is grouped into semantic roles such as display, headline, title, body, and label, with paired size and line-height values. | Chirp needs role vocabulary above `xs/sm/base/lg/xl` before agents can choose polished hierarchy. |
| Fluent 2 typography: `https://fluent2.microsoft.design/typography` | The ramp pairs semantic names with weight, size, and line height, and uses baseline alignment for rhythm. | Chirp roles should be bundles, not independent knobs. |
| Carbon typography: `https://carbondesignsystem.com/elements/typography/overview/` | Carbon separates productive product typography from expressive editorial typography. | Chirp profiles need different type intent for `atlas`/`signal` workspaces versus `ember` product/docs pages. |
| Atlassian typography: `https://atlassian.design/foundations/typography/` | Typography tokens include family, size, and line height, with app and brand contexts separated. | Chirp should distinguish product UI roles from brand/display roles without creating component skins. |
| Primer typography: `https://primer.style/product/getting-started/foundations/typography/` | Primer bundles size, family, weight, and line-height in opinionated typography tokens and discourages arbitrary weights. | Chirp should avoid arbitrary inline font values in fixtures and examples. |
| GOV.UK layout/type scale: `https://design-system.service.gov.uk/styles/layout/` and `https://design-system.service.gov.uk/styles/type-scale/` | Readability is governed by page width, line length, type scale, and line height together. | Chirp needs measure and layout rhythm in the type pass, not only token names. |
| USWDS typography: `https://designsystem.digital.gov/components/typography/` | Typesetting spans microtypography and macrotypography: text styling plus arrangement on the page. | Chirp should evaluate type inside panels, rails, tables, cards, and page shells. |
| WCAG text spacing: `https://www.w3.org/WAI/WCAG21/Understanding/text-spacing.html` | Layouts must survive user text-spacing overrides without clipped, hidden, or overlapping content. | Dense Chirp screens need proof that text rhythm remains accessible under stress. |

## Local Evidence

Current Chirp UI typography has useful foundations:

- `docs/fundamentals/typography.md` separates UI, Prose, and Code scales.
- `docs/theming/app-theme.md` identifies typography as a first override job.
- `src/chirp_ui/templates/chirpui.css` exposes font family, font size,
  line-height, prose measure, code, and weight tokens.
- The golden screens in `docs/screens/` give real product contexts for type
  proof instead of isolated specimen rows.

The gap is that current guidance still mostly exposes size buckets:

- UI and prose scales are named by size rather than role.
- Core font sizes use viewport-driven `clamp()` values, which can make dense app
  hierarchy drift with viewport width.
- Line-height is largely `tight`, `normal`, or `relaxed`, not tied to roles,
  measure, or content length.
- Metadata, captions, status text, metrics, logs, labels, page titles, panel
  titles, and proof copy do not yet have a shared role system.
- Existing typography utility classes are compatibility surface, not the
  preferred way to author polished screens.

## Role Taxonomy

These names are planning vocabulary only. They do not authorize public token
names or macros until a stop-and-ask promotion plan exists.

| Role Family | Candidate Roles | Job |
|---|---|---|
| Structure | `display`, `page-title`, `section-title`, `panel-title`, `card-title`, `object-title` | Establish screen hierarchy without relying on generic heading size changes. |
| Reading | `body`, `dense-body`, `lead`, `caption`, `helper`, `prose-body` | Make short UI copy, dense content, and long-form content read differently. |
| Metadata | `metadata`, `timestamp`, `owner`, `provenance`, `route`, `count-label` | Give secondary information dignity without making it invisible. |
| Controls | `button-label`, `nav-item`, `tab-label`, `field-label`, `menu-item` | Keep interaction labels aligned, legible, and stable across components. |
| State | `status-label`, `severity-label`, `validation-text`, `loading-text` | Make state text recognizable without color-only emphasis. |
| Data | `metric`, `metric-unit`, `table-cell`, `table-header`, `axis-label` | Keep numbers, labels, and dense tabular text stable and scannable. |
| Technical | `code-inline`, `code-block`, `log-line`, `trace-label` | Support agent, build, docs, and observability contexts. |
| Expressive | `hero-display`, `proof-copy`, `story-heading`, `cta-heading` | Let `ember` and site/product pages feel polished without leaking marketing type into dense apps. |

## Taste Laws For Type

1. Type roles are bundles: family, size, line-height, weight, emphasis color,
   measure, and intended context move together.
2. App UI should prefer stable rem-based role sizes; responsive display type
   belongs mainly to expressive and editorial contexts.
3. Font choice follows role clarity. Do not add a font dependency to compensate
   for missing hierarchy.
4. Muted text is hierarchy, not disabled text. It must remain legible and useful.
5. Letter spacing is a precise tool. Keep it conservative, avoid negative
   tracking outside display roles, and never use it to fake font quality.
6. Line height depends on content length and measure. Dense labels, one-line
   controls, two-line descriptions, and reading prose need different rhythm.
7. Metrics and logs need dedicated treatment. They should not inherit generic
   title or body styling by accident.
8. Accessibility stress is part of taste. Text-spacing overrides must not clip,
   overlap, or hide meaningful content.

## Execution Slices

### Slice 1. Typography Audit

- Inventory current typography token use in CSS partials, theme packs, examples,
  and the four golden screens.
- Flag arbitrary inline font sizes, raw font weights, negative letter spacing,
  viewport-driven type in dense UI, and muted text that fails hierarchy.
- Classify each finding as token gap, role gap, recipe gap, component gap, or
  fixture-only cleanup.

Proof:

- Docs ratchet for this research record and plan references.
- Focused grep/audit output recorded in the follow-up implementation note.

### Slice 2. Role Matrix

- Draft a role matrix that maps candidate roles to current tokens and screen
  surfaces.
- Keep the matrix recipe-only until repeated screen evidence justifies public
  token names.
- Identify profile-specific overrides for `atlas`, `sage`, `signal`, and
  `ember` without changing packaged theme packs.

Proof:

- Docs/source-map tests when the matrix becomes durable guidance.
- No generated CSS or manifest changes unless token promotion is approved.

### Slice 3. Golden Screen Type Pass

- Revisit each golden screen with the role matrix.
- Improve hierarchy, metadata rhythm, metrics, logs, and prose measure using
  existing tokens and local recipes first.
- Record every repeated workaround as an extraction candidate.

Proof:

- Browser overflow proof for 320, 390, 768, and 1280 widths.
- Text-stress fixture or browser assertion for long labels and metadata.

### Slice 4. Token Promotion Decision

- Stop and ask before adding public typography role tokens, changing existing
  token defaults, adding a font dependency, or altering theme-pack contracts.
- If approved, promote only repeated semantic roles with migration notes,
  generated CSS updates, token catalog updates, docs, examples, and tests.

Proof:

- `uv run poe build-css-check`
- `uv run poe build-manifest-check` if generated metadata changes.
- `uv run pytest tests/test_template_css_contract.py tests/test_registry_emits_parity.py -q`

## Not Now

- New public typography macro.
- New utility classes for type roles.
- New font dependency or bundled web font.
- Token default changes for the core UI/prose scale.
- Manifest schema for type roles.
- Figma or design-token export tooling.
