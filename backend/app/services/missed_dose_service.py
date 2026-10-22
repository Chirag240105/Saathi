"""Marks overdue unlogged doses as missed and alerts once per dose."""
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.db.repositories.dose_logs import DoseLogRepo
from app.db.repositories.elders import ElderRepo
from app.notifications.dispatcher import Dispatcher
from app.services import concern_service
from app.services import reply_service as reply
from app.services.schedule_service import local_today, slots_for_day

MAX_OVERDUE = timedelta(hours=12)


def run(session: Session, dispatcher: Dispatcher, now: datetime, threshold_minutes: int) -> int:
    """Returns how many doses were newly marked missed."""
    count = 0
    today = local_today(now)
    for elder in ElderRepo(session).all():
        for day in (today - timedelta(days=1), today):
            for slot in slots_for_day(session, elder.id, day):
                overdue = now - slot.at
                if slot.log is not None or overdue < timedelta(minutes=threshold_minutes):
                    continue
                if overdue > MAX_OVERDUE:
                    continue
                DoseLogRepo(session).upsert(slot.medication.id, slot.at, "missed", None)
                session.commit()  # the row guarantees "once"
                msg = f"{slot.medication.name} (due {reply.spoken_time(slot.at)})"
                concern_service.raise_event(
                    session, dispatcher, elder, "missed_dose", msg, "low", now,
                    text=reply.alert_text(elder.name, "missed_dose", msg, now),
                )
                count += 1
    return count
