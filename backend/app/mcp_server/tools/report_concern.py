from typing import Literal

from mcp.server.fastmcp import Context, FastMCP

from app.core.time import utcnow
from app.db.session import session_scope
from app.mcp_server.logging import tracked
from app.notifications.dispatcher import get_dispatcher
from app.services import concern_service
from app.services.elder_service import primary_elder


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    @tracked("report_concern")
    def report_concern(
        message: str, severity: Literal["low", "high"] = "high", ctx: Context | None = None
    ) -> str:
        """Alert the family right now that the elder has a problem. Use for "I feel dizzy",
        "I fell", "I need help", chest pain or any worry. Pass the elder's own words as message.
        Severity is high unless it is clearly minor. This only informs family; it does not
        diagnose and does not replace emergency services."""
        text = (message or "").strip()[:500]
        if not text:
            return "What would you like me to tell your family?"
        with session_scope() as s:
            elder = primary_elder(s)
            _, spoken = concern_service.report_concern(
                s, get_dispatcher(), elder, text, severity, utcnow())
            return spoken
