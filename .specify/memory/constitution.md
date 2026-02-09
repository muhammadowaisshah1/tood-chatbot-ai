# Todo Full-Stack Web Application (Phase 2) Constitution

<!--
Sync Impact Report:
- Version: Initial → 1.0.0
- Type: New constitution creation
- Ratification: 2026-01-26
- Modified Principles: N/A (initial creation)
- Added Sections: All sections (initial creation)
- Templates Status:
  ✅ Constitution created
  ⚠ plan-template.md - requires review for alignment
  ⚠ spec-template.md - requires review for alignment
  ⚠ tasks-template.md - requires review for alignment
- Follow-up TODOs: Review dependent templates for consistency with new principles
-->

## Core Principles

### I. Monorepo Architecture & RESTful Design

**MUST** maintain strict separation between frontend and backend in `/frontend` and `/backend` folders.
**MUST** use RESTful API design with proper HTTP methods (GET, POST, PUT, DELETE).
**MUST** keep backend stateless with JWT-based authentication.
**MUST** store all secrets and configuration in environment variables, never hardcoded.

**Rationale**: Clear separation enables independent deployment, testing, and scaling. RESTful design ensures predictable API behavior. Stateless architecture allows horizontal scaling and simplifies deployment.

### II. User Isolation & Data Security

**MUST** validate user ID on every API request using JWT token claims.
**MUST** ensure each user sees only their own tasks through database-level filtering.
**MUST** never expose user data across user boundaries.
**MUST** implement proper CORS configuration for frontend-backend communication.

**Rationale**: Multi-user applications require strict data isolation to prevent unauthorized access. User ID validation at every endpoint is the primary defense against data leakage.

### III. Security-First Development

**MUST** require JWT tokens for all API endpoints (no public endpoints except auth).
**MUST** use Better Auth for password hashing and authentication flows.
**MUST** never store sensitive data in localStorage or client-side storage.
**MUST** validate and sanitize all user inputs on the backend.
**MUST** return appropriate HTTP status codes: 401 for unauthorized, 403 for forbidden, 404 for not found.

**Rationale**: Security cannot be retrofitted. JWT tokens provide stateless authentication. Better Auth handles password security correctly. Input validation prevents injection attacks.

### IV. Type Safety & Error Handling

**MUST** use TypeScript strict mode in frontend code.
**MUST** use Python type hints in all backend functions and classes.
**MUST** implement error handling on all API endpoints with try-catch blocks.
**MUST** use async/await for all I/O operations (database, API calls).
**MUST** return proper HTTP status codes (200, 201, 400, 401, 404, 500) with descriptive error messages.

**Rationale**: Type safety catches errors at compile time. Explicit error handling prevents crashes and provides better debugging information. Async/await ensures non-blocking operations.

### V. Performance & Optimization

**MUST** achieve API response time < 200ms for CRUD operations.
**MUST** optimize database queries with proper indexes on frequently queried fields.
**MUST** use Next.js Server Components by default; Client Components only when interactivity required.
**MUST** implement proper loading states in frontend components.

**Rationale**: Performance is a feature. Sub-200ms response times provide good user experience. Server Components reduce JavaScript bundle size and improve initial page load.

### VI. Testing & Database Reliability

**MUST** ensure all API endpoints are testable with clear inputs and outputs.
**MUST** make database migrations reversible with proper up/down scripts.
**MUST** handle loading, error, and empty states in frontend components.
**MUST** use SQLModel ORM for all database operations (no raw SQL).

**Rationale**: Testability enables confidence in changes. Reversible migrations allow safe rollbacks. ORM prevents SQL injection and provides type safety.

## Tech Stack Constraints

### Frontend Stack
- **Framework**: Next.js 16+ with App Router (Pages Router forbidden)
- **Language**: TypeScript with strict mode enabled
- **Styling**: Tailwind CSS
- **Deployment**: Vercel

### Backend Stack
- **Framework**: Python FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT tokens
- **Deployment**: Separate from frontend (not Vercel)

### Required Tools
- Environment variable management (.env files, never committed)
- Type checking (TypeScript compiler, mypy for Python)
- Database migration tools compatible with SQLModel

## Forbidden Practices

The following practices are **EXPLICITLY FORBIDDEN** and MUST be rejected in code review:

1. **No inline SQL queries** - Use SQLModel ORM exclusively
2. **No localStorage for sensitive data** - JWT tokens, user IDs, or personal information
3. **No mixing backend logic in frontend** - API calls only, no direct database access
4. **No user data leakage** - Every query MUST filter by authenticated user ID
5. **No hardcoded credentials** - Database URLs, API keys, secrets MUST be in environment variables
6. **No Pages Router** - Next.js App Router only
7. **No untyped code** - TypeScript strict mode, Python type hints required

**Rationale**: These practices lead to security vulnerabilities, maintenance nightmares, or architectural violations. They are non-negotiable.

## Development Workflow

### Code Standards Checklist
Before any PR is approved, verify:
- [ ] TypeScript strict mode passes with no errors
- [ ] Python type hints present on all functions
- [ ] All API endpoints have error handling
- [ ] User ID validation present on protected endpoints
- [ ] Environment variables used for all secrets
- [ ] Database queries use SQLModel (no raw SQL)
- [ ] Proper HTTP status codes returned
- [ ] Loading states implemented in UI components

### Testing Requirements
- All API endpoints MUST be manually testable via curl or Postman
- Database migrations MUST have both up and down scripts
- Frontend components MUST handle loading, error, and empty states

### Performance Validation
- API endpoints MUST respond in < 200ms for CRUD operations
- Database queries MUST use indexes on user_id and frequently queried fields
- Frontend MUST use Server Components by default

## Governance

This constitution supersedes all other development practices and guidelines. All code changes, architecture decisions, and technical discussions MUST align with these principles.

### Amendment Process
1. Proposed changes MUST be documented with rationale
2. Version number MUST be incremented according to semantic versioning:
   - **MAJOR**: Backward-incompatible principle removals or redefinitions
   - **MINOR**: New principles added or material expansions
   - **PATCH**: Clarifications, wording fixes, non-semantic refinements
3. All dependent templates and documentation MUST be updated
4. Migration plan required for breaking changes

### Compliance Review
- All PRs MUST verify compliance with constitution principles
- Architecture decisions MUST reference relevant principles
- Complexity MUST be justified against simplicity principle
- Security violations result in immediate PR rejection

### Version Control
This constitution is version-controlled in `.specify/memory/constitution.md`. Changes MUST be committed with descriptive messages following the format: `docs: amend constitution to vX.Y.Z (brief description)`.

**Version**: 1.0.0 | **Ratified**: 2026-01-26 | **Last Amended**: 2026-01-26
