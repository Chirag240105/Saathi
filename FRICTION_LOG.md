# Friction Log

One entry per problem. Fields: task attempted, steps taken, expected vs actual, severity, workaround, suggestion.

## Entry 1: MCP Python SDK version choice
- **Task attempted:** Pick an `mcp` SDK release that supports Streamable HTTP and spec 2025-11-25.
- **Steps taken:** Listed versions on PyPI; a 2.x line now exists alongside 1.x.
- **Expected vs actual:** Expected one obvious "latest". Found two major lines with possibly different APIs.
- **Severity:** Low
- **Workaround:** Pinned the latest 1.x (`<2`) for the stable `FastMCP` API; verify spec support in Phase 2.
- **Suggestion:** State the supported spec revision per release in the README.



## Entry 2: Mounting FastMCP inside FastAPI
- **Task attempted:** Serve `/mcp` from the same process as the REST API.
- **Steps taken:** `app.mount("/", mcp.streamable_http_app())`; first requests failed until the session manager was started.
- **Expected vs actual:** Expected the mounted app's lifespan to run. Starlette does not run lifespans of mounted apps, so `mcp.session_manager.run()` must be entered in the parent lifespan.
- **Severity:** Medium
- **Workaround:** Run the session manager in the FastAPI lifespan. A session manager can only run once per instance, so tests build a fresh server each time.
- **Suggestion:** Document the FastAPI-mount recipe (lifespan and single-run caveat) next to the Streamable HTTP docs.

## Entry 3: Host header checks behind tunnels and test clients
- **Task attempted:** Reach `/mcp` through a tunnel hostname and from in-process test clients.
- **Expected vs actual:** Expected it to just work; DNS-rebinding protection is on by default for localhost servers and rejects unknown Host headers.
- **Severity:** Low
- **Workaround:** Disabled it via `TransportSecuritySettings` and rely on the `X-Saathi-Key` shared secret.
- **Suggestion:** Document an allowed-hosts example for tunnels.

## Entry 4: Reading request headers inside a tool
- **Task attempted:** Record whether a call came from Alexa, the simulator or Inspector.
- **Expected vs actual:** A ContextVar set in ASGI middleware does not reach the tool in stateless mode (the handler runs in a different task). Using `ctx.request_context.request.headers` works.
- **Severity:** Low
- **Workaround:** Add `ctx: Context | None = None` to each tool (hidden from the input schema) and read headers from it.
- **Suggestion:** Document how to access per-request headers from tools.

## Entry 5: Alexa+ connection details
- **Task attempted:** Find out how Alexa+ registers a self-hosted MCP server.
- **Expected vs actual:** Not yet confirmed from the Resources page. TODO: fill before submitting.
- **Severity:** Unknown
- **Workaround:** Built the web simulator that calls the identical `/mcp` endpoint.
- **Suggestion:** A step-by-step "connect your MCP server to Alexa+" page.
