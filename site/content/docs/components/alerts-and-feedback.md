---
title: Alerts and feedback
description: alert, toast, callout, empty, skeleton, spinner, progress
draft: false
weight: 15
lang: en
type: doc
keywords: [chirp-ui, alert, toast, skeleton]
icon: bell-ringing
---

# Alerts and feedback

Components for status messages, loading states, empty placeholders, and transient notifications.

## Quick reference

| Template | Macro(s) | Role |
|----------|----------|------|
| `alert.html` | `alert` | Inline status message (variants: info, success, warning, error) |
| `callout.html` | `callout` | Editorial inset box for tips, notes, warnings |
| `toast.html` | `toast_container`, `toast` | Transient htmx OOB notifications |
| `confirm.html` | `confirm_dialog`, `confirm_trigger` | Confirmation modal for destructive actions |
| `empty.html` | `empty_state` | Zero-data placeholder |
| `empty_panel_state.html` | `empty_panel_state` | Compact empty state for panels |
| `progress.html` | `progress_bar` | Determinate progress indicator |
| `skeleton.html` | `skeleton` | Loading placeholder with shimmer |
| `spinner.html` | `spinner`, `spinner_thinking` | Indeterminate loading indicators |

---

## Alert

Status alert with optional dismiss button, collapsible mode, and an `actions` named slot.

```text
alert(variant="info", dismissible=false, icon=none, title=none, cls="", collapsible=false, open=true)
```

**Variants:** `info` (default), `success`, `warning`, `error`

```text
{% from "chirpui/alert.html" import alert %}

{# Basic alert #}
{% call alert(variant="success") %}
    Done! Your changes have been saved.
{% end %}

{# Dismissible with action slot #}
{% call alert(variant="error", dismissible=true) %}
    Something went wrong.
    {% slot actions %}<button>Retry</button>{% end %}
{% end %}

{# Collapsible, starts closed #}
{% call alert(variant="warning", collapsible=true, open=false, icon="warning", title="Shortcut collisions") %}
    Long warning content revealed on expand.
{% end %}
```

When `collapsible=true` the alert renders as a `<details>`/`<summary>` element. Set `open=false` to start collapsed.

---

## Callout

Inset box for editorial content -- tips, notes, warnings. Unlike `alert`, callouts have no dismiss and are meant for prose-adjacent emphasis. Supports a `header_actions` named slot.

```text
callout(variant="info", title=none, icon=none, cls="")
```

**Variants:** `info`, `success`, `warning`, `error`, `neutral`

```text
{% from "chirpui/callout.html" import callout %}

{% call callout(variant="info", title="Note") %}
    This is an informational callout with a title.
{% end %}

{% call callout(variant="warning", title="Tip") %}
    {% slot header_actions %}<button>Copy</button>{% end %}
    Body content goes here.
{% end %}
```

---

## Toast

Transient notifications delivered via htmx out-of-band swaps. Place the container once in your base template, then return `toast()` calls from any htmx response.

```text
toast_container(id="chirpui-toasts", cls="")
toast(message, variant="info", id=none, dismissible=true, oob=true, container_id="chirpui-toasts", cls="")
```

**Variants:** `info`, `success`, `warning`, `error`

```text
{% from "chirpui/toast.html" import toast, toast_container %}

{# In your base layout -- once #}
{{ toast_container() }}

{# In an htmx response #}
{{ toast("Item saved!", variant="success") }}
{{ toast("Connection lost.", variant="error") }}
```

The `oob=true` default wraps the toast in an `hx-swap-oob="beforeend"` targeting the container. Pair with `HX-Trigger` headers or htmx SSE for server-pushed notifications.

---

## Confirm dialog

Modal for destructive actions or confirmations. Uses the native `<dialog>` element. Pair `confirm_dialog` with `confirm_trigger` to wire the open action.

```text
confirm_dialog(id, title, message=none, confirm_label="Confirm", cancel_label="Cancel",
               variant="default", confirm_url=none, confirm_method="POST",
               hx_target=none, hx_swap="innerHTML", hx_select=none, hx_push_url=none, cls="")

confirm_trigger(target, label="Confirm", cls="")
```

**Variants:** `default`, `danger`

When `confirm_url` is provided the confirm button submits a form (htmx or native). Cancel always closes via `<form method="dialog">`. Supports named slots: `header_actions`, `message` (alternative to the `message` param), and `form_content` (hidden fields inside the confirm form).

```text
{% from "chirpui/confirm.html" import confirm_dialog, confirm_trigger %}

{{ confirm_trigger("del-dlg", label="Delete") }}

{% call confirm_dialog("del-dlg", title="Delete item?",
                       message="This cannot be undone.",
                       confirm_label="Delete", variant="danger",
                       confirm_url="/items/1/delete") %}
{% end %}
```

---

## Empty state

Placeholder for empty lists, search results, or zero-data views. Supports an `action` named slot for custom CTAs.

```text
empty_state(icon=none, title="No items", illustration=none, action_label=none, action_href=none,
            code=none, suggestions=none, search_hint=none, cls="")
```

| Param | Purpose |
|-------|---------|
| `icon` | Decorative icon above the title |
| `illustration` | Custom graphic (replaces icon) |
| `action_label` + `action_href` | Renders a primary button link |
| `code` | Inline code snippet (e.g. a query) |
| `suggestions` | List of suggestion strings rendered as `<ul>` |
| `search_hint` | Hint text for search refinement |

```text
{% from "chirpui/empty.html" import empty_state %}

{# Simple with action #}
{% call empty_state(icon="docs", title="No projects", action_label="Create", action_href="/new") %}
    <p>Create your first project to get started.</p>
{% end %}

{# Search results #}
{% call empty_state(title="No results", code="query", search_hint="Try a different search term") %}
    <p>No matches found.</p>
{% end %}
```

### Empty panel state

Compact variant for panel and workspace bodies. Wraps `empty_state` with tighter spacing. Same params plus `compact=true` (default).

```text
empty_panel_state(icon=none, title="No items", ..., compact=true, cls="")
```

```text
{% from "chirpui/empty_panel_state.html" import empty_panel_state %}

{% call empty_panel_state(title="No file selected", icon="docs") %}
    <p>Select a file from the tree to start editing.</p>
{% end %}
```

---

## Progress bar

Determinate progress indicator with variant colors and custom color support.

```text
progress_bar(value, max=100, label=none, variant="gold", size="md", cls="", color=none)
```

**Sizes:** `sm`, `md`, `lg`

Pass `color` (a hex value or registered color name) to override the variant with a custom fill color.

```text
{% from "chirpui/progress.html" import progress_bar %}

{{ progress_bar(value=60) }}
{{ progress_bar(value=75, max=100, label="75%", size="lg") }}
{{ progress_bar(value=40, color="#78c850") }}
```

---

## Skeleton

Loading placeholder with shimmer animation. Use to reserve space while content loads.

```text
skeleton(width=none, height=none, variant="", lines=1, cls="")
```

**Variants:** (default), `avatar`, `text`, `card`

```text
{% from "chirpui/skeleton.html" import skeleton %}

{# Basic bar #}
{{ skeleton(width="200px", height="2rem") }}

{# Avatar circle #}
{{ skeleton(variant="avatar") }}

{# Multi-line text block #}
{{ skeleton(variant="text", lines=3) }}

{# Card with image and lines #}
{{ skeleton(variant="card", lines=2) }}
```

---

## Spinner

Indeterminate loading indicators. Two animation styles are available.

```text
spinner(size="md", cls="")
spinner_thinking(size="md", cls="")
```

**Sizes:** `sm`, `md`, `lg`

- **`spinner`** -- mote pulse animation (pulsing star character)
- **`spinner_thinking`** -- spiral rotation animation

```text
{% from "chirpui/spinner.html" import spinner, spinner_thinking %}

{{ spinner() }}
{{ spinner(size="sm") }}
{{ spinner_thinking(size="lg") }}
```

Both set `role="status"` and an `aria-label` for accessibility.

---

## CSS classes

All components follow BEM naming under the `chirpui-` namespace:

`chirpui-alert`, `chirpui-callout`, `chirpui-toast`, `chirpui-toast-container`, `chirpui-confirm`, `chirpui-empty-state`, `chirpui-empty-panel-state`, `chirpui-progress-bar`, `chirpui-skeleton`, `chirpui-spinner`, `chirpui-spinner-thinking`

## Related

- [Status indicators](./status-indicators.md) -- badges and live dots
- [Modals and drawers](./modals-and-drawers.md) -- `confirm_dialog` uses the modal system
- [Buttons](./buttons.md) -- CTAs inside alerts and empty states
- [Security](../guides/security.md) -- never pass untrusted HTML into alerts
