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
            if (!window.Alpine.store("modals")) {
                window.Alpine.store("modals", {});
            }
            if (!window.Alpine.store("trays")) {
                window.Alpine.store("trays", {});
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
                    value: this.selected,
                });
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
})();
