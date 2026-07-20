# chirp-ui + Django

Integration guide for using chirp-ui in **Django** without Chirp.

> **Honest note:** Django is the **highest-friction** of the three frameworks in
> this saga — two template engines, static config, CSRF field naming, and manual
> form-error mapping. It is also the **strongest funnel into Chirp**: the upgrade
> deletes the most glue.

Shared wiring: [standalone-core.md](standalone-core.md).

Reference app: [`examples/integrations/django/`](../../examples/integrations/django/)

---

## Quickstart

```bash
pip install chirp-ui django
cd examples/integrations/django
python manage.py migrate
python manage.py runserver 5003
```

Open <http://127.0.0.1:5003>.

---

## Templating: two options

Django's template engine is not kida. **Do not mix** `{% %}` tags from both
engines in one file.

| Option | Effort | Feel |
|---|---|---|
| **(a) Django template backend wrapping kida** | High | Native `{% include %}` ergonomics |
| **(b) Render kida in the view, thin Django wrapper** | Low | **Recommended** — least magic |

This guide and the reference app use **(b)**:

```python
from django.middleware.csrf import get_token
from django.shortcuts import render
from kida.template import Markup

def _render_kida(request, template, **context):
    token = get_token(request)

    def csrf_field() -> Markup:
        return Markup(
            f'<input type="hidden" name="csrfmiddlewaretoken" value="{token}">'
        )

    env = make_env(template_dir=KIDA_DIR, csrf_field=csrf_field)
    body = render_template(env, template, **context)
    return page_shell(title="My app", body=body)

def index(request):
    html = _render_kida(request, "index.html", errors=errors, ...)
    return render(request, "pages/shell.html", {"content": html})
```

Django shell template (`templates/pages/shell.html`):

```django
{{ content|safe }}
```

These are narrow trust boundaries: `Markup` wraps only the hidden input built
from Django's `get_token()` value, and `content|safe` accepts only the
server-rendered, autoescaped Kida output returned by `_render_kida`. Never pass
request data, user-authored HTML, or raw database content directly through
either boundary.

---

## Static files

Add chirp-ui assets to `STATICFILES_DIRS`:

```python
import chirp_ui

STATIC_URL = "/static/"
STATICFILES_DIRS = [chirp_ui.static_path()]
```

Development: `runserver` serves them automatically. Production:

```bash
python manage.py collectstatic
```

Templates use `/static/chirpui.css` (same paths as other guides).

---

## CSRF bridge

Django middleware enforces CSRF. chirp-ui only **emits** the hidden field via
`csrf_field` / `csrf_hidden()`:

```python
from django.middleware.csrf import get_token

def csrf_field() -> Markup:
    return Markup(
        f'<input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">'
    )
```

Use Django's field name `csrfmiddlewaretoken` so middleware recognizes posts from
chirp-ui forms.

---

## Django forms → `field_errors`

chirp-ui's `text_field(..., errors=errors)` expects a **mapping of field name →
list of strings**. Django's `Form.errors` needs a one-liner adapter:

```python
def django_errors(form) -> dict[str, list[str]]:
    return {
        name: [str(error) for error in error_list]
        for name, error_list in form.errors.items()
    }
```

Pass `errors=django_errors(form)` into your kida template. On validation
failure, re-render the page with bound values from `form[field].value()`.

The reference app (`pages/forms.py`, `pages/views.py`) demonstrates the full loop.

---

## Optional: messages → toasts

Bridge `django.contrib.messages` to chirp-ui `toast()` in your kida template or
pass flash data as context — not shown in the minimal demo; add when you need it.

---

## What you hand-roll

| Concern | Standalone Django | On Chirp |
|---|---|---|
| kida render path | kida in views **or** custom backend | automatic |
| Filter registration | `register_filters()` once at startup | `use_chirp_ui(app)` |
| Static serving | `STATICFILES_DIRS` + `collectstatic` | auto |
| Alpine load + `safeData` | hand-rolled `<script>` + shim | injected |
| htmx | hand-added `<script>` | injected |
| CSRF (`csrf_field`) | bridge to `get_token()` | auto |
| Django form errors → `field_errors` | manual mapping | n/a (Chirp-native forms) |
| OOB / SSE / suspense responses | write the views yourself | helpers provided |

---

## Why this gets easier on Chirp

Django teams often adopt chirp-ui for the **design system** while keeping Django
for ORM, admin, and auth. That split works — but the template boundary tax is
real: two engines, error-shape adapters, static config, and Alpine bootstrap.

Chirp does not replace Django's ORM or admin. It replaces the **HTML delivery
layer** where the glue accumulates. If you are maintaining a kida render helper,
CSRF bridge, and fragment routes beside Django views, Chirp is the upgrade that
removes the seam — and Django had the most seam to begin with.

---

## Related

- [standalone-core.md](standalone-core.md)
- [capability-matrix.md](capability-matrix.md)
- [flask.md](flask.md) · [fastapi.md](fastapi.md)
- [kida-overlap-audit.md](kida-overlap-audit.md) — how this guide relates to Kida 0.11 docs
- Issue [#288](https://github.com/lbliii/chirp-ui/issues/288)

### See also (Kida engine)

- [Kida Django Integration tutorial](https://lbliii.github.io/kida/docs/tutorials/django-integration/) — `KidaTemplates` backend, `using="kida"`, `render_block`
- [Kida Framework Integration API](https://lbliii.github.io/kida/docs/usage/framework-integration/) — block rendering and introspection
- [Kida `django_components` example](https://github.com/lbliii/kida/tree/main/examples/django_components) — runnable smoke-tested app; pair with [capability-matrix upgrade pitch](capability-matrix.md#upgrade-pitch-why-chirp) when the two-engine seam dominates maintenance
