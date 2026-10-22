from typing import Literal

from mcp.server.fastmcp import Context, FastMCP

from app.core.time import utcnow
from app.db.session import session_scope
from app.mcp_server.logging import tracked
from app.notifications.dispatcher import get_dispatcher
from app.services import checkin_service
from app.services.elder_service import primary_elder


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    @tracked("daily_checkin")
    def daily_checkin(
        mood: Literal["good", "okay", "unwell"], note: str | None = None,
        ctx: Context | None = None,
    ) -> str:
        """Save how the elder says they feel today: good, okay or unwell, with an optional note
        in their own words. Use for "I am feeling fine today" or "I am a bit low". If the mood is
        unwell, the family is told straight away. For sudden symptoms, use report_concern."""
        with session_scope() as s:
            elder = primary_elder(s)
            clean = (note or "").strip()[:300] or None
            return checkin_service.record(s, get_dispatcher(), elder, mood, clean, utcnow())
