from datetime import timedelta

from sqlalchemy.orm import Session

from app.core.time import slot_at, utcnow
from app.db.repositories.elders import ElderRepo
from app.db.repositories.events import EventRepo
from app.db.seed import reset
from app.notifications.dispatcher import Dispatcher
from app.services import checkin_service, concern_service, missed_dose_service
from app.services.appointment_service import add as add_appt
from app.services.schedule_service import local_today
from tests.conftest import FakeNotifier


def test_concern_creates_event_and_notifies_everyone(db: Session, dispatcher: Dispatcher,
                                                     notifier: FakeNotifier) -> None:
    elder = ElderRepo(db).first()
    out, text = concern_service.report_concern(db, dispatcher, elder, "I feel dizzy", "high", utcnow())
    ev = EventRepo(db).recent(elder.id, 1)[0]
    assert ev.type == "concern" and ev.notified is True
    assert {n for n, _ in notifier.sent} == {"Rohan", "Anita"}
    assert "dizzy" in notifier.sent[0][1]
    assert "emergency services" in text and "Rohan and Anita" in text
    assert out.delivered


def test_failed_delivery_is_saved_and_reply_is_honest(db: Session) -> None:
    bad = FakeNotifier(ok=False)
    elder = ElderRepo(db).first()
    _, text = concern_service.report_concern(db, Dispatcher(bad), elder, "help", "high", utcnow())
    ev = EventRepo(db).recent(elder.id, 1)[0]
    assert ev.notified is False
    assert "delayed" in text


def test_unwell_checkin_alerts_family_but_good_does_not(db: Session, dispatcher: Dispatcher,
                                                        notifier: FakeNotifier) -> None:
    elder = ElderRepo(db).first()
    checkin_service.record(db, dispatcher, elder, "good", None, utcnow())
    assert notifier.sent == []
    checkin_service.record(db, dispatcher, elder, "unwell", "tired", utcnow())
    assert len(notifier.sent) == 2
    assert EventRepo(db).recent(elder.id, 1)[0].type == "unwell"


def test_missed_dose_job_alerts_exactly_once(db: Session, dispatcher: Dispatcher,
                                             notifier: FakeNotifier) -> None:
    morning = slot_at(local_today(utcnow()), "07:30")
    reset(db, morning)  # nothing taken yet today
    now = slot_at(local_today(utcnow()), "09:30")  # BP 08:00 and sugar 08:30 are > 60 min overdue
    n1 = missed_dose_service.run(db, dispatcher, now, 60)
    sent_after_first = len(notifier.sent)
    n2 = missed_dose_service.run(db, dispatcher, now + timedelta(minutes=1), 60)
    assert n1 >= 2 and sent_after_first == n1 * 2  # two contacts per missed dose
    assert n2 == 0 and len(notifier.sent) == sent_after_first


def test_appointment_validation(db: Session) -> None:
    elder = ElderRepo(db).first()
    now = utcnow()
    assert not add_appt(db, elder.id, "Eye checkup", "next friday-ish", now).ok
    assert "passed" in add_appt(db, elder.id, "Eye checkup", "2020-01-01T10:00", now).reply
    assert not add_appt(db, elder.id, "  ", "2030-01-01T10:00", now).ok
    ok = add_appt(db, elder.id, "Eye checkup", (now + timedelta(days=2)).isoformat(), now)
    assert ok.ok and ok.reply.startswith("Added: Eye checkup")
