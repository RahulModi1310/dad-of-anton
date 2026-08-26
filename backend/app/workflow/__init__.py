from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import BackgroundTasks

from app.workflow.workflow_config import BaseWorkflowConfig
from app.workflow.workflow_registry import WORKFLOWS
from app.workflow.workflow_task import BaseWorkflowTask

if TYPE_CHECKING:
    pass


def trigger_workflow(workflow_name: str, background_tasks: BackgroundTasks) -> str:
    from app.workflow.workflow_orchestrator import orchestrator

    return orchestrator.trigger_workflow(workflow_name, background_tasks)


__all__ = [
    "BaseWorkflowTask",
    "BaseWorkflowConfig",
    "WORKFLOWS",
    "trigger_workflow",
]
