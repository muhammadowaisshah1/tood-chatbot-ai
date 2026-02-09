---
id: 003
title: Create Authentication Module with JWT
stage: tasks
date: 2026-01-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-fullstack-todo-app
branch: 001-fullstack-todo-app
user: ADMIN
command: manual
labels: [backend, authentication, jwt, better-auth, security, bcrypt]
links:
  spec: specs/001-fullstack-todo-app/spec.md
  ticket: T011
  adr: null
  pr: null
files:
  - path: backend/app/auth.py
    status: created
    lines: 197
tests:
  - type: none
    status: pending
    note: Authentication will be tested via API endpoints
---

## Prompt

Continue with authentication setup after database connection module.

## Response snapshot

Created `backend/app/auth.py` with comprehensive JWT authentication:

**Password Management:**
- `hash_password()` - Bcrypt hashing for secure password storage
- `verify_password()` - Password verification against hash
- Uses passlib with bcrypt scheme

**JWT Token Management:**
- `create_access_token()` - Generate JWT with configurable expiry
- `decode_access_token()` - Verify and decode JWT tokens
- Includes `exp` (expiry) and `iat` (issued at) claims
- Uses Better Auth secret from environment

**Authentication Functions:**
- `authenticate_user()` - Validate email/password credentials
- `get_current_user()` - FastAPI dependency for protected routes
- Async database queries for user lookup

**Security Features:**
- HTTP Bearer token authentication
- Proper error handling with 401 Unauthorized responses
- WWW-Authenticate headers for OAuth2 compliance
- Environment variable validation on module load
- Token expiry configurable via JWT_EXPIRY_DAYS

**Configuration:**
- BETTER_AUTH_SECRET - Shared secret with frontend
- JWT_ALGORITHM - HS256 (HMAC SHA-256)
- JWT_EXPIRY_DAYS - Default 7 days

**Usage Pattern:**
```python
# Protected route example
@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"user_id": current_user.id}
```

## Outcome

- ✅ Impact: Complete authentication system with JWT and password hashing
- 🧪 Tests: Pending - will be tested via auth API endpoints
- 📁 Files: Created backend/app/auth.py (197 lines)
- 🔁 Next prompts: Update main.py with startup events, create auth routes (signup/login), create task routes (CRUD)
- 🧠 Reflection: Authentication layer follows OAuth2 Bearer token pattern, compatible with FastAPI's security utilities and Better Auth frontend integration.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A - awaiting endpoint integration
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test token generation and verification with sample user data
