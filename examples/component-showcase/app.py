"""chirp-ui Component Showcase — spin up to see all components.

Requires: pip install chirp chirp-ui
Run: python app.py
"""

import asyncio
import calendar as cal_mod
import csv
import inspect
import io
import re
from pathlib import Path
from urllib.parse import quote

from chirp import (
    App,
    AppConfig,
    EventStream,
    FormAction,
    Fragment,
    Request,
    Response,
    SSEEvent,
    Template,
    ValidationError,
)
from chirp.middleware.static import StaticFiles

import chirp_ui

TEMPLATES_DIR = Path(__file__).parent / "templates"

# Build config with only params supported by installed Chirp (islands added in newer versions)
_config_kwargs: dict[str, object] = {
    "template_dir": TEMPLATES_DIR,
    "debug": False,
    "view_transitions": True,
    "delegation": True,
    "islands": True,
}
_sig = inspect.signature(AppConfig)
_allowed = {k: v for k, v in _config_kwargs.items() if k in _sig.parameters}
app = App(AppConfig(**_allowed))
try:
    from chirp import use_chirp_ui

    use_chirp_ui(app)
except ImportError:
    app.add_middleware(StaticFiles(directory=str(chirp_ui.static_path()), prefix="/static"))

chirp_ui.register_filters(app)


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


@app.route("/navigation", template="showcase/navigation.html")
async def navigation() -> Template:
    return Template("showcase/navigation.html")


@app.route("/layout", template="showcase/layout.html")
async def layout() -> Template:
    return Template("showcase/layout.html")


@app.route("/layout/dir", methods=["GET"])
async def layout_dir(request: Request) -> Fragment:
    """Return Fragment with dir block for RTL/LTR toggle."""
    direction = request.query.get("dir", "ltr")
    return Fragment("showcase/_layout_dir.html", "dir_block", direction=direction)


@app.route("/carousel", template="showcase/carousel.html")
async def carousel_page() -> Template:
    return Template("showcase/carousel.html")


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


@app.route("/islands", template="showcase/islands.html")
async def islands_demo() -> Template:
    return Template("showcase/islands.html")


@app.route("/islands/remount", methods=["GET"])
async def islands_remount() -> Fragment:
    return Fragment("showcase/islands.html", "island_mount")


@app.route("/islands/grid-state", template="showcase/islands_grid_state.html")
async def islands_grid_state() -> Template:
    return Template("showcase/islands_grid_state.html")


@app.route("/islands/wizard-state", template="showcase/islands_wizard_state.html")
async def islands_wizard_state() -> Template:
    return Template("showcase/islands_wizard_state.html")


@app.route("/islands/upload-state", template="showcase/islands_upload_state.html")
async def islands_upload_state() -> Template:
    return Template("showcase/islands_upload_state.html")


@app.route("/streaming", template="showcase/streaming.html")
async def streaming() -> Template:
    return Template("showcase/streaming.html")


@app.route("/streaming/demo", methods=["GET"])
async def streaming_demo(request: Request) -> EventStream:
    """Mock SSE stream: yields fragments word-by-word, no LLM required."""

    async def generate():
        words = ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog."]
        text = ""
        for word in words:
            text = f"{text} {word}".strip() if text else word
            yield Fragment("showcase/_streaming_demo.html", "streaming_text", text=text)
            await asyncio.sleep(0.15)
        yield SSEEvent(event="done", data="complete")

    return EventStream(generate())


# Team roster: name, email, role, status, last_active, avatar
TABLE_DATA: list[tuple[str, str, str, str, str, str]] = [
    ("Alice", "alice@example.com", "Admin", "success", "2h ago", "◇"),
    ("Bob", "bob@example.com", "User", "warning", "1d ago", "◆"),
    ("Carol", "carol@example.com", "User", "success", "5m ago", "○"),
    ("Dave", "dave@example.com", "Admin", "default", "3d ago", "△"),
    ("Eve", "eve@example.com", "User", "success", "1h ago", "□"),
    ("Frank", "frank@example.com", "Guest", "default", "1w ago", "▷"),
    ("Grace", "grace@example.com", "Admin", "success", "30m ago", "◇"),
    ("Henry", "henry@example.com", "User", "warning", "2d ago", "◆"),
    ("Ivy", "ivy@example.com", "User", "success", "4h ago", "○"),
    ("Jack", "jack@example.com", "Guest", "default", "5d ago", "△"),
    ("Kate", "kate@example.com", "Admin", "success", "15m ago", "□"),
    ("Leo", "leo@example.com", "User", "success", "1h ago", "▷"),
    ("Mia", "mia@example.com", "User", "warning", "6h ago", "◇"),
    ("Noah", "noah@example.com", "Guest", "default", "2w ago", "◆"),
    ("Oscar", "oscar@example.com", "Admin", "success", "45m ago", "○"),
]
PAGE_SIZE = 5


def _filter_table_data(
    q: str,
    role: str,
    sort_col: str,
    sort_dir: str,
) -> list[tuple[str, str, str, str, str, str]]:
    """Filter and sort TABLE_DATA by query, role, and sort params."""
    col_map = {"name": 0, "email": 1, "role": 2, "status": 3, "last_active": 4}
    sort_idx = col_map.get(sort_col, 0)
    filtered = [
        r
        for r in TABLE_DATA
        if (not q or q in r[0].lower() or q in r[1].lower() or q in r[2].lower())
        and (not role or r[2] == role)
    ]
    return sorted(filtered, key=lambda r: str(r[sort_idx]).lower(), reverse=(sort_dir == "desc"))


@app.route("/data/table", methods=["GET"])
async def data_table(request: Request) -> Fragment:
    """Return table rows + pagination fragment for htmx-driven data page."""
    page = max(1, int(request.query.get("page", 1)))
    sort_col = request.query.get("sort", "name")
    sort_dir = request.query.get("dir", "asc")
    q = (request.query.get("q") or "").strip().lower()
    role = (request.query.get("role") or "").strip()
    density = request.query.get("density", "comfortable")

    sorted_data = _filter_table_data(q, role, sort_col, sort_dir)

    total_rows = len(sorted_data)
    total_pages = max(1, (total_rows + PAGE_SIZE - 1) // PAGE_SIZE)
    page = min(page, total_pages)
    start = (page - 1) * PAGE_SIZE
    rows = sorted_data[start : start + PAGE_SIZE]
    start_row = start + 1 if total_rows else 0
    end_row = min(start + len(rows), total_rows)

    return Fragment(
        "showcase/_table_fragment.html",
        "table_content",
        rows=rows,
        page=page,
        total_pages=total_pages,
        total_rows=total_rows,
        start_row=start_row,
        end_row=end_row,
        sort_col=sort_col,
        sort_dir=sort_dir,
        q=q,
        role=role,
        density=density,
    )


@app.route("/data/bulk-bar", methods=["GET"])
async def data_bulk_bar(request: Request) -> Fragment:
    """Return bulk action bar fragment when rows are selected."""
    selected = request.query.getlist("selected")
    if not selected:
        return Fragment("showcase/_bulk_bar.html", "bulk_bar", count=0)
    return Fragment("showcase/_bulk_bar.html", "bulk_bar", count=len(selected), selected=selected)


@app.route("/data/export", methods=["GET"])
async def data_export(request: Request) -> Response:
    """Export filtered table data as CSV. Use ?selected= to export only selected rows."""
    q = (request.query.get("q") or "").strip().lower()
    role = (request.query.get("role") or "").strip()
    sort_col = request.query.get("sort", "name")
    sort_dir = request.query.get("dir", "asc")
    selected = request.query.getlist("selected")

    sorted_data = _filter_table_data(q, role, sort_col, sort_dir)
    if selected:
        emails = set(selected)
        sorted_data = [r for r in sorted_data if r[1] in emails]

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["Name", "Email", "Role", "Status", "Last active"])
    writer.writerows((r[0], r[1], r[2], r[3], r[4]) for r in sorted_data)
    body = buf.getvalue().encode("utf-8")

    return Response(body=body, content_type="text/csv; charset=utf-8").with_header(
        "Content-Disposition", 'attachment; filename="team-roster.csv"'
    )


@app.route("/data-display", template="showcase/data-display.html")
async def data_display() -> Template:
    return Template("showcase/data-display.html")


@app.route("/calendar", template="showcase/calendar.html")
@app.route("/calendar/{year}/{month}", template="showcase/calendar.html")
async def calendar_view(year: int | str | None = None, month: int | str | None = None) -> Template:
    from datetime import date

    today = date.today()
    year = int(year) if year is not None else today.year
    month = int(month) if month is not None else today.month
    cal = cal_mod.Calendar(firstweekday=cal_mod.SUNDAY)
    weeks = cal.monthdayscalendar(year, month)
    month_name = cal_mod.month_name[month]
    month_label = f"{month_name} {year}"
    prev_month = month - 1 or 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    prev_url = f"/calendar/{prev_year}/{prev_month}"
    next_url = f"/calendar/{next_year}/{next_month}"
    return Template(
        "showcase/calendar.html",
        weeks=weeks,
        month_label=month_label,
        prev_url=prev_url,
        next_url=next_url,
    )


@app.route("/data", template="showcase/data.html")
async def data() -> Template:
    return Template("showcase/data.html")


@app.route("/animation", template="showcase/animation.html")
async def animation() -> Template:
    return Template("showcase/animation.html")


@app.route("/ascii", template="showcase/ascii.html")
async def ascii_icons() -> Template:
    return Template("showcase/ascii.html")


@app.route("/animation/swap-demo", methods=["GET"])
async def animation_swap_demo(request: Request) -> Fragment:
    return Fragment("showcase/_swap_content.html", "swap_demo")


@app.route("/messenger", template="showcase/messenger.html")
async def messenger() -> Template:
    return Template("showcase/messenger.html")


@app.route("/social", template="showcase/social.html")
async def social() -> Template:
    return Template("showcase/social.html")


@app.route("/video", template="showcase/video.html")
async def video() -> Template:
    return Template("showcase/video.html")


if __name__ == "__main__":
    app.run()
