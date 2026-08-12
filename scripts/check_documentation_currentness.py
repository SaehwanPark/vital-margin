#!/usr/bin/env python3
"""Classify Markdown roles and enforce the current documentation contract.

This checker deliberately audits only current-facing invariants. Historical
reports, accepted ADR bodies, generated registries, and versioned workspace
evidence may contain older wording and are classified rather than rewritten.
"""

from __future__ import annotations

import subprocess
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROLES = ("maintained", "generated", "historical", "ADR", "workspace")
GENERATED_PATHS = {
  "assets/ASSET_CREDITS.md",
  "assets/THIRD_PARTY_NOTICES.md",
  "gui/ASSET_CREDITS.md",
}

CURRENT_FILES = {
  "README.md": (
    "stabilization-v1",
    "competitive-regional-v1",
    "regional-affiliation-v1",
    "Chromium evergreen",
    "deferred",
  ),
  "SPEC.md": ("## Past", "## Present", "## Future", "GUI-focused documentation"),
  "ARCHITECTURE.md": (
    "## Loopback GUI host",
    "durable",
    "## Browser support boundary",
    "Chromium evergreen",
  ),
  "docs/README.md": (
    "Maintained",
    "Generated",
    "Historical",
    "ADR",
    "Workspace",
    "Codex in-app browser",
  ),
  "docs/roadmap.md": ("## Current position", "## GUI-first queue", "AI-native", "deferred"),
  "docs/visual_audio_enhancement_roadmap.md": (
    "## Current implemented baseline",
    "## Ranked active queue",
    "agent-executable",
    "Chromium evergreen",
    "## Phase 9:",
    "## Phase 10:",
  ),
  "docs/decision-records/README.md": ("ADR-0014", "Historical numbering note"),
  "docs/decision-records/0014-ai-native-gui-and-browser-boundary.md": (
    "AI-native",
    "Chromium evergreen",
    "optional external feedback",
  ),
  "gui/README.md": (
    "## Authority and presentation state",
    "campaign-coverage-v1",
    "text-first",
    "deferred and non-certified",
  ),
  "docs/validation/playtesting.md": (
    "Active agent-playtest",
    "regional-affiliation-v1",
    "optional external feedback",
  ),
  "docs/reference/mcp-agent-interface.md": (
    "regional-affiliation-v1",
    "checkpoint archives",
    "actor-visible",
  ),
  "docs/harness/vital-margin/team-spec.md": (
    "reference CLI",
    "host-backed loopback GUI",
    "AI-native",
  ),
}

FORBIDDEN_CURRENT_CLAIMS = {
  "README.md": ("competitive-only", "GUI thin-client proof"),
  "ARCHITECTURE.md": ("sessions in memory", "competitive GUI path only"),
  "SPEC.md": ("competitive-only", "GUI thin-client proof"),
  "docs/roadmap.md": ("pending human evidence", "human approval gate"),
  "docs/visual_audio_enhancement_roadmap.md": (
    "pending human evidence",
    "human approval gate",
    "release blocked",
  ),
  "gui/README.md": (
    "pending the authorized five-group pilot",
    "evidence gate is met",
    "competitive-only",
  ),
}


def tracked_markdown_files(root: Path = ROOT) -> list[Path]:
  result = subprocess.run(
    [
      "git",
      "-C",
      str(root),
      "ls-files",
      "--cached",
      "--others",
      "--exclude-standard",
      "--",
      "*.md",
    ],
    check=True,
    capture_output=True,
    text=True,
  )
  return [
    root / line
    for line in result.stdout.splitlines()
    if line and (root / line).is_file()
  ]


def classify_markdown(path: Path, root: Path = ROOT) -> str:
  relative = path.relative_to(root).as_posix()
  if relative in GENERATED_PATHS:
    return "generated"
  if relative.startswith("docs/history/"):
    return "historical"
  if relative.startswith("docs/evaluation/"):
    return "historical"
  if relative.startswith("docs/blog-posts/"):
    return "historical"
  if relative.startswith("_workspace/"):
    return "workspace"
  if relative.startswith("docs/decision-records/"):
    return "ADR"
  return "maintained"


def check_repository(root: Path = ROOT) -> tuple[list[str], Counter[str]]:
  issues: list[str] = []
  files = tracked_markdown_files(root)
  counts: Counter[str] = Counter()

  for path in files:
    relative = path.relative_to(root).as_posix()
    role = classify_markdown(path, root)
    if role not in ROLES:
      issues.append(f"{relative}: unclassified Markdown role {role!r}")
      continue
    counts[role] += 1
    if role != "maintained":
      continue
    text = path.read_text(encoding="utf-8")
    for marker in CURRENT_FILES.get(relative, ()):
      if marker not in text:
        issues.append(f"{relative}: missing currentness marker {marker!r}")
    # A maintained document may retain a clearly labeled point-in-time
    # compatibility index.  Enforce stale-claim checks on its current-facing
    # section while allowing historical evidence labels to remain verbatim.
    current_text = text
    if relative == "docs/visual_audio_enhancement_roadmap.md":
      current_text = text.split("## Historical technical evidence index", 1)[0]
    lowered = current_text.lower()
    for forbidden in FORBIDDEN_CURRENT_CLAIMS.get(relative, ()):
      if forbidden.lower() in lowered:
        issues.append(f"{relative}: stale current-state claim {forbidden!r}")

  for relative in CURRENT_FILES:
    if not (root / relative).is_file():
      issues.append(f"{relative}: current maintained document is missing")

  return issues, counts


def main() -> int:
  issues, counts = check_repository()
  if issues:
    for issue in issues:
      print(f"error: {issue}", file=sys.stderr)
    return 1
  summary = ", ".join(f"{role}={counts[role]}" for role in ROLES)
  print(f"documentation currentness check: passed ({summary})")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
