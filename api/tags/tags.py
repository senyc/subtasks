from typing import Sequence
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select, and_
from ..db.db import ProjectTag, SessionDep, Tag, TaskTag

tag_router = APIRouter(
    tags=["tags"],
    responses={404: {"description": "Not found"}},
)


@tag_router.post("/tag")
def create_tag(tag: Tag, session: SessionDep):
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


@tag_router.get("/tags/{tag_type}")
def get_tags(
    tag_type: str,
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    search: str = "",
):
    tags = session.exec(
        select(Tag)
        .where(
            and_(
                Tag.type == tag_type, Tag.name.like("%" + search + "%")  # type: ignore
            )
        )
        .offset(offset)
        .limit(limit)
    ).all()
    return tags


@tag_router.patch("/tag/{tag_id}")
def update_tag(tag_id: int, tag: Tag, session: SessionDep):
    updated_tag = session.get(Tag, tag_id)
    if not updated_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    for attr in ["color", "name", "description", "type"]:
        value = getattr(tag, attr, None)
        if value:
            setattr(updated_tag, attr, value)
    session.commit()
    session.refresh(updated_tag)
    return updated_tag


@tag_router.patch("/project/{project_id}/tags")
def update_project_tags(project_id: int, tags: Sequence[int], session: SessionDep):
    existing_tags = session.exec(
        select(ProjectTag).where(ProjectTag.project_id == project_id)
    ).all()
    existing_tag_ids = {tag.tag_id for tag in existing_tags}

    # Delete tags that are no longer in the provided sequence
    for existing_tag in existing_tags:
        if existing_tag.tag_id not in tags:
            session.delete(existing_tag)

    # Add new tags that are in the provided sequence but not in existing tags
    for tag_id in tags:
        if tag_id not in existing_tag_ids:
            new_project_tag = ProjectTag(project_id=project_id, tag_id=tag_id)
            session.add(new_project_tag)

    session.commit()
    return {"message": "Tags updated successfully"}


@tag_router.get("/project/{project_id}/tags")
def get_project_tags(project_id: int, session: SessionDep):
    projects_tags = session.exec(
        select(Tag)
        .join(Tag, ProjectTag.tag_id == Tag.id)  # type: ignore
        .where(ProjectTag.project_id == project_id)
    ).all()
    return projects_tags


@tag_router.get("/task/{task_id}/tags")
def get_task_tags(task_id: int, session: SessionDep):
    task_tags = session.exec(
        select(Tag)
        .select_from(TaskTag)
        .join(Tag, TaskTag.tag_id == Tag.id)  # type: ignore
        .where(TaskTag.task_id == task_id)
    ).all()
    return task_tags


@tag_router.put("/task/{task_id}/tags")
def update_task_tags(task_id: int, tags: Sequence[Tag] | None, session: SessionDep):
    if not tags:
        tags = []
    existing_tags = session.exec(
        select(TaskTag).where(TaskTag.task_id == task_id)
    ).all()
    existing_tag_ids = {tag.tag_id for tag in existing_tags}

    for existing_tag in existing_tags:
        if existing_tag.tag_id not in [tag.id for tag in tags]:
            session.delete(existing_tag)

    for tag in tags:
        if tag.id not in existing_tag_ids:
            task_tag = TaskTag(task_id=task_id, tag_id=tag.id)
            session.add(task_tag)

    session.commit()
    return {"message": "Tags updated successfully"}


@tag_router.put("/task/{task_id}/tags/add")
def add_task_tags(task_id: int, tags: Sequence[Tag], session: SessionDep):
    existing_tags = session.exec(
        select(TaskTag).where(TaskTag.task_id == task_id)
    ).all()
    existing_tag_ids = {tag.tag_id for tag in existing_tags}

    for tag in tags:
        if tag.id not in existing_tag_ids:
            task_tag = TaskTag(task_id=task_id, tag_id=tag.id)
            session.add(task_tag)

    session.commit()
    return {"message": "Tags added successfully"}


@tag_router.delete("/tag/{tag_id}")
def delete_tag(tag_id: int, session: SessionDep):
    db_tag = session.get(Tag, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    project_tags = session.exec(
        select(ProjectTag).where(ProjectTag.tag_id == tag_id)
    ).all()
    task_tags = session.exec(select(TaskTag).where(TaskTag.tag_id == tag_id)).all()

    for task_tag in task_tags:
        session.delete(task_tag)

    for project_tag in project_tags:
        session.delete(project_tag)

    session.delete(db_tag)
    session.commit()
    return {"message": "Tag deleted successfully"}
