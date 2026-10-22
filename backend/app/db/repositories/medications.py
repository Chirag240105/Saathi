from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Medication


class MedicationRepo:
    def __init__(self, s: Session) -> None:
        self.s = s

    def list(self, elder_id: int) -> list[Medication]:
        return list(
            self.s.scalars(
                select(Medication).where(Medication.elder_id == elder_id).order_by(Medication.id)
            )
        )

    def get(self, med_id: int) -> Medication | None:
        return self.s.get(Medication, med_id)

    def add(self, **kw: object) -> Medication:
        m = Medication(**kw)
        self.s.add(m)
        self.s.flush()
        return m

    def delete(self, med: Medication) -> None:
        self.s.delete(med)
        self.s.flush()
