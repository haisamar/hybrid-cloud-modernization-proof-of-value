# OpenShift artifacts

These manifests describe an **OpenShift-compatible** Order Intake deployment
for the modernization PoV. They have **not** been applied to a cluster in the
initial implementation unless `implementation-status.md` says otherwise.

## Persistence constraint

The Deployment sets `replicas: 1` because the demonstrated database is SQLite
on an `emptyDir` volume.

- SQLite / emptyDir is PoV-only and is **not** highly available
- Replacing the pod may lose ephemeral order data
- Horizontal scaling requires external shared persistence
- Production database modernization is **outside this PoV**
- Do not imply this SQLite path supports multi-replica OpenShift scaling

## NetworkPolicy

`networkpolicy.yaml` is an **example baseline**. Router namespaces, labels,
and ingress selectors differ by cluster. Validate them with the customer
platform team before apply. Sample selectors are not universally correct.

## Apply (requires a real cluster and `oc`)

```bash
oc apply -f namespace.yaml
oc apply -f configmap.yaml
oc apply -f secret.yaml
oc apply -f deployment.yaml
oc apply -f service.yaml
oc apply -f route.yaml
# Optional — confirm selectors first:
# oc apply -f networkpolicy.yaml
```

## Verification (requires a cluster)

```bash
oc get pods -n order-intake-pov
oc get route order-intake -n order-intake-pov
oc rollout status deployment/order-intake -n order-intake-pov
oc rollout history deployment/order-intake -n order-intake-pov
```

## Rollback (requires a cluster)

```bash
oc rollout undo deployment/order-intake -n order-intake-pov
oc rollout status deployment/order-intake -n order-intake-pov
```

Readiness (`/ready`) keeps an unready pod out of Service endpoints. That
behavior is **architected** in the Deployment probes. A live undo was
**not executed** unless a cluster was used.

## What requires an actual cluster

- image pull / `oc apply`
- Route hostname
- rollout status / history / undo
- NetworkPolicy enforcement
- live probe traffic

Without `oc`/`kubectl` and a cluster: manifests are IMPLEMENTED; deployment
is NOT EXECUTED.
