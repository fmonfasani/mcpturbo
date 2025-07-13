"""Integration helpers for the ``genesis`` project initializer."""

from typing import Any, Dict
import os

from mcpturbo_core import quick_setup
from mcpturbo_ai import create_multi_llm_setup
from mcpturbo_orchestrator import orchestrator


async def genesis_setup() -> Dict[str, Any]:
    """Setup orchestrator with agents based on environment variables."""
    # Load configuration and set environment variables via quick_setup
    config = quick_setup()

    agents = create_multi_llm_setup(
        openai_key=config.openai_api_key,
        claude_key=config.claude_api_key,
        deepseek_key=config.deepseek_api_key,
    )

    for agent in agents.values():
        orchestrator.register_agent(agent)

    return {
        "agents": list(agents.keys()),
        "config": config,
    }


async def genesis_init(project_name: str, app_type: str = "web") -> Dict[str, Any]:
    """Initialize a new project using the orchestrator workflow."""
    await genesis_setup()
    workflow_id = await orchestrator.create_workflow_from_template(
        "app_generation", app_name=project_name, app_type=app_type
    )
    result = await orchestrator.execute_workflow(workflow_id)
    return result

__all__ = ["genesis_setup", "genesis_init"]

