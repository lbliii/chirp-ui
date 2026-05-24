"""chirp-ui Component Showcase — spin up to see all components.

Requires: pip install -e ".[showcase]"
Run: python examples/component-showcase/app.py
"""

import asyncio
import calendar as cal_mod
import csv
import io
import re
from pathlib import Path
from urllib.parse import quote, urlencode

from chirp import (
    App,
    AppConfig,
    EventStream,
    FormAction,
    Fragment,
    Request,
    Response,
    ShellAction,
    ShellActions,
    ShellActionZone,
    SSEEvent,
    Template,
    ValidationError,
    use_chirp_ui,
)

from chirp_ui.theme_packs import get_theme_pack, list_theme_packs

TEMPLATES_DIR = Path(__file__).parent / "templates"

# Use source chirp-ui templates (many components not yet in installed package)
_CHIRPUI_SRC_TEMPLATES = Path(__file__).resolve().parents[2] / "src" / "chirp_ui" / "templates"

app = App(
    AppConfig(
        template_dir=TEMPLATES_DIR,
        debug=False,
        view_transitions=True,
        delegation=True,
        islands=True,
        component_dirs=(_CHIRPUI_SRC_TEMPLATES,) if _CHIRPUI_SRC_TEMPLATES.is_dir() else (),
    )
)
use_chirp_ui(app)


def _page(request: Request, template: str, **context: object) -> Template:
    """Render a full showcase page with route context for shell navigation."""
    context.setdefault("current_path", request.path)
    return Template(template, **context)


def _query_list(request: Request, key: str) -> list[str]:
    """Return repeated query values, accepting older comma-joined showcase links."""
    values = request.query.get_list(key)
    items: list[str] = []
    for value in values:
        items.extend(part.strip() for part in str(value).split(",") if part.strip())
    return items


@app.route("/toast", methods=["POST"])
async def show_toast(request: Request) -> Fragment:
    return Fragment("_toast.html", "toast_demo")


@app.route("/", template="index.html")
async def index(request: Request) -> Template:
    return _page(request, "index.html")


@app.route("/demo", template="showcase/demo.html")
async def demo(request: Request) -> Template:
    return _page(request, "showcase/demo.html")


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


@app.route("/htmx", template="showcase/htmx.html")
async def htmx_patterns(request: Request) -> Template:
    return _page(request, "showcase/htmx.html")


@app.route("/navigation", template="showcase/navigation.html")
async def navigation(request: Request) -> Template:
    return _page(request, "showcase/navigation.html")


CATALOG_CATEGORIES: tuple[dict[str, str], ...] = (
    {
        "id": "platform",
        "label": "Platform",
        "product_label": "Platform products",
        "icon": "PLT",
    },
    {
        "id": "intelligence",
        "label": "Intelligence",
        "product_label": "Search and AI products",
        "icon": "INT",
    },
    {
        "id": "data",
        "label": "Data",
        "product_label": "Data and analytics products",
        "icon": "DAT",
    },
    {
        "id": "workflow",
        "label": "Workflow",
        "product_label": "Automation and collaboration products",
        "icon": "WRK",
    },
    {
        "id": "operations",
        "label": "Operations",
        "product_label": "Reliability and administration products",
        "icon": "OPS",
    },
)


CATALOG_RECORDS: tuple[dict[str, object], ...] = (
    {
        "category": "platform",
        "family": "Core Platform",
        "product": "Northstar Console",
        "version": "latest",
        "docset": "User Guide",
        "title": "Plan a workspace model",
        "section": "Overview / Workspace model",
        "description": "Workspace, project, environment, and permission concepts for a multi-product platform.",
        "url": "/catalog-shell?doc=northstar-workspace-model",
        "content_type": "guide",
        "topics": ("workspaces", "permissions", "environments", "governance"),
        "product_category": "Platform",
    },
    {
        "category": "platform",
        "family": "Core Platform",
        "product": "Northstar Console",
        "version": "25.03",
        "docset": "API Reference",
        "title": "Workspace API fields",
        "section": "Reference / Workspace endpoints",
        "description": "Reference material for workspace creation, membership, environments, and audit metadata.",
        "url": "/catalog-shell?doc=northstar-workspace-api",
        "content_type": "reference",
        "topics": ("API", "workspace", "audit", "configuration"),
        "product_category": "Platform",
    },
    {
        "category": "platform",
        "family": "Developer Platform",
        "product": "Forge CI",
        "version": "latest",
        "docset": "Administration Guide",
        "title": "Operate build runners",
        "section": "Operations / Runner lifecycle",
        "description": "Runner pools, queues, cache policy, secret scopes, and build environment operations.",
        "url": "/catalog-shell?doc=forge-runner-lifecycle",
        "content_type": "how-to",
        "topics": ("CI", "runners", "secrets", "queues"),
        "product_category": "Developer tools",
    },
    {
        "category": "platform",
        "family": "Developer Platform",
        "product": "Launchpad",
        "version": "latest",
        "docset": "Installation Guide",
        "title": "Deploy a service template",
        "section": "Install / Service templates",
        "description": "Deployment guidance for template-backed services, preview environments, and release channels.",
        "url": "/catalog-shell?doc=launchpad-service-template",
        "content_type": "guide",
        "topics": ("deployment", "templates", "release channels", "platform engineering"),
        "product_category": "Developer tools",
    },
    {
        "category": "intelligence",
        "family": "Knowledge Systems",
        "product": "VectorLake",
        "version": "latest",
        "docset": "User Guide",
        "title": "Design a RAG workflow",
        "section": "Workflows / Retrieval augmented generation",
        "description": "Chunking, retrieval, evaluation, and deployment patterns for product knowledge systems.",
        "url": "/catalog-shell?doc=vectorlake-rag-workflow",
        "content_type": "tutorial",
        "topics": ("RAG", "retrieval", "evaluation", "deployment"),
        "product_category": "Knowledge AI",
    },
    {
        "category": "intelligence",
        "family": "Knowledge Systems",
        "product": "VectorLake",
        "version": "25.03",
        "docset": "API Reference",
        "title": "Retriever configuration",
        "section": "Reference / Retrieval profiles",
        "description": "API and configuration reference for indexes, retrievers, rerankers, and evaluation jobs.",
        "url": "/catalog-shell?doc=vectorlake-retriever-config",
        "content_type": "reference",
        "topics": ("retrieval", "indexes", "configuration", "evaluation"),
        "product_category": "Knowledge AI",
    },
    {
        "category": "intelligence",
        "family": "Assistants",
        "product": "PromptDeck",
        "version": "latest",
        "docset": "Quick Start",
        "title": "Ship an assistant prompt",
        "section": "Quick start / Assistant templates",
        "description": "Template deployment, tool policies, test fixtures, and production prompt review defaults.",
        "url": "/catalog-shell?doc=promptdeck-assistant-template",
        "content_type": "quickstart",
        "topics": ("prompts", "templates", "evaluation", "release review"),
        "product_category": "Knowledge AI",
    },
    {
        "category": "intelligence",
        "family": "Assistants",
        "product": "AnswerGraph",
        "version": "latest",
        "docset": "Best Practices",
        "title": "Tune answer quality",
        "section": "Quality / Citation coverage",
        "description": "Answer evaluation, citation coverage, fallback behavior, and source freshness practices.",
        "url": "/catalog-shell?doc=answergraph-quality",
        "content_type": "best-practices",
        "topics": ("answers", "citations", "quality", "freshness"),
        "product_category": "Knowledge AI",
    },
    {
        "category": "data",
        "family": "Data Pipelines",
        "product": "Streamline",
        "version": "latest",
        "docset": "Developer Guide",
        "title": "Build an ingestion pipeline",
        "section": "Pipelines / Streaming ingestion",
        "description": "Streaming ingestion, schema policy, retry queues, and backfill workflows.",
        "url": "/catalog-shell?doc=streamline-ingestion",
        "content_type": "guide",
        "topics": ("ingestion", "streaming", "schema", "backfill"),
        "product_category": "Data platform",
    },
    {
        "category": "data",
        "family": "Data Pipelines",
        "product": "Streamline",
        "version": "latest",
        "docset": "User Guide",
        "title": "Monitor pipeline health",
        "section": "Operations / Pipeline health",
        "description": "Run status, lag indicators, retry queues, and data freshness dashboards.",
        "url": "/catalog-shell?doc=streamline-health",
        "content_type": "guide",
        "topics": ("pipelines", "observability", "freshness", "retries"),
        "product_category": "Data platform",
    },
    {
        "category": "workflow",
        "family": "Team Workflows",
        "product": "Relay Inbox",
        "version": "latest",
        "docset": "Tutorials",
        "title": "Route incoming work",
        "section": "Tutorials / Assignment rules",
        "description": "Assignment rules, triage queues, service-level timers, and follow-up automation.",
        "url": "/catalog-shell?doc=relay-assignment-rules",
        "content_type": "tutorial",
        "topics": ("triage", "assignment", "automation", "SLAs"),
        "product_category": "Workflow",
    },
    {
        "category": "workflow",
        "family": "Team Workflows",
        "product": "CanvasFlow",
        "version": "latest",
        "docset": "Builder Guide",
        "title": "Compose an approval workflow",
        "section": "Builder / Approvals",
        "description": "Workflow stages, approvals, branch conditions, and audit history for operations teams.",
        "url": "/catalog-shell?doc=canvasflow-approvals",
        "content_type": "guide",
        "topics": ("approvals", "workflow builder", "audit", "automation"),
        "product_category": "Workflow",
    },
    {
        "category": "workflow",
        "family": "Messaging",
        "product": "Threadline",
        "version": "latest",
        "docset": "Best Practices",
        "title": "Design notification policies",
        "section": "Messaging / Notification policy",
        "description": "Digesting, priority rules, quiet hours, and escalation behavior for collaboration surfaces.",
        "url": "/catalog-shell?doc=threadline-notifications",
        "content_type": "best-practices",
        "topics": ("notifications", "digests", "priority", "collaboration"),
        "product_category": "Workflow",
    },
    {
        "category": "operations",
        "family": "Reliability",
        "product": "SignalDesk",
        "version": "latest",
        "docset": "Administration Guide",
        "title": "Operate incident rooms",
        "section": "Incidents / Response rooms",
        "description": "Incident response rooms, escalation policy, ownership, telemetry, and postmortem workflow.",
        "url": "/catalog-shell?doc=signaldesk-incidents",
        "content_type": "how-to",
        "topics": ("incidents", "telemetry", "ownership", "postmortems"),
        "product_category": "Operations",
    },
)


def _catalog_initials(label: str) -> str:
    words = [word for word in re.split(r"[^A-Za-z0-9]+", label) if word]
    if not words:
        return "*"
    return "".join(word[0].upper() for word in words[:3])


def _catalog_category_by_id(category_id: str) -> dict[str, str]:
    for category in CATALOG_CATEGORIES:
        if category["id"] == category_id:
            return category
    return {"id": "", "label": "All product areas", "product_label": "All products", "icon": "ALL"}


def _catalog_url(**params: object) -> str:
    clean = {key: str(value) for key, value in params.items() if value not in ("", None)}
    return "/catalog-shell" + (f"?{urlencode(clean)}" if clean else "")


def _catalog_matches(record: dict[str, object], query: str) -> bool:
    haystack = " ".join(
        [
            str(record["product"]),
            str(record["family"]),
            str(record["title"]),
            str(record["description"]),
            str(record["docset"]),
            str(record["content_type"]),
            " ".join(str(topic) for topic in record["topics"]),
        ]
    ).lower()
    return not query or query in haystack


def _top_values(records: list[dict[str, object]], key: str, limit: int) -> list[str]:
    counts: dict[str, int] = {}
    for record in records:
        raw = record[key]
        values = raw if isinstance(raw, tuple) else (raw,)
        for value in values:
            counts[str(value)] = counts.get(str(value), 0) + 1
    return [
        value
        for value, _count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]
    ]


def _catalog_context(request: Request) -> dict[str, object]:
    query = (request.query.get("q") or "").strip().lower()
    category = (request.query.get("category") or "").strip()
    family = (request.query.get("family") or "").strip()
    version = (request.query.get("version") or "latest").strip() or "latest"

    category_ids = {item["id"] for item in CATALOG_CATEGORIES}
    if category not in category_ids:
        category = ""

    category_records = [
        record for record in CATALOG_RECORDS if not category or record["category"] == category
    ]
    family_names = {str(record["family"]) for record in category_records}
    if family not in family_names:
        family = ""

    scoped_records = [
        record
        for record in category_records
        if (not family or record["family"] == family) and _catalog_matches(record, query)
    ]
    visible_records = [record for record in scoped_records if record["version"] == version]
    result_records = [record for record in CATALOG_RECORDS if _catalog_matches(record, query)]
    version_result_records = [record for record in result_records if record["version"] == version]
    category_visible_records = [
        record
        for record in category_records
        if _catalog_matches(record, query) and record["version"] == version
    ]

    categories = []
    for item in CATALOG_CATEGORIES:
        count = sum(1 for record in version_result_records if record["category"] == item["id"])
        categories.append(
            {
                **item,
                "count": count,
                "active": category == item["id"],
                "href": _catalog_url(q=query, category=item["id"], version="latest"),
            }
        )
    categories.insert(
        0,
        {
            "id": "",
            "label": "All product areas",
            "product_label": "All products",
            "icon": "ALL",
            "count": len(version_result_records),
            "active": not category,
            "href": _catalog_url(q=query, version="latest"),
        },
    )

    family_groups: dict[str, list[dict[str, object]]] = {}
    for record in category_visible_records:
        family_groups.setdefault(str(record["family"]), []).append(record)
    families = [
        {
            "name": name,
            "initials": _catalog_initials(name),
            "product_count": len({str(record["product"]) for record in records}),
            "record_count": len(records),
            "active": family == name,
            "href": _catalog_url(q=query, category=category, family=name, version="latest"),
        }
        for name, records in sorted(
            family_groups.items(), key=lambda item: (-len(item[1]), item[0])
        )
    ]

    product_groups: dict[str, list[dict[str, object]]] = {}
    for record in visible_records:
        product_groups.setdefault(str(record["product"]), []).append(record)

    products = []
    for product, records in sorted(
        product_groups.items(), key=lambda item: (-len(item[1]), item[0])
    ):
        first = records[0]
        docsets = _top_values(records, "docset", 6)
        content_types = _top_values(records, "content_type", 4)
        topics = _top_values(records, "topics", 4)
        products.append(
            {
                "name": product,
                "mark": _catalog_initials(product),
                "href": first["url"],
                "family": first["family"],
                "site": "docs.example.local",
                "record_count": len(records),
                "docsets": docsets,
                "content_types": content_types,
                "topics": [{"label": topic, "href": _catalog_url(q=topic)} for topic in topics],
                "summary": str(first["description"])
                if len(records) == 1
                else f"{len(records)} docs in {version} across {len(docsets)} docsets.",
                "links": [
                    {
                        "href": record["url"],
                        "docset": record["docset"],
                        "title": record["title"],
                        "label": record["section"],
                    }
                    for record in records[:5]
                ],
            }
        )

    selected_category = _catalog_category_by_id(category)
    versions = _top_values(scoped_records, "version", 8) or ["latest"]
    versions = sorted(versions, key=lambda item: (item != "latest", item), reverse=False)
    reset_href = _catalog_url()
    return {
        "catalog_categories": categories,
        "catalog_families": families,
        "catalog_products": products,
        "catalog_query": query,
        "catalog_category": category,
        "catalog_family": family,
        "catalog_version": version,
        "catalog_selected_category": selected_category,
        "catalog_versions": [
            {
                "label": item,
                "active": item == version,
                "href": _catalog_url(q=query, category=category, family=family, version=item),
            }
            for item in versions
        ],
        "catalog_all_families_href": _catalog_url(q=query, category=category, version="latest"),
        "catalog_all_families_record_count": len(category_visible_records),
        "catalog_metrics": {
            "products": len({str(record["product"]) for record in visible_records}),
            "docsets": len({str(record["docset"]) for record in visible_records}),
            "records": len(visible_records),
            "scope_label": family or selected_category["product_label"],
            "top_categories": _top_values(visible_records, "product_category", 3),
            "top_topics": [
                {"label": topic, "href": _catalog_url(q=topic)}
                for topic in _top_values(visible_records, "topics", 8)
            ],
        },
        "catalog_search_hints": [
            {
                "label": "RAG",
                "query": "rag",
                "href": _catalog_url(q="rag", category=category, family=family),
            },
            {
                "label": "deployment",
                "query": "deployment",
                "href": _catalog_url(q="deployment", category=category, family=family),
            },
            {
                "label": "API reference",
                "query": "api reference",
                "href": _catalog_url(q="api reference", category=category, family=family),
            },
            {
                "label": "Kubernetes",
                "query": "kubernetes",
                "href": _catalog_url(q="kubernetes", category=category, family=family),
            },
            {
                "label": "performance",
                "query": "performance",
                "href": _catalog_url(q="performance", category=category, family=family),
            },
        ],
        "catalog_reset_href": reset_href,
    }


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


def _ops_url(
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


def _ops_context(request: Request, *, base_path: str = "/operations-shell") -> dict[str, object]:
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
            "href": _ops_url(
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
                "href": _ops_url(q=q, area=str(item["id"]), status=status, base_path=base_path),
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
                "href": _ops_url(q="latency", area=area, status=status, base_path=base_path),
            },
            {
                "label": "deploy",
                "href": _ops_url(q="deploy", area=area, status=status, base_path=base_path),
            },
            {
                "label": "queues",
                "href": _ops_url(q="queues", area=area, status=status, base_path=base_path),
            },
            {
                "label": "freshness",
                "href": _ops_url(q="freshness", area=area, status=status, base_path=base_path),
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


def _support_url(
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


def _support_context(request: Request, *, base_path: str = "/support-shell") -> dict[str, object]:
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
            "href": _support_url(
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
                "href": _support_url(
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
                "href": _support_url(
                    q="latency", queue=queue, status=status, base_path=base_path
                ),
            },
            {
                "label": "invoice",
                "href": _support_url(
                    q="invoice", queue=queue, status=status, base_path=base_path
                ),
            },
            {
                "label": "migration",
                "href": _support_url(
                    q="migration", queue=queue, status=status, base_path=base_path
                ),
            },
            {
                "label": "webhooks",
                "href": _support_url(
                    q="webhooks", queue=queue, status=status, base_path=base_path
                ),
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


@app.route("/catalog-shell", template="showcase/catalog_shell.html")
async def catalog_shell(request: Request) -> Template:
    return _page(request, "showcase/catalog_shell.html", **_catalog_context(request))


@app.route("/operations-shell", template="showcase/operations_shell.html")
async def operations_shell(request: Request) -> Template:
    return _page(request, "showcase/operations_shell.html", **_ops_context(request))


@app.route("/operations-shell-workspace", template="showcase/operations_shell_workspace.html")
async def operations_shell_workspace(request: Request) -> Template:
    return _page(
        request,
        "showcase/operations_shell_workspace.html",
        **_ops_context(request, base_path="/operations-shell-workspace"),
    )


@app.route("/support-shell", template="showcase/support_shell.html")
async def support_shell(request: Request) -> Template:
    return _page(request, "showcase/support_shell.html", **_support_context(request))


@app.route("/screen-command-center", template="showcase/operations_shell.html")
async def screen_command_center(request: Request) -> Template:
    return _page(
        request,
        "showcase/operations_shell.html",
        **_ops_context(request, base_path="/screen-command-center"),
        ops_screen_title="Golden screen: Command Center",
        ops_screen_subtitle=(
            "Atlas profile fixture for metrics, queues, incidents, activity, "
            "and selected-object inspection."
        ),
        ops_screen_archetype="command-center",
        ops_screen_profile="atlas",
    )


@app.route("/screen-review-queue", template="showcase/support_shell.html")
async def screen_review_queue(request: Request) -> Template:
    return _page(
        request,
        "showcase/support_shell.html",
        **_support_context(request, base_path="/screen-review-queue"),
        support_screen_title="Golden screen: Review Queue",
        support_screen_subtitle=(
            "Sage profile fixture for filter rail, result collection, inspector, "
            "stateful tickets, and batch-ready review work."
        ),
        support_screen_archetype="review-queue",
        support_screen_profile="sage",
    )


@app.route("/layout", template="showcase/layout.html")
async def layout(request: Request) -> Template:
    direction = request.query.get("dir", "ltr")
    if direction not in {"ltr", "rtl"}:
        direction = "ltr"
    return _page(request, "showcase/layout.html", direction=direction)


@app.route("/chrome", template="showcase/chrome.html")
async def chrome(request: Request) -> Template:
    return _page(request, "showcase/chrome.html")


@app.route("/shell-actions", template="showcase/shell_actions.html")
async def shell_actions(request: Request) -> Template:
    actions = ShellActions(
        primary=ShellActionZone(
            items=(
                ShellAction(
                    id="new-thread",
                    label="New thread",
                    href="/forms",
                    variant="primary",
                ),
            )
        ),
        controls=ShellActionZone(
            items=(
                ShellAction(id="sort", label="Latest", href="/data", variant="default"),
                ShellAction(id="watch", label="Watch", action="watch-thread", variant="secondary"),
            )
        ),
        overflow=ShellActionZone(
            items=(
                ShellAction(id="share", label="Share", href="/social"),
                ShellAction(id="archive", label="Archive", action="archive-thread"),
            )
        ),
    )
    return _page(request, "showcase/shell_actions.html", shell_actions=actions)


@app.route("/sections", template="showcase/sections.html")
async def sections(request: Request) -> Template:
    return _page(request, "showcase/sections.html")


@app.route("/layout/dir", methods=["GET"])
async def layout_dir(request: Request) -> Fragment:
    """Return Fragment with dir block for RTL/LTR toggle."""
    direction = request.query.get("dir", "ltr")
    return Fragment("showcase/_layout_dir.html", "dir_block", direction=direction)


@app.route("/carousel", template="showcase/carousel.html")
async def carousel_page(request: Request) -> Template:
    return _page(request, "showcase/carousel.html")


@app.route("/cards", template="showcase/cards.html")
async def cards(request: Request) -> Template:
    return _page(request, "showcase/cards.html")


@app.route("/forms", template="showcase/forms.html")
async def forms(request: Request) -> Template:
    return _page(request, "showcase/forms.html")


@app.route("/appearance-tone", template="showcase/appearance-tone.html")
async def appearance_tone(request: Request) -> Template:
    return _page(request, "showcase/appearance-tone.html")


@app.route("/theme-packs", template="showcase/theme-packs.html")
async def theme_packs(request: Request) -> Template:
    return _page(request, "showcase/theme-packs.html", theme_packs=list_theme_packs())


@app.route("/theme-packs/preview/{name}/{mode}", template="showcase/theme_pack_preview.html")
async def theme_pack_preview(request: Request, name: str, mode: str) -> Template | Response:
    pack = get_theme_pack(name)
    if pack is None or mode not in pack.modes:
        return Response("Theme pack preview not found", status=404)
    return Template("showcase/theme_pack_preview.html", pack=pack, mode=mode)


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
async def ui(request: Request) -> Template:
    return _page(request, "showcase/ui.html")


@app.route("/ui/tab/{name}", methods=["GET"])
async def ui_tab(request: Request, name: str) -> Fragment:
    return Fragment("showcase/_tab_content.html", "tab_content", active_tab=name)


@app.route("/islands", template="showcase/islands.html")
async def islands_demo(request: Request) -> Template:
    return _page(request, "showcase/islands.html")


@app.route("/islands/remount", methods=["GET"])
async def islands_remount() -> Fragment:
    return Fragment("showcase/islands.html", "island_mount")


@app.route("/islands/grid-state", template="showcase/islands_grid_state.html")
async def islands_grid_state(request: Request) -> Template:
    return _page(request, "showcase/islands_grid_state.html")


@app.route("/islands/wizard-state", template="showcase/islands_wizard_state.html")
async def islands_wizard_state(request: Request) -> Template:
    return _page(request, "showcase/islands_wizard_state.html")


@app.route("/islands/upload-state", template="showcase/islands_upload_state.html")
async def islands_upload_state(request: Request) -> Template:
    return _page(request, "showcase/islands_upload_state.html")


@app.route("/streaming", template="showcase/streaming.html")
async def streaming(request: Request) -> Template:
    return _page(request, "showcase/streaming.html")


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
    selected = _query_list(request, "selected")
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
    selected = _query_list(request, "selected")

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
async def data_display(request: Request) -> Template:
    return _page(request, "showcase/data-display.html")


@app.route("/calendar", template="showcase/calendar.html")
@app.route("/calendar/{year}/{month}", template="showcase/calendar.html")
async def calendar_view(
    request: Request,
    year: int | str | None = None,
    month: int | str | None = None,
) -> Template:
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
    return _page(
        request,
        "showcase/calendar.html",
        weeks=weeks,
        month_label=month_label,
        prev_url=prev_url,
        next_url=next_url,
    )


@app.route("/data", template="showcase/data.html")
async def data(request: Request) -> Template:
    rows = _filter_table_data("", "", "name", "asc")[:PAGE_SIZE]
    total_rows = len(TABLE_DATA)
    total_pages = max(1, (total_rows + PAGE_SIZE - 1) // PAGE_SIZE)
    return _page(
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


@app.route("/effects", template="showcase/effects.html")
async def effects(request: Request) -> Template:
    return _page(request, "showcase/effects.html")


@app.route("/typography", template="showcase/typography.html")
async def typography(request: Request) -> Template:
    return _page(request, "showcase/typography.html")


@app.route("/ascii-primitives", template="showcase/ascii_primitives.html")
async def ascii_primitives(request: Request) -> Template:
    return _page(request, "showcase/ascii_primitives.html")


@app.route("/buttons", template="showcase/buttons.html")
async def buttons(request: Request) -> Template:
    return _page(request, "showcase/buttons.html")


@app.route("/dashboard", template="showcase/dashboard.html")
async def dashboard(request: Request) -> Template:
    return _page(request, "showcase/dashboard.html")


@app.route("/animation", template="showcase/animation.html")
async def animation(request: Request) -> Template:
    return _page(request, "showcase/animation.html")


@app.route("/ascii", template="showcase/ascii.html")
async def ascii_icons(request: Request) -> Template:
    return _page(request, "showcase/ascii.html")


@app.route("/animation/swap-demo", methods=["GET"])
async def animation_swap_demo(request: Request) -> Fragment:
    return Fragment("showcase/_swap_content.html", "swap_demo")


@app.route("/messenger", template="showcase/messenger.html")
async def messenger(request: Request) -> Template:
    return _page(request, "showcase/messenger.html")


@app.route("/social", template="showcase/social.html")
async def social(request: Request) -> Template:
    return _page(request, "showcase/social.html")


@app.route("/video", template="showcase/video.html")
async def video(request: Request) -> Template:
    return _page(request, "showcase/video.html")


if __name__ == "__main__":
    app.run()
