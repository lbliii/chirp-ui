import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { mockChirpIslands, createPayload, createMockApi } from "./helpers.js";

let mount;
let islands;

beforeEach(() => {
  islands = mockChirpIslands();
  global.fetch = vi.fn();
  global.htmx = { swap: vi.fn() };
});

afterEach(() => {
  islands.teardown();
  vi.restoreAllMocks();
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
  const input = root.querySelector("[data-upload-input]");
  const files = Array.from(
    { length: count },
    (_, i) => new File(["content"], `file-${i}.txt`, { type: "text/plain" })
  );
  Object.defineProperty(input, "files", {
    value: files,
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

  it("POSTs each file and applies OOB HTML from the server", async () => {
    const fn = await getMountFn();
    const root = createUploadDOM();
    const api = createMockApi();

    fetch.mockResolvedValue({
      text: async () => '<div id="attachment-1" hx-swap-oob="outerHTML"></div>',
    });

    fn(createPayload(root, { endpoint: "/api/upload" }), api);
    setFiles(root, 2);
    api.emitAction.mockClear();

    root.querySelector("[data-upload-start]").click();
    await vi.waitFor(() => {
      expect(fetch).toHaveBeenCalledTimes(2);
      expect(global.htmx.swap).toHaveBeenCalledTimes(2);
    });
    expect(api.emitAction).toHaveBeenCalledWith("upload", "success", {
      endpoint: "/api/upload",
      files: 2,
    });
    expect(root.querySelector("[data-upload-status]").textContent).toBe(
      "Uploaded to /api/upload"
    );
  });

  it("disables the start button while uploading", async () => {
    const fn = await getMountFn();
    const root = createUploadDOM();
    const api = createMockApi();
    let resolveFetch;
    fetch.mockReturnValue(
      new Promise((resolve) => {
        resolveFetch = resolve;
      })
    );

    fn(createPayload(root, {}), api);
    setFiles(root, 1);
    const btn = root.querySelector("[data-upload-start]");

    const pending = root.querySelector("[data-upload-start]").click();
    expect(btn.hasAttribute("disabled")).toBe(true);

    resolveFetch({ text: async () => "" });
    await pending;
    await Promise.resolve();

    expect(btn.hasAttribute("disabled")).toBe(false);
  });

  it("cleanup removes listener", async () => {
    const fn = await getMountFn();
    const root = createUploadDOM();
    const api = createMockApi();

    const cleanup = fn(createPayload(root, {}), api);
    cleanup();

    api.emitAction.mockClear();
    root.querySelector("[data-upload-start]").click();
    expect(api.emitAction).not.toHaveBeenCalled();
  });
});
