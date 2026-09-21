# Modernization decision matrix

This comparison is for **Northline Industrial Order Intake** in this PoV.
Replatform is selected here; it is **not** universally the best 6R choice.

Criteria are qualitative. No arbitrary numeric score is assigned.

| Criterion | Rehost | Replatform (selected) | Refactor |
|---|---|---|---|
| Implementation effort | Lowest — move the host process | Moderate — container, config, probes, manifests, IaC | Highest — domain rewrite / new services |
| Time to value | Fast move, slow operational relief | Faster relief of release/ops pain | Slowest |
| Business disruption | Low during move; ops toil remains | Low — same API and business rules | High — new contracts and testing surface |
| Portability | Tied to VM/host assumptions | Image + env contract | High if redesigned, expensive to reach |
| Operational consistency | Still operator-dependent | Git, image, OpenShift Deployment | Potentially highest after rewrite |
| Scalability | New hosts by hand | Constrained here by SQLite (`replicas: 1`) | Could introduce shared DB / services |
| Technical debt | Mostly unchanged | App-level debt remains; ops debt reduced | Lowest leftover debt if done well |
| Migration risk | Environment mismatch, same start procedure | Image/config mistakes; logic preserved | Logic and data-model risk |
| Rollback complexity | Restore files / previous VM | Deployment revision / prior image | Depends on dual-running and data migrations |

## Why Rehost is not selected

Rehost would relocate the same Flask process. Manual configuration, weak
health visibility, and operator-dependent starts would travel with it.
That does not address the stated pains.

## Why Refactor is not the first move

A rewrite could remove remaining application debt and unlock a shared
database, but it would delay value, raise disruption, and is unnecessary
while the business logic is adequate and the ERP cannot move.

## Why Replatform is selected for this PoV

Preserve order-intake behavior. Improve the operating model with
containerization, environment configuration, health/readiness,
OpenShift-compatible deployment, and Terraform for platform
prerequisites. ERP stays on-prem behind an integration boundary.

A later refactor (and a later database modernization) remains valid if
scale, HA, or domain complexity demand it. Those are **next phases**,
not this PoV.

## Persistence note

SQLite remains the PoV database so this decision is about **how the
application is run**, not a database migration project.
