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
import subprocess
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





# Exact source identities qualified by the two prior receiver recipes. The
# strict native runner checks its OWN checkout before Maven, not just a
# separate source-pins job, so it cannot silently compile another revision.
NATIVE_SOURCE_PINS = {
    "eclipse.platform.ui": "a6fa7796f150149eea123445fac4808dd14b3b3f",
    "eclipse.platform.swt": "51a70dad3ea1d4ede76ab74e79b42926b82b4857",
}
REVIEWED_UI_SOURCE_BLOBS = {
    "bundles/org.eclipse.e4.ui.progress/META-INF/MANIFEST.MF": "2be41b1fa3a8817f75f0a82b864e8878f79f25b0",
    "bundles/org.eclipse.e4.ui.progress/src/org/eclipse/e4/ui/progress/UIJob.java": "3c389b7dc04e00e3ec62366066411addff7ff6df",
    "bundles/org.eclipse.e4.ui.workbench.swt/META-INF/MANIFEST.MF": "06ff2021d9949ea2b8cd8bee0d50201668b56321",
    "bundles/org.eclipse.e4.ui.workbench.swt/src/org/eclipse/e4/ui/workbench/swt/DisplayUISynchronize.java": "9ce0c8c1d12d76e5d731e780d14aaf045644338d",
    "tests/org.eclipse.e4.ui.tests/META-INF/MANIFEST.MF": "9b3a261ae26654e82a007a9e274f5f3f7e7ee629",
    "tests/org.eclipse.e4.ui.tests/src/org/eclipse/e4/ui/tests/UIAllTests.java": "7a172578815787633d73686211ff4299427ee66b",
    "tests/org.eclipse.e4.ui.tests/src/org/eclipse/e4/ui/tests/workbench/DisplayUISynchronizeAdmissionTest.java": "297bf08cb1367349445c70fd29c83c22196229c1",
    "bundles/org.eclipse.jface/src/org/eclipse/jface/viewers/m3/M3Viewers.java": "e2cff7acddde8b3771754e17d455562a6a1e2bca",
    "tests/org.eclipse.jface.tests/src/org/eclipse/jface/tests/viewers/m3/M3ViewersTest.java": "2edfa76cc55d4ff7a929086ea04672bf5780c831",
}


def _git_text(directory: Path, *args: str) -> str:
    """Read local Git metadata only; never fetch or mutate source."""
    try:
        return subprocess.check_output(
            ["git", "-C", str(directory), *args],
            text=True, stderr=subprocess.PIPE).strip()
    except (OSError, subprocess.CalledProcessError) as error:
        raise ValueError("native checkout Git inspection failed: " + str(args)) from error


def verify_native_source_checkout(root: Path, *, pins=None, ui_blobs=None) -> dict:
    """Require that the current build runner materialized EXACT reviewed inputs.

    Production CLI uses the immutable defaults. Optional pin maps permit small,
    real-Git unit fixtures without constructing the nine proprietary sources.
    This is source-provenance verification, NOT native test execution.
    """
    pins = NATIVE_SOURCE_PINS if pins is None else pins
    ui_blobs = REVIEWED_UI_SOURCE_BLOBS if ui_blobs is None else ui_blobs
    root = root.resolve()
    if Path(_git_text(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise ValueError("SDK checkout must be its own Git worktree root")
    result = {"sdk_commit": _git_text(root, "rev-parse", "HEAD"),
              "pinned_submodules": {}, "reviewed_ui_blobs": 0}
    for name, expected in sorted(pins.items()):
        directory = root / name
        if directory.is_symlink() or not directory.is_dir():
            raise ValueError("native checkout missing or linked submodule: " + name)
        actual = _git_text(root, "ls-tree", "HEAD", "--", name)
        if actual != f"160000 commit {expected}\t{name}":
            raise ValueError("native SDK gitlink mismatch: " + name)
        if Path(_git_text(directory, "rev-parse", "--show-toplevel")).resolve() != directory:
            raise ValueError("native submodule is not its own checkout: " + name)
        checked = _git_text(directory, "rev-parse", "HEAD")
        if checked != expected:
            raise ValueError("native submodule checkout differs from Gitlink: " + name)
        if _git_text(directory, "status", "--porcelain=v1", "--untracked-files=all"):
            raise ValueError("native submodule has uncommitted changes: " + name)
        result["pinned_submodules"][name] = checked
    ui_dir = root / "eclipse.platform.ui"
    for path, blob in sorted(ui_blobs.items()):
        actual = _git_text(ui_dir, "ls-tree", "HEAD", "--", path)
        if actual != f"100644 blob {blob}\t{path}":
            raise ValueError("reviewed UI source blob mismatch: " + path)
    result["reviewed_ui_blobs"] = len(ui_blobs)
    return result


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
    parser.add_argument("--check-native-source", action="store_true",
                        help="before Maven, require exact Gitlinks, checked-out SHAs and nine UI owner blobs")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    try:
        if args.check_native_source:
            summary = verify_native_source_checkout(root)
        else:
            summary = verify(root, load_junit_report(root / "eclipse.platform.swt"),
                             require_e4_jface=args.require_e4_jface)
    except (OSError, ValueError, AttributeError, ET.ParseError) as error:
        print("SDK test-report check failed: " + str(error), file=sys.stderr)
        return 1
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
