# Architecture

## Components
```mermaid
flowchart TB
  subgraph Frontend [React app :5173]
    Elder[ElderPage + tool-call log]
    Family[FamilyDashboardPage]
    Hist[History / Care setup]
  end
  subgraph Backend [FastAPI :8000]
    REST[/api routes/]
    MCP[/mcp FastMCP, stateless Streamable HTTP/]
    Auth[SharedSecretASGI]
    SIM[simulator agent + mcp_client]
    SVC[services]
    REPO[repositories]
    SCH[APScheduler]
    NOTI[notifications]
  end
  DB[(SQLite)]
  TG[Telegram Bot API]
  Elder --> REST
  Family --> REST
  Hist --> REST
  REST --> SIM --> Auth --> MCP
  Alexa[Alexa+ / Inspector] --> Auth
  MCP --> SVC
  REST --> SVC
  SCH --> SVC
  SVC --> REPO --> DB
  SVC --> NOTI --> TG
```

## Request lifecycle: "I feel dizzy"
```mermaid
sequenceDiagram
  participant E as Elder (mic)
  participant UI as ElderPage
  participant A as /api/simulator/chat
  participant M as /mcp (report_concern)
  participant S as concern_service
  participant D as SQLite
  participant T as Telegram
  E->>UI: speech to text (Web Speech API)
  UI->>A: POST {text}
  A->>A: choose tool (LLM or rules)
  A->>M: tools/call over Streamable HTTP
  M->>S: raise_event
  S->>D: save event, commit
  S->>T: notify every contact (2 retries)
  S->>D: store notified/delivery
  M->>D: record tool_calls row (name, inputs, result, ms, source)
  M-->>A: calm speakable reply
  A-->>UI: {reply, tool_calls, used_llm}
  UI->>E: speechSynthesis reply
  Note over UI: dashboards poll /api/status (10 s) and /api/tool-calls (2 s)
```

## Data model
```mermaid
erDiagram
  elders ||--o{ medications : has
  elders ||--o{ checkins : has
  elders ||--o{ appointments : has
  elders ||--o{ contacts : has
  elders ||--o{ events : has
  medications ||--o{ dose_log : "unique(medication_id, scheduled_for)"
  elders { int id string name int age string language string timezone }
  medications { int id string name json aliases string dose json times }
  dose_log { int id datetime scheduled_for datetime taken_at string status }
  checkins { int id string mood string note datetime created_at }
  appointments { int id string title datetime starts_at }
  contacts { int id string name string telegram_chat_id string role }
  events { int id string type string severity string message bool notified string delivery }
  tool_calls { int id string tool_name json inputs string result int duration_ms bool success string source }
```
All datetimes are stored as UTC (a `UTCDateTime` column type rejects naive values) and shown in `TIMEZONE` (default Asia/Kolkata).

## Layer rules
1. `services/` holds all business logic. It never imports FastAPI or MCP.
2. `db/repositories/` owns all SQL; services call repositories.
3. REST routes and MCP tools are thin adapters over services.
4. Config is read only in `core/config.py`.
5. Reply wording lives only in `services/reply_service.py`.
6. Notifiers never raise: delivery failures are reported, the event is already saved.

## MCP SDK version and notes
- Pinned `mcp>=1.30,<2` (installed 1.30.0). `mcp.types.LATEST_PROTOCOL_VERSION` is `2025-11-25`; a raw `initialize` against `/mcp` negotiates `2025-11-25`. The PyPI 2.x line was not used (different API surface).
- Server: `FastMCP(stateless_http=True, json_response=True)`, endpoint `/mcp`, mounted at `/` in FastAPI. A mounted app's lifespan does not run, so `main.py` runs `mcp.session_manager.run()` in the FastAPI lifespan. A session manager can run only once per instance, so `build_mcp()` creates a fresh server per app.
- DNS-rebinding host checks are disabled (tunnel hostnames vary); access control is the `X-Saathi-Key` header enforced by a pure-ASGI guard in `mcp_server/auth.py` (safe for streaming).
- Tools are sync bodies wrapped by `@tracked`, which runs them off the event loop, converts exceptions to a friendly reply, and writes the `tool_calls` row. Source comes from the `X-Saathi-Source` header (`alexa` by default).
- The client uses `streamable_http_client` with a header-carrying `httpx.AsyncClient`.
