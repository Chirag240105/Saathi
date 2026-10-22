import socket
import threading
import time
from collections.abc import Iterator

import pytest
import uvicorn

from app.db.seed import seed_if_empty
from app.db.session import session_scope
from app.main import create_app


@pytest.fixture
def live_server(notifier) -> Iterator[str]:  # type: ignore[no-untyped-def]
    """Real uvicorn server on a free port, in-memory DB, so tests hit /mcp over real HTTP."""
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(create_app(), port=port, log_level="warning"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    for _ in range(100):
        if server.started:
            break
        time.sleep(0.05)
    with session_scope() as s:
        seed_if_empty(s)
    yield f"http://127.0.0.1:{port}"
    server.should_exit = True
    thread.join(timeout=5)
