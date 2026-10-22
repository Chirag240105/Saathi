"""Chooses a notifier and fans a message out to contacts."""
from collections.abc import Sequence
from typing import Protocol

from app.core.config import get_settings
from app.notifications.base import Delivery, Notifier
from app.notifications.console import ConsoleNotifier
from app.notifications.telegram import TelegramNotifier


class _HasContact(Protocol):
    name: str
    telegram_chat_id: str | None


class Dispatcher:
    def __init__(self, notifier: Notifier) -> None:
        self.notifier = notifier

    def broadcast(self, contacts: Sequence[_HasContact], text: str) -> list[Delivery]:
        out: list[Delivery] = []
        for c in contacts:
            try:
                out.append(self.notifier.send(c.name, c.telegram_chat_id, text))
            except Exception as exc:  # a notifier must not break a tool call
                out.append(Delivery(c.name, False, self.notifier.channel, type(exc).__name__))
        if not contacts and self.notifier.channel == "console":
            out.append(self.notifier.send("family", None, text))
        return out

    @staticmethod
    def summarize(deliveries: list[Delivery]) -> str:
        if not deliveries:
            return "no contacts"
        ok = sum(d.ok for d in deliveries)
        return f"{deliveries[0].channel}: {ok}/{len(deliveries)} delivered"


_dispatcher: Dispatcher | None = None


def get_dispatcher() -> Dispatcher:
    global _dispatcher
    if _dispatcher is None:
        token = get_settings().telegram_bot_token
        _dispatcher = Dispatcher(TelegramNotifier(token) if token else ConsoleNotifier())
    return _dispatcher


def set_dispatcher(d: Dispatcher | None) -> None:
    """Override (tests) or reset (None)."""
    global _dispatcher
    _dispatcher = d
