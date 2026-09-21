#!/usr/bin/env python3
"""Run what can genuinely be validated on this workstation."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], cwd: Path | None = None) -> int:
    print("+", " ".join(cmd))
    completed = subprocess.run(cmd, cwd=cwd or ROOT)
    return completed.returncode


def main() -> int:
    detect = run([sys.executable, str(ROOT / "scripts" / "detect_environment.py")])
    suites = [
        ["legacy-app/tests"],
        ["modernized-app/tests"],
        ["tests"],
    ]
    test_rc = 0
    for suite in suites:
        rc = run([sys.executable, "-m", "pytest", *suite, "-q"])
        if rc != 0:
            test_rc = rc
    print()
    print("Docker/Podman image build: skipped unless those binaries exist.")
    print("terraform fmt/validate: skipped unless terraform exists.")
    print("oc apply / rollout: skipped unless a cluster exists.")
    print("Do not update TESTED flags from planned CI; only from observed runs.")
    return 0 if detect == 0 and test_rc == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
