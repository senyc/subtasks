from fastapi import FastAPI
from collections.abc import Sequence
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Query, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select, func
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


class Project(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    body: str


class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    project_id: int = Field(default=0, foreign_key="project.id")
    title: str
    body: str
    completed: bool = Field(default=False)


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
    projects_with_task_count = session.exec(
        select(Project, func.count(Task.id), func.count(select(Task.id).where(Task.completed)))  # type: ignore
        .outerjoin(Task, Project.id == Task.project_id)
        .group_by(Project.id)
        .offset(offset)
        .limit(limit)
    ).all()

    return [
        ProjectResponse(
            **project.dict(), total_tasks=task_count, completed_tasks=completed_tasks
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
    tasks = session.exec(select(Task).offset(offset).limit(limit)).all()
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
        select(Task).where(Task.project_id == project_id).offset(offset).limit(limit)
    ).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found for project")
    return tasks
