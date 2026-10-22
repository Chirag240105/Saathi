# Friction Log

One entry per problem. Fields: task attempted, steps taken, expected vs actual, severity, workaround, suggestion.

## Entry 1: MCP Python SDK version choice
- **Task attempted:** Pick an `mcp` SDK release that supports Streamable HTTP and spec 2025-11-25.
- **Steps taken:** Listed versions on PyPI; a 2.x line now exists alongside 1.x.
- **Expected vs actual:** Expected one obvious "latest". Found two major lines with possibly different APIs.
- **Severity:** Low
- **Workaround:** Pinned the latest 1.x (`<2`) for the stable `FastMCP` API; verify spec support in Phase 2.
- **Suggestion:** State the supported spec revision per release in the README.

<!-- Copy the block above for each new entry. -->
