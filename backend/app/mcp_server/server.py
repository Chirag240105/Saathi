"""FastMCP server (Streamable HTTP, MCP spec 2025-11-25). One tool per file in tools/."""
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from app.mcp_server.tools import (
    add_appointment,
    daily_checkin,
    get_today_schedule,
    log_medication_taken,
    report_concern,
)

TOOL_NAMES = [
    "get_today_schedule", "log_medication_taken", "daily_checkin", "report_concern",
    "add_appointment",
]


def build_mcp() -> FastMCP:
    """Create a fresh server (a session manager can only run once, so tests build several)."""
    mcp = FastMCP(
        "saathi",
        instructions=("Saathi is a caring elder companion. Replies are short and warm. "
                      "It logs and reminds only, never gives medical advice."),
        stateless_http=True,
        json_response=True,
        streamable_http_path="/mcp",
        # Host checks are disabled because the endpoint is reached through tunnels; the
        # X-Saathi-Key shared secret (see auth.py) is the access control.
        transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
    )
    for module in (get_today_schedule, log_medication_taken, daily_checkin, report_concern,
                   add_appointment):
        module.register(mcp)
    return mcp


if __name__ == "__main__":  # `python -m app.mcp_server.server` serves only the MCP endpoint
    build_mcp().run(transport="streamable-http")
