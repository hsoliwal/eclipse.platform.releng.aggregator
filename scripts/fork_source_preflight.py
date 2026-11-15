#!/usr/bin/env python3
"""Read-only, fail-closed source/gitlink closure gate for the fork aggregator.

This is a SOURCE gate, not build, runtime, provenance or release admission.
"""

from __future__ import annotations

import argparse
import configparser
import json
import re
import subprocess
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

SCHEMA = "SYNEXIA_FORK_SOURCE_CLOSURE_V1"
EXPECTED = {
    "eclipse.jdt": ("eclipse.jdt", "master"),
    "eclipse.jdt.core": ("eclipse.jdt.core", "master"),
    "eclipse.jdt.core.binaries": ("eclipse.jdt.core.binaries", "master"),
    "eclipse.jdt.debug": ("eclipse.jdt.debug", "master"),
    "eclipse.jdt.ui": ("eclipse.jdt.ui", "master"),
    "eclipse.pde": ("initiative31-eclipse.pde", "master"),
    "eclipse.platform": ("eclipse.platform", "master"),
    "eclipse.platform.swt": ("eclipse.platform.swt", "master"),
    "eclipse.platform.ui": ("eclipse.platform.ui", "master"),
    "equinox": ("equinox", "master"),
    "equinox.binaries": ("equinox.binaries", "master"),
    "equinox.p2": ("p2", "master"),
}
# This pinned repository supplies native artifacts to Equinox reactor modules.
NON_REACTOR_INPUTS = frozenset({"equinox.binaries"})
SHA_RE = re.compile(r"[0-9a-f]{40}\Z")


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def inspect(root: Path, *, require_checkout: bool = False) -> dict:
    root = root.resolve()
    errors: list[str] = []
    records: list[dict] = []
    parent_sha = None

    try:
        parent_sha = git(root, "rev-parse", "HEAD")
        if not SHA_RE.fullmatch(parent_sha):
            errors.append("Parent HEAD is not a lowercase 40-character Git commit")
        dirty = git(root, "status", "--porcelain", "--untracked-files=no", "--", ".gitmodules", "pom.xml")
        if dirty:
            errors.append("Tracked source anchors differ from HEAD: .gitmodules or pom.xml")
    except (OSError, subprocess.CalledProcessError) as exc:
        errors.append(f"Cannot inspect parent Git checkout: {type(exc).__name__}")

    configured: dict[str, tuple[str | None, str | None]] = {}
    try:
        parser = configparser.ConfigParser(interpolation=None, strict=True)
        with (root / ".gitmodules").open(encoding="utf-8") as handle:
            parser.read_file(handle)
        for section in parser.sections():
            match = re.fullmatch(r'submodule "([^"\\]+)"', section)
            if match is None:
                errors.append(f"Unexpected .gitmodules section: {section}")
                continue
            path = match.group(1)
            configured[path] = (parser.get(section, "url", fallback=None),
                                parser.get(section, "branch", fallback=None))
            if parser.has_option(section, "path") and parser.get(section, "path") != path:
                errors.append(f"Submodule section/path mismatch: {path}")
            if set(parser.options(section)) != {"path", "url", "branch"}:
                errors.append(f"Submodule metadata keys differ from v1 contract: {path}")
    except (OSError, configparser.Error) as exc:
        errors.append(f"Cannot parse .gitmodules: {type(exc).__name__}")

    try:
        pom_root = ET.parse(root / "pom.xml").getroot()
        reactor = {"".join(m.itertext()).strip().rstrip("/")
                   for m in pom_root.findall("./{*}modules/{*}module")}
    except (OSError, ET.ParseError) as exc:
        reactor = set()
        errors.append(f"Cannot parse pom.xml reactor: {type(exc).__name__}")

    for unexpected in sorted(set(configured) - set(EXPECTED)):
        errors.append(f"Unexpected submodule section: {unexpected}")

    for path, (repo, branch) in sorted(EXPECTED.items()):
        expected_url = f"https://github.com/hsoliwal/{repo}.git"
        url, configured_branch = configured.get(path, (None, None))
        if path not in configured:
            errors.append(f"Missing submodule section: {path}")
        if url != expected_url:
            errors.append(f"Unexpected fork URL for {path}: {url!r}")
        if configured_branch != branch:
            errors.append(f"Unexpected tracking branch for {path}: {configured_branch!r}")
        if path in NON_REACTOR_INPUTS:
            if path in reactor:
                errors.append(f"Non-reactor binary input is declared as Maven module: {path}")
        elif path not in reactor:
            errors.append(f"Missing Maven reactor module: {path}")

        pin = None
        try:
            entry = git(root, "ls-tree", "HEAD", "--", path)
            match = re.fullmatch(r"160000 commit ([0-9a-f]{40})\t" + re.escape(path), entry)
            if match is None:
                errors.append(f"Missing/invalid committed gitlink: {path}")
            else:
                pin = match.group(1)
        except (OSError, subprocess.CalledProcessError):
            errors.append(f"Cannot inspect committed gitlink: {path}")

        if require_checkout and pin:
            checkout = root / path
            try:
                observed = git(checkout, "rev-parse", "HEAD")
                if observed != pin:
                    errors.append(f"Checkout HEAD differs from gitlink: {path}")
            except (OSError, subprocess.CalledProcessError):
                errors.append(f"Uninitialized or unreadable checkout: {path}")

        records.append({"path": path, "repository": f"hsoliwal/{repo}",
                        "branch": branch, "gitlink_sha": pin})

    return {
        "schema": SCHEMA,
        "aggregator_sha": parent_sha,
        "submodules": records,
        "require_checkout": require_checkout,
        "source_closure_passed": not errors,
        "release_admitted": False,
        "errors": errors,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--require-checkout", action="store_true")
    args = ap.parse_args(argv)
    result = inspect(args.root, require_checkout=args.require_checkout)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["source_closure_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
