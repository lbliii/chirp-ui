/**
 * Smoke tests for the Bengal chirp-theme tabs enhancement (#152).
 *
 * enhancements/tabs.js is a plain IIFE layered over a CSS :target state machine.
 * It exposes window.BengalTabs = {sync,switch,restoreSync}, toggles the `active`
 * class on nav items + panes, persists sync preferences under
 * `bengal-tabs-sync-<key>` in localStorage, and dispatches a `tabSwitched` event.
 * These tests build the `.tabs > .tab-nav` / `.tab-pane` DOM the theme templates
 * emit, evaluate the IIFE with jsdom globals in scope, and assert the switch /
 * sync / restore contract.
 *
 * Mirrors:
 *   src/bengal_themes/chirp_theme/assets/js/enhancements/tabs.js
 */
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { mockLocalStorage } from "./helpers.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TABS_JS_PATH = path.resolve(
  __dirname,
  "../../src/bengal_themes/chirp_theme/assets/js/enhancements/tabs.js"
);
const TABS_SRC = readFileSync(TABS_JS_PATH, "utf8");

const STORAGE_PREFIX = "bengal-tabs-sync-";

/**
 * Build a tab set with two panes. `syncKey` (optional) wires the
 * data-sync / data-sync-value cross-container sync hooks.
 */
function renderTabSet(id, syncKey) {
  const syncAttr = syncKey ? ` data-sync="${syncKey}"` : "";
  document.body.insertAdjacentHTML(
    "beforeend",
    `
    <div class="tabs"${syncAttr} id="${id}">
      <ul class="tab-nav">
        <li>
          <a href="#${id}-py"
             data-tab-target="${id}-py"
             ${syncKey ? 'data-sync-value="python"' : ""}>Python</a>
        </li>
        <li>
          <a href="#${id}-rs"
             data-tab-target="${id}-rs"
             ${syncKey ? 'data-sync-value="rust"' : ""}>Rust</a>
        </li>
      </ul>
      <div class="tab-pane" id="${id}-py">py body</div>
      <div class="tab-pane" id="${id}-rs">rs body</div>
    </div>`
  );
  return document.getElementById(id);
}

/** Execute tabs.js in the current jsdom global scope. */
function loadTabsScript() {
  // tabs.js attaches document-level delegated listeners and window.BengalTabs;
  // evaluate it as a script with the jsdom globals injected.
  // eslint-disable-next-line no-new-func
  new Function(
    "window",
    "document",
    "localStorage",
    "navigator",
    `${TABS_SRC}\n//# sourceURL=tabs.js`
  )(window, document, window.localStorage, window.navigator);
}

let storage;

beforeEach(() => {
  storage = mockLocalStorage();
  document.body.innerHTML = "";
});

afterEach(() => {
  delete window.BengalTabs;
  storage.teardown();
  document.body.innerHTML = "";
  vi.restoreAllMocks();
});

describe("tabs.js public API", () => {
  it("exposes BengalTabs.sync/switch/restoreSync after the IIFE runs", () => {
    loadTabsScript();
    expect(window.BengalTabs).toBeDefined();
    expect(typeof window.BengalTabs.sync).toBe("function");
    expect(typeof window.BengalTabs.switch).toBe("function");
    expect(typeof window.BengalTabs.restoreSync).toBe("function");
  });

  it("init activates the first tab when no pane is marked active", () => {
    const container = renderTabSet("t1");
    loadTabsScript();
    const firstItem = container.querySelector(".tab-nav li");
    expect(firstItem.classList.contains("active")).toBe(true);
    expect(document.getElementById("t1-py").classList.contains("active")).toBe(
      true
    );
    expect(document.getElementById("t1-py").dataset.printLabel).toBe("Python");
    expect(document.getElementById("t1-rs").dataset.printLabel).toBe("Rust");
  });

  it("switch() moves the active class onto the target pane and nav item", () => {
    const container = renderTabSet("t2");
    loadTabsScript();
    const rustLink = container.querySelector('[data-tab-target="t2-rs"]');
    window.BengalTabs.switch(container, rustLink, "t2-rs");

    expect(document.getElementById("t2-rs").classList.contains("active")).toBe(
      true
    );
    expect(document.getElementById("t2-py").classList.contains("active")).toBe(
      false
    );
    expect(rustLink.closest("li").classList.contains("active")).toBe(true);
    expect(rustLink.getAttribute("aria-selected")).toBe("true");
  });

  it("switch() dispatches a tabSwitched event on the container", () => {
    const container = renderTabSet("t3");
    loadTabsScript();
    const handler = vi.fn();
    container.addEventListener("tabSwitched", handler);
    const rustLink = container.querySelector('[data-tab-target="t3-rs"]');
    window.BengalTabs.switch(container, rustLink, "t3-rs");
    expect(handler).toHaveBeenCalled();
    expect(handler.mock.calls.at(-1)[0].detail.pane.id).toBe("t3-rs");
  });

  it("sync() switches every container sharing a key and persists the value", () => {
    const a = renderTabSet("a", "lang");
    const b = renderTabSet("b", "lang");
    loadTabsScript();

    window.BengalTabs.sync("lang", "rust");

    expect(document.getElementById("a-rs").classList.contains("active")).toBe(
      true
    );
    expect(document.getElementById("b-rs").classList.contains("active")).toBe(
      true
    );
    expect(window.localStorage.getItem(`${STORAGE_PREFIX}lang`)).toBe("rust");
    void a;
    void b;
  });

  it("restoreSync() re-applies a saved preference on load", () => {
    window.localStorage.setItem(`${STORAGE_PREFIX}lang`, "rust");
    renderTabSet("c", "lang");
    loadTabsScript(); // init() calls restoreSyncPreferences()
    expect(document.getElementById("c-rs").classList.contains("active")).toBe(
      true
    );
  });
});
