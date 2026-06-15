Unified active-link sync into one canonical implementation in
`shell_runtime_script()`, emitted by **both** shell entry points. The
`app_shell()` macro path now gets client active-sync it never had, and
`app_shell_layout.html` no longer carries a divergent inline copy. The shared
`syncNav` **mirrors the server's per-item `match=`**: `sidebar_link` /
`navbar_link` emit `data-chirpui-shell-match="exact"|"prefix"` only when `match=`
is set, and the JS toggles the `--active` class plus `aria-current` for those
links alone. The macro's `#chirpui-sidebar-nav` and the layout's
`#chirpui-topbar-breadcrumbs` announcers now reach parity.

**Behavior change to call out:** the layout's old blind-prefix client toggle —
which ran `path === href || path.startsWith(href + "/")` against **every** link
regardless of `match=` — is gone. Match-less sidebar/navbar links are now
**server-authoritative** (active state comes from server-rendered `active=` /
`aria-current`, not a client path guess). Shells that relied on the old
auto-highlight without setting `match=` should set `match="prefix"` (or
`match="exact"`) on those links to restore client re-highlighting across boosted
navigation ([#197](https://github.com/lbliii/chirp-ui/issues/197)).
