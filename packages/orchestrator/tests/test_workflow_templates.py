import pytest

from mcpturbo_orchestrator import ProjectOrchestrator, WorkflowStatus
from mcpturbo_agents.base_agent import LocalAgent


class EchoAgent(LocalAgent):
    def __init__(self):
        super().__init__("template", "Template Agent")

    async def handle_request(self, request):
        return request.data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "template_name, action",
    [
        ("app_generation", "generate_app"),
        ("code_review", "review_code"),
        ("architecture_design", "design_architecture"),
    ],
)
async def test_template_builders_execute(template_name, action):
    orchestrator = ProjectOrchestrator()
    agent = EchoAgent()
    orchestrator.register_agent(agent)

    workflow = orchestrator.create_workflow_from_template(
        template_name, agent_id=agent.config.agent_id
    )

    assert workflow.id in orchestrator.workflows

    result = await orchestrator.execute_workflow(workflow)
    assert result["status"] == WorkflowStatus.COMPLETED.value
    assert result["tasks"][0]["action"] == action


def test_unknown_template_raises():
    orchestrator = ProjectOrchestrator()
    with pytest.raises(ValueError):
        orchestrator.create_workflow_from_template("unknown")

