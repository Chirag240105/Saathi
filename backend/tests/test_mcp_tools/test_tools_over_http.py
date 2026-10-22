"""MCP tools exercised through the real MCP client over Streamable HTTP."""
import anyio
import httpx
import pytest

from app.db.repositories.events import EventRepo
from app.db.repositories.tool_calls import ToolCallRepo
from app.db.session import session_scope
from app.simulator.mcp_client import McpClient, McpServerConfig, load_config

EXPECTED = {"get_today_schedule", "log_medication_taken", "daily_checkin", "report_concern",
            "add_appointment"}


def client_for(base: str, source: str = "simulator") -> McpClient:
    cfg = load_config().model_copy(update={"url": f"{base}/mcp"})
    return McpClient(cfg, source=source)


def run(coro_fn):  # type: ignore[no-untyped-def]
    return anyio.run(coro_fn)


def test_lists_exactly_the_five_tools(live_server: str) -> None:
    tools = run(client_for(live_server).list_tools)
    assert {t.name for t in tools} == EXPECTED and len(tools) == 5
    by = {t.name: t for t in tools}
    assert by["report_concern"].description  # docstring doubles as tool description
    assert set(by["report_concern"].schema["properties"]) == {"message", "severity"}  # ctx hidden


def test_schedule_returns_short_speakable_text(live_server: str) -> None:
    rec = run(lambda: client_for(live_server).call_tool("get_today_schedule", {}))
    assert rec.success and rec.result and len(rec.result.split()) < 40


def test_log_medication_and_duplicate(live_server: str) -> None:
    c = client_for(live_server)

    async def go():  # type: ignore[no-untyped-def]
        return (await c.call_tool("log_medication_taken", {"name": "vit d"}),
                await c.call_tool("log_medication_taken", {"name": "vitamin d"}),
                await c.call_tool("log_medication_taken", {"name": "aspirin"}))

    first, second, unknown = run(go)
    assert first.success
    assert "already noted" in second.result or "all your" in second.result  # pre-taken or duplicate
    assert "could not find" in unknown.result and "BP tablet" in unknown.result


def test_daily_checkin_unwell_alerts_family(live_server: str, notifier) -> None:  # type: ignore[no-untyped-def]
    ok = run(lambda: client_for(live_server).call_tool("daily_checkin", {"mood": "good"}))
    assert ok.success and notifier.sent == []
    bad = run(lambda: client_for(live_server).call_tool(
        "daily_checkin", {"mood": "unwell", "note": "very tired"}))
    assert "emergency services" in bad.result and len(notifier.sent) == 2


def test_report_concern_flow_and_tool_call_log(live_server: str, notifier) -> None:  # type: ignore[no-untyped-def]
    rec = run(lambda: client_for(live_server, "inspector").call_tool(
        "report_concern", {"message": "I feel dizzy"}))
    assert "emergency services" in rec.result
    assert {n for n, _ in notifier.sent} == {"Rohan", "Anita"}
    with session_scope() as s:
        assert EventRepo(s).recent(1, 1)[0].type == "concern"
        tc = ToolCallRepo(s).list(1)[0]
    assert tc.tool_name == "report_concern" and tc.source == "inspector" and tc.success
    assert tc.inputs == {"message": "I feel dizzy", "severity": "high"} or tc.inputs["message"]
    assert tc.duration_ms >= 0


def test_add_appointment_and_friendly_errors(live_server: str) -> None:
    c = client_for(live_server)

    async def go():  # type: ignore[no-untyped-def]
        return (await c.call_tool("add_appointment",
                                  {"title": "Dentist", "starts_at": "2099-03-04T11:00"}),
                await c.call_tool("add_appointment", {"title": "Dentist", "starts_at": "soon"}))

    good, bad = run(go)
    assert good.result.startswith("Added: Dentist on 4 March at eleven in the morning")
    assert "did not catch the date" in bad.result


def test_tool_not_in_allowlist_is_refused(live_server: str) -> None:
    cfg = McpServerConfig(url=f"{live_server}/mcp", tool_allowlist=["get_today_schedule"])
    with pytest.raises(PermissionError):
        run(lambda: McpClient(cfg).call_tool("report_concern", {"message": "x"}))


def test_auth_rejects_missing_header_with_401(live_server: str, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    from app.core.config import get_settings

    monkeypatch.setenv("SHARED_SECRET", "s3cret")
    get_settings.cache_clear()
    body = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    hdr = {"Accept": "application/json, text/event-stream"}
    r = httpx.post(f"{live_server}/mcp", json=body, headers=hdr)
    assert r.status_code == 401 and r.json()["error"]["code"] == "unauthorized"
    r = httpx.post(f"{live_server}/mcp", json=body, headers={**hdr, "X-Saathi-Key": "wrong"})
    assert r.status_code == 401
    tools = run(client_for(live_server).list_tools)  # client sends the right key
    assert len(tools) == 5
    r = httpx.post(f"{live_server}/api/medications", headers={}, json={})
    assert r.status_code == 401
