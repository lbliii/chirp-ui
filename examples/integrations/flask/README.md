# Flask + chirp-ui reference app

Minimal runnable example for [#286](https://github.com/lbliii/chirp-ui/issues/286).

## Install

From the repo root (or any venv):

```bash
pip install chirp-ui flask flask-wtf
```

## Run

```bash
python examples/integrations/flask/app.py
```

Open <http://127.0.0.1:5001>. Submit the form empty to see `field_errors` wiring; submit with a name to see Flask-WTF CSRF + success alert.

## What this proves

- kida `render_template()` path (not `flask.render_template()`)
- `register_filters()` via the shared kida adapter
- Static files from `chirp_ui.static_path()` at `/static/`
- `csrf_field` global bridged to Flask-WTF
- `theme_toggle()` interactive component with hand-rolled Alpine bootstrap

See [docs/integration/flask.md](../../../docs/integration/flask.md) for the full guide.
