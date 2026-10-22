"""Groq free tier (OpenAI-compatible chat completions with tools)."""
import json
from datetime import datetime

import httpx

from app.simulator.llm.base import Plan, clean_schema, system_prompt
from app.simulator.mcp_client import ToolInfo


class GroqProvider:
    name = "groq"

    def __init__(self, api_key: str, model: str, client: httpx.AsyncClient | None = None) -> None:
        self.key, self.model, self._client = api_key, model, client

    async def plan(self, text: str, tools: list[ToolInfo], now: datetime) -> Plan | None:
        body = {
            "model": self.model, "tool_choice": "required", "temperature": 0,
            "messages": [{"role": "system", "content": system_prompt(now)},
                         {"role": "user", "content": text}],
            "tools": [{"type": "function", "function": {
                "name": t.name, "description": t.description,
                "parameters": clean_schema(t.schema)}} for t in tools],
        }
        client = self._client or httpx.AsyncClient(timeout=10.0)
        try:
            r = await client.post("https://api.groq.com/openai/v1/chat/completions", json=body,
                                  headers={"Authorization": f"Bearer {self.key}"})
            r.raise_for_status()
        finally:
            if self._client is None:
                await client.aclose()
        calls = r.json()["choices"][0]["message"].get("tool_calls") or []
        if not calls:
            return None
        fn = calls[0]["function"]
        return Plan(fn["name"], json.loads(fn.get("arguments") or "{}"))
