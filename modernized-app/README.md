# Modernized Order Intake

Same business API as `legacy-app`. Operating-model changes only.

Local Windows: `python app.py` (Flask). Linux containers: gunicorn (Dockerfile).

SQLite is the required database. `DATABASE_URL` is tested with SQLite URLs.
PostgreSQL-ready architecture is documented only (ARCHITECTED). No Postgres
driver is required.
