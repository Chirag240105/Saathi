import os

os.environ.update(APP_ENV="test", DATABASE_URL="sqlite://", SHARED_SECRET="", TELEGRAM_BOT_TOKEN="")

from collections.abc import Iterator  # noqa: E402

import pytest  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.core.config import get_settings  # noqa: E402
from app.core.time import utcnow  # noqa: E402
from app.db.seed import seed_if_empty  # noqa: E402
from app.db.session import init_engine, session_scope  # noqa: E402
from app.notifications.base import Delivery  # noqa: E402
from app.notifications.dispatcher import Dispatcher, set_dispatcher  # noqa: E402


class FakeNotifier:
    channel = "fake"

    def __init__(self, ok: bool = True) -> None:
        self.ok, self.sent = ok, []

    def send(self, contact_name: str, chat_id: str | None, text: str) -> Delivery:
        self.sent.append((contact_name, text))
        return Delivery(contact_name, self.ok, self.channel)


@pytest.fixture(autouse=True)
def _settings() -> Iterator[None]:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def notifier() -> Iterator[FakeNotifier]:
    n = FakeNotifier()
    set_dispatcher(Dispatcher(n))
    yield n
    set_dispatcher(None)


@pytest.fixture
def db(notifier: FakeNotifier) -> Iterator[Session]:
    """Fresh in-memory DB, seeded, fixed clock-independent."""
    init_engine("sqlite://")
    with session_scope() as s:
        seed_if_empty(s, utcnow())
        yield s


@pytest.fixture
def dispatcher(notifier: FakeNotifier) -> Dispatcher:
    return Dispatcher(notifier)
