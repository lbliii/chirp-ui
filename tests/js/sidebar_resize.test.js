import fs from "node:fs";
import path from "node:path";
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { mockLocalStorage } from "./helpers.js";

const SRC = fs.readFileSync(
  path.resolve(process.cwd(), "src/chirp_ui/templates/chirpui-alpine.js"),
  "utf8",
);

function loadRuntime() {
  delete window.__chirpuiAlpineRuntimeLoaded;
  (0, eval)(SRC);
}

function createSidebar(options = { collapsible: true, resizable: true }) {
  const factories = {};
  window.Alpine = {
    version: "3.14.0",
    data(name, factory) {
      factories[name] = factory;
    },
    safeData(name, factory) {
      factories[name] = factory;
    },
    store() {},
  };
  loadRuntime();
  document.body.innerHTML =
    '<div class="chirpui-app-shell chirpui-app-shell--sidebar-collapsible">' +
    '<div data-chirpui-sidebar-toggle></div></div>';
  const el = document.querySelector(".chirpui-app-shell");
  const component = factories.chirpuiSidebar(options);
  component.$el = el;
  component.init();
  return component;
}

describe("chirpuiSidebar continuous resize (#219)", () => {
  let storage;

  beforeEach(() => {
    storage = mockLocalStorage();
    document.documentElement.removeAttribute("data-chirpui-sidebar-collapsed");
    document.documentElement.style.removeProperty("--chirpui-sidebar-width");
  });

  afterEach(() => {
    storage.teardown();
    delete window.Alpine;
    delete window.__chirpuiAlpineRuntimeLoaded;
    document.body.innerHTML = "";
  });

  it("restores a persisted width on init", () => {
    storage.store.set("chirpui-sidebar-width", "288px");
    storage.store.set("chirpui-sidebar-collapsed", "false");

    const sidebar = createSidebar();

    expect(sidebar.widthPx).toBe(288);
    expect(sidebar.collapsed).toBe(false);
    expect(sidebar.$el.style.getPropertyValue("--chirpui-sidebar-width")).toBe("288px");
  });

  it("updates width continuously while dragging", () => {
    const sidebar = createSidebar();
    const handle = sidebar.$el.querySelector("[data-chirpui-sidebar-toggle]");

    sidebar.startDrag({ clientX: 200, preventDefault() {} });
    sidebar.onMove({ clientX: 240 });
    sidebar.onUp();

    expect(sidebar.widthPx).toBe(296);
    expect(storage.store.get("chirpui-sidebar-width")).toBe("296px");
    expect(handle.getAttribute("role")).toBe("separator");
    expect(handle.getAttribute("aria-valuenow")).toBe("296");
  });

  it("collapses when dragged below the snap threshold", () => {
    const sidebar = createSidebar();

    sidebar.startDrag({ clientX: 300, preventDefault() {} });
    sidebar.onMove({ clientX: 140 });
    sidebar.onUp();

    expect(sidebar.collapsed).toBe(true);
    expect(storage.store.get("chirpui-sidebar-collapsed")).toBe("true");
    expect(sidebar.$el.classList.contains("chirpui-app-shell--sidebar-collapsed")).toBe(true);
  });

  it("supports keyboard resize and double-click toggle", () => {
    const sidebar = createSidebar();

    sidebar.onKeydown({ key: "ArrowRight", shiftKey: false, preventDefault() {} });
    expect(sidebar.widthPx).toBe(264);

    sidebar.onDoubleClick({ preventDefault() {} });
    expect(sidebar.collapsed).toBe(true);

    sidebar.onDoubleClick({ preventDefault() {} });
    expect(sidebar.collapsed).toBe(false);
    expect(sidebar.widthPx).toBe(256);
  });
});
