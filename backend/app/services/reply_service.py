"""All speakable reply templates live here so tone is easy to tune.

Rules: warm, calm, short (<40 words), spoken-form times, never medical advice, no internals.
"""
from datetime import datetime

from app.core.time import to_local

EMERGENCY = "Call emergency services if it gets worse."
_ONES = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
         "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
         "eighteen", "nineteen"]
_TENS = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty"}


def _minutes_words(m: int) -> str:
    if m < 20:
        return ("oh " + _ONES[m]) if m < 10 else _ONES[m]
    tens, ones = divmod(m, 10)
    return _TENS[tens] + (f" {_ONES[ones]}" if ones else "")


def spoken_time(dt: datetime) -> str:
    """'eight in the evening', 'eight thirty in the morning'."""
    dt = to_local(dt)
    h, m = dt.hour, dt.minute
    if (h, m) == (0, 0):
        return "midnight"
    if (h, m) == (12, 0):
        return "twelve noon"
    hour = _ONES[h % 12 or 12]
    clock = hour if m == 0 else f"{hour} {_minutes_words(m)}"
    part = ("in the morning" if 5 <= h < 12 else "in the afternoon" if 12 <= h < 17
            else "in the evening" if 17 <= h < 21 else "at night")
    return f"{clock} {part}"


def spoken_day(dt: datetime, now: datetime) -> str:
    d, n = to_local(dt).date(), to_local(now).date()
    delta = (d - n).days
    if delta == 0:
        return "today"
    if delta == 1:
        return "tomorrow"
    if 1 < delta < 7:
        return f"on {to_local(dt):%A}"
    return f"on {d.day} {d:%B}"


def join_words(items: list[str]) -> str:
    if not items:
        return ""
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def family_names(names: list[str]) -> str:
    return join_words(names) if names else "your family"


def schedule(items: list[tuple[str, datetime]], day_label: str = "today") -> str:
    """items: (label, time) already sorted soonest first."""
    if not items:
        return f"You have nothing left {day_label}. Enjoy a restful time." if day_label == "today" \
            else f"You have nothing planned {day_label}."
    shown = [f"{label} at {spoken_time(at)}" for label, at in items[:3]]
    extra = len(items) - 3
    tail = f", and {extra} more" if extra > 0 else ""
    lead = "You have" if day_label == "today" else f"{day_label.capitalize()} you have"
    return f"{lead} {join_words(shown)}{tail}."


def med_logged(name: str, next_text: str | None) -> str:
    nxt = f"Next is {next_text}." if next_text else "That was the last one for today."
    return f"Done, well done. I have noted your {name}. {nxt}"


def med_duplicate(name: str) -> str:
    return f"I already noted your {name} a little while ago, so I have not added it again."


def med_unknown(names: list[str]) -> str:
    return f"I could not find that medicine. Your medicines are {join_words(names)}."


def med_all_done(name: str) -> str:
    return f"You have already noted all your {name} doses for today."


def checkin(mood: str, names: list[str], delivered: bool) -> str:
    if mood == "good":
        return "Glad to hear it. Have a lovely day."
    if mood == "okay":
        return "Thank you for telling me. I hope the day gets brighter."
    who = family_names(names)
    told = f"I have told {who}." if delivered else "I could not reach them just now, but I saved it."
    return f"I am sorry you are not feeling well. {told} Please rest. {EMERGENCY}"


def concern(severity: str, names: list[str], delivered: bool) -> str:
    who = family_names(names)
    if not delivered:
        base = "I could not reach your family just now, so the message may be delayed, but I saved it."
        return f"{base} Please sit down and rest. {EMERGENCY}"
    if severity == "high":
        return f"I have told {who}. Please sit down and rest. {EMERGENCY}"
    return f"Thank you for telling me. I have let {who} know."


def appointment_added(title: str, when: str) -> str:
    return f"Added: {title} {when}."


def appointment_bad_date() -> str:
    return "I did not catch the date. Could you say the day and time again?"


def appointment_past() -> str:
    return "That time has already passed. Could you give me a time ahead?"


def appointment_bad_title() -> str:
    return "What is the appointment for? Please tell me the name and the time."


def generic_error() -> str:
    return "Sorry, something went wrong on my side. Please try again in a moment."


# ---- Telegram texts for family ----
def alert_text(elder: str, kind: str, message: str, at: datetime, severity: str = "high") -> str:
    t = f"{to_local(at):%-I:%M %p}"
    if kind == "unwell":
        return f"{elder} reported feeling unwell today ({t}). Note: \"{message}\""
    if kind == "missed_dose":
        return f"Missed dose: {message}"
    head = "ALERT" if severity == "high" else "Note"
    return f"{head}: {elder} said \"{message}\" at {t}."
