"""Telegram Bot API notifier: 2 retries with exponential backoff, never raises."""
import logging
import time
from collections.abc import Callable

import httpx

from app.core.logging import log_event
from app.notifications.base import Delivery

log = logging.getLogger("saathi.notify")


class TelegramNotifier:
    channel = "telegram"

    def __init__(
        self,
        token: str,
        client: httpx.Client | None = None,
        retries: int = 2,
        backoff: float = 0.5,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self._url = f"https://api.telegram.org/bot{token}/sendMessage"
        self._client = client or httpx.Client(timeout=5.0)
        self._retries, self._backoff, self._sleep = retries, backoff, sleep

    def send(self, contact_name: str, chat_id: str | None, text: str) -> Delivery:
        if not chat_id:
            return Delivery(contact_name, False, self.channel, "no telegram chat id")
        last = ""
        for attempt in range(self._retries + 1):
            try:
                r = self._client.post(self._url, json={"chat_id": chat_id, "text": text})
                if r.status_code == 200:
                    log_event(log, "notification", channel="telegram", to=contact_name, ok=True)
                    return Delivery(contact_name, True, self.channel)
                last = f"http {r.status_code}"
            except httpx.HTTPError as exc:  # network trouble
                last = type(exc).__name__
            log_event(log, "notification_retry", to=contact_name, attempt=attempt + 1, error=last)
            if attempt < self._retries:
                self._sleep(self._backoff * (2**attempt))
        return Delivery(contact_name, False, self.channel, last)
