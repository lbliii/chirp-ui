/**
 * chirp-ui — Pre-paint theme/style init only.
 * Interactive components use Alpine.js plus chirpui-alpine.js for shared controllers.
 * Include Alpine.js before components. app_shell_layout includes Alpine + pre-paint inline.
 *
 * For custom layouts: include this for theme init, or add the inline script from app_shell_layout.
 * Usage: <script src="/static/chirpui.js"></script>
 *
 * This script MUST execute synchronously (no defer/async) before first paint to prevent
 * a flash of unstyled content. Place it in <head> or early in <body>.
 */
(function () {
    "use strict";
    var t, s;
    try {
        t = localStorage.getItem("chirpui-theme");
        s = localStorage.getItem("chirpui-style");
    } catch (_) {
        /* localStorage may throw in private browsing, sandboxed iframes, or
           when storage quota is exceeded. Fall through to defaults. */
    }
    document.documentElement.setAttribute("data-theme", t || "system");
    document.documentElement.setAttribute("data-style", s || "default");
})();
