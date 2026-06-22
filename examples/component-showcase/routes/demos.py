"""Interactive demo routes: quick demo, streaming, islands, and team roster."""

from __future__ import annotations

import asyncio
import csv
import io
import re
from urllib.parse import quote

from chirp import (
    App,
    EventStream,
    FormAction,
    Fragment,
    Request,
    Response,
    SSEEvent,
    Template,
    ValidationError,
)
from fixtures.roster import PAGE_SIZE, TABLE_DATA, filter_table_data
from showcase.helpers import page, query_list


def register(app: App) -> None:
    @app.route("/", template="index.html")
    async def index(request: Request) -> Template:
        return page(request, "index.html")

    @app.route("/demo", template="showcase/demo.html")
    async def demo(request: Request) -> Template:
        return page(request, "showcase/demo.html")

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

    @app.route("/islands", template="showcase/islands.html")
    async def islands_demo(request: Request) -> Template:
        return page(request, "showcase/islands.html")

    @app.route("/islands/remount", methods=["GET"])
    async def islands_remount() -> Fragment:
        return Fragment("showcase/islands.html", "island_mount")

    @app.route("/islands/grid-state", template="showcase/islands_grid_state.html")
    async def islands_grid_state(request: Request) -> Template:
        return page(request, "showcase/islands_grid_state.html")

    @app.route("/islands/wizard-state", template="showcase/islands_wizard_state.html")
    async def islands_wizard_state(request: Request) -> Template:
        return page(request, "showcase/islands_wizard_state.html")

    @app.route("/islands/upload-state", template="showcase/islands_upload_state.html")
    async def islands_upload_state(request: Request) -> Template:
        return page(request, "showcase/islands_upload_state.html")

    @app.route("/streaming", template="showcase/streaming.html")
    async def streaming(request: Request) -> Template:
        return page(request, "showcase/streaming.html")

    @app.route("/message-turn", template="showcase/message_turn.html")
    async def message_turn(request: Request) -> Template:
        return page(request, "showcase/message_turn.html")

    @app.route("/composer", template="showcase/composer.html")
    async def composer_demo(request: Request) -> Template:
        return page(request, "showcase/composer.html")

    @app.route("/composer/send", methods=["POST"])
    async def composer_send(request: Request) -> Fragment:
        form = await request.form()
        message = (form.get("message") or "").strip() or "(empty)"
        return Fragment(
            "showcase/_composer_turn.html",
            "composer_turn",
            message=message,
        )

    @app.route("/composer/abort", methods=["POST"])
    async def composer_abort(request: Request) -> Response:
        return Response(status_code=204)

    @app.route("/composer/dismiss/{file_id}", methods=["POST"])
    async def composer_dismiss(request: Request, file_id: str) -> Response:
        return Response("", status_code=200)

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

    @app.route("/streaming/retry", methods=["GET"])
    async def streaming_retry(request: Request) -> Fragment:
        return Fragment("showcase/_streaming_retry.html", "retry_status")

    @app.route("/data/table", methods=["GET"])
    async def data_table(request: Request) -> Fragment:
        """Return table rows + pagination fragment for htmx-driven data page."""
        page_num = max(1, int(request.query.get("page", 1)))
        sort_col = request.query.get("sort", "name")
        sort_dir = request.query.get("dir", "asc")
        q = (request.query.get("q") or "").strip().lower()
        role = (request.query.get("role") or "").strip()
        density = request.query.get("density", "comfortable")

        sorted_data = filter_table_data(q, role, sort_col, sort_dir)

        total_rows = len(sorted_data)
        total_pages = max(1, (total_rows + PAGE_SIZE - 1) // PAGE_SIZE)
        page_num = min(page_num, total_pages)
        start = (page_num - 1) * PAGE_SIZE
        rows = sorted_data[start : start + PAGE_SIZE]
        start_row = start + 1 if total_rows else 0
        end_row = min(start + len(rows), total_rows)

        return Fragment(
            "showcase/_table_fragment.html",
            "table_content",
            rows=rows,
            page=page_num,
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
        selected = query_list(request, "selected")
        if not selected:
            return Fragment("showcase/_bulk_bar.html", "bulk_bar", count=0)
        return Fragment(
            "showcase/_bulk_bar.html", "bulk_bar", count=len(selected), selected=selected
        )

    @app.route("/data/export", methods=["GET"])
    async def data_export(request: Request) -> Response:
        """Export filtered table data as CSV. Use ?selected= to export only selected rows."""
        q = (request.query.get("q") or "").strip().lower()
        role = (request.query.get("role") or "").strip()
        sort_col = request.query.get("sort", "name")
        sort_dir = request.query.get("dir", "asc")
        selected = query_list(request, "selected")

        sorted_data = filter_table_data(q, role, sort_col, sort_dir)
        if selected:
            emails = set(selected)
            sorted_data = [row for row in sorted_data if row[1] in emails]

        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["Name", "Email", "Role", "Status", "Last active"])
        writer.writerows((row[0], row[1], row[2], row[3], row[4]) for row in sorted_data)
        body = buf.getvalue().encode("utf-8")

        return Response(body=body, content_type="text/csv; charset=utf-8").with_header(
            "Content-Disposition", 'attachment; filename="team-roster.csv"'
        )

    @app.route("/data", template="showcase/data.html")
    async def data(request: Request) -> Template:
        rows = filter_table_data("", "", "name", "asc")[:PAGE_SIZE]
        total_rows = len(TABLE_DATA)
        total_pages = max(1, (total_rows + PAGE_SIZE - 1) // PAGE_SIZE)
        return page(
            request,
            "showcase/data.html",
            rows=rows,
            page=1,
            total_pages=total_pages,
            total_rows=total_rows,
            start_row=1,
            end_row=len(rows),
            sort_col="name",
            sort_dir="asc",
            q="",
            role="",
            density="comfortable",
        )

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
