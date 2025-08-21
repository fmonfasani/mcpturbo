"""Predefined workflow templates and builders."""

from __future__ import annotations

from typing import Callable, Dict, Any

from .workflow_model import Workflow
from .task_model import Task


def _create_app_generation_workflow(
    *,
    agent_id: str,
    data: Dict[str, Any] | None = None,
    workflow_id: str = "app_generation",
    name: str = "App Generation",
    **kwargs: Any,
) -> Workflow:
    """Build a simple app generation workflow.

    Parameters
    ----------
    agent_id:
        The agent responsible for handling the task.
    data:
        Optional payload forwarded to the agent.
    workflow_id / name:
        Optional identifiers for the resulting workflow.
    """

    task = Task(
        id="generate_app",
        agent_id=agent_id,
        action="generate_app",
        data=data or {},
    )
    return Workflow(id=workflow_id, name=name, tasks=[task])


def _create_code_review_workflow(
    *,
    agent_id: str,
    code: str = "",
    workflow_id: str = "code_review",
    name: str = "Code Review",
    **kwargs: Any,
) -> Workflow:
    """Build a workflow that performs a code review."""

    task = Task(
        id="review_code",
        agent_id=agent_id,
        action="review_code",
        data={"code": code},
    )
    return Workflow(id=workflow_id, name=name, tasks=[task])


def _create_architecture_workflow(
    *,
    agent_id: str,
    requirements: str = "",
    workflow_id: str = "architecture_design",
    name: str = "Architecture Design",
    **kwargs: Any,
) -> Workflow:
    """Build an architecture design workflow."""

    task = Task(
        id="design_architecture",
        agent_id=agent_id,
        action="design_architecture",
        data={"requirements": requirements},
    )
    return Workflow(id=workflow_id, name=name, tasks=[task])


TEMPLATE_BUILDERS: Dict[str, Callable[..., Workflow]] = {
    "app_generation": _create_app_generation_workflow,
    "code_review": _create_code_review_workflow,
    "architecture_design": _create_architecture_workflow,
}

