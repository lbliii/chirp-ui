import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { mockChirpIslands, createPayload, createMockApi } from "./helpers.js";

let mount;
let islands;

beforeEach(() => {
  vi.useFakeTimers();
  islands = mockChirpIslands();
});

afterEach(() => {
  vi.useRealTimers();
  islands.teardown();
});

async function getMountFn() {
  if (!mount) {
    await import("../../src/chirp_ui/templates/islands/upload_state.js");
    mount = islands.register.mock.calls.find(
      (c) => c[0] === "upload_state"
    )?.[1]?.mount;
  }
  return mount;
}

function createUploadDOM() {
  const root = document.createElement("div");
  root.innerHTML = `
    <input data-upload-input type="file" />
    <button data-upload-start>Upload</button>
    <progress data-upload-progress value="0" max="100"></progress>
    <span data-upload-status></span>
  `;
  return root;
}

function setFiles(root, count) {
  // Mock the files property on the file input
  const input = root.querySelector("[data-upload-input]");
  Object.defineProperty(input, "files", {
    value: { length: count },
    writable: true,
    configurable: true,
  });
}

describe("upload_state", () => {
  it("registers as 'upload_state' primitive", async () => {
    const fn = await getMountFn();
    expect(fn).toBeTypeOf("function");
  });

  it("initializes with idle state", async () => {
    const fn = await getMountFn();
    const root = createUploadDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    expect(root.querySelector("[data-upload-status]").textContent).toBe("Idle");
    expect(api.emitState).toHaveBeenCalledWith(
      expect.objectContaining({ percent: 0, message: "Idle" })
    );
  });

  it("errors when no files selected", async () => {
    const fn = await getMountFn();
    const root = createUploadDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);
    api.emitAction.mockClear();

    root.querySelector("[data-upload-start]").click();

    expect(api.emitAction).toHaveBeenCalledWith("upload", "error", {
      reason: "no_files",
    });
    expect(root.querySelector("[data-upload-status]").textContent).toBe(
      "Select at least one file."
    );
  });

  it("starts upload with pending action when files exist", async () => {
    const fn = await getMountFn();
    const root = createUploadDOM();
    const api = createMockApi();

    fn(createPayload(root, { endpoint: "/api/upload" }), api);
    setFiles(root, 2);
    api.emitAction.mockClear();

    root.querySelector("[data-upload-start]").click();

    expect(api.emitAction).toHaveBeenCalledWith("upload", "pending", {
      endpoint: "/api/upload",
      files: 2,
    });
    expect(
      root.querySelector("[data-upload-start]").hasAttribute("disabled")
    ).toBe(true);
  });

  it("progress increments by 15 every 120ms", async () => {
    const fn = await getMountFn();
    const root = createUploadDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);
    setFiles(root, 1);

    root.querySelector("[data-upload-start]").click();

    vi.advanceTimersByTime(120); // +15 → 15
    expect(root.querySelector("[data-upload-progress]").value).toBe(15);

    vi.advanceTimersByTime(120); // +15 → 30
    expect(root.querySelector("[data-upload-progress]").value).toBe(30);
  });

  it("progress is capped at 100", async () => {
    const fn = await getMountFn();
    const root = createUploadDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);
    setFiles(root, 1);

    root.querySelector("[data-upload-start]").click();

    // 7 ticks × 15 = 105, but capped to 100
    // Tick at: 15, 30, 45, 60, 75, 90, 100 (cap)
    vi.advanceTimersByTime(120 * 7);

    expect(root.querySelector("[data-upload-progress]").value).toBe(100);
  });

  it("emits success action on completion", async () => {
    const fn = await getMountFn();
    const root = createUploadDOM();
    const api = createMockApi();

    fn(createPayload(root, { endpoint: "/files" }), api);
    setFiles(root, 1);

    root.querySelector("[data-upload-start]").click();
    api.emitAction.mockClear();

    // Run enough ticks to reach 100
    vi.advanceTimersByTime(120 * 7);

    expect(api.emitAction).toHaveBeenCalledWith("upload", "success", {
      endpoint: "/files",
      files: 1,
    });
  });

  it("re-enables button after completion", async () => {
    const fn = await getMountFn();
    const root = createUploadDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);
    setFiles(root, 1);

    const btn = root.querySelector("[data-upload-start]");
    btn.click();
    expect(btn.hasAttribute("disabled")).toBe(true);

    vi.advanceTimersByTime(120 * 7);
    expect(btn.hasAttribute("disabled")).toBe(false);
  });

  it("shows final message with endpoint", async () => {
    const fn = await getMountFn();
    const root = createUploadDOM();
    const api = createMockApi();

    fn(createPayload(root, { endpoint: "/api/v2" }), api);
    setFiles(root, 1);

    root.querySelector("[data-upload-start]").click();
    vi.advanceTimersByTime(120 * 7);

    expect(root.querySelector("[data-upload-status]").textContent).toBe(
      "Uploaded to /api/v2"
    );
  });

  it("cleanup clears interval and removes listener", async () => {
    const fn = await getMountFn();
    const root = createUploadDOM();
    const api = createMockApi();

    const cleanup = fn(createPayload(root, {}), api);
    setFiles(root, 1);
    root.querySelector("[data-upload-start]").click();

    // Partially through upload
    vi.advanceTimersByTime(120 * 2); // 30%

    cleanup();
    api.emitState.mockClear();

    // Advance more — should NOT continue ticking
    vi.advanceTimersByTime(120 * 10);
    expect(api.emitState).not.toHaveBeenCalled();
  });

  it("uses default endpoint /upload and stateKey upload", async () => {
    const fn = await getMountFn();
    const root = createUploadDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    expect(api.emitState).toHaveBeenCalledWith(
      expect.objectContaining({
        stateKey: "upload",
        endpoint: "/upload",
      })
    );
  });
});
