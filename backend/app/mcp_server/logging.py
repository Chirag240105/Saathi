"""Decorator that records every MCP tool call (inputs, result, duration, success, source)."""
import functools
import logging
import time
from collections.abc import Callable
from typing import Any

import anyio.to_thread

from app.core.logging import log_event
from app.core.time import utcnow
from app.db.repositories.tool_calls import ToolCallRepo
from app.db.session import session_scope
from app.services import reply_service as reply

log = logging.getLogger("saathi.mcp")
SOURCES = {"alexa", "simulator", "inspector"}


def source_of(ctx: Any) -> str:
    """Who called? Header X-Saathi-Source, else a guess from the user agent, else 'alexa'."""
    try:
        headers = ctx.request_context.request.headers
        declared = headers.get("x-saathi-source", "").lower()
        if declared in SOURCES:
            return declared
        if "inspector" in headers.get("user-agent", "").lower():
            return "inspector"
    except Exception:
        pass
    return "alexa"


def tracked(tool_name: str) -> Callable[[Callable[..., str]], Callable[..., Any]]:
    """Wrap a sync tool body: run it off the event loop, time it, store a tool_calls row."""

    def deco(fn: Callable[..., str]) -> Callable[..., Any]:
        @functools.wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> str:
            source = source_of(kwargs.get("ctx"))
            inputs = {k: v for k, v in kwargs.items() if k != "ctx"}
            start = time.perf_counter()
            ok = True
            try:
                result = await anyio.to_thread.run_sync(lambda: fn(*args, **inputs))
            except Exception:
                log.exception("tool failed: %s", tool_name)
                ok, result = False, reply.generic_error()  # never leak internals
            ms = int((time.perf_counter() - start) * 1000)
            try:
                with session_scope() as s:
                    ToolCallRepo(s).add(
                        tool_name=tool_name, inputs=inputs, result=result, duration_ms=ms,
                        success=ok, source=source, created_at=utcnow(),
                    )
            except Exception:
                log.exception("could not store tool call")
            log_event(log, "tool_call", tool=tool_name, ms=ms, ok=ok, source=source)
            return result

        return wrapper

    return deco
