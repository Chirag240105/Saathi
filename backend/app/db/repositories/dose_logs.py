from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import DoseLog


class DoseLogRepo:
    def __init__(self, s: Session) -> None:
        self.s = s

    def between(self, med_ids: list[int], start: datetime, end: datetime) -> list[DoseLog]:
        if not med_ids:
            return []
        q = select(DoseLog).where(
            DoseLog.medication_id.in_(med_ids),
            DoseLog.scheduled_for >= start,
            DoseLog.scheduled_for < end,
        )
        return list(self.s.scalars(q))

    def get_slot(self, med_id: int, scheduled_for: datetime) -> DoseLog | None:
        return self.s.scalars(
            select(DoseLog).where(
                DoseLog.medication_id == med_id, DoseLog.scheduled_for == scheduled_for
            )
        ).first()

    def last_taken(self, med_id: int) -> DoseLog | None:
        return self.s.scalars(
            select(DoseLog)
            .where(DoseLog.medication_id == med_id, DoseLog.status == "taken")
            .order_by(DoseLog.taken_at.desc())
        ).first()

    def upsert(
        self, med_id: int, scheduled_for: datetime, status: str, taken_at: datetime | None
    ) -> DoseLog:
        row = self.get_slot(med_id, scheduled_for)
        if row is None:
            row = DoseLog(medication_id=med_id, scheduled_for=scheduled_for)
            self.s.add(row)
        row.status, row.taken_at = status, taken_at
        self.s.flush()
        return row
