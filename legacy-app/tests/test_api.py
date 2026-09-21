from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

LEGACY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LEGACY_ROOT))


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "orders.db"
    monkeypatch.setenv("ORDERS_DB_PATH", str(db_path))
    import importlib

    import config

    importlib.reload(config)
    import app as legacy_app

    importlib.reload(legacy_app)
    legacy_app.init_db()
    return legacy_app.app.test_client()


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.get_json()
    assert body["service"] == "legacy-order-intake"


def test_create_and_retrieve_order(client):
    created = client.post(
        "/orders",
        json={"customer_id": "CUST-1001", "sku": "PUMP-A", "quantity": 2},
    )
    assert created.status_code == 201
    order = created.get_json()
    assert order["id"] >= 1
    assert order["status"] == "accepted"

    listed = client.get("/orders")
    assert listed.status_code == 200
    assert len(listed.get_json()) == 1

    fetched = client.get(f"/orders/{order['id']}")
    assert fetched.status_code == 200
    assert fetched.get_json()["sku"] == "PUMP-A"


def test_invalid_request(client):
    response = client.post("/orders", json={"customer_id": "CUST-1", "sku": "X", "quantity": 0})
    assert response.status_code == 400
    missing = client.get("/orders/999")
    assert missing.status_code == 404


def test_historical_host_paths_are_documented():
    import config

    assert config.HISTORICAL_WINDOWS_DB_PATH.startswith(r"C:")
    assert config.HISTORICAL_LINUX_DB_PATH.startswith("/var/lib/")
    # Running default must not require those host paths.
    assert not str(config.DEFAULT_DB_PATH).startswith(r"C:\orders")
    os.environ.get("ORDERS_DB_PATH")
