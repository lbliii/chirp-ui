import { describe, it, expect, vi, afterEach } from "vitest";
import {
  readProps,
  attachCleanup,
  runCleanup,
  setState,
  setAction,
  setError,
  registerPrimitive,
} from "../../src/chirp_ui/templates/islands/foundation.js";

// ---------------------------------------------------------------------------
// readProps
// ---------------------------------------------------------------------------
describe("readProps", () => {
  it("extracts props from payload", () => {
    expect(readProps({ props: { seed: 5 } })).toEqual({ seed: 5 });
  });

  it("returns empty object for empty payload", () => {
    expect(readProps({})).toEqual({});
  });

  it("returns empty object for null payload", () => {
    expect(readProps(null)).toEqual({});
  });

  it("returns empty object for undefined payload", () => {
    expect(readProps(undefined)).toEqual({});
  });

  it("returns empty object when props is a non-object", () => {
    expect(readProps({ props: "string" })).toEqual({});
    expect(readProps({ props: 42 })).toEqual({});
    expect(readProps({ props: null })).toEqual({});
  });
});

// ---------------------------------------------------------------------------
// attachCleanup + runCleanup
// ---------------------------------------------------------------------------
describe("attachCleanup / runCleanup", () => {
  it("registers and runs a cleanup function", () => {
    const el = document.createElement("div");
    const cleanup = vi.fn();
    attachCleanup({ element: el }, cleanup);
    runCleanup({ element: el });
    expect(cleanup).toHaveBeenCalledOnce();
  });

  it("double runCleanup is a no-op (no double call)", () => {
    const el = document.createElement("div");
    const cleanup = vi.fn();
    attachCleanup({ element: el }, cleanup);
    runCleanup({ element: el });
    runCleanup({ element: el });
    expect(cleanup).toHaveBeenCalledOnce();
  });

  it("runCleanup without prior attach is a no-op", () => {
    const el = document.createElement("div");
    // Should not throw
    runCleanup({ element: el });
  });

  it("independent elements have independent cleanups", () => {
    const el1 = document.createElement("div");
    const el2 = document.createElement("div");
    const c1 = vi.fn();
    const c2 = vi.fn();
    attachCleanup({ element: el1 }, c1);
    attachCleanup({ element: el2 }, c2);
    runCleanup({ element: el1 });
    expect(c1).toHaveBeenCalledOnce();
    expect(c2).not.toHaveBeenCalled();
    runCleanup({ element: el2 });
    expect(c2).toHaveBeenCalledOnce();
  });

  it("no-ops when payload is null or has no element", () => {
    // Should not throw
    attachCleanup(null, vi.fn());
    attachCleanup({}, vi.fn());
    attachCleanup({ element: document.createElement("div") }, "not a function");
    runCleanup(null);
    runCleanup({});
  });
});

// ---------------------------------------------------------------------------
// setState
// ---------------------------------------------------------------------------
describe("setState", () => {
  afterEach(() => {
    // Clean up any lingering listeners
  });

  it("dispatches CustomEvent on document and window when no api", () => {
    const docSpy = vi.fn();
    const winSpy = vi.fn();
    document.addEventListener("chirp:island:state", docSpy);
    window.addEventListener("chirp:island:state", winSpy);

    const payload = { name: "test", id: "t1", version: "1" };
    setState(payload, null, { count: 42 });

    expect(docSpy).toHaveBeenCalledOnce();
    expect(winSpy).toHaveBeenCalledOnce();
    expect(docSpy.mock.calls[0][0].detail.state).toEqual({ count: 42 });

    document.removeEventListener("chirp:island:state", docSpy);
    window.removeEventListener("chirp:island:state", winSpy);
  });

  it("uses api.emitState when available", () => {
    const emitState = vi.fn();
    setState({}, { emitState }, { count: 1 });
    expect(emitState).toHaveBeenCalledWith({ count: 1 });
  });

  it("event detail includes safeDetail (name, id, version only)", () => {
    const spy = vi.fn();
    document.addEventListener("chirp:island:state", spy);

    const payload = {
      name: "my-island",
      id: "i42",
      version: "2",
      element: document.createElement("div"),
      props: { secret: true },
    };
    setState(payload, null, { active: true });

    const detail = spy.mock.calls[0][0].detail;
    expect(detail.name).toBe("my-island");
    expect(detail.id).toBe("i42");
    expect(detail.version).toBe("2");
    expect(detail.element).toBeUndefined();
    expect(detail.props).toBeUndefined();

    document.removeEventListener("chirp:island:state", spy);
  });

  it("does not call CustomEvent when api.emitState exists", () => {
    const spy = vi.fn();
    document.addEventListener("chirp:island:state", spy);

    setState({}, { emitState: vi.fn() }, { x: 1 });
    expect(spy).not.toHaveBeenCalled();

    document.removeEventListener("chirp:island:state", spy);
  });
});

// ---------------------------------------------------------------------------
// setAction
// ---------------------------------------------------------------------------
describe("setAction", () => {
  it("uses api.emitAction when available", () => {
    const emitAction = vi.fn();
    setAction({}, { emitAction }, "increment", "success", { delta: 1 });
    expect(emitAction).toHaveBeenCalledWith("increment", "success", {
      delta: 1,
    });
  });

  it("dispatches CustomEvent with action, status, and extra when no api", () => {
    const spy = vi.fn();
    document.addEventListener("chirp:island:action", spy);

    const payload = { name: "ctr", id: "c1", version: "1" };
    setAction(payload, null, "save", "pending", { draftKey: "notes" });

    const detail = spy.mock.calls[0][0].detail;
    expect(detail.action).toBe("save");
    expect(detail.status).toBe("pending");
    expect(detail.draftKey).toBe("notes");
    expect(detail.name).toBe("ctr");

    document.removeEventListener("chirp:island:action", spy);
  });

  it("dispatches on both document and window", () => {
    const docSpy = vi.fn();
    const winSpy = vi.fn();
    document.addEventListener("chirp:island:action", docSpy);
    window.addEventListener("chirp:island:action", winSpy);

    setAction({ name: "x", id: "1", version: "1" }, null, "click", "success");

    expect(docSpy).toHaveBeenCalledOnce();
    expect(winSpy).toHaveBeenCalledOnce();

    document.removeEventListener("chirp:island:action", docSpy);
    window.removeEventListener("chirp:island:action", winSpy);
  });

  it("extra defaults to empty object", () => {
    const emitAction = vi.fn();
    setAction({}, { emitAction }, "test", "done");
    expect(emitAction).toHaveBeenCalledWith("test", "done", {});
  });
});

// ---------------------------------------------------------------------------
// setError
// ---------------------------------------------------------------------------
describe("setError", () => {
  it("uses api.emitError when available", () => {
    const emitError = vi.fn();
    setError({}, { emitError }, "timeout", { ms: 5000 });
    expect(emitError).toHaveBeenCalledWith("timeout", { ms: 5000 });
  });

  it("dispatches CustomEvent with error='primitive' and reason when no api", () => {
    const spy = vi.fn();
    document.addEventListener("chirp:island:error", spy);

    const payload = { name: "uploader", id: "u1", version: "1" };
    setError(payload, null, "network_fail", { endpoint: "/api" });

    const detail = spy.mock.calls[0][0].detail;
    expect(detail.error).toBe("primitive");
    expect(detail.reason).toBe("network_fail");
    expect(detail.endpoint).toBe("/api");
    expect(detail.name).toBe("uploader");

    document.removeEventListener("chirp:island:error", spy);
  });

  it("dispatches on both document and window", () => {
    const docSpy = vi.fn();
    const winSpy = vi.fn();
    document.addEventListener("chirp:island:error", docSpy);
    window.addEventListener("chirp:island:error", winSpy);

    setError({ name: "x", id: "1", version: "1" }, null, "oops");

    expect(docSpy).toHaveBeenCalledOnce();
    expect(winSpy).toHaveBeenCalledOnce();

    document.removeEventListener("chirp:island:error", docSpy);
    window.removeEventListener("chirp:island:error", winSpy);
  });

  it("extra defaults to empty object", () => {
    const emitError = vi.fn();
    setError({}, { emitError }, "fail");
    expect(emitError).toHaveBeenCalledWith("fail", {});
  });
});

// ---------------------------------------------------------------------------
// registerPrimitive
// ---------------------------------------------------------------------------
describe("registerPrimitive", () => {
  afterEach(() => {
    delete window.chirpIslands;
  });

  it("throws when window.chirpIslands is missing", () => {
    delete window.chirpIslands;
    expect(() => registerPrimitive("foo", () => {})).toThrow(
      "chirpIslands.register() missing"
    );
  });

  it("throws when chirpIslands exists but register is not a function", () => {
    window.chirpIslands = {};
    expect(() => registerPrimitive("foo", () => {})).toThrow(
      "chirpIslands.register() missing"
    );
  });

  it("calls register with name and adapter", () => {
    const register = vi.fn();
    window.chirpIslands = { register };
    const adapter = { mount: () => {} };
    registerPrimitive("counter-widget", adapter);
    expect(register).toHaveBeenCalledWith("counter-widget", adapter);
  });
});
