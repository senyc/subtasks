from dataclasses import dataclass
from datetime import datetime, timezone
from fastapi import FastAPI
from collections.abc import Sequence
from contextlib import asynccontextmanager
from typing import Annotated
from pydantic import ConfigDict
from fastapi import Depends, FastAPI, Query, HTTPException
from pydantic import BeforeValidator
from sqlmodel import Field, Session, SQLModel, create_engine, select, func, and_
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# This allows for objects with table=true to have validations run
# per: https://github.com/fastapi/sqlmodel/issues/52#issuecomment-1225746421
class BaseSQLModel(SQLModel):
    model_config = ConfigDict(validate_assignment=True)  # type: ignore


def convert_to_date(s: str | datetime | None) -> datetime | None:
    if s is None or s == "":
        return None
    if isinstance(s, datetime):
        return s
    return datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc)


DueDate = Annotated[datetime | None, BeforeValidator(convert_to_date)]


class Project(BaseSQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    body: str
    completed: bool = Field(default=False)
    due_date: DueDate
    completed_date: DueDate
    created_at: datetime = Field(default=datetime.now(), nullable=False)


class Task(BaseSQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    project_id: int | None = Field(default=None, foreign_key="project.id")
    title: str
    body: str
    completed: bool = Field(default=False)
    due_date: DueDate
    completed_date: DueDate
    created_at: datetime = Field(default=datetime.now(), nullable=False)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

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


@app.post("/project")
def create_project(project: Project, session: SessionDep) -> Project:
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


class ProjectResponse(Project):
    total_tasks: int
    completed_tasks: int


@dataclass
class PagedProjectResponse:
    projects: Sequence[ProjectResponse]
    count: int


@app.get("/projects/all")
def all_projects(
    session: SessionDep,
) -> Sequence[Project]:
    """Used for the select box when choosing to swap a task that a project is in
    Returns less data than the standard /projects endpoint
    """
    projects = session.exec(select(Project)).all()
    return projects


@app.get("/projects/")
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
    ).all()
    project_count = session.exec(select(func.count(Project.id))).one()  # type: ignore
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


@app.get("/projects/completed")
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
    ).all()

    project_count = session.exec(select(func.count(Project.id))).one()  # type: ignore

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


@app.get("/project/{project_id}")
def read_project(project_id: int, session: SessionDep) -> Project:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.put("/project/{project_id}")
def update_project(project_id: int, project: Project, session: SessionDep) -> Project:
    updated_project = session.get(Project, project_id)
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    updated_project.title = project.title
    updated_project.body = project.body
    updated_project.due_date = project.due_date
    session.commit()
    session.refresh(updated_project)
    return updated_project


@app.delete("/project/{project_id}")
def delete_project(project_id: int, session: SessionDep) -> int | None:
    project_to_delete = session.get(Project, project_id)

    if not project_to_delete:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(project_to_delete)
    session.commit()

    return project_to_delete.id


@app.patch("/project/{project_id}/complete")
def complete_project(project_id, session: SessionDep) -> Project:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.completed = True
    project.completed_date = datetime.now()
    session.commit()
    session.refresh(project)
    return project


@app.post("/tasks")
def create_task(task: Task, session: SessionDep) -> Task:
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.patch("/task/{task_id}/complete")
def complete_task(task_id, session: SessionDep) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = True
    task.completed_date = datetime.now()
    session.commit()
    session.refresh(task)
    return task


@app.patch("/task/{task_id}/incomplete")
def incomplete_task(task_id, session: SessionDep) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = False
    session.commit()
    session.refresh(task)
    return task


@app.patch("/project/{project_id}/incomplete")
def incomplete_project(project_id, session: SessionDep) -> Project:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.completed = False
    session.commit()
    session.refresh(project)
    return project


@app.post("/project/{project_id}/task")
def create_project_task(
    project_id: int, task: Task, session: SessionDep
) -> Task | None:
    task.project_id = project_id
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.get("/tasks")
def read_tasks(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    search: str = "",
) -> Sequence[Task]:
    tasks = session.exec(
        select(Task)
        .where(and_(Task.completed == False, Task.title.like("%" + search + "%")))
        .offset(offset)
        .limit(limit)
    ).all()
    return tasks


@app.get("/tasks/completed")
def read_completed_tasks(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    search: str = "",
) -> Sequence[Task]:
    tasks = session.exec(
        select(Task)
        .where(Task.completed)
        .where(Task.title.like("%" + search + "%"))
        .offset(offset)
        .limit(limit)
    ).all()
    if tasks:
        return tasks
    return []


@app.get("/task/{task_id}")
def read_task(task_id: int, session: SessionDep) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/task/{task_id}")
def Update_task(task_id: int, task: Task, session: SessionDep) -> Task | None:
    updated_task = session.get(Task, task_id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    updated_task.title = task.title
    updated_task.body = task.body
    updated_task.due_date = task.due_date
    updated_task.project_id = task.project_id
    session.commit()
    session.refresh(updated_task)
    return updated_task


@app.delete("/task/{task_id}")
def delete_task(task_id: int, session: SessionDep) -> int | None:
    task_to_delete = session.get(Task, task_id)

    if not task_to_delete:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task_to_delete)
    session.commit()

    return task_to_delete.id


@dataclass
class PagedProjectTasksResponse:
    tasks: Sequence[Task]
    count: int


@app.get("/project/{project_id}/tasks")
def read_project_tasks(
    project_id: int,
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    search: str = "",
) -> PagedProjectTasksResponse | None:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    tasks = session.exec(
        select(Task)
        .where(
            and_(
                Task.project_id == project_id,
                Task.completed != True,
                Task.title.like("%" + search + "%"),
            )
        )
        .offset(offset)
        .limit(limit)
    ).all()

    if not tasks:
        return PagedProjectTasksResponse(tasks=tasks, count=0)

    count = session.exec(
            select(func.count(Task.id).filter( # type:ignore
                and_(
                    Task.project_id == project_id,
                    Task.completed == False,
                    Task.title.like("%" + search + "%"),  # type: ignore
                )
            )
        )
    ).one()
    return PagedProjectTasksResponse(tasks=tasks, count=count)


@app.get("/project/{project_id}/tasks/completed")
def read_completed_project_tasks(
    project_id: int,
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    search: str = "",
) -> PagedProjectTasksResponse | None:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    tasks = session.exec(
        select(Task)
        .where(
            and_(
                Task.project_id == project_id,
                Task.completed == True,
                Task.title.like("%" + search + "%"), # type: ignore
            )
        )
        .offset(offset)
        .limit(limit)
    ).all()

    if not tasks:
        return PagedProjectTasksResponse(tasks=tasks, count=0)

    count = session.exec(
            select(func.count(Task.id).filter( # type: ignore
                and_(
                    Task.project_id == project_id,
                    Task.completed == True,
                    Task.title.like("%" + search + "%"),  # type: ignore
                )
            )
        )
    ).one()
    return PagedProjectTasksResponse(tasks=tasks, count=count)
