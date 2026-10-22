"""Offline rule-based intent matching. No API key, no network: the demo can never fail."""
import re
from datetime import datetime, timedelta

from app.simulator.llm.base import Plan

WEEKDAYS = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4,
            "saturday": 5, "sunday": 6, "mon": 0, "tue": 1, "tues": 1, "wed": 2, "thu": 3,
            "thur": 3, "thurs": 3, "fri": 4, "sat": 5, "sun": 6}
URGENT = re.compile(
    r"\b(help|emergency|dizzy|dizziness|giddy|faint|fainted|fell|fallen|fall|chest|breath|breathe|"
    r"breathing|pain|hurts?|hurting|bleed|bleeding|vomit|vomiting|sick|unwell|weak|ache|aching|"
    r"nausea|ambulance)\b|\bnot (feeling )?(so )?(well|good|okay|ok|right|great)\b")
LOW_MOOD = re.compile(r"\b(tired|low|sad|lonely|down|bad|exhausted|worried|anxious)\b")
TOOK = re.compile(r"\b(took|taken|take|had|ate|swallowed|finished)\b\s+(.*)$")
FEEL = re.compile(r"\b(feel|feeling|i am|i'm|im|doing)\b")
GOOD = re.compile(r"\b(good|great|wonderful|happy|fantastic|well|better|fine)\b")
OKAY = re.compile(r"\b(okay|ok|alright|all right|so-so|normal)\b")
SCHEDULE = re.compile(
    r"\bwhat\b.*\b(have|next|today|due|left|medicine|medicines|tablet|tablets|schedule|plan)\b|"
    r"\b(schedule|agenda|remaining)\b|\bwhat'?s next\b|\bany(thing)?\b.*\b(today|left|due)\b|"
    r"\bwhat.*(to do|on)\b")
ADD_VERB = re.compile(r"\b(add|book|schedule|set up|fix|make)\b|remind me (of|about)")
NOISE_HEAD = re.compile(r"^(?:my|the|a|an|some|just|already|both|all|any)\s+")
NOISE_TAIL = re.compile(
    r"\s+(?:now|today|already|just|too|again|this morning|this evening|tonight|just now|"
    r"a while ago|please)$")
TIME_RE = re.compile(r"(?:\bat\s*|@\s*)(\d{1,2})(?::(\d{2}))?\s*(a\.?m\.?|p\.?m\.?)?")
TIME_AMPM = re.compile(r"\b(\d{1,2})(?::(\d{2}))?\s*(a\.?m\.?|p\.?m\.?)\b")


def _clean(text: str) -> str:
    return re.sub(r"[’`]", "'", text.lower()).strip().rstrip(".!? ")


def _hour(h: int, ampm: str | None) -> int:
    if ampm:
        pm = ampm.startswith("p")
        return (h % 12) + (12 if pm else 0)
    return h + 12 if 1 <= h <= 6 else h  # "at 4" means 4 pm; "at 11" means 11 am


def parse_when(t: str, now: datetime) -> tuple[datetime | None, str]:
    """Returns (local datetime or None, text with date/time phrases removed)."""
    rest, hour, minute = t, None, 0
    m = TIME_RE.search(t) or TIME_AMPM.search(t)
    if m:
        hour, minute = _hour(int(m.group(1)), m.group(3)), int(m.group(2) or 0)
        rest = rest.replace(m.group(0), " ")
    elif "noon" in t:
        hour = 12
    day = None
    for word in sorted(WEEKDAYS, key=len, reverse=True):
        if re.search(rf"\b{word}\b", rest):
            ahead = (WEEKDAYS[word] - now.weekday()) % 7 or 7
            day = now.date() + timedelta(days=ahead)
            rest = re.sub(rf"\b(next\s+|on\s+)?{word}\b", " ", rest)
            break
    if day is None:
        if "day after tomorrow" in rest:
            day, rest = now.date() + timedelta(days=2), rest.replace("day after tomorrow", " ")
        elif "tomorrow" in rest:
            day, rest = now.date() + timedelta(days=1), rest.replace("tomorrow", " ")
        elif re.search(r"\btoday\b", rest):
            day, rest = now.date(), re.sub(r"\btoday\b", " ", rest)
    if hour is None or hour > 23 or minute > 59:
        return None, rest
    if day is None:
        day = now.date()
        if datetime.combine(day, datetime.min.time(), tzinfo=now.tzinfo).replace(
                hour=hour, minute=minute) <= now:
            day += timedelta(days=1)
    return datetime(day.year, day.month, day.day, hour, minute), rest


def _title(rest: str) -> str:
    s = ADD_VERB.sub(" ", rest)
    s = re.sub(r"\b(please|appointment with|appointment for|appointment|an?|the|my|for|on|at|with me)\b",
               " ", s)
    s = re.sub(r"\s+", " ", s).strip(" ,.")
    return s[:1].upper() + s[1:]


def plan(text: str, now: datetime) -> Plan | None:
    """`now` must be a timezone-aware local datetime."""
    t = _clean(text)
    if not t:
        return None
    if ADD_VERB.search(t) and not TOOK.search(t.replace("remind", "")):
        when, rest = parse_when(t, now)
        return Plan("add_appointment", {"title": _title(rest),
                                        "starts_at": when.isoformat() if when else ""})
    if URGENT.search(t):
        return Plan("report_concern", {"message": text.strip(), "severity": "high"})
    took = TOOK.search(t)
    if took:
        name = took.group(2)
        for _ in range(3):
            name = NOISE_HEAD.sub("", NOISE_TAIL.sub("", name.strip()))
        return Plan("log_medication_taken", {"name": name.strip() or "medicine"})
    if LOW_MOOD.search(t) and FEEL.search(t):
        return Plan("daily_checkin", {"mood": "unwell", "note": text.strip()})
    if FEEL.search(t):
        if OKAY.search(t) and not GOOD.search(t.replace("all right", "")):
            return Plan("daily_checkin", {"mood": "okay", "note": text.strip()})
        if GOOD.search(t):
            return Plan("daily_checkin", {"mood": "good", "note": text.strip()})
        if OKAY.search(t):
            return Plan("daily_checkin", {"mood": "okay", "note": text.strip()})
    if SCHEDULE.search(t):
        return Plan("get_today_schedule", {})
    return None
