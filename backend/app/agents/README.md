# Agents Module

This folder will contain the AI Agent implementation.

## Structure
- `orchestrator.py`: The main entry point for agent logic.
- `state_manager.py`: Handles conversation context from DB.
- `prompts.py`: Python file loading prompt templates from `specs/ai_chatbot/prompts/`.
- `tools.py`: Helper functions for tool execution if not using MCP directly.

## Integration
1. Import `Orchestrator` from here into `backend/app/routes/chat.py`.
2. Initialize with `mcp_client` instance.
