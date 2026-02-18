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
  let timer = null;

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

  const run = () => {
    const fileCount = input?.files ? input.files.length : 0;
    if (fileCount === 0) {
      setAction(payload, api, "upload", "error", { reason: "no_files" });
      write(0, "Select at least one file.");
      return;
    }
    let percent = 0;
    start?.setAttribute("disabled", "disabled");
    setAction(payload, api, "upload", "pending", { endpoint, files: fileCount });
    write(percent, "Uploading...");
    timer = window.setInterval(() => {
      percent = Math.min(100, percent + 15);
      write(percent, `Uploading... ${percent}%`);
      if (percent >= 100) {
        if (timer) {
          window.clearInterval(timer);
          timer = null;
        }
        start?.removeAttribute("disabled");
        write(100, `Uploaded to ${endpoint}`);
        setAction(payload, api, "upload", "success", { endpoint, files: fileCount });
      }
    }, 120);
  };

  start?.addEventListener("click", run);
  write(0, "Idle");

  return () => {
    start?.removeEventListener("click", run);
    if (timer) {
      window.clearInterval(timer);
    }
  };
}

registerPrimitive("upload_state", { mount });
