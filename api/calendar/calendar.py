from typing import Sequence
from fastapi import APIRouter
from sqlmodel import desc, select, and_

from ..annotations.types import TimeSlot
from ..db.db import Event, SessionDep

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

    # Build the query with optional date filters
    query = select(Event).where(
        and_(Event.end_at < end_datetime, Event.start_at >= start_datetime)  # type: ignore
    )

    events = session.exec(query.order_by(desc(Event.start_at))).all()

    time_slots = [TimeSlot(**event.model_dump(), type='event') for event in events]

    return time_slots
