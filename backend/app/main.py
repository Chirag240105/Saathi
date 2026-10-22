"""App factory: wires routers, MCP mount, scheduler and error handling."""
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import (
    admin,
    appointments,
    contacts,
    events,
    health,
    history,
    medications,
    simulator,
    status,
    tool_calls,
)
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.core.security import AuthError
from app.db.seed import seed_if_empty
from app.db.session import init_engine, session_scope
from app.mcp_server.auth import SharedSecretASGI
from app.mcp_server.server import build_mcp
from app.scheduler.missed_dose import start_scheduler


def _error(status_code: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"error": {"code": code, "message": message}})


def create_app() -> FastAPI:
    setup_logging()
    settings = get_settings()
    mcp = build_mcp()
    mcp_app = mcp.streamable_http_app()  # must exist before session_manager is used

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        init_engine()
        with session_scope() as s:
            seed_if_empty(s)
        scheduler = start_scheduler() if settings.app_env != "test" else None
        async with mcp.session_manager.run():  # required for Streamable HTTP
            yield
        if scheduler:
            scheduler.shutdown(wait=False)

    app = FastAPI(title="Saathi", version="1.0.0", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware, allow_origins=settings.cors_origin_list, allow_methods=["*"],
        allow_headers=["*"], expose_headers=["mcp-session-id"],
    )

    @app.exception_handler(AuthError)
    async def _auth(_: Request, exc: AuthError) -> JSONResponse:
        return _error(401, "unauthorized", str(exc))

    @app.exception_handler(RequestValidationError)
    async def _invalid(_: Request, exc: RequestValidationError) -> JSONResponse:
        first = exc.errors()[0] if exc.errors() else {}
        where = ".".join(str(p) for p in first.get("loc", [])[1:])
        return _error(422, "validation_error", f"{where}: {first.get('msg', 'invalid input')}".strip(": "))

    @app.exception_handler(LookupError)
    async def _missing(_: Request, exc: LookupError) -> JSONResponse:
        return _error(404, "not_found", str(exc))

    for r in (health, status, history, medications, appointments, contacts, events, tool_calls,
              simulator, admin):
        app.include_router(r.router)
    app.mount("/", SharedSecretASGI(mcp_app))  # serves POST /mcp
    return app


app = create_app()
