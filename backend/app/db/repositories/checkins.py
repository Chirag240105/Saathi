from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Checkin


class CheckinRepo:
    def __init__(self, s: Session) -> None:
        self.s = s

    def add(self, elder_id: int, mood: str, note: str | None, at: datetime) -> Checkin:
        c = Checkin(elder_id=elder_id, mood=mood, note=note, created_at=at)
        self.s.add(c)
        self.s.flush()
        return c

    def latest(self, elder_id: int) -> Checkin | None:
        return self.s.scalars(
            select(Checkin).where(Checkin.elder_id == elder_id).order_by(Checkin.created_at.desc())
        ).first()

    def since(self, elder_id: int, start: datetime) -> list[Checkin]:
        return list(
            self.s.scalars(
                select(Checkin)
                .where(Checkin.elder_id == elder_id, Checkin.created_at >= start)
                .order_by(Checkin.created_at)
            )
        )
