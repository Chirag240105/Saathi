"""APScheduler wiring. Logic lives in services/missed_dose_service.py (isolated, cut-able)."""
import logging

from apscheduler.schedulers.background import BackgroundScheduler

from app.core.config import get_settings
from app.core.time import utcnow
from app.db.session import session_scope
from app.notifications.dispatcher import get_dispatcher
from app.services import missed_dose_service

log = logging.getLogger("saathi.scheduler")


def check_missed_doses() -> int:
    try:
        with session_scope() as s:
            return missed_dose_service.run(
                s, get_dispatcher(), utcnow(), get_settings().missed_dose_minutes)
    except Exception:
        log.exception("missed dose check failed")
        return 0


def start_scheduler() -> BackgroundScheduler:
    sched = BackgroundScheduler(timezone="UTC")
    sched.add_job(check_missed_doses, "interval", minutes=1, id="missed_doses",
                  max_instances=1, coalesce=True)
    sched.start()
    return sched
