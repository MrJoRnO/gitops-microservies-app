import pytest
from src.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_root_returns_200(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_root_contains_environment(client, monkeypatch):
    monkeypatch.setenv("APP_ENV", "staging")
    resp = client.get("/")
    assert b"staging" in resp.data


def test_healthz_returns_healthy(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "healthy"}


def test_readyz_returns_ready(client):
    resp = client.get("/readyz")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ready"}


def test_unknown_route_returns_404(client):
    resp = client.get("/does-not-exist")
    assert resp.status_code == 404
