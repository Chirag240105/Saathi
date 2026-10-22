"""Shared-secret check (header X-Saathi-Key)."""
import hmac

from fastapi import Depends, Header

from app.core.config import Settings, get_settings


class AuthError(Exception):
    """Raised when the shared secret is missing or wrong."""


def is_authorized(provided: str | None, settings: Settings) -> bool:
    if not settings.auth_enabled:
        return True
    return provided is not None and hmac.compare_digest(provided, settings.shared_secret)


def require_key(
    x_saathi_key: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> None:
    if not is_authorized(x_saathi_key, settings):
        raise AuthError("Missing or invalid X-Saathi-Key header.")
