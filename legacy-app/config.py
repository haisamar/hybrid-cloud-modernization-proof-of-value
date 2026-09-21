"""Legacy host-bound configuration.

Historical operators edited this file (or the sibling INI) on each host.
The defaults below document that operating model: a path that assumed
a specific machine layout rather than an injected environment contract.
"""

from __future__ import annotations

import os
from pathlib import Path

# Historical host assumption documented for the case study.
# Windows operators used something like C:\orders\orders.db.
# Linux operators used /var/lib/order-intake/orders.db.
# The running default is a local relative file so the PoV can start
# without that host layout. The *assumption* remains in DEPLOY.md.
HISTORICAL_WINDOWS_DB_PATH = r"C:\orders\orders.db"
HISTORICAL_LINUX_DB_PATH = "/var/lib/order-intake/orders.db"

APP_NAME = "legacy-order-intake"
HOST = os.environ.get("LEGACY_BIND_HOST", "127.0.0.1")
PORT = int(os.environ.get("LEGACY_BIND_PORT", "5000"))

_BASE = Path(__file__).resolve().parent
DEFAULT_DB_PATH = _BASE / "data" / "orders.db"

# Operators overrode this by editing the path on the host.
ORDERS_DB_PATH = os.environ.get("ORDERS_DB_PATH", str(DEFAULT_DB_PATH))
