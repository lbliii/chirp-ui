import { readProps, registerPrimitive, setAction, setState } from "/static/islands/foundation.js";

function mount(payload, api) {
  const props = readProps(payload);
  const root = payload.element;
  const draftKey = String(props.draftKey || "draft");
  const storageKey = `chirp:draft:${draftKey}`;
  const fields = root.querySelectorAll("[data-draft-field]");
  const savedNode = root.querySelector("[data-draft-saved-at]");
  let timer = null;

  const writeSavedAt = (iso) => {
    if (savedNode) {
      savedNode.textContent = iso ? new Date(iso).toLocaleTimeString() : "never";
    }
  };

  const snapshot = () => {
    const data = {};
    fields.forEach((el) => {
      const key = el.getAttribute("name") || el.getAttribute("data-draft-field");
      if (!key) return;
      data[key] = "value" in el ? String(el.value) : "";
    });
    return data;
  };

  const persist = () => {
    const now = new Date().toISOString();
    const data = snapshot();
    window.localStorage.setItem(storageKey, JSON.stringify({ savedAt: now, data }));
    writeSavedAt(now);
    setState(payload, api, { draftKey, savedAt: now, keys: Object.keys(data) });
    setAction(payload, api, "save", "success", { draftKey });
  };

  const schedule = () => {
    if (timer) window.clearTimeout(timer);
    timer = window.setTimeout(persist, 250);
  };

  const handlers = [];
  fields.forEach((el) => {
    el.addEventListener("input", schedule);
    handlers.push([el, schedule]);
  });

  const raw = window.localStorage.getItem(storageKey);
  if (raw) {
    try {
      const parsed = JSON.parse(raw);
      const data = parsed && parsed.data ? parsed.data : {};
      fields.forEach((el) => {
        const key = el.getAttribute("name") || el.getAttribute("data-draft-field");
        if (!key || !(key in data) || !("value" in el)) return;
        el.value = String(data[key]);
      });
      writeSavedAt(parsed.savedAt || null);
      setState(payload, api, { draftKey, restored: true });
    } catch {
      writeSavedAt(null);
    }
  } else {
    writeSavedAt(null);
  }

  return () => {
    handlers.forEach(([el, fn]) => el.removeEventListener("input", fn));
    if (timer) {
      window.clearTimeout(timer);
    }
  };
}

registerPrimitive("draft_store", { mount });
