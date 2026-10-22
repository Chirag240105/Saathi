from sqlalchemy.orm import Session

from app.db.models import Elder
from app.db.repositories.elders import ElderRepo


def primary_elder(session: Session) -> Elder:
    """The demo supports one elder; multi-elder is a future extension."""
    elder = ElderRepo(session).first()
    if elder is None:
        raise LookupError("No elder configured. Run the seed.")
    return elder
