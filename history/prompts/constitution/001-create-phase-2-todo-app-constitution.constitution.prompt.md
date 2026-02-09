---
id: 001
title: Create Phase 2 Todo App Constitution
stage: constitution
date: 2026-01-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: ["constitution", "setup", "phase-2", "todo-app", "hackathon"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

Create a constitution file for Phase 2 Full-Stack Todo Application with these principles:

PROJECT IDENTITY:
- Name: Todo Full-Stack Web Application (Phase 2)
- Type: Multi-user web application with REST API
- Target: Hackathon Phase 2 completion

TECH STACK CONSTRAINTS:
- Frontend: Next.js 16+ (App Router only), TypeScript, Tailwind CSS
- Backend: Python FastAPI, SQLModel ORM
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT tokens
- Deployment: Frontend on Vercel, Backend separately

ARCHITECTURE PRINCIPLES:
1. Monorepo structure: /frontend and /backend folders
2. RESTful API design with proper HTTP methods
3. User isolation: Each user sees only their own tasks
4. Stateless backend: JWT for authentication
5. Environment variables for all secrets

SECURITY RULES:
- JWT tokens required for all API endpoints
- User ID validation on every request
- No hardcoded credentials
- CORS properly configured
- Password hashing with Better Auth

CODE STANDARDS:
- TypeScript strict mode in frontend
- Python type hints in backend
- Async/await for all I/O operations
- Error handling on all endpoints
- Proper HTTP status codes (200, 201, 400, 401, 404, 500)

TESTING REQUIREMENTS:
- All API endpoints must be testable
- Database migrations must be reversible
- Frontend components should handle loading states

PERFORMANCE EXPECTATIONS:
- API response time < 200ms for CRUD operations
- Database queries optimized with proper indexes
- Frontend: Server components by default, client components only when needed

FORBIDDEN PRACTICES:
- No inline SQL queries (use SQLModel)
- No localStorage for sensitive data
- No mixing of backend logic in frontend
- No user data leakage between users

## Response snapshot

Created comprehensive constitution file (v1.0.0) at `.specify/memory/constitution.md` with:

**Six Core Principles:**
1. Monorepo Architecture & RESTful Design - Separation of concerns, stateless backend
2. User Isolation & Data Security - JWT validation, database-level filtering
3. Security-First Development - Better Auth, input validation, proper status codes
4. Type Safety & Error Handling - TypeScript strict mode, Python type hints, async/await
5. Performance & Optimization - <200ms response times, indexed queries, Server Components
6. Testing & Database Reliability - Testable endpoints, reversible migrations, SQLModel ORM

**Additional Sections:**
- Tech Stack Constraints (Next.js 16+, FastAPI, Neon PostgreSQL, Better Auth)
- Forbidden Practices (7 explicit prohibitions with rationale)
- Development Workflow (code standards checklist, testing requirements, performance validation)
- Governance (amendment process, compliance review, version control)

**Sync Impact Report:**
- Version: Initial → 1.0.0
- Ratification: 2026-01-26
- Templates flagged for review: plan-template.md, spec-template.md, tasks-template.md

## Outcome

- ✅ Impact: Constitution established as authoritative governance document for Phase 2 Todo App development
- 🧪 Tests: N/A (governance document)
- 📁 Files: Created .specify/memory/constitution.md (156 lines)
- 🔁 Next prompts: Review dependent templates for alignment; Begin feature specification with /sp.specify
- 🧠 Reflection: Constitution provides clear, testable principles with explicit forbidden practices. All placeholders filled. Version 1.0.0 ratified.

## Evaluation notes (flywheel)

- Failure modes observed: None - all placeholders successfully replaced, no ambiguity
- Graders run and results (PASS/FAIL): PASS - Constitution complete, versioned, and actionable
- Prompt variant (if applicable): Standard constitution creation from detailed user requirements
- Next experiment (smallest change to try): Monitor template alignment during first feature specification
