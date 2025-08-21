import asyncio
import time
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime
from .workflow_model import Workflow
from .task_model import Task
from .workflow_state import WorkflowStatus, TaskPriority
from .workflow_templates import TEMPLATE_BUILDERS
from mcpturbo_core.protocol import protocol
from mcpturbo_core.exceptions import MCPError
from mcpturbo_agents import BaseAgent
from opentelemetry import metrics, trace


tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)
_workflow_counter = meter.create_counter("workflow_executions_total")
_workflow_duration = meter.create_histogram("workflow_execution_duration")

class ProjectOrchestrator:
    def __init__(self):
        self.workflows: Dict[str, Workflow] = {}
        self.agents: Dict[str, BaseAgent] = {}
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.running_workflows: Dict[str, asyncio.Task] = {}
        self.max_concurrent_tasks = 10

    def register_agent(self, agent: BaseAgent, **config):
        self.agents[agent.config.agent_id] = agent
        protocol.register_agent(agent.config.agent_id, agent, **config)

    def subscribe_to_events(self, event: str, handler: Callable):
        self.event_handlers.setdefault(event, []).append(handler)

    def create_workflow_from_template(self, name: str, **kwargs) -> Workflow:
        """Instantiate a workflow from a named template.

        Parameters
        ----------
        name:
            Template identifier present in :data:`TEMPLATE_BUILDERS`.
        **kwargs:
            Parameters forwarded to the template builder.

        Returns
        -------
        Workflow
            The newly created workflow, also registered in ``self.workflows``.
        """

        builder = TEMPLATE_BUILDERS.get(name)
        if builder is None:
            raise ValueError(f"Unknown workflow template: {name}")

        workflow = builder(**kwargs)
        self.workflows[workflow.id] = workflow
        return workflow

    async def execute_workflow(self, workflow: Workflow) -> Dict[str, Any]:
        self.workflows[workflow.id] = workflow
        start = time.perf_counter()
        with tracer.start_as_current_span("orchestrator.execute_workflow") as span:
            span.set_attribute("workflow.id", workflow.id)
            task = asyncio.create_task(self._execute_workflow_internal(workflow))
            self.running_workflows[workflow.id] = task
            try:
                result = await task
            finally:
                self.running_workflows.pop(workflow.id, None)

        duration = time.perf_counter() - start
        _workflow_counter.add(1, {"workflow": workflow.id})
        _workflow_duration.record(duration, {"workflow": workflow.id})
        return result

    async def _execute_workflow_internal(self, workflow: Workflow) -> Dict[str, Any]:
        workflow.status = WorkflowStatus.RUNNING
        workflow.started_at = datetime.utcnow()
        await self._emit_event("workflow_started", {"workflow_id": workflow.id})

        semaphore = asyncio.Semaphore(self.max_concurrent_tasks)

        while not workflow.is_completed() and not workflow.has_failed():
            ready_tasks = workflow.get_ready_tasks()
            if not ready_tasks:
                await asyncio.sleep(1)
                continue
            await asyncio.gather(*[
                self._execute_task_with_semaphore(semaphore, workflow, task)
                for task in ready_tasks
            ])

        workflow.completed_at = datetime.utcnow()
        workflow.status = WorkflowStatus.FAILED if workflow.has_failed() else WorkflowStatus.COMPLETED

        await self._emit_event("workflow_completed", {
            "workflow_id": workflow.id,
            "status": workflow.status.value
        })
        return self._generate_workflow_result(workflow)

    async def _execute_task_with_semaphore(self, semaphore: asyncio.Semaphore, workflow: Workflow, task: Task):
        async with semaphore:
            await self._execute_task(workflow, task)

    async def _execute_task(self, workflow: Workflow, task: Task):
        task.status = WorkflowStatus.RUNNING
        task.started_at = datetime.utcnow()
        task.attempts += 1

        await self._emit_event("task_started", {"workflow_id": workflow.id, "task_id": task.id})

        try:
            task_data = {**task.data, **workflow.context}
            for dep_id in task.dependencies:
                dep = next((t for t in workflow.tasks if t.id == dep_id), None)
                if dep and dep.status == WorkflowStatus.COMPLETED:
                    task_data[f"{dep_id}_result"] = dep.result

            response = await protocol.send_request(
                sender_id="orchestrator",
                target_id=task.agent_id,
                action=task.action,
                data=task_data,
                timeout=task.timeout
            )

            task.result = response.result if response.success else None
            task.error = response.error if not response.success else None
            task.status = WorkflowStatus.COMPLETED if response.success else WorkflowStatus.FAILED

        except Exception as e:
            task.error = str(e)
            task.status = WorkflowStatus.FAILED
            if task.attempts < task.retry_attempts:
                task.status = WorkflowStatus.PENDING
                await asyncio.sleep(2 ** task.attempts)

        task.completed_at = datetime.utcnow()

        await self._emit_event("task_completed", {
            "workflow_id": workflow.id,
            "task_id": task.id,
            "status": task.status.value
        })

    def _generate_workflow_result(self, workflow: Workflow) -> Dict[str, Any]:
        return {
            "workflow_id": workflow.id,
            "name": workflow.name,
            "status": workflow.status.value,
            "tasks": [
                {
                    "id": task.id,
                    "agent_id": task.agent_id,
                    "action": task.action,
                    "status": task.status.value,
                    "result": task.result,
                    "error": task.error
                }
                for task in workflow.tasks
            ],
            "context": workflow.context
        }

    async def _emit_event(self, event: str, data: Dict[str, Any]):
        for handler in self.event_handlers.get(event, []):
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
            except Exception:
                continue

# Singleton instance
orchestrator = ProjectOrchestrator()
