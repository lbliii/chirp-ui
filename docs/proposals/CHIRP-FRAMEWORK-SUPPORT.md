# Proposal: Framework Support For Safer Chirp UI Showcase + Fragment Workflows

During the recent `chirp-ui` showcase sweeps, most issues were fixable inside
`chirp-ui`: layout primitives, CSS contracts, component descriptors, manifest
drift, and stale examples. However, the work exposed a few places where Chirp
itself could provide stronger framework-level support and prevent runtime-only
failures.

## Context

The `chirp-ui` showcase now functions as more than a demo. It is effectively a
contract test for component macros, app-shell layout behavior, HTMX fragments,
route-backed navigation, islands, generated CSS, and manifest-backed component
metadata.

While updating the showcase, we repeatedly found useful upstream primitive gaps
in `chirp-ui`, but one class of problem belongs closer to Chirp: framework
render context and fragment safety.

## Primary Ask: Fragment/Block Render Diagnostics

We hit a concrete issue on `/islands/remount`.

The page rendered normally, but the fragment route failed because the fragment
block referenced macros imported inside `{% block main %}`. When Chirp rendered
only the named fragment block, those imports were unavailable.

Example shape:

```jinja
{% block main %}
{% from "chirpui/surface.html" import surface %}

{% block island_mount %}
  {% call surface() %}
    ...
  {% end %}
{% end %}
{% end %}
```

The full page worked. The fragment route failed at runtime because `surface` was
not in scope when rendering `island_mount` directly.

We fixed this in `chirp-ui` by moving fragment-needed imports to top-level scope,
but Chirp/Kida could help catch this earlier.

### Request

Add diagnostics for fragment/block rendering that can detect when a named
fragment block references symbols only defined inside another block's local
scope.

The ideal warning/error would say something like:

> Fragment block `island_mount` references `surface`, but `surface` is imported
> inside `block main`. Move imports required by fragment blocks to template top
> level.

### Why This Matters

Fragment routes are a key Chirp pattern. They are easy to make accidentally
dependent on full-page render context. The failure mode is subtle: the page
route works, but the fragment route 500s.

This is especially risky for:

- HTMX remount fragments
- island remount targets
- partial update routes
- dashboard widgets
- form fragments
- route-tab content fragments

## Secondary Ask: Route/Fragment Smoke Test Utility

It would be useful for Chirp to expose a small test helper that can enumerate or
register app routes and assert expected render modes.

Desired capabilities:

- Assert full routes return `200`.
- Assert fragment routes return `200`.
- Assert a route renders as full page vs fragment intentionally.
- Surface template render errors with route name, template name, block name, and
  render intent.

`chirp-ui` has local smoke tests for showcase routes now, but this seems broadly
useful for Chirp apps.

## Secondary Ask: App Shell Layout Context

Some UI primitives need to know the available main content region rather than
the viewport. Example: `chirpui-blade` previously used `100vw`, which caused
full-width sections to slide under the sidebar in an app shell.

We fixed this with shell-scoped CSS, but Chirp could provide stable app-shell
context hooks or CSS variables such as:

```css
--chirp-shell-main-inline-size
--chirp-shell-sidebar-width
--chirp-shell-content-inline-start
```

This would let design systems build shell-aware primitives without depending on
private shell class structure.

## Secondary Ask: Island Root Class/Class Merge Convention

`chirp-ui` added a default `chirpui-island-root` class so islands have a stable
styling hook. Chirp's `island_attrs` / `primitive_attrs` could formalize class
merging or default root-class behavior.

Desired behavior:

- Always preserve library-provided root class.
- Merge user classes predictably.
- Avoid each component library inventing its own wrapper convention.

This is not urgent, but it would make framework-agnostic islands easier to style
consistently.

## Suggested Priority

1. Fragment/block scope diagnostic: highest value, prevents real runtime 500s.
2. Route/fragment smoke helper: high value, gives apps a simple safety net.
3. Shell context variables/hooks: medium value, helps design systems avoid
   brittle shell-aware CSS.
4. Island class merge convention: medium/low value, mostly ergonomics and
   consistency.

## Conclusion

No hard blocker exists right now. `chirp-ui` can work around the current gaps.
But Chirp can make these patterns safer by making fragment render context, shell
context, and island root contracts more explicit.

The main principle: if Chirp encourages named fragments, HTMX partials, islands,
and app-shell composition, it should also provide diagnostics and test helpers
that make those contracts visible before runtime.
