from dataclasses import dataclass
from typing import Protocol


@dataclass
class Delivery:
    contact: str
    ok: bool
    channel: str
    detail: str = ""


class Notifier(Protocol):
    channel: str

    def send(self, contact_name: str, chat_id: str | None, text: str) -> Delivery:
        """Deliver one message. Must never raise; report failure in the Delivery."""
        ...
