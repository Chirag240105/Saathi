from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client(notifier) -> Iterator[TestClient]:  # type: ignore[no-untyped-def]
    with TestClient(create_app()) as c:
        yield c


def test_status_shape(client: TestClient) -> None:
    d = client.get("/api/status").json()
    assert d["elder"]["name"] == "Sharda Devi"
    assert d["overall"] in {"all_good", "attention", "alert"}
    assert len(d["doses"]) == 7 and {x["status"] for x in d["doses"]} <= {"taken", "pending", "missed"}
    assert d["next_appointment"]["title"] == "Doctor visit"


def test_history_days(client: TestClient) -> None:
    d = client.get("/api/history?days=7").json()["days"]
    assert len(d) == 7 and d[0]["taken"] + d[0]["missed"] > 0
    assert client.get("/api/history?days=0").status_code == 422


def test_medication_crud_and_validation(client: TestClient) -> None:
    body = {"name": "Iron", "aliases": ["iron tablet"], "dose": "1", "times": ["09:15"]}
    r = client.post("/api/medications", json=body)
    assert r.status_code == 201
    mid = r.json()["id"]
    assert client.put(f"/api/medications/{mid}", json={**body, "times": ["10:00"]}).json()["times"] == ["10:00"]
    bad = client.post("/api/medications", json={**body, "times": ["9am"]})
    assert bad.status_code == 422 and bad.json()["error"]["code"] == "validation_error"
    assert client.delete(f"/api/medications/{mid}").status_code == 204
    assert client.delete(f"/api/medications/{mid}").status_code == 404


def test_contacts_and_appointments(client: TestClient) -> None:
    c = client.post("/api/contacts", json={"name": "Neha", "telegram_chat_id": "12345"})
    assert c.status_code == 201 and len(client.get("/api/contacts").json()) == 3
    assert client.post("/api/contacts", json={"name": "X", "telegram_chat_id": "abc"}).status_code == 422
    a = client.post("/api/appointments", json={"title": "Dentist", "starts_at": "2099-01-01T10:00:00"})
    assert a.status_code == 201
    assert client.post("/api/appointments", json={"title": "Old", "starts_at": "2001-01-01T10:00:00"}).status_code == 422


def test_simulator_chat_runs_through_mcp_in_process_server(live_server_chat) -> None:  # type: ignore[no-untyped-def]
    r = live_server_chat.post("/api/simulator/chat", json={"text": "I feel unwell"})
    d = r.json()
    assert r.status_code == 200 and d["tool_calls"][0]["name"] == "report_concern"
    assert "emergency services" in d["reply"] and d["used_llm"] is False
    events = live_server_chat.get("/api/events?limit=5").json()
    assert events[0]["type"] == "concern"
    calls = live_server_chat.get("/api/tool-calls?limit=5").json()
    assert calls[0]["tool_name"] == "report_concern" and calls[0]["source"] == "simulator"
    newer = live_server_chat.get(f"/api/tool-calls?after_id={calls[0]['id']}").json()
    assert newer == []


def test_gentle_checkin_and_reset(client: TestClient, notifier) -> None:  # type: ignore[no-untyped-def]
    assert client.post("/api/messages/check-in").json() == {"sent": 2, "total": 2}
    assert client.post("/api/admin/reset-demo").status_code == 200
