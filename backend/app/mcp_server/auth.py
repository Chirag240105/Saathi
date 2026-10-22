"""Pure-ASGI shared-secret guard for /mcp (safe for streaming responses)."""
import json
from collections.abc import Callable

from starlette.types import ASGIApp, Receive, Scope, Send

from app.core.config import get_settings
from app.core.security import is_authorized


class SharedSecretASGI:
    def __init__(self, app: ASGIApp, prefix: str = "/mcp",
                 settings: Callable[[], object] = get_settings) -> None:
        self.app, self.prefix = app, prefix

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http" and scope["path"].startswith(self.prefix):
            headers = {k.decode().lower(): v.decode() for k, v in scope["headers"]}
            if not is_authorized(headers.get("x-saathi-key"), get_settings()):
                body = json.dumps({"error": {"code": "unauthorized",
                                             "message": "Missing or invalid X-Saathi-Key header."}})
                await send({"type": "http.response.start", "status": 401,
                            "headers": [(b"content-type", b"application/json")]})
                await send({"type": "http.response.body", "body": body.encode()})
                return
        await self.app(scope, receive, send)
