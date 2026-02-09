# MCP Server Module

This folder will contain the MCP (Machine Control Protocol) implementation for Todo operations.

## Structure
- `tools.py`: Contains `@mcp.tool` definitions for `add_task`, `list_tasks`, etc.
- `server.py`: Sets up the `FastMCP` instance and registers tools.

## Integration
1. In `backend/app/main.py` or `dependencies.py`, import this module to ensure tools are registered.
2. The Agent will use `mcp_client.call_tool` referencing these tool names.
