/**
 * TypeScript type definitions for the Todo application.
 *
 * These types match the backend API response schemas defined in:
 * - backend/app/schemas.py (Pydantic schemas)
 * - backend/app/models.py (SQLModel database models)
 */

/**
 * User interface representing authenticated users.
 *
 * Corresponds to backend UserResponse schema.
 */
export interface User {
  /** Unique identifier (UUID as string) */
  id: string;

  /** User's email address */
  email: string;

  /** User's display name */
  name: string;

  /** Registration timestamp (ISO 8601 format) */
  created_at: string;
}

/**
 * Task interface representing todo items.
 *
 * Corresponds to backend TaskResponse schema.
 */
export interface Task {
  /** Unique identifier (auto-increment integer) */
  id: number;

  /** Owner's user ID (UUID as string) */
  user_id: string;

  /** Task title (1-200 characters) */
  title: string;

  /** Optional task description (max 1000 characters) */
  description: string | null;

  /** Task completion status */
  completed: boolean;

  /** Creation timestamp (ISO 8601 format) */
  created_at: string;

  /** Last update timestamp (ISO 8601 format) */
  updated_at: string;

  /** Optional task category (e.g., work, personal, shopping) */
  category: string | null;

  /** Task priority level (low, medium, high) */
  priority: string | null;

  /** Optional task deadline (ISO 8601 format) */
  due_date: string | null;

  /** Custom order position for drag-drop functionality */
  order: number;
}

/**
 * Authentication response interface.
 *
 * Returned after successful login or registration.
 */
export interface AuthResponse {
  /** Authenticated user information */
  user: User;

  /** JWT access token for API authentication */
  access_token: string;

  /** Token type (always "bearer") */
  token_type: string;
}
