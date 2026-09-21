# PoV success criteria

Statuses below reflect **commands actually run**, including GitHub Actions
workflow **validate #2** on commit `518e3d0`. Docker **image build** in CI
is not an OpenShift deployment. Terraform fmt/init/validate in CI is not
`terraform plan` or `terraform apply`.

| Criterion | Metric | Baseline (legacy) | PoV target | Validation method | Actual result / status |
|---|---|---|---|---|---|
| Repeatability | Same start path without host-specific copy steps | `python app.py` after manual file copy (`legacy-app/DEPLOY.md`) | Image + env + declared manifests | Code review of Dockerfile, ConfigMap, Deployment; CI `docker build` | **TESTED IN CI** for image **build** (`validate` #2, `518e3d0`). OpenShift deploy **NOT EXECUTED**. |
| Health visibility | `/health` and `/ready` plus probes | No probe endpoints | HTTP health + ready; YAML probes | pytest + static YAML tests | **TESTED** for app endpoints and YAML presence. Live cluster probes **NOT EXECUTED**. |
| Configuration separation | No host path required in modernized runtime | Historical `C:\orders\...` / `/var/lib/order-intake/...` | `DATABASE_URL` and ConfigMap | pytest override of `DATABASE_URL`; path scan | **TESTED** on SQLite URL override. |
| Deployment standardization | Complete OpenShift workload set | Operator runbook | Namespace, ConfigMap, Secret template, Deployment (`replicas: 1`), Service, Route | Static tests | **TESTED** (static). Apply **NOT EXECUTED**. |
| Infrastructure repeatability | Terraform files + validate | None | versions/providers/variables/main/outputs | File tests + CI fmt/init/validate | **TESTED IN CI** for `terraform fmt -check`, `init -backend=false`, and `validate` (`validate` #2, `518e3d0`). `terraform plan` / `apply` **NOT EXECUTED**. |
| Recovery / rollback | Documented rollout undo | Restore files | `oc rollout undo` + readiness | Docs + Deployment strategy | **ARCHITECTED** / docs **IMPLEMENTED**. Live undo **NOT EXECUTED**. |
| Portability | Container-friendly paths | Host-bound docs | Dockerfile, `/app/data`, env | Dockerfile + path tests + CI `docker build` | Dockerfile **IMPLEMENTED**. Image **build TESTED IN CI**. Container was not deployed to OpenShift. |

## Persistence criteria (explicit)

| Criterion | Status |
|---|---|
| SQLite persistence | IMPLEMENTED / TESTED |
| DATABASE_URL abstraction | IMPLEMENTED / TESTED |
| PostgreSQL-ready architecture | ARCHITECTED |
| PostgreSQL runtime | NOT EXECUTED |
