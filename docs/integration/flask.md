# chirp-ui + Flask

Integration guide for using chirp-ui in **Flask** without Chirp. Shared wiring
(kida bootstrap, Alpine shim, static assets) lives in
[standalone-core.md](standalone-core.md).

Reference app: [`examples/integrations/flask/`](../../examples/integrations/flask/)

---

## Quickstart

```bash
pip install chirp-ui flask flask-wtf
python examples/integrations/flask/app.py
```

Open <http://127.0.0.1:5001>.

---

## The Flask-specific rule

Flask's native engine is **Jinja2**. chirp-ui macros are **kida** templates.
Do not call `flask.render_template()` for chirp-ui — render kida in Python and
return the HTML string:

```python
from flask import Response

html = render_template(env, "index.html", errors=errors)
return Response(page_shell(title="My app", body=html), mimetype="text/html")
```

Your Jinja templates (if any) can wrap kida output, but never mix `{% %}`
engines in the same file.

---

## `render_kida()` helper

The reference app uses shared bootstrap code in
`examples/integrations/_shared/chirpui_bootstrap.py`:

```python
from pathlib import Path
from kida.template import Markup
from flask_wtf.csrf import generate_csrf

from chirpui_bootstrap import make_env, page_shell, render_template

env = make_env(
    template_dir=Path("templates"),
    csrf_field=lambda: Markup(
        f'<input type="hidden" name="csrf_token" value="{generate_csrf()}">'
    ),
)

def render_page(template: str, **context) -> str:
    body = render_template(env, template, **context)
    return page_shell(title="My app", body=body)
```

Copy `chirpui_bootstrap.py` into your project or import it from the examples
tree while prototyping.

---

## Static files

Mount `chirp_ui.static_path()` — do not copy CSS/JS into your repo unless you
pin versions deliberately.

```python
from flask import send_from_directory
from chirp_ui import static_path

@app.get("/static/<path:filename>")
def static_files(filename: str):
    root = static_path()
    return send_from_directory(root, filename)
```

Templates reference `/static/chirpui.css`, `/static/chirpui-alpine.js`, etc.

---

## CSRF bridge

`form()` and `csrf_hidden()` expect a **`csrf_field`** global. Wire it to
Flask-WTF:

```python
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf

CSRFProtect(app)

# In make_env(...):
csrf_field=lambda: Markup(
    f'<input type="hidden" name="csrf_token" value="{generate_csrf()}">'
)
```

Flask-WTF validates the token on POST; chirp-ui only emits the hidden field.

---

## Forms and validation

Pass a `errors` dict shaped `{field_name: [message, ...]}` into kida templates
for `text_field(..., errors=errors)`:

```python
errors: dict[str, list[str]] = {}
if not name.strip():
    errors["name"] = ["Name is required."]
```

---

## What you hand-roll

| Concern | Standalone Flask | On Chirp |
|---|---|---|
| kida render path | manual `render_kida()` helper | automatic |
| Filter registration | `register_filters()` at app init | `use_chirp_ui(app)` |
| Static serving | blueprint / `send_from_directory` | auto |
| Alpine load + `safeData` | hand-rolled `<script>` + shim | injected |
| htmx | hand-added `<script>` | injected |
| CSRF (`csrf_field`) | bridge to Flask-WTF | auto |
| OOB / SSE / suspense responses | write the fragment routes yourself | helpers provided |

See [capability-matrix.md](capability-matrix.md) for the full comparison.

---

## Why this gets easier on Chirp

Flask glue is moderate — one render helper, one static route, one CSRF bridge,
and the Alpine bootstrap from [standalone-core.md](standalone-core.md). Chirp's
[`use_chirp_ui(app)`](https://lbliii.github.io/chirp/docs/guides/chirp-ui/)
removes all of that and adds route-aware HTMX attrs, OOB shell updates, and
streaming/SSE response helpers you would otherwise write per route.

When Flask starts feeling like a template glue factory, you are ready for
Chirp — not because Flask failed, but because you have already mapped the seams.

---

## Related

- [standalone-core.md](standalone-core.md)
- [fastapi.md](fastapi.md) · [django.md](django.md)
- [kida-overlap-audit.md](kida-overlap-audit.md) — how this guide relates to Kida 0.11 docs
- Issue [#286](https://github.com/lbliii/chirp-ui/issues/286)

### See also (Kida engine)

- [Kida Flask Integration tutorial](https://lbliii.github.io/kida/docs/tutorials/flask-integration/) — `init_kida`, `render_block`, typed components
- [Kida Framework Integration API](https://lbliii.github.io/kida/docs/usage/framework-integration/) — block rendering and introspection
- [Kida `flask_components` example](https://github.com/lbliii/kida/tree/main/examples/flask_components) — runnable smoke-tested app; pair with [capability-matrix upgrade pitch](capability-matrix.md#upgrade-pitch-why-chirp) when standalone glue accumulates
