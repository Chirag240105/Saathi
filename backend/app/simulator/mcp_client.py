"""Calls the real /mcp endpoint over Streamable HTTP. Loads mcp_config.json."""
import json
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from mcp.types import TextContent
from pydantic import BaseModel

from app.core.config import get_settings

CONFIG_PATH = Path(__file__).with_name("mcp_config.json")


class McpServerConfig(BaseModel):
    url: str
    transport: str = "streamable-http"
    headers: dict[str, str] = {}
    auth_header: str = "X-Saathi-Key"
    tool_allowlist: list[str] = []


def load_config(path: Path = CONFIG_PATH, name: str = "saathi") -> McpServerConfig:
    cfg = McpServerConfig(**json.loads(path.read_text())["servers"][name])
    override = get_settings().mcp_local_url
    return cfg.model_copy(update={"url": override}) if override else cfg


@dataclass
class ToolInfo:
    name: str
    description: str
    schema: dict[str, Any]


@dataclass
class CallRecord:
    name: str
    arguments: dict[str, Any]
    result: str
    duration_ms: int
    success: bool


class McpClient:
    def __init__(self, config: McpServerConfig | None = None, source: str | None = None) -> None:
        self.config = config or load_config()
        self.source = source

    def _headers(self) -> dict[str, str]:
        h = dict(self.config.headers)
        if self.source:
            h["X-Saathi-Source"] = self.source
        secret = get_settings().shared_secret
        if secret:
            h[self.config.auth_header] = secret
        return h

    @asynccontextmanager
    async def _session(self) -> AsyncIterator[ClientSession]:
        async with httpx.AsyncClient(headers=self._headers(), timeout=30.0) as http:
            async with streamable_http_client(self.config.url, http_client=http) as (r, w, _):
                async with ClientSession(r, w) as session:
                    await session.initialize()
                    yield session

    async def list_tools(self) -> list[ToolInfo]:
        async with self._session() as s:
            res = await s.list_tools()
        allow = self.config.tool_allowlist
        return [ToolInfo(t.name, t.description or "", t.inputSchema)
                for t in res.tools if not allow or t.name in allow]

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> CallRecord:
        if self.config.tool_allowlist and name not in self.config.tool_allowlist:
            raise PermissionError(f"Tool not allowed by mcp_config.json: {name}")
        start = time.perf_counter()
        async with self._session() as s:
            res = await s.call_tool(name, arguments)
        text = " ".join(c.text for c in res.content if isinstance(c, TextContent))
        return CallRecord(name, arguments, text, int((time.perf_counter() - start) * 1000),
                          not res.isError)
