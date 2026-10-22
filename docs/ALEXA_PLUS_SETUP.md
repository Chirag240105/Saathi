# Connecting Alexa+

## Fill from the hackathon Resources page
_TODO: copy the official steps for registering a self-hosted MCP server with Alexa+ (endpoint registration, auth, preview access). Record any confusion in `FRICTION_LOG.md`._

## Generic steps for any MCP client
1. Run Saathi (`make dev`) and confirm `GET /health`.
2. Expose it: `cloudflared tunnel --url http://localhost:8000` (or `ngrok http 8000`).
3. Set a strong `SHARED_SECRET` in `.env` and restart.
4. Point the client at `MCP_PUBLIC_URL`, for example `https://<tunnel-host>/mcp` (Streamable HTTP, MCP spec 2025-11-25).
5. Send header `X-Saathi-Key: <SHARED_SECRET>`. Optionally send `X-Saathi-Source: alexa` (the default).
6. Verify with MCP Inspector: it must list `get_today_schedule`, `log_medication_taken`, `daily_checkin`, `report_concern`, `add_appointment`.

If real Alexa+ access is unavailable, the web simulator at `/elder` exercises the same server and shows each tool call live.
