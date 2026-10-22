import json
from datetime import datetime
from zoneinfo import ZoneInfo

import anyio
import httpx
import pytest

from app.simulator.llm import rules
from app.simulator.llm.base import clean_schema
from app.simulator.llm.gemini import GeminiProvider
from app.simulator.llm.groq import GroqProvider
from app.simulator.mcp_client import ToolInfo

NOW = datetime(2026, 10, 22, 9, 0, tzinfo=ZoneInfo("Asia/Kolkata"))  # a Thursday


@pytest.mark.parametrize("text,tool", [
    ("What do I have today?", "get_today_schedule"),
    ("what's next", "get_today_schedule"),
    ("I took my medicine", "log_medication_taken"),
    ("I took my BP tablet", "log_medication_taken"),
    ("I have taken my sugar medicine now", "log_medication_taken"),
    ("I feel okay", "daily_checkin"),
    ("I am feeling good today", "daily_checkin"),
    ("I feel a bit lonely", "daily_checkin"),
    ("I feel unwell", "report_concern"),
    ("I need help", "report_concern"),
    ("I'm feeling dizzy", "report_concern"),
    ("I am not feeling well", "report_concern"),
    ("add eye checkup Friday at 11", "add_appointment"),
])
def test_intents(text: str, tool: str) -> None:
    p = rules.plan(text, NOW)
    assert p is not None and p.tool == tool


def test_arguments_extracted() -> None:
    assert rules.plan("I took my BP tablet", NOW).args == {"name": "bp tablet"}
    assert rules.plan("I took my medicine", NOW).args == {"name": "medicine"}
    assert rules.plan("I feel okay", NOW).args["mood"] == "okay"
    assert rules.plan("I am feeling good today", NOW).args["mood"] == "good"
    assert rules.plan("I feel dizzy", NOW).args["severity"] == "high"


def test_appointment_parsing() -> None:
    p = rules.plan("add eye checkup Friday at 11", NOW)
    assert p.args == {"title": "Eye checkup", "starts_at": "2026-10-23T11:00:00"}
    p = rules.plan("book a doctor appointment tomorrow at 4 pm", NOW)
    assert p.args == {"title": "Doctor", "starts_at": "2026-10-23T16:00:00"}
    assert rules.plan("add dentist", NOW).args["starts_at"] == ""  # tool replies kindly


def test_unknown_text_has_no_plan() -> None:
    assert rules.plan("the weather is nice", NOW) is None


TOOLS = [ToolInfo("report_concern", "Alert family",
                  {"title": "x", "type": "object", "properties": {
                      "message": {"title": "Message", "type": "string"},
                      "note": {"anyOf": [{"type": "string"}, {"type": "null"}], "default": None}}})]


def test_clean_schema_drops_titles_and_nullable() -> None:
    c = clean_schema(TOOLS[0].schema)
    assert "title" not in c and c["properties"]["note"] == {"type": "string"}


def test_gemini_parses_function_call() -> None:
    def handler(req: httpx.Request) -> httpx.Response:
        assert json.loads(req.content)["tools"][0]["functionDeclarations"][0]["name"] == "report_concern"
        return httpx.Response(200, json={"candidates": [{"content": {"parts": [
            {"functionCall": {"name": "report_concern", "args": {"message": "dizzy"}}}]}}]})

    async def go():  # type: ignore[no-untyped-def]
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as c:
            return await GeminiProvider("k", "m", c).plan("I feel dizzy", TOOLS, NOW)

    assert anyio.run(go).args == {"message": "dizzy"}


def test_groq_parses_tool_call_and_errors_raise() -> None:
    ok = {"choices": [{"message": {"tool_calls": [{"function": {
        "name": "report_concern", "arguments": json.dumps({"message": "dizzy"})}}]}}]}

    async def go(status: int):  # type: ignore[no-untyped-def]
        h = lambda r: httpx.Response(status, json=ok)  # noqa: E731
        async with httpx.AsyncClient(transport=httpx.MockTransport(h)) as c:
            return await GroqProvider("k", "m", c).plan("x", TOOLS, NOW)

    assert anyio.run(go, 200).tool == "report_concern"
    with pytest.raises(httpx.HTTPStatusError):
        anyio.run(go, 429)
