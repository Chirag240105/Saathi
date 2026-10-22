from app.core.config import Settings
from app.core.security import is_authorized


def test_auth_disabled_when_secret_empty() -> None:
    assert is_authorized(None, Settings(shared_secret=""))


def test_auth_rejects_missing_and_wrong_header() -> None:
    s = Settings(shared_secret="abc")
    assert not is_authorized(None, s)
    assert not is_authorized("nope", s)
    assert is_authorized("abc", s)
