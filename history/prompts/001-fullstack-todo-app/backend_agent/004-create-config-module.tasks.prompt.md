---
id: 004
title: Create Configuration Module with Pydantic Settings
stage: tasks
date: 2026-01-27T23:20:00Z
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-fullstack-todo-app
branch: 001-fullstack-todo-app
user: backend_agent
command: sp.implement
labels: [backend, configuration, pydantic-settings, environment-variables]
links:
  spec: specs/001-fullstack-todo-app/spec.md
  ticket: T013
  adr: null
  pr: null
files:
  - path: backend/app/config.py
    status: created
    lines: 253
tests:
  - type: import
    description: Configuration module imports successfully
    status: passed
  - type: validation
    description: Environment variables loaded and validated
    status: passed
---

## Prompt

Execute Task T013: Create backend/app/config.py to load environment variables using pydantic-settings

**File**: backend/app/config.py

**Requirements**:
- Pydantic Settings class
- Loads from backend/.env file
- All required config vars: DATABASE_URL, BETTER_AUTH_SECRET, JWT_ALGORITHM, JWT_EXPIRY_DAYS, CORS_ORIGINS

**Context**: Configuration management for FastAPI backend using pydantic-settings.

## Response snapshot

Created a comprehensive configuration module using pydantic-settings with the following features:

**Core Configuration Class (Settings)**:
- Centralized configuration management using Pydantic BaseSettings
- Type-safe environment variable loading with validation
- Automatic .env file parsing

**Configuration Categories**:
1. Database Configuration
   - DATABASE_URL with format validation

2. Authentication Configuration
   - BETTER_AUTH_SECRET (minimum 32 characters)
   - JWT_ALGORITHM (default: HS256)
   - JWT_EXPIRY_DAYS (default: 7, range: 1-365)

3. CORS Configuration
   - CORS_ORIGINS with URL format validation
   - Helper method to get origins as list

4. Server Configuration
   - SERVER_HOST (default: 0.0.0.0)
   - SERVER_PORT (default: 8001, range: 1024-65535)

5. Application Configuration
   - APP_NAME, APP_VERSION, DEBUG mode

**Validation Features**:
- Field validators for DATABASE_URL format
- CORS origins URL validation
- JWT secret strength validation
- Automatic validation on import

**Helper Methods**:
- `get_cors_origins_list()`: Parse comma-separated origins
- `is_production()`: Check if running in production mode
- `validate_settings()`: Additional startup validation

**Global Instance**:
- Single `settings` instance exported for app-wide use
- Configuration loaded once and reused

**Testing**:
- Successfully imported and loaded configuration
- All environment variables validated correctly
- CORS origins parsed as list: ['http://localhost:3000']
- Server configuration: 0.0.0.0:8001
- Production mode: True (DEBUG=False)

## Outcome

- Impact: Centralized configuration management for entire backend application. Replaces scattered os.getenv() calls with type-safe, validated settings.
- Tests: Import test passed, validation test passed, all environment variables loaded correctly
- Files: Created backend/app/config.py (253 lines)
- Next prompts: Update db.py and auth.py to use settings instead of direct environment variable access
- Reflection: Configuration module provides strong type safety and validation. The field validators ensure critical settings like DATABASE_URL and CORS_ORIGINS are properly formatted. The global settings instance pattern ensures configuration is loaded once and reused throughout the application.

## Evaluation notes (flywheel)

- Failure modes observed: None. Configuration loaded successfully on first attempt.
- Graders run and results (PASS/FAIL): Import test PASS, Validation test PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Refactor existing modules (db.py, auth.py) to import from config.settings instead of using os.getenv() directly
