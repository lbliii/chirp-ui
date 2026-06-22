import { readProps, registerPrimitive, setAction, setState } from "/static/islands/foundation.js";

function mount(payload, api) {
  const props = readProps(payload);
  const root = payload.element;
  const stateKey = String(props.stateKey || "upload");
  const endpoint = String(props.endpoint || "/upload");
  const input = root.querySelector("[data-upload-input]");
  const start = root.querySelector("[data-upload-start]");
  const progress = root.querySelector("[data-upload-progress]");
  const status = root.querySelector("[data-upload-status]");

  const write = (percent, message) => {
    if (progress) {
      progress.value = percent;
    }
    if (status) {
      status.textContent = message;
    }
    setState(payload, api, {
      stateKey,
      endpoint,
      percent,
      message,
      files: input?.files ? input.files.length : 0,
    });
  };

  const run = async () => {
    const files = input?.files ? Array.from(input.files) : [];
    if (!files.length) {
      setAction(payload, api, "upload", "error", { reason: "no_files" });
      write(0, "Select at least one file.");
      return;
    }
    start?.setAttribute("disabled", "disabled");
    setAction(payload, api, "upload", "pending", { endpoint, files: files.length });
    write(0, "Uploading...");
    try {
      for (const file of files) {
        const body = new FormData();
        body.append("file", file);
        const res = await fetch(endpoint, { method: "POST", body });
        const html = await res.text();
        if (window.htmx && typeof window.htmx.swap === "function") {
          window.htmx.swap(document.body, html, { swapStyle: "none" });
        }
      }
      write(100, `Uploaded to ${endpoint}`);
      setAction(payload, api, "upload", "success", { endpoint, files: files.length });
    } catch (error) {
      write(0, "Upload failed.");
      setAction(payload, api, "upload", "error", { reason: "network_error" });
    } finally {
      start?.removeAttribute("disabled");
    }
  };

  start?.addEventListener("click", run);
  write(0, "Idle");

  return () => {
    start?.removeEventListener("click", run);
  };
}

registerPrimitive("upload_state", { mount });
