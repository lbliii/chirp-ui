---
title: Dashboard patterns
description: Action hierarchy, edit modes, and confirmations
draft: false
weight: 42
lang: en
type: doc
keywords: [chirp-ui, dashboard, ux]
icon: chart-line
---

# Dashboard patterns

Guidelines for CRM/dashboard-quality interaction — consistent with chirp-ui components.

## Principles

1. **One interaction model** — same patterns for edit, delete, filter, and run across pages.
2. **Progressive disclosure** — advanced controls in trays, popovers, or collapsibles.
3. **Explicit action hierarchy** — one primary per region; destructive actions always confirmed in UI (not native `confirm()`).
4. **Clear edit affordances** — inline vs explicit edit mode; obvious Save/Cancel.

## Action hierarchy

| Zone | Examples |
|------|----------|
| **Primary** | Create, Save, Run |
| **Secondary** | Edit, Export, Filters |
| **Destructive** | Delete — always behind **`confirm_dialog`** |

Use **`action_strip`**, **`command_bar`**, **`filter_bar`** with primary/secondary zones.

## Edit modes

- **Inline** — single-field tweaks (`inline_edit_field`).
- **Explicit** — multi-field forms with edit mode toggle.

## Tooltips vs popovers

- **Tooltip** — short hints (1–2 lines), icon-only buttons.
- **Popover** — interactive filters/options.

## Related

- [Components: Headers](../components/headers.md)
- [Modals](../components/modals-and-drawers.md)

Source: [DASHBOARD-MATURITY-CONTRACT.md](https://github.com/lbliii/chirp-ui/blob/main/docs/DASHBOARD-MATURITY-CONTRACT.md).
