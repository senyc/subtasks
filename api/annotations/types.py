from datetime import datetime
from ..db.db import BaseSQLModel, Project, Tag
from collections.abc import Sequence
from dataclasses import dataclass


class NewTask(BaseSQLModel, table=False):
    project_id: int | None = None
    title: str | None = None
    body: str | None = None
    completed: bool = False
    due_date: datetime | None = None
    completed_date: datetime | None = None
    time_estimate: int | None = None
    """Estimated minutes until completion in minutes"""
    order: float = 0
    tags: Sequence[Tag] | None = None


class TaskData(BaseSQLModel, table=False):
    id: int | None = None
    project_id: int | None = None
    title: str | None = None
    body: str | None = None
    completed: bool = False
    due_date: datetime | None = None
    completed_date: datetime | None = None
    created_at: datetime | None = None
    time_estimate: int | None = None
    """Estimated minutes until completion in minutes"""
    order: float | None = None
    tags: Sequence[Tag] | None = None


@dataclass
class PagedTasks:
    tasks: Sequence[TaskData]
    count: int


class ProjectResponse(Project):
    total_tasks: int
    completed_tasks: int


@dataclass
class PagedProjectResponse:
    projects: Sequence[ProjectResponse]
    count: int
