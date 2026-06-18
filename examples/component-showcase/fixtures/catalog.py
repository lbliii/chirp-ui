"""Catalog shell fixture data and context builder."""

from __future__ import annotations

import re
from urllib.parse import urlencode

from chirp import Request

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


def catalog_initials(label: str) -> str:
    words = [word for word in re.split(r"[^A-Za-z0-9]+", label) if word]
    if not words:
        return "*"
    return "".join(word[0].upper() for word in words[:3])


def catalog_category_by_id(category_id: str) -> dict[str, str]:
    for category in CATALOG_CATEGORIES:
        if category["id"] == category_id:
            return category
    return {"id": "", "label": "All product areas", "product_label": "All products", "icon": "ALL"}


def catalog_url(**params: object) -> str:
    clean = {key: str(value) for key, value in params.items() if value not in ("", None)}
    return "/catalog-shell" + (f"?{urlencode(clean)}" if clean else "")


def catalog_matches(record: dict[str, object], query: str) -> bool:
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


def top_values(records: list[dict[str, object]], key: str, limit: int) -> list[str]:
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


def catalog_context(request: Request) -> dict[str, object]:
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
        if (not family or record["family"] == family) and catalog_matches(record, query)
    ]
    visible_records = [record for record in scoped_records if record["version"] == version]
    result_records = [record for record in CATALOG_RECORDS if catalog_matches(record, query)]
    version_result_records = [record for record in result_records if record["version"] == version]
    category_visible_records = [
        record
        for record in category_records
        if catalog_matches(record, query) and record["version"] == version
    ]

    categories = []
    for item in CATALOG_CATEGORIES:
        count = sum(1 for record in version_result_records if record["category"] == item["id"])
        categories.append(
            {
                **item,
                "count": count,
                "active": category == item["id"],
                "href": catalog_url(q=query, category=item["id"], version="latest"),
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
            "href": catalog_url(q=query, version="latest"),
        },
    )

    family_groups: dict[str, list[dict[str, object]]] = {}
    for record in category_visible_records:
        family_groups.setdefault(str(record["family"]), []).append(record)
    families = [
        {
            "name": name,
            "initials": catalog_initials(name),
            "product_count": len({str(record["product"]) for record in records}),
            "record_count": len(records),
            "active": family == name,
            "href": catalog_url(q=query, category=category, family=name, version="latest"),
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
        docsets = top_values(records, "docset", 6)
        content_types = top_values(records, "content_type", 4)
        topics = top_values(records, "topics", 4)
        products.append(
            {
                "name": product,
                "mark": catalog_initials(product),
                "href": first["url"],
                "family": first["family"],
                "site": "docs.example.local",
                "record_count": len(records),
                "docsets": docsets,
                "content_types": content_types,
                "topics": [{"label": topic, "href": catalog_url(q=topic)} for topic in topics],
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

    selected_category = catalog_category_by_id(category)
    versions = top_values(scoped_records, "version", 8) or ["latest"]
    versions = sorted(versions, key=lambda item: (item != "latest", item), reverse=False)
    reset_href = catalog_url()
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
                "href": catalog_url(q=query, category=category, family=family, version=item),
            }
            for item in versions
        ],
        "catalog_all_families_href": catalog_url(q=query, category=category, version="latest"),
        "catalog_all_families_record_count": len(category_visible_records),
        "catalog_metrics": {
            "products": len({str(record["product"]) for record in visible_records}),
            "docsets": len({str(record["docset"]) for record in visible_records}),
            "records": len(visible_records),
            "scope_label": family or selected_category["product_label"],
            "top_categories": top_values(visible_records, "product_category", 3),
            "top_topics": [
                {"label": topic, "href": catalog_url(q=topic)}
                for topic in top_values(visible_records, "topics", 8)
            ],
        },
        "catalog_search_hints": [
            {
                "label": "RAG",
                "query": "rag",
                "href": catalog_url(q="rag", category=category, family=family),
            },
            {
                "label": "deployment",
                "query": "deployment",
                "href": catalog_url(q="deployment", category=category, family=family),
            },
            {
                "label": "API reference",
                "query": "api reference",
                "href": catalog_url(q="api reference", category=category, family=family),
            },
            {
                "label": "Kubernetes",
                "query": "kubernetes",
                "href": catalog_url(q="kubernetes", category=category, family=family),
            },
            {
                "label": "performance",
                "query": "performance",
                "href": catalog_url(q="performance", category=category, family=family),
            },
        ],
        "catalog_reset_href": reset_href,
    }
