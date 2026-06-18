"""Support shell fixture data and context builder."""

from __future__ import annotations

from urllib.parse import urlencode

from chirp import Request

SUPPORT_QUEUES: tuple[dict[str, str], ...] = (
    {"id": "priority", "label": "Priority", "icon": "P1"},
    {"id": "billing", "label": "Billing", "icon": "BI"},
    {"id": "product", "label": "Product", "icon": "PR"},
    {"id": "success", "label": "Success", "icon": "CS"},
)

SUPPORT_TICKETS: tuple[dict[str, object], ...] = (
    {
        "id": "t-1042",
        "queue": "priority",
        "customer": "Acme Robotics",
        "subject": "Deployment webhook retries block launch",
        "status": "danger",
        "owner": "Maya",
        "age": "18m",
        "plan": "Enterprise",
        "score": 96,
        "summary": "Webhook retries are holding a launch checklist and need a platform review.",
        "tags": ("webhooks", "deployment", "launch"),
        "timeline": (
            "Customer escalated launch risk",
            "Retries reproduced",
            "Platform owner paged",
        ),
    },
    {
        "id": "t-1043",
        "queue": "billing",
        "customer": "Northwind Labs",
        "subject": "Invoice export missing regional tax rows",
        "status": "warning",
        "owner": "Iris",
        "age": "1h",
        "plan": "Scale",
        "score": 74,
        "summary": "Finance export does not include regional tax rows for the current cycle.",
        "tags": ("invoice", "export", "tax"),
        "timeline": ("CSV sample attached", "Billing job inspected", "Tax mapping review queued"),
    },
    {
        "id": "t-1044",
        "queue": "product",
        "customer": "Helio Foods",
        "subject": "Saved views should include team filters",
        "status": "success",
        "owner": "Noah",
        "age": "3h",
        "plan": "Business",
        "score": 52,
        "summary": "Product feedback about team-scoped saved views and dashboard defaults.",
        "tags": ("saved views", "filters", "dashboard"),
        "timeline": ("Feedback grouped", "Design review linked", "No response needed today"),
    },
    {
        "id": "t-1045",
        "queue": "success",
        "customer": "BrightPath Health",
        "subject": "Migration workspace readiness check",
        "status": "warning",
        "owner": "Sana",
        "age": "42m",
        "plan": "Enterprise",
        "score": 81,
        "summary": "Success team needs readiness signals before a workspace migration call.",
        "tags": ("migration", "readiness", "workspace"),
        "timeline": ("Checklist generated", "Two blockers remain", "Call scheduled"),
    },
    {
        "id": "t-1046",
        "queue": "priority",
        "customer": "VectorShop",
        "subject": "Search latency above support threshold",
        "status": "danger",
        "owner": "Theo",
        "age": "9m",
        "plan": "Enterprise",
        "score": 92,
        "summary": "Search response latency crosses the contractual support threshold.",
        "tags": ("latency", "search", "sla"),
        "timeline": ("Latency alert fired", "Trace bundle attached", "Search team acknowledged"),
    },
)


def support_url(
    *,
    q: str = "",
    queue: str = "",
    status: str = "",
    ticket: str = "",
    base_path: str = "/support-shell",
) -> str:
    params = {
        key: value
        for key, value in {
            "q": q,
            "queue": queue,
            "status": status,
            "ticket": ticket,
        }.items()
        if value
    }
    return base_path + (f"?{urlencode(params)}" if params else "")


def support_context(request: Request, *, base_path: str = "/support-shell") -> dict[str, object]:
    q = (request.query.get("q") or "").strip().lower()
    queue = (request.query.get("queue") or "").strip()
    status = (request.query.get("status") or "").strip()
    ticket = (request.query.get("ticket") or "").strip()
    if queue not in {item["id"] for item in SUPPORT_QUEUES}:
        queue = ""
    if status not in {"success", "warning", "danger"}:
        status = ""

    def query_matches(item: dict[str, object]) -> bool:
        haystack = " ".join(
            [
                str(item["customer"]),
                str(item["subject"]),
                str(item["summary"]),
                str(item["owner"]),
                " ".join(str(tag) for tag in item["tags"]),
            ]
        ).lower()
        return not q or q in haystack

    def matches(item: dict[str, object]) -> bool:
        return (
            query_matches(item)
            and (not queue or item["queue"] == queue)
            and (not status or item["status"] == status)
        )

    def view(item: dict[str, object]) -> dict[str, object]:
        status_id = str(item["status"])
        return {
            **item,
            "status_label": {
                "success": "Ready",
                "warning": "Needs reply",
                "danger": "Escalated",
            }[status_id],
            "status_variant": "error" if status_id == "danger" else status_id,
            "href": support_url(
                q=q,
                queue=queue,
                status=status,
                ticket=str(item["id"]),
                base_path=base_path,
            ),
        }

    filtered = [view(item) for item in SUPPORT_TICKETS if matches(item)]
    selected = next((item for item in filtered if item["id"] == ticket), None)
    if selected is None:
        selected = filtered[0] if filtered else view(SUPPORT_TICKETS[0])

    queue_items = []
    for item in SUPPORT_QUEUES:
        count = sum(
            1
            for ticket_item in SUPPORT_TICKETS
            if ticket_item["queue"] == item["id"]
            and (not status or ticket_item["status"] == status)
            and query_matches(ticket_item)
        )
        queue_items.append(
            {
                **item,
                "active": queue == item["id"],
                "count": count,
                "href": support_url(
                    q=q,
                    queue=str(item["id"]),
                    status=status,
                    base_path=base_path,
                ),
            }
        )

    status_items = []
    for status_id, label in (
        ("", "All states"),
        ("danger", "Escalated"),
        ("warning", "Needs reply"),
        ("success", "Ready"),
    ):
        count = sum(
            1
            for item in SUPPORT_TICKETS
            if (not status_id or item["status"] == status_id)
            and (not queue or item["queue"] == queue)
            and query_matches(item)
        )
        status_items.append(
            {
                "id": status_id,
                "label": label,
                "active": status == status_id,
                "count": count,
            }
        )

    active_queue = next((item for item in SUPPORT_QUEUES if item["id"] == queue), None)
    metrics = {
        "tickets": len(filtered),
        "escalated": sum(1 for item in filtered if item["status"] == "danger"),
        "waiting": sum(1 for item in filtered if item["status"] == "warning"),
        "avg_score": round(sum(int(item["score"]) for item in filtered) / len(filtered))
        if filtered
        else 0,
    }
    return {
        "support_filtered": filtered,
        "support_hints": [
            {
                "label": "latency",
                "href": support_url(q="latency", queue=queue, status=status, base_path=base_path),
            },
            {
                "label": "invoice",
                "href": support_url(q="invoice", queue=queue, status=status, base_path=base_path),
            },
            {
                "label": "migration",
                "href": support_url(q="migration", queue=queue, status=status, base_path=base_path),
            },
            {
                "label": "webhooks",
                "href": support_url(q="webhooks", queue=queue, status=status, base_path=base_path),
            },
        ],
        "support_metrics": metrics,
        "support_query": q,
        "support_queue": queue,
        "support_queue_label": active_queue["label"] if active_queue else "All queues",
        "support_queues": queue_items,
        "support_reset_href": base_path,
        "support_route": base_path,
        "support_selected": selected,
        "support_status": status,
        "support_status_items": status_items,
    }
