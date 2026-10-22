"""Events: store first, then notify family."""
from dataclasses import dataclass, field
from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models import Elder, Event
from app.db.repositories.contacts import ContactRepo
from app.db.repositories.events import EventRepo
from app.notifications.base import Delivery
from app.notifications.dispatcher import Dispatcher
from app.services import reply_service as reply


@dataclass
class AlertOutcome:
    event: Event
    deliveries: list[Delivery] = field(default_factory=list)
    names: list[str] = field(default_factory=list)

    @property
    def delivered(self) -> bool:
        return any(d.ok for d in self.deliveries)


def raise_event(
    session: Session,
    dispatcher: Dispatcher,
    elder: Elder,
    kind: str,
    message: str,
    severity: str,
    now: datetime,
    text: str | None = None,
) -> AlertOutcome:
    """Persist the event, commit, then notify all contacts. Never raises on notifier failure."""
    event = EventRepo(session).add(elder.id, kind, message, severity, now)
    session.commit()
    contacts = ContactRepo(session).list(elder.id)
    body = text or reply.alert_text(elder.name, kind, message, now, severity)
    deliveries = dispatcher.broadcast(contacts, body)
    event.notified = any(d.ok for d in deliveries)
    event.delivery = dispatcher.summarize(deliveries)
    session.commit()
    return AlertOutcome(event, deliveries, [c.name for c in contacts])


def report_concern(
    session: Session, dispatcher: Dispatcher, elder: Elder, message: str, severity: str,
    now: datetime,
) -> tuple[AlertOutcome, str]:
    out = raise_event(session, dispatcher, elder, "concern", message, severity, now)
    return out, reply.concern(severity, out.names, out.delivered)
