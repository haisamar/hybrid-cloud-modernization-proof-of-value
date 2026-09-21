from __future__ import annotations

import sys
from pathlib import Path

import pytest

MOD_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MOD_ROOT))

from app import create_app  # noqa: E402
from sqlalchemy.exc import SQLAlchemyError  # noqa: E402


@pytest.fixture()
def client(tmp_path):
    db_file = tmp_path / "orders.db"
    flask_app = create_app(f"sqlite:///{db_file.as_posix()}")
    return flask_app.test_client()


def test_root_and_health(client):
    root = client.get("/")
    assert root.status_code == 200
    assert root.get_json()["service"] == "order-intake"
    health = client.get("/health")
    assert health.status_code == 200
    assert health.get_json()["status"] == "ok"


def test_create_retrieve_and_list(client):
    created = client.post(
        "/orders",
        json={"customer_id": "CUST-2001", "sku": "VALVE-B", "quantity": 3},
    )
    assert created.status_code == 201
    order = created.get_json()
    assert order["sku"] == "VALVE-B"
    fetched = client.get(f"/orders/{order['id']}")
    assert fetched.status_code == 200
    listed = client.get("/orders")
    assert len(listed.get_json()) == 1


def test_invalid_and_missing(client):
    bad = client.post("/orders", json={"customer_id": "C", "sku": "S"})
    assert bad.status_code == 400
    missing = client.get("/orders/4040")
    assert missing.status_code == 404


def test_ready_ok(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ready"


def test_database_url_override(tmp_path):
    other = tmp_path / "alt.db"
    flask_app = create_app(f"sqlite:///{other.as_posix()}")
    client = flask_app.test_client()
    created = client.post(
        "/orders",
        json={"customer_id": "CUST-9", "sku": "SKU-9", "quantity": 1},
    )
    assert created.status_code == 201
    assert other.exists()
    assert flask_app.config["DATABASE_URL"].endswith("alt.db")


def test_ready_fails_when_database_ping_fails(tmp_path, monkeypatch):
    db_file = tmp_path / "orders.db"
    flask_app = create_app(f"sqlite:///{db_file.as_posix()}")

    def boom(_engine):
        raise SQLAlchemyError("unavailable")

    monkeypatch.setattr("app.ping_database", boom)
    response = flask_app.test_client().get("/ready")
    assert response.status_code == 503


def test_no_workstation_specific_paths():
    source = (MOD_ROOT / "app.py").read_text(encoding="utf-8")
    config = (MOD_ROOT / "config.py").read_text(encoding="utf-8")
    combined = source + config
    assert "C:\\Users\\" not in combined
    assert "/Users/" not in combined
    assert "C:\\orders\\" not in combined
