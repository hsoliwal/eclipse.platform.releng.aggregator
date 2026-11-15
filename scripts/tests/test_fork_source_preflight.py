"""Isolated Git fixture tests of source closure; no network or remote changes."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "fork_source_preflight.py"
SPEC = importlib.util.spec_from_file_location("fork_source_preflight", SOURCE)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def run(root: Path, *args: str) -> str:
    env = os.environ.copy()
    env.update({"GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@example.test",
                "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@example.test"})
    return subprocess.check_output(["git", "-C", str(root), *args],
                                   text=True, env=env).strip()


class SourceClosureTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        run(self.root, "init", "-q")
        modules = []
        for path, (repo, branch) in MODULE.EXPECTED.items():
            modules.append(f'[submodule "{path}"]\n\tpath = {path}\n'
                           f'\turl = https://github.com/hsoliwal/{repo}.git\n'
                           f'\tbranch = {branch}\n')
        (self.root / ".gitmodules").write_text("".join(modules), encoding="utf-8")
        reactor = "".join(f"<module>{path}</module>" for path in MODULE.EXPECTED)
        (self.root / "pom.xml").write_text(f"<project><modules>{reactor}</modules></project>", encoding="utf-8")
        run(self.root, "add", ".gitmodules", "pom.xml")
        for i, path in enumerate(MODULE.EXPECTED, start=1):
            run(self.root, "update-index", "--add", "--cacheinfo", "160000", f"{i:040x}", path)
        run(self.root, "commit", "-qm", "synthetic pinned source")

    def test_exact_source_closure_passes_without_release_admission(self) -> None:
        result = MODULE.inspect(self.root)
        self.assertTrue(result["source_closure_passed"], result["errors"])
        self.assertFalse(result["release_admitted"])
        self.assertEqual(12, len(result["submodules"]))

    def test_uncommitted_manifest_drift_fails(self) -> None:
        with (self.root / ".gitmodules").open("a", encoding="utf-8") as handle:
            handle.write("\n# drift\n")
        result = MODULE.inspect(self.root)
        self.assertFalse(result["source_closure_passed"])
        self.assertTrue(any("Tracked source anchors" in x for x in result["errors"]))

    def test_upstream_remote_cannot_satisfy_fork_contract(self) -> None:
        path = self.root / ".gitmodules"
        path.write_text(path.read_text().replace("https://github.com/hsoliwal/eclipse.jdt.git",
                                                  "https://github.com/eclipse-jdt/eclipse.jdt.git"), encoding="utf-8")
        run(self.root, "add", ".gitmodules")
        run(self.root, "commit", "-qm", "change remote")
        result = MODULE.inspect(self.root)
        self.assertTrue(any("Unexpected fork URL for eclipse.jdt" in x for x in result["errors"]))

    def test_missing_gitlink_fails(self) -> None:
        run(self.root, "rm", "--cached", "-q", "equinox")
        run(self.root, "commit", "-qm", "remove gitlink")
        result = MODULE.inspect(self.root)
        self.assertTrue(any("Missing/invalid committed gitlink: equinox" in x for x in result["errors"]))

    def test_missing_reactor_member_fails(self) -> None:
        path = self.root / "pom.xml"
        path.write_text(path.read_text().replace("<module>equinox</module>", ""), encoding="utf-8")
        run(self.root, "add", "pom.xml")
        run(self.root, "commit", "-qm", "remove reactor module")
        result = MODULE.inspect(self.root)
        self.assertTrue(any("Missing Maven reactor module: equinox" in x for x in result["errors"]))

    def test_tracking_branch_drift_fails(self) -> None:
        path = self.root / ".gitmodules"
        path.write_text(path.read_text().replace("branch = upstream-master", "branch = master"), encoding="utf-8")
        run(self.root, "add", ".gitmodules")
        run(self.root, "commit", "-qm", "alter PDE branch")
        result = MODULE.inspect(self.root)
        self.assertTrue(any("Unexpected tracking branch for eclipse.pde" in x for x in result["errors"]))

    def test_uninitialized_checkout_fails_when_required(self) -> None:
        result = MODULE.inspect(self.root, require_checkout=True)
        self.assertFalse(result["source_closure_passed"])
        self.assertTrue(any("checkout" in x.lower() for x in result["errors"]))


if __name__ == "__main__":
    unittest.main()
