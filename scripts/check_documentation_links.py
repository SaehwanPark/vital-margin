#!/usr/bin/env python3
"""Check repository Markdown links and contributor documentation entry points."""

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_PATHS = (
  "docs/README.md",
  "docs/proposal.md",
  "docs/roadmap.md",
  "docs/design_principles.md",
  "SPEC.md",
  "ARCHITECTURE.md",
  "docs/visual_audio_enhancement_roadmap.md",
  "docs/decision-records/0014-ai-native-gui-and-browser-boundary.md",
  "docs/harness/vital-margin/team-spec.md",
)
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
MACHINE_LOCAL_PATH = re.compile(r"file:///|/(?:Users|home)/[^/\s]+/")


def tracked_markdown_files(root):
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


def _link_target(raw_target):
  target = raw_target.strip()
  if target.startswith("<"):
    closing = target.find(">")
    return target[1:closing] if closing >= 0 else target[1:]
  return target.split(maxsplit=1)[0] if target else ""


def check_markdown_file(path, root):
  relative_path = path.relative_to(root)
  content = path.read_text(encoding="utf-8")
  issues = []

  for match in MACHINE_LOCAL_PATH.finditer(content):
    line = content.count("\n", 0, match.start()) + 1
    issues.append(f"{relative_path}:{line}: machine-local path")

  for match in MARKDOWN_LINK.finditer(content):
    target = _link_target(match.group(1))
    if not target or target.startswith("#"):
      continue
    parsed = urlsplit(target)
    if parsed.scheme:
      continue
    local_target = unquote(parsed.path)
    if not local_target:
      continue
    if Path(local_target).is_absolute():
      line = content.count("\n", 0, match.start()) + 1
      issues.append(f"{relative_path}:{line}: absolute local link {target}")
      continue
    resolved = (path.parent / local_target).resolve()
    if not resolved.exists():
      line = content.count("\n", 0, match.start()) + 1
      issues.append(f"{relative_path}:{line}: missing local link {target}")

  return issues


def check_repository(root=ROOT):
  issues = []
  for relative_path in CANONICAL_PATHS:
    if not (root / relative_path).is_file():
      issues.append(f"{relative_path}: missing canonical documentation")
  for path in tracked_markdown_files(root):
    issues.extend(check_markdown_file(path, root))
  return issues


def main():
  issues = check_repository()
  if issues:
    for issue in issues:
      print(f"error: {issue}", file=sys.stderr)
    return 1
  count = len(tracked_markdown_files(ROOT))
  print(f"documentation link check: passed ({count} Markdown files)")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
