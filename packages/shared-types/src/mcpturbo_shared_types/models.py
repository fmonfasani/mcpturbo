"""Pydantic models shared across MCPturbo packages."""

from __future__ import annotations

from typing import List
from uuid import uuid4

from pydantic import BaseModel, Field


class Message(BaseModel):
    """Represents a message exchanged between actors."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    role: str
    content: str

    def to_dict(self) -> dict:
        """Return a serialisable dictionary representation of the message."""
        return self.model_dump()


class Task(BaseModel):
    """A unit of work consisting of multiple messages."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    messages: List[Message] = []

    def to_dict(self) -> dict:
        """Return a serialisable dictionary representation of the task."""
        return self.model_dump()


class Workflow(BaseModel):
    """A workflow composed of ordered tasks."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    tasks: List[Task] = []

    def to_dict(self) -> dict:
        """Return a serialisable dictionary representation of the workflow."""
        return self.model_dump()
