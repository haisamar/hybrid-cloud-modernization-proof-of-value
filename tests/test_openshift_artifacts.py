from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OS_DIR = ROOT / "deploy" / "openshift"


def _read(name: str) -> str:
    return (OS_DIR / name).read_text(encoding="utf-8")


def test_probes_present():
    text = _read("deployment.yaml")
    assert "readinessProbe:" in text
    assert "path: /ready" in text
    assert "livenessProbe:" in text
    assert "path: /health" in text


def test_resources_present():
    text = _read("deployment.yaml")
    assert "requests:" in text
    assert "limits:" in text
    assert "cpu:" in text
    assert "memory:" in text


def test_config_and_secret_references():
    text = _read("deployment.yaml")
    assert "configMapRef:" in text
    assert "order-intake-config" in text
    assert "secretRef:" in text
    assert "order-intake-secrets" in text


def test_non_root_security_context():
    text = _read("deployment.yaml")
    assert "runAsNonRoot: true" in text
    assert "allowPrivilegeEscalation: false" in text


def test_replicas_is_one_for_sqlite():
    text = _read("deployment.yaml")
    assert "replicas: 1" in text
    assert "emptyDir" in text


def test_route_is_openshift():
    text = _read("route.yaml")
    assert "apiVersion: route.openshift.io/v1" in text
    assert "kind: Route" in text


def test_secret_values_are_placeholders():
    text = _read("secret.yaml")
    assert "CHANGE_ME" in text
    assert "password123" not in text.lower()
    assert "BEGIN" not in text


def test_networkpolicy_is_documented_as_example():
    text = _read("networkpolicy.yaml")
    assert "EXAMPLE BASELINE" in text
    assert "cluster-specific" in text
