# AI chat patterns

Server-rendered chat UIs in chirp-ui compose `chat_layout`, `message_thread`,
`streaming`, and the **`composer()`** macro. This document covers the
server-side contracts the macros assume but do not enforce.

---

## Composer send / stop cancellation

The `composer()` macro ships a send/stop toggle. **Stop must abort upstream
generation**, not merely close the htmx SSE listener client-side.

When the user clicks Stop, two things must happen:

1. **Client** — `chirpuiComposer.stop()` sets `generating=false` and the SSE
   element closes (visual stop).
2. **Server** — the Stop button `hx-POST`s `stop_action` (e.g.
   `POST /chat/{id}/abort`) which **cancels the in-flight generation task**
   before the response returns.

If only (1) happens, the model keeps producing tokens and a reconnect resumes
the “stopped” answer. This is the same failure mode as open-webui #1166 /
#20018.

### Reference abort handler

```python
# App-owned — chirp-ui ships the UI; you own the endpoint.
GENERATIONS: dict[str, asyncio.Task] = {}

@app.post("/chat/{chat_id}/abort")
async def abort(chat_id: str):
    task = GENERATIONS.pop(chat_id, None)
    if task is not None:
        task.cancel()
    return Response(status=204)  # hx-swap="none"; UI already toggled
```

Wire the composer:

```jinja
{% call composer(action="/chat/send", stop_action="/chat/abort",
                 hx_post="/chat/send", hx_target="#thread", hx_swap="beforeend") %}
{% end %}
```

When the stream completes normally, the streaming region dispatches
`chirpui:generation-done` (via `sse_close="done"` on `streaming_bubble`) and
the composer flips back to Send.

---

## Attachment status (OOB-driven)

Attachment chips (`attachment_chip()` / `file_item.html`) are **id-addressable**
(`id="attachment-{id}"`). Status lifecycle is server-authoritative:

| Status | Meaning |
|---|---|
| `uploading` | bytes in flight |
| `processing` | server-side extraction / virus scan / embedding |
| `ready` | attachable to the prompt |
| `error` | show `role="alert"` styling |

The server OOB-swaps a fresh chip fragment targeting `#attachment-{id}`:

```jinja
{% from "chirpui/oob.html" import oob_fragment %}
{% from "chirpui/file_item.html" import attachment_chip %}

{{ oob_fragment("attachment-" ~ file_id, swap="outerHTML") }}
  {{ attachment_chip(id=file_id, name=name, status="ready", dismiss_url=dismiss_url) }}
{% end %}
```

Each chip dispatches `chirpui:attachment-changed` on render so
`chirpuiComposer.syncAttachments()` keeps `uploadPending` and send disabled
state honest.

**Do not** fake upload progress with client timers. The `upload_state` island
POSTs files and applies OOB HTML from the response — status comes from the
server, not a `setInterval` percent bar.

---

## Suggestion / follow-up chips

`suggestion_chips()` renders deduped chips for empty states and post-stream
follow-ups. Each item is a dict:

```python
{"label": "Summarize", "prompt": "Summarize the thread", "key": "summarize"}
```

Dedupe key: `item["key"]` if present, else `item["prompt"]`. Re-OOB-ing the
same set to `#follow-ups` is idempotent.

- `mode="prefill"` — fills the composer and focuses the textarea
- `mode="send"` — prefills and submits when `canSend`

The composer listens for `chirpui:suggestion` on `window`.

---

## IME-safe Enter-to-send

`send_key="enter"` (default) sends on Enter; Shift+Enter inserts a newline.
`send_key="mod-enter"` requires Cmd/Ctrl+Enter.

The factory guards CJK IME commits via `isComposing`, `keyCode === 229`, and a
500ms window after `compositionend` (Safari/Firefox quirk).

---

## Disabled-says-why

Disabled composer controls accept `send_disabled_reason`. When send is
disabled, the reason appears in a tooltip on a non-disabled wrapper (disabled
elements do not receive pointer events).

Apply the same pattern to other disabled controls: wrap in `tooltip()` and pass
`disabled_reason` when the control is inert.
