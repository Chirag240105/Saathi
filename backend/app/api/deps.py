from collections.abc import Iterator

from sqlalchemy.orm import Session

from app.db.models import Elder
from app.db.session import get_factory
from app.services.elder_service import primary_elder


def get_db() -> Iterator[Session]:
    session = get_factory()()
    try:
        yield session
    finally:
        session.close()


def elder_of(session: Session) -> Elder:
    return primary_elder(session)
