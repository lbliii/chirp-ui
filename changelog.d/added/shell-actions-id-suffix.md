Added an **`id_suffix`** parameter to `shell_actions_bar()` and `shell_action()`
(`chirpui/shell_actions.html`). Passing e.g. `id_suffix="-drawer"` namespaces the
overflow dropdown id and each menu-action id, so the same actions bar can render
in two regions at once (a topbar copy plus a mobile-drawer copy) without colliding
duplicate element ids. `shell_actions_bar` threads the suffix down into each
`shell_action`. The default `""` preserves the canonical ids, keeping every
single-instance render byte-identical
([#224](https://github.com/lbliii/chirp-ui/issues/224)).
