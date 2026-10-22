import httpx

from app.notifications.telegram import TelegramNotifier


def _notifier(handler, sleeps):
    client = httpx.Client(transport=httpx.MockTransport(handler))
    return TelegramNotifier("T", client=client, sleep=sleeps.append)


def test_success_first_try() -> None:
    calls = []
    n = _notifier(lambda r: (calls.append(r), httpx.Response(200, json={"ok": True}))[1], [])
    assert n.send("Rohan", "123", "hi").ok and len(calls) == 1


def test_retries_twice_with_backoff_then_gives_up_without_raising() -> None:
    sleeps: list[float] = []
    n = _notifier(lambda r: httpx.Response(500), sleeps)
    d = n.send("Rohan", "123", "hi")
    assert not d.ok and sleeps == [0.5, 1.0]


def test_recovers_after_failures() -> None:
    state = {"n": 0}

    def handler(_: httpx.Request) -> httpx.Response:
        state["n"] += 1
        return httpx.Response(200) if state["n"] == 3 else httpx.Response(502)

    assert _notifier(handler, []).send("Rohan", "123", "hi").ok


def test_missing_chat_id_is_reported_not_raised() -> None:
    assert not _notifier(lambda r: httpx.Response(200), []).send("Rohan", None, "hi").ok
