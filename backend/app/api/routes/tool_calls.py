from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.repositories.tool_calls import ToolCallRepo
from app.schemas.care import ToolCallOut

router = APIRouter(prefix="/api", tags=["tool-calls"])


@router.get("/tool-calls", response_model=list[ToolCallOut])
def tool_calls(
    limit: int = Query(50, ge=1, le=200),
    after_id: int | None = Query(None, ge=0),
    db: Session = Depends(get_db),
) -> list[ToolCallOut]:
    """Newest first. Pass after_id to fetch only calls made since the last poll."""
    return [ToolCallOut.model_validate(t) for t in ToolCallRepo(db).list(limit, after_id)]
