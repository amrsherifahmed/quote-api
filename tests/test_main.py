import pytest

from app.main import QUOTES, create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_quote_returns_a_known_quote(client):
    res = client.get("/quote")
    assert res.status_code == 200
    data = res.get_json()
    assert set(data) == {"text", "author"}
    assert data in QUOTES


def test_version_default_is_dev(client, monkeypatch):
    monkeypatch.delenv("APP_VERSION", raising=False)
    res = client.get("/version")
    assert res.status_code == 200
    assert res.get_json() == {"version": "dev"}


def test_version_from_env(client, monkeypatch):
    monkeypatch.setenv("APP_VERSION", "abc1234")
    res = client.get("/version")
    assert res.get_json() == {"version": "abc1234"}


def test_unknown_route_returns_json_404(client):
    res = client.get("/does-not-exist")
    assert res.status_code == 404
    assert res.get_json() == {"error": "not found"}
