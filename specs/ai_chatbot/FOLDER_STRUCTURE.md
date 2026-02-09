# Folder Structure Additions

## Backend Structure After Changes

```markdown
backend/
└── app/
    ├── agents/             # NEW: Agent logic and prompts
    │   ├── __init__.py
    │   ├── orchestrator.py
    │   ├── state_manager.py
    │   └── prompts.py
    ├── mcp/                # NEW: MCP Server module
    │   ├── __init__.py
    │   ├── server.py       # Server setup
    │   └── tools.py        # Tool implementations
    ├── routes/
    │   ├── chat.py         # NEW: Chat endpoints
    │   └── ... (existing routes)
    └── models.py           # MODIFIED: Added Conversation & Message
```

## Frontend Structure After Changes (Conceptual)

```markdown
frontend/
└── src/
    ├── components/
    │   ├── ChatInterface.tsx  # NEW: Chat UI component
    │   └── ...
    └── app/
        ├── chat/              # NEW: Chat page (optional)
        │   └── page.tsx
        └── ...
```

## No changes requested to existing files other than `backend/app/main.py` (to include new routes) and `frontend` (to link new components).
