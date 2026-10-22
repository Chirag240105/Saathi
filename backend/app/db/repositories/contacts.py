from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Contact


class ContactRepo:
    def __init__(self, s: Session) -> None:
        self.s = s

    def list(self, elder_id: int) -> list[Contact]:
        return list(
            self.s.scalars(select(Contact).where(Contact.elder_id == elder_id).order_by(Contact.id))
        )

    def get(self, contact_id: int) -> Contact | None:
        return self.s.get(Contact, contact_id)

    def add(self, **kw: object) -> Contact:
        c = Contact(**kw)
        self.s.add(c)
        self.s.flush()
        return c

    def delete(self, c: Contact) -> None:
        self.s.delete(c)
        self.s.flush()
