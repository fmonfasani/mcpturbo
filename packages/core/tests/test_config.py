import pytest

from mcpturbo_core.config import MCPConfig, set_config
from mcpturbo_core.messages import Request, AIRequest


def test_config_fields_defaults():
    config = MCPConfig()
    assert config.max_tokens == 2000
    assert config.timeout == 30
    assert config.tool_permissions == {}
    assert "write_file" in config.sensitive_actions


def test_request_timeout_validation():
    config = MCPConfig(timeout=5, max_tokens=100)
    set_config(config)
    with pytest.raises(ValueError):
        Request(sender="s", target="t", action="a", timeout=10)
    set_config(MCPConfig())


def test_request_max_tokens_validation():
    config = MCPConfig(timeout=5, max_tokens=50)
    set_config(config)
    with pytest.raises(ValueError):
        AIRequest(sender="s", target="t", action="generate", max_tokens=100)
    set_config(MCPConfig())
