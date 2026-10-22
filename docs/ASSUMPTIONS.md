# Assumptions

1. `mcp` SDK pinned to the latest 1.x (`>=1.30,<2`); 2.x has a different surface and is not needed for this MVP. Revisit in Phase 2.
2. Python 3.11+ is required; developed on 3.12.
3. Auth: `SHARED_SECRET` empty disables the `X-Saathi-Key` check (local dev only).
4. `VITE_SHARED_SECRET` ends up in the browser bundle, so it is demo-grade protection only.
5. Demo timezone is Asia/Kolkata; all stored times are timezone-aware UTC, converted for display.
6. Demo data is fictional.
