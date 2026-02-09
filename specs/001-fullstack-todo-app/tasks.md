---
description: "Task list for Phase 2 Todo Full-Stack Web Application"
---

# Tasks: Phase 2 Todo Full-Stack Web Application

**Input**: Design documents from `/specs/001-fullstack-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/api.yaml, research.md

**Tests**: Tests are OPTIONAL in Phase 2 - manual testing via curl/Postman is sufficient per constitution.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Agent Assignment**: Each task includes assigned agent for sp.implement automation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- **Agent**: Specialized agent responsible for task execution
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/app/`, `frontend/app/`, `frontend/components/`, `frontend/lib/`
- Paths shown below follow monorepo structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] **T001**: Create /frontend and /backend directories at repository root
  - **Agent**: @devops_agent
  - **Dependencies**: None
  - **Acceptance**:
    - `frontend/` directory exists at root
    - `backend/` directory exists at root

- [X] **T002**: Initialize Next.js 16+ in frontend/ with App Router and TypeScript strict mode
  - **Agent**: @frontend_agent
  - **Dependencies**: T001
  - **Acceptance**:
    - `frontend/package.json` with Next.js 16+
    - `frontend/tsconfig.json` with strict mode
    - `frontend/app/` directory exists (App Router)

- [X] **T003** [P]: Initialize Python project in backend/ with FastAPI and SQLModel dependencies
  - **Agent**: @backend_agent
  - **Dependencies**: T001
  - **Acceptance**:
    - `backend/requirements.txt` with FastAPI, SQLModel, uvicorn
    - `backend/pyproject.toml` or `backend/setup.py` configured

- [X] **T004** [P]: Create frontend/.env.local with BETTER_AUTH_SECRET, BETTER_AUTH_URL, NEXT_PUBLIC_API_URL
  - **Agent**: @frontend_agent
  - **Dependencies**: T002
  - **Acceptance**:
    - `frontend/.env.local` exists
    - Contains BETTER_AUTH_SECRET, BETTER_AUTH_URL, NEXT_PUBLIC_API_URL
    - `.gitignore` includes `.env.local`

- [X] **T005** [P]: Create backend/.env with DATABASE_URL, BETTER_AUTH_SECRET, JWT_ALGORITHM, JWT_EXPIRY_DAYS, CORS_ORIGINS
  - **Agent**: @backend_agent
  - **Dependencies**: T003
  - **Acceptance**:
    - `backend/.env` exists
    - Contains all required variables
    - `.gitignore` includes `.env`

- [X] **T006** [P]: Configure Tailwind CSS in frontend/tailwind.config.js
  - **Agent**: @frontend_agent
  - **Dependencies**: T002
  - **Acceptance**:
    - `frontend/tailwind.config.js` configured
    - `frontend/globals.css` with Tailwind directives

- [X] **T007** [P]: Create frontend/tsconfig.json with strict mode enabled
  - **Agent**: @frontend_agent
  - **Dependencies**: T002
  - **Acceptance**:
    - `"strict": true` in tsconfig.json
    - TypeScript compilation works

- [X] **T008**: Sign up for Neon account and create "hackathon-todo" project, copy connection string to backend/.env
  - **Agent**: @db_auth_agent
  - **Dependencies**: T005
  - **Acceptance**:
    - Neon database "hackathon-todo" created
    - DATABASE_URL in `backend/.env` points to Neon
    - Connection verified

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] **T009**: Create backend/app/models.py with SQLModel imports and base configuration
  - **Agent**: @db_auth_agent
  - **Dependencies**: T008
  - **Acceptance**:
    - `backend/app/models.py` exists
    - SQLModel imported
    - Base model configuration done

- [ ] **T010** [P]: Create User model in backend/app/models.py with id (UUID), email (unique), password_hash, name, created_at
  - **Agent**: @db_auth_agent
  - **Dependencies**: T009
  - **Acceptance**:
    - User model with all fields
    - id as UUID primary key
    - email with unique constraint
    - password_hash field (not plain password)

- [ ] **T011** [P]: Create Task model in backend/app/models.py with id, user_id (FK), title, description, completed, created_at, updated_at
  - **Agent**: @db_auth_agent
  - **Dependencies**: T009
  - **Acceptance**:
    - Task model with all fields
    - user_id foreign key to User
    - completed boolean default False
    - Timestamps auto-managed

- [ ] **T012**: Create backend/app/database.py with async engine, connection pool, and get_session dependency
  - **Agent**: @db_auth_agent
  - **Dependencies**: T008
  - **Acceptance**:
    - `backend/app/database.py` exists
    - Async SQLAlchemy engine configured
    - get_session dependency function
    - Connection pool configured

- [ ] **T013**: Create backend/app/config.py to load environment variables using pydantic-settings
  - **Agent**: @backend_agent
  - **Dependencies**: T005
  - **Acceptance**:
    - `backend/app/config.py` exists
    - Pydantic Settings class
    - Loads from .env file
    - All required config vars defined

- [ ] **T014**: Create backend/app/main.py with FastAPI app instance and CORS configuration for frontend origin
  - **Agent**: @backend_agent
  - **Dependencies**: T013
  - **Acceptance**:
    - `backend/app/main.py` exists
    - FastAPI app instance created
    - CORS middleware configured
    - Frontend origin allowed

- [ ] **T015**: Create backend/app/dependencies.py with get_db and get_current_user dependency functions
  - **Agent**: @backend_agent
  - **Dependencies**: T012
  - **Acceptance**:
    - `backend/app/dependencies.py` exists
    - get_db dependency for database sessions
    - get_current_user dependency for JWT auth

- [ ] **T016**: Create backend/init_db.py script to run SQLModel.metadata.create_all() and initialize database tables
  - **Agent**: @db_auth_agent
  - **Dependencies**: T010, T011, T012
  - **Acceptance**:
    - `backend/init_db.py` script exists
    - Creates all tables when run
    - Idempotent (safe to run multiple times)

- [ ] **T017**: Run backend/init_db.py to create users and tasks tables in Neon database
  - **Agent**: @db_auth_agent
  - **Dependencies**: T016
  - **Acceptance**:
    - Script executed successfully
    - users table exists in Neon
    - tasks table exists in Neon
    - Schema matches models

- [ ] **T018** [P]: Add health check route GET / in backend/app/main.py returning {"message": "Todo API is running"}
  - **Agent**: @backend_agent
  - **Dependencies**: T014
  - **Acceptance**:
    - GET / endpoint returns JSON
    - Status code 200
    - Message confirms API running

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration & Authentication (Priority: P1) 🎯 MVP

**Goal**: Users can register, log in, log out, and access protected routes with JWT authentication

**Independent Test**: Create account → Log out → Log back in → Access dashboard (no task functionality needed)

### Implementation for User Story 1

- [ ] **T019** [P] [US1]: Install better-auth package in frontend/ with npm install better-auth
  - **Agent**: @frontend_agent
  - **Dependencies**: T002
  - **Acceptance**:
    - better-auth in `frontend/package.json`
    - `npm install` runs successfully

- [ ] **T020** [P] [US1]: Create frontend/lib/auth.ts with Better Auth configuration, JWT plugin, 7-day expiry
  - **Agent**: @frontend_agent
  - **Dependencies**: T019
  - **Acceptance**:
    - `frontend/lib/auth.ts` exists
    - Better Auth configured
    - JWT plugin enabled
    - Token expiry set to 7 days

- [ ] **T021** [P] [US1]: Create frontend/lib/types.ts with TypeScript interfaces for User, Task, AuthResponse
  - **Agent**: @frontend_agent
  - **Dependencies**: T002
  - **Acceptance**:
    - `frontend/lib/types.ts` exists
    - User interface defined
    - Task interface defined
    - AuthResponse interface defined

- [ ] **T022** [US1]: Create backend/app/routes/auth.py with JWT validation middleware and get_current_user dependency
  - **Agent**: @backend_agent
  - **Dependencies**: T015
  - **Acceptance**:
    - `backend/app/routes/auth.py` exists
    - JWT validation function
    - get_current_user dependency extracts user from token

- [ ] **T023** [US1]: Add POST /api/auth/register endpoint in backend/app/routes/auth.py with email/password/name validation
  - **Agent**: @backend_agent
  - **Dependencies**: T022
  - **Acceptance**:
    - POST /api/auth/register endpoint
    - Email validation (format + uniqueness)
    - Password hashing (bcrypt/argon2)
    - Name required
    - Returns user data (no password)

- [ ] **T024** [US1]: Add POST /api/auth/login endpoint in backend/app/routes/auth.py with credential verification and JWT generation
  - **Agent**: @backend_agent
  - **Dependencies**: T022
  - **Acceptance**:
    - POST /api/auth/login endpoint
    - Email + password verification
    - JWT token generation
    - Returns token + user data

- [ ] **T025** [US1]: Register auth routes in backend/app/main.py
  - **Agent**: @backend_agent
  - **Dependencies**: T023, T024
  - **Acceptance**:
    - Auth router included in main.py
    - Routes accessible at /api/auth/*

- [ ] **T026** [P] [US1]: Create frontend/components/AuthForm.tsx with sign up and sign in forms
  - **Agent**: @frontend_agent
  - **Dependencies**: T021
  - **Acceptance**:
    - `frontend/components/AuthForm.tsx` exists
    - Sign up form (email, password, name)
    - Sign in form (email, password)
    - Client-side validation
    - Toggle between forms

- [ ] **T027** [P] [US1]: Create frontend/app/page.tsx as landing page with AuthForm component
  - **Agent**: @frontend_agent
  - **Dependencies**: T026
  - **Acceptance**:
    - `frontend/app/page.tsx` exists
    - Shows AuthForm component
    - Redirects to dashboard if authenticated

- [ ] **T028** [US1]: Create frontend/app/dashboard/page.tsx as protected route with auth middleware
  - **Agent**: @frontend_agent
  - **Dependencies**: T020
  - **Acceptance**:
    - `frontend/app/dashboard/page.tsx` exists
    - Checks authentication on mount
    - Redirects to login if unauthenticated
    - Shows user info if authenticated

- [ ] **T029** [US1]: Add logout functionality to frontend/app/dashboard/page.tsx
  - **Agent**: @frontend_agent
  - **Dependencies**: T028
  - **Acceptance**:
    - Logout button in dashboard
    - Clears auth token
    - Redirects to landing page

- [ ] **T030** [US1]: Test authentication flow: register → login → access dashboard → logout
  - **Agent**: @orchestrator
  - **Dependencies**: T025, T027, T028, T029
  - **Acceptance**:
    - Can register new user
    - Can login with credentials
    - Dashboard accessible when authenticated
    - Logout redirects to login
    - Cannot access dashboard after logout

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Management (Priority: P2)

**Goal**: Authenticated users can create, view, update, complete, and delete their personal tasks

**Independent Test**: Log in → Create task → View tasks → Update task → Mark complete → Delete task

### Implementation for User Story 2

- [ ] **T031** [P] [US2]: Create backend/app/routes/tasks.py with task router
  - **Agent**: @backend_agent
  - **Dependencies**: T017
  - **Acceptance**:
    - `backend/app/routes/tasks.py` exists
    - Task router configured
    - Depends on get_current_user

- [ ] **T032** [P] [US2]: Implement POST /api/tasks endpoint in backend/app/routes/tasks.py with title validation (1-200 chars), description (max 1000 chars), user_id from JWT
  - **Agent**: @backend_agent
  - **Dependencies**: T031
  - **Acceptance**:
    - POST /api/tasks endpoint
    - Title required, 1-200 chars
    - Description optional, max 1000 chars
    - user_id from JWT token
    - Returns created task

- [ ] **T033** [P] [US2]: Implement GET /api/tasks endpoint in backend/app/routes/tasks.py filtering by user_id, optional status query param, order by created_at DESC
  - **Agent**: @backend_agent
  - **Dependencies**: T031
  - **Acceptance**:
    - GET /api/tasks endpoint
    - Filters by current user only
    - Optional ?status=pending|completed
    - Ordered newest first
    - Returns array of tasks

- [ ] **T034** [P] [US2]: Implement GET /api/tasks/{id} endpoint in backend/app/routes/tasks.py with ownership verification
  - **Agent**: @backend_agent
  - **Dependencies**: T031
  - **Acceptance**:
    - GET /api/tasks/{id} endpoint
    - Verifies task belongs to current user
    - Returns 404 if not found or not owned
    - Returns task data

- [ ] **T035** [P] [US2]: Implement PUT /api/tasks/{id} endpoint in backend/app/routes/tasks.py with ownership verification and updated_at timestamp
  - **Agent**: @backend_agent
  - **Dependencies**: T031
  - **Acceptance**:
    - PUT /api/tasks/{id} endpoint
    - Ownership verification
    - Updates title/description
    - Auto-updates updated_at
    - Returns updated task

- [ ] **T036** [P] [US2]: Implement PATCH /api/tasks/{id}/complete endpoint in backend/app/routes/tasks.py to toggle completed status
  - **Agent**: @backend_agent
  - **Dependencies**: T031
  - **Acceptance**:
    - PATCH /api/tasks/{id}/complete endpoint
    - Toggles completed boolean
    - Ownership verification
    - Updates updated_at
    - Returns updated task

- [ ] **T037** [P] [US2]: Implement DELETE /api/tasks/{id} endpoint in backend/app/routes/tasks.py with ownership verification
  - **Agent**: @backend_agent
  - **Dependencies**: T031
  - **Acceptance**:
    - DELETE /api/tasks/{id} endpoint
    - Ownership verification
    - Deletes task from database
    - Returns 204 No Content

- [ ] **T038** [US2]: Register task routes in backend/app/main.py
  - **Agent**: @backend_agent
  - **Dependencies**: T032, T033, T034, T035, T036, T037
  - **Acceptance**:
    - Task router included in main.py
    - Routes accessible at /api/tasks/*

- [ ] **T039** [P] [US2]: Create frontend/lib/api.ts with API client functions: createTask, getTasks, getTask, updateTask, toggleComplete, deleteTask
  - **Agent**: @frontend_agent
  - **Dependencies**: T021
  - **Acceptance**:
    - `frontend/lib/api.ts` exists
    - All CRUD functions implemented
    - JWT token included in headers
    - Error handling

- [ ] **T040** [P] [US2]: Create frontend/components/TaskForm.tsx with title and description inputs, client-side validation
  - **Agent**: @frontend_agent
  - **Dependencies**: T021
  - **Acceptance**:
    - `frontend/components/TaskForm.tsx` exists
    - Title input (required, max 200)
    - Description textarea (optional, max 1000)
    - Client-side validation
    - Submit handler

- [ ] **T041** [P] [US2]: Create frontend/components/TaskItem.tsx with task display, checkbox for completion, edit/delete buttons, strikethrough for completed
  - **Agent**: @frontend_agent
  - **Dependencies**: T021
  - **Acceptance**:
    - `frontend/components/TaskItem.tsx` exists
    - Shows title, description, date
    - Checkbox toggles completion
    - Edit/delete buttons
    - Strikethrough style for completed

- [ ] **T042** [US2]: Create frontend/components/TaskList.tsx fetching tasks on mount, mapping to TaskItem, empty state, loading state
  - **Agent**: @frontend_agent
  - **Dependencies**: T039, T041
  - **Acceptance**:
    - `frontend/components/TaskList.tsx` exists
    - Fetches tasks on mount
    - Maps to TaskItem components
    - Shows loading spinner
    - Shows empty state message

- [ ] **T043** [US2]: Update frontend/app/dashboard/page.tsx to include TaskList and "New Task" button with modal
  - **Agent**: @frontend_agent
  - **Dependencies**: T042
  - **Acceptance**:
    - Dashboard shows TaskList
    - "New Task" button present
    - Modal opens TaskForm
    - Modal closes on submit/cancel

- [ ] **T044** [US2]: Implement task creation flow in frontend/app/dashboard/page.tsx with optimistic UI update
  - **Agent**: @frontend_agent
  - **Dependencies**: T040, T043
  - **Acceptance**:
    - TaskForm submits to API
    - Optimistic UI update
    - Refreshes on success
    - Error handling

- [ ] **T045** [US2]: Implement task update flow with inline editing or modal in TaskItem component
  - **Agent**: @frontend_agent
  - **Dependencies**: T041
  - **Acceptance**:
    - Edit button opens form
    - Updates via API
    - Optimistic UI update
    - Error handling

- [ ] **T046** [US2]: Implement task completion toggle in TaskItem component with optimistic update
  - **Agent**: @frontend_agent
  - **Dependencies**: T041
  - **Acceptance**:
    - Checkbox calls toggleComplete API
    - Optimistic UI update
    - Reverts on error

- [ ] **T047** [US2]: Implement task deletion flow in TaskItem component with confirmation modal
  - **Agent**: @frontend_agent
  - **Dependencies**: T041
  - **Acceptance**:
    - Delete button shows confirmation
    - Calls deleteTask API
    - Removes from UI
    - Error handling

- [ ] **T048** [US2]: Test task management: create → view → update → complete → delete, verify user isolation
  - **Agent**: @orchestrator
  - **Dependencies**: T038, T044, T045, T046, T047
  - **Acceptance**:
    - Can create tasks
    - Tasks appear in list
    - Can update tasks
    - Can toggle completion
    - Can delete tasks
    - User A cannot see User B's tasks

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Secure Session Management (Priority: P3)

**Goal**: JWT tokens are properly validated, expired tokens redirect to login, sessions persist across page refreshes

**Independent Test**: Log in → Refresh page (session persists) → Wait for token expiry → Access protected route (redirects to login)

### Implementation for User Story 3

- [ ] **T049** [US3]: Add token expiry validation in backend/app/routes/auth.py get_current_user dependency
  - **Agent**: @backend_agent
  - **Dependencies**: T022
  - **Acceptance**:
    - Checks token exp claim
    - Returns 401 if expired
    - Clear error message

- [ ] **T050** [US3]: Add automatic token refresh logic in frontend/lib/auth.ts for tokens nearing expiry
  - **Agent**: @frontend_agent
  - **Dependencies**: T020
  - **Acceptance**:
    - Checks token expiry on page load
    - Refreshes if < 1 day remaining
    - Updates stored token

- [ ] **T051** [US3]: Add error handling in frontend/lib/api.ts to catch 401 errors and redirect to login
  - **Agent**: @frontend_agent
  - **Dependencies**: T039
  - **Acceptance**:
    - Catches 401 responses
    - Clears auth state
    - Redirects to login page
    - Shows error message

- [ ] **T052** [US3]: Add session persistence check in frontend/app/dashboard/page.tsx on mount
  - **Agent**: @frontend_agent
  - **Dependencies**: T028
  - **Acceptance**:
    - Reads token from storage on mount
    - Validates token not expired
    - Redirects if invalid

- [ ] **T053** [US3]: Test session management: login → refresh page → verify persistence → test expired token → verify redirect
  - **Agent**: @orchestrator
  - **Dependencies**: T049, T050, T051, T052
  - **Acceptance**:
    - Session persists on refresh
    - Expired token redirects to login
    - Auto-refresh works

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] **T054** [P]: Add responsive styling with Tailwind CSS to all frontend components (mobile 320px+, tablet, desktop)
  - **Agent**: @frontend_agent
  - **Dependencies**: T043
  - **Acceptance**:
    - All components responsive
    - Mobile (320px+) tested
    - Tablet breakpoints work
    - Desktop layout optimal

- [ ] **T055** [P]: Add loading spinners to all async operations in frontend components
  - **Agent**: @frontend_agent
  - **Dependencies**: T043
  - **Acceptance**:
    - Loading states on all API calls
    - Spinners visible during requests
    - Disabled buttons while loading

- [ ] **T056** [P]: Add error toast notifications in frontend/components/Toast.tsx for user-friendly error messages
  - **Agent**: @frontend_agent
  - **Dependencies**: T002
  - **Acceptance**:
    - Toast component created
    - Shows on API errors
    - Auto-dismisses after 5s
    - Error/success variants

- [ ] **T057** [P]: Add empty state messages in TaskList component when no tasks exist
  - **Agent**: @frontend_agent
  - **Dependencies**: T042
  - **Acceptance**:
    - Empty state message when no tasks
    - Helpful CTA text
    - Styled nicely

- [ ] **T058** [P]: Create backend/Dockerfile for FastAPI deployment
  - **Agent**: @devops_agent
  - **Dependencies**: T014
  - **Acceptance**:
    - `backend/Dockerfile` exists
    - Builds successfully
    - Runs FastAPI app
    - Production-ready config

- [ ] **T059** [P]: Create frontend/README.md with setup instructions
  - **Agent**: @frontend_agent
  - **Dependencies**: T002
  - **Acceptance**:
    - README with setup steps
    - Environment variable list
    - Run instructions
    - Development guide

- [ ] **T060**: Test all API endpoints with Postman/curl: register, login, create/get/update/delete tasks, verify JWT validation
  - **Agent**: @orchestrator
  - **Dependencies**: T038
  - **Acceptance**:
    - All endpoints tested
    - JWT validation works
    - Error cases handled
    - Documentation updated

- [ ] **T061**: Test user isolation: create second user, verify cannot access first user's tasks
  - **Agent**: @orchestrator
  - **Dependencies**: T048
  - **Acceptance**:
    - User A tasks invisible to User B
    - API returns 404 for wrong user
    - No data leakage

- [ ] **T062**: Test error cases: invalid token, missing fields, wrong user, expired token
  - **Agent**: @orchestrator
  - **Dependencies**: T053
  - **Acceptance**:
    - Invalid token returns 401
    - Missing fields return 422
    - Wrong user returns 404
    - Expired token returns 401

- [ ] **T063**: Deploy backend to Render/Railway with environment variables, verify health check
  - **Agent**: @devops_agent
  - **Dependencies**: T058, T060
  - **Acceptance**:
    - Backend deployed to Render/Railway
    - Environment variables set
    - Health check endpoint works
    - HTTPS enabled

- [ ] **T064**: Deploy frontend to Vercel with NEXT_PUBLIC_API_URL pointing to backend, verify deployment
  - **Agent**: @devops_agent
  - **Dependencies**: T063
  - **Acceptance**:
    - Frontend deployed to Vercel
    - NEXT_PUBLIC_API_URL points to deployed backend
    - Deployment successful
    - HTTPS enabled

- [ ] **T065**: End-to-end testing on live app: signup → login → CRUD tasks → logout → login
  - **Agent**: @orchestrator
  - **Dependencies**: T064
  - **Acceptance**:
    - Full flow works on production
    - No console errors
    - All features functional

- [ ] **T066**: Create demo video (90 seconds) showing signup, task CRUD, upload to YouTube/Loom
  - **Agent**: @orchestrator
  - **Dependencies**: T065
  - **Acceptance**:
    - Video under 90 seconds
    - Shows signup, login, CRUD
    - Uploaded with public link
    - Clear audio/video quality

- [ ] **T067**: Prepare GitHub repository: add README.md, /specs folder, verify CLAUDE.md, push as public repo
  - **Agent**: @devops_agent
  - **Dependencies**: T059
  - **Acceptance**:
    - Repository is public
    - README comprehensive
    - /specs folder included
    - CLAUDE.md present
    - Clean commit history

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Requires US1 for authentication but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Enhances US1 but independently testable

### Within Each User Story

- Models before services (already in Foundational phase)
- Backend routes before frontend API client
- API client before UI components
- Individual components before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Within each story, tasks marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Agent Routing Summary

### By Agent:

**@db_auth_agent** (Database & Authentication):
- T008, T009, T010, T011, T012, T016, T017

**@backend_agent** (FastAPI Backend):
- T003, T005, T013, T014, T015, T018
- T022, T023, T024, T025
- T031-T038
- T049

**@frontend_agent** (Next.js Frontend):
- T002, T004, T006, T007
- T019, T020, T021, T026, T027, T028, T029
- T039-T047
- T050, T051, T052
- T054, T055, T056, T057, T059

**@devops_agent** (Deployment & Infrastructure):
- T001, T058, T063, T064, T067

**@orchestrator** (Testing & Coordination):
- T030, T048, T053, T060, T061, T062, T065, T066

---

## Parallel Example: User Story 2
```bash
# Launch all backend endpoints for User Story 2 together:
Task T032: "POST /api/tasks endpoint" (@backend_agent)
Task T033: "GET /api/tasks endpoint" (@backend_agent)
Task T034: "GET /api/tasks/{id} endpoint" (@backend_agent)
Task T035: "PUT /api/tasks/{id} endpoint" (@backend_agent)
Task T036: "PATCH /api/tasks/{id}/complete endpoint" (@backend_agent)
Task T037: "DELETE /api/tasks/{id} endpoint" (@backend_agent)

# Launch all frontend components for User Story 2 together:
Task T040: "TaskForm.tsx component" (@frontend_agent)
Task T041: "TaskItem.tsx component" (@frontend_agent)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Authentication)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Authentication)
   - Developer B: User Story 2 (Task Management) - starts after US1 auth is available
   - Developer C: User Story 3 (Session Management) - starts after US1 auth is available
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- **Agent** field enables sp.implement automation
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Tests are optional per constitution - manual testing via curl/Postman is sufficient

---

## Task Summary

**Total Tasks**: 67

**By Phase**:
- Phase 1 (Setup): 8 tasks
- Phase 2 (Foundational): 10 tasks
- Phase 3 (User Story 1 - Authentication): 12 tasks
- Phase 4 (User Story 2 - Task Management): 18 tasks
* **Phase 5 – User Story 3 (Session Management)**: 5 tasks
* **Phase 6 – Polish & Deployment**: 14 tasks

---

## Completion Criteria (Definition of Done)

The project is considered **DONE** when:

* ✅ All Phase 1 & Phase 2 tasks are completed (non-negotiable)
* ✅ At least **User Story 1 (Authentication)** works independently
* ✅ API health check returns `200 OK`
* ✅ JWT authentication is enforced on protected routes
* ✅ Users can only access their own data
* ✅ Frontend + Backend are deployed with HTTPS
* ✅ Manual testing completed via Postman / curl
* ✅ README + specs committed
* ✅ CLAUDE.md present and validated

---

## Validation Checklist (Final QA)

Before declaring success, verify:

### Backend

* [ ] FastAPI starts without errors
* [ ] `/` health check works
* [ ] `/api/auth/*` endpoints secured
* [ ] `/api/tasks/*` enforce user isolation
* [ ] Expired JWT returns `401`
* [ ] Neon DB connected and stable

### Frontend

* [ ] Auth persists on refresh
* [ ] Redirects work correctly
* [ ] Task CRUD works smoothly
* [ ] Loading + error states visible
* [ ] Mobile responsiveness verified

### Deployment

* [ ] Backend reachable via public URL
* [ ] Frontend uses deployed API URL
* [ ] Environment variables correctly set
* [ ] No secrets committed
* [ ] HTTPS enabled everywhere
---

## Final Note for Claude Code / Agents

* This task list is **Spec-Driven**
* Agents MUST follow:

  * File paths exactly
  * Dependencies strictly
  * No hallucinated APIs
* Stop execution at **each checkpoint**
* Ask user before skipping or modifying scope

---
