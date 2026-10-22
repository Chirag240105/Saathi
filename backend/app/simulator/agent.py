"""Speech text -> tool choice (LLM if configured, else rules) -> real MCP call -> reply."""
import logging
from dataclasses import dataclass, field

from app.core.config import get_settings
from app.core.logging import log_event
from app.core.time import now_local
from app.services import reply_service as reply
from app.simulator.llm import rules
from app.simulator.llm.base import Provider
from app.simulator.llm.gemini import GeminiProvider
from app.simulator.llm.groq import GroqProvider
from app.simulator.mcp_client import CallRecord, McpClient

log = logging.getLogger("saathi.simulator")
NOT_UNDERSTOOD = ("I did not quite catch that. You can ask what you have today, tell me you took "
                  "a medicine, say how you feel, or ask for help.")


@dataclass
class ChatResult:
    reply: str
    tool_calls: list[CallRecord] = field(default_factory=list)
    used_llm: bool = False


def get_provider() -> Provider | None:
    s = get_settings()
    if s.llm_provider == "gemini" and s.gemini_api_key:
        return GeminiProvider(s.gemini_api_key, s.gemini_model)
    if s.llm_provider == "groq" and s.groq_api_key:
        return GroqProvider(s.groq_api_key, s.groq_model)
    return None


async def chat(text: str, client: McpClient | None = None,
               provider: Provider | None = None) -> ChatResult:
    client = client or McpClient(source="simulator")
    provider = provider if provider is not None else get_provider()
    now = now_local()
    plan = None
    used_llm = False
    if provider is not None:
        try:
            plan = await provider.plan(text, await client.list_tools(), now)
            used_llm = plan is not None
        except Exception as exc:  # rate limit, network, bad JSON: fall back to rules
            log_event(log, "llm_fallback", provider=provider.name, error=type(exc).__name__)
    if plan is None:
        plan = rules.plan(text, now)
    if plan is None:
        return ChatResult(NOT_UNDERSTOOD)
    try:
        rec = await client.call_tool(plan.tool, plan.args)
    except Exception as exc:
        log_event(log, "mcp_call_failed", tool=plan.tool, error=type(exc).__name__)
        return ChatResult(reply.generic_error())
    return ChatResult(rec.result if rec.success else reply.generic_error(), [rec], used_llm)
