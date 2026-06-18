"""Operations shell fixture data and context builder."""

from __future__ import annotations

from urllib.parse import urlencode

from chirp import Request

OPS_AREAS: tuple[dict[str, str], ...] = (
    {"id": "edge", "label": "Edge", "icon": "ED"},
    {"id": "compute", "label": "Compute", "icon": "CP"},
    {"id": "data", "label": "Data", "icon": "DA"},
    {"id": "workflow", "label": "Workflow", "icon": "WF"},
)

OPS_WORKLOADS: tuple[dict[str, object], ...] = (
    {
        "id": "atlas-edge",
        "area": "edge",
        "name": "Atlas Edge",
        "status": "success",
        "owner": "Release",
        "region": "iad",
        "tier": "production",
        "latency": 42,
        "error_rate": "0.03%",
        "deploy": "2026.05.21",
        "summary": "Ingress and traffic shaping for the public workspace shell.",
        "tags": ("routing", "traffic", "cdn"),
        "events": ("Canary completed", "No active incidents", "Cache warmup stable"),
    },
    {
        "id": "forge-runners",
        "area": "compute",
        "name": "Forge Runners",
        "status": "warning",
        "owner": "Platform",
        "region": "ord",
        "tier": "production",
        "latency": 118,
        "error_rate": "0.41%",
        "deploy": "2026.05.20",
        "summary": "Elastic build runners with queue and secret-scope isolation.",
        "tags": ("queues", "runners", "deploy"),
        "events": (
            "Queue depth above target",
            "Runner image refresh pending",
            "Secrets audit clean",
        ),
    },
    {
        "id": "lakehouse-sync",
        "area": "data",
        "name": "Lakehouse Sync",
        "status": "success",
        "owner": "Data",
        "region": "dfw",
        "tier": "production",
        "latency": 76,
        "error_rate": "0.08%",
        "deploy": "2026.05.19",
        "summary": "Freshness pipeline for catalog, billing, and analytics records.",
        "tags": ("freshness", "schema", "pipelines"),
        "events": ("Backfill finished", "Freshness inside SLO", "Schema drift watcher idle"),
    },
    {
        "id": "relay-inbox",
        "area": "workflow",
        "name": "Relay Inbox",
        "status": "danger",
        "owner": "Operations",
        "region": "sfo",
        "tier": "critical",
        "latency": 244,
        "error_rate": "1.82%",
        "deploy": "2026.05.18",
        "summary": "Assignment, triage, and follow-up automation for team workflows.",
        "tags": ("automation", "approvals", "sla"),
        "events": ("Webhook retry storm", "SLA timer paused", "Escalation rule reviewed"),
    },
    {
        "id": "northstar-console",
        "area": "compute",
        "name": "Northstar Console",
        "status": "success",
        "owner": "Console",
        "region": "iad",
        "tier": "production",
        "latency": 64,
        "error_rate": "0.05%",
        "deploy": "2026.05.21",
        "summary": "Workspace and environment control plane for tenant operations.",
        "tags": ("workspaces", "governance", "permissions"),
        "events": ("Policy cache refreshed", "Permission audit clean", "No failed mutations"),
    },
)


def ops_url(
    *,
    q: str = "",
    area: str = "",
    status: str = "",
    workload: str = "",
    base_path: str = "/operations-shell",
) -> str:
    params = {
        key: value
        for key, value in {
            "q": q,
            "area": area,
            "status": status,
            "workload": workload,
        }.items()
        if value
    }
    return base_path + (f"?{urlencode(params)}" if params else "")


def ops_context(request: Request, *, base_path: str = "/operations-shell") -> dict[str, object]:
    q = (request.query.get("q") or "").strip().lower()
    area = (request.query.get("area") or "").strip()
    status = (request.query.get("status") or "").strip()
    workload = (request.query.get("workload") or "").strip()
    if area not in {item["id"] for item in OPS_AREAS}:
        area = ""
    if status not in {"success", "warning", "danger"}:
        status = ""

    def query_matches(item: dict[str, object]) -> bool:
        haystack = " ".join(
            [
                str(item["name"]),
                str(item["summary"]),
                str(item["owner"]),
                str(item["region"]),
                " ".join(str(tag) for tag in item["tags"]),
            ]
        ).lower()
        return not q or q in haystack

    def matches(item: dict[str, object]) -> bool:
        return (
            query_matches(item)
            and (not area or item["area"] == area)
            and (not status or item["status"] == status)
        )

    def view(item: dict[str, object]) -> dict[str, object]:
        status_id = str(item["status"])
        return {
            **item,
            "status_label": {
                "success": "Healthy",
                "warning": "Watch",
                "danger": "Incident",
            }[status_id],
            "status_variant": "error" if status_id == "danger" else status_id,
            "href": ops_url(
                q=q,
                area=area,
                status=status,
                workload=str(item["id"]),
                base_path=base_path,
            ),
        }

    filtered = [view(item) for item in OPS_WORKLOADS if matches(item)]
    selected = next((item for item in filtered if item["id"] == workload), None)
    if selected is None:
        selected = filtered[0] if filtered else view(OPS_WORKLOADS[0])

    status_items = []
    for status_id, label in (
        ("", "All states"),
        ("success", "Healthy"),
        ("warning", "Watch"),
        ("danger", "Incident"),
    ):
        count = sum(
            1
            for item in OPS_WORKLOADS
            if (not status_id or item["status"] == status_id)
            and (not area or item["area"] == area)
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

    area_items = []
    for item in OPS_AREAS:
        count = sum(
            1
            for workload_item in OPS_WORKLOADS
            if workload_item["area"] == item["id"]
            and (not status or workload_item["status"] == status)
            and query_matches(workload_item)
        )
        area_items.append(
            {
                **item,
                "active": area == item["id"],
                "count": count,
                "href": ops_url(q=q, area=str(item["id"]), status=status, base_path=base_path),
            }
        )

    active_area = next((item for item in OPS_AREAS if item["id"] == area), None)
    avg_latency = (
        round(sum(int(item["latency"]) for item in filtered) / len(filtered)) if filtered else 0
    )
    metrics = {
        "workloads": len(filtered),
        "watch": sum(1 for item in filtered if item["status"] == "warning"),
        "incidents": sum(1 for item in filtered if item["status"] == "danger"),
        "avg_latency": avg_latency,
        "regions": len({item["region"] for item in filtered}),
    }
    return {
        "ops_area": area,
        "ops_area_label": active_area["label"] if active_area else "All systems",
        "ops_areas": area_items,
        "ops_filtered": filtered,
        "ops_hints": [
            {
                "label": "latency",
                "href": ops_url(q="latency", area=area, status=status, base_path=base_path),
            },
            {
                "label": "deploy",
                "href": ops_url(q="deploy", area=area, status=status, base_path=base_path),
            },
            {
                "label": "queues",
                "href": ops_url(q="queues", area=area, status=status, base_path=base_path),
            },
            {
                "label": "freshness",
                "href": ops_url(q="freshness", area=area, status=status, base_path=base_path),
            },
        ],
        "ops_metrics": metrics,
        "ops_query": q,
        "ops_reset_href": base_path,
        "ops_route": base_path,
        "ops_selected": selected,
        "ops_status": status,
        "ops_status_items": status_items,
    }

