from ..db.db import Project, Task
from dataclasses import dataclass
from collections.abc import Sequence


@dataclass
class PagedTasks:
    tasks: Sequence[Task]
    count: int


class ProjectResponse(Project):
    total_tasks: int
    completed_tasks: int


@dataclass
class PagedProjectResponse:
    projects: Sequence[ProjectResponse]
    count: int
