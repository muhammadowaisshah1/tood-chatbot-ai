# AI Chatbot Implementation Specification (Phase III)

## 1. Analysis of Integration Points

### Current System Overview
- **Backend**: Python FastAPI with SQLModel/PostgreSQL.
- **Frontend**: React/Next.js (implied from context).
- **Existing Functionality**: Todo CRUD, Authentication (Better Auth/custom), user-specific data isolation.

### Integration Strategy
The AI Chatbot will be implemented as a new module within the existing backend structure, strictly adhering to the "Extension, Not Modification" principle.

- **Endpoint**: A new route `POST /api/chat` will be exposed.
- **State Management**: All conversation state will be persisted in `conversations` and `messages` tables. The server remains stateless between requests.
- **Tooling**: The existing service logic in `app.services` or directly in `app.routes` will be wrapped into MCP tools. Since the logic is currently inside route handlers, we will extract the core logic into a reusable service layer or directly invoke the route logic if cleanly separated (which it seems to be partially, but safer to extract). However, per instructions "Do NOT rewrite existing CRUD logic", we will wrapper the existing *route functionality* or ideally re-use the `models` and `db` session dependency injection pattern.
- **Agent Framework**: OpenAI Agents SDK (or similar high-level abstraction) will drive the logic. The agent will have access to the MCP tools.

## 2. MCP Tools Definition
These tools map 1:1 to existing Todo operations. They accept natural language parameters parsed by the LLM.

### 1. `add_task`
- **Description**: Creates a new task for the user.
- **Parameters**: 
  - `title` (string, required): The task title.
  - `description` (string, optional): Additional details.
  - `priority` (string, optional): 'low', 'medium', 'high'.
  - `due_date` (string, optional): ISO format date.
- **Output**: JSON representation of the created task.

### 2. `list_tasks`
- **Description**: Retrieves tasks based on filters.
- **Parameters**:
  - `status` (string, optional): 'completed', 'pending', 'all'.
  - `limit` (integer, optional): Max number of tasks (default 10).
- **Output**: List of task objects.

### 3. `update_task`
- **Description**: Modifies an existing task.
- **Parameters**:
  - `task_id` (integer, required): The ID of the task to update.
  - `updates` (object, required): Fields to update (title, description, status, priority).
- **Output**: Updated task object.

### 4. `complete_task`
- **Description**: Marks a task as completed.
- **Parameters**:
  - `task_id` (integer, required).
- **Output**: Updated task object showing `completed=true`.

### 5. `delete_task`
- **Description**: Permanently removes a task.
- **Parameters**:
  - `task_id` (integer, required).
- **Output**: Confirmation message.

## 3. Database Schema Additions
We need to persist conversation history.

```python
# app/models.py (New Additions)

class Conversation(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(default="New Chat")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True)
    conversation_id: str = Field(foreign_key="conversation.id", index=True)
    role: str = Field(description="user, assistant, or system")
    content: str = Field(description="The text content or tool result")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    conversation: Conversation = Relationship(back_populates="messages")
```

## 4. Agent Architecture
The system uses a multi-agent orchestration pattern (or a single smart agent with distinct tools, given the scope).
For this implementation, a **Single Sovereign Agent with MCP Tools** is sufficient and robust, but we will define roles conceptually.

### Roles
1. **Orchestrator**: The primary LLM that receives user input + conversation history.
2. **Tools Executor**: The MCP client that executes the requested tools.
3. **Response Formatter**: The LLM then generates the final natural language response based on tool outputs.

### Architecture Flow
1. **Input**: User sends message to `/api/chat`.
2. **Context Loading**: Backend loads last N messages for this conversation.
3. **Reasoning**: LLM (Orchestrator) decides if a tool is needed.
   - *If tool needed*: Generates tool call.
   - *If no tool*: Generates direct response.
4. **Execution**: Backend executes tool (CRUD) against DB.
5. **Observation**: Tool result is fed back to LLM.
6. **Final Response**: LLM summarizes action or answers query.
7. **Persistence**: User message and Assistant response (and tool calls/results) are saved to DB.
8. **Output**:  Response returned to Frontend.

## 5. Stateless Chat Flow (Specification)

### Endpoint: `POST /api/chat`
**Request Body**:
```json
{
  "conversation_id": "uuid-string (optional)",
  "message": "Add a task to buy milk"
}
```

**Process**:
1. **Auth Check**: Verify `current_user`.
2. **Session**: 
   - If `conversation_id` provided, fetch history.
   - If not, create new `Conversation`.
3. **Append User Msg**: Save user message to `Message` table.
4. **Agent Invocation**:
   - Construct prompt with System Prompt + History + Current Msg.
   - Call LLM with Tools definitions.
5. **Tool Loop**:
   - If LLM requests tool -> Execute locally -> Append Tool Result to history -> Call LLM again.
   - Repeat until LLM produces final text.
6. **Append Assistant Msg**: Save final response to `Message` table.
7. **Response**: Return the final text and updated `conversation_id`.

## 6. Frontend Integration Plan
- **New Component**: `ChatInterface` (floating widget or separate page).
- **State**: Local React state for message list, synced with backend.
- **API Client**: Add `chatApi` methods to existing API utility.
- **UI/UX**: 
  - Validates `user_id` is present.
  - Shows "Thinking..." state during agent execution.
  - Renders markdown response from agent.

## 7. Folder Structure Additions
```
backend/
  app/
    agents/           # New: Orchestrator and logic
      orchestrator.py
      prompts.py
    mcp/              # New: MCP Server/Tools definitions
      server.py
      tools.py
    routes/
      chat.py         # New: Chat endpoint
```

## 8. Error Handling
- **Tool Failures**: If a tool fails (e.g., DB error, validation), the error message is fed back to the LLM so it can apologize or retry.
- **Auth Failures**: Standard 401/403.
- **Quota/Rate Limits**: Handle LLM API errors gracefully with a "Please try again later" message.
