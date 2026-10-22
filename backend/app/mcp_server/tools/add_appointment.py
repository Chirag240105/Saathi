from mcp.server.fastmcp import Context, FastMCP

from app.core.time import utcnow
from app.db.session import session_scope
from app.mcp_server.logging import tracked
from app.services import appointment_service
from app.services.elder_service import primary_elder


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    @tracked("add_appointment")
    def add_appointment(title: str, starts_at: str, ctx: Context | None = None) -> str:
        """Add a doctor visit or other appointment. title is what it is for ("eye checkup");
        starts_at is the local date and time in ISO format, for example 2026-10-30T11:00. Use for
        "add eye checkup Friday at 11". The spoken confirmation repeats the day and time."""
        with session_scope() as s:
            elder = primary_elder(s)
            return appointment_service.add(s, elder.id, title, starts_at, utcnow()).reply
