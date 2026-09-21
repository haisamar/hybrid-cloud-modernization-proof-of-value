# Implementation status

Allowed labels: **IMPLEMENTED**, **TESTED**, **TESTED IN CI**, **ARCHITECTED**, **NOT EXECUTED**.

Workstation detection was recorded on 2026-09-20. GitHub Actions workflow
**validate #2** completed successfully on commit `518e3d0`. That run is the
evidence for Python 3.12 tests, Docker image **build**, and Terraform
**fmt / init / validate**. It is not evidence of OpenShift deploy, rollback,
or `terraform plan` / `terraform apply`.

| Item | Status | Evidence |
|---|---|---|
| Legacy application | IMPLEMENTED / TESTED | `legacy-app/` pytest (local) |
| Modernized application | IMPLEMENTED / TESTED | `modernized-app/` pytest (local) |
| Application tests | IMPLEMENTED / TESTED | pytest run recorded on the implementation workstation (Python 3.14.7 locally) |
| Python 3.12 application tests | TESTED IN CI | GitHub Actions `validate` #2 on `518e3d0`: pytest on Python 3.12 for legacy, modernized, and infrastructure tests |
| SQLite persistence | IMPLEMENTED / TESTED | default DB + tests |
| DATABASE_URL abstraction | IMPLEMENTED / TESTED | override test to alternate SQLite file |
| PostgreSQL-ready architecture | ARCHITECTED | SQLAlchemy `DATABASE_URL` could accept a future `postgresql://` URL; no driver, no server, no exercise |
| PostgreSQL runtime | NOT EXECUTED | no Postgres server, no psycopg test |
| Dockerfile | IMPLEMENTED | `modernized-app/Dockerfile` |
| Docker image build | TESTED IN CI | GitHub Actions `validate` #2 on `518e3d0` ran `docker build` for `modernized-app`. This is an image **build**, not a container running on OpenShift. |
| OpenShift manifests | IMPLEMENTED / TESTED | static pytest on YAML |
| OpenShift deployment | NOT EXECUTED | `oc` / `kubectl` absent; no cluster; CI does not apply manifests |
| OpenShift rollback | NOT EXECUTED | rollout undo was not run against a cluster |
| Terraform configuration | IMPLEMENTED | `infra/terraform/` |
| Terraform validation | TESTED IN CI | GitHub Actions `validate` #2 on `518e3d0`: `terraform fmt -check`, `terraform init -backend=false`, `terraform validate`. This is not `terraform plan` or `terraform apply`. |
| Terraform apply | NOT EXECUTED | no kubeconfig/cluster apply; CI does not plan or apply |
| Hybrid architecture | ARCHITECTED | README + demo Mermaid; not a live dual-site deploy |
| IBM Cloud deployment | NOT EXECUTED | not in scope |
| Public portfolio demo | IMPLEMENTED / TESTED | `npm run build` succeeded locally |
| Public demo hosting (Vercel) | NOT EXECUTED | not deployed unless later requested |
| GitHub Actions | TESTED IN CI | workflow `validate` #2 succeeded on commit `518e3d0` |
