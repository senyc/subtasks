from datetime import datetime
from typing import Sequence
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from api.db.db import SessionDep, Task

task_router = APIRouter(
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)


@task_router.get("tasks/completed")
def read_completed_tasks(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    search: str = "",
) -> Sequence[Task]:
    tasks = session.exec(
        select(Task)
        .where(Task.completed)
        .where(Task.title.like("%" + search + "%"))  # type: ignore
        .offset(offset)
        .limit(limit)
    ).all()
    if tasks:
        return tasks
    return []


@task_router.get("/tasks")
def read_tasks(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    search: str = "",
) -> Sequence[Task]:
    tasks = session.exec(
        select(Task)
        .where(and_(Task.completed == False, Task.title.like("%" + search + "%")))  # type: ignore
        .offset(offset)
        .limit(limit)
    ).all()
    return tasks

@task_router.get("/task/{task_id}")
def read_task(task_id: int, session: SessionDep) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@task_router.put("/task/{task_id}")
def update_task(task_id: int, task: Task, session: SessionDep) -> Task | None:
    updated_task = session.get(Task, task_id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Only update values that are set in the request
    for attr in ["title", "body", "due_date", "project_id"]:
        value = getattr(task, attr, None)
        if value is not None:
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

@task_router.post("/tasks")
def create_task(task: Task, session: SessionDep) -> Task:
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


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
