# Implementation Plan: Phase 2 Todo Full-Stack Web Application

**Branch**: `001-fullstack-todo-app` | **Date**: 2026-01-26 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-fullstack-todo-app/spec.md`

## Summary

Build a multi-user todo application with secure authentication and task management. Users can register, log in with JWT tokens, and perform full CRUD operations on their personal tasks. The system enforces strict user isolation at the database level, ensuring each user sees only their own data. The application uses a modern monorepo architecture with Next.js frontend and FastAPI backend, deployed separately for optimal scalability.

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.x with Next.js 16+
- Backend: Python 3.11+

**Primary Dependencies**:
- Frontend: Next.js 16+ (App Router), React 19+, Tailwind CSS, Better Auth
- Backend: FastAPI 0.110+, SQLModel 0.0.14+, Pydantic 2.x, python-jose (JWT), asyncpg

**Storage**: Neon Serverless PostgreSQL (compatible with PostgreSQL 15+)

**Testing**:
- Frontend: Jest, React Testing Library (optional in Phase 2)
- Backend: pytest, httpx (for API testing)

**Target Platform**:
- Frontend: Web browsers (Chrome, Firefox, Safari, Edge - last 2 versions), deployed on Vercel
- Backend: Linux server (Docker container), deployed on Render/Railway/similar

**Project Type**: Web application (monorepo with /frontend and /backend)

**Performance Goals**:
- API response time: <200ms p95 for CRUD operations
- Page load time: <2 seconds initial load
- Support 100+ concurrent users

**Constraints**:
- API response time <200ms p95
- JWT token expiry: 7 days
- Title length: 1-200 characters
- Description length: max 1000 characters
- Mobile responsive (320px+ width)

**Scale/Scope**:
- Target: 100+ concurrent users
- Database: Unlimited tasks per user (no quota in Phase 2)
- 2 database tables (users, tasks)
- 6 API endpoints (auth + CRUD)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Principle I: Monorepo Architecture & RESTful Design
- [x] Strict separation: `/frontend` and `/backend` folders
- [x] RESTful API with proper HTTP methods (GET, POST, PUT, PATCH, DELETE)
- [x] Stateless backend with JWT authentication
- [x] Environment variables for all secrets

### ✅ Principle II: User Isolation & Data Security
- [x] JWT token validation on every API request
- [x] Database-level filtering by user_id
- [x] No cross-user data exposure
- [x] CORS properly configured

### ✅ Principle III: Security-First Development
- [x] JWT tokens required for all endpoints (except auth)
- [x] Better Auth for password hashing
- [x] No localStorage for sensitive data (httpOnly cookies)
- [x] Input validation on backend
- [x] Proper HTTP status codes (401, 403, 404, etc.)

### ✅ Principle IV: Type Safety & Error Handling
- [x] TypeScript strict mode in frontend
- [x] Python type hints in backend
- [x] Error handling on all endpoints
- [x] Async/await for I/O operations
- [x] Descriptive error messages with proper status codes

### ✅ Principle V: Performance & Optimization
- [x] API response time <200ms target
- [x] Database indexes on user_id and frequently queried fields
- [x] Next.js Server Components by default
- [x] Loading states in UI components

### ✅ Principle VI: Testing & Database Reliability
- [x] All endpoints testable via curl/Postman
- [x] SQLModel ORM (no raw SQL)
- [x] Loading, error, and empty states in frontend
- [x] Database migrations (SQLModel.metadata.create_all)

**Status**: ✅ ALL GATES PASSED - No violations, ready to proceed

## Project Structure

### Documentation (this feature)

```text
specs/001-fullstack-todo-app/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (technology decisions)
├── data-model.md        # Phase 1 output (database schema)
├── quickstart.md        # Phase 1 output (setup instructions)
├── contracts/           # Phase 1 output (API specifications)
│   └── api.yaml         # OpenAPI specification
├── checklists/
│   └── requirements.md  # Specification quality checklist
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── app/
│   ├── page.tsx                    # Landing page with login/signup
│   ├── dashboard/
│   │   └── page.tsx                # Main task list (protected route)
│   ├── layout.tsx                  # Root layout with providers
│   └── globals.css                 # Global styles
├── components/
│   ├── TaskList.tsx                # Task list container
│   ├── TaskForm.tsx                # Create/edit task modal
│   ├── TaskItem.tsx                # Individual task card
│   ├── AuthForm.tsx                # Login/signup form
│   └── ui/                         # Reusable UI components
│       ├── Button.tsx
│       ├── Input.tsx
│       └── Modal.tsx
├── lib/
│   ├── api.ts                      # API client wrapper
│   ├── auth.ts                     # Better Auth configuration
│   └── types.ts                    # TypeScript type definitions
├── public/                         # Static assets
├── .env.local                      # Environment variables (not committed)
├── package.json
├── tsconfig.json                   # TypeScript strict mode config
├── next.config.js
└── tailwind.config.js

backend/
├── app/
│   ├── main.py                     # FastAPI app + CORS setup
│   ├── models.py                   # SQLModel User and Task models
│   ├── database.py                 # Database connection and session
│   ├── config.py                   # Environment variables (pydantic-settings)
│   ├── dependencies.py             # Dependency injection (get_db, get_current_user)
│   └── routes/
│       ├── __init__.py
│       ├── auth.py                 # Authentication endpoints
│       └── tasks.py                # Task CRUD endpoints
├── migrations/                     # Database migrations (if using Alembic)
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_tasks.py
├── .env                            # Environment variables (not committed)
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container definition
└── pyproject.toml                  # Python project config (optional)

# Root level
.gitignore
README.md
docker-compose.yml                  # Local development setup
```

**Structure Decision**: Web application monorepo structure selected based on constitution requirement for `/frontend` and `/backend` separation. This enables independent deployment (frontend to Vercel, backend to Render/Railway), separate technology stacks, and clear API boundaries. The structure follows Next.js App Router conventions for frontend and FastAPI best practices for backend.

## Complexity Tracking

> **No violations detected - this section is empty**

All architecture decisions align with constitution principles. No complexity justification required.

---

## Phase 0: Research & Technology Decisions

### Authentication Strategy

**Decision**: Better Auth with JWT tokens stored in httpOnly cookies

**Rationale**:
- Better Auth provides secure password hashing out of the box
- JWT tokens enable stateless authentication (constitution requirement)
- httpOnly cookies prevent XSS attacks (constitution forbids localStorage for sensitive data)
- 7-day expiry balances security and user convenience

**Alternatives Considered**:
- Session-based auth: Rejected due to stateless requirement in constitution
- OAuth2 only: Rejected as Phase 2 focuses on email/password (OAuth can be added later)
- JWT in localStorage: Rejected due to XSS vulnerability and constitution prohibition

### Database ORM Selection

**Decision**: SQLModel for backend ORM

**Rationale**:
- Constitution mandates SQLModel (no raw SQL)
- Combines SQLAlchemy and Pydantic for type safety
- Async support with asyncpg driver
- Automatic validation and serialization

**Alternatives Considered**:
- Raw SQL: Forbidden by constitution
- Django ORM: Rejected as we're using FastAPI, not Django
- Tortoise ORM: Less mature, smaller ecosystem than SQLModel

### Frontend State Management

**Decision**: React Server Components + Client Components with useState/useContext

**Rationale**:
- Constitution requires Server Components by default
- Simple app doesn't need Redux/Zustand complexity
- Server Components reduce JavaScript bundle size
- Client Components only for interactive forms and modals

**Alternatives Considered**:
- Redux: Overkill for simple CRUD app
- Zustand: Unnecessary complexity for Phase 2
- React Query: Good for caching but adds dependency (can add in future phases)

### API Design Pattern

**Decision**: RESTful API with standard HTTP methods

**Rationale**:
- Constitution mandates RESTful design
- Industry standard, well-understood by all developers
- Proper HTTP verbs (GET, POST, PUT, PATCH, DELETE)
- Status codes convey meaning (200, 201, 401, 404, etc.)

**Alternatives Considered**:
- GraphQL: Overkill for simple CRUD, adds complexity
- RPC-style: Violates constitution's RESTful requirement
- WebSockets: Not needed for Phase 2 (no real-time requirements)

### Deployment Strategy

**Decision**:
- Frontend: Vercel (constitution requirement)
- Backend: Render or Railway (separate deployment, constitution requirement)
- Database: Neon Serverless PostgreSQL

**Rationale**:
- Vercel optimized for Next.js with zero-config deployment
- Separate backend deployment enables independent scaling
- Neon provides serverless PostgreSQL with automatic scaling
- All platforms support environment variables for secrets

**Alternatives Considered**:
- Monolithic deployment: Violates constitution's separation requirement
- AWS/GCP: More complex setup, overkill for hackathon Phase 2
- Self-hosted: Requires infrastructure management, slower iteration

---

## Phase 1: Data Model & API Contracts

### Data Model

See [data-model.md](./data-model.md) for complete schema definitions.

**Entities**:
1. **User**: Authentication and identity
2. **Task**: Todo items with user ownership

**Relationships**:
- User → Task: One-to-many (one user owns many tasks)
- Task → User: Many-to-one (each task belongs to one user)

**Key Constraints**:
- User email must be unique
- Task title required (1-200 chars)
- Task description optional (max 1000 chars)
- Foreign key: task.user_id → user.id with CASCADE delete
- Indexes on user_id for fast filtering

### API Contracts

See [contracts/api.yaml](./contracts/api.yaml) for OpenAPI specification.

**Base URL**: `http://localhost:8000` (development) / `https://api.yourdomain.com` (production)

**Authentication**: Bearer token in Authorization header (except auth endpoints)

**Endpoints**:
1. `POST /api/auth/register` - User registration
2. `POST /api/auth/login` - User login
3. `POST /api/tasks` - Create task
4. `GET /api/tasks` - List user's tasks
5. `GET /api/tasks/{id}` - Get single task
6. `PUT /api/tasks/{id}` - Update task
7. `PATCH /api/tasks/{id}/complete` - Toggle completion
8. `DELETE /api/tasks/{id}` - Delete task

### Integration Points

**Frontend ↔ Backend**:
- Protocol: HTTP/HTTPS with JSON payloads
- CORS: Backend allows frontend origin
- Headers: `Authorization: Bearer <token>`, `Content-Type: application/json`
- Error handling: Standardized error responses with status codes

**Backend ↔ Database**:
- Connection: asyncpg driver via SQLModel
- Pooling: Managed by SQLModel/SQLAlchemy
- Environment: `DATABASE_URL` from Neon connection string
- Migrations: SQLModel.metadata.create_all() for Phase 2

**Better Auth ↔ Backend**:
- Shared secret: `BETTER_AUTH_SECRET` environment variable
- Algorithm: HS256 (HMAC with SHA-256)
- Token payload: `{ user_id, email, exp }`
- Verification: Backend validates signature and expiry

### Quickstart

See [quickstart.md](./quickstart.md) for complete setup instructions.

**Prerequisites**:
- Node.js 18+ and npm/yarn
- Python 3.11+
- Neon account (free tier)
- Git

**Setup Steps**:
1. Clone repository
2. Set up environment variables
3. Install frontend dependencies
4. Install backend dependencies
5. Run database migrations
6. Start development servers
7. Access application at http://localhost:3000

---

## Architecture Diagrams

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                         │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           Next.js App (Port 3000)                    │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │   │
│  │  │ Landing Page │  │  Dashboard   │  │Components │ │   │
│  │  │ (page.tsx)   │  │ (protected)  │  │ (Task UI) │ │   │
│  │  └──────────────┘  └──────────────┘  └───────────┘ │   │
│  │         │                  │                │        │   │
│  │         └──────────────────┴────────────────┘        │   │
│  │                        │                              │   │
│  │                   lib/api.ts                          │   │
│  │              (API Client Wrapper)                     │   │
│  └────────────────────────│────────────────────────────┘   │
└────────────────────────────│────────────────────────────────┘
                             │
                             │ HTTP/JSON
                             │ Authorization: Bearer <JWT>
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (Port 8000)                     │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    main.py                            │  │
│  │              (CORS + Route Registration)              │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
│         ┌─────────────┴─────────────┐                       │
│         │                           │                       │
│  ┌──────▼──────┐            ┌──────▼──────┐               │
│  │ routes/     │            │ routes/     │               │
│  │ auth.py     │            │ tasks.py    │               │
│  │ (JWT verify)│            │ (CRUD ops)  │               │
│  └──────┬──────┘            └──────┬──────┘               │
│         │                           │                       │
│         └─────────────┬─────────────┘                       │
│                       │                                      │
│                ┌──────▼──────┐                              │
│                │  models.py  │                              │
│                │ (SQLModel)  │                              │
│                └──────┬──────┘                              │
│                       │                                      │
│                ┌──────▼──────┐                              │
│                │ database.py │                              │
│                │(Connection) │                              │
│                └──────┬──────┘                              │
└────────────────────────┼────────────────────────────────────┘
                         │
                         │ SQL (asyncpg)
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│           Neon Serverless PostgreSQL                         │
│                                                               │
│  ┌──────────────┐              ┌──────────────┐            │
│  │    users     │              │    tasks     │            │
│  │──────────────│              │──────────────│            │
│  │ id (UUID)    │◄─────────────│ id (SERIAL)  │            │
│  │ email        │   FK         │ user_id      │            │
│  │ password_hash│              │ title        │            │
│  │ name         │              │ description  │            │
│  │ created_at   │              │ completed    │            │
│  └──────────────┘              │ created_at   │            │
│                                 │ updated_at   │            │
│                                 └──────────────┘            │
│                                                               │
│  Indexes: tasks(user_id), tasks(completed)                  │
└─────────────────────────────────────────────────────────────┘
```

### Authentication Flow

```
User                Frontend              Backend              Database
 │                     │                     │                     │
 │  1. Enter email    │                     │                     │
 │     & password     │                     │                     │
 │────────────────────>│                     │                     │
 │                     │                     │                     │
 │                     │  2. POST /api/auth/login                 │
 │                     │     { email, password }                  │
 │                     │─────────────────────>│                     │
 │                     │                     │                     │
 │                     │                     │  3. Query user      │
 │                     │                     │     by email        │
 │                     │                     │─────────────────────>│
 │                     │                     │                     │
 │                     │                     │  4. Return user     │
 │                     │                     │<─────────────────────│
 │                     │                     │                     │
 │                     │                     │  5. Verify password │
 │                     │                     │     (Better Auth)   │
 │                     │                     │                     │
 │                     │                     │  6. Generate JWT    │
 │                     │                     │     { user_id,      │
 │                     │                     │       email, exp }  │
 │                     │                     │                     │
 │                     │  7. Return JWT      │                     │
 │                     │     + Set httpOnly  │                     │
 │                     │     cookie          │                     │
 │                     │<─────────────────────│                     │
 │                     │                     │                     │
 │  8. Redirect to    │                     │                     │
 │     /dashboard     │                     │                     │
 │<────────────────────│                     │                     │
 │                     │                     │                     │
 │  9. Access         │                     │                     │
 │     dashboard      │                     │                     │
 │────────────────────>│                     │                     │
 │                     │                     │                     │
 │                     │  10. GET /api/tasks │                     │
 │                     │      Authorization: │                     │
 │                     │      Bearer <JWT>   │                     │
 │                     │─────────────────────>│                     │
 │                     │                     │                     │
 │                     │                     │  11. Verify JWT     │
 │                     │                     │      signature      │
 │                     │                     │                     │
 │                     │                     │  12. Extract        │
 │                     │                     │      user_id        │
 │                     │                     │                     │
 │                     │                     │  13. Query tasks    │
 │                     │                     │      WHERE user_id  │
 │                     │                     │─────────────────────>│
 │                     │                     │                     │
 │                     │                     │  14. Return tasks   │
 │                     │                     │<─────────────────────│
 │                     │                     │                     │
 │                     │  15. Return tasks   │                     │
 │                     │      JSON array     │                     │
 │                     │<─────────────────────│                     │
 │                     │                     │                     │
 │  16. Display       │                     │                     │
 │      tasks         │                     │                     │
 │<────────────────────│                     │                     │
```

### Task Creation Flow

```
User                Frontend              Backend              Database
 │                     │                     │                     │
 │  1. Fill task form │                     │                     │
 │     (title, desc)  │                     │                     │
 │────────────────────>│                     │                     │
 │                     │                     │                     │
 │                     │  2. Validate form   │                     │
 │                     │     (client-side)   │                     │
 │                     │                     │                     │
 │                     │  3. POST /api/tasks │                     │
 │                     │     Authorization:  │                     │
 │                     │     Bearer <JWT>    │                     │
 │                     │     { title, desc } │                     │
 │                     │─────────────────────>│                     │
 │                     │                     │                     │
 │                     │                     │  4. Verify JWT      │
 │                     │                     │     Extract user_id │
 │                     │                     │                     │
 │                     │                     │  5. Validate input  │
 │                     │                     │     (Pydantic)      │
 │                     │                     │                     │
 │                     │                     │  6. INSERT task     │
 │                     │                     │     WITH user_id    │
 │                     │                     │─────────────────────>│
 │                     │                     │                     │
 │                     │                     │  7. Return task     │
 │                     │                     │     with id         │
 │                     │                     │<─────────────────────│
 │                     │                     │                     │
 │                     │  8. Return 201      │                     │
 │                     │     Created         │                     │
 │                     │     { task object } │                     │
 │                     │<─────────────────────│                     │
 │                     │                     │                     │
 │                     │  9. Update UI       │                     │
 │                     │     (add to list)   │                     │
 │                     │                     │                     │
 │  10. See new task  │                     │                     │
 │<────────────────────│                     │                     │
```

---

## Environment Variables

### Frontend (.env.local)

```bash
# Better Auth
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host/database

# Better Auth (must match frontend)
BETTER_AUTH_SECRET=your-secret-key-min-32-chars

# JWT
JWT_ALGORITHM=HS256
JWT_EXPIRY_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3000,https://yourdomain.vercel.app
```

---

## Deployment Configuration

### Frontend (Vercel)

**Build Command**: `npm run build`
**Output Directory**: `.next`
**Install Command**: `npm install`

**Environment Variables** (set in Vercel dashboard):
- `BETTER_AUTH_SECRET`
- `BETTER_AUTH_URL` (production URL)
- `NEXT_PUBLIC_API_URL` (backend production URL)

### Backend (Render/Railway)

**Build Command**: `pip install -r requirements.txt`
**Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Environment Variables** (set in platform dashboard):
- `DATABASE_URL` (from Neon)
- `BETTER_AUTH_SECRET` (must match frontend)
- `JWT_ALGORITHM=HS256`
- `JWT_EXPIRY_DAYS=7`
- `CORS_ORIGINS` (Vercel frontend URL)

### Database (Neon)

1. Create project on Neon dashboard
2. Copy connection string (includes credentials)
3. Add to backend `DATABASE_URL`
4. Run migrations on first deploy

---

## Next Steps

This plan is complete. To proceed with implementation:

1. **Run `/sp.tasks`** to generate the task breakdown from this plan
2. **Review generated tasks** for implementation order
3. **Begin Phase 1: Setup** (project initialization)
4. **Proceed to Phase 2: Foundational** (auth + database)
5. **Implement user stories** in priority order (P1 → P2 → P3)

**Files Generated**:
- ✅ plan.md (this file)
- ⏳ research.md (next: Phase 0 output)
- ⏳ data-model.md (next: Phase 1 output)
- ⏳ contracts/api.yaml (next: Phase 1 output)
- ⏳ quickstart.md (next: Phase 1 output)
