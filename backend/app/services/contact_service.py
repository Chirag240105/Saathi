from sqlalchemy.orm import Session

from app.db.models import Contact
from app.db.repositories.contacts import ContactRepo


def create(session: Session, elder_id: int, **data: object) -> Contact:
    c = ContactRepo(session).add(elder_id=elder_id, **data)
    session.commit()
    return c


def update(session: Session, contact: Contact, **data: object) -> Contact:
    for k, v in data.items():
        setattr(contact, k, v)
    session.commit()
    return contact


def delete(session: Session, contact: Contact) -> None:
    ContactRepo(session).delete(contact)
    session.commit()
