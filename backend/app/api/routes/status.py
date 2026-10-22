from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import elder_of, get_db
from app.core.time import to_local, utcnow
from app.schemas.care import EventOut
from app.services.status_service import get_status

router = APIRouter(prefix="/api", tags=["status"])


@router.get("/status")
def status(db: Session = Depends(get_db)) -> dict[str, Any]:
    now = utcnow()
    st = get_status(db, elder_of(db), now)
    last, appt = st.last_checkin, st.next_appointment
    return {
        "elder": {"id": st.elder.id, "name": st.elder.name, "age": st.elder.age},
        "overall": st.overall,
        "server_time": now,
        "doses": [{
            "medication_id": s.medication.id, "name": s.medication.name, "dose": s.medication.dose,
            "scheduled_for": s.at, "time": f"{to_local(s.at):%H:%M}", "status": s.status,
        } for s in st.doses],
        "last_checkin": {"mood": last.mood, "note": last.note, "created_at": last.created_at}
        if last else None,
        "next_appointment": {"id": appt.id, "title": appt.title, "starts_at": appt.starts_at}
        if appt else None,
        "recent_events": [EventOut.model_validate(e) for e in st.events],
    }
