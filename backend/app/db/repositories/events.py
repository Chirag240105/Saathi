from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Event


class EventRepo:
    def __init__(self, s: Session) -> None:
        self.s = s

    def add(
        self, elder_id: int, type_: str, message: str, severity: str, at: datetime
    ) -> Event:
        e = Event(elder_id=elder_id, type=type_, message=message, severity=severity, created_at=at)
        self.s.add(e)
        self.s.flush()
        return e

    def recent(self, elder_id: int, limit: int = 20, type_: str | None = None) -> list[Event]:
        q = select(Event).where(Event.elder_id == elder_id)
        if type_:
            q = q.where(Event.type == type_)
        return list(self.s.scalars(q.order_by(Event.created_at.desc(), Event.id.desc()).limit(limit)))

    def since(self, elder_id: int, start: datetime) -> list[Event]:
        return list(
            self.s.scalars(
                select(Event).where(Event.elder_id == elder_id, Event.created_at >= start)
            )
        )
