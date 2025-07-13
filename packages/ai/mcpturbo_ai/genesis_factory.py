from typing import Dict
from mcpturbo_agents import BaseAgent
from mcpturbo_orchestrator import orchestrator

from .genesis_agents import (
    GenesisArchitectAgent,
    GenesisBackendAgent,
    GenesisFrontendAgent,
    GenesisDevOpsAgent,
)


def create_genesis_agents() -> Dict[str, BaseAgent]:
    """Instantiate all Genesis agents."""
    agents = {
        "genesis_architect": GenesisArchitectAgent(),
        "genesis_backend": GenesisBackendAgent(),
        "genesis_frontend": GenesisFrontendAgent(),
        "genesis_devops": GenesisDevOpsAgent(),
    }
    return agents


def setup_genesis_environment() -> Dict[str, BaseAgent]:
    """Create and register Genesis agents with the global orchestrator."""
    agents = create_genesis_agents()
    for agent in agents.values():
        orchestrator.register_agent(agent)
    return agents

