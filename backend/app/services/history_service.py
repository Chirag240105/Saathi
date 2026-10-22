"""Per-day dose and mood history."""
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.time import day_bounds_utc, to_local
from app.db.repositories.checkins import CheckinRepo
from app.services.schedule_service import local_today, slots_for_day

MOOD_SCORE = {"unwell": 1, "okay": 2, "good": 3}


def build(session: Session, elder_id: int, days: int, now: datetime) -> list[dict[str, object]]:
    today = local_today(now)
    start_day = today - timedelta(days=days - 1)
    checkins = CheckinRepo(session).since(elder_id, day_bounds_utc(start_day)[0])
    by_day: dict[object, list[str]] = {}
    for c in checkins:
        by_day.setdefault(to_local(c.created_at).date(), []).append(c.mood)
    out: list[dict[str, object]] = []
    for i in range(days):
        day = start_day + timedelta(days=i)
        slots = slots_for_day(session, elder_id, day)
        taken = sum(s.status == "taken" for s in slots)
        missed = sum(s.status == "missed" for s in slots)
        moods = by_day.get(day, [])
        mood = moods[-1] if moods else None
        out.append({
            "date": day.isoformat(), "taken": taken, "missed": missed,
            "pending": len(slots) - taken - missed, "mood": mood,
            "mood_score": MOOD_SCORE.get(mood) if mood else None,
        })
    return out
