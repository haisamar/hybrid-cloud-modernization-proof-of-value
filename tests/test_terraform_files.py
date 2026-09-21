from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TF_DIR = ROOT / "infra" / "terraform"

REQUIRED = [
    "versions.tf",
    "providers.tf",
    "variables.tf",
    "main.tf",
    "outputs.tf",
    "terraform.tfvars.example",
    "README.md",
]


def test_required_terraform_files_exist():
    for name in REQUIRED:
        assert (TF_DIR / name).is_file(), name


def test_version_constraints_present():
    text = (TF_DIR / "versions.tf").read_text(encoding="utf-8")
    assert "required_version" in text
    assert "hashicorp/kubernetes" in text
    assert "~> 2.32" in text


def test_gitignore_excludes_state():
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".terraform/" in gitignore
    assert "*.tfstate" in gitignore
    assert "!terraform.tfvars.example" in gitignore
