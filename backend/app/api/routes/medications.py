from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import elder_of, get_db
from app.core.security import require_key
from app.db.repositories.medications import MedicationRepo
from app.schemas.care import MedicationIn, MedicationOut
from app.services import medication_service

router = APIRouter(prefix="/api/medications", tags=["medications"])


def _get(db: Session, med_id: int):  # type: ignore[no-untyped-def]
    med = MedicationRepo(db).get(med_id)
    if med is None:
        raise HTTPException(404, detail="Medicine not found")
    return med


@router.get("", response_model=list[MedicationOut])
def list_(db: Session = Depends(get_db)) -> list[MedicationOut]:
    return [MedicationOut.model_validate(m) for m in MedicationRepo(db).list(elder_of(db).id)]


@router.post("", response_model=MedicationOut, status_code=201, dependencies=[Depends(require_key)])
def create(body: MedicationIn, db: Session = Depends(get_db)) -> MedicationOut:
    return MedicationOut.model_validate(
        medication_service.create(db, elder_of(db).id, **body.model_dump()))


@router.put("/{med_id}", response_model=MedicationOut, dependencies=[Depends(require_key)])
def update(med_id: int, body: MedicationIn, db: Session = Depends(get_db)) -> MedicationOut:
    return MedicationOut.model_validate(
        medication_service.update(db, _get(db, med_id), **body.model_dump()))


@router.delete("/{med_id}", status_code=204, dependencies=[Depends(require_key)])
def delete(med_id: int, db: Session = Depends(get_db)) -> None:
    medication_service.delete(db, _get(db, med_id))
