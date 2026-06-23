# Control Selection Guide

Use this guide when choosing between native form controls, interactive Chirp UI
controls, and composite data surfaces. It exists to make the shipped component
surface feel complete without inventing duplicate APIs.

## Decision Matrix

| Need | Use | Source | Why |
|---|---|---|---|
| Submit a normal form value from a short option list | `select_field(...)` | `chirpui/forms.html` | Native `<select>` keeps browser behavior, mobile pickers, validation, and form submission. |
| Pick from a compact app-command or filter menu without typing | `dropdown_select(...)` | `chirpui/dropdown_menu.html` | Stable button trigger over a fixed listbox; dispatches selection events and supports keyboard focus. |
| Type to search a long or open-ended option list in a form | `combobox(...)` | `chirpui/combobox.html` | Text input typeahead with hidden form value, optional multi-select token pills, and client-side filtering. |
| Choose one option from a small visible set | `toggle_group(type="single", ...)` | `chirpui/toggle_group.html` | Keeps the options visible and renders native radio inputs. |
| Choose several options from a small visible set | `toggle_group(type="multiple", ...)` | `chirpui/toggle_group.html` | Renders native checkbox inputs with grouped button anatomy. |
| Enter a date with browser-native validation | `date_field(...)` | `chirpui/forms.html` | Native date input is the stable default until a popover picker has browser proof. |
| Adjust a numeric value visually | `slider(...)` or `range_field(...)` | `chirpui/slider.html`, `chirpui/forms.html` | `slider` is the standalone primitive; `range_field` is the form-field wrapper with errors and hints. |
| Show scrollable content inside a bounded panel | `scroll_area(...)` | `chirpui/scroll_area.html` | Contains overflow without custom scrollbar behavior. |
| Render a reusable row inside lists, menus, command surfaces, or result sets | `item(...)` | `chirpui/item.html` | Provides shared row anatomy without coupling to a specific parent component. |
| Render tabular records | `data_table(...)` or `table(...)` with `filter_row(...)`, `pagination(...)`, and empty/loading states | `chirpui/data_table.html`, `chirpui/table.html`, `chirpui/filter_bar.html` | Chirp UI composes data-table jobs from smaller primitives instead of shipping a grid engine. |

## Combobox Boundary

Chirp UI ships two combobox-like surfaces with different triggers and jobs:

| Surface | Registry key | Trigger | Best for |
| --- | --- | --- | --- |
| `dropdown_select(...)` | `dropdown-select` (stable) | Button showing the current label | Toolbar filters, view switchers, app-state picks from a short fixed list |
| `combobox(...)` | `combobox` (experimental) | Text input with typeahead | Form fields, tag pickers, and long option lists where users search by typing |

Both use combobox/listbox ARIA wiring, but only `combobox(...)` filters options
as the user types and writes a hidden input for normal form submission.
`dropdown_select(...)` uses `chirpuiDropdownSelect()` and dispatches
`chirpui:dropdown-selected`; `combobox(...)` uses `chirpuiCombobox()` and
dispatches `chirpui:combobox-selected`.

Use `dropdown_select(...)` when the option list is short, fixed, and chosen from
a compact control without free-text entry.

Use `combobox(...)` when the field needs typeahead search, multi-select token
pills, or a form-backed hidden value under `name`.

Use `select_field(...)` when the value belongs to a normal HTML form and should
submit with native `<select>` semantics.

Do not add a third combobox macro. See [combobox-anatomy.md](combobox-anatomy.md)
and [dropdown-anatomy.md](dropdown-anatomy.md) for rendered contracts and proof.

## Date Picker Boundary

The stable date control is `date_field(...)`. It uses a native `<input
type="date">`, which keeps platform date pickers, validation, `min`/`max`, and
form submission semantics.

A popover calendar picker remains behavior-heavy. Before promotion it needs
browser proof for focus movement, Escape/outside dismissal, keyboard navigation,
viewport containment, and reduced-motion behavior.

## Data Table Boundary

Chirp UI does not currently need a separate data-grid engine. For common record
pages, use `data_table(...)` as the parent wrapper around filters, table rows,
and pagination. For custom layouts, compose the same parts directly:

1. `filter_row(...)` for search, select filters, and export actions.
2. `table(...)` for records, alignment, sticky headers, and action columns.
3. `pagination(...)` for page movement.
4. `empty_state(...)`, `skeleton(...)`, or `progress_bar(...)` for state.
5. `scroll_area(...)` only around the region that should scroll.

Keep data-grid features such as virtual rows, column resizing, remote query
adapters, and drag-to-reorder columns out of `data_table(...)` until repeated
browser-backed examples prove those contracts.

## Proof Sources

- `tests/test_components.py::TestMaturityPrimitives` covers `toggle_group`,
  `slider`, `scroll_area`, `item`, and `data_table` rendering.
- `tests/test_manifest.py::test_dropdown_select_manifest_entry_documents_combobox_boundary`
  keeps `dropdown_select(...)` discoverable as the `dropdown-select` manifest
  entry.
- `tests/test_manifest.py::test_combobox_manifest_entry_documents_typeahead_boundary`
  keeps `combobox(...)` discoverable with its typeahead/form-field contract.
- `tests/test_components.py::TestCombobox` and `TestCombobox` render tests cover
  combobox anatomy, disabled options, and multi-select scaffold.
- `tests/test_components.py` covers `select_field`, `date_field`,
  `range_field`, `dropdown_select`, `table`, and pagination rendering.
- `tests/browser/test_dropdowns.py` covers dropdown menu and dropdown-select
  browser behavior.
- `tests/browser/test_combobox_gauntlet.py` covers combobox typeahead, roving
  select, disabled-option skip, multi-select, and axe.
- `tests/test_template_css_contract.py` and
  `tests/test_registry_emits_parity.py` keep template, CSS, and registry output
  aligned.
