# FastAPI + chirp-ui reference app

Minimal runnable example for [#287](https://github.com/lbliii/chirp-ui/issues/287).

## Install

```bash
pip install chirp-ui fastapi uvicorn python-multipart itsdangerous
```

(`itsdangerous` is pulled in by Starlette session middleware.)

## Run

From repo root:

```bash
uvicorn examples.integrations.fastapi.app:app --reload --port 5002
```

Or from this directory:

```bash
cd examples/integrations/fastapi
uvicorn app:app --reload --port 5002
```

Open <http://127.0.0.1:5002>. Try the htmx greet form — the swap route is yours to own (no Chirp OOB helpers).

## What this proves

- kida render helper returning `HTMLResponse`
- `StaticFiles` mount for `chirp_ui.static_path()`
- Session-backed CSRF bridge (documented swap: `starlette-csrf`)
- htmx script + swap route you write yourself

See [docs/integration/fastapi.md](../../../docs/integration/fastapi.md).
