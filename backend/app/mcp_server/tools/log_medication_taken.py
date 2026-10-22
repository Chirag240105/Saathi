from mcp.server.fastmcp import Context, FastMCP

from app.core.time import utcnow
from app.db.session import session_scope
from app.mcp_server.logging import tracked
from app.services import medication_service
from app.services import reply_service as reply
from app.services.elder_service import primary_elder


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    @tracked("log_medication_taken")
    def log_medication_taken(name: str, ctx: Context | None = None) -> str:
        """Record that the elder just took a medicine. Use when they say "I took my BP tablet" or
        "I had my sugar medicine". Pass the medicine as they said it ("BP tablet", "sugar
        medicine"); it is matched loosely. If they only say "my medicine", pass "medicine"."""
        now = utcnow()
        with session_scope() as s:
            elder = primary_elder(s)
            r = medication_service.log_taken(s, elder.id, name, now)
            if r.status == "unknown":
                return reply.med_unknown(r.names or [])
            assert r.medication is not None or r.status == "all_done"
            label = r.medication.name if r.medication else "medicine"
            if r.status == "duplicate":
                return reply.med_duplicate(label)
            if r.status == "all_done":
                return reply.med_all_done(label)
            nxt = r.next_slot
            nxt_text = (f"your {nxt.medication.name} {reply.spoken_time(nxt.at)}".replace(
                f"{nxt.medication.name} ", f"{nxt.medication.name} at ", 1) if nxt else None)
            return reply.med_logged(label, nxt_text)
