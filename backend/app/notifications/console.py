"""Fallback notifier: logs the message and counts it as delivered to the console."""
import logging

from app.core.logging import log_event
from app.notifications.base import Delivery

log = logging.getLogger("saathi.notify")


class ConsoleNotifier:
    channel = "console"

    def send(self, contact_name: str, chat_id: str | None, text: str) -> Delivery:
        log_event(log, "notification", channel="console", to=contact_name, text=text)
        return Delivery(contact_name, True, self.channel, "delivered to console")
