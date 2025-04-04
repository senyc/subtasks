from sqlmodel import select, func, and_
from ..db.db import SessionDep, Task

def new_task(task: Task, session: SessionDep) -> Task:
    session.add(task)
    session.commit()
    session.refresh(task)
    # Set order to id
    task.order = task.id
    session.commit()
    session.refresh(task)

    return task

def get_task_count(session: SessionDep, completed: bool, search: str):
    return session.exec(
        select(
            func.count(Task.id).filter(  # type:ignore
                and_(
                    Task.completed == completed,
                    Task.title.like("%" + search + "%"),  # type: ignore
                )
            )
        )
    ).one()
