#!/usr/bin/env python3
"""Detect local tools. Results change allowed status claims."""

from __future__ import annotations

import shutil
import subprocess
import sys


TOOLS = [
    ["python", "--version"],
    ["docker", "--version"],
    ["podman", "--version"],
    ["terraform", "version"],
    ["oc", "version"],
    ["kubectl", "version", "--client"],
    ["node", "--version"],
    ["npm", "--version"],
]


def run(cmd: list[str]) -> tuple[bool, str]:
    executable = shutil.which(cmd[0])
    if not executable:
        return False, "NOT FOUND"
    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        output = (completed.stdout or completed.stderr).strip().splitlines()
        first = output[0] if output else f"exit {completed.returncode}"
        return completed.returncode == 0 or bool(output), first
    except OSError as exc:
        return False, str(exc)


def main() -> int:
    print("Environment detection")
    print("=====================")
    for cmd in TOOLS:
        ok, detail = run(cmd)
        status = "PRESENT" if ok else "ABSENT"
        print(f"{cmd[0]:12} {status:8} {detail}")
    print()
    print("Claim rules")
    print("-----------")
    print("python present     -> application tests may be TESTED")
    print("docker/podman absent -> Dockerfile IMPLEMENTED; image NOT EXECUTED")
    print("terraform absent   -> configuration IMPLEMENTED; validate NOT EXECUTED")
    print("oc/kubectl absent  -> manifests IMPLEMENTED; deployment NOT EXECUTED")
    print("node/npm present   -> portfolio-demo build may be TESTED")
    print("CI planned         -> does not by itself make Docker/Terraform TESTED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
