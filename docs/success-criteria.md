# PoV success criteria

Statuses below reflect **commands actually run on the implementation
workstation**, not planned CI. Docker and Terraform are not marked TESTED
because those binaries were absent and no GitHub Actions run has been
observed yet.

| Criterion | Metric | Baseline (legacy) | PoV target | Validation method | Actual result / status |
|---|---|---|---|---|---|
| Repeatability | Same start path without host-specific copy steps | `python app.py` after manual file copy (`legacy-app/DEPLOY.md`) | Image + env + declared manifests | Code review of Dockerfile, ConfigMap, Deployment | **IMPLEMENTED** for artifacts. Image build **NOT EXECUTED** (no Docker/Podman). |
| Health visibility | `/health` and `/ready` plus probes | No probe endpoints | HTTP health + ready; YAML probes | pytest + static YAML tests | **TESTED** for app endpoints and YAML presence. Live cluster probes **NOT EXECUTED**. |
| Configuration separation | No host path required in modernized runtime | Historical `C:\orders\...` / `/var/lib/order-intake/...` | `DATABASE_URL` and ConfigMap | pytest override of `DATABASE_URL`; path scan | **TESTED** on SQLite URL override. |
| Deployment standardization | Complete OpenShift workload set | Operator runbook | Namespace, ConfigMap, Secret template, Deployment (`replicas: 1`), Service, Route | Static tests | **TESTED** (static). Apply **NOT EXECUTED**. |
| Infrastructure repeatability | Terraform files + validate | None | versions/providers/variables/main/outputs | File tests | Configuration **IMPLEMENTED**. `terraform validate` **NOT EXECUTED** (binary absent). |
| Recovery / rollback | Documented rollout undo | Restore files | `oc rollout undo` + readiness | Docs + Deployment strategy | **ARCHITECTED** / docs **IMPLEMENTED**. Live undo **NOT EXECUTED**. |
| Portability | Container-friendly paths | Host-bound docs | Dockerfile, `/app/data`, env | Dockerfile + path tests | Dockerfile **IMPLEMENTED**. Image **NOT EXECUTED**. |

## Persistence criteria (explicit)

| Criterion | Status |
|---|---|
| SQLite persistence | IMPLEMENTED / TESTED |
| DATABASE_URL abstraction | IMPLEMENTED / TESTED |
| PostgreSQL-ready architecture | ARCHITECTED |
| PostgreSQL runtime | NOT EXECUTED |
