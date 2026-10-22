# Safety and privacy

## Safety
- Saathi **logs and reminds only**. It does not diagnose, suggest doses or treatments, or interpret symptoms.
- High-severity replies always include "Call emergency services if it gets worse." The UI shows "In an emergency, call your local emergency number."
- Spoken replies never contain stack traces, IDs or internals; failures become a plain apology and are logged.
- If family cannot be reached, the reply says so honestly and the event is still saved.
- Symptom wording ("dizzy", "chest pain", "fell") is always treated as high severity by the offline rules.
- Limits: speech recognition can mishear, a missed alert is possible if Telegram is down or no chat ID is set, and Saathi is not a medical device or alarm system.

## Privacy
- Health-related data is sensitive. It lives in a local SQLite file (`saathi.db`, git-ignored). No third-party analytics.
- Fields are minimal: names, medicine schedule, mood, short notes, appointments.
- Telegram messages contain the elder's name, time and own words and go only to configured contacts.
- If an LLM provider is enabled, the **spoken sentence and tool descriptions** are sent to it (not the database). Keep `LLM_PROVIDER=rules` to stay fully local.
- Delete everything: `backend/.venv/bin/python scripts/reset_demo.py` (reseeds fictional data) or delete `saathi.db`.
- Consent: the elder should know and agree that family is alerted, and who is on the list.
- Secrets: only in `.env` (git-ignored). `VITE_SHARED_SECRET` is embedded in the browser bundle, so treat it as demo-grade; do not reuse a real secret. Real deployments need per-user authentication.
- All demo data is fictional.
