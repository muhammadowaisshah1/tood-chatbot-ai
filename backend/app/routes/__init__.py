"""
Routes package initialization.

This module exports all route modules for easy importing in main.py.
"""
from app.routes import auth, tasks, chat

__all__ = ["auth", "tasks", "chat"]