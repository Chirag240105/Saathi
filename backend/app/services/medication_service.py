"""Medicine matching (rapidfuzz), dose logging with duplicate guard, and CRUD."""
from dataclasses import dataclass
from datetime import datetime, timedelta

from rapidfuzz import fuzz, process
from sqlalchemy.orm import Session

from app.db.models import Medication
from app.db.repositories.dose_logs import DoseLogRepo
from app.db.repositories.medications import MedicationRepo
from app.services.schedule_service import Slot, local_today, slots_for_day

DUPLICATE_WINDOW = timedelta(minutes=30)
MATCH_CUTOFF = 80
GENERIC = {"medicine", "medicines", "medication", "tablet", "tablets", "pill", "pills", "meds",
           "my medicine", "my tablet", "my tablets", "my pills", "my medication", "my meds"}


@dataclass
class LogResult:
    status: str  # logged | duplicate | unknown | all_done
    medication: Medication | None = None
    next_slot: Slot | None = None
    names: list[str] | None = None


def find_medicine(session: Session, elder_id: int, name: str) -> Medication | None:
    q = (name or "").strip().lower()
    if not q:
        return None
    meds = MedicationRepo(session).list(elder_id)
    choices: dict[str, Medication] = {}
    for m in meds:
        for label in [m.name, *(m.aliases or [])]:
            choices.setdefault(label.lower(), m)
    hit = process.extractOne(q, list(choices), scorer=fuzz.WRatio, score_cutoff=MATCH_CUTOFF)
    return choices[hit[0]] if hit else None


def _pending(session: Session, elder_id: int, now: datetime) -> list[Slot]:
    return [s for s in slots_for_day(session, elder_id, local_today(now)) if s.status != "taken"]


def next_pending(session: Session, elder_id: int, now: datetime) -> Slot | None:
    pend = _pending(session, elder_id, now)
    return pend[0] if pend else None


def log_taken(session: Session, elder_id: int, name: str, now: datetime) -> LogResult:
    names = [m.name for m in MedicationRepo(session).list(elder_id)]
    pending = _pending(session, elder_id, now)
    if (name or "").strip().lower() in GENERIC:
        if not pending:
            return LogResult("all_done", names=names)
        med = min(pending, key=lambda s: abs(s.at - now)).medication
    else:
        found = find_medicine(session, elder_id, name)
        if found is None:
            return LogResult("unknown", names=names)
        med = found

    last = DoseLogRepo(session).last_taken(med.id)
    if last and last.taken_at and now - last.taken_at < DUPLICATE_WINDOW:
        return LogResult("duplicate", med)
    mine = [s for s in pending if s.medication.id == med.id]
    if not mine:
        return LogResult("all_done", med)
    slot = min(mine, key=lambda s: abs(s.at - now))
    DoseLogRepo(session).upsert(med.id, slot.at, "taken", now)
    session.commit()
    nxt = next_pending(session, elder_id, now)
    return LogResult("logged", med, nxt)


# ---- CRUD used by REST ----
def create(session: Session, elder_id: int, **data: object) -> Medication:
    med = MedicationRepo(session).add(elder_id=elder_id, **data)
    session.commit()
    return med


def update(session: Session, med: Medication, **data: object) -> Medication:
    for k, v in data.items():
        setattr(med, k, v)
    session.commit()
    return med


def delete(session: Session, med: Medication) -> None:
    MedicationRepo(session).delete(med)
    session.commit()
