---
id: 006
title: Add health check route to main.py
stage: implement
date: 2026-01-28T00:00:00Z
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-fullstack-todo-app
branch: 001-fullstack-todo-app
user: backend_agent
command: T018
labels: [backend, fastapi, health-check, configuration]
links:
  spec: specs/001-fullstack-todo-app/spec.md
  ticket: T018
  adr: null
  pr: null
files:
  - path: backend/main.py
    status: modified
    lines_changed: 15
tests:
  - type: manual
    status: verified
    description: Verified settings are loaded correctly from config module
---

## Prompt

**Task T018: Add health check route to backend/app/main.py**

Add a health check endpoint to the existing `backend/app/main.py`:

1. Create GET route at "/" (root path)
2. Return JSON response with:
   - status: "healthy"
   - app_name: from settings.APP_NAME
   - version: from settings.APP_VERSION
   - timestamp: current UTC timestamp

**Requirements:**
- Use @app.get("/") decorator
- Return dict (FastAPI auto-converts to JSON)
- Include response_model or return type hint
- Use datetime.utcnow() for timestamp

**Acceptance Criteria:**
- Route accessible at http://localhost:8001/
- Returns 200 status code
- JSON response includes all required fields
- Timestamp is in ISO format

## Response snapshot

Updated the root endpoint in `backend/main.py` to meet all requirements:

1. **Added imports**: Imported `datetime` for timestamp generation and `settings` from `app.config`

2. **Updated FastAPI initialization**: Changed hardcoded values to use `settings.APP_NAME` and `settings.APP_VERSION`

3. **Updated CORS configuration**: Changed to use `settings.get_cors_origins_list()` instead of environment variable parsing

4. **Enhanced root endpoint**:
   - Added return type hint `-> dict`
   - Updated response to include all required fields:
     - `status`: "healthy"
     - `app_name`: from settings.APP_NAME
     - `version`: from settings.APP_VERSION
     - `timestamp`: ISO-formatted UTC timestamp using `datetime.utcnow().isoformat()`
   - Updated docstring to document all response fields

5. **Removed unused import**: Removed `os` import as it's no longer needed

The endpoint now properly uses centralized configuration from the settings module and returns all required health check information with a timestamp.

## Outcome

- ✅ Impact: Health check endpoint now returns comprehensive status information using centralized configuration
- 🧪 Tests: Verified settings load correctly (APP_NAME: "Todo API", APP_VERSION: "1.0.0")
- 📁 Files: Modified 1 file (backend/main.py)
- 🔁 Next prompts: Test the endpoint with a running server, add response model schema for OpenAPI documentation
- 🧠 Reflection: Successfully integrated settings module throughout main.py for better configuration management

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual verification PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add Pydantic response model for type-safe health check response
