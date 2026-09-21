# Legacy Order Intake — manual deployment

This document describes the **current-state operating model** used as the
before picture in the PoV. It is intentionally operator-dependent.

## Release steps (as practiced)

1. Copy `app.py` and `config.py` onto the target host (often via shared drive or USB).
2. Edit `config.py` or set `ORDERS_DB_PATH` to the host path used last time.
   - Historical Windows: `C:\orders\orders.db`
   - Historical Linux: `/var/lib/order-intake/orders.db`
3. Install Python packages on that host (`pip install -r requirements.txt`).
4. Start the process: `python app.py`.
5. Verify by opening `http://<host>:5000/` in a browser or with curl.
6. If something looks wrong, read the console output on that host.

## Rollback

1. Stop the Python process (Ctrl+C or Task Manager / kill).
2. Restore yesterday’s copied files.
3. Start `python app.py` again.
4. Hope the SQLite file is still consistent.

There is no rollout history, no readiness gate, and no standard image.

## What this PoV does **not** claim

This folder is a functional baseline, not a recommended production practice.
