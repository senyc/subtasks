from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import desc, select, and_

from ..tags.tags import get_task_tags, update_task_tags

from ..shared.shared import get_ids_from_search, new_task, get_task_count
from ..types.types import NewTask, TaskData, PagedTasks

from ..db.db import SessionDep, Task

task_router = APIRouter(
    tags=["tasks"],
)


@task_router.get("/tasks/completed")
def read_completed_tasks(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    search: str = "",
) -> PagedTasks:
    tasks = session.exec(
        select(Task)
        .where(and_(Task.completed == True, Task.title.like("%" + search + "%")))  # type: ignore
        .offset(offset)
        .limit(limit)
        .order_by(desc(Task.order))
    ).all()

    tasks_with_tags = [
        TaskData(**task.model_dump(), tags=get_task_tags(task.id, session))
        for task in tasks
    ]
    if not tasks:
        return PagedTasks(tasks=tasks_with_tags, count=0)
    count = get_task_count(session, True, search)
    return PagedTasks(tasks=tasks_with_tags, count=count)


@task_router.get("/tasks")
def read_tasks(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    search: str = "",
) -> PagedTasks:

    task_ids, search_text = get_ids_from_search(search, session)
    tasks_query = select(Task).where(Task.completed == False)
    if task_ids:
        tasks_query = tasks_query.where(Task.id.in_(task_ids))  # type: ignore
    tasks_query = tasks_query.where(Task.title.like(f"%{search_text}%"))  # type: ignore
    tasks_query = tasks_query.order_by(desc(Task.order)).offset(offset).limit(limit)
    tasks = session.exec(tasks_query).all()
    if not tasks:
        return PagedTasks(tasks=[], count=0)
    count = get_task_count(session, False, search)

    tasks_with_tags = [
        TaskData(**task.model_dump(), tags=get_task_tags(task.id, session))
        for task in tasks
    ]

    return PagedTasks(
        tasks=tasks_with_tags,
        count=count,
    )


@task_router.get("/task/{task_id}")
def read_task(task_id: int, session: SessionDep) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@task_router.patch("/task/{task_id}")
def update_task(task_id: int, task: TaskData, session: SessionDep) -> Task | None:
    updated_task = session.get(Task, task_id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Only update values that are set in the request
    for attr in [
        "time_estimate",
        "title",
        "body",
        "due_date",
        "project_id",
        "order",
        "tags",
    ]:

        value = getattr(task, attr, None)
        if value is None:
            continue
        # If tags we should put the new tags, otherwise just update the model
        if attr == "tags":
            update_task_tags(task_id, value, session)
        else:
            setattr(updated_task, attr, value)
    session.commit()
    session.refresh(updated_task)
    return updated_task


@task_router.delete("/task/{task_id}")
def delete_task(task_id: int, session: SessionDep) -> int | None:
    task_to_delete = session.get(Task, task_id)

    if not task_to_delete:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task_to_delete)
    session.commit()

    return task_to_delete.id


@task_router.post("/task")
def create_task(task: NewTask, session: SessionDep) -> Task:
    task_item = Task(**task.model_dump())
    created_task = new_task(task_item, session)
    update_task_tags(created_task.id, task.tags, session)
    return created_task


@task_router.patch("/task/{task_id}/complete")
def complete_task(task_id, session: SessionDep) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = True
    task.completed_date = datetime.now()
    session.commit()
    session.refresh(task)
    return task


@task_router.patch("/task/{task_id}/incomplete")
def incomplete_task(task_id, session: SessionDep) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = False
    session.commit()
    session.refresh(task)
    return task
