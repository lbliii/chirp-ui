---
title: CSS class index
description: chirpui-* contract and how it is enforced
draft: false
weight: 48
lang: en
type: doc
keywords: [chirp-ui, css, bem]
icon: list-bullets
---

# CSS class index

## Contract

Every **`chirpui-*`** class referenced in Kida templates must exist in **`chirpui.css`**. The project enforces this with **`tests/test_template_css_contract.py`** — CI fails if templates reference unknown classes.

## Organization

`chirpui.css` is organized by section comments (e.g. **Layout**, **Entity header**, **Action Containers**, **Chat Layout**). Tokens live at the top under **Design system foundation**.

## Finding classes

1. Search **`chirpui.css`** for the component name.
2. Check the matching template under **`src/chirp_ui/templates/chirpui/`** for the exact class strings.
3. Run the contract test locally: **`uv run pytest tests/test_template_css_contract.py`**.

## Related

- [BEM naming](../concepts/bem-naming.md)
- [Components](../components/)
