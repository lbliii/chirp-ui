"""chirp-ui Component Showcase — spin up to see all components.

Requires: pip install chirp chirp-ui
Run: python app.py
"""

import asyncio
import re
from pathlib import Path
from urllib.parse import quote

import chirp_ui
from chirp import (
    App,
    AppConfig,
    EventStream,
    FormAction,
    Fragment,
    Request,
    SSEEvent,
    Template,
    ValidationError,
)
from chirp.middleware.static import StaticFiles

TEMPLATES_DIR = Path(__file__).parent / "templates"
CHIRPUI_TEMPLATES = Path(chirp_ui.__file__).parent / "templates"

app = App(
    AppConfig(
        template_dir=TEMPLATES_DIR,
        component_dirs=(str(CHIRPUI_TEMPLATES),),
        debug=False,
        view_transitions=True,
        delegation=True,
    )
)
app.add_middleware(
    StaticFiles(directory=str(CHIRPUI_TEMPLATES), prefix="/static")
)


@app.route("/toast", methods=["POST"])
async def show_toast(request: Request) -> Fragment:
    return Fragment("_toast.html", "toast_demo")


@app.route("/", template="index.html")
async def index() -> Template:
    return Template("index.html")


@app.route("/demo", template="showcase/demo.html")
async def demo() -> Template:
    return Template("showcase/demo.html")


@app.route("/demo/submit", methods=["POST"])
async def demo_submit(request: Request) -> Fragment:
    """Return Fragment with model_card for SSE streaming."""
    form = await request.form()
    prompt = (form.get("prompt") or "").strip() or "Hello"
    stream_url = f"/demo/stream?prompt={quote(prompt)}"
    return Fragment("showcase/_demo_card.html", "demo_card", stream_url=stream_url)


@app.route("/demo/stream", methods=["GET"])
async def demo_stream(request: Request) -> EventStream:
    """Stream mock tokens, then OOB toast on done."""

    async def generate():
        prompt = request.query.get("prompt", "Hello")
        words = f"Response to '{prompt}': The quick brown fox jumps over the lazy dog.".split()
        text = ""
        for word in words:
            text = f"{text} {word}".strip() if text else word
            yield Fragment("showcase/_streaming_demo.html", "streaming_text", text=text)
            await asyncio.sleep(0.12)
        yield Fragment("_toast.html", "toast_demo", message="Stream complete")
        yield SSEEvent(event="done", data="complete")

    return EventStream(generate())


@app.route("/layout", template="showcase/layout.html")
async def layout() -> Template:
    return Template("showcase/layout.html")


@app.route("/layout/dir", methods=["GET"])
async def layout_dir(request: Request) -> Fragment:
    """Return Fragment with dir block for RTL/LTR toggle."""
    direction = request.query.get("dir", "ltr")
    return Fragment("showcase/_layout_dir.html", "dir_block", direction=direction)


@app.route("/cards", template="showcase/cards.html")
async def cards() -> Template:
    return Template("showcase/cards.html")


@app.route("/forms", template="showcase/forms.html")
async def forms() -> Template:
    return Template("showcase/forms.html")


@app.route("/forms/demo", methods=["POST"])
async def forms_demo(request: Request) -> FormAction | ValidationError:
    """Validate form; on error return ValidationError, on success FormAction + toast."""
    form = await request.form()
    name = (form.get("name") or "").strip()
    email = (form.get("email") or "").strip()

    errors: dict[str, list[str]] = {}
    if not name:
        errors.setdefault("name", []).append("Name is required")
    if not email:
        errors.setdefault("email", []).append("Email is required")
    elif not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
        errors.setdefault("email", []).append("Enter a valid email address")

    if errors:
        return ValidationError(
            "showcase/_form_demo.html",
            "form_body",
            errors=errors,
            name=name,
            email=email,
        )

    return FormAction(
        "/",
        Fragment("_toast.html", "toast_demo", message="Saved!"),
    )


@app.route("/ui", template="showcase/ui.html")
async def ui() -> Template:
    return Template("showcase/ui.html")


@app.route("/ui/tab/{name}", methods=["GET"])
async def ui_tab(request: Request, name: str) -> Fragment:
    return Fragment("showcase/_tab_content.html", "tab_content", active_tab=name)


@app.route("/streaming", template="showcase/streaming.html")
async def streaming() -> Template:
    return Template("showcase/streaming.html")


@app.route("/streaming/demo", methods=["GET"])
async def streaming_demo(request: Request) -> EventStream:
    """Mock SSE stream: yields fragments word-by-word, no LLM required."""

    async def generate():
        words = "The quick brown fox jumps over the lazy dog.".split()
        text = ""
        for word in words:
            text = f"{text} {word}".strip() if text else word
            yield Fragment("showcase/_streaming_demo.html", "streaming_text", text=text)
            await asyncio.sleep(0.15)
        yield SSEEvent(event="done", data="complete")

    return EventStream(generate())


# Mock data for data table (15 rows, 5 per page)
TABLE_DATA: list[tuple[str, str, str]] = [
    ("Alice", "alice@example.com", "Admin"),
    ("Bob", "bob@example.com", "User"),
    ("Carol", "carol@example.com", "User"),
    ("Dave", "dave@example.com", "Admin"),
    ("Eve", "eve@example.com", "User"),
    ("Frank", "frank@example.com", "Guest"),
    ("Grace", "grace@example.com", "Admin"),
    ("Henry", "henry@example.com", "User"),
    ("Ivy", "ivy@example.com", "User"),
    ("Jack", "jack@example.com", "Guest"),
    ("Kate", "kate@example.com", "Admin"),
    ("Leo", "leo@example.com", "User"),
    ("Mia", "mia@example.com", "User"),
    ("Noah", "noah@example.com", "Guest"),
    ("Oscar", "oscar@example.com", "Admin"),
]
PAGE_SIZE = 5


@app.route("/data", template="showcase/data.html")
async def data() -> Template:
    return Template("showcase/data.html")


@app.route("/data/table", methods=["GET"])
async def data_table(request: Request) -> Fragment:
    """Return table rows + pagination fragment for htmx-driven data page."""
    page = max(1, int(request.query.get("page", 1)))
    sort_col = request.query.get("sort", "name")

    col_map = {"name": 0, "email": 1, "role": 2}
    sort_idx = col_map.get(sort_col, 0)
    sorted_data = sorted(TABLE_DATA, key=lambda r: r[sort_idx].lower())

    total_pages = (len(sorted_data) + PAGE_SIZE - 1) // PAGE_SIZE
    page = min(page, max(1, total_pages))
    start = (page - 1) * PAGE_SIZE
    rows = sorted_data[start : start + PAGE_SIZE]

    return Fragment(
        "showcase/_table_fragment.html",
        "table_content",
        rows=rows,
        page=page,
        total_pages=total_pages,
        sort_col=sort_col,
    )


@app.route("/animation", template="showcase/animation.html")
async def animation() -> Template:
    return Template("showcase/animation.html")


@app.route("/ascii", template="showcase/ascii.html")
async def ascii_icons() -> Template:
    return Template("showcase/ascii.html")


@app.route("/animation/swap-demo", methods=["GET"])
async def animation_swap_demo(request: Request) -> Fragment:
    return Fragment("showcase/_swap_content.html", "swap_demo")


if __name__ == "__main__":
    app.run()
