from api import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_check() -> None:
    resp = client.get("/check").raise_for_status()
    assert resp.json()["status"] == "ok"


def test_app() -> None:
    resp = client.get("/app").raise_for_status()
    assert resp.json()["message"] == "aaa!!!"
