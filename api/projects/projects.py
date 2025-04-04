from datetime import datetime
from sqlmodel import desc, select, func, and_
from fastapi import APIRouter, HTTPException, Query
from collections.abc import Sequence


from ..db.db import Project, SessionDep, Task
from ..types.types import PagedProjectResponse, PagedTasks, ProjectResponse
from ..shared.shared import new_task


project_router = APIRouter(
    tags=["projects"],
    responses={404: {"description": "Not found"}},
)


@project_router.post("/project")
def create_project(project: Project, session: SessionDep) -> Project:
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@project_router.get("/projects/all")
def all_projects(
    session: SessionDep,
) -> Sequence[Project]:
    """Used for the select box when choosing to swap a task that a project is in
    Returns less data than the standard /projects endpoint
    """
    projects = session.exec(select(Project)).all()
    return projects


@project_router.get("/projects/")
def read_projects(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    search: str = "",
) -> PagedProjectResponse:

    projects_with_task_count = session.exec(
        select(  # type: ignore
            Project,
            func.count(Task.id),  # type: ignore
            func.count(Task.id).filter(Task.completed == True),  # type: ignore
        )
        .where(Project.completed == False)
        .where(Project.title.like("%" + search + "%"))  # type: ignore
        .join(Task, Project.id == Task.project_id, isouter=True)
        .group_by(Project.id)
        .offset(offset)
        .limit(limit)
        .order_by(desc(Project.order))  # type: ignore
    ).all()

    project_count = session.exec(select(func.count(Project.id).filter(and_(Project.title.like("%" + search + "%"), Project.completed == False)))).one()  # type: ignore
    return PagedProjectResponse(
        projects=[
            ProjectResponse(
                **project.model_dump(),
                total_tasks=task_count,
                completed_tasks=completed_tasks,
            )
            for project, task_count, completed_tasks in projects_with_task_count
        ],
        count=project_count,
    )


@project_router.get("/projects/completed")
def read_completed_projects(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    search: str = "",
) -> PagedProjectResponse:

    projects_with_task_count = session.exec(
        select(  # type: ignore
            Project,
            func.count(Task.id),  # type: ignore
            func.count(Task.id).filter(Task.completed == True),  # type: ignore
        )
        .where(Project.completed == True)
        .where(Project.title.like("%" + search + "%"))  # type: ignore
        .join(Task, Project.id == Task.project_id, isouter=True)
        .group_by(Project.id)
        .offset(offset)
        .limit(limit)
        .order_by(desc(Task.order))  # type: ignore
    ).all()

    project_count = session.exec(select(func.count(Project.id).filter(and_(Project.title.like("%" + search + "%"), Project.completed == True)))).one()  # type: ignore

    return PagedProjectResponse(
        projects=[
            ProjectResponse(
                **project.model_dump(),
                total_tasks=task_count,
                completed_tasks=completed_tasks,
            )
            for project, task_count, completed_tasks in projects_with_task_count
        ],
        count=project_count,
    )


@project_router.get("/project/{project_id}")
def read_project(project_id: int, session: SessionDep) -> Project:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@project_router.patch("/project/{project_id}")
def update_project(project_id: int, project: Project, session: SessionDep) -> Project:
    updated_project = session.get(Project, project_id)
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    for attr in ["title", "body", "due_date", "order"]:
        value = getattr(project, attr, None)
        if value:
            setattr(updated_project, attr, value)
    session.commit()
    session.refresh(updated_project)
    return updated_project


@project_router.delete("/project/{project_id}")
def delete_project(project_id: int, session: SessionDep) -> int | None:
    project_to_delete = session.get(Project, project_id)

    if not project_to_delete:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(project_to_delete)
    session.commit()

    return project_to_delete.id


@project_router.patch("/project/{project_id}/complete")
def complete_project(project_id, session: SessionDep) -> Project:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.completed = True
    project.completed_date = datetime.now()
    session.commit()
    session.refresh(project)
    return project


@project_router.patch("/project/{project_id}/incomplete")
def incomplete_project(project_id, session: SessionDep) -> Project:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.completed = False
    session.commit()
    session.refresh(project)
    return project


@project_router.post("/project/{project_id}/task")
def create_project_task(
    project_id: int, task: Task, session: SessionDep
) -> Task | None:
    task.project_id = project_id
    return new_task(task, session)


@project_router.get("/project/{project_id}/tasks")
def read_project_tasks(
    project_id: int,
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    search: str = "",
) -> PagedTasks | None:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    tasks = get_project_tasks(project_id, session, False, offset, limit, search)
    if not tasks:
        return PagedTasks(tasks=tasks, count=0)

    count = get_project_task_count(project_id, session, False, search)
    return PagedTasks(tasks=tasks, count=count)


def get_project_tasks(
    project_id: int,
    session: SessionDep,
    completed: bool,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    search: str = "",
):
    return session.exec(
        select(Task)
        .where(
            and_(
                Task.project_id == project_id,
                Task.completed == completed,
                Task.title.like("%" + search + "%"),  # type: ignore
            )
        )
        .offset(offset)
        .limit(limit)
        .order_by(desc(Task.order))
    ).all()


def get_project_task_count(
    project_id, session: SessionDep, completed: bool, search: str
):
    return session.exec(
        select(
            func.count(Task.id).filter(  # type:ignore
                and_(
                    Task.project_id == project_id,
                    Task.completed == completed,
                    Task.title.like("%" + search + "%"),  # type: ignore
                )
            )
        )
    ).one()


@project_router.get("/project/{project_id}/tasks/completed")
def read_completed_project_tasks(
    project_id: int,
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    search: str = "",
) -> PagedTasks | None:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    tasks = get_project_tasks(project_id, session, True, offset, limit, search)

    if not tasks:
        return PagedTasks(tasks=tasks, count=0)

    count = get_project_task_count(project_id, session, True, search)

    return PagedTasks(tasks=tasks, count=count)
