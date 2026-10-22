# Assumptions

1. `mcp` SDK pinned to the latest 1.x (`>=1.30,<2`); 2.x has a different surface and is not needed for this MVP. Revisit in Phase 2.
2. Python 3.11+ is required; developed on 3.12.
3. Auth: `SHARED_SECRET` empty disables the `X-Saathi-Key` check (local dev only).
4. `VITE_SHARED_SECRET` ends up in the browser bundle, so it is demo-grade protection only.
5. Demo timezone is Asia/Kolkata; all stored times are timezone-aware UTC, converted for display.
6. Demo data is fictional.
7. Telegram is the only family channel; contacts without a chat ID are reported as "not delivered" when a token is set.
8. "Send a gentle check-in message" nudges the family circle (the elder has no Telegram). It is not stored as an event.
9. Generic phrases ("my medicine") log the dose nearest to the current time.
10. Missed-dose job only considers doses overdue for 12 hours or less. Seeding marks today's doses older than 1 hour as taken so startup never fires surprise alerts.
11. The demo supports one elder (the schema allows more).
12. CareSetup supports add and delete; backend PUT routes exist for edit but the UI keeps add/delete only (cut list).
13. Dark theme and CSV export were not built (cut list). No SSE; polling is used (10 s status, 2 s tool calls).
14. Gemini/Groq model defaults (`gemini-2.0-flash`, `llama-3.3-70b-versatile`) are configurable and were only tested against mocked responses, not live keys.
15. `X-Saathi-Source` defaults to `alexa` when absent.
