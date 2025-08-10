from typing import Sequence
from fastapi import APIRouter, HTTPException
from sqlmodel import desc, select, and_
from ..shared.shared import new_event
from ..db.db import Event, SessionDep

event_router = APIRouter(
    tags=["events"],
)


from datetime import datetime


# add pagination endpt (for a list display or something
@event_router.get("/events")
def get_events(
    session: SessionDep,
    start_at: str = "",
    end_at: str = "",
) -> Sequence[Event]:
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

    return events


@event_router.post("/event")
def create_event(event: Event, session: SessionDep) -> Event:
    event_item = Event(
        **event.model_dump(),
    )
    created_event = new_event(event_item, session)
    return created_event


@event_router.patch("/event/{event_id}")
def update_event(event_id: int, event: Event, session: SessionDep) -> Event:
    updated_event = session.get(Event, event_id)
    if not updated_event:
        raise HTTPException(status_code=404, detail="Event not found")
    for attr in ["title", "notes", "start_at", "end_at"]:
        value = getattr(event, attr, None)
        if value:
            setattr(updated_event, attr, value)
    session.commit()
    session.refresh(updated_event)
    return updated_event


@event_router.delete("/event/{event_id}")
def delete_event(event_id: int, session: SessionDep) -> int | None:
    event_to_delete = session.get(Event, event_id)

    if not event_to_delete:
        raise HTTPException(status_code=404, detail="Event not found")
    session.delete(event_to_delete)
    session.commit()

    return event_to_delete.id
