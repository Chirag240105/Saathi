from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import ToolCall


class ToolCallRepo:
    def __init__(self, s: Session) -> None:
        self.s = s

    def add(self, **kw: Any) -> ToolCall:
        tc = ToolCall(**kw)
        self.s.add(tc)
        self.s.flush()
        return tc

    def list(self, limit: int = 50, after_id: int | None = None) -> list[ToolCall]:
        q = select(ToolCall)
        if after_id is not None:
            q = q.where(ToolCall.id > after_id)
        return list(self.s.scalars(q.order_by(ToolCall.id.desc()).limit(limit)))
