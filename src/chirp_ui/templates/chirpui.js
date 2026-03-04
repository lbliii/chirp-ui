/**
 * chirp-ui — Client-side behavior for theme/style toggle, dropdown, tray, modal, copy, tabs.
 * Include after chirpui.css. Sets data-theme and data-style on <html> from localStorage.
 *
 * Usage: <script src="/static/chirpui.js"></script>
 */
(function () {
    "use strict";

    /* Theme/style init — run immediately so attrs are set before first paint */
    var t = localStorage.getItem("chirpui-theme") || "system";
    var s = localStorage.getItem("chirpui-style") || "default";
    document.documentElement.setAttribute("data-theme", t);
    document.documentElement.setAttribute("data-style", s);

    var key = "chirpui-theme";
    var styleKey = "chirpui-style";
    var order = ["system", "light", "dark"];
    var styleOrder = ["default", "neumorphic"];
    var icons = { light: "\u25CB", dark: "\u25CF", system: "\u25D0" };
    var styleIcons = { default: "\u25A1", neumorphic: "\u25A3" };
    function setThemeIcon(btn, theme) {
        var icon = btn.querySelector("[data-chirpui-theme-icon]");
        if (icon) icon.textContent = icons[theme] || icons.system;
    }
    function initThemeToggle() {
        document.querySelectorAll("[data-chirpui-theme-toggle]").forEach(function (btn) {
            if (btn.dataset.chirpuiThemeToggleInit) return;
            btn.dataset.chirpuiThemeToggleInit = "1";
            var current = document.documentElement.getAttribute("data-theme") || "system";
            setThemeIcon(btn, current);
            function cycle() {
                current = document.documentElement.getAttribute("data-theme") || "system";
                var idx = (order.indexOf(current) + 1) % order.length;
                var next = order[idx];
                document.documentElement.setAttribute("data-theme", next);
                localStorage.setItem(key, next);
                btn.setAttribute("title", "Theme: " + next);
                setThemeIcon(btn, next);
            }
            btn.addEventListener("click", cycle);
        });
    }

    function setStyleIcon(btn, style) {
        var icon = btn.querySelector("[data-chirpui-style-icon]");
        if (icon) icon.textContent = styleIcons[style] || styleIcons.default;
    }
    function initStyleToggle() {
        document.querySelectorAll("[data-chirpui-style-toggle]").forEach(function (btn) {
            if (btn.dataset.chirpuiStyleToggleInit) return;
            btn.dataset.chirpuiStyleToggleInit = "1";
            var current = document.documentElement.getAttribute("data-style") || "default";
            setStyleIcon(btn, current);
            function cycle() {
                current = document.documentElement.getAttribute("data-style") || "default";
                var idx = (styleOrder.indexOf(current) + 1) % styleOrder.length;
                var next = styleOrder[idx];
                document.documentElement.setAttribute("data-style", next);
                localStorage.setItem(styleKey, next);
                btn.setAttribute("title", "Style: " + next);
                setStyleIcon(btn, next);
            }
            btn.addEventListener("click", cycle);
        });

        document.querySelectorAll("[data-chirpui-style-select]").forEach(function (control) {
            if (control.dataset.chirpuiStyleSelectInit) return;
            control.dataset.chirpuiStyleSelectInit = "1";
            control.value = document.documentElement.getAttribute("data-style") || "default";
            control.addEventListener("change", function () {
                var next = styleOrder.indexOf(control.value) >= 0 ? control.value : "default";
                document.documentElement.setAttribute("data-style", next);
                localStorage.setItem(styleKey, next);
                document.querySelectorAll("[data-chirpui-style-toggle]").forEach(function (btn) {
                    setStyleIcon(btn, next);
                });
            });
        });
    }

    function initThemeAndStyleControls() {
        initThemeToggle();
        initStyleToggle();
    }
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initThemeAndStyleControls);
    } else initThemeAndStyleControls();
    if (document.body) document.body.addEventListener("htmx:afterSettle", initThemeAndStyleControls);
})();

(function () {
    function initDropdowns() {
        document.querySelectorAll("[data-chirpui-dropdown]").forEach(function (root) {
            if (root.dataset.chirpuiDropdownInit) return;
            root.dataset.chirpuiDropdownInit = "1";
            var trigger = root.querySelector("[data-chirpui-dropdown-trigger]");
            var menu = root.querySelector(".chirpui-dropdown__menu");
            if (!trigger || !menu) return;
            function open() {
                menu.hidden = false;
                trigger.setAttribute("aria-expanded", "true");
                var first = menu.querySelector('[role="menuitem"], [role="option"]');
                if (first) first.focus();
                document.addEventListener("click", closeOnOutside);
                document.addEventListener("keydown", onKeydown);
            }
            function close() {
                menu.hidden = true;
                trigger.setAttribute("aria-expanded", "false");
                document.removeEventListener("click", closeOnOutside);
                document.removeEventListener("keydown", onKeydown);
                trigger.focus();
            }
            function closeOnOutside(e) {
                if (!root.contains(e.target)) close();
            }
            function onKeydown(e) {
                if (e.key === "Escape") {
                    close();
                    e.preventDefault();
                    return;
                }
                var items = [].slice.call(menu.querySelectorAll('[role="menuitem"], [role="option"]'));
                var idx = items.indexOf(document.activeElement);
                if (e.key === "ArrowDown" && idx < items.length - 1) {
                    items[idx + 1].focus();
                    e.preventDefault();
                } else if (e.key === "ArrowUp" && idx > 0) {
                    items[idx - 1].focus();
                    e.preventDefault();
                } else if (e.key === "Enter" && idx >= 0) {
                    items[idx].click();
                    close();
                    e.preventDefault();
                }
            }
            trigger.addEventListener("click", function (e) {
                e.stopPropagation();
                if (menu.hidden) open();
                else close();
            });
            menu.querySelectorAll("a, button").forEach(function (el) {
                el.addEventListener("click", function () {
                    close();
                });
            });
        });
    }
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initDropdowns);
    else initDropdowns();
    if (document.body) document.body.addEventListener("htmx:afterSettle", initDropdowns);
})();

(function () {
    function initTrays() {
        document.querySelectorAll("[data-chirpui-tray-trigger]").forEach(function (btn) {
            if (btn.dataset.chirpuiTrayInit) return;
            btn.dataset.chirpuiTrayInit = "1";
            var id = btn.getAttribute("data-tray-id");
            var tray = document.getElementById("tray-" + id);
            if (!tray) return;
            function open() {
                tray.classList.remove("chirpui-tray--closed");
                tray.classList.add("chirpui-tray--open");
                tray.setAttribute("aria-hidden", "false");
                btn.setAttribute("aria-expanded", "true");
                document.body.style.overflow = "hidden";
                var closeBtn = tray.querySelector(".chirpui-tray__close");
                if (closeBtn) setTimeout(function () {
                    closeBtn.focus();
                }, 50);
                document.addEventListener("keydown", onEscape);
            }
            function close() {
                tray.classList.add("chirpui-tray--closed");
                tray.classList.remove("chirpui-tray--open");
                tray.setAttribute("aria-hidden", "true");
                btn.setAttribute("aria-expanded", "false");
                document.body.style.overflow = "";
                btn.focus();
                document.removeEventListener("keydown", onEscape);
            }
            function onEscape(e) {
                if (e.key === "Escape") close();
            }
            btn.addEventListener("click", open);
            var closeBtn = tray.querySelector("[data-chirpui-tray-close]");
            if (closeBtn) closeBtn.addEventListener("click", close);
            var backdrop = tray.querySelector("[data-chirpui-tray-backdrop]");
            if (backdrop) backdrop.addEventListener("click", close);
        });
    }
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initTrays);
    else initTrays();
    if (document.body) document.body.addEventListener("htmx:afterSettle", initTrays);
})();

(function () {
    function initModals() {
        document.querySelectorAll("[data-chirpui-modal-trigger]").forEach(function (btn) {
            if (btn.dataset.chirpuiModalInit) return;
            btn.dataset.chirpuiModalInit = "1";
            var id = btn.getAttribute("data-modal-id");
            var modal = document.getElementById("modal-" + id);
            if (!modal) return;
            function open() {
                modal.classList.remove("chirpui-modal--closed");
                modal.classList.add("chirpui-modal--open");
                modal.setAttribute("aria-hidden", "false");
                btn.setAttribute("aria-expanded", "true");
                document.body.style.overflow = "hidden";
                var closeBtn = modal.querySelector(".chirpui-modal__close");
                if (closeBtn) setTimeout(function () {
                    closeBtn.focus();
                }, 50);
                document.addEventListener("keydown", onEscape);
            }
            function close() {
                modal.classList.add("chirpui-modal--closed");
                modal.classList.remove("chirpui-modal--open");
                modal.setAttribute("aria-hidden", "true");
                btn.setAttribute("aria-expanded", "false");
                document.body.style.overflow = "";
                btn.focus();
                document.removeEventListener("keydown", onEscape);
            }
            function onEscape(e) {
                if (e.key === "Escape") close();
            }
            btn.addEventListener("click", open);
            var closeBtn = modal.querySelector("[data-chirpui-modal-close]");
            if (closeBtn) closeBtn.addEventListener("click", close);
            var backdrop = modal.querySelector("[data-chirpui-modal-backdrop]");
            if (backdrop) backdrop.addEventListener("click", close);
        });
    }
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initModals);
    else initModals();
    if (document.body) document.body.addEventListener("htmx:afterSettle", initModals);
})();

(function () {
    function init() {
        if (!document.body) return;
        document.body.addEventListener("click", onCopyClick);
    }
    function onCopyClick(e) {
        var btn = e.target.closest("[data-chirpui-copy]");
        if (!btn) return;
        var text = btn.getAttribute("data-copy-text") || "";
        var label = btn.querySelector(".chirpui-copy-btn__label");
        var done = btn.querySelector(".chirpui-copy-btn__done");
        if (!navigator.clipboard || !navigator.clipboard.writeText) return;
        navigator.clipboard.writeText(text).then(function () {
            if (label) label.hidden = true;
            if (done) done.hidden = false;
            setTimeout(function () {
                if (label) label.hidden = false;
                if (done) done.hidden = true;
            }, 1500);
        });
    }
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
    else init();
})();

(function () {
    function init() {
        if (!document.body) return;
        document.body.addEventListener("click", onTabClick);
    }
    function onTabClick(e) {
        var btn = e.target.closest("[data-tab-trigger]");
        if (!btn) return;
        var id = btn.getAttribute("data-tab-trigger");
        var tabs = btn.closest("[data-chirpui-tabs]");
        if (!tabs) return;
        tabs.querySelectorAll("[data-tab-trigger]").forEach(function (t) {
            t.setAttribute("aria-selected", t === btn ? "true" : "false");
            t.classList.toggle("chirpui-tabs__tab--active", t === btn);
        });
        tabs.querySelectorAll("[data-tab-panel]").forEach(function (p) {
            p.hidden = p.getAttribute("data-tab-panel") !== id;
        });
    }
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
    else init();
})();
