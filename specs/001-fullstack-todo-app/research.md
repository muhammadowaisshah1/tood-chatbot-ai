# Research & Technology Decisions

**Feature**: Phase 2 Todo Full-Stack Web Application
**Date**: 2026-01-26
**Status**: Complete

## Overview

This document captures the research and technology decisions made during the planning phase. All decisions align with the project constitution and are optimized for hackathon Phase 2 delivery.

## Authentication Strategy

### Decision
Better Auth with JWT tokens stored in httpOnly cookies

### Research Findings

**Better Auth Benefits**:
- Built-in password hashing with bcrypt/argon2
- JWT token generation and validation
- TypeScript-first design
- Minimal configuration required
- Active maintenance and community support

**JWT Token Strategy**:
- Stateless authentication (constitution requirement)
- 7-day expiry balances security and UX
- httpOnly cookies prevent XSS attacks
- Bearer token in Authorization header for API requests

**Security Considerations**:
- httpOnly cookies cannot be accessed by JavaScript (XSS protection)
- Secure flag ensures HTTPS-only transmission in production
- SameSite attribute prevents CSRF attacks
- Token expiry forces re-authentication after 7 days

### Alternatives Evaluated

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Session-based auth | Simple, server-controlled revocation | Requires stateful backend, violates constitution | ❌ Rejected |
| OAuth2 only | Industry standard, social login | Complex setup, overkill for Phase 2 | ⏳ Future phase |
| JWT in localStorage | Easy to implement | XSS vulnerable, forbidden by constitution | ❌ Rejected |
| Better Auth + JWT | Secure, stateless, constitution-compliant | Requires shared secret management | ✅ Selected |

### Implementation Notes
- Shared secret (`BETTER_AUTH_SECRET`) must be identical in frontend and backend
- Minimum 32 characters for secret strength
- Token payload: `{ user_id: UUID, email: string, exp: timestamp }`
- Backend validates signature and expiry on every request

---

## Database ORM Selection

### Decision
SQLModel for backend ORM with asyncpg driver

### Research Findings

**SQLModel Advantages**:
- Mandated by constitution (no raw SQL allowed)
- Combines SQLAlchemy (ORM) + Pydantic (validation)
- Type safety with Python type hints
- Automatic request/response validation
- Async support via asyncpg driver
- Single model definition for DB and API

**Performance Characteristics**:
- asyncpg is fastest PostgreSQL driver for Python
- Connection pooling handled automatically
- Lazy loading prevents N+1 query problems
- Indexes on user_id ensure <200ms query times

### Alternatives Evaluated

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Raw SQL | Maximum control, performance | Forbidden by constitution, SQL injection risk | ❌ Rejected |
| Django ORM | Mature, feature-rich | Requires Django framework, not FastAPI | ❌ Rejected |
| Tortoise ORM | Async-first design | Smaller ecosystem, less mature | ❌ Rejected |
| SQLModel | Constitution-compliant, type-safe, async | Newer library (less battle-tested) | ✅ Selected |

### Implementation Notes
- Use `SQLModel.metadata.create_all()` for initial schema creation
- For production, consider Alembic for migrations (Phase 3+)
- All models inherit from SQLModel base class
- Relationships defined with `Relationship()` for type safety

---

## Frontend State Management

### Decision
React Server Components + Client Components with useState/useContext

### Research Findings

**Server Components Benefits**:
- Constitution requires Server Components by default
- Reduced JavaScript bundle size (better performance)
- Direct database access (not applicable here due to API architecture)
- Automatic code splitting
- SEO-friendly rendering

**Client Components Usage**:
- Interactive forms (TaskForm, AuthForm)
- Modals with state (TaskForm modal)
- Real-time updates (task completion toggle)
- User input handling

**State Management Approach**:
- Server Components for static content (layout, landing page)
- Client Components for interactivity (forms, modals, task list)
- useState for local component state
- useContext for shared state (auth status, user info)
- No global state library needed for Phase 2

### Alternatives Evaluated

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Redux | Predictable state, dev tools | Overkill for simple CRUD, boilerplate | ❌ Rejected |
| Zustand | Lightweight, simple API | Unnecessary for Phase 2 scope | ❌ Rejected |
| React Query | Excellent caching, auto-refetch | Adds dependency, complexity | ⏳ Future phase |
| Server + Client Components | Constitution-compliant, performant | Requires careful component boundaries | ✅ Selected |

### Implementation Notes
- Mark interactive components with `"use client"` directive
- Keep Server Components as default
- Pass data from Server to Client Components via props
- Use React 19 features (useOptimistic for optimistic updates)

---

## API Design Pattern

### Decision
RESTful API with standard HTTP methods

### Research Findings

**RESTful Principles Applied**:
- Resources: `/api/tasks`, `/api/auth`
- HTTP verbs: GET (read), POST (create), PUT (update), PATCH (partial update), DELETE (remove)
- Status codes: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 404 (Not Found)
- Stateless: Each request contains all necessary information (JWT token)
- JSON payloads for request/response

**Endpoint Design**:
- Collection: `GET /api/tasks` (list all user's tasks)
- Resource: `GET /api/tasks/{id}` (get single task)
- Create: `POST /api/tasks` (create new task)
- Update: `PUT /api/tasks/{id}` (full update)
- Partial update: `PATCH /api/tasks/{id}/complete` (toggle completion)
- Delete: `DELETE /api/tasks/{id}` (remove task)

### Alternatives Evaluated

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| GraphQL | Flexible queries, single endpoint | Overkill for CRUD, adds complexity | ❌ Rejected |
| RPC-style | Simple for actions | Violates RESTful constitution requirement | ❌ Rejected |
| WebSockets | Real-time updates | Not needed for Phase 2, adds complexity | ⏳ Future phase |
| RESTful API | Constitution-compliant, standard, simple | Requires multiple endpoints | ✅ Selected |

### Implementation Notes
- Use FastAPI's automatic OpenAPI generation
- Pydantic models for request/response validation
- Consistent error response format: `{ "detail": "error message" }`
- CORS configured to allow frontend origin only

---

## Deployment Strategy

### Decision
- Frontend: Vercel (constitution requirement)
- Backend: Render or Railway
- Database: Neon Serverless PostgreSQL

### Research Findings

**Vercel for Frontend**:
- Optimized for Next.js (zero-config deployment)
- Automatic HTTPS and CDN
- Environment variable management
- Preview deployments for branches
- Free tier sufficient for Phase 2

**Render/Railway for Backend**:
- Docker container support
- Automatic deployments from Git
- Environment variable management
- Free tier available (with limitations)
- Easy PostgreSQL integration

**Neon for Database**:
- Serverless PostgreSQL (auto-scaling)
- Generous free tier (3 GB storage)
- Automatic backups
- Connection pooling built-in
- Compatible with standard PostgreSQL tools

### Alternatives Evaluated

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Monolithic (single platform) | Simpler deployment | Violates constitution separation requirement | ❌ Rejected |
| AWS/GCP | Full control, scalable | Complex setup, overkill for hackathon | ❌ Rejected |
| Self-hosted | Maximum control | Requires infrastructure management | ❌ Rejected |
| Vercel + Render + Neon | Constitution-compliant, simple, free tier | Separate platforms to manage | ✅ Selected |

### Implementation Notes
- Use environment variables for all secrets (never commit)
- Frontend `NEXT_PUBLIC_API_URL` points to backend production URL
- Backend `CORS_ORIGINS` includes frontend production URL
- Database connection string from Neon dashboard
- All platforms support automatic deployments from Git

---

## Performance Optimization Strategy

### Decision
Database indexing + Server Components + Async operations

### Research Findings

**Database Optimization**:
- Index on `tasks.user_id` (most frequent query filter)
- Index on `tasks.completed` (for status filtering)
- Connection pooling via SQLModel/SQLAlchemy
- Async queries prevent blocking

**Frontend Optimization**:
- Server Components reduce JavaScript bundle
- Code splitting via Next.js App Router
- Tailwind CSS purges unused styles
- Image optimization via Next.js Image component

**Backend Optimization**:
- Async/await for all I/O operations
- FastAPI's async support (non-blocking)
- Pydantic validation (fast C extensions)
- Minimal middleware overhead

### Performance Targets
- API response time: <200ms p95 (constitution requirement)
- Page load time: <2 seconds initial load
- Task list rendering: <100ms for 1000 tasks
- Database query time: <50ms with indexes

### Implementation Notes
- Use `asyncpg` driver (fastest PostgreSQL driver)
- Create indexes in migration: `CREATE INDEX idx_tasks_user_id ON tasks(user_id)`
- Monitor performance with FastAPI's built-in metrics
- Use React.memo() for expensive components if needed

---

## Security Best Practices

### Decision
Defense in depth: JWT validation + input sanitization + CORS + HTTPS

### Research Findings

**Authentication Security**:
- JWT tokens in httpOnly cookies (XSS protection)
- Token expiry enforced (7 days)
- Signature verification on every request
- User ID extracted from token (not from request body)

**Input Validation**:
- Pydantic models validate all inputs
- SQLModel prevents SQL injection
- Title length: 1-200 characters
- Description length: max 1000 characters

**CORS Configuration**:
- Allow only frontend origin
- Credentials: true (for cookies)
- Methods: GET, POST, PUT, PATCH, DELETE
- Headers: Authorization, Content-Type

**HTTPS Enforcement**:
- Vercel provides automatic HTTPS
- Render/Railway provide automatic HTTPS
- Secure flag on cookies in production

### Implementation Notes
- Never trust client input (validate on backend)
- Filter database queries by authenticated user_id
- Return generic error messages (don't leak system info)
- Log security events (failed auth attempts)

---

## Testing Strategy (Phase 2 Scope)

### Decision
Manual testing via curl/Postman + optional automated tests

### Research Findings

**Manual Testing**:
- Constitution requires all endpoints testable via curl/Postman
- Faster iteration for hackathon Phase 2
- Sufficient for MVP validation

**Automated Testing (Optional)**:
- Backend: pytest + httpx for API tests
- Frontend: Jest + React Testing Library
- Can be added in Phase 3+ if time permits

### Implementation Notes
- Document curl commands in quickstart.md
- Test all endpoints with valid/invalid tokens
- Test user isolation (cannot access other users' tasks)
- Test validation errors (missing title, too long, etc.)

---

## Summary

All technology decisions align with the project constitution and are optimized for Phase 2 delivery. The stack (Next.js + FastAPI + Neon PostgreSQL) provides:

- ✅ Type safety (TypeScript + Python type hints)
- ✅ Security (JWT + httpOnly cookies + input validation)
- ✅ Performance (<200ms API responses + Server Components)
- ✅ Scalability (stateless backend + serverless database)
- ✅ Developer experience (modern tools + good documentation)

**Ready to proceed to implementation** with confidence in these architectural choices.
