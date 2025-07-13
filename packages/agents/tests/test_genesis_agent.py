import pytest
from mcpturbo_agents import GenesisAgent, AgentConfig, AgentType, registry, register_agent


def test_genesis_registration():
    agent = GenesisAgent(AgentConfig(agent_id="gen-test", name="Genesis Test", agent_type=AgentType.LOCAL))
    register_agent(agent)
    assert registry.exists("gen-test")
