"""MCP server over the chirp-ui manifest — agent-native registry distribution.

Requires the optional ``mcp`` extra::

    pip install "chirp-ui[mcp]"
    chirp-ui mcp

Tools expose the same manifest surface as ``chirp-ui find``, backed by the
shipped ``manifest.json`` so the MCP contract cannot drift from the package.
"""

from __future__ import annotations

import argparse
import json
from typing import Any

from chirp_ui import load_manifest
from chirp_ui.find import detailed_search, search


def _require_mcp():
    try:
        import mcp.server.stdio
        import mcp.types
        from mcp.server import Server
    except ImportError as exc:  # pragma: no cover - exercised via import guard test
        raise SystemExit(
            "chirp-ui MCP server requires the optional mcp dependency.\n"
            'Install with: pip install "chirp-ui[mcp]"\n'
        ) from exc
    return Server, mcp.types, mcp.server.stdio


def _tool_result(payload: Any) -> list[Any]:
    _server_cls, mcp_types, _stdio = _require_mcp()
    return [
        mcp_types.TextContent(type="text", text=json.dumps(payload, indent=2, ensure_ascii=True))
    ]


def create_server():
    """Build and return the configured MCP server instance."""
    server_cls, mcp_types, _stdio = _require_mcp()
    server = server_cls("chirp-ui")

    @server.list_tools()
    async def list_tools() -> list[Any]:
        return [
            mcp_types.Tool(
                name="find_components",
                description=(
                    "Search public chirp-ui components by substring across name, "
                    "category, and description. Supports category/authoring/maturity/role filters."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "default": ""},
                        "category": {"type": "string"},
                        "authoring": {"type": "string"},
                        "maturity": {"type": "string"},
                        "role": {"type": "string"},
                        "details": {"type": "boolean", "default": False},
                    },
                },
            ),
            mcp_types.Tool(
                name="get_component",
                description="Return the full manifest entry for one component by name.",
                inputSchema={
                    "type": "object",
                    "properties": {"name": {"type": "string"}},
                    "required": ["name"],
                },
            ),
            mcp_types.Tool(
                name="list_categories",
                description="List manifest categories with public component counts.",
                inputSchema={"type": "object", "properties": {}},
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[Any]:
        manifest = load_manifest()
        if name == "find_components":
            query = str(arguments.get("query") or "")
            details = bool(arguments.get("details"))
            category = arguments.get("category")
            authoring = arguments.get("authoring")
            maturity = arguments.get("maturity")
            role = arguments.get("role")
            if details:
                rows = detailed_search(
                    manifest,
                    query,
                    category=category,
                    authoring=authoring,
                    maturity=maturity,
                    role=role,
                )
                payload = [
                    {
                        "name": row[0],
                        "category": row[1],
                        "maturity": row[2],
                        "authoring": row[3],
                        "role": row[4],
                        "macro": row[5],
                        "template": row[6],
                        "runtime": row[7],
                        "slots": row[8],
                        "summary": row[9],
                    }
                    for row in rows
                ]
            else:
                rows = search(
                    manifest,
                    query,
                    category=category,
                    authoring=authoring,
                    maturity=maturity,
                    role=role,
                )
                payload = [{"name": row[0], "category": row[1], "summary": row[2]} for row in rows]
            return _tool_result({"count": len(payload), "results": payload})

        if name == "get_component":
            component_name = str(arguments.get("name") or "").strip()
            components = manifest.get("components", {})
            entry = components.get(component_name)
            if entry is None:
                return _tool_result({"error": f"unknown component: {component_name!r}"})
            return _tool_result({"name": component_name, **entry})

        if name == "list_categories":
            counts: dict[str, int] = {}
            for entry in manifest.get("components", {}).values():
                if entry.get("maturity") == "internal" or entry.get("authoring") == "internal":
                    continue
                category = entry.get("category") or "uncategorized"
                counts[category] = counts.get(category, 0) + 1
            payload = [
                {"category": category, "count": counts[category]} for category in sorted(counts)
            ]
            return _tool_result({"count": len(payload), "categories": payload})

        return _tool_result({"error": f"unknown tool: {name!r}"})

    return server, _stdio


async def _run_stdio() -> None:
    server, stdio = create_server()
    async with stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="chirp-ui mcp",
        description="Run the chirp-ui manifest MCP server (stdio transport).",
    )
    parser.parse_args(argv)
    import asyncio

    asyncio.run(_run_stdio())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
