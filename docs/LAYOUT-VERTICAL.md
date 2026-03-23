# Layout vertical fill (full-height main)

How ChirpUI’s app shell behaves in the **block axis** (height): when the main column scrolls vs when the page fills the viewport and **inner** regions scroll.

## Two modes

| Mode | `main` scroll | Typical use |
|------|----------------|------------|
| **Default** | Yes (`overflow-y: auto`) | Long-form content, lists, docs |
| **Fill** | No (`overflow: hidden`); flex column | Chat, maps, split editors, anything that should use the full area below the topbar |

Default mode is unchanged: `#page-content` is a flex column with vertical gap, but it only grows with its content. **Fill mode** makes `#page-content` a flex item with `flex: 1; min-height: 0` so a single child can stretch to the bottom of the shell.

## Opt in to fill mode

1. On layouts extending [`chirpui/app_shell_layout.html`](../src/chirp_ui/templates/chirpui/app_shell_layout.html), set:

   ```kida
   {% block main_shell_class %} chirpui-app-shell__main--fill{% end %}
   ```

   (Leading space is optional; the block is appended to the base `chirpui-app-shell__main` class.)

2. Wrap your route body in a single root that uses **`chirpui-page-fill`** as a class on the **direct child of `#page-content`**:

   ```html
   <div class="chirpui-page-fill my-page-root">…</div>
   ```

   That class applies `display: flex; flex-direction: column; flex: 1; min-height: 0` so nested layouts (e.g. `chat_layout(fill=true)`) can participate in the flex chain.

## Chat layout

- Use **`{% call chat_layout(..., fill=true) %}`** so the root gets **`chirpui-chat-layout--fill`**.
- If the messages slot contains a **wrapper** around the scroll region (SSE, HTMX, custom div), add **`chirpui-chat-layout__messages-body`** to that wrapper so it receives `flex: 1; min-height: 0` and column flex. The actual scroll target (e.g. transcript) should use `flex: 1; min-height: 0; overflow-y: auto` inside that wrapper.

## Why `min-height: 0` matters

Flex and grid children default to `min-height: auto`, which can prevent shrinking and break nested scroll. Any flex child that should **scroll internally** needs **`min-height: 0`** (or `overflow: hidden` on an ancestor that establishes the bound).

## HTMX / `#page-content`

Swapping `#page-content` via HTMX does not change this contract: the same classes on the new fragment re-establish the flex chain on each navigation.

## See also

- [LAYOUT-OVERFLOW.md](LAYOUT-OVERFLOW.md) — horizontal overflow and the main column scrollport
- [site content app-shell](../site/content/docs/app-shell/_index.md) — shell overview and fragment targets
