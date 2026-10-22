# API reference

Errors use `{ "error": { "code", "message" } }`. Write routes (POST/PUT/DELETE, `/api/simulator/chat`, `/api/admin/*`, `/api/messages/*`) require header `X-Saathi-Key` when `SHARED_SECRET` is set.

## REST
| Route | Notes |
|---|---|
| `GET /health` | `{"status":"ok"}` |
| `GET /api/status` | elder, `overall` (`all_good`/`attention`/`alert`), today's `doses` (taken/pending/missed), `last_checkin`, `next_appointment`, `recent_events` |
| `GET /api/history?days=7` | per day: `taken`, `missed`, `pending`, `mood`, `mood_score` (1-3). `days` 1-60 |
| `GET /api/events?limit=20&type=` | type: `concern`, `missed_dose`, `unwell` |
| `GET /api/tool-calls?limit=50&after_id=` | newest first; poll every 2 s |
| `GET/POST /api/medications`, `PUT/DELETE /api/medications/{id}` | body `{name, aliases[], dose, times["08:00"]}` |
| `GET/POST /api/appointments`, `DELETE /api/appointments/{id}` | body `{title, starts_at}`; naive time is local; past times rejected |
| `GET/POST /api/contacts`, `PUT/DELETE /api/contacts/{id}` | body `{name, telegram_chat_id (digits), role}` |
| `POST /api/simulator/chat` | `{text}` → `{reply, tool_calls[], used_llm}`; calls the real `/mcp` |
| `POST /api/messages/check-in` | gentle nudge to all contacts → `{sent, total}` |
| `POST /api/admin/reset-demo` | wipe and reseed |

## MCP (`POST /mcp`, Streamable HTTP, headers `X-Saathi-Key`, optional `X-Saathi-Source: alexa|simulator|inspector`)

| Tool | Inputs | Example reply |
|---|---|---|
| `get_today_schedule` | `date?` (YYYY-MM-DD) | "You have your sugar tablet at two in the afternoon and your BP tablet at eight in the evening." |
| `log_medication_taken` | `name` | "Done, well done. I have noted your BP tablet. Next is your sugar tablet at two in the afternoon." |
| `daily_checkin` | `mood` good/okay/unwell, `note?` | "Thank you for telling me. I hope the day gets brighter." |
| `report_concern` | `message`, `severity` low/high (default high) | "I have told Rohan and Anita. Please sit down and rest. Call emergency services if it gets worse." |
| `add_appointment` | `title`, `starts_at` ISO | "Added: Eye checkup on Friday at eleven in the morning." |

Behaviours worth knowing:
- Medicine names are fuzzy matched (rapidfuzz, cutoff 80) against the name and aliases. "medicine"/"my tablets" log the dose nearest to now. Unknown names list the elder's medicines.
- A second log of the same medicine within 30 minutes is refused kindly and no row is added.
- Notifier failures never fail the call: the event is saved first and the reply says the message may be delayed.
- Internal errors become "Sorry, something went wrong on my side." and are logged, never spoken.

```bash
curl -s -X POST http://localhost:8000/mcp \
  -H 'X-Saathi-Key: change-me' -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"report_concern","arguments":{"message":"I feel dizzy"}}}'
```
