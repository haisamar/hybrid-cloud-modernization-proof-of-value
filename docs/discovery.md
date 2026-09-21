# Discovery — Legacy Order Intake Service

This note is written as a Technical Seller discovery record for a **fictional
case study** (Northline Industrial). It is not a transcript of a live customer.

Every item is labeled so assumptions are not presented as customer facts.

## How to read the labels

| Label | Meaning |
|---|---|
| KNOWN FOR CASE STUDY | Consistent facts invented for this PoV |
| ASSUMED FOR POV | Needed to build artifacts; not customer-attested |
| MUST VALIDATE WITH CUSTOMER | Questions that would be asked in a real engagement |

---

## Business discovery

### What business process depends on this application?

- **KNOWN FOR CASE STUDY:** Customer service / B2B order clerks submit orders into the Order Intake Service before fulfillment.
- **ASSUMED FOR POV:** The API is the system of record for *accepted intake*, not for invoicing.
- **MUST VALIDATE WITH CUSTOMER:** Which upstream channels (EDI, portal, CSR desktop) actually call this service today?

### Business impact of a failed release?

- **KNOWN FOR CASE STUDY:** A failed start on the app host blocks new order capture until an operator restores files and restarts the process.
- **ASSUMED FOR POV:** Existing accepted orders in SQLite remain, but new capture stops.
- **MUST VALIDATE WITH CUSTOMER:** Revenue/SLA impact, peak hours, and whether a paper/email workaround exists.

### Deployment frequency?

- **KNOWN FOR CASE STUDY:** Releases are infrequent and operator-scheduled.
- **ASSUMED FOR POV:** Weekly or less, because each release is a copy/edit/start procedure.
- **MUST VALIDATE WITH CUSTOMER:** Actual cadence and change-freeze windows.

### Acceptable downtime?

- **KNOWN FOR CASE STUDY:** Planned maintenance is tolerated; unplanned outages during the order desk shift are not.
- **ASSUMED FOR POV:** Rolling updates with readiness are acceptable for the PoV target.
- **MUST VALIDATE WITH CUSTOMER:** RTO/RPO and whether a maintenance window is required.

### Rollback expectations?

- **KNOWN FOR CASE STUDY:** Rollback today means stop process, restore prior files, start again.
- **ASSUMED FOR POV:** OpenShift `rollout undo` is the desired operating model.
- **MUST VALIDATE WITH CUSTOMER:** Who is authorized to roll back, and is data-forward repair required?

### Compliance / data residency?

- **KNOWN FOR CASE STUDY:** Order records are treated as operational manufacturing data that currently lives on-prem.
- **ASSUMED FOR POV:** The PoV may run the *application* on OpenShift while ERP stays on-prem.
- **MUST VALIDATE WITH CUSTOMER:** Residency rules, retention, and whether order payloads may leave the current site.

### Which systems cannot move?

- **KNOWN FOR CASE STUDY:** The on-prem ERP / order fulfillment stack cannot move in this phase (licensed vendor, batch jobs, local integrations).
- **ASSUMED FOR POV:** A later integration hop can remain a documented boundary without a live ERP connection in the PoV.
- **MUST VALIDATE WITH CUSTOMER:** Exact ERP product, interfaces (file, queue, API), and freeze dates.

### Growth expectations?

- **KNOWN FOR CASE STUDY:** Volume is moderate; pain is operational consistency, not extreme scale.
- **ASSUMED FOR POV:** A single replica with SQLite is enough to demonstrate replatforming.
- **MUST VALIDATE WITH CUSTOMER:** Peak orders/minute and whether multi-site intake is planned.

### Operating ownership?

- **KNOWN FOR CASE STUDY:** Application owners plus a small ops group who know “how we start it on that host.”
- **ASSUMED FOR POV:** Platform team would own the OpenShift project after a successful PoV.
- **MUST VALIDATE WITH CUSTOMER:** RACI for app vs platform vs ERP.

---

## Technical discovery

### Runtime

- **KNOWN FOR CASE STUDY:** Python / Flask process started on a host.
- **ASSUMED FOR POV:** Python 3.12+ in containers is acceptable.
- **MUST VALIDATE WITH CUSTOMER:** Current Python version, OS, and whether a corporate base image is mandatory.

### Persistence

- **KNOWN FOR CASE STUDY:** Local SQLite file; path historically host-specific.
- **ASSUMED FOR POV:** SQLite remains valid for the PoV; `DATABASE_URL` removes the host-path assumption.
- **MUST VALIDATE WITH CUSTOMER:** Whether shared enterprise DB is already required for HA. PostgreSQL is **not** in this PoV runtime.

### Integrations

- **KNOWN FOR CASE STUDY:** Downstream ERP must remain on-prem.
- **ASSUMED FOR POV:** Handoff can be delayed; PoV demonstrates the intake API only.
- **MUST VALIDATE WITH CUSTOMER:** Protocol, auth, retry, and idempotency of the ERP interface.

### Auth

- **ASSUMED FOR POV:** Network-internal API for this phase (no SSO implemented).
- **MUST VALIDATE WITH CUSTOMER:** IdP, mTLS, API keys, and who the callers are.

### Networking

- **ASSUMED FOR POV:** An OpenShift Route can expose the service inside the customer platform.
- **MUST VALIDATE WITH CUSTOMER:** Private vs public Route, DNS, TLS certs, and ingress NetworkPolicy selectors (cluster-specific).

### Secrets / configuration

- **KNOWN FOR CASE STUDY:** Operators edit files on the host.
- **ASSUMED FOR POV:** ConfigMap + Secret template is the target contract.
- **MUST VALIDATE WITH CUSTOMER:** Existing secret store (Vault, cloud KMS, sealed secrets).

### Observability

- **KNOWN FOR CASE STUDY:** Console logs on the host; no `/health` or `/ready`.
- **ASSUMED FOR POV:** Structured stdout plus probes is the first increment.
- **MUST VALIDATE WITH CUSTOMER:** Required APM, log sink, and SLO tooling.

### Deployment process

- **KNOWN FOR CASE STUDY:** Copy files, edit config, start process, eyeball the result.
- **ASSUMED FOR POV:** Git → container image → `oc apply` / rolling update.
- **MUST VALIDATE WITH CUSTOMER:** Image registry, cluster project, and change-management tickets.

### Recovery expectations

- **KNOWN FOR CASE STUDY:** Manual rollback of files.
- **ASSUMED FOR POV:** Deployment revision history is sufficient for app rollback; SQLite on emptyDir is **not** a DR story.
- **MUST VALIDATE WITH CUSTOMER:** Backup of order data and ERP reconciliation.

---

## Discovery outcome used by this PoV

Modernize the **deployment and operating model** first (replatform). Do not
rewrite business logic and do not move the ERP in this phase.
