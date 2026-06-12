Added a **route-context rail** region to `app_shell` (`context_rail=true` + a
`context_rail` slot on the macro; a `context_rail` flag + `{% block context_rail %}`
on `app_shell_layout.html`). It renders an optional trailing-edge secondary region
(`<aside id="chirpui-context-rail">`, a labelled `complementary` landmark) for an
inspector/detail panel that updates with the current route. The update protocol
mirrors shell actions: a route response includes an out-of-band fragment targeting
the outlet — use the new `context_rail_oob()` helper in `chirpui/oob.html`. Works
standalone with htmx OOB; under Chirp, boosted navigation carries the rail fragment
in the same response. Responsive: the rail stacks under main below 72rem and joins
the single column below 48rem. Width is `--chirpui-context-rail-width` (default
20rem); `context_rail_variant="muted"` tints the surface. This is the one blessed
shell-region composite per the [Application Chrome Posture ADR](docs/decisions/application-chrome-posture.md)
([#195](https://github.com/lbliii/chirp-ui/issues/195)).
