---
title: Component showcase
description: Live, interactive gallery of every chirp-ui macro and pattern
draft: false
weight: 5
# Hidden from the auto-discovered top nav: the "Component showcase" link is
# defined explicitly in site/config/_default/menu.yaml so it can point at the
# live Railway showcase app instead of this internal /showcase/ route (#245).
menu: false
type: page
template: page.html
lang: en
keywords: [chirp-ui, showcase, gallery, components, macros, patterns]
---

# Component showcase

The full, interactive showcase is the real `examples/component-showcase` Chirp app,
deployed as a live service. Click through every macro, shell, form, island, and
streaming demo running against the actual server runtime — htmx swaps, SSE, and
Alpine behave exactly as they would in your own app.

→ **[Open the live showcase ↗](https://chirp-ui-showcase-production.up.railway.app)**

Prefer reading to clicking? [Browse the component reference](/docs/components/) for the
full catalog with usage guidance, options, variants, and source links.

The specimens below are rendered inline from the component registry as a quick,
zero-dependency preview of the design language.

## Live specimens

{{< component_specimen name="toggle_group" title="Toggle group" description="Visible grouped options for compact single or multiple choice." >}}

{{< component_specimen name="slider" title="Slider" description="The standalone range primitive outside full form-field chrome." >}}

{{< component_specimen name="data_table" title="Data table" description="A parent wrapper for filters, table rows, empty state, and pagination." >}}

{{< component_specimen name="item" title="Item" description="Reusable row anatomy for result lists, menu rows, and command surfaces." >}}

{{< component_specimen name="kbd" title="Keyboard key" description="Inline key and chord rendering." >}}

{{< component_specimen name="separator" title="Separator" description="Semantic or decorative separation with optional label." >}}

Browse the [component reference](/docs/components/) for the full catalog with usage
guidance and source links.
