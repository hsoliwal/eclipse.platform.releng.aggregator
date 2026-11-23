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

# Explicitly opt-in for the E4/JFace receiver candidates. Legacy SDK verification
# remains unchanged unless --require-e4-jface is supplied by a native CI lane.
E4_REPORT = "eclipse.platform.ui/tests/org.eclipse.e4.ui.tests/target/surefire-reports"
JFACE_REPORT = "eclipse.platform.ui/tests/org.eclipse.jface.tests/target/surefire-reports"
NATIVE_UI_CONTRACTS = {
    E4_REPORT: frozenset({
        ("org.eclipse.e4.ui.tests.workbench.DisplayUISynchronizeAdmissionTest",
         name)
        for name in (
            "missingOrDisposedDisplayRejectsWithoutPosting",
            "liveSubmissionAcknowledgesAndPreservesLegacyAsyncExec",
            "disposedDuringAdmissionRefusesButLegacyPathStillThrows",
            "unrelatedSwtSubmissionFailurePropagatesExactly",
            "e4JobRefusalReturnsTerminalCancelWithoutInvokingUiBody",
            "e4JobAcceptedCallbackRemainsAsynchronous",
            "e4JobDispositionRaceReturnsTerminalCancel",
            "e4JobRetainsCustomSynchronizerDispatchContract",
            "refusedSubmissionCompletesOnceThroughJobManager",
            "acceptedJobCompletesOnNativeDisplayExactlyOnce",
        )
    }),
    JFACE_REPORT: frozenset({
        ("org.eclipse.jface.tests.viewers.m3.M3ViewersTest",
         "failedObsoleteBatchCannotRefreshReplacementInput"),
        ("org.eclipse.jface.tests.viewers.m3.M3ViewersTest",
         "failingCurrentGenerationStillUsesExistingRefreshFallback"),
    }),
}


def verify_native_ui_contract_cases(root: Path) -> dict:
    """Reject missing/skipped/failed/duplicate native UI contract test cases.

    This verifies report contents, not the identity, freshness, or provenance
    of the build that generated them; CI must pin the tested checkout itself.
    """
    checked = {}
    for directory, required in NATIVE_UI_CONTRACTS.items():
        actual = root / directory
        observed = set()
        for report in sorted(actual.glob("TEST-*.xml")):
            suite = ET.parse(report).getroot()
            for case in suite.iter("testcase"):
                identity = (case.get("classname"), case.get("name"))
                if identity not in required:
                    continue
                if identity in observed:
                    raise ValueError("duplicate required UI case: " + repr(identity))
                if any(case.find(tag) is not None
                       for tag in ("skipped", "failure", "error")):
                    raise ValueError("skipped or failed required UI case: " + repr(identity))
                observed.add(identity)
        missing = sorted(required - observed)
        if missing:
            raise ValueError("missing required UI cases in " + directory + ": " + repr(missing))
        checked[directory] = len(observed)
    return checked




def load_junit_report(swt_root: Path):
    """Use the parser owned by the exact SWT submodule being built."""
    source = swt_root / "tools/release/readiness.py"
    spec = importlib.util.spec_from_file_location("swt_readiness", source)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load SWT test-report parser: " + str(source))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.junit_report


def verify(root: Path, junit_report, require_e4_jface: bool = False) -> dict:
    root = root.resolve()
    directories = {path.parent for path in root.rglob("TEST-*.xml")
                   if path.parent.name == "surefire-reports"
                   and path.parent.parent.name == "target"}
    required_directories = REQUIRED + ((E4_REPORT,) if require_e4_jface else ())
    missing = [path for path in required_directories if root / path not in directories]
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
    result = {"scope": "SDK reported test execution; not coverage or release approval",
              **totals, "passed": totals["tests"] - totals["skipped"],
              "modules": modules}
    if require_e4_jface:
        result["required_ui_contract_cases"] = verify_native_ui_contract_cases(root)
    return result


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Verify executed SDK test reports")
    parser.add_argument("--require-e4-jface", action="store_true",
                        help="also require 10 E4 UIJob and 2 JFace native test cases")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    try:
        summary = verify(root, load_junit_report(root / "eclipse.platform.swt"),
                         require_e4_jface=args.require_e4_jface)
    except (OSError, ValueError, AttributeError, ET.ParseError) as error:
        print("SDK test-report check failed: " + str(error), file=sys.stderr)
        return 1
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
