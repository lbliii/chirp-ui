/**
 * Smoke tests for the Bengal chirp-theme enhanced TOC (#152).
 *
 * enhancements/toc.js is a plain IIFE that hard-requires window.BengalUtils
 * (throttleScroll / debounce / ready) — it console.errors and bails if absent.
 * It scroll-spies `[data-toc-item]` links against their heading targets, drives
 * native <details class="toc-group"> open/close, persists `toc-state` in
 * localStorage, and exposes window.BengalTOC = {init,cleanup,updateActiveItem,
 * expandAll,collapseAll}. These tests stub BengalUtils, build the TOC + heading
 * DOM the theme templates emit, evaluate the IIFE with jsdom globals in scope,
 * and assert the init / expand / collapse / cleanup contract.
 *
 * Mirrors:
 *   src/bengal_themes/chirp_theme/assets/js/enhancements/toc.js
 */
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { mockLocalStorage } from "./helpers.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TOC_JS_PATH = path.resolve(
  __dirname,
  "../../src/bengal_themes/chirp_theme/assets/js/enhancements/toc.js"
);
const TOC_SRC = readFileSync(TOC_JS_PATH, "utf8");

/**
 * Build a sidebar with two grouped TOC links + matching heading anchors.
 * Mirrors the toc-sidebar / toc-group / data-toc-item hooks.
 */
function renderTocPage() {
  document.body.innerHTML = `
    <aside class="toc-sidebar">
      <nav class="toc-nav">
        <div class="toc-scroll-container">
          <details class="toc-group" open>
            <summary>Group A</summary>
            <a class="toc-link" data-toc-item="#sec-a" href="#sec-a">Section A</a>
          </details>
          <details class="toc-group" open>
            <summary>Group B</summary>
            <a class="toc-link" data-toc-item="#sec-b" href="#sec-b">Section B</a>
          </details>
        </div>
      </nav>
    </aside>
    <main>
      <h2 id="sec-a">Section A</h2>
      <p>body a</p>
      <h2 id="sec-b">Section B</h2>
      <p>body b</p>
    </main>`;
}

/** Execute toc.js in the current jsdom global scope. */
function loadTocScript() {
  // toc.js attaches window.BengalTOC; evaluate it as a script with the jsdom
  // globals injected (console included so its BengalUtils guard can warn).
  // eslint-disable-next-line no-new-func
  new Function(
    "window",
    "document",
    "localStorage",
    "console",
    "history",
    `${TOC_SRC}\n//# sourceURL=toc.js`
  )(window, document, window.localStorage, console, window.history);
}

/** Minimal stand-in for window.BengalUtils (real one lives in utils.js). */
function installBengalUtils() {
  window.BengalUtils = {
    // Run the scroll callback as-is and ready() synchronously for determinism.
    throttleScroll: (cb) => cb,
    debounce: (cb) => cb,
    ready: (cb) => cb(),
  };
}

let storage;

beforeEach(() => {
  storage = mockLocalStorage();
  // jsdom does not implement these scroll APIs — stub them.
  window.scrollTo = vi.fn();
  window.HTMLElement.prototype.scrollIntoView = vi.fn();
  installBengalUtils();
  renderTocPage();
});

afterEach(() => {
  if (window.BengalTOC) {
    window.BengalTOC.cleanup();
    delete window.BengalTOC;
  }
  delete window.BengalUtils;
  storage.teardown();
  document.body.innerHTML = "";
  vi.restoreAllMocks();
});

describe("toc.js public API", () => {
  it("exposes BengalTOC.{init,cleanup,updateActiveItem,expandAll,collapseAll}", () => {
    loadTocScript();
    expect(window.BengalTOC).toBeDefined();
    expect(typeof window.BengalTOC.init).toBe("function");
    expect(typeof window.BengalTOC.cleanup).toBe("function");
    expect(typeof window.BengalTOC.updateActiveItem).toBe("function");
    expect(typeof window.BengalTOC.expandAll).toBe("function");
    expect(typeof window.BengalTOC.collapseAll).toBe("function");
  });

  it("bails out (console.error, no BengalTOC) when BengalUtils is missing", () => {
    delete window.BengalUtils;
    const errSpy = vi.spyOn(console, "error").mockImplementation(() => {});
    loadTocScript();
    expect(errSpy).toHaveBeenCalled();
    expect(window.BengalTOC).toBeUndefined();
  });

  it("auto-init (via ready) marks an active link without throwing", () => {
    loadTocScript();
    // ready() ran initTOC synchronously; the initial updateOnScroll marks
    // exactly one link active. In jsdom every getBoundingClientRect().top is 0,
    // so updateActiveItem picks the last heading at/above the offset — which one
    // depends on layout, so the regression we guard is "no link became active".
    const active = Array.from(document.querySelectorAll(".toc-link.active"));
    expect(active).toHaveLength(1);
    expect(["#sec-a", "#sec-b"]).toContain(
      active[0].getAttribute("data-toc-item")
    );
  });

  it("collapseAll() closes every toc-group, expandAll() re-opens them", () => {
    loadTocScript();
    window.BengalTOC.collapseAll();
    const groups = Array.from(document.querySelectorAll("details.toc-group"));
    expect(groups.every((g) => !g.open)).toBe(true);

    window.BengalTOC.expandAll();
    expect(groups.every((g) => g.open)).toBe(true);
  });

  it("persists compact mode + collapsed groups to the toc-state key", () => {
    loadTocScript();
    window.BengalTOC.collapseAll();
    const saved = JSON.parse(window.localStorage.getItem("toc-state"));
    expect(saved).toMatchObject({ compact: false });
    expect(Array.isArray(saved.collapsed)).toBe(true);
    // Each closed group records its data-toc-item id.
    expect(saved.collapsed).toContain("#sec-a");
  });

  it("cleanup() detaches without throwing (idempotent)", () => {
    loadTocScript();
    expect(() => window.BengalTOC.cleanup()).not.toThrow();
    expect(() => window.BengalTOC.cleanup()).not.toThrow();
  });

  it("clicking a TOC link smooth-scrolls and updates the hash", () => {
    loadTocScript();
    const link = document.querySelector('[data-toc-item="#sec-b"]');
    link.click();
    expect(window.scrollTo).toHaveBeenCalled();
    expect(window.location.hash).toBe("#sec-b");
  });
});
