from typing import Optional, List, Dict, Any
# from mcp.server.fastmcp import FastMCP  # Not needed for OpenAI function calling
from pydantic import BaseModel, Field
from datetime import datetime
import json
import contextvars
from sqlmodel import select, Session

from app.models import Task, User

# Context Variables
current_user_cv = contextvars.ContextVar("current_user", default=None)
db_session_cv = contextvars.ContextVar("db_session", default=None)

# Initialize FastMCP (server instance)
# mcp = FastMCP("todo-server")  # Not needed - using direct function calls

def get_ctx():
    user = current_user_cv.get()
    session = db_session_cv.get()
    if not user or not session:
        # In production, handle this gracefully or ensure context is always set
        # For now, it might raise LookupError if not set
        raise ValueError("Context not set")
    return user, session

# Tools Implementation

def add_task(title: str, description: str = "", priority: str = "medium", due_date: Optional[str] = None) -> str:
    """Create a new task."""
    try:
        user, session = get_ctx()
        
        parsed_date = None
        if due_date:
            try:
                parsed_date = datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                return "Error: Invalid date format. Use YYYY-MM-DD."

        new_task = Task(
            user_id=user.id,
            title=title,
            description=description,
            priority=priority,
            due_date=parsed_date,
            completed=False
        )
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        return json.dumps({
            "status": "success",
            "task": {
                "id": new_task.id,
                "title": new_task.title
            }
        })
    except Exception as e:
        return f"Error creating task: {str(e)}"

def list_tasks(status: str = "all", limit: int = 10) -> str:
    """List tasks. status can be 'completed', 'pending', or 'all'."""
    try:
        user, session = get_ctx()
        query = select(Task).where(Task.user_id == user.id)
        
        if status == "completed":
            query = query.where(Task.completed == True)
        elif status == "pending":
            query = query.where(Task.completed == False)
            
        query = query.order_by(Task.created_at.desc()).limit(limit)
        results = session.exec(query).all()
        
        tasks_list = []
        for t in results:
            tasks_list.append({
                "id": t.id, 
                "title": t.title, 
                "completed": t.completed,
                "priority": t.priority,
                "due_date": t.due_date.strftime("%Y-%m-%d") if t.due_date else None
            })
        return json.dumps(tasks_list)
    except Exception as e:
        return f"Error listing tasks: {str(e)}"

def update_task(task_id: int, title: Optional[str] = None, completed: Optional[bool] = None, priority: Optional[str] = None, due_date: Optional[str] = None) -> str:
    """Update a task."""
    try:
        user, session = get_ctx()
        task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user.id)).one_or_none()
        if not task:
            return f"Error: Task {task_id} not found."
            
        if title is not None: task.title = title
        if completed is not None: task.completed = completed
        if priority is not None: task.priority = priority
        if due_date is not None:
             try:
                task.due_date = datetime.strptime(due_date, "%Y-%m-%d")
             except ValueError:
                return "Error: Invalid date format."

        session.add(task)
        session.commit()
        session.refresh(task)
        return f"Task {task_id} updated."
    except Exception as e:
        return f"Error updating task: {str(e)}"

def complete_task(task_id: int) -> str:
    """Mark task as completed."""
    return update_task(task_id, completed=True)

def delete_task(task_id: int) -> str:
    """Delete a task."""
    try:
        user, session = get_ctx()
        task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user.id)).one_or_none()
        if not task:
            return f"Error: Task {task_id} not found."
        session.delete(task)
        session.commit()
        return f"Task {task_id} deleted."
    except Exception as e:
        return f"Error deleting task: {str(e)}"


# Export tools mapping for Agent Execution
AVAILABLE_TOOLS = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "update_task": update_task,
    "complete_task": complete_task,
    "delete_task": delete_task
}

# OpenAI Tool Schemas
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The task title"},
                    "description": {"type": "string", "description": "Details about the task"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                    "due_date": {"type": "string", "description": "YYYY-MM-DD format"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Get a list of tasks, filtered by status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": ["all", "completed", "pending"]},
                    "limit": {"type": "integer", "default": 10}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update an existing task properties.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "ID of the task to update"},
                    "title": {"type": "string"},
                    "completed": {"type": "boolean"},
                    "priority": {"type": "string"},
                    "due_date": {"type": "string", "description": "YYYY-MM-DD"}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer"}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Permanently delete a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer"}
                },
                "required": ["task_id"]
            }
        }
    }
]
