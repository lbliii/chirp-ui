# Screen: Product/Docs Home

Status: golden screen fixture
Profile: `ember`
Fixture route: `/screen-product-docs-home`
Source template:
`examples/component-showcase/templates/showcase/screen_product_docs_home.html`
Proof: `tests/test_data_integration.py`,
`tests/browser/test_golden_screen_fixtures.py`

## Use When

Use Product/Docs Home when a product, library, or internal platform needs a
first page with:

- product identity,
- primary and secondary actions,
- proof near the first viewport,
- lifecycle or feature explanation,
- documentation entry points,
- customer or internal-team outcomes,
- closing CTA.

Good fits include docs homes, product-family pages, launch pages, and internal
platform entry pages.

## Do Not Use When

Do not use this screen for dense operational tools, review queues, settings, or
live execution monitors. Use Command Center, Review Queue, Settings Surface, or
Agent Run Monitor instead.

## Composition Map

| Job | Current Surface |
|---|---|
| Profile | `ember` metadata for product/docs/editorial mood. |
| Site shell | `site_shell`, `site_header`, `site_footer`. |
| First viewport | `hero`, action slot, `btn`, `cluster`. |
| Proof | `band`, `container`, `logo_cloud`, `metric_grid`, `metric_card`. |
| Lifecycle explanation | `lifecycle_showcase`, `feature_section`, tabs. |
| Entry points | `index_card` grid. |
| Outcomes | `story_card` grid. |
| Closing action | `cta_band`. |

## Data Shape

The fixture expects:

- product name and value proposition,
- navigation entries,
- proof logos,
- lifecycle stages,
- metrics,
- screen or docs entry cards,
- customer/team stories,
- CTA labels and destinations.

Do not use placeholder product names in final examples. The first viewport
should make the product or offer obvious.

## Required States

- Primary action.
- Secondary action.
- Proof band.
- Lifecycle tabs/panels.
- Entry-card grid.
- Outcome/story cards.
- Closing CTA.

## Agent Guidance

When the user asks for a product page, docs home, library homepage, launch page,
or internal platform landing page, start from this screen before composing
sections manually.

Prefer this screen over a generic hero plus card grid when the page needs proof,
docs entry points, and product narrative in one coherent first screen.

Use the `ember` profile unless the page is an operational tool or review
workspace.

Do not fill the page with explanatory copy about Chirp UI itself. Use real
product content, proof, and entry points.

## Proof Checklist

- Server route renders and exposes `data-screen-archetype="product-docs-home"`.
- Browser proof covers 320, 390, 768, and 1280 widths with no document
  horizontal overflow.
- Browser proof verifies site header, logo cloud, lifecycle showcase, and CTA
  band surfaces are present.

## Extraction Candidates

Track, but do not promote yet:

- `proof_band`
- `screen_header`
- stronger product/docs first-viewport recipe

These need repeated product/docs pages before public API work.
