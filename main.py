from datetime import date, datetime
from fastapi import FastAPI
from collections.abc import Sequence
from contextlib import asynccontextmanager
from typing import Annotated
from pydantic import ConfigDict, InstanceOf
from fastapi import Depends, FastAPI, Query, HTTPException
from pydantic import AfterValidator, BeforeValidator
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


def convert_to_date(s: str | date | None) -> date | None:
    if s is None or s == "":
        return None
    if isinstance(s, date):
        return s
    return datetime.strptime(s, "%Y-%m-%d").date()


DueDate = Annotated[date | None, BeforeValidator(convert_to_date)]


class Project(BaseSQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    body: str
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


@app.get("/projects/")
def read_projects(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> Sequence[ProjectResponse]:

    stmt = (
        select(
            Project,
            select(func.count(Task.id)).subquery(), # type: ignore
            select(func.count(select(Task.id).where(Task.completed))).subquery(),  # type: ignore
        )
        .outerjoin(Task, Project.id == Task.project_id) # type: ignore
        .group_by(Project.id)  # type: ignore
    ).offset(offset).limit(limit)
    projects_with_task_count = session.exec(stmt).all()
    return [
        ProjectResponse(
            **project.model_dump(),
            total_tasks=task_count,
            completed_tasks=completed_tasks,
        )
        for project, task_count, completed_tasks in projects_with_task_count
    ]


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
) -> Sequence[Task]:
    tasks = session.exec(
        select(Task).where(not Task.completed).offset(offset).limit(limit)
    ).all()
    return tasks


@app.get("/tasks/completed")
def read_completed_tasks(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> Sequence[Task]:
    tasks = session.exec(
        select(Task).where(Task.completed).offset(offset).limit(limit)
    ).all()
    return tasks


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


@app.get("/project/{project_id}/tasks")
def read_project_tasks(
    project_id: int,
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> Sequence[Task] | None:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    tasks = session.exec(
        select(Task)
        .where(and_(Task.project_id == project_id, Task.completed != True))
        .offset(offset)
        .limit(limit)
    ).all()

    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found for project")
    return tasks


@app.get("/project/{project_id}/tasks/completed")
def read_completed_project_tasks(
    project_id: int,
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> Sequence[Task] | None:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    tasks = session.exec(
        select(Task)
        .where(and_(Task.project_id == project_id, Task.completed == True))
        .offset(offset)
        .limit(limit)
    ).all()

    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found for project")
    return tasks
