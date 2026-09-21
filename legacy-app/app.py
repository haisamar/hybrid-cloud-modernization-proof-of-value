"""Legacy Order Intake Service.

Functional Flask API with a direct-process operating model:
start with python app.py, persist to a local SQLite file, no probes.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request

from config import APP_NAME, HOST, ORDERS_DB_PATH, PORT

app = Flask(__name__)


def _connect() -> sqlite3.Connection:
    path = Path(ORDERS_DB_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT NOT NULL,
                sku TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'accepted'
            )
            """
        )
        conn.commit()


def _row_to_order(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "customer_id": row["customer_id"],
        "sku": row["sku"],
        "quantity": row["quantity"],
        "status": row["status"],
    }


def validate_order_payload(payload: object) -> tuple[dict | None, tuple[dict, int] | None]:
    if not isinstance(payload, dict):
        return None, ({"error": "JSON object required"}, 400)
    customer_id = payload.get("customer_id")
    sku = payload.get("sku")
    quantity = payload.get("quantity")
    if not customer_id or not isinstance(customer_id, str):
        return None, ({"error": "customer_id is required"}, 400)
    if not sku or not isinstance(sku, str):
        return None, ({"error": "sku is required"}, 400)
    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 1:
        return None, ({"error": "quantity must be an integer greater than 0"}, 400)
    return {
        "customer_id": customer_id.strip(),
        "sku": sku.strip(),
        "quantity": quantity,
    }, None


@app.get("/")
def root():
    return jsonify(
        {
            "service": APP_NAME,
            "operating_model": "legacy-direct-process",
            "message": "Legacy Order Intake Service",
        }
    )


@app.get("/orders")
def list_orders():
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM orders ORDER BY id").fetchall()
    return jsonify([_row_to_order(row) for row in rows])


@app.post("/orders")
def create_order():
    payload, error = validate_order_payload(request.get_json(silent=True))
    if error:
        body, status = error
        return jsonify(body), status
    with _connect() as conn:
        cursor = conn.execute(
            "INSERT INTO orders (customer_id, sku, quantity, status) VALUES (?, ?, ?, ?)",
            (payload["customer_id"], payload["sku"], payload["quantity"], "accepted"),
        )
        conn.commit()
        order_id = cursor.lastrowid
        row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    return jsonify(_row_to_order(row)), 201


@app.get("/orders/<int:order_id>")
def get_order(order_id: int):
    with _connect() as conn:
        row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if row is None:
        return jsonify({"error": "order not found"}), 404
    return jsonify(_row_to_order(row))


init_db()


if __name__ == "__main__":
    # Legacy operating model: Flask development server started by an operator.
    app.run(host=HOST, port=PORT, debug=False)
