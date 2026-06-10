/**
 * Smoke tests for the Bengal chirp-theme core theme manager (#152).
 *
 * core/theme.js is a plain IIFE that exposes window.BengalTheme = {get,set,toggle},
 * persists the preference under the `bengal-theme` localStorage key, mirrors the
 * resolved theme onto <html data-theme>, and dispatches a `themechange` event.
 * These tests build the minimal DOM in jsdom, evaluate the IIFE with the jsdom
 * globals in scope (it is not an ES module), and assert the public contract so a
 * regression in init / set / toggle / system-watch can't land silently.
 *
 * Mirrors:
 *   src/bengal_themes/chirp_theme/assets/js/core/theme.js
 */
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { mockLocalStorage } from "./helpers.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const THEME_JS_PATH = path.resolve(
  __dirname,
  "../../src/bengal_themes/chirp_theme/assets/js/core/theme.js"
);
const THEME_SRC = readFileSync(THEME_JS_PATH, "utf8");

const THEME_KEY = "bengal-theme";

/** Execute theme.js in the current jsdom global scope. */
function loadThemeScript() {
  // theme.js attaches window.BengalTheme; evaluate it as a script with the
  // jsdom globals injected so its closure resolves them.
  // eslint-disable-next-line no-new-func
  new Function(
    "window",
    "document",
    "localStorage",
    `${THEME_SRC}\n//# sourceURL=theme.js`
  )(window, document, window.localStorage);
}

/** Force a matchMedia result for the prefers-color-scheme query. */
function mockMatchMedia(dark) {
  const listeners = new Set();
  window.matchMedia = vi.fn().mockImplementation((query) => ({
    matches: dark && query.includes("prefers-color-scheme: dark"),
    media: query,
    addEventListener: (_evt, cb) => listeners.add(cb),
    removeEventListener: (_evt, cb) => listeners.delete(cb),
    addListener: (cb) => listeners.add(cb),
    removeListener: (cb) => listeners.delete(cb),
    dispatchEvent: () => true,
  }));
  return listeners;
}

let storage;

beforeEach(() => {
  // jsdom's default localStorage lacks .clear(); use a Map-backed mock.
  storage = mockLocalStorage();
  mockMatchMedia(false);
  // Start each test from a known document state (theme.js auto-inits on load).
  document.documentElement.removeAttribute("data-theme");
  document.body.innerHTML = "";
});

afterEach(() => {
  delete window.BengalTheme;
  storage.teardown();
  document.documentElement.removeAttribute("data-theme");
  document.body.innerHTML = "";
  vi.restoreAllMocks();
});

describe("theme.js public API", () => {
  it("exposes BengalTheme.get/set/toggle after the IIFE runs", () => {
    loadThemeScript();
    expect(window.BengalTheme).toBeDefined();
    expect(typeof window.BengalTheme.get).toBe("function");
    expect(typeof window.BengalTheme.set).toBe("function");
    expect(typeof window.BengalTheme.toggle).toBe("function");
  });

  it("auto-init resolves a stored 'dark' preference onto <html data-theme>", () => {
    window.localStorage.setItem(THEME_KEY, "dark");
    loadThemeScript();
    expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
  });

  it("falls back to system (light) when no preference is stored", () => {
    mockMatchMedia(false); // system = light
    loadThemeScript();
    // initTheme() writes the 'system' default and resolves it to light.
    expect(document.documentElement.getAttribute("data-theme")).toBe("light");
  });

  it("set('dark') persists the literal preference and resolves the attribute", () => {
    loadThemeScript();
    window.BengalTheme.set("dark");
    expect(window.localStorage.getItem(THEME_KEY)).toBe("dark");
    expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
  });

  it("set fires a 'themechange' event carrying the resolved theme", () => {
    loadThemeScript();
    const handler = vi.fn();
    window.addEventListener("themechange", handler);
    window.BengalTheme.set("dark");
    expect(handler).toHaveBeenCalled();
    const evt = handler.mock.calls.at(-1)[0];
    expect(evt.detail.theme).toBe("dark");
    window.removeEventListener("themechange", handler);
  });

  it("toggle flips light -> dark -> light", () => {
    loadThemeScript();
    window.BengalTheme.set("light");
    window.BengalTheme.toggle();
    expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
    window.BengalTheme.toggle();
    expect(document.documentElement.getAttribute("data-theme")).toBe("light");
  });

  it("clears the legacy bengal-palette key/attribute on init", () => {
    window.localStorage.setItem("bengal-palette", "violet");
    document.documentElement.setAttribute("data-palette", "violet");
    loadThemeScript();
    expect(window.localStorage.getItem("bengal-palette")).toBeNull();
    expect(document.documentElement.hasAttribute("data-palette")).toBe(false);
  });

  it("wires a click handler onto a .theme-toggle button", () => {
    document.body.innerHTML = `<button class="theme-toggle"></button>`;
    window.localStorage.setItem(THEME_KEY, "light");
    loadThemeScript();
    document.querySelector(".theme-toggle").click();
    expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
  });
});
