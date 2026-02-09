"""
SQLModel database models for the Todo application.

This module defines the database schema using SQLModel ORM.
Models include User and Task entities with proper relationships.
"""

from __future__ import annotations

from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.orm import relationship as sa_relationship
from sqlalchemy import Column, Enum as SQLAlchemyEnum
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from uuid import uuid4
import enum

if TYPE_CHECKING:
    pass


def generate_uuid() -> str:
    """Generate a UUID string for primary keys."""
    return str(uuid4())


# Enum for message roles
class MessageRole(str, enum.Enum):
    """Enum for message roles in conversations."""
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    SYSTEM = "system"


# Base configuration for SQLModel
# All models will inherit from SQLModel with table=True


class User(SQLModel, table=True):
    """
    User model representing authenticated users in the system.

    Attributes:
        id: Unique identifier (UUID as string)
        email: User's email address (unique, indexed)
        name: User's display name
        hashed_password: Bcrypt hashed password (managed by Better Auth)
        created_at: Timestamp of user creation
        tasks: Relationship to user's tasks
    """
    __tablename__ = "users"

    id: Optional[str] = Field(
        default_factory=generate_uuid,
        primary_key=True,
        max_length=36
    )
    email: str = Field(
        unique=True,
        index=True,
        max_length=255
    )
    name: str = Field(max_length=200)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships using sa_relationship to avoid resolution issues with generic type hints
    tasks: list[Task] = Relationship(
        sa_relationship=sa_relationship("Task", back_populates="user")
    )
    conversations: list[Conversation] = Relationship(
        sa_relationship=sa_relationship("Conversation", back_populates="user")
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"


class Task(SQLModel, table=True):
    """
    Task model representing todo items.

    Attributes:
        id: Unique identifier (auto-increment)
        user_id: Foreign key to users table
        title: Task title
        description: Optional task description
        completed: Task completion status
        created_at: Timestamp of task creation
        updated_at: Timestamp of last update
        category: Optional task category (e.g., work, personal, shopping)
        priority: Task priority level (low, medium, high)
        due_date: Optional task deadline
        order: Custom ordering for drag-drop functionality
        user: Relationship to task owner
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        max_length=36
    )
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Phase 2 fields - Advanced task management
    category: Optional[str] = Field(default=None, max_length=50)
    priority: Optional[str] = Field(default="medium", max_length=20)
    due_date: Optional[datetime] = Field(default=None)
    order: int = Field(default=0)

    user: User = Relationship(
        sa_relationship=sa_relationship("User", back_populates="tasks")
    )

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title={self.title}, completed={self.completed})>"


class Conversation(SQLModel, table=True):
    """
    Conversation model representing a chat session.
    """
    __tablename__ = "conversations"

    id: Optional[str] = Field(
        default_factory=generate_uuid,
        primary_key=True,
        max_length=36
    )
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        max_length=36
    )
    title: str = Field(default="New Chat", max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: User = Relationship(
        sa_relationship=sa_relationship("User", back_populates="conversations")
    )
    messages: list[Message] = Relationship(
        sa_relationship=sa_relationship("Message", back_populates="conversation")
    )

    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, title={self.title})>"


class Message(SQLModel, table=True):
    """
    Message model representing a single chat message.
    """
    __tablename__ = "messages"

    id: Optional[str] = Field(
        default_factory=generate_uuid,
        primary_key=True,
        max_length=36
    )
    conversation_id: str = Field(
        foreign_key="conversations.id",
        index=True,
        max_length=36
    )
    role: MessageRole = Field(
        sa_column=Column(SQLAlchemyEnum(MessageRole, name="messagerole", create_type=False)),
        description="user, assistant, tool, or system"
    )
    content: str = Field(description="The text content or tool result")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    conversation: Conversation = Relationship(
        sa_relationship=sa_relationship("Conversation", back_populates="messages")
    )

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, role={self.role})>"
