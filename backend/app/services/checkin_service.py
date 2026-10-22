"""Daily mood check-in. 'unwell' also alerts family."""
from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models import Elder
from app.db.repositories.checkins import CheckinRepo
from app.notifications.dispatcher import Dispatcher
from app.services import concern_service
from app.services import reply_service as reply

MOODS = ("good", "okay", "unwell")


def record(
    session: Session, dispatcher: Dispatcher, elder: Elder, mood: str, note: str | None,
    now: datetime,
) -> str:
    """Store the check-in and return the spoken reply."""
    CheckinRepo(session).add(elder.id, mood, note, now)
    session.commit()
    if mood != "unwell":
        return reply.checkin(mood, [], True)
    out = concern_service.raise_event(
        session, dispatcher, elder, "unwell", note or "feeling unwell", "high", now,
        text=reply.alert_text(elder.name, "unwell", note or "feeling unwell", now),
    )
    return reply.checkin(mood, out.names, out.delivered)
