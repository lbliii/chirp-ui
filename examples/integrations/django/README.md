# Django + chirp-ui reference app

Minimal runnable example for [#288](https://github.com/lbliii/chirp-ui/issues/288).

Django has the **most integration glue** of the three frameworks — this demo uses
the recommended **option (b)**: render kida in the view, wrap with a thin Django
template via `mark_safe`.

## Install

```bash
pip install chirp-ui django
```

## Run

```bash
cd examples/integrations/django
python manage.py migrate
python manage.py runserver 5003
```

Open <http://127.0.0.1:5003>. Submit empty to see Django form errors mapped into
chirp-ui `field_errors`.

## What this proves

- kida render path in views (not Django template macros)
- `STATICFILES_DIRS` → `chirp_ui.static_path()`
- CSRF via `get_token(request)` bridged to `csrf_field`
- Django `Form.errors` → `{name: [str, …]}` for `text_field(..., errors=...)`
- Interactive `theme_toggle()` with hand-rolled Alpine bootstrap

See [docs/integration/django.md](../../../docs/integration/django.md).

## Production static files

```bash
python manage.py collectstatic
```

Serve the collected `STATIC_ROOT` behind your reverse proxy.
