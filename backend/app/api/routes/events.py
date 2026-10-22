from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import elder_of, get_db
from app.db.repositories.events import EventRepo
from app.schemas.care import EventOut

router = APIRouter(prefix="/api", tags=["events"])


@router.get("/events", response_model=list[EventOut])
def events(
    limit: int = Query(20, ge=1, le=200),
    type: str | None = Query(None, pattern="^(concern|missed_dose|unwell)$"),
    db: Session = Depends(get_db),
) -> list[EventOut]:
    return [EventOut.model_validate(e) for e in EventRepo(db).recent(elder_of(db).id, limit, type)]
