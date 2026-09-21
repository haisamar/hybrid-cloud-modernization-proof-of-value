# Before / after operating model

## BEFORE

Developer/Operator → copy code onto a host → change configuration manually →
start the process (`python app.py`) → verify in a browser or curl → diagnose
from the console on that machine → roll back by restoring files and restarting.

Pain in plain language: each environment is a little different, only some
people know the start ritual, and a bad release is a scavenger hunt rather
than a revision.

## AFTER (target)

Git change → versioned container image → configuration in ConfigMap/Secret →
OpenShift Deployment (`replicas: 1` for this SQLite PoV) → readiness and
liveness probes → rolling update → `oc rollout undo` to a prior revision.

Pain reduced: the same artifact and declared config are reused; an unready
pod should not take Service traffic; rollback is a platform action.

## What changed vs what did not

Changed: how the service is packaged, configured, started, observed, and
rolled back.

Unchanged: order fields, validation, create/list/get semantics, and the
decision that ERP remains on-prem.

## SQLite honesty

The after picture still uses SQLite on local/emptyDir storage. That is
acceptable for a replatform PoV of the **application operating model**.
It is **not** a production HA data tier. Pod replacement may lose
ephemeral data. Horizontal scaling needs shared persistence — out of
scope here.

## Execution honesty

The after model is **implemented as artifacts**. A live OpenShift rollout
was **not executed** on the implementation workstation (no `oc` / cluster).
