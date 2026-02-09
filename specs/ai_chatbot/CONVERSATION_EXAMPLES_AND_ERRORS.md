# Example AI Conversations & Error Handling

## 1. Successful Task Creation

**User**: "Add 'Book dentist appointment' for next Tuesday at 3 PM."

**Assistant**: 
- **Internal Thought**: Needs `add_task`.
- **Tool Call**: `add_task(title="Book dentist appointment", due_date="202X-MM-DD", time="15:00")`
- **Tool Result**: `{"id": 42, "title": "Book dentist appointment", "created_at": "..."}`
- **System**: Save tool result.
- **Orchestrator**: "I've added 'Book dentist appointment' to your tasks for next Tuesday."

**User**: "Great, thanks!"

## 2. Querying Tasks

**User**: "What do I have to do today?"

**Assistant**:
- **Internal Thought**: Needs `list_tasks` filtered by date=today.
- **Tool Call**: `list_tasks(status="pending", date="202X-MM-DD")`
- **Tool Result**: `[{"title": "Submit report"}, {"title": "Call client"}]`
- **Orchestrator**: "You have 2 tasks due today:
  1. Submit report
  2. Call client"

## 3. Handling Ambiguity (Error Case 1)

**User**: "Change the due date."

**Assistant**:
- **Internal Thought**: Missing `task_id` and new `date`.
- **Response**: "Which task would you like to update, and what is the new due date?"

**User**: "The report task. Make it Friday."

**Assistant**:
- **Internal Thought**: Find task "report".
- **Tool Call**: `list_tasks(search="report")`
- **Tool Result**: `[{"id": 105, "title": "Submit Q3 Report"}]`
- **Internal Thought**: Update task 105.
- **Tool Call**: `update_task(task_id=105, due_date="202X-MM-Friday")`
- **Orchestrator**: "I've updated the due date for 'Submit Q3 Report' to this Friday."

## 4. Resource Not Found (Error Case 2)

**User**: "Mark task #999 as complete."

**Assistant**:
- **Tool Call**: `complete_task(task_id=999)`
- **Tool Result**: `{"error": "Task not found."}`
- **Orchestrator**: "I couldn't find a task with ID #999. Please check the ID or ask me to list your tasks."

## 5. Tool Failure (Error Case 3)

**User**: "List my tasks."

**Assistant**:
- **Tool Call**: `list_tasks()`
- **Tool Result**: `{"error": "Database connection failed."}` (Simulated)
- **Orchestrator**: "I'm having trouble accessing your tasks right now due to a system error. Please try again in a moment."

## 6. Authentication Error

**User** (Unauthenticated): "Add a task."

**System**: Returns 401 Unauthorized. Frontend redirects to Login.
