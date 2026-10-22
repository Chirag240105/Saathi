from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import elder_of, get_db
from app.core.security import require_key
from app.db.repositories.contacts import ContactRepo
from app.schemas.care import ContactIn, ContactOut
from app.services import contact_service

router = APIRouter(prefix="/api/contacts", tags=["contacts"])


def _get(db: Session, cid: int):  # type: ignore[no-untyped-def]
    c = ContactRepo(db).get(cid)
    if c is None:
        raise HTTPException(404, detail="Contact not found")
    return c


@router.get("", response_model=list[ContactOut])
def list_(db: Session = Depends(get_db)) -> list[ContactOut]:
    return [ContactOut.model_validate(c) for c in ContactRepo(db).list(elder_of(db).id)]


@router.post("", response_model=ContactOut, status_code=201, dependencies=[Depends(require_key)])
def create(body: ContactIn, db: Session = Depends(get_db)) -> ContactOut:
    return ContactOut.model_validate(contact_service.create(db, elder_of(db).id, **body.model_dump()))


@router.put("/{cid}", response_model=ContactOut, dependencies=[Depends(require_key)])
def update(cid: int, body: ContactIn, db: Session = Depends(get_db)) -> ContactOut:
    return ContactOut.model_validate(contact_service.update(db, _get(db, cid), **body.model_dump()))


@router.delete("/{cid}", status_code=204, dependencies=[Depends(require_key)])
def delete(cid: int, db: Session = Depends(get_db)) -> None:
    contact_service.delete(db, _get(db, cid))
