Fixed route-scoped shell regions stranding stale content on boosted navigation.
The `htmx:beforeSwap` reset that empties a shell region before its out-of-band
fragment lands previously lived only in `app_shell_layout.html`'s inline script
and was hardcoded to `#chirp-shell-actions` — so the `app_shell()` macro path had
no reset at all, and the new route-context rail (`#chirpui-context-rail`) was
never cleared. It is now in the shared `shell_runtime_script()` (emitted by both
shell entry points) and covers both regions: navigating to a route that ships no
fragment for a region now empties it rather than stranding the prior route's
content. Adds a Playwright gauntlet proving the rail swaps on boosted nav and
clears on a contextless route (wired into the `test-browser-chrome` gate)
([#195](https://github.com/lbliii/chirp-ui/issues/195)).
