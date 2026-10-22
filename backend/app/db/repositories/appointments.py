from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Appointment


class AppointmentRepo:
    def __init__(self, s: Session) -> None:
        self.s = s

    def add(self, elder_id: int, title: str, starts_at: datetime) -> Appointment:
        a = Appointment(elder_id=elder_id, title=title, starts_at=starts_at)
        self.s.add(a)
        self.s.flush()
        return a

    def get(self, appt_id: int) -> Appointment | None:
        return self.s.get(Appointment, appt_id)

    def between(self, elder_id: int, start: datetime, end: datetime) -> list[Appointment]:
        return list(
            self.s.scalars(
                select(Appointment)
                .where(
                    Appointment.elder_id == elder_id,
                    Appointment.starts_at >= start,
                    Appointment.starts_at < end,
                )
                .order_by(Appointment.starts_at)
            )
        )

    def upcoming(self, elder_id: int, after: datetime, limit: int = 20) -> list[Appointment]:
        return list(
            self.s.scalars(
                select(Appointment)
                .where(Appointment.elder_id == elder_id, Appointment.starts_at >= after)
                .order_by(Appointment.starts_at)
                .limit(limit)
            )
        )

    def delete(self, a: Appointment) -> None:
        self.s.delete(a)
        self.s.flush()
