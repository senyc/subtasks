from datetime import datetime
from typing import Optional
from ..db.db import BaseSQLModel, Project, Tag
from collections.abc import Sequence
from dataclasses import dataclass


class TaskData(BaseSQLModel, table=False):
    id: Optional[int] = None
    project_id: int | None = None
    title: str
    body: str = ""
    completed: bool = False
    due_date: datetime | None = None
    completed_date: datetime | None = None
    created_at: datetime | None = None
    time_estimate: int | None =None
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
