from datetime import UTC

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import elder_of, get_db
from app.core.security import require_key
from app.core.time import local_tz, utcnow
from app.db.repositories.appointments import AppointmentRepo
from app.schemas.care import AppointmentIn, AppointmentOut
from app.services import appointment_service

router = APIRouter(prefix="/api/appointments", tags=["appointments"])


@router.get("", response_model=list[AppointmentOut])
def list_(db: Session = Depends(get_db)) -> list[AppointmentOut]:
    rows = AppointmentRepo(db).upcoming(elder_of(db).id, utcnow(), 50)
    return [AppointmentOut.model_validate(a) for a in rows]


@router.post("", response_model=AppointmentOut, status_code=201, dependencies=[Depends(require_key)])
def create(body: AppointmentIn, db: Session = Depends(get_db)) -> AppointmentOut:
    when = body.starts_at
    when = (when.replace(tzinfo=local_tz()) if when.tzinfo is None else when).astimezone(UTC)
    res = appointment_service.add(db, elder_of(db).id, body.title, when.isoformat(), utcnow())
    if not res.ok or res.appointment is None:
        raise HTTPException(422, detail=res.reply)
    return AppointmentOut.model_validate(res.appointment)


@router.delete("/{appt_id}", status_code=204, dependencies=[Depends(require_key)])
def delete(appt_id: int, db: Session = Depends(get_db)) -> None:
    appt = AppointmentRepo(db).get(appt_id)
    if appt is None:
        raise HTTPException(404, detail="Appointment not found")
    appointment_service.delete(db, appt)
