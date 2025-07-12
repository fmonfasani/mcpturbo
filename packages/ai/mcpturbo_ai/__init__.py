"""
MCPturbo AI - AI and LLM Integration Components v2

Advanced adapters for external AI services including OpenAI, Claude, and DeepSeek.
"""

__version__ = "2.0.0"
__author__ = "Federico Monfasani"

# AI Agent adapters
from .adapters import (
    OpenAIAgent, ClaudeAgent, DeepSeekAgent,
    create_openai_agent, create_claude_agent, create_deepseek_agent,
    create_multi_llm_setup
)

# Main exports
__all__ = [
    # Agent classes
    "OpenAIAgent",
    "ClaudeAgent", 
    "DeepSeekAgent",
    
    # Factory functions
    "create_openai_agent",
    "create_claude_agent",
    "create_deepseek_agent",
    "create_multi_llm_setup",
    
    # Metadata
    "__version__",
    "__author__"
]

# Convenience functions for quick setup
def setup_openai(api_key: str, model: str = "gpt-4", **kwargs) -> OpenAIAgent:
    """Quick setup for OpenAI agent"""
    agent = create_openai_agent(api_key, model, **kwargs)
    
    # Register with global registry if available
    try:
        from mcpturbo_agents import register_agent
        register_agent(agent)
    except ImportError:
        pass
    
    return agent

def setup_claude(api_key: str, model: str = "claude-3-sonnet-20240229", **kwargs) -> ClaudeAgent:
    """Quick setup for Claude agent"""
    agent = create_claude_agent(api_key, model, **kwargs)
    
    # Register with global registry if available
    try:
        from mcpturbo_agents import register_agent
        register_agent(agent)
    except ImportError:
        pass
    
    return agent

def setup_deepseek(api_key: str, model: str = "deepseek-coder", **kwargs) -> DeepSeekAgent:
    """Quick setup for DeepSeek agent"""
    agent = create_deepseek_agent(api_key, model, **kwargs)
    
    # Register with global registry if available
    try:
        from mcpturbo_agents import register_agent
        register_agent(agent)
    except ImportError:
        pass
    
    return agent

def setup_all_agents(openai_key: str = None, claude_key: str = None, deepseek_key: str = None) -> dict:
    """Setup all available AI agents"""
    agents = {}
    
    if openai_key:
        agents["openai"] = setup_openai(openai_key)
    
    if claude_key:
        agents["claude"] = setup_claude(claude_key)
    
    if deepseek_key:
        agents["deepseek"] = setup_deepseek(deepseek_key)
    
    return agents

# Default models for each provider
DEFAULT_MODELS = {
    "openai": "gpt-4",
    "claude": "claude-3-sonnet-20240229", 
    "deepseek": "deepseek-coder"
}

# Capability mappings
AGENT_CAPABILITIES = {
    "openai": ["generate_text", "code_generation", "reasoning", "analysis"],
    "claude": ["reasoning", "analysis", "writing", "critique"],
    "deepseek": ["fast_coding", "code_optimization", "technical_writing"]
}