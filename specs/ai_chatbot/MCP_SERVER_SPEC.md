# MCP Server Specification (Internal Module)

## Overview
The "MCP Server" will be implemented as an internal Python module within the existing FastAPI backend (`backend/app/mcp`). It leverages the official MCP Python SDK (`mcp-python`) to expose existing Todo CRUD operations as tools for the AI agent.

Instead of running a separate process, we instantiate an MCP Server object within the `FastAPI` application context (or simply use the MCP SDK types directly if preferred for a monolithic app).

## Server Configuration
- **Name**: `todo-mcp-server`
- **Transport**: `stdio` (if run as separate process) or direct function calls (if integrated).
- **Dependencies**: `mcp-python`, `fastapi`, `sqlmodel`.

## Tool Definitions (Python)

```python
# app/mcp/tools.py

from mcp.server.fastmcp import FastMCP
from typing import Optional
from app.models import Task, User
from app.routes.tasks import create_task_logic, list_tasks_logic # Abstract logic needed

mcp = FastMCP("todo-server")

@mcp.tool()
def add_task(title: str, description: str = "", priority: str = "medium") -> str:
    """Create a new task."""
    # Logic to interact with DB using dependency injection or context
    # ...
    return f"Task '{title}' created with ID {new_task.id}"

@mcp.tool()
def list_tasks(status: Optional[str] = None) -> str:
    """List tasks, optionally filtered by status ('completed', 'pending')."""
    # ...
    return json.dumps(tasks_list)

@mcp.tool()
def update_task(task_id: int, title: Optional[str] = None, completed: Optional[bool] = None) -> str:
    """Update task details."""
    # ...
    return f"Task {task_id} updated."

@mcp.tool()
def complete_task(task_id: int) -> str:
    """Mark a task as completed."""
    # ...
    return f"Task {task_id} marked as completed."

@mcp.tool()
def delete_task(task_id: int) -> str:
    """Delete a task permanently."""
    # ...
    return f"Task {task_id} deleted."
```

## Integration with Agent
The Orchestrator Agent will be initialized with these tools. When the Agent decides to call a tool, the corresponding function in `app/mcp/tools.py` is executed.

## Security
- **Authentication**: Tools operate within the context of the `current_user` from the request.
- **Authorization**: Ensure `user_id` checks are enforced inside tool logic (just like in API routes).
