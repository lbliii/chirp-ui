Extended `check_alpine_runtime()` to detect Alpine **core** (not just the
`chirpui-alpine.js` registration script): the result now carries `core_loaded`
and `core_url_valid` plus a human-readable `problems` tuple, and flags the
silent CDN footgun where an Alpine core `<script>` is present but its URL is a
bare `alpinejs@<version>` (CommonJS) instead of the browser build ending in
`/dist/cdn.min.js`. Detection is framework-agnostic (matches `alpinejs@` /
`@alpinejs/csp` srcs and Chirp's `data-chirp="alpine"` marker, and ignores the
mask/intersect/focus plugins). The existing `ok` / `script_loaded` contract is
unchanged ([#191](https://github.com/lbliii/chirp-ui/issues/191)).
