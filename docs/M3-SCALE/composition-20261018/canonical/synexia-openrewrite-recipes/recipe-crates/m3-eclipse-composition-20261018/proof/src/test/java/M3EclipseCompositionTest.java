// SPDX-FileCopyrightText: 2026 Hitesh Soliwal and Contributors to the Synexia Project
// SPDX-License-Identifier: Apache-2.0
import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class M3EclipseCompositionTest {
    private static final List<String> MODULES = List.of("eclipse.jdt", "eclipse.jdt.core",
            "eclipse.jdt.core.binaries", "eclipse.jdt.debug", "eclipse.jdt.ui", "eclipse.pde",
            "eclipse.platform", "eclipse.platform.swt", "eclipse.platform.ui", "equinox",
            "equinox.binaries", "equinox.p2");
    private static final String CLASS = "org.eclipse.jface.tests.viewers.M3TreeForwardingTest";
    private static final String METHOD = "testExpandedStateDelegatesToSwtWithoutWalkingColdVirtualSiblings";

    @TempDir Path temporary;

    @Test void acceptsAllTwelveExactCleanInitializedGitlinksWithoutWritingGitState() throws Exception {
        Fixture fixture = fixture();
        byte[] index = Files.readAllBytes(fixture.root.resolve(".git/index"));
        byte[] config = Files.readAllBytes(fixture.root.resolve(".git/config"));
        assertDoesNotThrow(() -> M3EclipseComposition.verifySource(fixture.root, fixture.manifest));
        assertTrue(java.util.Arrays.equals(index, Files.readAllBytes(fixture.root.resolve(".git/index"))));
        assertTrue(java.util.Arrays.equals(config, Files.readAllBytes(fixture.root.resolve(".git/config"))));
        assertEquals("", git(fixture.root, "status", "--porcelain", "--untracked-files=all"));
    }

    @Test void rejectsRecordedGitlinkThatDisagreesWithManifest() throws Exception {
        Fixture fixture = fixture();
        git(fixture.root, "update-index", "--cacheinfo", "160000," + "a".repeat(40) + ",eclipse.platform.swt");
        sourceRefuses(fixture);
    }

    @Test void rejectsInitializedWorktreeAtAStaleCommit() throws Exception {
        Fixture fixture = fixture();
        Path module = fixture.root.resolve("eclipse.platform.swt");
        Files.writeString(module.resolve("owner.txt"), "new source\n");
        git(module, "add", "owner.txt");
        git(module, "commit", "-m", "drift");
        sourceRefuses(fixture);
    }

    @Test void rejectsEmptyUninitializedSubmoduleInsteadOfFallingBackToParentGitRoot() throws Exception {
        Fixture fixture = fixture();
        git(fixture.root, "submodule", "deinit", "-f", "--", "eclipse.platform.swt");
        assertTrue(Files.isDirectory(fixture.root.resolve("eclipse.platform.swt")));
        sourceRefuses(fixture);
    }

    @Test void rejectsTrackedSourceDrift() throws Exception {
        Fixture fixture = fixture();
        Files.writeString(fixture.root.resolve("eclipse.platform.ui/owner.txt"), "dirty\n");
        sourceRefuses(fixture);
    }

    @Test void rejectsUntrackedSubmoduleSource() throws Exception {
        Fixture fixture = fixture();
        Files.writeString(fixture.root.resolve("eclipse.platform.ui/unreviewed.java"), "unreviewed\n");
        sourceRefuses(fixture);
    }

    @Test void rejectsCommittedUrlDriftEvenWithMatchingGitlinks() throws Exception {
        Fixture fixture = fixture();
        git(fixture.root, "config", "--file", ".gitmodules", "submodule.eclipse.platform.swt.url", "https://github.com/eclipse-platform/eclipse.platform.swt.git");
        git(fixture.root, "add", ".gitmodules");
        git(fixture.root, "commit", "-m", "wrong URL");
        sourceRefuses(fixture);
    }

    @Test void rejectsMissingManifestModule() throws Exception {
        Fixture fixture = fixture();
        rewriteManifest(fixture, Files.readString(fixture.manifest).replaceFirst("(?m)^equinox\\.p2\\t.*\\n", ""));
        sourceRefuses(fixture);
    }

    @Test void rejectsDuplicateManifestModule() throws Exception {
        Fixture fixture = fixture();
        rewriteManifest(fixture, Files.readString(fixture.manifest) + row("equinox.p2", fixture.commit));
        sourceRefuses(fixture);
    }

    @Test void rejectsForeignManifestModule() throws Exception {
        Fixture fixture = fixture();
        rewriteManifest(fixture, Files.readString(fixture.manifest) + row("nebula", fixture.commit));
        sourceRefuses(fixture);
    }

    @Test void rejectsManifestTraversal() throws Exception {
        Fixture fixture = fixture();
        rewriteManifest(fixture, Files.readString(fixture.manifest).replace("eclipse.platform.swt\t", "../eclipse.platform.swt\t"));
        sourceRefuses(fixture);
    }

    @Test void rejectsShortCommitAndNonGithubOrExecutableUrl() throws Exception {
        Fixture fixture = fixture();
        String valid = Files.readString(fixture.manifest);
        for (String invalid : List.of(valid.replace(fixture.commit, fixture.commit.substring(0, 8)),
                valid.replace("https://github.com/", "https://evil.example/"),
                valid.replace("https://github.com/", "ext::sh -c "),
                valid.replace("https://github.com/", "http://github.com/"))) {
            rewriteManifest(fixture, invalid);
            sourceRefuses(fixture);
        }
    }

    @Test void rejectsDuplicateGitmodulesEntry() throws Exception {
        Fixture fixture = fixture();
        git(fixture.root, "config", "--file", ".gitmodules", "--add", "submodule.eclipse.platform.swt.url", url("eclipse.platform.swt"));
        git(fixture.root, "add", ".gitmodules");
        git(fixture.root, "commit", "-m", "duplicate URL");
        sourceRefuses(fixture);
    }

    @Test void rejectsExtraGitmodulesEntry() throws Exception {
        Fixture fixture = fixture();
        git(fixture.root, "config", "--file", ".gitmodules", "submodule.extra.path", "extra");
        git(fixture.root, "config", "--file", ".gitmodules", "submodule.extra.url", url("extra"));
        git(fixture.root, "add", ".gitmodules");
        git(fixture.root, "commit", "-m", "extra module");
        sourceRefuses(fixture);
    }

    @Test void rejectsSymlinkedSubmoduleEscape() throws Exception {
        Fixture fixture = fixture();
        Path module = fixture.root.resolve("eclipse.platform.swt");
        Path escaped = temporary.resolve("escaped");
        Files.move(module, escaped);
        Files.createSymbolicLink(module, escaped);
        sourceRefuses(fixture);
    }

    @Test void rejectsSymlinkedManifest() throws Exception {
        Fixture fixture = fixture();
        Path escaped = temporary.resolve("outside.tsv");
        Files.move(fixture.manifest, escaped);
        Files.createSymbolicLink(fixture.manifest, escaped);
        sourceRefuses(fixture);
    }

    @Test void rejectsOversizedManifest() throws Exception {
        Fixture fixture = fixture();
        rewriteManifest(fixture, Files.readString(fixture.manifest) + "#".repeat(65536));
        sourceRefuses(fixture);
    }

    @Test void rejectsDirtySourceHiddenByAssumeUnchanged() throws Exception {
        Fixture fixture = fixture();
        Path module = fixture.root.resolve("eclipse.platform.swt");
        git(module, "update-index", "--assume-unchanged", "owner.txt");
        Files.writeString(module.resolve("owner.txt"), "concealed drift\n");
        assertEquals("", git(module, "status", "--porcelain"));
        sourceRefuses(fixture);
    }

    @Test void rejectsDirtySourceHiddenBySkipWorktree() throws Exception {
        Fixture fixture = fixture();
        Path module = fixture.root.resolve("eclipse.platform.swt");
        git(module, "update-index", "--skip-worktree", "owner.txt");
        Files.writeString(module.resolve("owner.txt"), "concealed drift\n");
        assertEquals("", git(module, "status", "--porcelain"));
        sourceRefuses(fixture);
    }

    @Test void rejectsCommittedTrackedSymlinkEscape() throws Exception {
        Fixture fixture = fixture();
        Path module = fixture.root.resolve("eclipse.platform.swt");
        Files.createSymbolicLink(module.resolve("escaped-source"), temporary.resolve("upstream/owner.txt"));
        git(module, "add", "escaped-source");
        git(module, "commit", "-m", "tracked symlink");
        String newCommit = git(module, "rev-parse", "HEAD").strip();
        git(fixture.root, "add", "eclipse.platform.swt");
        rewriteManifest(fixture, Files.readString(fixture.manifest).replace(row("eclipse.platform.swt", fixture.commit), row("eclipse.platform.swt", newCommit)));
        sourceRefuses(fixture);
    }

    @Test void rejectsExtraCommittedGitlinkEvenWithoutGitmodulesEntry() throws Exception {
        Fixture fixture = fixture();
        git(fixture.root, "update-index", "--add", "--cacheinfo", "160000," + fixture.commit + ",extra");
        git(fixture.root, "commit", "-m", "extra gitlink");
        sourceRefuses(fixture);
    }

    @Test void rejectsNonRootRepositoryArgument() throws Exception {
        Fixture fixture = fixture();
        Path nested = Files.createDirectories(fixture.root.resolve("nested"));
        assertThrows(IOException.class, () -> M3EclipseComposition.verifySource(nested, fixture.manifest));
    }

    @Test void rejectsSourceConcealedByLocalInfoExclude() throws Exception {
        Fixture fixture = fixture();
        Path module = fixture.root.resolve("eclipse.platform.swt");
        String exclude = git(module, "rev-parse", "--path-format=absolute", "--git-path", "info/exclude").strip();
        Files.writeString(Path.of(exclude), "unreviewed.java\n");
        Files.writeString(module.resolve("unreviewed.java"), "concealed new source\n");
        assertEquals("", git(module, "status", "--porcelain"));
        sourceRefuses(fixture);
    }

    @Test void rejectsSourceConcealedByLocalCoreExcludesFile() throws Exception {
        Fixture fixture = fixture();
        Path module = fixture.root.resolve("eclipse.platform.swt");
        Path excludes = temporary.resolve("excludes");
        Files.writeString(excludes, "unreviewed.java\n");
        git(module, "config", "core.excludesFile", excludes.toString());
        Files.writeString(module.resolve("unreviewed.java"), "concealed new source\n");
        assertEquals("", git(module, "status", "--porcelain"));
        sourceRefuses(fixture);
    }

    @Test void acceptsExactNamedPassingTestWithOtherIntentionalSkips() throws Exception {
        Path directory = reports();
        report(directory, "nested/TEST-native.xml", suite(test("") + "<testcase classname='other' name='optional'><skipped/></testcase>"));
        assertDoesNotThrow(() -> M3EclipseComposition.verifyReports(directory));
    }

    @Test void rejectsNoXmlReports() throws Exception {
        assertThrows(IOException.class, () -> M3EclipseComposition.verifyReports(reports()));
    }

    @Test void rejectsZeroTestsAggregate() throws Exception {
        Path directory = reports();
        report(directory, "TEST-empty.xml", "<testsuite tests='0' failures='0' errors='0'/>\n");
        reportsRefuse(directory);
    }

    @Test void rejectsDifferentClassOrMethodEvenWhenAggregateIsGreen() throws Exception {
        Path directory = reports();
        report(directory, "TEST-other.xml", suite("<testcase classname='other' name='" + METHOD + "'/>"));
        reportsRefuse(directory);
        report(directory, "TEST-other.xml", suite("<testcase classname='" + CLASS + "' name='other'/>"));
        reportsRefuse(directory);
    }

    @Test void rejectsSkippedRequiredTest() throws Exception {
        Path directory = reports();
        report(directory, "TEST-skipped.xml", suite(test("<skipped message='M3 absent'/>")));
        reportsRefuse(directory);
    }

    @Test void rejectsFailedOrErroredRequiredTest() throws Exception {
        Path directory = reports();
        for (String failure : List.of("failure", "error")) {
            report(directory, "TEST-failed.xml", suite(test("<" + failure + " message='broken'/>")));
            reportsRefuse(directory);
        }
    }

    @Test void rejectsAnyOtherFailureInSelectedReportDirectory() throws Exception {
        Path directory = reports();
        report(directory, "TEST-pass.xml", suite(test("")));
        report(directory, "TEST-fail.xml", suite("<testcase classname='other' name='broken'><failure/></testcase>"));
        reportsRefuse(directory);
    }

    @Test void rejectsNonzeroFailureOrErrorAggregateWithoutFailureElement() throws Exception {
        Path directory = reports();
        report(directory, "TEST-inconsistent.xml", "<testsuite failures='1'>" + test("") + "</testsuite>");
        reportsRefuse(directory);
        report(directory, "TEST-inconsistent.xml", "<testsuite errors='1'>" + test("") + "</testsuite>");
        reportsRefuse(directory);
    }

    @Test void rejectsDuplicateRequiredTestWithinOrAcrossFiles() throws Exception {
        Path directory = reports();
        report(directory, "TEST-duplicate.xml", suite(test("") + test("")));
        reportsRefuse(directory);
        report(directory, "TEST-duplicate.xml", suite(test("")));
        report(directory, "nested/TEST-copy.xml", suite(test("")));
        reportsRefuse(directory);
    }

    @Test void rejectsExplicitNotRunStatus() throws Exception {
        Path directory = reports();
        report(directory, "TEST-notrun.xml", suite(test("").replace("<testcase ", "<testcase status='notrun' ")));
        reportsRefuse(directory);
    }

    @Test void rejectsExternalEntityAndDoctype() throws Exception {
        Path directory = reports();
        Path secret = temporary.resolve("secret.txt");
        Files.writeString(secret, "test secret");
        report(directory, "TEST-xxe.xml", "<!DOCTYPE testsuite [<!ENTITY xxe SYSTEM '" + secret.toUri() + "'>]><testsuite>" + test("<system-out>&xxe;</system-out>") + "</testsuite>");
        reportsRefuse(directory);
        report(directory, "TEST-xxe.xml", "<!DOCTYPE testsuite [<!ENTITY local 'local'>]><testsuite>" + test("") + "</testsuite>");
        reportsRefuse(directory);
    }

    @Test void rejectsMalformedAndForeignXml() throws Exception {
        Path directory = reports();
        report(directory, "TEST-bad.xml", "<testsuite>");
        reportsRefuse(directory);
        report(directory, "TEST-bad.xml", "<other>" + test("") + "</other>");
        reportsRefuse(directory);
    }

    @Test void rejectsReportSymlinkEscape() throws Exception {
        Path directory = reports();
        Path outside = temporary.resolve("outside.xml");
        Files.writeString(outside, suite(test("")));
        Files.createSymbolicLink(directory.resolve("TEST-linked.xml"), outside);
        reportsRefuse(directory);
    }

    @Test void rejectsReportDirectorySymlinkEscape() throws Exception {
        Path directory = reports();
        Path outside = temporary.resolve("outside");
        Files.createDirectories(outside);
        report(outside, "TEST-pass.xml", suite(test("")));
        Files.createSymbolicLink(directory.resolve("linked"), outside);
        reportsRefuse(directory);
    }

    @Test void rejectsOversizedReport() throws Exception {
        Path directory = reports();
        report(directory, "TEST-large.xml", suite(test("") + "<system-out>" + "x".repeat(2 * 1024 * 1024) + "</system-out>"));
        reportsRefuse(directory);
    }

    @Test void rejectsExcessiveReportCount() throws Exception {
        Path directory = reports();
        report(directory, "TEST-pass.xml", suite(test("")));
        for (int i = 0; i < 256; i++) report(directory, "TEST-" + i + ".xml", suite("<testcase classname='other' name='ok'/>"));
        reportsRefuse(directory);
    }

    @Test void rejectsExcessiveTotalReportBytes() throws Exception {
        Path directory = reports();
        report(directory, "TEST-pass.xml", suite(test("")));
        for (int i = 0; i < 17; i++) report(directory, "TEST-" + i + ".xml", suite("<system-out>" + "x".repeat(1024 * 1024) + "</system-out>"));
        reportsRefuse(directory);
    }

    @Test void rejectsExcessiveReportDepth() throws Exception {
        Path directory = reports();
        report(directory, "nested/".repeat(17) + "TEST-pass.xml", suite(test("")));
        reportsRefuse(directory);
    }

    @Test void rejectsTestcaseHiddenOutsideTestsuiteChildren() throws Exception {
        Path directory = reports();
        report(directory, "TEST-hidden.xml", suite("<properties>" + test("") + "</properties>"));
        reportsRefuse(directory);
    }

    @Test void rejectsHiddenDuplicateBesideValidRequiredTest() throws Exception {
        Path directory = reports();
        report(directory, "TEST-hidden.xml", suite(test("") + "<properties>" + test("") + "</properties>"));
        reportsRefuse(directory);
    }

    @Test void rejectsHiddenFailedSuiteBesideValidRequiredTest() throws Exception {
        Path directory = reports();
        report(directory, "TEST-hidden.xml", suite(test("") + "<properties><testsuite failures='1'/></properties>"));
        reportsRefuse(directory);
    }

    @Test void rejectsContradictoryZeroTestsSuiteContainingRequiredTest() throws Exception {
        Path directory = reports();
        report(directory, "TEST-inconsistent.xml", "<testsuite tests='0' failures='0' errors='0'>" + test("") + "</testsuite>");
        reportsRefuse(directory);
    }

    private Fixture fixture() throws Exception {
        Path root = temporary.resolve("sdk");
        Path upstream = temporary.resolve("upstream");
        Files.createDirectories(upstream);
        git(upstream, "init", "--quiet");
        git(upstream, "config", "user.name", "Composition fixture");
        git(upstream, "config", "user.email", "fixture@example.invalid");
        Files.writeString(upstream.resolve("owner.txt"), "existing M3 owner fixture\n");
        git(upstream, "add", "owner.txt");
        git(upstream, "commit", "--quiet", "-m", "fixture owner");
        String commit = git(upstream, "rev-parse", "HEAD").strip();
        Files.createDirectories(root);
        git(root, "init", "--quiet");
        git(root, "config", "user.name", "Composition fixture");
        git(root, "config", "user.email", "fixture@example.invalid");
        StringBuilder manifest = new StringBuilder("path\turl\tcommit\n");
        for (String module : MODULES) {
            git(root, "-c", "protocol.file.allow=always", "submodule", "add", "--quiet", upstream.toString(), module);
            git(root.resolve(module), "config", "user.name", "Composition fixture");
            git(root.resolve(module), "config", "user.email", "fixture@example.invalid");
            git(root, "config", "--file", ".gitmodules", "submodule." + module + ".url", url(module));
            git(root, "config", "--file", ".gitmodules", "submodule." + module + ".branch", "master");
            manifest.append(row(module, commit));
        }
        Path file = root.resolve("composition.tsv");
        Files.writeString(file, manifest.toString());
        git(root, "add", ".");
        git(root, "commit", "--quiet", "-m", "pin twelve modules");
        return new Fixture(root, file, commit);
    }

    private static String git(Path root, String... arguments) throws Exception {
        List<String> command = new ArrayList<>(List.of("git", "-C", root.toString()));
        command.addAll(List.of(arguments));
        ProcessBuilder builder = new ProcessBuilder(command).redirectErrorStream(true);
        builder.environment().keySet().removeIf(name -> name.startsWith("GIT_"));
        builder.environment().put("GIT_CONFIG_NOSYSTEM", "1");
        builder.environment().put("GIT_CONFIG_GLOBAL", "/dev/null");
        Process process = builder.start();
        String output = new String(process.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
        if (!process.waitFor(10, TimeUnit.SECONDS)) { process.destroyForcibly(); throw new IOException("fixture git timed out"); }
        assertEquals(0, process.exitValue(), () -> command + "\n" + output);
        return output;
    }

    private static String url(String module) { return "https://github.com/example/" + module + ".git"; }
    private static String row(String module, String commit) { return module + "\t" + url(module) + "\t" + commit + "\n"; }
    private static void sourceRefuses(Fixture fixture) { assertThrows(IOException.class, () -> M3EclipseComposition.verifySource(fixture.root, fixture.manifest)); }
    private static void rewriteManifest(Fixture fixture, String content) throws Exception {
        Files.writeString(fixture.manifest, content);
        git(fixture.root, "add", "composition.tsv");
        git(fixture.root, "commit", "--quiet", "--allow-empty", "-m", "manifest variant");
    }
    private Path reports() throws IOException { return Files.createDirectories(temporary.resolve("reports")); }
    private static void report(Path directory, String name, String xml) throws IOException {
        Path file = directory.resolve(name);
        Files.createDirectories(file.getParent());
        Files.writeString(file, xml);
    }
    private static String suite(String cases) { return "<testsuite failures='0' errors='0'>" + cases + "</testsuite>"; }
    private static String test(String body) { return "<testcase classname='" + CLASS + "' name='" + METHOD + "'>" + body + "</testcase>"; }
    private static void reportsRefuse(Path directory) { assertThrows(IOException.class, () -> M3EclipseComposition.verifyReports(directory)); }
    private record Fixture(Path root, Path manifest, String commit) { }
}
