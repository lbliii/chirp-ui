# SSE Event Vocabulary & the Terminal-Done Rule

chirp-ui's streaming primitives are server-driven and unopinionated about wire
format on purpose — but a chat/agent UI built on raw `sse-swap` will drift unless
the server and client agree on (1) a stable set of **event names**, (2) which
macro/swap each event drives, and (3) two non-negotiable rules. This doc is that
contract. It does NOT replace the live-region a11y semantics in #260 — those say
*how appended content is announced*; this says *what each event means and when the
shimmer must stop*.

See also:

- [COMPONENT-OPTIONS.md § Streaming](../COMPONENT-OPTIONS.md)
- [COMPONENT-OPTIONS.md § SSE Status](../COMPONENT-OPTIONS.md)
- [HTMX-PATTERNS.md](../components/htmx-patterns.md)
- #260 — Live-region polish (`role=log` + load sentinel)

## The event table

The server emits named SSE events; each maps to one macro target + one htmx swap
strategy. Names are a *recommended canonical set* — the rules below are mandatory,
the names are a starting vocabulary you can extend.

| Event name        | Meaning                              | Target macro / element                              | htmx swap strategy                          | Persist on reload? |
|-------------------|--------------------------------------|-----------------------------------------------------|---------------------------------------------|--------------------|
| `token`           | One token / chunk of assistant text  | inner `streaming_block` (`sse-swap="token"`)        | `hx-swap="beforeend"` (append)              | **Yes** (replay full text) |
| `thinking-start`  | Model began reasoning                 | the `streaming_bubble` article                       | client sets `aria-busy="true"` + `--thinking`| No (transient state) |
| `thinking-stop`   | Reasoning finished, answer begins     | same article                                         | client clears `aria-busy` / `--thinking`     | No |
| `tool-call`       | Agent invoked a tool                  | a `streaming_block` / card appended to the turn      | `hx-swap="beforeend"` (new block)           | **Yes** (replay result) |
| `citation`        | A source/citation chip                | a citation list region (`sse-swap="citation"`)       | `hx-swap="beforeend"`                        | **Yes** |
| `error`           | Recoverable stream error              | `streaming_bubble(state="error")` + `sse_retry()`    | `hx-swap="beforeend"` then **terminal-done** | No (re-render on retry) |
| `done`            | Stream finished cleanly               | the block's lifecycle hook                           | **terminal-done** (Rule 1)                   | n/a (it IS the end) |
| `toast`           | Transient notice (rate limit, saved)  | `oob_toast(...)` into `#chirpui-toasts`              | `hx-swap-oob` (OOB)                          | **No** (ephemeral) |

> The `done` row is special: it is named via `sse-close="done"` on the macro
> (the default), which tells htmx's SSE extension to close the EventSource. See
> Rule 1.

## Rule 1 (NON-NEGOTIABLE) — every stream close is a terminal "done"

A dropped connection, a network error, a server crash, and a clean `done` event
are **indistinguishable to the user** and must all land on the same terminal
state: shimmer off, `aria-busy` cleared. htmx's SSE extension fires `htmx:sseClose`
when the EventSource closes (including `sse-close="done"`) and `htmx:sseError` on a
connection error. chirp-ui ships a tiny `chirpuiStreamLifecycle` Alpine factory
that listens for both and performs the terminal-done cleanup. Opt in by adding the
`x-data` hook to the SSE-connected block (the macro does this for you when
`sse_connect` or `sse_swap_target` is set):

```javascript
// chirpui-alpine.js — registered beside chirpuiSseRetry.
register("chirpuiStreamLifecycle", function () {
    // listens for htmx:sseClose, htmx:sseError, and send-error siblings;
    // removes chirpui-streaming-block--active and clears aria-busy once.
});
```

Without this, a dropped socket strands `chirpui-streaming-block--active` (infinite
blinking cursor) and `aria-busy="true"` (a screen reader stuck on "busy") forever —
the single most common open-webui-class streaming bug.

## Rule 2 (NON-NEGOTIABLE) — persist-vs-ephemeral

On reload the server re-renders the conversation from its own store. Decide per
event whether it is **persisted** (replayed on reload) or **ephemeral** (lives only
in the live stream):

- **Persist & replay:** `token` text (the assistant turn), `tool-call` results,
  `citation`s, the final assistant message. On reload these come back as ordinary
  server-rendered `streaming_bubble`s with `streaming=false` — no SSE, no shimmer.
- **Ephemeral (never replay):** `toast` (an `oob_toast` is a one-shot notice),
  `thinking-start`/`thinking-stop` (a live state, not content), and `sse_status`
  transitions (connection chrome). A reloaded page shows the *result*, not the
  reasoning animation.

The litmus test: *if the user reloads mid-answer, would they be confused to NOT see
this again?* If yes → persist. If it's chrome/notice/animation → ephemeral.

## Relationship to #260

#260 standardizes the **live-region semantics**: `role="log" aria-relevant="additions text"`
on append targets and the `role="status"` `load_sentinel`. Those ship today. This
doc is the orthogonal layer — **event vocabulary + the terminal-done invariant** —
and depends on #260's roles being present (the lifecycle handler clears the
`aria-busy` that those regions rely on). They are complementary; neither subsumes
the other.

## Route + template sketch

```python
@app.get("/chat/{id}/stream")
def chat_stream(id: str):
    def events():
        yield sse("token", partial_text)
        yield sse("done", "")
    return EventSourceResponse(events())
```

```html
{% from "chirpui/streaming.html" import streaming_bubble %}
{% call streaming_bubble(sse_connect="/chat/" ~ id ~ "/stream", streaming=true) %}
{% end %}
```

The inner `streaming_block` carries `x-data="chirpuiStreamLifecycle()"` automatically
when SSE is connected — no extra wiring in the route template.
