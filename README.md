# Hybrid Cloud Modernization Proof-of-Value

A public portfolio project that demonstrates how a working legacy application can be modernized without unnecessarily rewriting the business logic that already works.

[**View the Live Demo**](https://hybrid-cloud-modernization-proof-of.vercel.app/) · [**View the Source Code**](https://github.com/haisamar/hybrid-cloud-modernization-proof-of-value)

---

## What this project is about

A legacy application does not automatically need to be rewritten.

Sometimes the application still performs its business function correctly, but everything around it has become difficult:

- deployments are manual
- configuration differs between environments
- application health is difficult to verify
- rollback is risky
- infrastructure is inconsistent
- operational knowledge lives in people rather than repeatable processes
- existing systems cannot simply be replaced

This project explores a more practical modernization question:

> **If the business logic still works, what should actually be modernized?**

The answer in this proof of value is **replatforming**.

The application keeps its useful core behavior while its configuration, packaging, deployment model, health visibility, infrastructure definition, and operating model are modernized.

---

## Live demo

**Public demo:**  
https://hybrid-cloud-modernization-proof-of.vercel.app/

The hosted experience is designed to explain the modernization story in plain English before introducing the deeper technical architecture.

It walks through:

- the original business and operational problem
- the legacy application
- Rehost vs Replatform vs Refactor
- why Replatform was selected
- the modernized application
- before-and-after operating models
- Docker
- OpenShift
- Terraform
- hybrid cloud
- success criteria
- implementation and validation status

The public website uses a deterministic browser-based demonstration.

It does **not** pretend to be a live OpenShift cluster or deployed cloud environment.

The deeper implementation and infrastructure artifacts are available in this repository.

---

# The idea in plain English

The easiest analogy is:

> **The recipe still works. The kitchen is the problem.**

Imagine a restaurant with a great recipe, but:

- every cook prepares it differently
- nobody knows whether the oven is working until an order fails
- setup instructions exist only in someone's head
- moving to another kitchen is painful
- rollback means manually undoing changes

You do not necessarily need a new recipe.

You need a better kitchen and a better way of operating it.

That is what this project demonstrates.

```text
Working business logic
        ↓
Identify the real operational problems
        ↓
Keep the useful application behavior
        ↓
Modernize configuration and runtime
        ↓
Package it consistently
        ↓
Define deployment as code
        ↓
Prepare it for a modern platform
```

---

# Customer scenario

The proof of value uses a fictional company called **Northline Industrial**.

Northline relies on a legacy **Order Intake Service**.

Employees can still create and manage orders, so the application is providing real business value.

The problem is how the application is operated.

The legacy environment represents challenges such as:

- manual startup
- machine-specific configuration
- inconsistent environments
- limited application-health visibility
- manual rollback
- infrastructure that is difficult to reproduce
- dependencies on an existing on-premises ERP

The goal is not to replace everything.

The goal is to improve the application and operating model while preserving the parts of the environment that still make sense.

---

# The modernization decision

The project compares three common modernization strategies.

## Rehost

Move the application with as few changes as possible.

In plain English:

> **Move the same application somewhere new.**

This can be fast, but it can also move the same operational problems into a different environment.

```text
Legacy application
        ↓
New infrastructure
```

The hosting location changes, but the application operating model may remain mostly the same.

---

## Replatform

Keep most of the working application while improving how it is configured, packaged, deployed, and operated.

In plain English:

> **Keep the recipe, improve the kitchen.**

```text
Existing business logic
        ↓
External configuration
        ↓
Health + readiness
        ↓
Container artifact
        ↓
Standardized deployment
```

This is the strategy selected for the proof of value.

---

## Refactor

Make significant architectural or code changes.

In plain English:

> **Redesign the recipe and the kitchen.**

This can make sense when the application architecture itself is the primary problem.

But it usually introduces more:

- engineering effort
- migration complexity
- delivery time
- testing requirements
- business risk

For this case study, the immediate problems did not justify that level of change.

---

# Why Replatform was selected

The application already worked.

The biggest problems were around:

- deployments
- configuration
- runtime health
- repeatability
- environment consistency
- rollback
- operational friction

That makes this primarily an **operating-model problem**, not a broken-business-logic problem.

So the project chooses:

**REPLATFORM**

rather than rewriting functionality that does not need to be rewritten.

---

# Before modernization

The legacy application represents a traditional operating model.

```text
Users
  ↓
Legacy Order Intake Service
  ↓
Application logic
  ↓
Local persistence
  ↓
Existing business systems
```

The legacy version intentionally represents characteristics such as:

- Flask application
- manual startup assumptions
- configuration tied closely to the runtime environment
- limited explicit health information
- local persistence
- manual operational procedures
- no standardized container artifact
- infrastructure not consistently represented as code

The point is not that legacy software is inherently bad.

The problem is that operating it becomes more difficult as the environment grows.

---

# After modernization

The modernized version preserves the business capability while changing how the application is operated.

```text
Users
  ↓
Application Route
  ↓
Modernized Order Intake Service
  ↓
Externalized configuration
  ↓
Health + readiness checks
  ↓
Container-ready runtime
  ↓
Standardized platform definition
```

The modernized application includes:

- environment-based configuration
- structured logging
- `/health`
- `/ready`
- SQLAlchemy persistence abstraction
- configurable `DATABASE_URL`
- container-ready packaging
- non-root container execution
- production-style application serving
- OpenShift-compatible manifests
- Terraform infrastructure definitions

---

# What actually changed?

Modernization does not mean changing everything.

The project deliberately separates **business behavior** from **operational behavior**.

## Business behavior

The core order-intake capability remains.

The application can still perform the same general business function.

## Operational behavior

The application becomes easier to:

- configure
- inspect
- package
- deploy
- validate
- reproduce
- move between environments

That is the main value of the modernization.

---

# Configuration

The legacy application represents environment-specific assumptions.

The modernized version externalizes configuration.

For example:

```text
DATABASE_URL
```

can define where persistence lives.

This creates a clean boundary between:

```text
Application code
```

and:

```text
Environment configuration
```

The application does not need to be rewritten simply because the environment changes.

---

# Health and readiness

The modernized application exposes two operational checks.

## `/health`

Answers:

> **Is the application process alive?**

## `/ready`

Answers:

> **Is the application ready to receive traffic?**

These sound similar, but they solve different operational problems.

A platform may need to know that an application process exists while still preventing traffic from reaching it until the application is actually ready.

This distinction becomes particularly useful in container orchestration environments.

---

# Database abstraction

The modernized application uses SQLAlchemy with a configurable database URL.

The proof of value uses SQLite.

```text
Application
    ↓
SQLAlchemy
    ↓
DATABASE_URL
    ↓
SQLite in the PoV
```

The important architectural improvement is the boundary.

Persistence configuration is no longer tightly embedded in the application.

A future external database could use the same boundary.

**PostgreSQL runtime was not executed or claimed as tested in this project.**

---

# Structured logging

The modernized application also improves operational visibility through structured application logging.

Instead of treating the application as a black box, operational behavior becomes easier to inspect and reason about.

This is part of modernization even though it does not change the business feature itself.

---

# Containerization with Docker

The project includes a Docker artifact for the modernized application.

The goal is to create a repeatable application package.

Instead of:

> “It works on this particular machine.”

the goal becomes:

> “This artifact contains the application and the runtime expectations needed to run it consistently.”

The container design includes practices such as:

- no embedded application secrets
- non-root execution
- externalized configuration
- production-style application serving

The Docker image build is **tested in GitHub Actions**.

That proves the artifact builds successfully in a clean CI environment.

It does **not** mean the image was deployed to a production cluster.

---

# What Docker solves here

Without a standardized artifact:

```text
Application
+
Machine configuration
+
Installed packages
+
Manual setup
=
"It depends on the server"
```

With containerization:

```text
Application
+
Runtime dependencies
+
Defined startup behavior
=
Repeatable artifact
```

Docker does not solve every infrastructure problem.

It gives the application a more consistent packaging boundary.

---

# OpenShift architecture

The repository includes OpenShift-compatible application deployment artifacts.

These demonstrate how the modernized workload could run on an orchestration platform.

The artifacts cover concepts such as:

- Namespace
- ConfigMap
- Secret template
- Deployment
- Service
- Route
- NetworkPolicy
- health/readiness probes
- resource requests and limits
- rolling updates
- security context

A simplified application path is:

```text
User
 ↓
OpenShift Route
 ↓
Service
 ↓
Application Pod
 ↓
Modernized Order Intake Service
```

---

# What OpenShift would add

Docker gives us the application artifact.

OpenShift would help operate that artifact.

It provides concepts around:

- scheduling
- routing
- deployment
- configuration
- health checking
- rollout behavior
- isolation
- resources
- networking

In other words:

```text
Docker
= What should run?

OpenShift
= How should it run and be operated?
```

---

# Important OpenShift boundary

The repository contains the OpenShift-compatible manifests.

However:

**A live OpenShift deployment was not executed as part of this proof of value.**

The manifests are implementation artifacts and architecture evidence.

They should not be interpreted as proof that the application was deployed to a real OpenShift cluster.

---

# Why the example uses one replica

The proof of value uses SQLite and local application storage.

That matters.

Running multiple application replicas against independent local SQLite files would create misleading behavior.

Because of that, the example platform configuration intentionally uses a single application replica.

```text
1 application replica
+
PoV SQLite persistence
```

This is appropriate for the proof of value.

A production architecture would require a shared external persistence layer before scaling the application horizontally.

The project does not pretend otherwise.

---

# Terraform

Terraform represents platform and infrastructure prerequisites as code.

Instead of relying on manual infrastructure creation:

```text
Someone clicks around
→ resources exist
→ nobody remembers exactly how
```

the goal becomes:

```text
Infrastructure definition
→ version controlled
→ reviewable
→ repeatable
→ validated
```

---

# Separation between Terraform and OpenShift manifests

The project intentionally avoids defining the exact same application deployment twice.

The responsibilities are separated.

```text
Terraform
    ↓
Platform / infrastructure prerequisites

OpenShift manifests
    ↓
Application deployment definition
```

This gives each tool a clear purpose.

---

# Terraform validation

The Terraform configuration is validated in CI.

GitHub Actions successfully checks:

```text
terraform fmt
terraform init
terraform validate
```

This means the Terraform configuration is structurally valid in the validation environment.

It does **not** mean:

```text
terraform apply
```

was executed against real infrastructure.

A real infrastructure apply remains outside the executed scope of this proof of value.

---

# Hybrid cloud

One of the most important decisions in the project is what **does not move**.

The fictional Northline environment already has an ERP system.

The project does not assume that modernization means:

> Move every existing system into the cloud.

Instead, the target architecture allows the modernized workload and existing environment to coexist.

```text
Customers / Employees
        ↓
Modern application entry point
        ↓
Order Intake Service
        ↓
      ┌─┴─────────────────┐
      ↓                   ↓
Application           Integration
persistence            boundary
                          ↓
                    Existing ERP
                    remains on-prem
```

That is the hybrid-cloud idea.

---

# Why keep an existing system on-premises?

Real organizations rarely start modernization with an empty environment.

They may already have:

- ERP systems
- databases
- specialized hardware
- regulated workloads
- established integrations
- vendor dependencies
- large amounts of operational history

Replacing everything may create more risk than value.

A hybrid architecture allows an organization to modernize where it makes sense while retaining systems that still serve a purpose.

---

# Integration boundary

The modernized application does not pretend the legacy ERP disappeared.

Instead, it creates a clearer architectural boundary around integration with that system.

```text
Modernized application
        ↓
Integration boundary
        ↓
Existing ERP
```

This allows modernization to happen incrementally.

---

# Discovery comes before technology

Another important part of the project is that modernization does not begin with:

> “Let's use Kubernetes.”

or:

> “Let's move everything to cloud.”

It begins with understanding the customer problem.

Useful discovery questions include:

- What currently causes deployment failures?
- How often is the application released?
- How does rollback work today?
- What systems cannot move?
- What configuration changes between environments?
- What data needs to persist?
- What uptime is actually required?
- Which systems depend on the ERP?
- Who operates the application?
- What would make the modernization successful?

The project documentation distinguishes between:

- **KNOWN FOR CASE STUDY**
- **ASSUMED FOR POV**
- **MUST VALIDATE WITH CUSTOMER**

This keeps assumptions separate from confirmed requirements.

---

# Success criteria

A modernization effort should not be judged by:

> “Did we use cloud technology?”

It should be judged by whether it improved the problems that mattered.

The proof of value evaluates criteria such as:

- existing business behavior remains functional
- configuration can be externalized
- health is explicitly observable
- readiness is explicitly observable
- the container artifact builds successfully
- deployment configuration is reproducible
- Terraform configuration validates
- business logic remains separated from deployment mechanics
- the existing ERP can remain behind a clear integration boundary

The repository documents the validation status of these areas.

---

# Public portfolio experience

The live website is designed for both technical and non-technical visitors.

**Live demo:**  
https://hybrid-cloud-modernization-proof-of.vercel.app/

The public experience intentionally presents the project in layers.

A non-technical visitor can understand:

- what the problem is
- why the old model is difficult
- what modernization changes
- why Replatform was selected
- what the business gains

A technical visitor can go deeper into:

- Flask
- Docker
- OpenShift
- Terraform
- probes
- environment configuration
- persistence
- CI validation

The goal is **plain English first, technical detail second**.

---

# Interactive proof of value

The public frontend includes an interactive representation of the application and modernization flow.

The hosted website runs in deterministic browser mode.

This keeps the public portfolio:

- fast
- safe
- easy to explore
- independent from paid infrastructure
- understandable without requiring a cloud account

The hosted frontend is **not** a live OpenShift cluster.

The repository contains the implementation artifacts behind the architecture.

---

# Public demo vs repository

The two parts intentionally serve different purposes.

| Area | Public website | Repository |
|---|---|---|
| Modernization story | Yes | Yes |
| Legacy vs modernized comparison | Yes | Yes |
| Rehost / Replatform / Refactor | Yes | Yes |
| Interactive PoV | Browser demonstration | Application implementation |
| Health/readiness explanation | Yes | Implementation included |
| Docker | Explained | Docker artifact |
| OpenShift | Explained | Manifests included |
| Terraform | Explained | Configuration included |
| Automated tests | Results explained | Tests included |
| Live OpenShift cluster | No | Not executed |
| Terraform apply | No | Not executed |

---

# Technology stack

## Application

- Python
- Flask
- SQLAlchemy
- SQLite
- Gunicorn

## Containerization

- Docker

## Container-platform architecture

- Red Hat OpenShift
- Kubernetes-compatible resources

## Infrastructure as Code

- Terraform

## Frontend

- React
- Vite

## Validation

- Pytest
- GitHub Actions

---

# Validation

This project does more than provide architecture diagrams.

The implemented artifacts are automatically validated.

## Application tests

The project has a validated baseline of:

**22 passing tests**

These cover the legacy and modernized application behavior along with infrastructure-related validation.

---

# GitHub Actions

GitHub Actions provides a clean validation environment using Python 3.12.

The CI pipeline validates:

### Python application

**TESTED IN CI**

The application test suite runs successfully.

### Docker image

**TESTED IN CI**

The Docker image builds successfully.

### Terraform

**TESTED IN CI**

The workflow successfully performs:

```text
terraform fmt
terraform init
terraform validate
```

This gives the project stronger evidence than relying only on a local development machine.

---

# What was actually executed?

The project deliberately separates:

- implementation
- testing
- architecture
- execution

That prevents architecture diagrams from being presented as deployed infrastructure.

---

## IMPLEMENTED / TESTED

The project includes implemented artifacts for:

- legacy Flask application
- modernized Flask application
- SQLAlchemy persistence
- SQLite proof-of-value database
- environment configuration
- health endpoint
- readiness endpoint
- structured logging
- container definition
- OpenShift-compatible manifests
- Terraform configuration
- automated application/infrastructure tests
- public interactive frontend

---

## TESTED IN CI

The following were validated through GitHub Actions:

- Python 3.12 test suite
- Docker image build
- Terraform formatting
- Terraform initialization
- Terraform validation

---

## ARCHITECTED

The project includes architecture for:

- OpenShift application runtime
- hybrid cloud placement
- integration with an existing on-premises ERP
- future shared/external database
- infrastructure provisioning

---

## NOT EXECUTED

The project does **not** claim execution of:

- live OpenShift deployment
- live OpenShift rollback
- Terraform `apply`
- production PostgreSQL runtime
- IBM Cloud deployment
- real ERP integration

These limitations are intentional and documented.

---

# What this project demonstrates

## 1. Modernization strategy

Not every legacy application needs to be rewritten.

The modernization strategy should respond to the actual problem.

---

## 2. Business logic preservation

A useful application can keep its business capability while its operational environment is improved.

---

## 3. Containerization

The application can be packaged into a repeatable artifact instead of depending on a particular development machine.

---

## 4. Platform readiness

The project introduces concepts such as:

- health checks
- readiness
- configuration
- resource definitions
- security context
- network boundaries
- rollout strategy

that become important in an orchestrated environment.

---

## 5. Infrastructure as Code

Terraform turns platform configuration into something that can be:

- reviewed
- version-controlled
- repeated
- validated

---

## 6. Hybrid-cloud thinking

The architecture modernizes the application without pretending every existing enterprise system must move with it.

---

## 7. Technical communication

The public site explains concepts such as Docker, OpenShift, Terraform, and hybrid cloud without requiring the visitor to already be a cloud engineer.

---

# Why this is a Proof-of-Value

This is intentionally a **Proof-of-Value**, not a simulated claim of a completed enterprise migration.

The project asks:

- Can we preserve the business capability?
- Can configuration be separated from application code?
- Can operational health become visible?
- Can we build a repeatable container artifact?
- Can we describe deployment consistently?
- Can infrastructure be represented as code?
- Can the existing ERP remain part of the architecture?
- Can we validate the modernization artifacts before committing to a larger migration?

A PoV helps answer those questions before investing in a full modernization program.

---

# Key design principle

The project can be summarized in one sentence:

> **Modernize the operating model without rewriting business logic that still provides value.**

Or, more simply:

> **Keep the recipe. Modernize the kitchen.**

---

# Local development

The repository includes the legacy application, modernized application, infrastructure artifacts, tests, and public portfolio frontend.

Python target:

```text
3.12
```

The proof-of-value database uses SQLite by default.

The frontend is built with Vite and can be run with:

```bash
npm install
npm run dev
```

See the repository structure and project documentation for the relevant application-specific commands.

---

# Validation

Run the repository's Python validation from the appropriate project directory:

```bash
python -m pytest
```

Validated baseline:

```text
22 passed
```

Infrastructure validation is also performed by GitHub Actions.

---

# Current limitations

This project is a proof of value, not a production migration.

Current boundaries include:

- fictional customer scenario
- synthetic application data
- SQLite PoV persistence
- single-replica example deployment
- no live OpenShift cluster
- no production PostgreSQL runtime
- no executed Terraform apply
- no IBM Cloud deployment
- no real ERP connection
- public frontend uses deterministic browser execution
- no claim of production availability, scalability, or resilience

These limitations are documented rather than hidden.

---

# Project status at a glance

| Capability | Status |
|---|---|
| Legacy application | **IMPLEMENTED / TESTED** |
| Modernized application | **IMPLEMENTED / TESTED** |
| Environment-based configuration | **IMPLEMENTED / TESTED** |
| Health endpoint | **IMPLEMENTED / TESTED** |
| Readiness endpoint | **IMPLEMENTED / TESTED** |
| SQLite persistence | **IMPLEMENTED / TESTED** |
| Docker artifact | **IMPLEMENTED / TESTED IN CI** |
| OpenShift manifests | **IMPLEMENTED / STATICALLY VALIDATED** |
| Terraform configuration | **IMPLEMENTED / TESTED IN CI** |
| React portfolio demo | **IMPLEMENTED / DEPLOYED** |
| GitHub Actions | **IMPLEMENTED / PASSING** |
| OpenShift runtime deployment | **NOT EXECUTED** |
| Terraform apply | **NOT EXECUTED** |
| PostgreSQL runtime | **NOT EXECUTED** |
| IBM Cloud deployment | **NOT EXECUTED** |
| ERP integration | **ARCHITECTED / NOT EXECUTED** |

---

# About this project

I built this project to explore a practical modernization question:

> **How can an organization improve a legacy application's deployment and operating model without creating the cost and risk of an unnecessary rewrite?**

The result is an end-to-end proof of value combining:

- discovery
- modernization strategy
- application changes
- containerization
- OpenShift architecture
- Terraform
- hybrid-cloud design
- automated validation
- a public interactive explanation

The project is intentionally designed as a portfolio case study that can be understood by both technical and non-technical visitors.

The website explains the business problem first.

The repository preserves the technical depth behind it.

---

# Explore the project

### Live interactive demo

https://hybrid-cloud-modernization-proof-of.vercel.app/

### Source code

https://github.com/haisamar/hybrid-cloud-modernization-proof-of-value
