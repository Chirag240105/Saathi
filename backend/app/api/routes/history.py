from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import elder_of, get_db
from app.core.time import utcnow
from app.services import history_service

router = APIRouter(prefix="/api", tags=["history"])


@router.get("/history")
def history(days: int = Query(7, ge=1, le=60), db: Session = Depends(get_db)) -> dict[str, Any]:
    return {"days": history_service.build(db, elder_of(db).id, days, utcnow())}
