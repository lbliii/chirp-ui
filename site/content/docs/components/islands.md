---
title: Islands & primitives
description: Lightweight client-side state primitives for server-rendered UIs
draft: false
weight: 30
lang: en
type: doc
keywords: [chirp-ui, islands, primitives, state, htmx, fragment, draft, wizard, upload, grid]
category: components
tags: [islands, primitives, state]
---

# Islands & primitives

Islands are lightweight JavaScript adapters that add client-side state to server-rendered HTML. They are not a framework — each island is a small, self-contained module that communicates through DOM events. No build step required.

## When to use islands vs Alpine.js

| Reach for | When |
|-----------|------|
| **Alpine.js** | Toggle visibility, simple UI state, `x-show`/`x-bind` patterns |
| **Islands** | Persistent state (localStorage, URL params), multi-step flows, file uploads, error boundaries |
| **Fragment islands** | Isolating HTMX mutation regions from inherited shell attributes |

Alpine handles ephemeral UI state. Islands handle durable state that survives navigation or needs coordination across components.

## Architecture

### Foundation API

Every island primitive imports from `foundation.js`, which provides the core lifecycle:

| Function | Purpose |
|----------|---------|
| `readProps(payload)` | Extract props object from the island payload |
| `attachCleanup(payload, fn)` | Register a cleanup function (called on unmount) |
| `runCleanup(payload)` | Execute and remove the cleanup function |
| `setState(payload, api, state)` | Emit a `chirp:island:state` event |
| `setAction(payload, api, action, status, extra)` | Emit a `chirp:island:action` event |
| `setError(payload, api, reason, extra)` | Emit a `chirp:island:error` event |
| `registerPrimitive(name, adapter)` | Register an adapter with `window.chirpIslands` |

Each emit function checks for a Chirp-provided `api` object first (with `emitState`/`emitAction`/`emitError` methods). If no API is available, it falls back to dispatching `CustomEvent` on both `document` and `window`.

### Adapter contract

Every island primitive exports a single adapter object with a `mount` method:

```javascript
import { readProps, setState, registerPrimitive } from "./foundation.js";

registerPrimitive("my_primitive", {
  mount(payload, api) {
    const props = readProps(payload);
    const root = payload.element;

    // Set up DOM listeners, read initial state...
    setState(payload, api, { value: props.initial });

    // Return cleanup function
    return () => {
      // Remove listeners, clear timers
    };
  }
});
```

The `payload` object contains:

| Field | Type | Description |
|-------|------|-------------|
| `element` | `HTMLElement` | The root `<section>` element |
| `name` | `string` | Primitive name |
| `id` | `string` | Unique mount ID |
| `version` | `string` | Primitive version |
| `props` | `object` | Props passed from the template macro |

## Event protocol

Islands communicate through six lifecycle events, all dispatched on both `document` and `window`:

| Event | Detail fields | When |
|-------|--------------|------|
| `chirp:island:mount` | `name, id, version` | Island mounts for the first time |
| `chirp:island:unmount` | `name, id` | Island is destroyed |
| `chirp:island:remount` | `name, id` | Island re-mounts after an HTMX swap |
| `chirp:island:state` | `name, id, version, state` | State changes |
| `chirp:island:action` | `name, id, version, action, status, ...extra` | Action triggered |
| `chirp:island:error` | `name, id, version, error, reason, ...extra` | Error occurs |

Listen globally:

```javascript
document.addEventListener("chirp:island:state", (e) => {
  const { name, id, state } = e.detail;
  console.log(`${name}#${id}:`, state);
});
```

## Built-in primitives

chirp-ui ships seven ready-to-use primitives, each with a corresponding Kida macro in `state_primitives.html`:

| Primitive | Macro | Purpose | Key data attributes |
|-----------|-------|---------|-------------------|
| `state_sync` | `state_sync(state_key)` | Sync inputs with URL query params | `data-state-field` |
| `action_queue` | `action_queue(action_id)` | Button-triggered action with status | `data-action-trigger`, `data-action-status` |
| `draft_store` | `draft_store(draft_key)` | Auto-save form fields to localStorage | `data-draft-field`, `data-draft-saved-at` |
| `error_boundary` | `error_boundary(boundary_id)` | Catch errors and show fallback UI | `data-error-body`, `data-error-fallback`, `data-error-reset` |
| `grid_state` | `grid_state(state_key, columns)` | Filter, sort, select table rows | `data-grid-filter`, `data-grid-row`, `data-grid-select`, `data-grid-sort` |
| `wizard_state` | `wizard_state(state_key, steps)` | Multi-step wizard navigation | `data-wizard-step`, `data-wizard-next`, `data-wizard-prev`, `data-wizard-status` |
| `upload_state` | `upload_state(state_key, endpoint)` | File upload with progress | `data-upload-input`, `data-upload-start`, `data-upload-progress`, `data-upload-status` |

### Usage

Import the macro and wrap your content:

```kida
{% from "chirpui/state_primitives.html" import state_sync %}

{% call state_sync("search", query_param="q") %}
  <input type="text" data-state-field placeholder="Search..." />
{% end %}
```

The macro handles loading the JavaScript, mounting the island, and wiring up the data attributes. All you provide is the HTML inside the slot.

### Draft store example

```kida
{% from "chirpui/state_primitives.html" import draft_store %}

{% call draft_store("new-post") %}
  <input name="title" data-draft-field placeholder="Title" />
  <textarea name="body" data-draft-field placeholder="Body..."></textarea>
  <small data-draft-saved-at></small>
{% end %}
```

Fields with `data-draft-field` are auto-saved to localStorage with a 250ms debounce. The `data-draft-saved-at` element displays the last save timestamp. Values are restored on mount.

### Wizard example

```kida
{% from "chirpui/state_primitives.html" import wizard_state %}

{% call wizard_state("onboarding", steps=3) %}
  <div data-wizard-step>Step 1: Account details</div>
  <div data-wizard-step>Step 2: Preferences</div>
  <div data-wizard-step>Step 3: Confirmation</div>
  <button data-wizard-prev>Back</button>
  <button data-wizard-next>Next</button>
  <span data-wizard-status></span>
{% end %}
```

Only the active step is visible. Navigation buttons disable at boundaries. The status element shows "Step 1 of 3".

## Fragment islands

Fragment islands solve a different problem: HTMX attribute inheritance. In an app shell with `hx-boost` or `hx-select`, child forms inherit those attributes, causing unexpected behavior. Fragment islands isolate a region by applying `hx-disinherit`.

### `fragment_island`

```kida
{% from "chirpui/fragment_island.html" import fragment_island %}

{% call fragment_island("step-list") %}
  {% for step in steps %}
    <div>{{ step.name }}</div>
  {% end %}
{% end %}
```

Renders a `<div>` with `hx-disinherit="hx-select hx-target hx-swap"`, preventing inherited HTMX attributes from leaking into the region.

### `fragment_island_with_result`

Adds a mutation result container for form feedback:

```kida
{% from "chirpui/fragment_island.html" import fragment_island_with_result %}

{% call fragment_island_with_result("items", "item-result") %}
  <form hx-post="/items" hx-target="#item-result" hx-swap="innerHTML">
    <input name="title" />
    <button type="submit">Add</button>
  </form>
{% end %}
```

The result `<div>` (with `aria-live="polite"`) sits inside the fragment, guaranteeing the target exists in the same DOM subtree.

### `poll_trigger`

A hidden button that fires on page load, useful for deferred content:

```kida
{% from "chirpui/fragment_island.html" import poll_trigger %}

{{ poll_trigger("/dashboard/stats", "#stats-panel", delay="2s") }}
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `url` | required | Endpoint to poll |
| `target` | required | CSS selector for the swap target |
| `delay` | `none` | Delay before first trigger (e.g. `"2s"`) |
| `swap` | `"innerHTML"` | HTMX swap strategy |
| `select` | `none` | Optional `hx-select` |

## Writing a custom primitive

1. Create a JS file in your static directory (e.g. `/static/islands/my_counter.js`):

```javascript
import {
  readProps,
  setState,
  setAction,
  registerPrimitive,
} from "./foundation.js";

registerPrimitive("my_counter", {
  mount(payload, api) {
    const { initial = 0 } = readProps(payload);
    const root = payload.element;
    let count = initial;

    const display = root.querySelector("[data-counter-value]");
    const plusBtn = root.querySelector("[data-counter-plus]");
    const minusBtn = root.querySelector("[data-counter-minus]");

    function update() {
      if (display) display.textContent = count;
      setState(payload, api, { count });
    }

    function onPlus() {
      count++;
      update();
      setAction(payload, api, "increment", "success");
    }

    function onMinus() {
      count--;
      update();
      setAction(payload, api, "decrement", "success");
    }

    plusBtn?.addEventListener("click", onPlus);
    minusBtn?.addEventListener("click", onMinus);
    update();

    return () => {
      plusBtn?.removeEventListener("click", onPlus);
      minusBtn?.removeEventListener("click", onMinus);
    };
  },
});
```

2. Use `island_root` directly in a template:

```kida
{% from "chirpui/islands.html" import island_root %}

{% call island_root(
    "my_counter",
    props={"initial": 0},
    src="/static/islands/my_counter.js",
    primitive="my_counter"
) %}
  <span data-counter-value>0</span>
  <button data-counter-minus>-</button>
  <button data-counter-plus>+</button>
{% end %}
```

Or wrap it in a macro in your own template file for reuse, following the same pattern as the built-in `state_primitives.html` macros.
