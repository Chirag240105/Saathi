"""Builds the day's dose slots and schedule."""
from dataclasses import dataclass
from datetime import date, datetime

from sqlalchemy.orm import Session

from app.core.time import day_bounds_utc, local_tz, slot_at, to_local
from app.db.models import Appointment, DoseLog, Medication
from app.db.repositories.appointments import AppointmentRepo
from app.db.repositories.dose_logs import DoseLogRepo
from app.db.repositories.medications import MedicationRepo


@dataclass
class Slot:
    medication: Medication
    at: datetime  # aware UTC
    log: DoseLog | None

    @property
    def status(self) -> str:
        return self.log.status if self.log else "pending"


@dataclass
class Schedule:
    day: date
    pending: list[Slot]
    appointments: list[Appointment]


def slots_for_day(session: Session, elder_id: int, day: date) -> list[Slot]:
    meds = MedicationRepo(session).list(elder_id)
    start, end = day_bounds_utc(day)
    logs = {
        (d.medication_id, d.scheduled_for): d
        for d in DoseLogRepo(session).between([m.id for m in meds], start, end)
    }
    slots = [
        Slot(m, at, logs.get((m.id, at)))
        for m in meds
        for t in m.times
        for at in [slot_at(day, t)]
    ]
    return sorted(slots, key=lambda s: s.at)


def build_schedule(session: Session, elder_id: int, day: date) -> Schedule:
    start, end = day_bounds_utc(day)
    return Schedule(
        day=day,
        pending=[s for s in slots_for_day(session, elder_id, day) if s.status != "taken"],
        appointments=AppointmentRepo(session).between(elder_id, start, end),
    )


def local_today(now: datetime) -> date:
    return now.astimezone(local_tz()).date()


def parse_day(value: str | None, now: datetime) -> date | None:
    """ISO date string -> date; None if absent; raises ValueError if bad."""
    if not value:
        return local_today(now)
    return datetime.fromisoformat(value).date() if "T" in value else date.fromisoformat(value)


def label_time(slot: Slot) -> str:
    return f"{to_local(slot.at):%H:%M}"
