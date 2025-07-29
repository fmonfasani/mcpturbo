"""
MCPturbo Agents - Agent Base Classes and Lifecycle Management v2

Enhanced agent system supporting both local and external AI agents.
"""

__version__ = "2.0.0"
__author__ = "Federico Monfasani"

from .base_agent import (
    BaseAgent,
    AgentConfig,
    AgentCapability,
    AgentStatus,
    AgentType,
    create_local_agent,
    create_external_agent,
    LocalAgent,
    ExternalAgent,
    HybridAgent,
)
from .registry import AgentRegistry
from .genesis_agent import GenesisAgent

__all__ = [
    "BaseAgent",
    "LocalAgent",
    "ExternalAgent",
    "HybridAgent",
    "GenesisAgent",
    "AgentConfig",
    "AgentCapability",
    "AgentType",
    "AgentStatus",
    "AgentRegistry",
    "create_local_agent",
    "create_external_agent",
    "__version__",
    "__author__",
]

registry = AgentRegistry()


def register_agent(agent: BaseAgent, **kwargs) -> None:
    """Register agent in global registry and protocol."""
    registry.register(agent)
    try:
        from mcpturbo_core.protocol import protocol

        protocol.register_agent(agent.config.agent_id, agent, **kwargs)
    except ImportError:  # pragma: no cover - optional core
        pass


def get_agent(agent_id: str) -> BaseAgent | None:
    """Retrieve agent from global registry."""
    return registry.get(agent_id)


def list_agents() -> list[str]:
    """List all registered agent IDs."""
    return registry.list_agents()


def create_simple_agent(agent_id: str, name: str | None = None) -> LocalAgent:
    """Create and register a simple local agent."""
    agent = create_local_agent(agent_id, name)
    register_agent(agent)
    return agent
