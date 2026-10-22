"""Timezone helpers. Store UTC, display in the configured zone."""
from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from app.core.config import get_settings


def local_tz() -> ZoneInfo:
    return ZoneInfo(get_settings().timezone)


def utcnow() -> datetime:
    return datetime.now(UTC)


def now_local() -> datetime:
    return datetime.now(local_tz())


def to_local(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(local_tz())


def day_bounds_utc(day: date, tz: ZoneInfo | None = None) -> tuple[datetime, datetime]:
    """Start (inclusive) and end (exclusive) of a local calendar day, as aware UTC datetimes."""
    tz = tz or local_tz()
    start = datetime.combine(day, time(0, 0), tzinfo=tz)
    end = datetime.combine(day + timedelta(days=1), time(0, 0), tzinfo=tz)
    return start.astimezone(UTC), end.astimezone(UTC)


def slot_at(day: date, hhmm: str, tz: ZoneInfo | None = None) -> datetime:
    """Aware UTC datetime for a local day + 'HH:MM'."""
    tz = tz or local_tz()
    h, m = (int(x) for x in hhmm.split(":"))
    return datetime.combine(day, time(h, m), tzinfo=tz).astimezone(UTC)
