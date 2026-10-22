"""Gemini free tier, function calling over REST."""
from datetime import datetime

import httpx

from app.simulator.llm.base import Plan, clean_schema, system_prompt
from app.simulator.mcp_client import ToolInfo


class GeminiProvider:
    name = "gemini"

    def __init__(self, api_key: str, model: str, client: httpx.AsyncClient | None = None) -> None:
        self.key, self.model, self._client = api_key, model, client

    async def plan(self, text: str, tools: list[ToolInfo], now: datetime) -> Plan | None:
        body = {
            "systemInstruction": {"parts": [{"text": system_prompt(now)}]},
            "contents": [{"role": "user", "parts": [{"text": text}]}],
            "tools": [{"functionDeclarations": [
                {"name": t.name, "description": t.description, "parameters": clean_schema(t.schema)}
                for t in tools]}],
            "toolConfig": {"functionCallingConfig": {"mode": "ANY"}},
        }
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        client = self._client or httpx.AsyncClient(timeout=10.0)
        try:
            r = await client.post(url, json=body, headers={"x-goog-api-key": self.key})
            r.raise_for_status()
        finally:
            if self._client is None:
                await client.aclose()
        for part in r.json()["candidates"][0]["content"]["parts"]:
            if "functionCall" in part:
                fc = part["functionCall"]
                return Plan(fc["name"], dict(fc.get("args", {})))
        return None
