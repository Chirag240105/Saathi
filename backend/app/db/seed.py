"""Fictional demo data. Idempotent: does nothing if an elder already exists."""
import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.time import local_tz, slot_at, utcnow
from app.db.base import Base
from app.db.repositories.appointments import AppointmentRepo
from app.db.repositories.checkins import CheckinRepo
from app.db.repositories.contacts import ContactRepo
from app.db.repositories.dose_logs import DoseLogRepo
from app.db.repositories.elders import ElderRepo
from app.db.repositories.events import EventRepo
from app.db.repositories.medications import MedicationRepo

MEDS = [
    ("BP tablet", ["bp tablet", "bp", "blood pressure", "blood pressure tablet", "pressure tablet",
                   "bp medicine"], "1 tablet", ["08:00", "20:00"]),
    ("Sugar tablet", ["sugar", "sugar medicine", "sugar pill", "diabetes tablet"], "1 tablet",
     ["08:30", "14:00", "21:30"]),
    ("Calcium", ["calcium tablet", "calcium"], "1 tablet", ["13:00"]),
    ("Vitamin D", ["vitamin d", "vit d", "vitamin d tablet"], "1 capsule", ["09:00"]),
]
MOODS = ["good", "good", "okay", "good", "okay", "good", "okay"]


def seed_if_empty(session: Session, now: datetime | None = None) -> bool:
    if ElderRepo(session).first() is not None:
        return False
    now = now or utcnow()
    rng = random.Random(42)
    today = now.astimezone(local_tz()).date()
    elder = ElderRepo(session).add(name="Sharda Devi", age=72, language="en-IN",
                                   timezone="Asia/Kolkata")
    meds = [MedicationRepo(session).add(elder_id=elder.id, name=n, aliases=a, dose=d, times=t)
            for n, a, d, t in MEDS]

    for back in range(7, 0, -1):  # past days
        day = today - timedelta(days=back)
        for m in meds:
            for t in m.times:
                at = slot_at(day, t)
                missed = rng.random() < 0.12
                DoseLogRepo(session).upsert(
                    m.id, at, "missed" if missed else "taken",
                    None if missed else at + timedelta(minutes=rng.randint(1, 25)))
        CheckinRepo(session).add(elder.id, MOODS[back - 1], None, slot_at(day, "10:00"))
    for m in meds:  # today: anything overdue by an hour is already taken
        for t in m.times:
            at = slot_at(today, t)
            if now - at >= timedelta(hours=1):
                DoseLogRepo(session).upsert(m.id, at, "taken", at + timedelta(minutes=3))
    CheckinRepo(session).add(elder.id, "good", None, now - timedelta(hours=2))

    AppointmentRepo(session).add(elder.id, "Doctor visit", slot_at(today + timedelta(days=1), "16:00"))
    AppointmentRepo(session).add(elder.id, "Eye checkup", slot_at(today + timedelta(days=3), "11:00"))
    ContactRepo(session).add(elder_id=elder.id, name="Rohan", telegram_chat_id=None, role="son")
    ContactRepo(session).add(elder_id=elder.id, name="Anita", telegram_chat_id=None, role="daughter")
    e = EventRepo(session).add(elder.id, "missed_dose", "Calcium (due one in the afternoon)",
                               "low", now - timedelta(days=2))
    e.notified, e.delivery = True, "console: 2/2 delivered"
    session.commit()
    return True


def reset(session: Session, now: datetime | None = None) -> None:
    """Delete all data and reseed."""
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    seed_if_empty(session, now)


if __name__ == "__main__":
    from app.db.session import init_engine, session_scope

    init_engine()
    with session_scope() as s:
        print("seeded" if seed_if_empty(s) else "already seeded")
