#!/usr/bin/env python3
"""HTTP smoke checks against a running Order Intake instance."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request


def request(base: str, method: str, path: str, body: dict | None = None) -> tuple[int, object]:
    data = None
    headers = {}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(base.rstrip("/") + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            return resp.status, payload
    except urllib.error.HTTPError as exc:
        payload = json.loads(exc.read().decode("utf-8")) if exc.fp else {}
        return exc.code, payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8080")
    parser.add_argument("--mode", choices=["legacy", "modernized"], default="modernized")
    args = parser.parse_args()
    base = args.base_url

    status, _ = request(base, "GET", "/")
    if status != 200:
        print("FAIL root", status)
        return 1

    status, created = request(
        base,
        "POST",
        "/orders",
        {"customer_id": "SMOKE-1", "sku": "SKU-SMOKE", "quantity": 1},
    )
    if status != 201:
        print("FAIL create", status)
        return 1
    order_id = created["id"]

    status, _ = request(base, "GET", f"/orders/{order_id}")
    if status != 200:
        print("FAIL retrieve", status)
        return 1

    status, _ = request(base, "POST", "/orders", {"customer_id": "X", "sku": "Y", "quantity": 0})
    if status != 400:
        print("FAIL invalid", status)
        return 1

    if args.mode == "modernized":
        status, health = request(base, "GET", "/health")
        if status != 200 or health.get("status") != "ok":
            print("FAIL health", status)
            return 1
        status, ready = request(base, "GET", "/ready")
        if status != 200:
            print("FAIL ready", status)
            return 1

    print("SMOKE OK", args.mode, base)
    return 0


if __name__ == "__main__":
    sys.exit(main())
