from typing import Dict, Any
from mcpturbo_agents import LocalAgent, AgentCapability
from mcpturbo_core.protocol import protocol


class GenesisArchitectAgent(LocalAgent):
    """Agent that designs software architecture using other LLM agents."""

    def __init__(self):
        super().__init__("genesis_architect", "Genesis Architect")
        self.add_capability(
            AgentCapability(
                name="design_architecture",
                description="Design system architecture from requirements",
                input_schema={"requirements": {"type": "string", "required": True}},
                output_schema={"architecture": {"type": "string"}},
            )
        )

    async def handle_design_architecture(self, request) -> Dict[str, Any]:
        requirements = request.data.get("requirements", "")
        prompt = (
            "Design a software architecture for the following requirements:\n"
            f"{requirements}\nProvide an overview of the main components."
        )
        response = await protocol.send_request(
            sender_id=self.config.agent_id,
            target_id="claude",
            action="reasoning",
            data={"prompt": prompt},
        )
        return {"architecture": response.result.get("reasoning") or response.result.get("text", "")}


class GenesisBackendAgent(LocalAgent):
    """Agent that generates backend code using LLMs."""

    def __init__(self):
        super().__init__("genesis_backend", "Genesis Backend")
        self.add_capability(
            AgentCapability(
                name="generate_backend",
                description="Generate backend code from specification",
                input_schema={
                    "spec": {"type": "string", "required": True},
                    "language": {"type": "string", "default": "python"},
                },
                output_schema={"code": {"type": "string"}},
            )
        )

    async def handle_generate_backend(self, request) -> Dict[str, Any]:
        spec = request.data.get("spec", "")
        language = request.data.get("language", "python")
        response = await protocol.send_request(
            sender_id=self.config.agent_id,
            target_id="openai",
            action="code_generation",
            data={"prompt": spec, "language": language},
        )
        return {"code": response.result.get("code", "")}


class GenesisFrontendAgent(LocalAgent):
    """Agent that generates frontend code using LLMs."""

    def __init__(self):
        super().__init__("genesis_frontend", "Genesis Frontend")
        self.add_capability(
            AgentCapability(
                name="generate_frontend",
                description="Generate frontend code from specification",
                input_schema={
                    "spec": {"type": "string", "required": True},
                    "language": {"type": "string", "default": "typescript"},
                },
                output_schema={"code": {"type": "string"}},
            )
        )

    async def handle_generate_frontend(self, request) -> Dict[str, Any]:
        spec = request.data.get("spec", "")
        language = request.data.get("language", "typescript")
        response = await protocol.send_request(
            sender_id=self.config.agent_id,
            target_id="deepseek",
            action="fast_coding",
            data={"prompt": spec, "language": language},
        )
        return {"code": response.result.get("code", "")}


class GenesisDevOpsAgent(LocalAgent):
    """Agent that generates DevOps scripts and configuration."""

    def __init__(self):
        super().__init__("genesis_devops", "Genesis DevOps")
        self.add_capability(
            AgentCapability(
                name="generate_devops",
                description="Generate deployment or CI/CD scripts",
                input_schema={"instructions": {"type": "string", "required": True}},
                output_schema={"scripts": {"type": "string"}},
            )
        )

    async def handle_generate_devops(self, request) -> Dict[str, Any]:
        instructions = request.data.get("instructions", "")
        prompt = (
            "Create CI/CD or deployment scripts for the following instructions:\n"
            f"{instructions}"
        )
        response = await protocol.send_request(
            sender_id=self.config.agent_id,
            target_id="openai",
            action="code_generation",
            data={"prompt": prompt, "language": "bash"},
        )
        return {"scripts": response.result.get("code", "")}

