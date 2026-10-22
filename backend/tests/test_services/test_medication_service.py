from datetime import timedelta

import pytest
from sqlalchemy.orm import Session

from app.core.time import local_tz, slot_at, utcnow
from app.db.repositories.elders import ElderRepo
from app.db.seed import reset
from app.services import medication_service as med
from app.services.schedule_service import local_today, slots_for_day


@pytest.mark.parametrize("phrase", ["BP tablet", "bp", "Blood Pressure", "my blood pressure tablet"])
def test_bp_phrases_resolve_to_same_medicine(db: Session, phrase: str) -> None:
    elder = ElderRepo(db).first()
    found = med.find_medicine(db, elder.id, phrase)
    assert found is not None and found.name == "BP tablet"


def test_other_aliases_and_unknown(db: Session) -> None:
    elder = ElderRepo(db).first()
    assert med.find_medicine(db, elder.id, "sugar medicine").name == "Sugar tablet"
    assert med.find_medicine(db, elder.id, "vit d").name == "Vitamin D"
    assert med.find_medicine(db, elder.id, "aspirin") is None
    assert med.find_medicine(db, elder.id, "   ") is None


def _early_morning():
    # 07:30 local: every slot of today is still in the future, so nothing is pre-taken
    return slot_at(local_today(utcnow()), "07:30")


def test_log_then_duplicate_guard(db: Session) -> None:
    now = _early_morning()
    reset(db, now)
    elder = ElderRepo(db).first()
    first = med.log_taken(db, elder.id, "BP tablet", now)
    assert first.status == "logged"
    again = med.log_taken(db, elder.id, "bp", now + timedelta(minutes=10))
    assert again.status == "duplicate"
    taken = [s for s in slots_for_day(db, elder.id, local_today(now))
             if s.medication.name == "BP tablet" and s.status == "taken"]
    assert len(taken) == 1  # no second row


def test_unknown_medicine_lists_names(db: Session) -> None:
    elder = ElderRepo(db).first()
    r = med.log_taken(db, elder.id, "aspirin", utcnow())
    assert r.status == "unknown" and "BP tablet" in (r.names or [])


def test_generic_phrase_logs_nearest_pending(db: Session) -> None:
    now = _early_morning()
    reset(db, now)
    elder = ElderRepo(db).first()
    r = med.log_taken(db, elder.id, "my medicine", now)
    assert r.status == "logged" and r.medication.name == "BP tablet"  # 08:00 is nearest


def test_local_tz_is_kolkata() -> None:
    assert str(local_tz()) == "Asia/Kolkata"
