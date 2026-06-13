Added an opt-in **mobile nav drawer** to `app_shell` (`nav_drawer=true` on the
macro; `nav_drawer=True` in the render context for `app_shell_layout.html`).
Below the 48rem breakpoint a topbar hamburger opens the sidebar as an accessible
off-canvas slide-over, and — with `context_rail=true` — a second trigger opens
the rail. It is a thin, additive affordance over the existing regions: the same
sidebar/rail `<aside>` is repositioned (no duplicated nav), so `aria-current`,
`syncNav`, and OOB swaps keep working; unset, the shell is byte-for-byte
unchanged (the horizontal-strip fallback). The open/close behavior — focus trap,
`Esc`, scrim dismiss, body scroll-lock, focus return, link-dismiss, and
auto-close when the viewport grows past the breakpoint — is vanilla JS in
`shell_runtime_script()` with **no Alpine dependency** ("works without Chirp,
better with Chirp"). The open drawer is `role="dialog" aria-modal="true"` and
named (sidebar via `aria-labelledby`, rail via its `aria-label`); the rail's
close control is injected by the runtime so it is never stranded by the rail's
OOB content swaps. Proven end-to-end by `tests/browser/test_shell_nav_drawer_gauntlet.py`
(in the `test-browser-chrome-check` gate). See `docs/patterns/navigation.md § Mobile Nav Drawer`
([#196](https://github.com/lbliii/chirp-ui/issues/196)).
