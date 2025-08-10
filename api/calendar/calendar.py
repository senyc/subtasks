from typing import Sequence
from fastapi import APIRouter
from sqlmodel import desc, select, and_

from ..annotations.types import TimeSlot
from ..db.db import Event, SessionDep, Task

calendar_router = APIRouter(
    tags=["calendar"],
)
from datetime import datetime


@calendar_router.get("/calendar")
def get_calendar(
    session: SessionDep,
    start_at: str = "",
    end_at: str = "",
) -> Sequence[TimeSlot]:
    # Parse the ISO string dates, handling the 'Z' UTC identifier
    start_datetime = None
    end_datetime = None

    start_datetime = datetime.fromisoformat(start_at)

    end_datetime = datetime.fromisoformat(end_at)

    event_query = select(Event).where(
        and_(Event.end_at < end_datetime, Event.start_at >= start_datetime)
    )

    events = session.exec(event_query.order_by(desc(Event.start_at))).all()

    task_query = select(Task).where(
        and_(
            Task.start_at.isnot(None),  # type: ignore
            Task.end_at.isnot(None),  # type: ignore
            Task.end_at < end_datetime,
            Task.start_at >= start_datetime,
        )
    )

    tasks = session.exec(task_query.order_by(desc(Task.start_at))).all()
    time_slots = [TimeSlot(**event.model_dump(), type="event") for event in events]
    time_slots.extend(
        [TimeSlot(**task.model_dump(), type="task", notes=task.body) for task in tasks]
    )

    return time_slots
