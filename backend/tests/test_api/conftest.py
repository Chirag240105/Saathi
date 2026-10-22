import httpx
import pytest

from tests.test_mcp_tools.conftest import live_server  # noqa: F401  (reuse the live server)


@pytest.fixture
def live_server_chat(live_server: str, monkeypatch):  # type: ignore[no-untyped-def]  # noqa: F811
    """httpx client against the live server, with the simulator pointed at it."""
    from app.core.config import get_settings

    monkeypatch.setenv("MCP_LOCAL_URL", f"{live_server}/mcp")
    get_settings.cache_clear()
    with httpx.Client(base_url=live_server, timeout=20) as c:
        yield c
