(function () {
    "use strict";

    if (window.__chirpuiAlpineRuntimeLoaded) {
        return;
    }
    window.__chirpuiAlpineRuntimeLoaded = true;

    function safeGetItem(key) {
        try {
            return window.localStorage.getItem(key);
        } catch {
            return null;
        }
    }

    function safeSetItem(key, value) {
        try {
            window.localStorage.setItem(key, value);
        } catch (e) {
            console.warn(
                'chirp-ui: localStorage write failed for key "' +
                    key +
                    '":',
                e.message
            );
        }
    }

    function safeRemoveItem(key) {
        try {
            window.localStorage.removeItem(key);
        } catch {}
    }

    function focusElement(element) {
        if (element && typeof element.focus === "function") {
            element.focus();
        }
    }

    function parseInteger(value, fallback) {
        var parsed = Number.parseInt(value || "", 10);
        return Number.isFinite(parsed) ? parsed : fallback;
    }

    function readDocumentPreference(attribute, fallback) {
        return document.documentElement.getAttribute(attribute) || fallback;
    }

    function writeDocumentPreference(attribute, storageKey, value) {
        document.documentElement.setAttribute(attribute, value);
        safeSetItem(storageKey, value);
    }

    function resolveDialogTarget(element) {
        var target = element.dataset.dialogTarget || element.dataset.target || "";
        return target ? document.getElementById(target) : null;
    }

    function menuAlignment(trigger, panel) {
        var padding = 12;
        var panelRect = panel.getBoundingClientRect();
        var triggerRect = trigger.getBoundingClientRect();
        var rightSpace = window.innerWidth - triggerRect.left - padding;
        var leftSpace = triggerRect.right - padding;
        var bottomSpace = window.innerHeight - triggerRect.bottom - padding;
        var topSpace = triggerRect.top - padding;

        return {
            alignX: panelRect.width > rightSpace && leftSpace > rightSpace ? "end" : "start",
            alignY: panelRect.height > bottomSpace && topSpace > bottomSpace ? "top" : "bottom",
        };
    }

    function createDropdownState() {
        return {
            open: false,
            alignX: "start",
            alignY: "bottom",
            toggle: function () {
                if (this.open) {
                    return this.close();
                }
                focusElement(this.$refs.trigger);
                this.open = true;
                this.$nextTick(
                    function () {
                        this.reposition();
                    }.bind(this)
                );
            },
            close: function (focusAfter) {
                if (!this.open) {
                    return;
                }
                this.open = false;
                focusElement(focusAfter);
            },
            selectItem: function (element, focusAfter) {
                var detail = { label: element.dataset.label || "" };
                if (element.dataset.href) {
                    detail.href = element.dataset.href;
                }
                if (element.dataset.action) {
                    detail.action = element.dataset.action;
                }
                this.close(focusAfter);
                this.$dispatch("chirpui:dropdown-selected", detail);
            },
            reposition: function () {
                var panel = this.$refs.panel;
                var trigger = this.$refs.trigger;
                if (!panel || !trigger) {
                    return;
                }
                var alignment = menuAlignment(trigger, panel);
                this.alignX = alignment.alignX;
                this.alignY = alignment.alignY;
            },
        };
    }

    var _registeredComponents = {};

    // ── Alpine runtime self-check (silent-disable guard) ────────────────
    // When Alpine never loads — a missing/blocked/misconfigured CDN script,
    // a CSP block, a network error, or alpine=False — register()'s factories
    // queue on an `alpine:init` event that never fires, and every chirp-ui
    // component is silently inert with a clean console. This guard makes that
    // failure LOUD instead. See CLAUDE.md troubleshooting:
    // "all interactive components are dead".
    var _alpineInitSeen = false;
    var _alpineHealthWarned = false;
    var ALPINE_HEALTH_CHECK_DELAY_MS = 1500;

    document.addEventListener("alpine:init", function () {
        _alpineInitSeen = true;
    });

    function chirpuiAlpineComponents() {
        var nodes = document.querySelectorAll("[x-data]");
        var matches = [];
        for (var i = 0; i < nodes.length; i++) {
            var value = nodes[i].getAttribute("x-data") || "";
            if (/chirpui\w+\s*\(/.test(value)) {
                matches.push(nodes[i]);
            }
        }
        return matches;
    }

    function runAlpineHealthCheck() {
        if (_alpineHealthWarned) {
            return;
        }
        // Alpine is alive — nothing to warn about. These are the only honest
        // signals that Alpine actually ran: window.Alpine is set by the core
        // script, and alpine:init only fires once the core script executes.
        // (Chirp's inline window._chirpAlpineData bridge is NOT a signal: it
        // is injected alongside Alpine and merely queues registrations until
        // an alpine:init that never comes if the core script failed to load.)
        if (window.Alpine || _alpineInitSeen) {
            return;
        }
        var needers = chirpuiAlpineComponents();
        if (!needers.length) {
            return;
        }
        _alpineHealthWarned = true;
        console.warn(
            "[chirp-ui] Alpine.js never initialized, but " +
                needers.length +
                " chirp-ui component(s) on this page require it — they are now " +
                "INERT (dropdowns, modals, theme/style toggles, tabs, copy " +
                "buttons, and the collapsible sidebar will not respond).\n" +
                "Likely causes:\n" +
                "  1. The Alpine core <script> is missing. Chirp injects it via " +
                "use_chirp_ui(app); confirm alpine=True and that a " +
                '<script data-chirp="alpine"> tag is in the page.\n' +
                "  2. The Alpine CDN URL is wrong: it must end in " +
                "/dist/cdn.min.js. A bare alpinejs@<version> resolves to a " +
                "CommonJS build that fails silently in browsers.\n" +
                '  3. A Content-Security-Policy or network error blocked it ' +
                '(a "Script error." at line 0 in the console = cross-origin ' +
                "failure masking the real error).\n" +
                "See chirp-ui troubleshooting: \"all interactive components are " +
                "dead\" (https://github.com/lbliii/chirp-ui)."
        );
    }

    function scheduleAlpineHealthCheck() {
        function arm() {
            window.setTimeout(runAlpineHealthCheck, ALPINE_HEALTH_CHECK_DELAY_MS);
        }
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", arm, { once: true });
        } else {
            arm();
        }
        // Components can arrive via htmx swaps after the initial check; re-run
        // cheaply (a no-op once Alpine is alive or we've already warned).
        document.addEventListener("htmx:afterSettle", runAlpineHealthCheck);
    }

    function register(name, factory) {
        if (_registeredComponents[name]) {
            return;
        }
        _registeredComponents[name] = true;

        if (window.Alpine && window.Alpine.version) {
            var reg = window.Alpine.safeData || window.Alpine.data;
            reg(name, factory);
            return;
        }
        if (typeof window._chirpAlpineData === "function") {
            window._chirpAlpineData(name, factory);
            return;
        }
        document.addEventListener(
            "alpine:init",
            function () {
                if (window.Alpine) {
                    var reg = window.Alpine.safeData || window.Alpine.data;
                    reg(name, factory);
                }
            },
            { once: true }
        );
    }

    document.addEventListener(
        "alpine:init",
        function () {
            if (
                window.Alpine &&
                typeof window.Alpine.store === "function"
            ) {
                if (!window.Alpine.store("modals")) {
                    window.Alpine.store("modals", {});
                }
                if (!window.Alpine.store("trays")) {
                    window.Alpine.store("trays", {});
                }
            }
        },
        { once: true }
    );

    register("chirpuiDropdown", function () {
        return createDropdownState();
    });

    register("chirpuiDropdownSelect", function () {
        var state = createDropdownState();
        return {
            open: state.open,
            alignX: state.alignX,
            alignY: state.alignY,
            selected: "",
            focusedIndex: 0,
            itemCount: 0,
            init: function () {
                this.selected = this.$el.dataset.selected || "";
                this.itemCount = parseInteger(this.$el.dataset.itemCount, 0);
            },
            toggle: function () {
                if (this.open) {
                    return this.close();
                }
                this.open = true;
                this.$nextTick(
                    function () {
                        this.reposition();
                        this.focusedIndex = 0;
                        focusElement(this.$refs["item-0"]);
                    }.bind(this)
                );
            },
            close: state.close,
            reposition: state.reposition,
            keyDown: function () {
                var maxIndex = Math.max(this.itemCount - 1, 0);
                if (this.focusedIndex < maxIndex) {
                    this.focusedIndex += 1;
                    focusElement(this.$refs["item-" + this.focusedIndex]);
                }
            },
            keyUp: function () {
                if (this.focusedIndex > 0) {
                    this.focusedIndex -= 1;
                    focusElement(this.$refs["item-" + this.focusedIndex]);
                }
            },
            keyEnter: function () {
                var element = this.$refs["item-" + this.focusedIndex];
                if (!element) {
                    return;
                }
                this.selected = element.dataset.label || "";
                this.close(this.$refs.trigger);
                this.$dispatch("chirpui:dropdown-selected", {
                    label: this.selected,
                    value: element.dataset.value || this.selected,
                });
            },
        };
    });

    // Right-click / keyboard context menu anchored at the pointer. Roving
    // tabindex over role="menuitem" children; opens at clientX/clientY (mouse)
    // or the region's box (keyboard) and clamps to the viewport. Disabled items
    // (aria-disabled) stay focusable but inert, per WAI-ARIA. $root is the
    // focusable region; $refs.panel is the role="menu" surface.
    register("chirpuiContextMenu", function () {
        return {
            open: false,
            x: 0,
            y: 0,
            focusedIndex: -1,
            itemCount: 0,
            init: function () {
                this.itemCount = parseInteger(this.$root.dataset.itemCount, 0);
            },
            openAt: function (event) {
                event.preventDefault();
                this._show(event.clientX, event.clientY);
            },
            openAtElement: function () {
                var rect = this.$refs.trigger.getBoundingClientRect();
                this._show(rect.left, rect.top + rect.height);
            },
            onTriggerKeydown: function (event) {
                if (this.open) {
                    return;
                }
                var key = event.key;
                var isOpenKey =
                    key === "Enter" ||
                    key === " " ||
                    key === "Spacebar" ||
                    key === "ArrowDown" ||
                    key === "ContextMenu" ||
                    (event.shiftKey && key === "F10");
                if (!isOpenKey) {
                    return;
                }
                event.preventDefault();
                this.openAtElement();
            },
            _show: function (x, y) {
                this.x = x;
                this.y = y;
                this.open = true;
                this.$nextTick(
                    function () {
                        this.clampToViewport();
                        this.focusedIndex = 0;
                        focusElement(this.$refs["item-0"]);
                    }.bind(this)
                );
            },
            close: function () {
                if (!this.open) {
                    return;
                }
                this.open = false;
                this.focusedIndex = -1;
                // Return focus to the trigger synchronously (mirrors dropdown):
                // moving focus before Alpine hides the panel keeps the panel-hide
                // blur from stranding focus on <body>.
                focusElement(this.$refs.trigger);
            },
            clampToViewport: function () {
                var panel = this.$refs.panel;
                if (!panel) {
                    return;
                }
                var rect = panel.getBoundingClientRect();
                var pad = 8;
                if (this.x + rect.width + pad > window.innerWidth) {
                    this.x = Math.max(pad, window.innerWidth - rect.width - pad);
                }
                if (this.y + rect.height + pad > window.innerHeight) {
                    this.y = Math.max(pad, window.innerHeight - rect.height - pad);
                }
                this.x = Math.max(pad, this.x);
                this.y = Math.max(pad, this.y);
            },
            keyDown: function () {
                var maxIndex = Math.max(this.itemCount - 1, 0);
                if (this.focusedIndex < maxIndex) {
                    this.focusedIndex += 1;
                    focusElement(this.$refs["item-" + this.focusedIndex]);
                }
            },
            keyUp: function () {
                if (this.focusedIndex > 0) {
                    this.focusedIndex -= 1;
                    focusElement(this.$refs["item-" + this.focusedIndex]);
                }
            },
            keyHome: function () {
                this.focusedIndex = 0;
                focusElement(this.$refs["item-0"]);
            },
            keyEnd: function () {
                this.focusedIndex = Math.max(this.itemCount - 1, 0);
                focusElement(this.$refs["item-" + this.focusedIndex]);
            },
            selectItem: function (element) {
                if (
                    !element ||
                    element.getAttribute("aria-disabled") === "true"
                ) {
                    return;
                }
                var detail = { label: element.dataset.label || "" };
                if (element.dataset.action) {
                    detail.action = element.dataset.action;
                }
                if (element.dataset.href) {
                    detail.href = element.dataset.href;
                }
                this.close();
                this.$dispatch("chirpui:context-menu-selected", detail);
            },
        };
    });

    // Combobox / autocomplete: a role="combobox" text input over a filtered
    // role="listbox". Options are server-rendered <li role="option"> elements;
    // the factory filters them by the typed query (x-show via matches()), roves
    // the visible subset with aria-activedescendant, and on select writes the
    // option label to the visible input + the value to the hidden input.
    register("chirpuiCombobox", function () {
        return {
            open: false,
            query: "",
            activeId: "",
            multiple: false,
            selected: [],
            _suppressOpen: false,
            init: function () {
                this.multiple = this.$root.dataset.multiple === "true";
                this.query = this.$refs.input.value || "";
            },
            _options: function () {
                return Array.prototype.slice.call(
                    this.$root.querySelectorAll(".chirpui-combobox__option")
                );
            },
            _isSelected: function (value) {
                for (var i = 0; i < this.selected.length; i++) {
                    if (this.selected[i].value === value) {
                        return true;
                    }
                }
                return false;
            },
            _visible: function () {
                var q = this.query.trim().toLowerCase();
                var self = this;
                return this._options().filter(function (o) {
                    if (self.multiple && self._isSelected(o.dataset.value || "")) {
                        return false;
                    }
                    var label = (o.dataset.label || "").toLowerCase();
                    return !q || label.indexOf(q) !== -1;
                });
            },
            matches: function (label, value) {
                // Already-selected options drop out of the multi-select list.
                if (this.multiple && this._isSelected(value)) {
                    return false;
                }
                var q = this.query.trim().toLowerCase();
                return !q || (label || "").toLowerCase().indexOf(q) !== -1;
            },
            visibleCount: function () {
                return this._visible().length;
            },
            onInput: function () {
                this.query = this.$refs.input.value;
                this.open = true;
                var active = this.activeId;
                var stillVisible = this._visible().some(function (o) {
                    return o.id === active;
                });
                if (!stillVisible) {
                    this.activeId = "";
                }
            },
            openList: function () {
                // Skip the focus that choose() re-issues after a selection, so
                // returning focus to the input does not immediately reopen the list.
                if (this._suppressOpen) {
                    return;
                }
                if (this._options().length) {
                    this.open = true;
                }
            },
            close: function () {
                this.open = false;
                this.activeId = "";
            },
            move: function (delta) {
                var vis = this._visible();
                this.open = true;
                if (!vis.length) {
                    return;
                }
                var idx = -1;
                for (var i = 0; i < vis.length; i++) {
                    if (vis[i].id === this.activeId) {
                        idx = i;
                        break;
                    }
                }
                idx = idx === -1 ? (delta > 0 ? 0 : vis.length - 1) : idx + delta;
                if (idx < 0) {
                    idx = vis.length - 1;
                }
                if (idx >= vis.length) {
                    idx = 0;
                }
                this.activeId = vis[idx].id;
                vis[idx].scrollIntoView({ block: "nearest" });
            },
            selectActive: function () {
                var el = this.activeId ? document.getElementById(this.activeId) : null;
                if (!el) {
                    var vis = this._visible();
                    if (vis.length === 1) {
                        el = vis[0];
                    } else {
                        return;
                    }
                }
                this.choose(el);
            },
            choose: function (el) {
                if (!el) {
                    return;
                }
                var label = el.dataset.label || "";
                var value = el.dataset.value || "";
                if (this.multiple) {
                    this.addToken({ value: value, label: label });
                    // Clear the query and keep the list open for the next pick;
                    // the chosen option drops out of the list (now selected).
                    this.$refs.input.value = "";
                    this.query = "";
                    this.activeId = "";
                    this.open = true;
                    this.$refs.input.focus();
                    this.$dispatch("chirpui:combobox-selected", {
                        value: value,
                        label: label,
                    });
                    return;
                }
                this.$refs.input.value = label;
                this.query = label;
                if (this.$refs.value) {
                    this.$refs.value.value = value;
                }
                this.open = false;
                this.activeId = "";
                // Suppress only the focus() reopen below; clear on the next tick
                // so a later genuine focus still opens the list (the keyboard
                // path leaves the input already focused, firing no focus event).
                this._suppressOpen = true;
                this.$refs.input.focus();
                this.$nextTick(
                    function () {
                        this._suppressOpen = false;
                    }.bind(this)
                );
                this.$dispatch("chirpui:combobox-selected", {
                    value: value,
                    label: label,
                });
            },
            addToken: function (token) {
                if (!this._isSelected(token.value)) {
                    this.selected.push(token);
                }
            },
            removeToken: function (value) {
                this.selected = this.selected.filter(function (t) {
                    return t.value !== value;
                });
                this.$refs.input.focus();
            },
            removeLast: function () {
                if (this.selected.length) {
                    this.selected.pop();
                }
            },
            onBackspace: function () {
                // Backspace on the empty input removes the last pill (multi only).
                if (this.multiple && !this.$refs.input.value && this.selected.length) {
                    this.removeLast();
                }
            },
        };
    });

    // Command palette: opens the <dialog> on Cmd/Ctrl+K and adds arrow-key
    // navigation over htmx-loaded results. The role=combobox input tracks the
    // active role=option via aria-activedescendant; each fresh result set
    // (htmx:afterSettle into the results listbox) auto-highlights its first item.
    register("chirpuiCommandPalette", function () {
        return {
            activeId: "",
            hasOptions: false,
            init: function () {
                this.refresh();
                var self = this;
                this._onSettle = function (e) {
                    var target = e.detail && e.detail.target;
                    var results = self.$refs.results;
                    if (results && target && (target === results || results.contains(target))) {
                        self.refresh();
                    }
                };
                document.addEventListener("htmx:afterSettle", this._onSettle);
            },
            destroy: function () {
                if (this._onSettle) {
                    document.removeEventListener("htmx:afterSettle", this._onSettle);
                }
            },
            open: function () {
                var dialog = this.$refs.dialog;
                if (dialog && typeof dialog.showModal === "function" && !dialog.open) {
                    dialog.showModal();
                }
            },
            _options: function () {
                return this.$refs.results
                    ? Array.prototype.slice.call(
                          this.$refs.results.querySelectorAll('[role="option"]')
                      )
                    : [];
            },
            // Set aria-selected + the --active class imperatively (the options are
            // htmx-swapped plain HTML with no Alpine directives — binding them via
            // x-bind would fight the swap). The input's aria-activedescendant is an
            // Alpine binding on the non-swapped input, so it stays reactive.
            _applyActive: function () {
                var opts = this._options();
                for (var i = 0; i < opts.length; i++) {
                    var on = opts[i].id === this.activeId;
                    opts[i].setAttribute("aria-selected", on ? "true" : "false");
                    opts[i].classList.toggle(
                        "chirpui-command-palette__item--active",
                        on
                    );
                }
            },
            refresh: function () {
                // A new result set landed — highlight the first item so Enter runs it.
                var opts = this._options();
                this.hasOptions = opts.length > 0;
                this.activeId = opts.length ? opts[0].id : "";
                this._applyActive();
            },
            move: function (delta) {
                var opts = this._options();
                if (!opts.length) {
                    return;
                }
                var idx = -1;
                for (var i = 0; i < opts.length; i++) {
                    if (opts[i].id === this.activeId) {
                        idx = i;
                        break;
                    }
                }
                idx = idx === -1 ? (delta > 0 ? 0 : opts.length - 1) : idx + delta;
                if (idx < 0) {
                    idx = opts.length - 1;
                }
                if (idx >= opts.length) {
                    idx = 0;
                }
                this.activeId = opts[idx].id;
                this._applyActive();
                opts[idx].scrollIntoView({ block: "nearest" });
            },
            activate: function () {
                var el = this.activeId ? document.getElementById(this.activeId) : null;
                if (el) {
                    el.click();
                }
            },
        };
    });

    register("chirpuiTabs", function () {
        return {
            active: "",
            init: function () {
                this.active = this.$el.dataset.active || "";
            },
            selectTab: function (element) {
                this.active = element.dataset.tabId || "";
                this.$dispatch("chirpui:tab-changed", { tab: this.active });
            },
        };
    });

    register("chirpuiCopy", function () {
        return {
            copied: false,
            _resetTimer: 0,
            resolveText: function () {
                return this.$el.dataset.copyText || this.$el.previousElementSibling?.textContent || "";
            },
            resolveDelay: function () {
                return parseInteger(this.$el.dataset.copyTimeout, 1500);
            },
            copy: async function () {
                var text = this.resolveText();
                if (!text || !navigator.clipboard || !navigator.clipboard.writeText) {
                    return;
                }
                await navigator.clipboard.writeText(text);
                this.copied = true;
                window.clearTimeout(this._resetTimer);
                this._resetTimer = window.setTimeout(
                    function () {
                        this.copied = false;
                    }.bind(this),
                    this.resolveDelay()
                );
            },
        };
    });

    register("chirpuiFader", function (config) {
        config = config || {};
        return {
            value: 0,
            steps: 8,
            init: function () {
                this.steps = Math.max(parseInteger(config.steps, 8), 1);
                var input = this.$el.querySelector(".chirpui-ascii-fader__input");
                this.setValue(input ? input.value : config.value);
            },
            setValue: function (rawValue) {
                var parsed = Number.parseFloat(rawValue);
                if (!Number.isFinite(parsed)) {
                    parsed = Number.parseFloat(config.value);
                }
                if (!Number.isFinite(parsed)) {
                    parsed = 0;
                }
                this.value = Math.min(100, Math.max(0, Math.round(parsed)));
            },
            level: function () {
                return Math.min(
                    this.steps,
                    Math.max(0, Math.trunc((this.value / 100) * this.steps))
                );
            },
            isFilled: function (index) {
                return index <= this.level();
            },
            segmentGlyph: function (index) {
                return this.isFilled(index) ? "█" : "░";
            },
        };
    });

    register("chirpuiSseRetry", function () {
        return {
            retrying: false,
            init: function () {
                var reset = function () {
                    this.retrying = false;
                }.bind(this);
                [
                    "htmx:afterRequest",
                    "htmx:after-request",
                    "htmx:afterSettle",
                    "htmx:after-settle",
                    "htmx:responseError",
                    "htmx:response-error",
                    "htmx:sendError",
                    "htmx:send-error",
                ].forEach(
                    function (eventName) {
                        this.$el.addEventListener(eventName, reset);
                    }.bind(this)
                );
            },
            retry: function () {
                this.retrying = true;
            },
        };
    });

    register("chirpuiThemeToggle", function () {
        return {
            theme: "system",
            icons: { light: "\u25CB", dark: "\u25CF", system: "\u25D0" },
            init: function () {
                this.theme = readDocumentPreference("data-theme", "system");
            },
            cycle: function () {
                var order = ["system", "light", "dark"];
                var index = (order.indexOf(this.theme) + 1) % order.length;
                this.theme = order[index];
                writeDocumentPreference("data-theme", "chirpui-theme", this.theme);
            },
        };
    });

    register("chirpuiStyleToggle", function () {
        return {
            style: "default",
            icons: { default: "\u25A1", neumorphic: "\u25A3" },
            init: function () {
                this.style = readDocumentPreference("data-style", "default");
            },
            cycle: function () {
                var order = ["default", "neumorphic"];
                var index = (order.indexOf(this.style) + 1) % order.length;
                this.style = order[index];
                writeDocumentPreference("data-style", "chirpui-style", this.style);
            },
        };
    });

    register("chirpuiStyleSelect", function () {
        return {
            style: "default",
            init: function () {
                this.style = readDocumentPreference("data-style", "default");
                this.$el.value = this.style;
            },
            change: function () {
                this.style = this.$el.value;
                writeDocumentPreference("data-style", "chirpui-style", this.style);
            },
        };
    });

    register("chirpuiDialogTarget", function () {
        return {
            open: function () {
                var dialog = resolveDialogTarget(this.$el);
                if (dialog && typeof dialog.showModal === "function") {
                    dialog.showModal();
                }
            },
        };
    });

    register("chirpuiSidebar", function (options) {
        var config = options || {};
        return {
            collapsible: Boolean(config.collapsible),
            resizable: Boolean(config.resizable),
            collapsed: false,
            _dragging: false,
            _startX: 0,
            _startCollapsed: false,
            _lastX: 0,
            init: function () {
                if (!this.collapsible) {
                    this.collapsed = false;
                    this.$el.classList.remove("chirpui-app-shell--sidebar-collapsed");
                    return;
                }
                this.collapsed = this.readInitialCollapsed();
                this.$el.classList.toggle("chirpui-app-shell--sidebar-collapsed", this.collapsed);
            },
            readInitialCollapsed: function () {
                var collapsed = safeGetItem("chirpui-sidebar-collapsed");
                if (collapsed === null && this.resizable) {
                    var legacyWidth = safeGetItem("chirpui-sidebar-width");
                    if (legacyWidth) {
                        var match = legacyWidth.match(/^(\d+)(px|rem)$/);
                        var pixels = null;
                        if (match) {
                            pixels =
                                match[2] === "rem"
                                    ? Number.parseInt(match[1], 10) * 16
                                    : Number.parseInt(match[1], 10);
                        }
                        collapsed = pixels !== null && pixels <= 96 ? "true" : "false";
                        safeRemoveItem("chirpui-sidebar-width");
                    } else {
                        collapsed = "false";
                    }
                }
                return collapsed === "true";
            },
            setCollapsed: function (value) {
                this.collapsed = Boolean(value);
                this.$el.classList.toggle("chirpui-app-shell--sidebar-collapsed", this.collapsed);
                this.$el.style.removeProperty("--chirpui-sidebar-width");
                safeSetItem("chirpui-sidebar-collapsed", this.collapsed ? "true" : "false");
                var handle = this.$el.querySelector("[data-chirpui-sidebar-toggle]");
                if (handle) {
                    handle.setAttribute("aria-expanded", this.collapsed ? "false" : "true");
                }
            },
            toggle: function () {
                if (!this.collapsible) {
                    return;
                }
                this.setCollapsed(!this.collapsed);
            },
            startDrag: function (event) {
                if (!this.resizable) {
                    this.toggle();
                    return;
                }
                event.preventDefault();
                this._dragging = true;
                this._startX = event.clientX;
                this._startCollapsed = this.collapsed;
                this._lastX = event.clientX;
                document.body.style.userSelect = "none";
            },
            onMove: function (event) {
                if (!this._dragging) {
                    return;
                }
                this._lastX = event.clientX;
            },
            onUp: function () {
                if (!this._dragging) {
                    return;
                }
                this._dragging = false;
                document.body.style.userSelect = "";
                var delta = this._lastX - this._startX;
                if (Math.abs(delta) >= 5) {
                    if (delta < 0 && !this._startCollapsed) {
                        this.setCollapsed(true);
                    } else if (delta > 0 && this._startCollapsed) {
                        this.setCollapsed(false);
                    }
                } else {
                    this.toggle();
                }
            },
        };
    });

    register("chirpuiResponsiveSidebar", function () {
        return {
            query: null,
            sections: [],
            _listeners: [],
            init: function () {
                this.query = window.matchMedia("(max-width: 48rem)");
                this.sections = Array.from(
                    this.$el.querySelectorAll("details.chirpui-sidebar__section")
                );
                this.sections.forEach(
                    function (section) {
                        var onToggle = function () {
                            this.syncOpenSection(section);
                        }.bind(this);
                        section.addEventListener("toggle", onToggle);
                        this._listeners.push([section, "toggle", onToggle]);
                    }.bind(this)
                );

                var onChange = function () {
                    this.syncMode();
                }.bind(this);
                if (typeof this.query.addEventListener === "function") {
                    this.query.addEventListener("change", onChange);
                    this._listeners.push([this.query, "change", onChange]);
                } else if (typeof this.query.addListener === "function") {
                    this.query.addListener(onChange);
                    this._listeners.push([this.query, "legacy-change", onChange]);
                }
                this.syncMode();
            },
            destroy: function () {
                this._listeners.forEach(function (entry) {
                    var target = entry[0];
                    var event = entry[1];
                    var listener = entry[2];
                    if (event === "legacy-change" && typeof target.removeListener === "function") {
                        target.removeListener(listener);
                    } else if (typeof target.removeEventListener === "function") {
                        target.removeEventListener(event, listener);
                    }
                });
                this._listeners = [];
            },
            isResponsive: function () {
                return Boolean(this.query && this.query.matches);
            },
            syncMode: function () {
                if (this.isResponsive()) {
                    this.closeMenus();
                    return;
                }
                this.sections.forEach(function (section) {
                    section.open = true;
                });
            },
            syncOpenSection: function (activeSection) {
                if (!this.isResponsive()) {
                    if (!activeSection.open) {
                        window.requestAnimationFrame(function () {
                            activeSection.open = true;
                        });
                    }
                    return;
                }
                if (!activeSection.open) {
                    return;
                }
                this.sections.forEach(function (section) {
                    if (section !== activeSection) {
                        section.open = false;
                    }
                });
            },
            closeMenus: function () {
                if (!this.isResponsive()) {
                    return;
                }
                this.sections.forEach(function (section) {
                    section.open = false;
                });
            },
        };
    });

    register("chirpuiGridSelection", function () {
        return {
            selected: new Set(),
            count: 0,
            total: 0,
            allSelected: false,
            someSelected: false,
            // Cache the component root in init(). Alpine's `this.$el` is the
            // element the *current* expression is bound to — inside a method
            // invoked from a child checkbox's @change it is that checkbox, not
            // the grid root, so querying it for row boxes would find nothing.
            // `this.$root` is the nearest x-data root and is stable across
            // every handler, so all row queries go through it.
            root: function () {
                return this.$root;
            },
            init: function () {
                this.total = parseInteger(this.$root.dataset.totalRows, 0);
                this.reseed();
                // The load-more control uses hx-swap="beforeend" into this grid's
                // <tbody> — it appends rows WITHOUT replacing the x-data <section>,
                // so init() does not re-fire. Without this listener reseed() would
                // never run after a load-more append: the select-all checkbox would
                // report a stale "all selected" (instead of indeterminate) and any
                // server-checked appended row would be silently dropped. The sort
                // control swaps outerHTML (re-inits the component), so it is already
                // covered by init() -> reseed(); we deliberately only re-scan when
                // the settled target is THIS grid's own body to stay idempotent and
                // not cross-talk with other grids on the page.
                var self = this;
                var bodyId = this.$root.id ? this.$root.id + "-body" : "";
                this._onAfterSettle = function (event) {
                    var target = event && event.detail ? event.detail.target : null;
                    if (!target || !bodyId) {
                        return;
                    }
                    // Re-scan when the body itself settled, or any element inside
                    // this grid's body did (htmx reports the swap target). Look the
                    // body up by id (no CSS.escape dependency; the id is a slug).
                    var body = document.getElementById(bodyId);
                    if (body && (target === body || body.contains(target) || target.contains(body))) {
                        self.reseed();
                    }
                };
                document.body.addEventListener("htmx:afterSettle", this._onAfterSettle);
            },
            destroy: function () {
                if (this._onAfterSettle) {
                    document.body.removeEventListener("htmx:afterSettle", this._onAfterSettle);
                    this._onAfterSettle = null;
                }
            },
            // Re-scan server-rendered checked row checkboxes and recompute
            // derived state. Called on init and after htmx swaps (load-more /
            // sort) re-render the body so newly appended rows participate and
            // stale checked state never leaks.
            reseed: function () {
                var checked = this.$root.querySelectorAll(
                    ".chirpui-table__select-row:checked"
                );
                var seeded = new Set(this.selected);
                Array.prototype.forEach.call(checked, function (box) {
                    if (box.value) {
                        seeded.add(box.value);
                    }
                });
                this.selected = seeded;
                this.recompute();
            },
            rowBoxes: function () {
                return this.$root.querySelectorAll(".chirpui-table__select-row");
            },
            recompute: function () {
                this.count = this.selected.size;
                var boxes = this.rowBoxes();
                var n = boxes.length;
                var sel = 0;
                for (var i = 0; i < n; i++) {
                    if (this.selected.has(boxes[i].value)) {
                        sel++;
                    }
                }
                this.allSelected = n > 0 && sel === n;
                this.someSelected = sel > 0 && sel < n;
            },
            toggle: function (id, checked) {
                if (checked) {
                    this.selected.add(String(id));
                } else {
                    this.selected.delete(String(id));
                }
                // Reassign so Alpine's reactivity observes the Set change.
                this.selected = new Set(this.selected);
                this.recompute();
            },
            toggleAll: function (event) {
                var check = event && event.target ? event.target.checked : !this.allSelected;
                var boxes = this.rowBoxes();
                var next = new Set(this.selected);
                Array.prototype.forEach.call(boxes, function (box) {
                    if (!box.value) {
                        return;
                    }
                    if (check) {
                        next.add(box.value);
                    } else {
                        next.delete(box.value);
                    }
                });
                this.selected = next;
                this.recompute();
            },
            clear: function () {
                this.selected = new Set();
                this.recompute();
            },
        };
    });

    scheduleAlpineHealthCheck();
})();
