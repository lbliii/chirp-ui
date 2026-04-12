/**
 * chirp-ui — Pre-paint theme/style init only.
 * Interactive components use Alpine.js plus chirpui-alpine.js for shared controllers.
 * Include Alpine.js before components. app_shell_layout includes Alpine + pre-paint inline.
 *
 * For custom layouts: include this for theme init, or add the inline script from app_shell_layout.
 * Usage: <script src="/static/chirpui.js"></script>
 */
(function () {
    "use strict";
    var t = localStorage.getItem("chirpui-theme") || "system";
    var s = localStorage.getItem("chirpui-style") || "default";
    document.documentElement.setAttribute("data-theme", t);
    document.documentElement.setAttribute("data-style", s);
})();
