#!/usr/bin/env python3
"""Bump a spec file to the latest upstream GitHub release.

Only the Python standard library, git and the GitHub CLI (``gh``) are needed.
The script updates Version/Release, optional upstream tag and build-date macros,
and prepends a changelog entry. Source URLs are derived from macros, so they
follow the updated version automatically.
"""

from __future__ import annotations

import argparse
import datetime
import json
import locale
import re
import subprocess
import sys
from pathlib import Path

BOT_NAME = "github-actions[bot]"
BOT_EMAIL = "41898282+github-actions[bot]@users.noreply.github.com"


def gh_api(endpoint: str) -> dict:
    try:
        output = subprocess.check_output(["gh", "api", endpoint], text=True)
    except subprocess.CalledProcessError as exc:
        sys.exit(f"error: 'gh api {endpoint}' failed with exit code {exc.returncode}")
    return json.loads(output)


def replace_field(text: str, field: str, value: str) -> str:
    """Replace a header field such as ``Version:`` while keeping alignment."""
    pattern = rf"^{re.escape(field)}:.*$"
    replacement = f"{field}:".ljust(16) + value
    text, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        sys.exit(f"error: could not find a '{field}:' line")
    return text


def replace_macro(text: str, name: str, value: str) -> str:
    """Replace ``%global <name> ...`` when the macro is present."""
    pattern = rf"^%global\s+{re.escape(name)}\s+.*$"
    if not re.search(pattern, text, flags=re.MULTILINE):
        return text
    text, count = re.subn(
        pattern, f"%global {name} {value}", text, count=1, flags=re.MULTILINE
    )
    if count != 1:
        sys.exit(f"error: could not update the %global {name} macro")
    return text


def find_build_date(assets: list[dict]) -> str | None:
    """Extract the YYYYMMDD suffix from Linux release assets."""
    dates = set()
    for asset in assets:
        name = asset.get("name", "")
        if "linux-" not in name:
            continue
        match = re.search(r"_(20\d{6})\.", name)
        if match:
            dates.add(match.group(1))
    if len(dates) > 1:
        sys.exit(f"error: conflicting build dates in release assets: {sorted(dates)}")
    return dates.pop() if dates else None


def changelog_entry(version: str, tag: str) -> str:
    locale.setlocale(locale.LC_TIME, "C")
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%a %b %d %Y")
    return (
        f"* {today} {BOT_NAME} <{BOT_EMAIL}> - {version}-1\n"
        f"- Update to {tag}\n"
        "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path, help="spec file to update")
    parser.add_argument("--repo", required=True, help="upstream GitHub repository")
    parser.add_argument(
        "--tag-pattern",
        required=True,
        help="regex matched against the release tag; group 1 is the RPM version",
    )
    args = parser.parse_args()

    release = gh_api(f"repos/{args.repo}/releases/latest")
    tag = release["tag_name"]
    match = re.fullmatch(args.tag_pattern, tag)
    if match is None:
        print(f"warning: tag {tag!r} does not match {args.tag_pattern!r}; skipping")
        return 0
    version = match.group(1)

    text = args.spec.read_text(encoding="utf-8")
    current = re.search(r"^Version:\s*(\S+)", text, flags=re.MULTILINE)
    if current is None:
        sys.exit(f"error: {args.spec}: no Version line found")
    if current.group(1) == version:
        print(f"{args.spec}: already at {version}")
        return 0

    updated = replace_field(text, "Version", version)
    updated = replace_field(updated, "Release", "1%{?dist}")

    tag_version = tag[1:] if tag.startswith("v") else tag
    updated = replace_macro(updated, "upstream_tag", tag_version)

    build_date = find_build_date(release.get("assets", []))
    if re.search(r"^%global\s+build_date\b", updated, flags=re.MULTILINE):
        if build_date is None:
            sys.exit("error: spec uses %global build_date but no date was found")
        updated = replace_macro(updated, "build_date", build_date)

    updated, count = re.subn(
        r"^%changelog[^\n]*\n",
        lambda m: m.group(0) + changelog_entry(version, tag),
        updated,
        count=1,
        flags=re.MULTILINE,
    )
    if count != 1:
        sys.exit(f"error: {args.spec}: no %changelog section found")

    if updated == text:
        print(f"{args.spec}: no changes")
        return 0

    args.spec.write_text(updated, encoding="utf-8")
    print(f"{args.spec}: updated to {version} (tag {tag})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
