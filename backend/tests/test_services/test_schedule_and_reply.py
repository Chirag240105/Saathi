from datetime import datetime

from sqlalchemy.orm import Session

from app.core.time import slot_at, utcnow
from app.db.repositories.elders import ElderRepo
from app.db.seed import reset
from app.services import reply_service as reply
from app.services.schedule_service import build_schedule, local_today


def test_spoken_time() -> None:
    day = local_today(utcnow())
    assert reply.spoken_time(slot_at(day, "20:00")) == "eight in the evening"
    assert reply.spoken_time(slot_at(day, "08:30")) == "eight thirty in the morning"
    assert reply.spoken_time(slot_at(day, "14:05")) == "two oh five in the afternoon"
    assert reply.spoken_time(slot_at(day, "12:00")) == "twelve noon"


def test_schedule_reply_is_short_and_sorted(db: Session) -> None:
    now = slot_at(local_today(utcnow()), "07:30")
    reset(db, now)
    elder = ElderRepo(db).first()
    sched = build_schedule(db, elder.id, local_today(now))
    assert [s.at for s in sched.pending] == sorted(s.at for s in sched.pending)
    items: list[tuple[str, datetime]] = [(f"your {s.medication.name}", s.at) for s in sched.pending]
    text = reply.schedule(items)
    assert len(text.split()) < 40 and "more" in text


def test_empty_schedule_reply() -> None:
    assert "nothing left" in reply.schedule([])
