"""Aggregates what the family dashboard needs."""
from dataclasses import dataclass
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.db.models import Appointment, Checkin, Elder, Event
from app.db.repositories.appointments import AppointmentRepo
from app.db.repositories.checkins import CheckinRepo
from app.db.repositories.events import EventRepo
from app.services.schedule_service import Slot, local_today, slots_for_day

ALERT_WINDOW = timedelta(hours=4)


@dataclass
class Status:
    elder: Elder
    doses: list[Slot]
    last_checkin: Checkin | None
    next_appointment: Appointment | None
    events: list[Event]
    overall: str


def overall_status(doses: list[Slot], last: Checkin | None, events: list[Event], now: datetime) -> str:
    recent = [e for e in events if now - e.created_at <= ALERT_WINDOW]
    if any(e.type == "unwell" or (e.type == "concern" and e.severity == "high") for e in recent):
        return "alert"
    if any(d.status == "missed" for d in doses) or any(e.type == "concern" for e in recent):
        return "attention"
    if last and last.mood == "unwell" and now - last.created_at <= ALERT_WINDOW:
        return "attention"
    return "all_good"


def get_status(session: Session, elder: Elder, now: datetime) -> Status:
    doses = slots_for_day(session, elder.id, local_today(now))
    last = CheckinRepo(session).latest(elder.id)
    events = EventRepo(session).recent(elder.id, 10)
    nxt = AppointmentRepo(session).upcoming(elder.id, now, 1)
    return Status(elder, doses, last, nxt[0] if nxt else None, events,
                  overall_status(doses, last, events, now))
