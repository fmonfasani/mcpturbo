"""Tests for MCP Protocol"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock


def test_mcp_message_creation():
    """Test MCP message creation"""
    try:
        from mcpturbo_core import MCPMessage
        
        message = MCPMessage(
            sender="test_agent",
            recipient="target_agent", 
            action="test_action",
            params={"key": "value"}
        )
        
        assert message.sender == "test_agent"
        assert message.recipient == "target_agent"
        assert message.action == "test_action"
        assert message.params["key"] == "value"
        
    except ImportError:
        pytest.skip("MCPMessage not yet implemented")


def test_mcp_protocol_init():
    """Test MCP protocol initialization"""
    try:
        from mcpturbo_core import MCPProtocol
        
        protocol = MCPProtocol()
        assert protocol is not None
        assert hasattr(protocol, 'agents')
        
    except ImportError:
        pytest.skip("MCPProtocol not yet implemented")


@pytest.mark.asyncio
async def test_agent_registration():
    """Test agent registration with protocol"""
    try:
        from mcpturbo_core import MCPProtocol, BaseAgent
        
        protocol = MCPProtocol()
        
        # Mock agent
        agent = Mock()
        agent.agent_id = "test_agent"
        
        protocol.register_agent("test_agent", agent)
        assert "test_agent" in protocol.agents
        
    except ImportError:
        pytest.skip("Protocol/Agent classes not yet implemented")
