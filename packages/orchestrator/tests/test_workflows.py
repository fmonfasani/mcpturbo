import pytest

from mcpturbo_orchestrator import ProjectOrchestrator, Task, Workflow, WorkflowStatus
from mcpturbo_agents.base_agent import LocalAgent
from mcpturbo_core.protocol import protocol


class EchoAgent(LocalAgent):
    def __init__(self):
        super().__init__("echo", "Echo Agent")

    async def handle_request(self, request):
        return request.data


@pytest.mark.asyncio
async def test_workflow_with_dependencies():
    """Create workflow with dependent tasks and verify execution"""
    protocol.agents.clear()
    orch = ProjectOrchestrator()
    agent = EchoAgent()
    orch.register_agent(agent)

    tasks = [
        Task(id="t1", agent_id="echo", action="echo", data={"msg": "one"}),
        Task(id="t2", agent_id="echo", action="echo", data={"msg": "two"}, dependencies=["t1"]),
        Task(id="t3", agent_id="echo", action="echo", data={"msg": "three"}, dependencies=["t1", "t2"]),
    ]
    wf = Workflow(id="wf", name="deps", tasks=tasks)

    result = await orch.execute_workflow(wf)
    assert result["status"] == WorkflowStatus.COMPLETED.value
    task_results = {t["id"]: t["result"] for t in result["tasks"]}
    assert task_results["t2"]["t1_result"]["msg"] == "one"
    assert task_results["t3"]["t2_result"]["msg"] == "two"
