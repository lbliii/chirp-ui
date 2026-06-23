# Combobox Anatomy

**Status:** anatomy contract (experimental surface)
**Scope:** `combobox`, `combobox__input`, `combobox__list`, `combobox__option`, `combobox__token`
**Runtime:** Alpine.js through `chirpui-alpine.js`

The combobox is a typeahead text input over a filtered `role="listbox"` of
suggestions. It uses the WAI-ARIA combobox pattern with
`aria-activedescendant` roving. It is distinct from `dropdown_select`, which
uses a button trigger over a fixed listbox, and from `select_field`, which
submits a native `<select>` value.

## Macro

Import from `chirpui/combobox.html`:

```kida
{% from "chirpui/combobox.html" import combobox %}

{{ combobox(name="country", label="Country", placeholder="Search countries…",
            options=[
  {"label": "Canada", "value": "ca"},
  {"label": "United States", "value": "us"},
  {"label": "Mexico", "value": "mx", "disabled": true},
]) }}

{{ combobox(name="tags", label="Tags", multiple=true, placeholder="Add tags…",
            options=[...]) }}
```

## Rendered Contract

- root class: `chirpui-combobox` with `--multiple` when token mode is enabled
- label class: `chirpui-combobox__label` associated with the input id
- input class: `chirpui-combobox__input` with `role="combobox"`
- list class: `chirpui-combobox__list` with `role="listbox"`
- option class: `chirpui-combobox__option` with `--active` for the roved option
- empty class: `chirpui-combobox__empty` when filtering yields no matches
- token classes: `combobox__tokens`, `combobox__token`, `combobox__token-remove`
  in multi-select mode
- Alpine controller: `x-data="chirpuiCombobox()"`
- hidden input(s): single-select writes one hidden `name`; multi-select repeats
  hidden `name` inputs per selected token

The input binds `aria-autocomplete="list"`, bound `aria-expanded`, bound
`aria-controls`, and bound `aria-activedescendant`. Options bind `role="option"`,
escaped `data-label` / `data-value`, and `aria-disabled="true"` when disabled.

## Selection Events

Single-select dispatches `chirpui:combobox-selected` with:

```javascript
{ value: "us", label: "United States" }
```

Multi-select dispatches the same payload each time a token is added. Removing a
pill does not dispatch an event in v1.

## Focus And Keyboard Behavior

- Typing filters visible options client-side (substring match on label)
- Focus opens the list when options exist
- ArrowDown and ArrowUp rove visible enabled options via `aria-activedescendant`
- Enter selects the active option (or the sole visible match)
- Escape closes the list and keeps focus on the input
- Click outside closes the list
- Multi-select: Backspace on an empty input removes the last token; remove
  buttons drop individual tokens and restore options to the list

Disabled options remain visible but are skipped during roving and cannot be
selected.

## Boundary

| Need | Use | Why |
| --- | --- | --- |
| Submit a form value from a short static option list | `select_field(...)` | Native `<select>` keeps mobile pickers, validation, and form submit semantics. |
| Pick from a compact toolbar/filter menu without typing | `dropdown_select(...)` | Button trigger over a fixed listbox; stable surface for app-state filters. |
| Type to search a long or open-ended option list | `combobox(...)` | Text input typeahead with optional multi-select token pills and hidden form values. |
| Global search over remote results | `command_palette(...)` or app search wiring | Combobox filters a server-rendered option list; it is not a remote search shell. |

Do not add a second combobox macro. `dropdown_select(...)` and `combobox(...)`
cover the two combobox-like jobs: fixed-list selection vs typeahead form input.

## Evidence Ledger

This ledger applies the interactive anatomy contract from
[DESIGN-interactive-anatomy.md](../decisions/interactive-anatomy.md). It is a
docs/tests contract for the rendered combobox, not descriptor or manifest
metadata.

| Field | Combobox |
| --- | --- |
| Surface | `combobox` typeahead input over a filtered listbox; optional multi-select tokens. |
| Label | `experimental` rendered macro contract; keep experimental until browser gauntlet and disposition review complete. |
| Anatomy | `.chirpui-combobox`, label, input, listbox, options, empty state, hidden value input(s), optional token scaffold. |
| Native semantics | Text input with `role="combobox"`, `aria-autocomplete="list"`, bound expansion/controls/active-descendant; listbox/options with `aria-selected`; disabled options use `aria-disabled="true"`. |
| Keyboard | Filter on input; ArrowDown/ArrowUp rove enabled visible options; Enter selects; Escape closes; multi-select Backspace removes last token. |
| Focus | Input keeps focus during roving via `aria-activedescendant`; selection returns focus to input with reopen suppressed briefly. |
| Runtime | Requires `chirpuiCombobox()` in `chirpui-alpine.js`, Alpine refs, `x-show`, `x-cloak`, `x-transition`, and click-outside close. |
| Motion | List uses `x-transition`; reduced-motion expectations follow component CSS. |
| Responsive and overflow | Options scroll within the list; `scrollIntoView({ block: "nearest" })` keeps the active option visible. |
| Security and escaping | Option labels/values are HTML-escaped in `data-*` attributes; Alpine reads payloads from DOM attributes, not interpolated JS literals. |
| Performance | Filtering is local to the combobox root; no page-global observers. |
| Proof | `tests/test_components.py` checks rendered anatomy and disabled options; `tests/browser/test_combobox_gauntlet.py` covers filter, roving, select, Escape, click-outside, disabled skip, multi-select, and axe. |
| Residual risk | Arrow/Enter paths use Alpine factory hooks in headless CI where Playwright keydown through Alpine is unreliable; manual screen-reader proof is not claimed. |

## Proof

Executable coverage lives in:

- `tests/test_components.py::TestCombobox` for rendered anatomy, initial value,
  multi-select scaffold, and disabled options.
- `tests/browser/test_combobox_gauntlet.py` for typeahead filter, roving select,
  Escape/click-outside, disabled-option skip, multi-select tokens, and axe.

See also [control-selection.md](control-selection.md) for the authoring decision
matrix across native select, dropdown-select, and combobox.
