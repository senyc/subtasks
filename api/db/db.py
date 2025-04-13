from sqlmodel import Field, Session, SQLModel, create_engine, Relationship
from fastapi import Depends
from pydantic import ConfigDict
from typing import Annotated, List
from datetime import datetime, timezone
from pydantic import BeforeValidator
from pathlib import Path

sqlite_path = Path("~/database.db").expanduser()
sqlite_url = f"sqlite:///{sqlite_path}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
"""This is basically just an annotation with extra information
The `Depends` is a fastapi specific thing using dependency injection to give the handler the item requested
basically dependency injection"""


# This allows for objects with table=true to have validations run
# per: https://github.com/fastapi/sqlmodel/issues/52#issuecomment-1225746421
class BaseSQLModel(SQLModel):
    model_config = ConfigDict(validate_assignment=True)  # type: ignore


def convert_to_date(s: str | datetime | None) -> datetime | None:
    if not s or s == "":
        return None
    if isinstance(s, datetime):
        return s
    return datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc)


DueDate = Annotated[datetime | None, BeforeValidator(convert_to_date)]


class Project(BaseSQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str
    # TODO: update this to support passing in JSON and converting to a string
    # (or we can just store the rich text as a blob)
    body: str
    completed: bool = Field(default=False)
    due_date: DueDate
    completed_date: DueDate
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    order: float = Field(default=0.0, nullable=False)


class Tag(BaseSQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    description: str = Field(default=None, nullable=True)
    type: str = Field(default="")
    color: str = Field(default="#ADD8E6")
    """Defaults to light blue"""


class ProjectTag(BaseSQLModel, table=True):
    project_id: int = Field(foreign_key="project.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)


class TaskTag(BaseSQLModel, table=True):
    task_id: int = Field(foreign_key="task.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)


class Task(BaseSQLModel, table=True):
    id: int = Field(primary_key=True)
    project_id: int | None = Field(default=None, foreign_key="project.id")
    title: str
    body: str
    completed: bool = Field(default=False)
    due_date: DueDate
    completed_date: DueDate
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    time_estimate: int = Field(default=15, nullable=False)
    """Estimated minutes until completion in minutes"""
    order: float = Field(default=0.0, nullable=False)
