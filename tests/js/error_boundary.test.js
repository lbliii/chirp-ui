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
    await import("../../src/chirp_ui/templates/islands/error_boundary.js");
    mount = islands.register.mock.calls.find(
      (c) => c[0] === "error_boundary"
    )?.[1]?.mount;
  }
  return mount;
}

function createBoundaryDOM() {
  const root = document.createElement("div");
  root.innerHTML = `
    <div data-error-body>Content here</div>
    <div data-error-fallback hidden>Something went wrong</div>
    <button data-error-reset>Retry</button>
  `;
  return root;
}

function dispatchError(detail = {}) {
  document.dispatchEvent(
    new CustomEvent("chirp:island:error", { detail })
  );
}

describe("error_boundary", () => {
  it("registers as 'error_boundary' primitive", async () => {
    const fn = await getMountFn();
    expect(fn).toBeTypeOf("function");
  });

  it("starts in healthy state with body visible", async () => {
    const fn = await getMountFn();
    const root = createBoundaryDOM();
    const api = createMockApi();

    fn(createPayload(root, {}, { id: "b1", name: "boundary" }), api);

    expect(root.querySelector("[data-error-body]").hasAttribute("hidden")).toBe(
      false
    );
    expect(
      root.querySelector("[data-error-fallback]").hasAttribute("hidden")
    ).toBe(true);
    expect(api.emitState).toHaveBeenCalledWith(
      expect.objectContaining({ state: "healthy" })
    );
  });

  it("shows fallback on matching error event (same id)", async () => {
    const fn = await getMountFn();
    const root = createBoundaryDOM();
    const api = createMockApi();

    fn(createPayload(root, {}, { id: "b1", name: "boundary" }), api);

    dispatchError({ id: "b1", name: "boundary", error: "primitive" });

    expect(root.querySelector("[data-error-body]").hasAttribute("hidden")).toBe(
      true
    );
    expect(
      root.querySelector("[data-error-fallback]").hasAttribute("hidden")
    ).toBe(false);
    expect(api.emitState).toHaveBeenLastCalledWith(
      expect.objectContaining({ state: "error" })
    );
  });

  it("ignores error event with different id", async () => {
    const fn = await getMountFn();
    const root = createBoundaryDOM();
    const api = createMockApi();

    fn(createPayload(root, {}, { id: "b1", name: "boundary" }), api);
    api.emitState.mockClear();

    dispatchError({ id: "other-id", name: "other" });

    // Body should still be visible — error was not for this boundary
    expect(root.querySelector("[data-error-body]").hasAttribute("hidden")).toBe(
      false
    );
    // No new state emission since we cleared
    expect(api.emitState).not.toHaveBeenCalled();
  });

  it("catches error with no id (broadcast error)", async () => {
    const fn = await getMountFn();
    const root = createBoundaryDOM();
    const api = createMockApi();

    fn(createPayload(root, {}, { id: "b1", name: "boundary" }), api);

    // Error with no targetId — should match (targetId is null, so the id check is skipped)
    dispatchError({ error: "primitive", reason: "crash" });

    expect(root.querySelector("[data-error-body]").hasAttribute("hidden")).toBe(
      true
    );
  });

  it("catches error with matching name and error field", async () => {
    const fn = await getMountFn();
    const root = createBoundaryDOM();
    const api = createMockApi();

    fn(createPayload(root, {}, { id: null, name: "my-boundary" }), api);

    // detail.name matches payload.name AND detail.error is truthy
    dispatchError({ name: "my-boundary", error: "primitive" });

    expect(root.querySelector("[data-error-body]").hasAttribute("hidden")).toBe(
      true
    );
  });

  it("ignores error with different name and no error field", async () => {
    const fn = await getMountFn();
    const root = createBoundaryDOM();
    const api = createMockApi();

    fn(createPayload(root, {}, { id: null, name: "my-boundary" }), api);

    // Different name + no detail.error → second guard triggers return
    dispatchError({ name: "other-name" });

    expect(root.querySelector("[data-error-body]").hasAttribute("hidden")).toBe(
      false
    );
  });

  it("reset button restores healthy state", async () => {
    const fn = await getMountFn();
    const root = createBoundaryDOM();
    const api = createMockApi();

    fn(createPayload(root, {}, { id: "b1", name: "boundary" }), api);

    // Trigger error
    dispatchError({ id: "b1" });
    expect(root.querySelector("[data-error-body]").hasAttribute("hidden")).toBe(
      true
    );

    // Click reset
    root.querySelector("[data-error-reset]").click();

    expect(root.querySelector("[data-error-body]").hasAttribute("hidden")).toBe(
      false
    );
    expect(
      root.querySelector("[data-error-fallback]").hasAttribute("hidden")
    ).toBe(true);
    expect(api.emitState).toHaveBeenLastCalledWith(
      expect.objectContaining({ state: "healthy" })
    );
  });

  it("uses boundaryId from props", async () => {
    const fn = await getMountFn();
    const root = createBoundaryDOM();
    const api = createMockApi();

    fn(
      createPayload(root, { boundaryId: "custom-b" }, { id: "x", name: "y" }),
      api
    );

    expect(api.emitState).toHaveBeenCalledWith(
      expect.objectContaining({ boundaryId: "custom-b" })
    );
  });

  it("falls back to payload.id then payload.name for boundaryId", async () => {
    const fn = await getMountFn();
    const root = createBoundaryDOM();
    const api = createMockApi();

    fn(createPayload(root, {}, { id: "from-id", name: "from-name" }), api);
    expect(api.emitState).toHaveBeenCalledWith(
      expect.objectContaining({ boundaryId: "from-id" })
    );
  });

  it("cleanup removes document listener and reset listener", async () => {
    const fn = await getMountFn();
    const root = createBoundaryDOM();
    const api = createMockApi();

    const cleanup = fn(
      createPayload(root, {}, { id: "b1", name: "boundary" }),
      api
    );
    api.emitState.mockClear();

    cleanup();

    // Error after cleanup should not trigger state change
    dispatchError({ id: "b1" });
    expect(api.emitState).not.toHaveBeenCalled();

    // Reset after cleanup should also not trigger
    root.querySelector("[data-error-reset]").click();
    expect(api.emitState).not.toHaveBeenCalled();
  });

  it("populates [data-error-message] with detail.reason", async () => {
    const fn = await getMountFn();
    const root = createBoundaryDOM();
    root.querySelector("[data-error-fallback]").innerHTML +=
      '<span data-error-message></span>';
    const api = createMockApi();

    fn(createPayload(root, {}, { id: "b1", name: "boundary" }), api);

    dispatchError({ id: "b1", reason: "Component crashed" });

    expect(root.querySelector("[data-error-message]").textContent).toBe(
      "Component crashed"
    );
  });

  it("clears [data-error-message] on reset", async () => {
    const fn = await getMountFn();
    const root = createBoundaryDOM();
    root.querySelector("[data-error-fallback]").innerHTML +=
      '<span data-error-message></span>';
    const api = createMockApi();

    fn(createPayload(root, {}, { id: "b1", name: "boundary" }), api);

    dispatchError({ id: "b1", reason: "Component crashed" });
    expect(root.querySelector("[data-error-message]").textContent).toBe(
      "Component crashed"
    );

    root.querySelector("[data-error-reset]").click();
    expect(root.querySelector("[data-error-message]").textContent).toBe("");
  });

  it("uses textContent for message (XSS safe)", async () => {
    const fn = await getMountFn();
    const root = createBoundaryDOM();
    root.querySelector("[data-error-fallback]").innerHTML +=
      '<span data-error-message></span>';
    const api = createMockApi();

    fn(createPayload(root, {}, { id: "b1", name: "boundary" }), api);

    dispatchError({ id: "b1", reason: "<script>alert(1)</script>" });

    const msgEl = root.querySelector("[data-error-message]");
    expect(msgEl.textContent).toBe("<script>alert(1)</script>");
    expect(msgEl.innerHTML).not.toContain("<script>");
  });

  it("retry button dispatches action and resets to healthy", async () => {
    const fn = await getMountFn();
    const root = createBoundaryDOM();
    root.querySelector("[data-error-fallback]").innerHTML +=
      '<button data-error-retry>Retry</button>';
    const api = createMockApi();

    fn(createPayload(root, {}, { id: "b1", name: "boundary" }), api);

    // Trigger error first
    dispatchError({ id: "b1", reason: "timeout" });
    expect(root.querySelector("[data-error-body]").hasAttribute("hidden")).toBe(
      true
    );

    // Click retry
    root.querySelector("[data-error-retry]").click();

    // Should dispatch action
    expect(api.emitAction).toHaveBeenCalledWith("retry", "pending", {});

    // Should reset to healthy
    expect(root.querySelector("[data-error-body]").hasAttribute("hidden")).toBe(
      false
    );
    expect(
      root.querySelector("[data-error-fallback]").hasAttribute("hidden")
    ).toBe(true);
    expect(api.emitState).toHaveBeenLastCalledWith(
      expect.objectContaining({ state: "healthy" })
    );
  });

  it("emits chirp:island:error:report telemetry event on error", async () => {
    const fn = await getMountFn();
    const root = createBoundaryDOM();
    const api = createMockApi();

    const cleanup = fn(
      createPayload(
        root,
        { boundaryId: "telem-boundary-1" },
        { id: "telem-1", name: "telem-name-1" }
      ),
      api
    );

    const reports = [];
    const listener = (e) => {
      if (e.detail.boundaryId === "telem-boundary-1") reports.push(e.detail);
    };
    document.addEventListener("chirp:island:error:report", listener);

    try {
      dispatchError({ id: "telem-1", reason: "render failed" });

      expect(reports).toHaveLength(1);
      expect(reports[0]).toMatchObject({
        boundaryId: "telem-boundary-1",
        reason: "render failed",
        source: "error_boundary",
      });
      expect(typeof reports[0].timestamp).toBe("number");
      expect(reports[0].timestamp).toBeGreaterThan(0);
    } finally {
      document.removeEventListener("chirp:island:error:report", listener);
      cleanup();
    }
  });

  it("telemetry event fires even with empty reason", async () => {
    const fn = await getMountFn();
    const root = createBoundaryDOM();
    const api = createMockApi();

    const cleanup = fn(
      createPayload(root, {}, { id: "telem-2", name: "boundary" }),
      api
    );

    const reports = [];
    const listener = (e) => {
      if (e.detail.boundaryId === "telem-2") reports.push(e.detail);
    };
    document.addEventListener("chirp:island:error:report", listener);

    try {
      dispatchError({ id: "telem-2" });

      expect(reports).toHaveLength(1);
      expect(reports[0].reason).toBe("");
      expect(reports[0].source).toBe("error_boundary");
    } finally {
      document.removeEventListener("chirp:island:error:report", listener);
      cleanup();
    }
  });

  it("cleanup removes retry listener", async () => {
    const fn = await getMountFn();
    const root = createBoundaryDOM();
    root.querySelector("[data-error-fallback]").innerHTML +=
      '<button data-error-retry>Retry</button>';
    const api = createMockApi();

    const cleanup = fn(
      createPayload(root, {}, { id: "b1", name: "boundary" }),
      api
    );
    api.emitAction.mockClear();
    api.emitState.mockClear();

    cleanup();

    // Retry after cleanup should not trigger action
    root.querySelector("[data-error-retry]").click();
    expect(api.emitAction).not.toHaveBeenCalled();
  });

  it("works without [data-error-message] element (backward compat)", async () => {
    const fn = await getMountFn();
    const root = createBoundaryDOM();
    const api = createMockApi();

    // No [data-error-message] in DOM — should not throw
    fn(createPayload(root, {}, { id: "b1", name: "boundary" }), api);

    dispatchError({ id: "b1", reason: "crash" });

    expect(root.querySelector("[data-error-body]").hasAttribute("hidden")).toBe(
      true
    );
    expect(api.emitState).toHaveBeenLastCalledWith(
      expect.objectContaining({ state: "error" })
    );
  });
});
