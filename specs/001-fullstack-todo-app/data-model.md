# Data Model

**Feature**: Phase 2 Todo Full-Stack Web Application
**Date**: 2026-01-26
**Status**: Complete

## Overview

This document defines the database schema for the todo application. The data model consists of two primary entities: User and Task, with a one-to-many relationship enforcing strict user isolation.

## Entity Relationship Diagram

```
┌─────────────────────────┐
│         User            │
│─────────────────────────│
│ id: UUID (PK)           │
│ email: VARCHAR(255) UQ  │
│ password_hash: VARCHAR  │
│ name: VARCHAR(100)      │
│ created_at: TIMESTAMP   │
└────────────┬────────────┘
             │
             │ 1:N
             │
             ▼
┌─────────────────────────┐
│         Task            │
│─────────────────────────│
│ id: SERIAL (PK)         │
│ user_id: UUID (FK)      │
│ title: VARCHAR(200)     │
│ description: TEXT       │
│ completed: BOOLEAN      │
│ created_at: TIMESTAMP   │
│ updated_at: TIMESTAMP   │
└─────────────────────────┘
```

## Entities

### User

Represents a registered user account with authentication credentials.

**Table Name**: `users`

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address (login identifier) |
| password_hash | VARCHAR(255) | NOT NULL | Hashed password (never store plain text) |
| name | VARCHAR(100) | NOT NULL | User's display name |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation timestamp |

**Indexes**:
- Primary key index on `id` (automatic)
- Unique index on `email` (for login lookups)

**Validation Rules**:
- Email must be valid format (validated by Better Auth)
- Password minimum 8 characters (validated by Better Auth)
- Name required, 1-100 characters

**SQLModel Definition**:

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    password_hash: str = Field(max_length=255)
    name: str = Field(max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship (not stored in DB, for ORM convenience)
    # tasks: list["Task"] = Relationship(back_populates="user")
```

**Security Notes**:
- Password is hashed using Better Auth (bcrypt/argon2)
- Never expose password_hash in API responses
- Email is case-insensitive for lookups (normalize to lowercase)

---

### Task

Represents a todo item belonging to a single user.

**Table Name**: `tasks`

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Unique task identifier |
| user_id | UUID | FOREIGN KEY (users.id), NOT NULL | Owner of the task |
| title | VARCHAR(200) | NOT NULL | Task title (required) |
| description | TEXT | NULL | Optional task description |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Task creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes**:
- Primary key index on `id` (automatic)
- Index on `user_id` (for fast filtering by user)
- Index on `completed` (for status filtering)
- Composite index on `(user_id, completed)` (for filtered queries)

**Foreign Keys**:
- `user_id` REFERENCES `users(id)` ON DELETE CASCADE
  - When a user is deleted, all their tasks are automatically deleted

**Validation Rules**:
- Title: Required, 1-200 characters
- Description: Optional, max 1000 characters
- Completed: Boolean (true/false)
- user_id: Must reference existing user

**SQLModel Definition**:

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200, min_length=1)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship (not stored in DB, for ORM convenience)
    # user: Optional[User] = Relationship(back_populates="tasks")
```

**Business Rules**:
- Tasks are private to the user who created them
- All queries MUST filter by authenticated user_id
- Soft delete not implemented (permanent deletion)
- No task sharing or collaboration in Phase 2

---

## Relationships

### User → Task (One-to-Many)

- One user can have zero or more tasks
- Each task belongs to exactly one user
- Relationship enforced by foreign key constraint
- Cascade delete: Deleting a user deletes all their tasks

**Query Examples**:

```python
# Get all tasks for a user
tasks = session.exec(
    select(Task).where(Task.user_id == current_user_id)
).all()

# Get completed tasks for a user
completed_tasks = session.exec(
    select(Task)
    .where(Task.user_id == current_user_id)
    .where(Task.completed == True)
).all()

# Get single task (with user validation)
task = session.exec(
    select(Task)
    .where(Task.id == task_id)
    .where(Task.user_id == current_user_id)
).first()
```

---

## Database Schema (SQL)

### Create Tables

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
```

### Constraints

```sql
-- Email must be unique (case-insensitive)
ALTER TABLE users ADD CONSTRAINT users_email_unique UNIQUE (email);

-- Title must not be empty
ALTER TABLE tasks ADD CONSTRAINT tasks_title_not_empty CHECK (LENGTH(title) > 0);

-- Title length limit
ALTER TABLE tasks ADD CONSTRAINT tasks_title_length CHECK (LENGTH(title) <= 200);

-- Description length limit
ALTER TABLE tasks ADD CONSTRAINT tasks_description_length CHECK (description IS NULL OR LENGTH(description) <= 1000);
```

---

## Migration Strategy

### Phase 2 (Initial Setup)

Use SQLModel's automatic table creation:

```python
from sqlmodel import SQLModel, create_engine

engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)
```

This creates all tables with proper constraints and indexes.

### Phase 3+ (Production)

For production environments, use Alembic for versioned migrations:

```bash
# Initialize Alembic
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

---

## Data Integrity Rules

### User Isolation

**Critical Security Requirement**: Every task query MUST filter by authenticated user_id.

**Correct**:
```python
# ✅ Correct: Filter by user_id from JWT token
task = session.exec(
    select(Task)
    .where(Task.id == task_id)
    .where(Task.user_id == current_user_id)
).first()
```

**Incorrect**:
```python
# ❌ WRONG: No user_id filter - security vulnerability!
task = session.exec(
    select(Task).where(Task.id == task_id)
).first()
```

### Timestamp Management

- `created_at`: Set once on creation, never updated
- `updated_at`: Updated on every modification

**Implementation**:
```python
# On create
task = Task(
    title=title,
    description=description,
    user_id=current_user_id,
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow()
)

# On update
task.title = new_title
task.updated_at = datetime.utcnow()
```

### Cascade Deletion

When a user is deleted, all their tasks are automatically deleted due to `ON DELETE CASCADE` constraint. This prevents orphaned tasks.

**Alternative**: If user deletion is not allowed in Phase 2, this is not a concern.

---

## Performance Considerations

### Index Usage

**Query**: Get all tasks for a user
```sql
SELECT * FROM tasks WHERE user_id = ?
```
**Index Used**: `idx_tasks_user_id`
**Expected Performance**: <10ms for 1000 tasks

**Query**: Get completed tasks for a user
```sql
SELECT * FROM tasks WHERE user_id = ? AND completed = true
```
**Index Used**: `idx_tasks_user_completed` (composite index)
**Expected Performance**: <10ms for 1000 tasks

### Connection Pooling

SQLModel/SQLAlchemy manages connection pooling automatically:
- Default pool size: 5 connections
- Max overflow: 10 connections
- Pool recycle: 3600 seconds (1 hour)

For Neon serverless PostgreSQL, connection pooling is handled by Neon's proxy.

### Query Optimization

- Use `select()` instead of raw SQL (SQLModel handles optimization)
- Avoid N+1 queries (not applicable in Phase 2 - no nested relationships)
- Use pagination for large result sets (future enhancement)

---

## API Response Models

### User Response (Public)

```python
class UserResponse(BaseModel):
    id: UUID
    email: str
    name: str
    created_at: datetime

    # Never include password_hash in responses!
```

### Task Response

```python
class TaskResponse(BaseModel):
    id: int
    user_id: UUID
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
```

### Task Create Request

```python
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)

    # user_id is NOT in request - extracted from JWT token
    # completed defaults to False
```

### Task Update Request

```python
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)

    # Only fields provided are updated
    # created_at is never updated
    # updated_at is automatically set
```

---

## Testing Data

### Sample Users

```sql
INSERT INTO users (id, email, password_hash, name) VALUES
('550e8400-e29b-41d4-a716-446655440000', 'alice@example.com', '$2b$12$...', 'Alice'),
('550e8400-e29b-41d4-a716-446655440001', 'bob@example.com', '$2b$12$...', 'Bob');
```

### Sample Tasks

```sql
INSERT INTO tasks (user_id, title, description, completed) VALUES
('550e8400-e29b-41d4-a716-446655440000', 'Buy groceries', 'Milk, eggs, bread', false),
('550e8400-e29b-41d4-a716-446655440000', 'Finish project', 'Complete Phase 2 implementation', false),
('550e8400-e29b-41d4-a716-446655440001', 'Call dentist', NULL, true);
```

---

## Summary

The data model is simple, secure, and optimized for Phase 2 requirements:

- ✅ Two entities: User and Task
- ✅ One-to-many relationship with cascade delete
- ✅ Proper indexes for <200ms query performance
- ✅ User isolation enforced at database level
- ✅ Type safety with SQLModel
- ✅ Validation rules aligned with functional requirements

**Ready for implementation** with clear schema definitions and query patterns.
