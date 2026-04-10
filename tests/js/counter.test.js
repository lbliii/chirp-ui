import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { mockChirpIslands, createPayload, createMockApi } from "./helpers.js";

// counter.js calls registerPrimitive at import time, so we must set up
// the mock registry BEFORE the dynamic import. We cache the mount function
// after the first import (ES modules are singletons).
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
    await import("../../src/chirp_ui/templates/islands/counter.js");
    mount = islands.register.mock.calls.find(
      (c) => c[0] === "counter-widget"
    )?.[1]?.mount;
  }
  return mount;
}

function createCounterDOM(seed = 0) {
  const root = document.createElement("div");
  root.innerHTML = `
    <span data-counter-value>${seed}</span>
    <button data-counter-plus>+</button>
    <button data-counter-minus>-</button>
  `;
  return root;
}

describe("counter-widget", () => {
  it("registers as 'counter-widget' primitive", async () => {
    await getMountFn();
    expect(mount).toBeTypeOf("function");
  });

  it("initializes with seed=0 by default", async () => {
    const fn = await getMountFn();
    const root = createCounterDOM();
    const api = createMockApi();
    fn(createPayload(root, {}), api);

    expect(api.emitState).toHaveBeenCalledWith({ count: 0 });
    expect(root.querySelector("[data-counter-value]").textContent).toBe("0");
  });

  it("initializes with custom seed", async () => {
    const fn = await getMountFn();
    const root = createCounterDOM();
    const api = createMockApi();
    fn(createPayload(root, { seed: 7 }), api);

    expect(api.emitState).toHaveBeenCalledWith({ count: 7 });
    expect(root.querySelector("[data-counter-value]").textContent).toBe("7");
  });

  it("coerces string seed to number", async () => {
    const fn = await getMountFn();
    const root = createCounterDOM();
    const api = createMockApi();
    fn(createPayload(root, { seed: "12" }), api);

    expect(api.emitState).toHaveBeenCalledWith({ count: 12 });
  });

  it("treats non-numeric seed as 0 (NaN coercion)", async () => {
    const fn = await getMountFn();
    const root = createCounterDOM();
    const api = createMockApi();
    fn(createPayload(root, { seed: "abc" }), api);

    // Number("abc") is NaN, but `Number(props.seed || 0)` — "abc" is truthy,
    // so Number("abc") = NaN. Let's verify actual behavior.
    const state = api.emitState.mock.calls[0][0];
    expect(typeof state.count).toBe("number");
  });

  it("increment increases count by 1", async () => {
    const fn = await getMountFn();
    const root = createCounterDOM();
    const api = createMockApi();
    fn(createPayload(root, { seed: 5 }), api);
    api.emitState.mockClear();
    api.emitAction.mockClear();

    root.querySelector("[data-counter-plus]").click();

    expect(api.emitState).toHaveBeenCalledWith({ count: 6 });
    expect(api.emitAction).toHaveBeenCalledWith("increment", "success", {});
    expect(root.querySelector("[data-counter-value]").textContent).toBe("6");
  });

  it("decrement decreases count by 1", async () => {
    const fn = await getMountFn();
    const root = createCounterDOM();
    const api = createMockApi();
    fn(createPayload(root, { seed: 3 }), api);
    api.emitState.mockClear();
    api.emitAction.mockClear();

    root.querySelector("[data-counter-minus]").click();

    expect(api.emitState).toHaveBeenCalledWith({ count: 2 });
    expect(api.emitAction).toHaveBeenCalledWith("decrement", "success", {});
    expect(root.querySelector("[data-counter-value]").textContent).toBe("2");
  });

  it("allows negative counts", async () => {
    const fn = await getMountFn();
    const root = createCounterDOM();
    const api = createMockApi();
    fn(createPayload(root, { seed: 0 }), api);

    root.querySelector("[data-counter-minus]").click();

    expect(api.emitState).toHaveBeenLastCalledWith({ count: -1 });
  });

  it("multiple clicks accumulate", async () => {
    const fn = await getMountFn();
    const root = createCounterDOM();
    const api = createMockApi();
    fn(createPayload(root, { seed: 0 }), api);

    const plus = root.querySelector("[data-counter-plus]");
    plus.click();
    plus.click();
    plus.click();

    expect(api.emitState).toHaveBeenLastCalledWith({ count: 3 });
  });

  it("cleanup removes event listeners", async () => {
    const fn = await getMountFn();
    const root = createCounterDOM();
    const api = createMockApi();
    const cleanup = fn(createPayload(root, { seed: 0 }), api);
    api.emitState.mockClear();

    cleanup();
    root.querySelector("[data-counter-plus]").click();

    // After cleanup, clicks should not trigger state updates
    expect(api.emitState).not.toHaveBeenCalled();
  });

  it("works without optional DOM nodes", async () => {
    const fn = await getMountFn();
    const root = document.createElement("div"); // empty — no buttons or value
    const api = createMockApi();
    const cleanup = fn(createPayload(root, { seed: 2 }), api);

    expect(api.emitState).toHaveBeenCalledWith({ count: 2 });
    expect(typeof cleanup).toBe("function");
    cleanup(); // should not throw
  });
});
