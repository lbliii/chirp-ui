/**
 * chirp-ui — Pre-paint theme/style init only.
 * Interactive components (dropdown, modal, tray, tabs, theme toggle, copy) use Alpine.js.
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
