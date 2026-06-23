"""Tests for the chirp-ui manifest MCP server."""

from __future__ import annotations

import pytest

pytest.importorskip("mcp")
import mcp.types

from chirp_ui import load_manifest
from chirp_ui.find import search
from chirp_ui.mcp_server import create_server


def test_create_server_registers_expected_tools() -> None:
    server, _stdio = create_server()
    assert server.name == "chirp-ui"


@pytest.mark.asyncio
async def test_find_components_tool_returns_manifest_backed_results() -> None:
    server, _stdio = create_server()
    handlers = server.request_handlers
    list_tools = handlers[mcp.types.ListToolsRequest]
    tools = await list_tools(None)
    tool_names = {tool.name for tool in tools.root.tools}
    assert {"find_components", "get_component", "list_categories"} <= tool_names

    call_tool = handlers[mcp.types.CallToolRequest]
    result = await call_tool(
        mcp.types.CallToolRequest(
            method="tools/call",
            params=mcp.types.CallToolRequestParams(
                name="find_components", arguments={"query": "badge"}
            ),
        )
    )
    call_result = result.root
    assert not call_result.isError
    assert call_result.content
    text = call_result.content[0].text
    assert "badge" in text

    manifest = load_manifest()
    expected = search(manifest, "badge")
    assert str(len(expected)) in text


@pytest.mark.asyncio
async def test_get_component_tool_returns_full_entry() -> None:
    server, _stdio = create_server()
    call_tool = server.request_handlers[mcp.types.CallToolRequest]
    result = await call_tool(
        mcp.types.CallToolRequest(
            method="tools/call",
            params=mcp.types.CallToolRequestParams(
                name="get_component", arguments={"name": "badge"}
            ),
        )
    )
    call_result = result.root
    assert not call_result.isError
    assert '"block": "badge"' in call_result.content[0].text


@pytest.mark.asyncio
async def test_list_categories_tool_counts_public_components() -> None:
    server, _stdio = create_server()
    call_tool = server.request_handlers[mcp.types.CallToolRequest]
    result = await call_tool(
        mcp.types.CallToolRequest(
            method="tools/call",
            params=mcp.types.CallToolRequestParams(name="list_categories", arguments={}),
        )
    )
    call_result = result.root
    assert not call_result.isError
    assert '"category"' in call_result.content[0].text
