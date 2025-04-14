from sqlmodel import select, func, and_
from ..db.db import SessionDep, Task, Tag, TaskTag


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


# TODO: make this accecpt a type field
def parse_ids_from_search(search: str, session: SessionDep):
    """Currently only works with tasks"""
    tag_prefix = "tag:"
    task_ids: list[int] = []
    remaining_search_text = ""
    if tag_prefix not in search:
        return [], search

    split = search.split(" ")
    if len(split) > 1:
        tag_search = split[0]
        remaining_search_text = "".join(split[1:])
    else:
        tag_search = search
    tags = tag_search.split(",")
    for tag in tags:
        tag_name = tag[len(tag_prefix) :].strip()
        # Query to find the tag ID
        tag_record = session.exec(select(Tag).where(Tag.name == tag_name)).one_or_none()
        if tag_record:
            # Query to find all task IDs associated with the tag
            task_ids.extend(
                session.exec(
                    select(TaskTag.task_id).where(TaskTag.tag_id == tag_record.id)
                ).all()
            )
    return task_ids, remaining_search_text
