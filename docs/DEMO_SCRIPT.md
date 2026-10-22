# Demo script (target 2:50, no music, no third-party trademarks)

Prep: `make dev`, set `TELEGRAM_BOT_TOKEN` and a real chat ID, `scripts/reset_demo.py`, open `/elder` and `/family` side by side, `curl localhost:8000/health` to warm up. If it is late in the day, add a medicine due in a few minutes. Record locally first.

| Time | Scene | On screen / say |
|---|---|---|
| 0:00-0:20 | Hook | "My mother lives alone in Ghaziabad and I live far away. Saathi turns Alexa+ into a caring companion: it reminds her, listens to her, and tells me when something is wrong." Show the landing page. |
| 0:20-1:15 | Voice demo | `/elder` with the tool-call log visible. Say "What do I have today?" (`get_today_schedule`), "I took my BP tablet" (`log_medication_taken`), "I feel okay" (`daily_checkin`). Point at the log: tool name, inputs, result, milliseconds, "MCP over Streamable HTTP". Cut to `/family` updating. |
| 1:15-2:00 | Alert | Say "I feel dizzy". Calm spoken reply, `report_concern` in the log, the Telegram message arriving on a phone, the dashboard chip turning to Alert with a toast. |
| 2:00-2:30 | Tech | Terminal: the Inspector CLI command listing exactly 5 tools; flash `server.py`, `mcp_client.py`, `mcp_config.json`; `pytest` green. One line: "Same MCP server serves the simulator today and Alexa+ tomorrow." |
| 2:30-2:50 | Impact + safety | "Free, open source, any family can run it. Saathi only logs and reminds; it never gives medical advice and tells people to call emergency services." |
| 2:50-3:00 | Close | Name, repo URL, thank you. |

Tips: lead with the strongest moment, speak clearly, English only, public video, test the link in a private window.
