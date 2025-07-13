import types
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'orchestrator'))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'agents'))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'core'))

from mcpturbo_ai.adapters import OpenAIAgent

class SimpleRequest(types.SimpleNamespace):
    pass


def test_build_payload_basic():
    agent = OpenAIAgent(api_key="key")
    req = SimpleRequest(action="generate_text", data={"prompt": "Hello"})
    payload = agent.build_payload(req)
    assert payload["model"] == agent.model
    assert payload["messages"] == [{"role": "user", "content": "Hello"}]
    assert payload["max_tokens"] == 1000
    assert payload["temperature"] == 0.7
    assert payload["stream"] is False


def test_build_payload_code_generation():
    agent = OpenAIAgent(api_key="key")
    req = SimpleRequest(action="code_generation", data={"prompt": "sum numbers", "language": "python"})
    payload = agent.build_payload(req)
    user_msg = payload["messages"][0]
    assert "Generate python code for: sum numbers" in user_msg["content"]


def test_parse_openai_response_text():
    agent = OpenAIAgent(api_key="key")
    req = SimpleRequest(action="generate_text", data={})
    response = {
        "choices": [{"message": {"content": "Hello"}}],
        "usage": {"total_tokens": 5},
        "model": "gpt-4",
    }
    result = agent._parse_openai_response(response, req)
    assert result == {"text": "Hello", "tokens_used": 5, "model": "gpt-4"}


def test_parse_openai_response_code_generation():
    agent = OpenAIAgent(api_key="key")
    req = SimpleRequest(action="code_generation", data={})
    content = "Here is code:\n```python\nprint('hi')\n```"
    response = {
        "choices": [{"message": {"content": content}}],
        "usage": {"total_tokens": 7},
        "model": "gpt-4",
    }
    result = agent._parse_openai_response(response, req)
    assert result["code"].strip() == "print('hi')"
    assert result["explanation"] == content
