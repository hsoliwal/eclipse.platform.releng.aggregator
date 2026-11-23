#!/usr/bin/env python3
# SPDX-License-Identifier: EPL-2.0
"""Regression cases for SDK report admission, using the actual SWT parser."""
import os
from pathlib import Path
import tempfile
import unittest

from verify_test_reports import (E4_REPORT, JFACE_REPORT, NATIVE_UI_CONTRACTS,
                                 REQUIRED, load_junit_report, verify)

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


if __name__ == "__main__":
    unittest.main()
