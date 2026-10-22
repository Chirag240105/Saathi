"""Provider interface + shared helpers."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Protocol

from app.simulator.mcp_client import ToolInfo


@dataclass
class Plan:
    tool: str
    args: dict[str, Any] = field(default_factory=dict)


class Provider(Protocol):
    name: str

    async def plan(self, text: str, tools: list[ToolInfo], now: datetime) -> Plan | None: ...


def system_prompt(now: datetime) -> str:
    return (
        "You are the voice brain of Saathi, a companion for an elderly person. Choose exactly one "
        "tool for what they said. Never give medical advice. Symptoms, falls or asking for help "
        "-> report_concern (severity high). Saying how they feel generally -> daily_checkin. "
        f"Current local time: {now:%A %Y-%m-%d %H:%M}. For appointments pass starts_at as local "
        "ISO date-time like 2026-10-30T11:00; assume 11 means 11 AM."
    )


def clean_schema(node: Any) -> Any:
    """Reduce an MCP JSON schema to the common subset LLM function calling accepts."""
    if isinstance(node, list):
        return [clean_schema(n) for n in node]
    if not isinstance(node, dict):
        return node
    if "anyOf" in node:
        options = [o for o in node["anyOf"] if o.get("type") != "null"]
        if len(options) == 1:
            merged = {**{k: v for k, v in node.items() if k != "anyOf"}, **options[0]}
            return clean_schema(merged)
    return {k: clean_schema(v) for k, v in node.items() if k not in ("title", "default", "$defs")}
