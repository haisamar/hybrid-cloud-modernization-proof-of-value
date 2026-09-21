"""SQLAlchemy helpers.

Exercised path: SQLite via DATABASE_URL.
PostgreSQL-ready architecture is ARCHITECTED only — a future postgresql://
URL is not a tested driver/runtime path.
"""

from __future__ import annotations

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


def sqlite_connect_args(url: str) -> dict:
    if url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


def make_engine(url: str) -> Engine:
    return create_engine(url, future=True, connect_args=sqlite_connect_args(url))


def make_session_factory(engine: Engine):
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db(engine: Engine) -> None:
    from models import Order  # noqa: F401

    Base.metadata.create_all(engine)


def ping_database(engine: Engine) -> None:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
