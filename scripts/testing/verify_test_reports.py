#!/usr/bin/env python3
# SPDX-License-Identifier: EPL-2.0
"""Require actual SDK test execution; reuse the pinned SWT JUnit parser.

This is a build-result check, not a coverage measurement or release approval.
Skipped tests remain separate from passing tests in the output.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

REQUIRED = (
    "eclipse.platform.swt/tests/org.eclipse.swt.tests/target/surefire-reports",
    "eclipse.platform.ui/tests/org.eclipse.jface.tests/target/surefire-reports",
    "eclipse.platform.ui/tests/org.eclipse.jface.m3.tests/target/surefire-reports",
    "eclipse.platform.ui/tests/org.eclipse.ui.tests/target/surefire-reports",
)
COUNTERS = ("tests", "failures", "errors", "skipped", "reports")


def load_junit_report(swt_root: Path):
    """Use the parser owned by the exact SWT submodule being built."""
    source = swt_root / "tools/release/readiness.py"
    spec = importlib.util.spec_from_file_location("swt_readiness", source)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load SWT test-report parser: " + str(source))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.junit_report


def verify(root: Path, junit_report) -> dict:
    root = root.resolve()
    directories = {path.parent for path in root.rglob("TEST-*.xml")
                   if path.parent.name == "surefire-reports"
                   and path.parent.parent.name == "target"}
    missing = [path for path in REQUIRED if root / path not in directories]
    if missing:
        raise ValueError("missing required test reports: " + ", ".join(missing))
    totals = dict.fromkeys(COUNTERS, 0)
    modules = []
    seen_files = set()
    for directory in sorted(directories):
        if any(parent.is_symlink() for parent in (directory, *directory.parents)
               if parent != root and root in parent.parents):
            raise ValueError("symlink in test-report directory: " + str(directory))
        counts = junit_report(directory, seen_files)
        if counts["failures"] or counts["errors"]:
            raise ValueError("failed tests: " + directory.relative_to(root).as_posix())
        for key in COUNTERS:
            totals[key] += counts[key]
        modules.append({"path": directory.relative_to(root).as_posix(),
                        **{key: counts[key] for key in COUNTERS}})
    return {"scope": "SDK reported test execution; not coverage or release approval",
            **totals, "passed": totals["tests"] - totals["skipped"],
            "modules": modules}


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    try:
        summary = verify(root, load_junit_report(root / "eclipse.platform.swt"))
    except (OSError, ValueError, AttributeError, ET.ParseError) as error:
        print("SDK test-report check failed: " + str(error), file=sys.stderr)
        return 1
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
