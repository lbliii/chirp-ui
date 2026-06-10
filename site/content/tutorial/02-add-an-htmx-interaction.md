---
title: "Step 2 — Add an htmx interaction"
description: Wire a button to swap a fragment without reloading the page.
draft: false
weight: 20
lang: en
keywords: [chirp-ui, htmx, swap, fragment, button]
---

## Make a button talk to the server

The `btn` macro accepts an `hx` dict, so a single call describes the whole
request: where it posts, what it targets, and how the response is swapped.

```jinja
{% from "chirpui/button.html" import btn %}

{{ btn("Refresh", hx={"get": "/widgets/latest", "target": "#widget", "swap": "innerHTML"}) }}

<div id="widget">
  {% include "partials/widget.html" %}
</div>
```

## What happens on click

htmx issues the request, the server returns just the widget fragment, and htmx
swaps it into `#widget`. The rest of the page — scroll position, focus, any
Alpine state — is untouched. No full reload, no client framework.

That is the whole loop: render HTML on the server, target a region, swap the
response. From here you can layer in forms, out-of-band updates, and
server-sent events using the same attribute vocabulary.
