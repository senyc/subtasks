from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .tasks.tasks import task_router
from .projects.projects import project_router
from .tags.tags import tag_router
from .events.events import event_router
from .calendar.calendar import calendar_router


app = FastAPI()
app.include_router(task_router)
app.include_router(project_router)
app.include_router(tag_router)
app.include_router(event_router)
app.include_router(calendar_router)
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
