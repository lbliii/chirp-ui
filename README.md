# chirp-ui

Reusable [Kida](https://github.com/lbliii/kida) component library for [Chirp](https://github.com/lbliii/chirp) — headless, htmx-native, zero JavaScript.

## Install

```bash
pip install chirp-ui
```

When used with Chirp, components are auto-detected — no configuration needed.

## Usage

```html
{% from "chirpui/card.html" import card %}
{% from "chirpui/modal.html" import modal, modal_trigger %}
{% from "chirpui/alert.html" import alert %}

{% call card(title="Recent Orders") %}
    <p>Card body content goes here.</p>
{% end %}

{% call alert(variant="success") %}
    Operation completed.
{% end %}
```

Include the structural CSS in your base template:

```html
<link rel="stylesheet" href="/static/chirpui.css">
```

## Components (v0.1)

| Component | Import | Features |
|-----------|--------|----------|
| **card** | `chirpui/card.html` | Header, body (slot), footer, collapsible |
| **modal** | `chirpui/modal.html` | Dialog-based, trigger button, close |
| **tabs** | `chirpui/tabs.html` | htmx tab switching, active state |
| **dropdown** | `chirpui/dropdown.html` | Native `<details>`-based |
| **toast** | `chirpui/toast.html` | htmx OOB notifications |
| **table** | `chirpui/table.html` | Headers, row helper, sortable |
| **pagination** | `chirpui/pagination.html` | htmx page navigation |
| **alert** | `chirpui/alert.html` | Info, success, warning, error variants |
| **forms** | `chirpui/forms.html` | Field macros with error display |

## Design Principles

- **Headless by default** — structure and BEM classes, minimal styling
- **htmx-native** — interactive components use htmx or native HTML (`<dialog>`, `<details>`)
- **Composable** — `{% slot %}` for content injection, components nest freely
- **Customizable** — CSS custom properties (`--chirpui-*`) for all structural values

## Manual Registration (without Chirp)

If using Kida directly without Chirp:

```python
from kida import ChoiceLoader, Environment, FileSystemLoader
from chirp_ui import get_loader

env = Environment(
    loader=ChoiceLoader([
        FileSystemLoader("templates"),
        get_loader(),
    ])
)
```

## Requirements

- Python >= 3.14
- kida-templates >= 0.1.2

## License

MIT
