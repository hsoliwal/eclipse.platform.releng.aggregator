/*
 * SPDX-FileCopyrightText: 2026 Hitesh Soliwal and Contributors to the Synexia Project
 * SPDX-License-Identifier: Apache-2.0
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.nio.charset.CodingErrorAction;
import java.nio.charset.StandardCharsets;
import java.nio.file.FileVisitResult;
import java.nio.file.Files;
import java.nio.file.LinkOption;
import java.nio.file.Path;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.attribute.BasicFileAttributes;
import java.time.Duration;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.FutureTask;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.xml.XMLConstants;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.xml.sax.SAXException;
import org.xml.sax.SAXParseException;
import org.xml.sax.helpers.DefaultHandler;

/** Read-only source selection and named native-test evidence checks; no runtime or checkout machinery. */
public final class M3EclipseComposition {
    private static final Set<String> MODULES = Set.of("eclipse.jdt", "eclipse.jdt.core",
            "eclipse.jdt.core.binaries", "eclipse.jdt.debug", "eclipse.jdt.ui", "eclipse.pde",
            "eclipse.platform", "eclipse.platform.swt", "eclipse.platform.ui", "equinox",
            "equinox.binaries", "equinox.p2");
    private static final String TEST_CLASS = "org.eclipse.jface.tests.viewers.M3TreeForwardingTest";
    private static final String TEST_METHOD = "testExpandedStateDelegatesToSwtWithoutWalkingColdVirtualSiblings";
    private static final Pattern HASH = Pattern.compile("[0-9a-f]{40}");
    private static final Pattern URL = Pattern.compile("https://github\\.com/[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9][A-Za-z0-9._-]*\\.git");
    private static final Pattern INDEX = Pattern.compile("([A-Za-z?]) ([0-9]{6}) ([0-9a-f]{40}) ([0-3])\\t(.+)", Pattern.DOTALL);
    private static final int MANIFEST_BYTES = 16 * 1024;
    private static final int GITMODULES_BYTES = 32 * 1024;
    private static final int GIT_OUTPUT_BYTES = 16 * 1024 * 1024;
    private static final int INDEX_ENTRIES = 200_000;
    private static final int REPORT_BYTES = 2 * 1024 * 1024;
    private static final long REPORT_TOTAL_BYTES = 16L * 1024 * 1024;
    private static final int REPORT_FILES = 256;
    private static final int REPORT_ENTRIES = 4096;
    private static final int REPORT_DEPTH = 16;
    private static final int REPORT_TESTCASES = 100_000;
    private static final Duration GIT_TIMEOUT = Duration.ofSeconds(15);
    private static final Duration SOURCE_TIMEOUT = Duration.ofSeconds(120);
    private static final Duration REPORT_TIMEOUT = Duration.ofSeconds(30);

    private M3EclipseComposition() { }

    public static void main(String[] arguments) throws IOException, InterruptedException {
        if (arguments.length == 3 && arguments[0].equals("source")) {
            verifySource(Path.of(arguments[1]), Path.of(arguments[2]));
            System.out.println("PASS source: twelve exact, initialized, clean Eclipse gitlinks.");
        } else if (arguments.length == 2 && arguments[0].equals("reports")) {
            verifyReports(Path.of(arguments[1]));
            System.out.println("PASS reports: exactly one passing " + TEST_CLASS + "#" + TEST_METHOD + ".");
        } else {
            throw new IOException("Usage: M3EclipseComposition source <repo-root> <composition.tsv> | reports <report-dir>");
        }
    }

    public static void verifySource(Path repository, Path manifest) throws IOException, InterruptedException {
        Budget budget = new Budget("source verification", SOURCE_TIMEOUT);
        Path root = checkedPath(repository, true);
        Map<String, Pin> pins = readManifest(manifest);
        requireRepositoryRoot(root, budget);
        checkGitmodules(root, pins, budget);
        Map<String, Entry> index = readIndex(root, budget);
        Map<String, String> gitlinks = new LinkedHashMap<>();
        for (Map.Entry<String, Entry> entry : index.entrySet()) {
            if (entry.getValue().mode.equals("160000")) gitlinks.put(entry.getKey(), entry.getValue().commit);
        }
        require(gitlinks.keySet().equals(MODULES), "index must contain exactly the twelve expected Eclipse gitlinks");
        require(index.containsKey(".gitmodules"), ".gitmodules must be tracked");
        for (Map.Entry<String, Pin> pin : pins.entrySet()) {
            String module = pin.getKey();
            require(pin.getValue().commit.equals(gitlinks.get(module)), "recorded gitlink disagrees with manifest: " + module);
            Path worktree = checkedPath(root.resolve(module), true);
            requireRepositoryRoot(worktree, budget);
            String head = git(worktree, budget, "rev-parse", "--verify", "HEAD^{commit}").strip();
            require(HASH.matcher(head).matches() && head.equals(pin.getValue().commit), "initialized HEAD disagrees with manifest: " + module);
            checkSourceTree(worktree, readIndex(worktree, budget), budget);
        }
        checkSourceTree(root, index, budget);
        budget.check();
    }

    private static Map<String, Pin> readManifest(Path manifest) throws IOException {
        String content = utf8(readFile(manifest, MANIFEST_BYTES));
        String[] lines = content.split("\\r?\\n", -1);
        require(lines.length > 0 && lines[0].equals("path\turl\tcommit"), "manifest header must be path<TAB>url<TAB>commit");
        Map<String, Pin> pins = new LinkedHashMap<>();
        for (int i = 1; i < lines.length; i++) {
            if (i == lines.length - 1 && lines[i].isEmpty()) break;
            String[] fields = lines[i].split("\t", -1);
            require(fields.length == 3, "manifest row must have exactly three tab-separated fields: " + (i + 1));
            require(MODULES.contains(fields[0]), "unexpected or unsafe manifest module: " + fields[0]);
            require(URL.matcher(fields[1]).matches(), "manifest URL must be a public HTTPS GitHub .git URL: " + fields[0]);
            require(HASH.matcher(fields[2]).matches(), "manifest commit must be a lowercase SHA-1 of forty hex digits: " + fields[0]);
            require(pins.putIfAbsent(fields[0], new Pin(fields[1], fields[2])) == null, "duplicate manifest module: " + fields[0]);
        }
        require(pins.keySet().equals(MODULES), "manifest must select exactly the twelve expected Eclipse modules");
        return pins;
    }

    private static void checkGitmodules(Path root, Map<String, Pin> pins, Budget budget) throws IOException, InterruptedException {
        Path metadata = checkedPath(root.resolve(".gitmodules"), false);
        readFile(metadata, GITMODULES_BYTES);
        String content = git(root, budget, "config", "--null", "--no-includes", "--file", metadata.toString(), "--list");
        Map<String, Map<String, String>> sections = new LinkedHashMap<>();
        for (String record : nulRecords(content)) {
            int newline = record.indexOf('\n');
            require(newline > 0, "malformed .gitmodules entry");
            String key = record.substring(0, newline);
            int fieldStart = key.lastIndexOf('.');
            require(key.startsWith("submodule.") && fieldStart > "submodule.".length(), "unexpected .gitmodules configuration");
            String name = key.substring("submodule.".length(), fieldStart);
            String field = key.substring(fieldStart + 1);
            Map<String, String> section = sections.computeIfAbsent(name, unused -> new LinkedHashMap<>());
            require(section.putIfAbsent(field, record.substring(newline + 1)) == null, "duplicate .gitmodules field: " + key);
        }
        require(sections.size() == MODULES.size(), ".gitmodules must contain exactly twelve modules");
        Set<String> seen = new HashSet<>();
        for (Map<String, String> section : sections.values()) {
            String path = section.get("path");
            require(path != null && MODULES.contains(path) && seen.add(path), "missing, duplicate or unexpected .gitmodules path");
            require(pins.get(path).url.equals(section.get("url")), ".gitmodules URL disagrees with manifest: " + path);
        }
        require(seen.equals(MODULES), ".gitmodules path set disagrees with manifest");
    }

    private static Map<String, Entry> readIndex(Path root, Budget budget) throws IOException, InterruptedException {
        Map<String, Entry> entries = new LinkedHashMap<>();
        for (String record : nulRecords(git(root, budget, "ls-files", "--stage", "-v", "-z"))) {
            Matcher match = INDEX.matcher(record);
            require(match.matches(), "malformed or unsupported Git index record");
            require(match.group(1).equals("H") && match.group(4).equals("0"), "unmerged, assume-unchanged or skip-worktree index entry is not admissible");
            String name = match.group(5);
            safeRelative(root, name);
            require(entries.putIfAbsent(name, new Entry(match.group(2), match.group(3))) == null, "duplicate index path: " + name);
            require(entries.size() <= INDEX_ENTRIES, "Git index entry limit exceeded");
            budget.check();
        }
        return entries;
    }

    private static void checkSourceTree(Path root, Map<String, Entry> entries, Budget budget) throws IOException, InterruptedException {
        Set<Path> checkedDirectories = new HashSet<>();
        checkedDirectories.add(root);
        for (Map.Entry<String, Entry> entry : entries.entrySet()) {
            Path path = safeRelative(root, entry.getKey());
            for (Path parent = path.getParent(); checkedDirectories.add(parent); parent = parent.getParent()) {
                require(!Files.isSymbolicLink(parent), "symlinked source directory is not admissible: " + parent);
            }
            if (Files.isSymbolicLink(path)) {
                require(entry.getValue().mode.equals("120000"), "unexpected source symlink: " + path);
                require(path.toRealPath().startsWith(root), "tracked source symlink escapes its worktree: " + path);
            }
            budget.check();
        }
        require(git(root, budget, "status", "--porcelain=v1", "-z", "--untracked-files=all", "--ignore-submodules=none").isEmpty(),
                "dirty tracked or untracked source tree: " + root);
    }

    private static void requireRepositoryRoot(Path root, Budget budget) throws IOException, InterruptedException {
        Path marker = root.resolve(".git");
        require(Files.exists(marker, LinkOption.NOFOLLOW_LINKS) && !Files.isSymbolicLink(marker), "uninitialized repository or symlinked Git marker: " + root);
        String top = git(root, budget, "rev-parse", "--show-toplevel");
        require(top.endsWith("\n") && !top.substring(0, top.length() - 1).contains("\n"), "ambiguous Git worktree root");
        require(Path.of(top.substring(0, top.length() - 1)).toRealPath().equals(root), "Git fell back to a different worktree root: " + root);
        Path excludes = Path.of(git(root, budget, "rev-parse", "--path-format=absolute", "--git-path", "info/exclude").strip());
        if (Files.exists(excludes, LinkOption.NOFOLLOW_LINKS)) {
            require(utf8(readFile(excludes, GITMODULES_BYTES)).lines().allMatch(line -> line.isBlank() || line.startsWith("#")),
                    "active local info/exclude rules can conceal source: " + root);
        }
    }

    private static String git(Path root, Budget budget, String... arguments) throws IOException, InterruptedException {
        String nullFile = System.getProperty("os.name").startsWith("Windows") ? "NUL" : "/dev/null";
        List<String> command = new ArrayList<>(List.of("git", "--no-pager", "--no-optional-locks", "--literal-pathspecs",
                "-c", "core.fsmonitor=false", "-c", "core.untrackedCache=false", "-c", "submodule.recurse=false",
                "-c", "core.excludesFile=" + nullFile, "-C", root.toString()));
        command.addAll(List.of(arguments));
        ProcessBuilder builder = new ProcessBuilder(command).redirectErrorStream(true);
        builder.environment().keySet().removeIf(name -> name.startsWith("GIT_"));
        builder.environment().put("GIT_CONFIG_NOSYSTEM", "1");
        builder.environment().put("GIT_CONFIG_GLOBAL", nullFile);
        builder.environment().put("GIT_TERMINAL_PROMPT", "0");
        builder.environment().put("GIT_NO_REPLACE_OBJECTS", "1");
        Process process = builder.start();
        FutureTask<byte[]> output = new FutureTask<>(() -> {
            try (InputStream stream = process.getInputStream()) {
                return readBounded(stream, GIT_OUTPUT_BYTES, "Git output");
            } catch (IOException failure) {
                process.destroyForcibly();
                throw failure;
            }
        });
        Thread.ofVirtual().start(output);
        try {
            long timeout = Math.min(GIT_TIMEOUT.toNanos(), budget.remaining());
            require(process.waitFor(timeout, TimeUnit.NANOSECONDS), "Git command time limit exceeded: " + arguments[0]);
            byte[] bytes;
            try {
                bytes = output.get(Math.min(GIT_TIMEOUT.toNanos(), budget.remaining()), TimeUnit.NANOSECONDS);
            } catch (ExecutionException failure) {
                throw new IOException("cannot read bounded Git output", failure.getCause());
            } catch (TimeoutException failure) {
                throw new IOException("Git output time limit exceeded", failure);
            }
            String result = utf8(bytes);
            require(process.exitValue() == 0, "Git " + arguments[0] + " failed with exit " + process.exitValue() + ": " + result.substring(0, Math.min(result.length(), 500)));
            budget.check();
            return result;
        } finally {
            if (process.isAlive()) process.destroyForcibly();
            output.cancel(true);
        }
    }

    public static void verifyReports(Path directory) throws IOException {
        Path root = checkedPath(directory, true);
        Budget budget = new Budget("report verification", REPORT_TIMEOUT);
        ReportCounts counts = new ReportCounts();
        Files.walkFileTree(root, Set.of(), REPORT_DEPTH, new SimpleFileVisitor<>() {
            private void visit(Path path) throws IOException {
                budget.check();
                require(++counts.entries <= REPORT_ENTRIES, "report directory entry limit exceeded");
                require(!Files.isSymbolicLink(path), "report symlink is not admissible: " + path);
            }

            @Override public FileVisitResult preVisitDirectory(Path path, BasicFileAttributes attributes) throws IOException {
                visit(path);
                return FileVisitResult.CONTINUE;
            }

            @Override public FileVisitResult visitFile(Path path, BasicFileAttributes attributes) throws IOException {
                visit(path);
                require(!attributes.isDirectory(), "report directory depth limit exceeded");
                if (path.getFileName().toString().toLowerCase(Locale.ROOT).endsWith(".xml")) {
                    require(++counts.files <= REPORT_FILES, "XML report file count limit exceeded");
                    byte[] bytes = readFile(path, REPORT_BYTES);
                    counts.bytes += bytes.length;
                    require(counts.bytes <= REPORT_TOTAL_BYTES, "total XML report byte limit exceeded");
                    checkReport(bytes, counts, budget);
                }
                return FileVisitResult.CONTINUE;
            }
        });
        budget.check();
        require(counts.files > 0 && counts.testcases > 0, "no executed testcases in selected XML reports");
        require(counts.required == 1, "required passing testcase must occur exactly once; found " + counts.required + ": " + TEST_CLASS + "#" + TEST_METHOD);
    }

    private static void checkReport(byte[] bytes, ReportCounts counts, Budget budget) throws IOException {
        try {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            factory.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true);
            factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
            factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
            factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
            factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
            factory.setAttribute(XMLConstants.ACCESS_EXTERNAL_DTD, "");
            factory.setAttribute(XMLConstants.ACCESS_EXTERNAL_SCHEMA, "");
            factory.setAttribute("http://www.oracle.com/xml/jaxp/properties/maxElementDepth", "128");
            factory.setXIncludeAware(false);
            factory.setExpandEntityReferences(false);
            DocumentBuilder parser = factory.newDocumentBuilder();
            parser.setEntityResolver((publicId, systemId) -> { throw new SAXException("external XML entities are forbidden"); });
            parser.setErrorHandler(new DefaultHandler() {
                @Override public void error(SAXParseException exception) throws SAXException { throw exception; }
                @Override public void fatalError(SAXParseException exception) throws SAXException { throw exception; }
            });
            Element root = parser.parse(new ByteArrayInputStream(bytes)).getDocumentElement();
            require(root.getTagName().equals("testsuite") || root.getTagName().equals("testsuites"), "XML report must have testsuite or testsuites root");
            require(root.getElementsByTagName("failure").getLength() == 0 && root.getElementsByTagName("error").getLength() == 0, "failure or error exists in selected XML reports");
            int casesBefore = counts.testcases;
            int suitesBefore = counts.suites;
            inspectSuite(root, counts, budget);
            require(counts.testcases - casesBefore == root.getElementsByTagName("testcase").getLength(), "misplaced testcase element in XML report");
            require(counts.suites - suitesBefore == 1 + root.getElementsByTagName("testsuite").getLength()
                    + root.getElementsByTagName("testsuites").getLength(), "misplaced suite element in XML report");
        } catch (ParserConfigurationException | SAXException failure) {
            throw new IOException("XML report was rejected by the secure parser", failure);
        }
    }

    private static void inspectSuite(Element suite, ReportCounts counts, Budget budget) throws IOException {
        budget.check();
        counts.suites++;
        if (suite.hasAttribute("tests")) {
            String tests = suite.getAttribute("tests");
            require(tests.matches("[0-9]{1,9}"), "malformed tests count in XML report");
            require(Long.parseLong(tests) == suite.getElementsByTagName("testcase").getLength(), "tests count contradicts testcase elements in XML report");
        }
        for (String attribute : List.of("failures", "errors")) {
            if (suite.hasAttribute(attribute)) {
                require(suite.getAttribute(attribute).matches("0+"), "nonzero or malformed " + attribute + " count in XML report");
            }
        }
        for (Node node = suite.getFirstChild(); node != null; node = node.getNextSibling()) {
            if (!(node instanceof Element element)) continue;
            if (element.getTagName().equals("testsuite") || element.getTagName().equals("testsuites")) {
                inspectSuite(element, counts, budget);
            } else if (element.getTagName().equals("testcase") && suite.getTagName().equals("testsuite")) {
                require(++counts.testcases <= REPORT_TESTCASES, "XML testcase count limit exceeded");
                if (element.getAttribute("classname").equals(TEST_CLASS) && element.getAttribute("name").equals(TEST_METHOD)) {
                    require(element.getElementsByTagName("skipped").getLength() == 0, "required native testcase was skipped");
                    require(!element.hasAttribute("status") || Set.of("run", "passed", "success").contains(element.getAttribute("status")), "required native testcase did not run");
                    require(!element.hasAttribute("result") || Set.of("completed", "passed", "success").contains(element.getAttribute("result")), "required native testcase did not complete");
                    require(++counts.required == 1, "duplicate required native testcase");
                }
            }
            budget.check();
        }
    }

    private static Path checkedPath(Path candidate, boolean directory) throws IOException {
        Path path = candidate.toAbsolutePath();
        Path current = path.getRoot();
        for (Path part : path) {
            require(!part.toString().equals(".."), "path traversal is not admissible: " + candidate);
            current = current.resolve(part);
            require(!Files.isSymbolicLink(current), "symlinked path is not admissible: " + candidate);
        }
        path = path.normalize();
        require(directory ? Files.isDirectory(path, LinkOption.NOFOLLOW_LINKS) : Files.isRegularFile(path, LinkOption.NOFOLLOW_LINKS), "required " + (directory ? "directory" : "regular file") + " is missing: " + path);
        return path;
    }

    private static Path safeRelative(Path root, String name) throws IOException {
        Path relative = Path.of(name);
        require(!relative.isAbsolute() && relative.getNameCount() > 0, "index path is not relative");
        for (Path part : relative) require(!part.toString().equals("..") && !part.toString().equals("."), "index path traversal");
        Path path = root.resolve(relative).normalize();
        require(path.startsWith(root) && !path.equals(root), "index path escapes worktree");
        return path;
    }

    private static byte[] readFile(Path file, int limit) throws IOException {
        Path path = checkedPath(file, false);
        require(Files.size(path) <= limit, "file byte limit exceeded: " + file);
        try (InputStream stream = Files.newInputStream(path, LinkOption.NOFOLLOW_LINKS)) {
            return readBounded(stream, limit, "file " + file);
        }
    }

    private static byte[] readBounded(InputStream stream, int limit, String label) throws IOException {
        byte[] bytes = stream.readNBytes(limit + 1);
        require(bytes.length <= limit, label + " byte limit exceeded");
        return bytes;
    }

    private static String utf8(byte[] bytes) throws IOException {
        return StandardCharsets.UTF_8.newDecoder().onMalformedInput(CodingErrorAction.REPORT)
                .onUnmappableCharacter(CodingErrorAction.REPORT).decode(ByteBuffer.wrap(bytes)).toString();
    }

    private static List<String> nulRecords(String text) throws IOException {
        if (text.isEmpty()) return List.of();
        require(text.endsWith("\0"), "Git record output is not NUL-terminated");
        return List.of(text.substring(0, text.length() - 1).split("\0", -1));
    }

    private static void require(boolean condition, String message) throws IOException {
        if (!condition) throw new IOException(message);
    }

    private record Pin(String url, String commit) { }
    private record Entry(String mode, String commit) { }
    private static final class ReportCounts { int entries; int files; int testcases; int suites; int required; long bytes; }
    private static final class Budget {
        private final String label;
        private final long deadline;
        Budget(String label, Duration duration) { this.label = label; deadline = System.nanoTime() + duration.toNanos(); }
        long remaining() throws IOException { long remaining = deadline - System.nanoTime(); require(remaining > 0, label + " time limit exceeded"); return remaining; }
        void check() throws IOException { remaining(); }
    }
}
