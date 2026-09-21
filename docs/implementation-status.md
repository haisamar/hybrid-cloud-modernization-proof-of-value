# Implementation status

Allowed labels: **IMPLEMENTED**, **TESTED**, **ARCHITECTED**, **NOT EXECUTED**.

Recorded after workstation detection on 2026-09-20. Planned GitHub Actions
does **not** change TESTED until a successful workflow run is observed.

| Item | Status | Evidence |
|---|---|---|
| Legacy application | IMPLEMENTED / TESTED | `legacy-app/` pytest |
| Modernized application | IMPLEMENTED / TESTED | `modernized-app/` pytest |
| Application tests | IMPLEMENTED / TESTED | pytest run recorded in implementation notes |
| SQLite persistence | IMPLEMENTED / TESTED | default DB + tests |
| DATABASE_URL abstraction | IMPLEMENTED / TESTED | override test to alternate SQLite file |
| PostgreSQL-ready architecture | ARCHITECTED | SQLAlchemy `DATABASE_URL` could accept a future `postgresql://` URL; no driver, no server, no exercise |
| PostgreSQL runtime | NOT EXECUTED | no Postgres server, no psycopg test |
| Dockerfile | IMPLEMENTED | `modernized-app/Dockerfile` |
| Docker image | NOT EXECUTED | `docker` / `podman` absent |
| OpenShift manifests | IMPLEMENTED / TESTED | static pytest on YAML |
| OpenShift deployment | NOT EXECUTED | `oc` / `kubectl` absent; no cluster |
| Terraform configuration | IMPLEMENTED | `infra/terraform/` |
| Terraform validation | NOT EXECUTED | `terraform` binary absent |
| Hybrid architecture | ARCHITECTED | README + demo Mermaid; not a live dual-site deploy |
| IBM Cloud deployment | NOT EXECUTED | not in scope |
| Public portfolio demo | IMPLEMENTED / TESTED | `npm run build` succeeded locally |
| Public demo hosting (Vercel) | NOT EXECUTED | not deployed unless later requested |
| GitHub Actions | IMPLEMENTED | workflow file present; run **NOT EXECUTED** until observed |
