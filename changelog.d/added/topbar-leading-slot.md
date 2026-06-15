Added an always-available **`topbar_leading`** zone to both shell entry points
(a `topbar_leading` slot on the `app_shell()` macro; a `{% block topbar_leading %}`
on `app_shell_layout.html`). It renders a **non-anchor** leading region before the
brand — the correct home for a hamburger / back / command affordance. Interactive
controls belong here, never in the `brand` slot/block (which nests inside the
brand `<a>`, producing invalid HTML and hijacking the click). The built-in
`nav_drawer` hamburger and the layout's collapsible `sidebar_toggle` render in the
same wrapper. See `docs/patterns/navigation.md § Leading affordance`
([#220](https://github.com/lbliii/chirp-ui/issues/220)).
