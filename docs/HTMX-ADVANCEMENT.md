# HTMX Advancement — Design Decisions

Design decisions for the chirp-ui HTMX advancement epic. Each question was
resolved before implementation began.

---

## Q1: Per-field validation — swap target strategy

**Decision: Option A — field_wrapper becomes its own OOB target.**

The wrapper div gets `id="field-{name}"`. Server returns the full wrapper
(label + input + errors) as an OOB fragment. This keeps all field parts in
sync and avoids a second target element.

When forms contain multiple fields with the same `name` (rare, but possible
in nested/repeated forms), callers pass a unique `field_id` override.

---

## Q2: OOB helper — macro vs filter

**Decision: Option A — `oob_fragment(id, swap)` macro.**

Macros compose with `{% slot %}` for block content. Filters cannot wrap
block content in Kida. The macro is a thin wrapper that adds
`hx-swap-oob="{swap}"` to a div.

---

## Q3: Navigation progress — CSS-only vs Alpine

**Decision: Option A — pure CSS triggered by `body.htmx-request`.**

htmx automatically adds/removes the `htmx-request` class on the body during
requests. A CSS-only progress bar respects chirp-ui's "no client JS in macros"
convention and requires zero Alpine.

---

## Q4: Streaming error — recovery scope

**Decision: Option A — retry button only (v1).**

User-initiated reconnect via a button that re-fetches the SSE endpoint.
Automatic exponential backoff deferred to a future version to keep the
initial implementation simple and predictable.
