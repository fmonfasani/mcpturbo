import asyncio
import pytest

from mcpturbo_agents import (
    create_local_agent,
    register_agent,
    get_agent,
    list_agents,
    registry,
)


@pytest.mark.asyncio
async def test_agent_registration():
    # clear registry
    registry.clear()
    agent = create_local_agent("genesis", "Genesis Agent")
    register_agent(agent)

    assert "genesis" in list_agents()
    assert get_agent("genesis") is agent
