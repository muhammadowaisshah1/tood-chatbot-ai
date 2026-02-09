---
id: 002
title: Create Phase 2 Todo App Implementation Plan
stage: plan
date: 2026-01-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: fullstack-todo-app
branch: 001-fullstack-todo-app
user: user
command: /sp.plan
labels: ["plan", "architecture", "todo-app", "fullstack", "phase-2"]
links:
  spec: specs/001-fullstack-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-fullstack-todo-app/plan.md
  - specs/001-fullstack-todo-app/research.md
  - specs/001-fullstack-todo-app/data-model.md
  - specs/001-fullstack-todo-app/contracts/api.yaml
  - specs/001-fullstack-todo-app/quickstart.md
  - CLAUDE.md
tests:
  - none
---

## Prompt

Create a technical plan for Phase 2 Full-Stack Todo App covering HOW we will build it:

SYSTEM ARCHITECTURE:
- Next.js App (Frontend, Port 3000) ↔ FastAPI (Backend, Port 8000) ↔ Neon DB (PostgreSQL)
- JWT Token authentication (Authorization: Bearer <token>)

COMPONENT BREAKDOWN:
1. Frontend (Next.js): /frontend with App Router, components, lib/api.ts, lib/auth.ts
2. Backend (FastAPI): /backend with main.py, models.py, routes/, db.py, config.py
3. Database (Neon PostgreSQL): users and tasks tables with indexes

API SPECIFICATION:
- Base URL: http://localhost:8000
- 8 endpoints: register, login, create/list/get/update/delete tasks, toggle completion
- Authentication header on all endpoints except auth
- Error responses: 401, 403, 404, 422

DATA FLOW:
- User creates task → Frontend validates → POST /api/tasks with JWT → Backend extracts user_id → SQLModel creates task → Database returns task → Frontend updates UI
- User views tasks → GET /api/tasks → Backend queries WHERE user_id = ? → Returns JSON array → Frontend renders TaskItem components

AUTHENTICATION FLOW:
- Better Auth with JWT plugin, 7-day expiry, httpOnly cookies
- Login → Better Auth validates → Generates JWT → Stores in cookie → Redirects to dashboard
- API requests → Better Auth attaches JWT → Backend verifies signature → Extracts user_id → Proceeds

DEPLOYMENT PLAN:
- Frontend: Vercel (BETTER_AUTH_SECRET, NEXT_PUBLIC_API_URL)
- Backend: Render/Railway (DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS)
- Database: Neon (connection string, migrations)

FOLDER STRUCTURE:
- frontend/: app/, components/, lib/, package.json, next.config.js
- backend/: app/main.py, app/models.py, app/routes/, requirements.txt, Dockerfile

INTEGRATION POINTS:
- Frontend ↔ Backend: CORS, Authorization header, JSON payloads
- Backend ↔ Database: asyncpg via SQLModel, connection pooling
- Better Auth ↔ Backend: Shared BETTER_AUTH_SECRET, HS256 algorithm

## Response snapshot

Created comprehensive implementation plan for Phase 2 Todo Full-Stack Web Application with complete architecture, data model, API contracts, and setup instructions.

**Plan Structure (plan.md - 613 lines)**:
- Summary and technical context (languages, dependencies, platforms)
- Constitution check: ✅ All 6 principles passed (no violations)
- Project structure: monorepo with /frontend and /backend
- Phase 0: Research & technology decisions (5 major decisions documented)
- Phase 1: Data model & API contracts overview
- Architecture diagrams: System, authentication flow, task creation flow
- Environment variables for frontend and backend
- Deployment configuration for Vercel, Render/Railway, Neon

**Research Document (research.md - 350+ lines)**:
- Authentication strategy: Better Auth + JWT in httpOnly cookies
- Database ORM: SQLModel with asyncpg driver
- Frontend state management: Server Components + Client Components
- API design: RESTful with standard HTTP methods
- Deployment strategy: Vercel + Render/Railway + Neon
- Performance optimization: Database indexing + async operations
- Security best practices: Defense in depth
- Testing strategy: Manual testing via curl/Postman

**Data Model (data-model.md - 450+ lines)**:
- Entity relationship diagram
- User entity: UUID id, email (unique), password_hash, name, created_at
- Task entity: SERIAL id, user_id (FK), title, description, completed, timestamps
- Indexes: user_id, completed, composite (user_id, completed)
- Foreign key: CASCADE delete on user deletion
- SQLModel definitions with type hints
- Query patterns for user isolation
- Migration strategy (SQLModel.metadata.create_all for Phase 2)
- API response models (UserResponse, TaskResponse, TaskCreate, TaskUpdate)

**API Contracts (contracts/api.yaml - 600+ lines)**:
- OpenAPI 3.0.3 specification
- 8 endpoints fully documented with request/response schemas
- Authentication: Bearer token (JWT)
- Error responses: 401, 403, 404, 422 with examples
- Request/response examples for all endpoints
- Security schemes and validation rules

**Quickstart Guide (quickstart.md - 400+ lines)**:
- Prerequisites: Node.js 18+, Python 3.11+, Neon account
- 8-step setup process with commands
- Environment variable configuration (frontend and backend)
- Database initialization instructions
- Verification steps with curl commands
- Docker setup alternative
- Troubleshooting section (common errors and solutions)
- Development workflow and useful commands
- Environment variables reference table

**Agent Context Update**:
- Updated CLAUDE.md with Neon Serverless PostgreSQL database

**Constitution Compliance**:
- ✅ Monorepo architecture (/frontend and /backend separation)
- ✅ RESTful API design with proper HTTP methods
- ✅ Stateless backend with JWT authentication
- ✅ User isolation at database level (WHERE user_id filter)
- ✅ Security-first (JWT tokens, httpOnly cookies, input validation)
- ✅ Type safety (TypeScript strict mode, Python type hints)
- ✅ Performance (<200ms API responses, database indexes)
- ✅ SQLModel ORM (no raw SQL)

## Outcome

- ✅ Impact: Complete technical plan ready for task generation and implementation
- 🧪 Tests: N/A (planning document)
- 📁 Files: Created 5 planning artifacts (2,400+ total lines)
- 🔁 Next prompts: Run `/sp.tasks` to generate implementation task breakdown
- 🧠 Reflection: Plan successfully bridges specification (WHAT) to implementation (HOW) with detailed architecture, technology decisions, data model, API contracts, and setup instructions. All constitution principles validated and passed.

## Evaluation notes (flywheel)

- Failure modes observed: None - all planning artifacts complete and consistent
- Graders run and results (PASS/FAIL): PASS - Constitution check passed all 6 principles
- Prompt variant (if applicable): Detailed technical plan with user-provided architecture
- Next experiment (smallest change to try): Monitor task generation quality from this detailed plan
