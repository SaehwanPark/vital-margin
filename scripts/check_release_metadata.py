#!/usr/bin/env python3
"""Check that the repository's public package version projections agree."""

import re
import sys
from pathlib import Path


VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
README_PATTERN = re.compile(r"playable Rust prototype at v(\d+\.\d+\.\d+)")
CHANGELOG_PATTERN = re.compile(r"^## \[(\d+\.\d+\.\d+)\]", re.MULTILINE)


def _package_version(cargo_toml):
  in_package = False
  for line in cargo_toml.splitlines():
    if line.startswith("["):
      in_package = line.strip() == "[package]"
    if in_package:
      match = re.fullmatch(r'version\s*=\s*"([^"]+)"', line.strip())
      if match:
        return match.group(1)
  return None


def _lockfile_version(cargo_lock):
  for block in cargo_lock.split("[[package]]")[1:]:
    if re.search(r'^name\s*=\s*"vital-margin"\s*$', block, re.MULTILINE):
      match = re.search(r'^version\s*=\s*"([^"]+)"\s*$', block, re.MULTILINE)
      return match.group(1) if match else None
  return None


def read_versions(root):
  cargo_toml = (root / "Cargo.toml").read_text(encoding="utf-8")
  cargo_lock = (root / "Cargo.lock").read_text(encoding="utf-8")
  readme = (root / "README.md").read_text(encoding="utf-8")
  changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
  readme_match = README_PATTERN.search(readme)
  changelog_match = CHANGELOG_PATTERN.search(changelog)
  return {
    "Cargo.toml": _package_version(cargo_toml),
    "Cargo.lock": _lockfile_version(cargo_lock),
    "README.md": readme_match.group(1) if readme_match else None,
    "CHANGELOG.md": changelog_match.group(1) if changelog_match else None,
  }


def validate_versions(versions):
  errors = []
  expected = versions.get("Cargo.toml")
  if expected is None:
    errors.append("Cargo.toml: missing [package] version")
  elif not VERSION_PATTERN.fullmatch(expected):
    errors.append(f"Cargo.toml: invalid package version {expected!r}")

  for path, actual in versions.items():
    if actual is None:
      errors.append(f"{path}: expected a version projection")
    elif expected is not None and actual != expected:
      errors.append(f"{path}: found {actual!r}; expected {expected!r}")
  return errors


def main():
  root = Path(__file__).resolve().parents[1]
  versions = read_versions(root)
  errors = validate_versions(versions)
  if errors:
    for error in errors:
      print(f"error: {error}", file=sys.stderr)
    return 1
  print(f"release metadata check: passed ({versions['Cargo.toml']})")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
