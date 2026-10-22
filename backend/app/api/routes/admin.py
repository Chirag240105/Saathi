from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import elder_of, get_db
from app.core.security import require_key
from app.db.repositories.contacts import ContactRepo
from app.db.seed import reset
from app.notifications.dispatcher import get_dispatcher

router = APIRouter(prefix="/api", tags=["admin"], dependencies=[Depends(require_key)])


@router.post("/admin/reset-demo")
def reset_demo(db: Session = Depends(get_db)) -> dict[str, str]:
    reset(db)
    return {"status": "reset"}


@router.post("/messages/check-in")
def gentle_check_in(db: Session = Depends(get_db)) -> dict[str, Any]:
    """Nudge the family circle to check in on the elder (sent over the active notifier)."""
    elder = elder_of(db)
    contacts = ContactRepo(db).list(elder.id)
    text = f"Gentle check-in: someone in the family asked everyone to say hello to {elder.name} today."
    deliveries = get_dispatcher().broadcast(contacts, text)
    return {"sent": sum(d.ok for d in deliveries), "total": len(deliveries)}
