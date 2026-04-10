import { readProps, registerPrimitive, setState, setAction } from "/static/islands/foundation.js";

function mount(payload, api) {
  const props = readProps(payload);
  const root = payload.element;
  const boundaryId = String(props.boundaryId || payload.id || payload.name);
  const fallback = root.querySelector("[data-error-fallback]");
  const reset = root.querySelector("[data-error-reset]");
  const retry = root.querySelector("[data-error-retry]");
  const body = root.querySelector("[data-error-body]");
  const messageEl = root.querySelector("[data-error-message]");

  const showFallback = (reason) => {
    fallback?.removeAttribute("hidden");
    body?.setAttribute("hidden", "hidden");
    if (messageEl && reason) {
      messageEl.textContent = String(reason);
    }
    setState(payload, api, { boundaryId, state: "error" });
  };

  const clearFallback = () => {
    fallback?.setAttribute("hidden", "hidden");
    body?.removeAttribute("hidden");
    if (messageEl) {
      messageEl.textContent = "";
    }
    setState(payload, api, { boundaryId, state: "healthy" });
  };

  const onError = (event) => {
    const detail = event.detail || {};
    const targetId = detail.id || null;
    if (targetId && payload.id && targetId !== payload.id) {
      return;
    }
    if (detail.name && detail.name !== payload.name && !detail.error) {
      return;
    }
    const reason = detail.reason || "";
    showFallback(reason);
    document.dispatchEvent(
      new CustomEvent("chirp:island:error:report", {
        detail: { boundaryId, reason, timestamp: Date.now(), source: "error_boundary" },
      })
    );
  };

  const onReset = () => clearFallback();

  const onRetry = () => {
    setAction(payload, api, "retry", "pending");
    clearFallback();
  };

  document.addEventListener("chirp:island:error", onError);
  reset?.addEventListener("click", onReset);
  retry?.addEventListener("click", onRetry);
  clearFallback();

  return () => {
    document.removeEventListener("chirp:island:error", onError);
    reset?.removeEventListener("click", onReset);
    retry?.removeEventListener("click", onRetry);
  };
}

registerPrimitive("error_boundary", { mount });
