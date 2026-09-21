"""Modernized Order Intake Service.

Same business capability as the legacy app. Operating-model changes:
environment configuration, DATABASE_URL, structured logs, health/ready.
"""

from __future__ import annotations

import logging
from pathlib import Path

from flask import Flask, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from config import APP_ENV, APP_NAME, BIND_HOST, CORS_ORIGINS, LOG_LEVEL, PORT, default_database_url, persistence_mode
from db import init_db, make_engine, make_session_factory, ping_database
from logging_config import configure_logging
from models import Order

configure_logging(LOG_LEVEL)
logger = logging.getLogger(APP_NAME)


def _ensure_sqlite_parent(database_url: str) -> None:
    if not database_url.startswith("sqlite"):
        return
    if ":memory:" in database_url:
        return
    raw = database_url.split("sqlite:///")[-1]
    if raw:
        Path(raw).parent.mkdir(parents=True, exist_ok=True)


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


def create_app(database_url: str | None = None) -> Flask:
    url = database_url or default_database_url()
    _ensure_sqlite_parent(url)
    engine = make_engine(url)
    SessionLocal = make_session_factory(engine)
    init_db(engine)

    app = Flask(__name__)
    app.config["DATABASE_URL"] = url
    app.config["ENGINE"] = engine
    allowed_origins = {item.strip() for item in CORS_ORIGINS.split(",") if item.strip()}

    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            return ("", 204)

    @app.after_request
    def add_cors(response):
        origin = request.headers.get("Origin")
        if origin in allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
            response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
        return response

    @app.get("/")
    def root():
        return jsonify(
            {
                "service": APP_NAME,
                "operating_model": "replatformed-container-ready",
                "environment": APP_ENV,
                "persistence_mode": persistence_mode(url),
                "message": "Order Intake Service",
            }
        )

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/ready")
    def ready():
        try:
            ping_database(engine)
        except SQLAlchemyError as exc:
            logger.error("readiness check failed: %s", exc)
            return jsonify({"status": "not_ready"}), 503
        return jsonify({"status": "ready"})

    @app.get("/orders")
    def list_orders():
        session = SessionLocal()
        try:
            orders = session.query(Order).order_by(Order.id).all()
            return jsonify([order.to_dict() for order in orders])
        finally:
            session.close()

    @app.post("/orders")
    def create_order():
        payload, error = validate_order_payload(request.get_json(silent=True))
        if error:
            body, status = error
            return jsonify(body), status
        session = SessionLocal()
        try:
            order = Order(
                customer_id=payload["customer_id"],
                sku=payload["sku"],
                quantity=payload["quantity"],
                status="accepted",
            )
            session.add(order)
            session.commit()
            session.refresh(order)
            logger.info("order_created id=%s sku=%s", order.id, order.sku)
            return jsonify(order.to_dict()), 201
        finally:
            session.close()

    @app.get("/orders/<int:order_id>")
    def get_order(order_id: int):
        session = SessionLocal()
        try:
            order = session.get(Order, order_id)
            if order is None:
                return jsonify({"error": "order not found"}), 404
            return jsonify(order.to_dict())
        finally:
            session.close()

    return app


app = create_app()


if __name__ == "__main__":
    # Local workstation startup. Container images use gunicorn (see Dockerfile).
    app.run(host=BIND_HOST, port=PORT, debug=False)
