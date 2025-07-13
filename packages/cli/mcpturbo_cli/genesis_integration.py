"""Integration helpers for the `genesis` command set."""

from __future__ import annotations

import os
from typing import Any, Dict

try:  # Optional runtime dependency
    from mcpturbo_orchestrator import orchestrator, setup_orchestrator, generate_app
except Exception:  # pragma: no cover - orchestrator might not be installed
    orchestrator = None  # type: ignore
    async def setup_orchestrator(*args, **kwargs):  # type: ignore
        raise ImportError("mcpturbo_orchestrator is required")

    async def generate_app(*args, **kwargs):  # type: ignore
        raise ImportError("mcpturbo_orchestrator is required")


__all__ = ["genesis_init", "genesis_setup"]


async def genesis_setup() -> Any:
    """Setup orchestrator with agents created from environment variables."""
    from mcpturbo_ai import create_multi_llm_setup  # Local import for optional dependency
    openai_key = os.getenv("OPENAI_API_KEY")
    claude_key = os.getenv("CLAUDE_API_KEY")
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")

    agents: Dict[str, Any] = create_multi_llm_setup(
        openai_key=openai_key,
        claude_key=claude_key,
        deepseek_key=deepseek_key,
    )

    if agents:
        await setup_orchestrator(*agents.values())

    return orchestrator


async def genesis_init(project_name: str, app_type: str = "web", **kwargs: Any) -> Any:
    """Initialize a new project using the orchestrator templates."""
    await genesis_setup()
    return await generate_app(project_name, app_type=app_type, **kwargs)
