"""
MCPturbo Agents - Agent Base Classes and Lifecycle Management v2

Enhanced agent system supporting both local and external AI agents.
"""

__version__ = "2.0.0"
__author__ = "Federico Monfasani"

# Base agent classes
from .base_agent import (
    BaseAgent, LocalAgent, ExternalAgent, HybridAgent,
    AgentType, AgentStatus, AgentCapability, AgentConfig,
    create_local_agent, create_external_agent
)

# Registry for managing agents
from .registry import AgentRegistry

# Main exports
__all__ = [
    # Base classes
    "BaseAgent",
    "LocalAgent", 
    "ExternalAgent",
    "HybridAgent",
    
    # Configuration and types
    "AgentConfig",
    "AgentCapability",
    "AgentType",
    "AgentStatus",
    
    # Registry
    "AgentRegistry",
    
    # Factory functions
    "create_local_agent",
    "create_external_agent",
    
    # Metadata
    "__version__",
    "__author__"
]

# Global registry instance
registry = AgentRegistry()

# Convenience functions
def register_agent(agent: BaseAgent, **kwargs):
    """Register agent in global registry and protocol"""
    registry.register(agent)
    
    # Also register with MCP protocol if available
    try:
        from mcpturbo_core.protocol import protocol
        protocol.register_agent(agent.config.agent_id, agent, **kwargs)
    except ImportError:
        pass  # Core not available

def get_agent(agent_id: str) -> BaseAgent:
    """Get agent from global registry"""
    return registry.get(agent_id)

def list_agents() -> list:
    """List all registered agents"""
    return registry.list_agents()

def create_simple_agent(agent_id: str, name: str = None) -> LocalAgent:
    """Create and register a simple local agent"""
    agent = create_local_agent(agent_id, name)
    register_agent(agent)
    return agent