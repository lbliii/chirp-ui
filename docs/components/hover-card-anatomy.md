# Hover Card Anatomy

**Status:** shipped contract
**Scope:** `hover_card`, `hover_card__trigger`, `hover_card__content`
**Runtime:** Alpine.js through `chirpui-alpine.js`

The hover card is a delayed hover/focus preview anchored to a trigger. It opens
after a short delay on pointer enter or focus and closes on leave, blur, or
Escape. It is not a modal, not a tooltip for critical-only copy, and not a
replacement for `dropdown_menu` command surfaces.

## Macro

Import from `chirpui/hover_card.html`:

```kida
{% from "chirpui/hover_card.html" import hover_card %}

{% call hover_card(open_delay=200, close_delay=100) %}
  {% slot trigger %}<button type="button">Preview user</button>{% end %}
  <p>Profile summary with richer detail than the trigger alone.</p>
{% end %}
```

## Rendered Contract

- root class: `chirpui-hover-card` with generated `id`
- trigger wrapper: `chirpui-hover-card__trigger` with `x-ref="trigger"`
- content class: `chirpui-hover-card__content` with `role="tooltip"` and `x-ref="panel"`
- Alpine controller: `x-data="chirpuiHoverCard({ openDelay, closeDelay })"` with `x-init="init()"`
- alignment: bound `data-align-x` and `data-align-y` from `menuAlignment()`

The root listens for `@mouseenter`, `@mouseleave`, `@focusin`, `@focusout`, and
`@keydown.escape.window`. The content panel repeats pointer enter/leave handlers
so users can move from trigger to card without an immediate close.

## Open And Close Behavior

- Pointer enter on the root or content schedules open after `openDelay`
- Focus entering the root schedules open after `openDelay`
- Pointer leave or focus leaving schedules close after `closeDelay`, unless focus
  moves into the content panel
- Escape dismisses immediately through `dismiss()`
- When `prefers-reduced-motion: reduce` is active, open and close delays are
  zeroed in `init()` and content transitions are disabled in CSS

On open, `reposition()` uses `menuAlignment()` to flip the card above/below or
end/start when the default placement would overflow the viewport.

## Boundary

Use `tooltip` for compact single-line hints, `dropdown_menu` for command
selection, and `modal`/`drawer` for blocking tasks that require explicit
dismissal.

## Evidence Ledger

This ledger applies the interactive anatomy contract from
[DESIGN-interactive-anatomy.md](../decisions/interactive-anatomy.md). It is a
docs/tests contract for the rendered hover card family, not descriptor or
manifest metadata.

| Field | Hover card |
| --- | --- |
| Surface | `hover_card` delayed hover/focus preview anchored to a trigger. |
| Label | `stable` rendered macro contract under the stable `hover-card` component family. |
| Anatomy | `.chirpui-hover-card`, `.chirpui-hover-card__trigger`, `.chirpui-hover-card__content`, bound `data-align-x` / `data-align-y`, trigger/panel refs. |
| Native semantics | Content uses `role="tooltip"`; trigger content is supplied by the caller and should remain a focusable or naturally focusable control. |
| Keyboard | Focus schedules open; blur schedules close unless focus moves into the panel; Escape dismisses immediately. |
| Focus | Open does not trap focus; users can tab through trigger and panel content according to caller markup. |
| Runtime | Requires `chirpuiHoverCard()` in `chirpui-alpine.js`, Alpine refs, `x-show`, `x-cloak`, `x-transition`, and `menuAlignment()` repositioning. |
| Motion | Open/close use configurable delays; `prefers-reduced-motion: reduce` zeroes delays and disables content transitions. |
| Responsive and overflow | Content uses bounded inline size; `menuAlignment()` flips placement when the default anchor would overflow the viewport. |
| Security and escaping | Trigger and content slots render through normal template escaping; callers must not inject untrusted HTML into slots. |
| Performance | Timers are local to the hover-card root; reposition runs on open only. |
| Proof | `tests/test_components.py` checks rendered anatomy; `tests/browser/test_hover_card_gauntlet.py` checks hover/focus open, blur/Escape close, reduced-motion instant open, and viewport containment. |
| Residual risk | Automated tests cover rendered semantics and open/close behavior, but no manual screen-reader or assistive-technology proof is claimed. |

## Proof

Executable coverage lives in:

- `tests/test_components.py` for rendered anatomy, tooltip role, and slot output.
- `tests/browser/test_hover_card_gauntlet.py` for hover/focus open after delay,
  blur/Escape close, reduced-motion instant open, and viewport containment.
