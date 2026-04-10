import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { mockChirpIslands, createPayload, createMockApi } from "./helpers.js";

let mount;
let islands;

beforeEach(() => {
  islands = mockChirpIslands();
});

afterEach(() => {
  islands.teardown();
});

async function getMountFn() {
  if (!mount) {
    await import("../../src/chirp_ui/templates/islands/grid_state.js");
    mount = islands.register.mock.calls.find(
      (c) => c[0] === "grid_state"
    )?.[1]?.mount;
  }
  return mount;
}

function createGridDOM() {
  const root = document.createElement("div");
  root.innerHTML = `
    <input data-grid-filter value="" />
    <button data-grid-sort>Sort</button>
    <div data-grid-body>
      <div data-grid-row data-grid-id="r1">
        <input type="checkbox" data-grid-select />
        Alpha item
      </div>
      <div data-grid-row data-grid-id="r2">
        <input type="checkbox" data-grid-select />
        Beta item
      </div>
      <div data-grid-row data-grid-id="r3">
        <input type="checkbox" data-grid-select />
        Charlie item
      </div>
    </div>
  `;
  return root;
}

describe("grid_state", () => {
  it("registers as 'grid_state' primitive", async () => {
    const fn = await getMountFn();
    expect(fn).toBeTypeOf("function");
  });

  it("initializes with all rows visible and empty filter", async () => {
    const fn = await getMountFn();
    const root = createGridDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    const rows = root.querySelectorAll("[data-grid-row]");
    rows.forEach((row) => {
      expect(row.hidden).toBe(false);
    });
    expect(api.emitState).toHaveBeenCalledWith(
      expect.objectContaining({
        filter: "",
        selected: [],
        sort: "asc",
      })
    );
  });

  it("filter hides non-matching rows", async () => {
    const fn = await getMountFn();
    const root = createGridDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    const filterInput = root.querySelector("[data-grid-filter]");
    filterInput.value = "alpha";
    filterInput.dispatchEvent(new Event("input"));

    const rows = root.querySelectorAll("[data-grid-row]");
    expect(rows[0].hidden).toBe(false); // "Alpha item" matches
    expect(rows[1].hidden).toBe(true); // "Beta item" doesn't
    expect(rows[2].hidden).toBe(true); // "Charlie item" doesn't
  });

  it("filter is case-insensitive", async () => {
    const fn = await getMountFn();
    const root = createGridDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    const filterInput = root.querySelector("[data-grid-filter]");
    filterInput.value = "BETA";
    filterInput.dispatchEvent(new Event("input"));

    const rows = root.querySelectorAll("[data-grid-row]");
    expect(rows[0].hidden).toBe(true);
    expect(rows[1].hidden).toBe(false);
  });

  it("filter trims whitespace", async () => {
    const fn = await getMountFn();
    const root = createGridDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    const filterInput = root.querySelector("[data-grid-filter]");
    filterInput.value = "  charlie  ";
    filterInput.dispatchEvent(new Event("input"));

    const rows = root.querySelectorAll("[data-grid-row]");
    expect(rows[2].hidden).toBe(false);
  });

  it("empty filter shows all rows", async () => {
    const fn = await getMountFn();
    const root = createGridDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    const filterInput = root.querySelector("[data-grid-filter]");
    filterInput.value = "alpha";
    filterInput.dispatchEvent(new Event("input"));

    // Now clear
    filterInput.value = "";
    filterInput.dispatchEvent(new Event("input"));

    const rows = root.querySelectorAll("[data-grid-row]");
    rows.forEach((row) => {
      expect(row.hidden).toBe(false);
    });
  });

  it("sort toggles between asc and desc", async () => {
    const fn = await getMountFn();
    const root = createGridDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);
    api.emitState.mockClear();
    api.emitAction.mockClear();

    // First click → asc becomes false (desc)
    root.querySelector("[data-grid-sort]").click();

    expect(api.emitAction).toHaveBeenCalledWith("sort", "success", {
      direction: "desc",
    });
    expect(api.emitState).toHaveBeenCalledWith(
      expect.objectContaining({ sort: "desc" })
    );

    api.emitAction.mockClear();

    // Second click → back to asc
    root.querySelector("[data-grid-sort]").click();

    expect(api.emitAction).toHaveBeenCalledWith("sort", "success", {
      direction: "asc",
    });
  });

  it("sort reorders DOM rows", async () => {
    const fn = await getMountFn();
    const root = createGridDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    // Initial order: Alpha, Beta, Charlie (asc=true)
    // Click sort → asc becomes false → desc order: Charlie, Beta, Alpha
    root.querySelector("[data-grid-sort]").click();

    const body = root.querySelector("[data-grid-body]");
    const ids = Array.from(body.querySelectorAll("[data-grid-row]")).map(
      (r) => r.getAttribute("data-grid-id")
    );
    expect(ids).toEqual(["r3", "r2", "r1"]);
  });

  it("checkbox select adds to selected set", async () => {
    const fn = await getMountFn();
    const root = createGridDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);
    api.emitAction.mockClear();

    const checkbox = root.querySelector(
      "[data-grid-id=r2] [data-grid-select]"
    );
    checkbox.checked = true;
    checkbox.dispatchEvent(new Event("change"));

    expect(api.emitAction).toHaveBeenCalledWith("select", "success", {
      count: 1,
    });
    expect(api.emitState).toHaveBeenLastCalledWith(
      expect.objectContaining({ selected: ["r2"] })
    );
  });

  it("checkbox uncheck removes from selected set", async () => {
    const fn = await getMountFn();
    const root = createGridDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    const checkbox = root.querySelector(
      "[data-grid-id=r1] [data-grid-select]"
    );
    checkbox.checked = true;
    checkbox.dispatchEvent(new Event("change"));

    checkbox.checked = false;
    checkbox.dispatchEvent(new Event("change"));

    expect(api.emitState).toHaveBeenLastCalledWith(
      expect.objectContaining({ selected: [] })
    );
  });

  it("render syncs checkbox checked state with selection set", async () => {
    const fn = await getMountFn();
    const root = createGridDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    // Select r1
    const cb1 = root.querySelector("[data-grid-id=r1] [data-grid-select]");
    cb1.checked = true;
    cb1.dispatchEvent(new Event("change"));

    // After render, r1 should be checked, others not
    const cb2 = root.querySelector("[data-grid-id=r2] [data-grid-select]");
    const cb3 = root.querySelector("[data-grid-id=r3] [data-grid-select]");
    expect(cb1.checked).toBe(true);
    expect(cb2.checked).toBe(false);
    expect(cb3.checked).toBe(false);
  });

  it("custom stateKey is reflected in state", async () => {
    const fn = await getMountFn();
    const root = createGridDOM();
    const api = createMockApi();

    fn(createPayload(root, { stateKey: "users" }), api);

    expect(api.emitState).toHaveBeenCalledWith(
      expect.objectContaining({ stateKey: "users" })
    );
  });

  it("cleanup removes all listeners", async () => {
    const fn = await getMountFn();
    const root = createGridDOM();
    const api = createMockApi();

    const cleanup = fn(createPayload(root, {}), api);
    api.emitState.mockClear();
    api.emitAction.mockClear();

    cleanup();

    // Filter, sort, checkbox should all be inert
    root.querySelector("[data-grid-filter]").value = "test";
    root.querySelector("[data-grid-filter]").dispatchEvent(new Event("input"));
    root.querySelector("[data-grid-sort]").click();
    const cb = root.querySelector("[data-grid-id=r1] [data-grid-select]");
    cb.checked = true;
    cb.dispatchEvent(new Event("change"));

    expect(api.emitState).not.toHaveBeenCalled();
    expect(api.emitAction).not.toHaveBeenCalled();
  });
});
