const cleanerByElement = new WeakMap();

function safeDetail(payload) {
  return {
    name: payload.name,
    id: payload.id,
    version: payload.version,
  };
}

export function readProps(payload) {
  return payload && payload.props && typeof payload.props === "object" ? payload.props : {};
}

export function attachCleanup(payload, cleanup) {
  if (!payload || !payload.element || typeof cleanup !== "function") {
    return;
  }
  cleanerByElement.set(payload.element, cleanup);
}

export function runCleanup(payload) {
  if (!payload || !payload.element) {
    return;
  }
  const cleanup = cleanerByElement.get(payload.element);
  if (!cleanup) {
    return;
  }
  cleanerByElement.delete(payload.element);
  cleanup();
}

export function setState(payload, api, state) {
  if (api && typeof api.emitState === "function") {
    api.emitState(state);
    return;
  }
  const detail = { ...safeDetail(payload), state };
  document.dispatchEvent(new CustomEvent("chirp:island:state", { detail }));
  window.dispatchEvent(new CustomEvent("chirp:island:state", { detail }));
}

export function setAction(payload, api, action, status, extra = {}) {
  if (api && typeof api.emitAction === "function") {
    api.emitAction(action, status, extra);
    return;
  }
  const detail = { ...safeDetail(payload), action, status, ...extra };
  document.dispatchEvent(new CustomEvent("chirp:island:action", { detail }));
  window.dispatchEvent(new CustomEvent("chirp:island:action", { detail }));
}

export function setError(payload, api, reason, extra = {}) {
  if (api && typeof api.emitError === "function") {
    api.emitError(reason, extra);
    return;
  }
  const detail = { ...safeDetail(payload), error: "primitive", reason, ...extra };
  document.dispatchEvent(new CustomEvent("chirp:island:error", { detail }));
  window.dispatchEvent(new CustomEvent("chirp:island:error", { detail }));
}

export function registerPrimitive(name, adapter) {
  if (!window.chirpIslands || typeof window.chirpIslands.register !== "function") {
    throw new Error(`chirpIslands.register() missing for primitive '${name}'`);
  }
  window.chirpIslands.register(name, adapter);
}
