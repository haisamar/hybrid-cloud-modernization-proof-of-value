"""Environment-based configuration.

SQLite is the only persistence runtime required for this PoV.
DATABASE_URL removes host-specific path assumptions.

PostgreSQL-ready architecture is ARCHITECTED only.
"""

from __future__ import annotations

import os
from pathlib import Path

APP_NAME = "order-intake"
APP_ENV = os.environ.get("APP_ENV", "local")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
PORT = int(os.environ.get("PORT", "8080"))
BIND_HOST = os.environ.get("BIND_HOST", "0.0.0.0")

_BASE = Path(__file__).resolve().parent
_DEFAULT_SQLITE = (_BASE / "data" / "orders.db").as_posix()


def default_database_url() -> str:
    return os.environ.get("DATABASE_URL", f"sqlite:///{_DEFAULT_SQLITE}")


# Local portfolio-demo (Vite) only. Production Vercel uses VITE_DEMO_MODE and
# never calls this API.
CORS_ORIGINS = os.environ.get(
    "CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
)


def persistence_mode(url: str) -> str:
    if url.startswith("sqlite"):
        return "sqlite"
    if url.startswith("postgresql"):
        return "postgresql"
    return "configured"
