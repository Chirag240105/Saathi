# Product Feedback

Fill one block per tool, API or SDK used (MCP Python SDK, MCP Inspector, Alexa+, Telegram Bot API, Gemini/Groq, ...).

## <Tool name>
- **What I used it for:**
- **What worked well:**
- **What needs work:**
- **Onboarding experience** (time to first working call, docs quality):
- **Would I build with it again** (yes/no and why):
- **AWS services used, if any:**

## MCP Python SDK (FastMCP, Streamable HTTP)
- **What I used it for:** Exposing five elder-care tools at `/mcp` and a client that calls them from the simulator and tests.
- **What worked well:** Decorator-based tools with docstrings as descriptions, typed `Literal` inputs producing clean JSON schemas, `stateless_http` + `json_response` making plain HTTP calls easy, and the official Inspector CLI listing the tools immediately.
- **What needs work:** FastAPI mounting (lifespan, run-once session manager), reading request headers in tools, and host-check settings for tunnels are easy to trip over (see FRICTION_LOG.md). A new 2.x line exists beside 1.x without an obvious migration guide.
- **Onboarding experience:** About 30 minutes to a first working tool call; most time went to the mounting caveats.
- **Would I build with it again:** Yes. Tools-as-functions is a natural fit for voice assistants.
- **AWS services used:** None.

## MCP Inspector
- **What I used it for:** Verifying the Streamable HTTP endpoint and header auth.
- **What worked well:** `--cli` with `--transport http --method tools/list --header` is scriptable.
- **What needs work:** Flag names are only discoverable from `--help`.
- **Would I build with it again:** Yes.

## Alexa+
- **What I used it for:** TODO (fill after trying the real connection).
