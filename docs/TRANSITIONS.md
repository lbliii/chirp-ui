# Transitions and motion

ChirpUI pairs with **HTMX** swap lifecycle classes and optional **View Transitions** (when Chirp’s `AppConfig(view_transitions=True)` is set — now the default).

## HTMX swap classes

During swaps, HTMX adds classes you can style:

| Class | When |
|-------|------|
| `htmx-swapping` | Outgoing content is being removed |
| `htmx-settling` | New content is being inserted |
| `htmx-added` | New content was just added |

Use them for subtle opacity or layout transitions without JavaScript. Prefer **design tokens** for duration and easing (`--chirpui-duration-*`, `--chirpui-easing-*`) so motion stays consistent; see `TOKENS.md` and `test_transition_tokens.py` in the repo.

## View Transitions (`chirpui-transitions.css`)

Include `chirpui-transitions.css` after `chirpui.css` when using the View Transition API with Chirp’s shell layouts. The stylesheet:

- Sets `view-transition-name: none` on modals and certain OOB shell regions to avoid duplicate-name glitches.
- Defines `::view-transition-old(page-content)` / `::view-transition-new(root)` animations with short fade keyframes.
- Respects `prefers-reduced-motion: reduce`.

See comments in `src/chirp_ui/templates/chirpui-transitions.css` for caveats (e.g. avoiding `view-transition-name` on `#main` when it is the boost swap target).

## Declarative hooks (future)

A `transition()` macro or `data-chirpui-transition` attribute may be added later; until then, use HTMX classes + CSS tokens above.
