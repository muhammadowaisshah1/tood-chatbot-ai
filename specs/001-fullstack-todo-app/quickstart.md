# Quickstart Guide

**Feature**: Phase 2 Todo Full-Stack Web Application
**Date**: 2026-01-26
**Status**: Complete

## Overview

This guide will help you set up and run the Todo Full-Stack application locally in under 15 minutes.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** 18+ and npm/yarn ([Download](https://nodejs.org/))
- **Python** 3.11+ ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Neon Account** (free tier) - [Sign up](https://neon.tech/)

**Optional**:
- **Docker** and Docker Compose (for containerized development)
- **VS Code** with Python and TypeScript extensions

---

## Setup Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Hackthon_Full-Stack_App
git checkout 001-fullstack-todo-app
```

### 2. Set Up Database (Neon)

1. Go to [Neon Console](https://console.neon.tech/)
2. Create a new project: "todo-app-phase2"
3. Copy the connection string (looks like: `postgresql://user:password@host/database`)
4. Save it for the next step

### 3. Configure Environment Variables

#### Frontend (.env.local)

Create `frontend/.env.local`:

```bash
# Better Auth
BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters-long-please
BETTER_AUTH_URL=http://localhost:3000

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Generate a secure secret**:
```bash
# On Linux/Mac
openssl rand -base64 32

# On Windows (PowerShell)
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))
```

#### Backend (.env)

Create `backend/.env`:

```bash
# Database (paste your Neon connection string)
DATABASE_URL=postgresql+asyncpg://user:password@host/database

# Better Auth (MUST match frontend secret)
BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters-long-please

# JWT Configuration
JWT_ALGORITHM=HS256
JWT_EXPIRY_DAYS=7

# CORS (allow frontend origin)
CORS_ORIGINS=http://localhost:3000
```

**Important**: The `BETTER_AUTH_SECRET` must be identical in both frontend and backend!

### 4. Install Frontend Dependencies

```bash
cd frontend
npm install
# or
yarn install
```

**Expected packages**:
- next@16+
- react@19+
- typescript@5+
- tailwindcss@3+
- better-auth

### 5. Install Backend Dependencies

```bash
cd ../backend
pip install -r requirements.txt
```

**Expected packages**:
- fastapi
- sqlmodel
- pydantic
- python-jose[cryptography]
- passlib[bcrypt]
- asyncpg
- uvicorn[standard]

**Alternative (using virtual environment)**:
```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 6. Initialize Database

Run database migrations to create tables:

```bash
cd backend
python -c "from app.database import init_db; init_db()"
```

**Alternative (if using Alembic)**:
```bash
alembic upgrade head
```

**Verify tables created**:
```bash
# Connect to Neon database using psql or Neon SQL Editor
# Check tables exist:
\dt

# Expected output:
# users
# tasks
```

### 7. Start Development Servers

Open two terminal windows:

**Terminal 1 - Backend**:
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
# or
yarn dev
```

**Expected output**:
- Backend: `INFO: Uvicorn running on http://0.0.0.0:8000`
- Frontend: `✓ Ready on http://localhost:3000`

### 8. Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/docs (Swagger UI)

---

## Verify Installation

### Test Backend API

**Check health endpoint**:
```bash
curl http://localhost:8000/
```

Expected response: `{"message": "Todo API is running"}`

**Register a test user**:
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123",
    "name": "Test User"
  }'
```

Expected response (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "test@example.com",
  "name": "Test User",
  "created_at": "2026-01-26T10:30:00Z"
}
```

**Login**:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123"
  }'
```

Expected response (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "test@example.com",
    "name": "Test User"
  }
}
```

**Create a task** (replace `<TOKEN>` with the access_token from login):
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "title": "Test task",
    "description": "This is a test"
  }'
```

Expected response (201 Created):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Test task",
  "description": "This is a test",
  "completed": false,
  "created_at": "2026-01-26T10:35:00Z",
  "updated_at": "2026-01-26T10:35:00Z"
}
```

### Test Frontend

1. Open http://localhost:3000
2. Click "Sign Up"
3. Enter email, password, and name
4. Click "Create Account"
5. You should be redirected to the dashboard
6. Create a new task
7. Mark it as complete
8. Delete it

---

## Docker Setup (Alternative)

If you prefer using Docker:

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - BETTER_AUTH_URL=http://localhost:3000
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - JWT_ALGORITHM=HS256
      - JWT_EXPIRY_DAYS=7
      - CORS_ORIGINS=http://localhost:3000
```

### Run with Docker

```bash
# Build and start services
docker-compose up --build

# Stop services
docker-compose down
```

---

## Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`
- **Solution**: Install dependencies: `pip install -r requirements.txt`

**Error**: `sqlalchemy.exc.OperationalError: could not connect to server`
- **Solution**: Check `DATABASE_URL` in `.env` is correct
- Verify Neon database is running (check Neon console)

**Error**: `ValueError: BETTER_AUTH_SECRET must be at least 32 characters`
- **Solution**: Generate a longer secret (see step 3)

### Frontend won't start

**Error**: `Error: Cannot find module 'next'`
- **Solution**: Install dependencies: `npm install`

**Error**: `NEXT_PUBLIC_API_URL is not defined`
- **Solution**: Create `frontend/.env.local` with correct variables

**Error**: `Failed to fetch` when calling API
- **Solution**: Ensure backend is running on port 8000
- Check CORS configuration in backend

### Database issues

**Error**: `relation "users" does not exist`
- **Solution**: Run database migrations (step 6)

**Error**: `duplicate key value violates unique constraint "users_email_key"`
- **Solution**: User already exists, use different email or login

### JWT token issues

**Error**: `Invalid or expired token`
- **Solution**: Token expired (7 days), login again
- Check `BETTER_AUTH_SECRET` matches in frontend and backend

**Error**: `Signature verification failed`
- **Solution**: `BETTER_AUTH_SECRET` mismatch between frontend and backend
- Ensure both use the exact same secret

---

## Development Workflow

### Making Changes

1. **Backend changes**: Server auto-reloads with `--reload` flag
2. **Frontend changes**: Next.js hot-reloads automatically
3. **Database schema changes**: Update models in `backend/app/models.py`, then run migrations

### Testing API Endpoints

Use the interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Or use curl/Postman with the examples above.

### Viewing Database

**Option 1: Neon SQL Editor**
1. Go to Neon Console
2. Select your project
3. Click "SQL Editor"
4. Run queries: `SELECT * FROM users;`

**Option 2: psql**
```bash
psql "postgresql://user:password@host/database"
\dt  # List tables
SELECT * FROM users;
SELECT * FROM tasks;
```

**Option 3: Database GUI**
- DBeaver
- pgAdmin
- TablePlus

---

## Next Steps

After successful setup:

1. **Explore the codebase**:
   - Frontend: `frontend/app/` and `frontend/components/`
   - Backend: `backend/app/routes/` and `backend/app/models.py`

2. **Review the specification**:
   - Read `specs/001-fullstack-todo-app/spec.md`
   - Understand user stories and acceptance criteria

3. **Start implementing**:
   - Run `/sp.tasks` to generate task breakdown
   - Follow tasks in priority order (P1 → P2 → P3)

4. **Test as you go**:
   - Use curl commands to test API endpoints
   - Test frontend flows manually
   - Verify user isolation (create multiple users)

---

## Useful Commands

### Backend

```bash
# Start server
uvicorn app.main:app --reload

# Run tests
pytest

# Check Python types
mypy app/

# Format code
black app/

# Lint code
flake8 app/
```

### Frontend

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run type checking
npm run type-check

# Lint code
npm run lint
```

### Database

```bash
# Create migration (if using Alembic)
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Reset database (WARNING: deletes all data)
alembic downgrade base
alembic upgrade head
```

---

## Environment Variables Reference

### Frontend

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| BETTER_AUTH_SECRET | Yes | Shared secret for JWT (min 32 chars) | `abc123...` |
| BETTER_AUTH_URL | Yes | Frontend URL | `http://localhost:3000` |
| NEXT_PUBLIC_API_URL | Yes | Backend API URL | `http://localhost:8000` |

### Backend

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| DATABASE_URL | Yes | PostgreSQL connection string | `postgresql+asyncpg://...` |
| BETTER_AUTH_SECRET | Yes | Shared secret (must match frontend) | `abc123...` |
| JWT_ALGORITHM | Yes | JWT signing algorithm | `HS256` |
| JWT_EXPIRY_DAYS | Yes | Token expiry in days | `7` |
| CORS_ORIGINS | Yes | Allowed origins (comma-separated) | `http://localhost:3000` |

---

## Support

If you encounter issues:

1. Check this troubleshooting section
2. Review error messages carefully
3. Verify environment variables are set correctly
4. Ensure all prerequisites are installed
5. Check that both frontend and backend are running

For additional help:
- Review the [specification](./spec.md)
- Check the [API contracts](./contracts/api.yaml)
- Read the [data model](./data-model.md)

---

## Summary

You should now have:
- ✅ Frontend running on http://localhost:3000
- ✅ Backend running on http://localhost:8000
- ✅ Database initialized with tables
- ✅ Ability to register, login, and manage tasks

**Ready to start implementing!** Run `/sp.tasks` to generate the implementation task list.
