# chirp-ui Component Showcase

Spin up a Chirp app to browse all chirp-ui components.

## Run

**Option A — pip (standalone):**

```bash
cd /path/to/chirp-ui
pip install -e ".[showcase]"   # installs chirp-ui + chirp + kida-templates
python examples/component-showcase/app.py
```

**Option B — uv (from b-stack workspace root):**

```bash
cd /path/to/b-stack
uv sync
uv run python chirp-ui/examples/component-showcase/app.py
```

Then open http://localhost:8000

> **Note:** chirp-ui requires `kida-templates>=0.2.0` (provides the `kida` module). If you see `ModuleNotFoundError: No module named 'kida'`, ensure you're using the same Python environment where dependencies were installed.

## Optional: Holy Light theme

Add to your base template's `{% block head %}`:

```html
<link rel="stylesheet" href="/static/themes/holy-light.css">
```
