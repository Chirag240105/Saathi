"""Appointments: parse, validate, add, list."""
from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.core.time import local_tz, to_local
from app.db.models import Appointment
from app.db.repositories.appointments import AppointmentRepo
from app.services import reply_service as reply


@dataclass
class AddResult:
    ok: bool
    reply: str
    appointment: Appointment | None = None


def parse_start(value: str) -> datetime | None:
    try:
        dt = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None
    return (dt.replace(tzinfo=local_tz()) if dt.tzinfo is None else dt).astimezone(UTC)


def add(session: Session, elder_id: int, title: str, starts_at: str, now: datetime) -> AddResult:
    title = (title or "").strip()
    if not title or len(title) > 120:
        return AddResult(False, reply.appointment_bad_title())
    when = parse_start(starts_at)
    if when is None:
        return AddResult(False, reply.appointment_bad_date())
    if when < now:
        return AddResult(False, reply.appointment_past())
    appt = AppointmentRepo(session).add(elder_id, title, when)
    session.commit()
    spoken = f"{reply.spoken_day(when, now)} at {reply.spoken_time(when)}"
    return AddResult(True, reply.appointment_added(title, spoken), appt)


def delete(session: Session, appt: Appointment) -> None:
    AppointmentRepo(session).delete(appt)
    session.commit()


def local_label(appt: Appointment) -> str:
    return f"{to_local(appt.starts_at):%a %d %b, %I:%M %p}"
