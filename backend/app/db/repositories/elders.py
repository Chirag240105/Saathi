from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Elder


class ElderRepo:
    def __init__(self, s: Session) -> None:
        self.s = s

    def first(self) -> Elder | None:
        return self.s.scalars(select(Elder).order_by(Elder.id)).first()

    def get(self, elder_id: int) -> Elder | None:
        return self.s.get(Elder, elder_id)

    def add(self, **kw: object) -> Elder:
        e = Elder(**kw)
        self.s.add(e)
        self.s.flush()
        return e

    def all(self) -> list[Elder]:
        return list(self.s.scalars(select(Elder).order_by(Elder.id)))
