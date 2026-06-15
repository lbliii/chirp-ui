/**
 * Unit coverage for the chirpuiGridSelection Alpine factory (issue #200).
 *
 * chirpui-alpine.js is a global IIFE, not an ES module: we eval its source in
 * the jsdom global with a mock window.Alpine that captures registered factories,
 * then instantiate chirpuiGridSelection() against a built grid DOM and drive its
 * state API the way the data_grid template's x-bindings do.
 *
 * The most-violated selection rule is asserted explicitly: `indeterminate` is a
 * derived boolean (`someSelected`) that the template binds via Alpine's
 * `:indeterminate` DOM-property binding — never an HTML attribute. This factory
 * never touches the attribute; the test proves the derived flag is correct so
 * the binding has the right value to apply.
 */
import fs from "node:fs";
import path from "node:path";
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";

const SRC = fs.readFileSync(
  path.resolve(process.cwd(), "src/chirp_ui/templates/chirpui-alpine.js"),
  "utf8",
);

let factories;

function loadRuntime() {
  delete window.__chirpuiAlpineRuntimeLoaded;
  factories = {};
  // Mock Alpine so register() captures factory functions by name.
  window.Alpine = {
    version: "3.0.0",
    data(name, factory) {
      factories[name] = factory;
    },
    store() {},
  };
  (0, eval)(SRC);
}

/**
 * Build a grid root with `n` rows; `selectedValues` seeds server-checked rows.
 * Mirrors the data_grid template: a root carrying data-total-rows, one
 * select-all checkbox, and `n` .chirpui-table__select-row checkboxes.
 */
function buildGrid(n, selectedValues = [], id = "members-grid") {
  const root = document.createElement("section");
  root.id = id;
  root.dataset.totalRows = String(n);
  const allBox = document.createElement("input");
  allBox.type = "checkbox";
  allBox.className = "chirpui-table__select-all";
  root.appendChild(allBox);
  // The body is the hx-swap="beforeend" target for load-more; the factory's
  // afterSettle listener keys off `#{root.id}-body`.
  const body = document.createElement("tbody");
  body.id = `${id}-body`;
  root.appendChild(body);
  for (let i = 1; i <= n; i++) {
    const box = document.createElement("input");
    box.type = "checkbox";
    box.className = "chirpui-table__select-row";
    box.value = String(i);
    if (selectedValues.includes(String(i))) {
      box.checked = true;
    }
    body.appendChild(box);
  }
  document.body.appendChild(root);
  return root;
}

/** Append `values` as new (unchecked unless in `checked`) row boxes to the
 * grid body and fire the htmx:afterSettle the factory listens for — the way a
 * real load-more `beforeend` swap drives reseed() in the browser. */
function loadMoreAppend(root, values, checked = []) {
  const body = root.querySelector("tbody");
  for (const value of values) {
    const box = document.createElement("input");
    box.type = "checkbox";
    box.className = "chirpui-table__select-row";
    box.value = String(value);
    if (checked.includes(String(value))) {
      box.checked = true;
    }
    body.appendChild(box);
  }
  document.body.dispatchEvent(
    new CustomEvent("htmx:afterSettle", { detail: { target: body } }),
  );
}

/** States created during a test, destroyed in afterEach so the document.body
 * afterSettle listener each init() adds does not bleed across tests. */
let liveStates = [];

/** Instantiate the factory bound to `root` as Alpine's `this.$root`. */
function makeState(root) {
  const state = factories.chirpuiGridSelection();
  // The factory queries through `this.$root` (the stable component root); Alpine
  // provides it as a magic at runtime, so we set it directly for the unit test.
  state.$root = root;
  liveStates.push(state);
  return state;
}

describe("chirpuiGridSelection (#200)", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
    liveStates = [];
    delete window.Alpine;
    vi.spyOn(console, "warn").mockImplementation(() => {});
    loadRuntime();
  });

  afterEach(() => {
    // Tear down each component so its document.body afterSettle listener is
    // removed and cannot fire against the next test's DOM.
    for (const state of liveStates) {
      if (typeof state.destroy === "function") {
        state.destroy();
      }
    }
    liveStates = [];
    delete window.Alpine;
    delete window.__chirpuiAlpineRuntimeLoaded;
    vi.restoreAllMocks();
  });

  it("registers the factory", () => {
    expect(typeof factories.chirpuiGridSelection).toBe("function");
  });

  it("seeds selection from server-rendered checked rows on init", () => {
    const root = buildGrid(3, ["1", "3"]);
    const state = makeState(root);
    state.init();
    expect(state.count).toBe(2);
    expect(state.selected.has("1")).toBe(true);
    expect(state.selected.has("3")).toBe(true);
    expect(state.allSelected).toBe(false);
    expect(state.someSelected).toBe(true); // partial -> indeterminate
  });

  it("toggle adds and removes a single id and recomputes derived flags", () => {
    const root = buildGrid(2);
    const state = makeState(root);
    state.init();
    expect(state.count).toBe(0);
    expect(state.someSelected).toBe(false);

    state.toggle("1", true);
    expect(state.count).toBe(1);
    expect(state.someSelected).toBe(true);
    expect(state.allSelected).toBe(false);

    state.toggle("2", true);
    expect(state.allSelected).toBe(true);
    expect(state.someSelected).toBe(false);

    state.toggle("1", false);
    expect(state.allSelected).toBe(false);
    expect(state.someSelected).toBe(true);
  });

  it("toggleAll selects every visible row, then clears them", () => {
    const root = buildGrid(3);
    const state = makeState(root);
    state.init();

    state.toggleAll({ target: { checked: true } });
    expect(state.count).toBe(3);
    expect(state.allSelected).toBe(true);
    expect(state.someSelected).toBe(false);

    state.toggleAll({ target: { checked: false } });
    expect(state.count).toBe(0);
    expect(state.allSelected).toBe(false);
    expect(state.someSelected).toBe(false);
  });

  it("clear() empties the selection", () => {
    const root = buildGrid(2, ["1", "2"]);
    const state = makeState(root);
    state.init();
    expect(state.allSelected).toBe(true);
    state.clear();
    expect(state.count).toBe(0);
    expect(state.allSelected).toBe(false);
  });

  it("re-seeds via the htmx:afterSettle hook when a load-more swap appends rows", () => {
    // Exercises the WIRING, not just the helper: init() registers a
    // document.body afterSettle listener; a load-more beforeend append +
    // afterSettle event must drive reseed() with no manual call.
    const root = buildGrid(2, ["1"]);
    const state = makeState(root);
    state.init();
    expect(state.count).toBe(1);
    expect(state.allSelected).toBe(false);

    loadMoreAppend(root, ["3", "4"]); // fires htmx:afterSettle on the body
    // Pre-existing selection of "1" is preserved; new rows default unselected.
    expect(state.selected.has("1")).toBe(true);
    expect(state.count).toBe(1);
    expect(state.allSelected).toBe(false);
    expect(state.someSelected).toBe(true);
  });

  it("select-all then load-more recomputes select-all to indeterminate", () => {
    // The regression for the WCAG 4.1.2 finding: select-all (all visible) then
    // load-more must flip the select-all from checked -> indeterminate because
    // only the original page is selected of the now-larger row set.
    const root = buildGrid(3);
    const state = makeState(root);
    state.init();
    state.toggleAll({ target: { checked: true } });
    expect(state.allSelected).toBe(true);
    expect(state.someSelected).toBe(false);

    loadMoreAppend(root, ["4", "5", "6"]); // 3 of 6 now selected
    expect(state.allSelected).toBe(false);
    expect(state.someSelected).toBe(true);
    expect(state.count).toBe(3);
  });

  it("re-adopts a server-checked appended row after load-more", () => {
    // The legitimate cross-request ?ids= scenario: the server renders an
    // appended row with a static `checked` attribute; reseed() must adopt it
    // into `selected` so the :checked binding does not strip it.
    const root = buildGrid(2, ["1"]);
    const state = makeState(root);
    state.init();
    expect(state.count).toBe(1);

    loadMoreAppend(root, ["3", "4"], ["4"]); // server pre-checks "4"
    expect(state.selected.has("1")).toBe(true);
    expect(state.selected.has("4")).toBe(true);
    expect(state.count).toBe(2);
  });

  it("two grids on a page do not cross-talk (scoped to this.$root)", () => {
    const a = buildGrid(2, ["1"], "grid-a");
    const b = buildGrid(2, [], "grid-b");
    const stateA = makeState(a);
    const stateB = makeState(b);
    stateA.init();
    stateB.init();
    stateA.toggleAll({ target: { checked: true } });
    expect(stateA.count).toBe(2);
    // Grid B is untouched.
    expect(stateB.count).toBe(0);

    // A load-more on grid A must not reseed grid B.
    loadMoreAppend(a, ["3"]);
    expect(stateB.count).toBe(0);
  });
});
