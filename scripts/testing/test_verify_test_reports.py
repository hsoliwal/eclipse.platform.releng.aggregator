#!/usr/bin/env python3
# SPDX-License-Identifier: EPL-2.0
"""Regression cases for SDK report admission, using the actual SWT parser."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from verify_test_reports import (E4_REPORT, JFACE_REPORT, NATIVE_UI_CONTRACTS,
                                 REQUIRED, load_junit_report, verify, verify_native_source_checkout)

ROOT = Path(__file__).resolve().parents[2]
PARSE = load_junit_report(Path(os.environ.get("SWT_SOURCE", ROOT / "eclipse.platform.swt")))
PASS = '<testsuite tests="1" failures="0" errors="0" skipped="0"><testcase name="ok"/></testsuite>'


class TestSdkReports(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for directory in REQUIRED:
            self.write(directory, PASS)

    def write(self, directory, xml, name="TEST-suite.xml"):
        path = self.root / directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(xml, encoding="utf-8")
        return path

    def test_all_required_components_execute(self):
        result = verify(self.root, PARSE)
        self.assertEqual(result["passed"], 4)
        self.assertEqual(result["skipped"], 0)

    def test_each_required_component_is_mandatory(self):
        for directory in REQUIRED:
            with self.subTest(directory=directory):
                path = self.root / directory / "TEST-suite.xml"
                path.unlink()
                with self.assertRaisesRegex(ValueError, "missing required"):
                    verify(self.root, PARSE)
                self.write(directory, PASS)

    def test_empty_report_is_not_execution(self):
        self.write(REQUIRED[0], '<testsuite tests="0"/>')
        with self.assertRaisesRegex(ValueError, "no executed"):
            verify(self.root, PARSE)

    def test_all_skipped_component_is_rejected(self):
        self.write(REQUIRED[0], '<testsuite tests="1" skipped="1"><testcase name="ignored"><skipped/></testcase></testsuite>')
        with self.assertRaisesRegex(ValueError, "all skipped"):
            verify(self.root, PARSE)

    def test_skipped_cases_are_not_counted_as_passed(self):
        self.write(REQUIRED[0], '<testsuite tests="2" skipped="1"><testcase name="ok"/><testcase name="ignored"><skipped/></testcase></testsuite>')
        result = verify(self.root, PARSE)
        self.assertEqual((result["tests"], result["passed"], result["skipped"]), (5, 4, 1))

    def test_failures_and_errors_are_rejected(self):
        for tag in ("failure", "error"):
            with self.subTest(tag=tag):
                self.write(REQUIRED[0], f'<testsuite tests="1"><testcase name="bad"><{tag}/></testcase></testsuite>')
                with self.assertRaisesRegex(ValueError, "failed tests"):
                    verify(self.root, PARSE)

    def test_other_reactor_module_failure_is_rejected(self):
        self.write("eclipse.jdt.core/tests/target/surefire-reports", '<testsuite tests="1"><testcase name="bad"><failure/></testcase></testsuite>')
        with self.assertRaisesRegex(ValueError, "failed tests"):
            verify(self.root, PARSE)

    def test_report_counters_must_match_cases(self):
        self.write(REQUIRED[0], '<testsuite tests="99"><testcase name="ok"/></testsuite>')
        with self.assertRaisesRegex(ValueError, "counter mismatch"):
            verify(self.root, PARSE)

    def test_nested_rollup_is_counted_once(self):
        self.write(REQUIRED[0], '<testsuites tests="1"><testsuite tests="1"><testcase name="ok"/></testsuite></testsuites>')
        self.assertEqual(verify(self.root, PARSE)["passed"], 4)

    def test_malformed_report_is_rejected(self):
        from xml.etree.ElementTree import ParseError
        self.write(REQUIRED[0], "<testsuite>")
        with self.assertRaises(ParseError):
            verify(self.root, PARSE)

    def test_duplicate_hardlinked_report_is_rejected(self):
        source = self.root / REQUIRED[0] / "TEST-suite.xml"
        target = self.root / REQUIRED[1] / "TEST-copy.xml"
        os.link(source, target)
        with self.assertRaisesRegex(ValueError, "duplicate/aliased"):
            verify(self.root, PARSE)

    @unittest.skipIf(os.name == "nt", "Windows symlinks require optional privileges")
    def test_symlink_report_is_rejected(self):
        source = self.root / REQUIRED[0] / "TEST-suite.xml"
        target = self.root / REQUIRED[1] / "TEST-copy.xml"
        target.symlink_to(source)
        with self.assertRaisesRegex(ValueError, "symlink"):
            verify(self.root, PARSE)


    def write_contracts(self, omitted=None, skipped=None, duplicate=None):
        from xml.etree import ElementTree as ET
        omitted = omitted or set()
        for directory, required in NATIVE_UI_CONTRACTS.items():
            cases = sorted(required - omitted)
            suite = ET.Element("testsuite", tests=str(len(cases)), failures="0",
                               errors="0", skipped=str(int(skipped in cases)))
            for classname, name in cases:
                element = ET.SubElement(suite, "testcase", classname=classname,
                                        name=name)
                if (classname, name) == skipped:
                    ET.SubElement(element, "skipped")
            self.write(directory, ET.tostring(suite, encoding="unicode"),
                       name="TEST-source-contracts.xml")
            if duplicate and directory == duplicate[0]:
                dup = ET.Element("testsuite", tests="1", failures="0",
                                 errors="0", skipped="0")
                ET.SubElement(dup, "testcase", classname=duplicate[1][0],
                              name=duplicate[1][1])
                self.write(directory, ET.tostring(dup, encoding="unicode"),
                           name="TEST-duplicate-contract.xml")

    def test_strict_e4_jface_accepts_twelve_named_methods(self):
        self.write_contracts()
        report = verify(self.root, PARSE, require_e4_jface=True)
        self.assertEqual(report["required_ui_contract_cases"],
                         {E4_REPORT: 10, JFACE_REPORT: 2})
        self.assertEqual(report["skipped"], 0)

    def test_strict_mode_does_not_weaken_old_required_modules(self):
        self.write_contracts()
        (self.root / REQUIRED[0] / "TEST-suite.xml").unlink()
        with self.assertRaisesRegex(ValueError, "missing required"):
            verify(self.root, PARSE, require_e4_jface=True)

    def test_strict_mode_requires_e4_module(self):
        with self.assertRaisesRegex(ValueError, "missing required test reports"):
            verify(self.root, PARSE, require_e4_jface=True)

    def test_strict_mode_rejects_missing_e4_test_method(self):
        missing = next(iter(sorted(NATIVE_UI_CONTRACTS[E4_REPORT])))
        self.write_contracts(omitted={missing})
        with self.assertRaisesRegex(ValueError, "missing required UI cases"):
            verify(self.root, PARSE, require_e4_jface=True)

    def test_strict_mode_rejects_missing_jface_test_method(self):
        missing = next(iter(sorted(NATIVE_UI_CONTRACTS[JFACE_REPORT])))
        self.write_contracts(omitted={missing})
        with self.assertRaisesRegex(ValueError, "missing required UI cases"):
            verify(self.root, PARSE, require_e4_jface=True)

    def test_strict_mode_rejects_skipped_e4_jobmanager(self):
        item = ("org.eclipse.e4.ui.tests.workbench.DisplayUISynchronizeAdmissionTest",
                "refusedSubmissionCompletesOnceThroughJobManager")
        self.write_contracts(skipped=item)
        with self.assertRaisesRegex(ValueError, "skipped or failed required UI case"):
            verify(self.root, PARSE, require_e4_jface=True)

    def test_strict_mode_rejects_skipped_jface_test(self):
        item = next(iter(sorted(NATIVE_UI_CONTRACTS[JFACE_REPORT])))
        self.write_contracts(skipped=item)
        with self.assertRaisesRegex(ValueError, "skipped or failed required UI case"):
            verify(self.root, PARSE, require_e4_jface=True)

    def test_strict_mode_rejects_duplicate_e4_test(self):
        item = next(iter(sorted(NATIVE_UI_CONTRACTS[E4_REPORT])))
        self.write_contracts(duplicate=(E4_REPORT, item))
        with self.assertRaisesRegex(ValueError, "duplicate required UI case"):
            verify(self.root, PARSE, require_e4_jface=True)




class NativeSourceClosureTests(unittest.TestCase):
    """Real Git DAG/gitlink fixtures; no mocks of ls-tree or rev-parse."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "sdk"
        self.root.mkdir()
        self.module_shas = {}
        for name in ("eclipse.platform.ui", "eclipse.platform.swt"):
            module = self.root / name
            module.mkdir()
            self.git(module, "init", "-q")
            self.git(module, "config", "user.name", "Native Test")
            self.git(module, "config", "user.email", "fixture@example.invalid")
            file = module / "fixture.txt"
            file.write_text(name, encoding="utf-8")
            self.git(module, "add", "fixture.txt")
            self.git(module, "commit", "-qm", "source input")
            self.module_shas[name] = self.git(module, "rev-parse", "HEAD")
        self.ui_blobs = {"fixture.txt": self.git(self.root / "eclipse.platform.ui",
                                                    "rev-parse", "HEAD:fixture.txt")}
        self.git(self.root, "init", "-q")
        self.git(self.root, "config", "user.name", "Native Test")
        self.git(self.root, "config", "user.email", "fixture@example.invalid")
        for name, sha in self.module_shas.items():
            self.git(self.root, "update-index", "--add", "--cacheinfo",
                     "160000," + sha + "," + name)
        self.git(self.root, "commit", "-qm", "pin Gitlinks")

    @staticmethod
    def git(directory, *args):
        return subprocess.check_output(["git", "-C", str(directory), *args],
                                       text=True, stderr=subprocess.PIPE).strip()

    def validate(self, **kwargs):
        return verify_native_source_checkout(self.root,
                pins=kwargs.get("pins", self.module_shas),
                ui_blobs=kwargs.get("blobs", self.ui_blobs))

    def test_exact_materialized_submodules_and_ui_blobs_pass(self):
        receipt = self.validate()
        self.assertEqual(receipt["pinned_submodules"], self.module_shas)
        self.assertEqual(receipt["reviewed_ui_blobs"], 1)

    def test_wrong_ui_pin_is_refused(self):
        pins = dict(self.module_shas)
        pins["eclipse.platform.ui"] = "f" * 40
        with self.assertRaisesRegex(ValueError, "gitlink mismatch"):
            self.validate(pins=pins)

    def test_wrong_swt_pin_is_refused(self):
        pins = dict(self.module_shas)
        pins["eclipse.platform.swt"] = "f" * 40
        with self.assertRaisesRegex(ValueError, "gitlink mismatch"):
            self.validate(pins=pins)

    def test_materialized_checkout_drift_is_refused(self):
        module = self.root / "eclipse.platform.ui"
        (module / "another.txt").write_text("new source", encoding="utf-8")
        self.git(module, "add", "another.txt")
        self.git(module, "commit", "-qm", "move HEAD after super checkout")
        with self.assertRaisesRegex(ValueError, "checkout differs"):
            self.validate()

    def test_wrong_reviewed_blob_is_refused(self):
        with self.assertRaisesRegex(ValueError, "reviewed UI source blob mismatch"):
            self.validate(blobs={"fixture.txt": "f" * 40})

    def test_dirty_reviewed_source_is_refused(self):
        (self.root / "eclipse.platform.ui" / "fixture.txt").write_text("mutated", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "uncommitted changes"):
            self.validate()

    def test_regular_blob_replacing_gitlink_is_refused(self):
        blob = subprocess.check_output(["git", "-C", str(self.root),
                                        "hash-object", "-w", "--stdin"],
                                       input=b"not-a-gitlink").decode().strip()
        self.git(self.root, "update-index", "--add", "--cacheinfo",
                 "100644," + blob + ",eclipse.platform.swt")
        self.git(self.root, "commit", "-qm", "bad regular blob")
        with self.assertRaisesRegex(ValueError, "gitlink mismatch"):
            self.validate()

    def test_missing_reviewed_ui_owner_is_refused(self):
        with self.assertRaisesRegex(ValueError, "reviewed UI source blob mismatch"):
            self.validate(blobs={"missing.java": "f" * 40})

    def test_dirty_native_swt_checkout_is_refused(self):
        (self.root / "eclipse.platform.swt" / "fixture.txt").write_text("mutated", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "uncommitted changes"):
            self.validate()

    def test_ignored_injected_ui_java_is_refused(self):
        module = self.root / "eclipse.platform.ui"
        with (module / ".git" / "info" / "exclude").open("a") as excluded:
            excluded.write("\nhidden.java\n")
        (module / "hidden.java").write_text("class Hidden {}", encoding="utf-8")
        # Without --ignored, ordinary status incorrectly reports clean.
        self.assertEqual(self.git(module, "status", "--porcelain=v1",
                                  "--untracked-files=all"), "")
        with self.assertRaisesRegex(ValueError, "uncommitted changes"):
            self.validate()

    def test_ignored_injected_swt_source_is_refused(self):
        module = self.root / "eclipse.platform.swt"
        with (module / ".git" / "info" / "exclude").open("a") as excluded:
            excluded.write("\nhidden.c\n")
        (module / "hidden.c").write_text("/* injected */", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "uncommitted changes"):
            self.validate()

    def test_assume_unchanged_modified_reviewed_source_is_refused(self):
        module = self.root / "eclipse.platform.ui"
        (module / "fixture.txt").write_text("tampered source", encoding="utf-8")
        self.git(module, "update-index", "--assume-unchanged", "fixture.txt")
        self.assertEqual(self.git(module, "status", "--porcelain=v1",
                                  "--untracked-files=all"), "")
        with self.assertRaisesRegex(ValueError, "reviewed UI worktree blob mismatch"):
            self.validate()

    def test_untracked_ui_java_is_refused(self):
        (self.root / "eclipse.platform.ui" / "injected.java").write_text("class Injected {}", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "uncommitted changes"):
            self.validate()



if __name__ == "__main__":
    unittest.main()
