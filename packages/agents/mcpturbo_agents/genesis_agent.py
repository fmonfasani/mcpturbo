from typing import Any
from .base_agent import BaseAgent, AgentConfig, AgentType


class GenesisAgent(BaseAgent):
    """Simple agent used for testing registration and workflows."""

    def __init__(self, config: AgentConfig | None = None):
        if config is None:
            config = AgentConfig(agent_id="genesis", name="Genesis Agent", agent_type=AgentType.LOCAL)
        super().__init__(config)

    async def handle_request(self, request) -> Any:  # pragma: no cover - trivial
        if request.action == "echo":
            return {"echo": request.data}
        return {"action": request.action, "data": request.data}
