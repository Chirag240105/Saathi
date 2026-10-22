from mcp.server.fastmcp import Context, FastMCP

from app.core.time import slot_at, utcnow
from app.db.session import session_scope
from app.mcp_server.logging import tracked
from app.services import reply_service as reply
from app.services.elder_service import primary_elder
from app.services.schedule_service import build_schedule, parse_day


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    @tracked("get_today_schedule")
    def get_today_schedule(date: str | None = None, ctx: Context | None = None) -> str:
        """Tell the elder what is still left to do today: medicines not yet taken and today's
        appointments, soonest first. Use when they ask "what do I have today", "what is next",
        or "do I have any medicine left". Optional date in YYYY-MM-DD for another day."""
        now = utcnow()
        try:
            day = parse_day(date, now)
        except ValueError:
            return reply.appointment_bad_date()
        assert day is not None
        with session_scope() as s:
            elder = primary_elder(s)
            sched = build_schedule(s, elder.id, day)
            is_today = day == parse_day(None, now)
            items = [(f"your {reply.plain(x.medication.name)}", x.at) for x in sched.pending]
            items += [(reply.plain(a.title), a.starts_at) for a in sched.appointments
                      if not is_today or a.starts_at >= now]
            items.sort(key=lambda i: i[1])
            label = "today" if is_today else reply.spoken_day(slot_at(day, "12:00"), now)
            return reply.schedule(items, label)
