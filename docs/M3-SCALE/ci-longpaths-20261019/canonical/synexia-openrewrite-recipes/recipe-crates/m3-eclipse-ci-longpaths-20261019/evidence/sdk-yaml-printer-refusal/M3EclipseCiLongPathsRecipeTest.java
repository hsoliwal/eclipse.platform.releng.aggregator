// SPDX-FileCopyrightText: 2026 Hitesh Soliwal and Contributors to the Synexia Project
// SPDX-License-Identifier: Apache-2.0
package com.synexia.rewrite;

import static org.junit.jupiter.api.Assertions.*;

import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HexFormat;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.TreeMap;
import java.util.concurrent.Callable;
import java.util.concurrent.Executors;
import org.junit.jupiter.api.Test;
import org.openrewrite.InMemoryExecutionContext;
import org.openrewrite.Parser;
import org.openrewrite.Recipe;
import org.openrewrite.SourceFile;
import org.openrewrite.config.Environment;
import org.openrewrite.config.YamlResourceLoader;
import org.openrewrite.internal.InMemoryLargeSourceSet;
import org.openrewrite.text.PlainTextParser;
import org.openrewrite.yaml.YamlParser;
import org.openrewrite.yaml.tree.Yaml;

/** Qualifies exact SDK output; hosted Windows checkout remains a separate gate. */
final class M3EclipseCiLongPathsRecipeTest {
    private static final String CRATE = "m3-eclipse-ci-longpaths-20261019";
    private static final String NAME = "com.synexia.eclipse.CiLongPaths20261019";
    private static final String TARGET = ".github/workflows/mavenBuild.yml";
    private static final String ROOT = "/com/synexia/rewrite/hash-pinned-text/" + CRATE + "/";
    private static final String BEFORE_SHA = "b9ba4a35ef634726477534373fc39ed23d5185254ee71ecf1ff63475830742e8";
    private static final String AFTER_SHA = "23522344c0010e850bdc279312e9c0ebf546f0af97162e51d59024d533d4c0d9";
    private static final String CHECKOUT = "    - name: Checkout\n";
    private static final String WINDOWS_STEP =
            "    - name: Enable long paths on Windows\n"
            + "      if: runner.os == 'Windows'\n"
            + "      run: git config --global core.longpaths true\n";

    private static String resource(String name) throws Exception {
        try (var input = M3EclipseCiLongPathsRecipeTest.class.getResourceAsStream(name)) {
            assertNotNull(input, name);
            return new String(input.readAllBytes(), StandardCharsets.UTF_8);
        }
    }

    private static String before() throws Exception { return resource(ROOT + "before-mavenBuild.yml.txt"); }
    private static String after() throws Exception { return resource(ROOT + "mavenBuild.yml.txt"); }

    private static String sha(String value) throws Exception {
        return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256")
                .digest(value.getBytes(StandardCharsets.UTF_8)));
    }

    private static InMemoryExecutionContext context() {
        return new InMemoryExecutionContext(error -> { throw new AssertionError(error); });
    }

    private static List<SourceFile> parse(Map<String, String> input) {
        var result = new ArrayList<SourceFile>();
        for (var source : input.entrySet()) {
            result.addAll(PlainTextParser.builder().build().parseInputs(
                    List.of(Parser.Input.fromString(Path.of(source.getKey()), source.getValue())),
                    null, context()).toList());
        }
        return result;
    }

    private static Recipe namedRecipe() throws Exception {
        try (var input = M3EclipseCiLongPathsRecipeTest.class.getResourceAsStream(
                "/META-INF/rewrite/" + CRATE + ".yml")) {
            assertNotNull(input);
            var loader = new YamlResourceLoader(input, URI.create("classpath:/" + CRATE), new Properties());
            var recipe = Environment.builder().load(loader).build().activateRecipes(NAME);
            assertTrue(recipe.validateAll().stream().allMatch(org.openrewrite.Validated::isValid));
            return recipe;
        }
    }

    private static Map<String, String> run(Recipe recipe, List<SourceFile> input) {
        var output = new TreeMap<String, String>();
        for (var change : recipe.run(new InMemoryLargeSourceSet(input), context(), 1)
                .getChangeset().getAllResults()) {
            assertNotNull(change.getBefore(), "This recipe admits no new workflow");
            assertNotNull(change.getAfter(), "This recipe deletes no workflow");
            var path = change.getAfter().getSourcePath().toString().replace('\\', '/');
            assertNull(output.put(path, change.getAfter().printAll()), "duplicate emitted path");
        }
        return output;
    }

    private static Map<String, String> run(List<SourceFile> input) throws Exception {
        return run(namedRecipe(), input);
    }

    private static Map<String, String> withDecoys() throws Exception {
        var input = new TreeMap<String, String>();
        input.put(TARGET, before());
        input.put("notes/decoy.yml", "literal: |\n  git config --global core.longpaths true\n"
                + "  if (runner.os == 'Windows') { Checkout(); }\n");
        input.put(".github/workflows/other.yml", before());
        return input;
    }

    private static void assertWorkflowContract(String output) throws Exception {
        assertEquals(BEFORE_SHA, sha(before()), "frozen upstream preimage");
        assertEquals(AFTER_SHA, sha(output), "reviewed three-line correction");
        assertTrue(output.contains(WINDOWS_STEP + CHECKOUT), "Windows setup must precede checkout");
        assertEquals(output.indexOf(WINDOWS_STEP), output.lastIndexOf(WINDOWS_STEP), "one setup step");
        assertEquals(before(), output.replace(WINDOWS_STEP, ""),
                "Every original permission, trigger, pin, input, profile and gate remains byte-identical");
        var parsed = YamlParser.builder().build().parseInputs(
                List.of(Parser.Input.fromString(Path.of(TARGET), output)), null, context()).toList();
        assertEquals(1, parsed.size());
        assertInstanceOf(Yaml.Documents.class, parsed.getFirst(), "actual YAML parser admission");
        assertEquals(output, parsed.getFirst().printAll(), "YAML round-trip byte identity");
    }

    @Test void namedRecipeCorrectsWindowsCheckoutAndMaterializes() throws Exception {
        var output = run(parse(Map.of(TARGET, before())));
        assertEquals(1, output.size(), "The SDK must emit the Windows checkout correction");
        assertEquals(Map.of(TARGET, after()), output);
        assertWorkflowContract(output.get(TARGET));
        String destination = System.getProperty("materialize.dir", "");
        if (!destination.isBlank()) {
            Path target = Path.of(destination).resolve(TARGET);
            Files.createDirectories(target.getParent());
            Files.writeString(target, output.get(TARGET), StandardCharsets.UTF_8);
        }
    }

    @Test void reviewedPostimageIsFixedPointAndManifestIsClosed() throws Exception {
        var owner = new M3HashPinnedTextSnapshotRecipe(CRATE);
        assertEquals(List.of(TARGET), owner.targetPaths());
        assertEquals(Map.of(TARGET, BEFORE_SHA), owner.preimageManifest());
        assertWorkflowContract(after());
        assertTrue(run(parse(Map.of(TARGET, after()))).isEmpty());
        assertTrue(run(owner, parse(Map.of(TARGET, after()))).isEmpty());
    }

    @Test void missingAndDriftedWorkflowRefuse() throws Exception {
        assertThrows(IllegalStateException.class, () -> run(List.of()));
        assertThrows(IllegalStateException.class,
                () -> run(parse(Map.of(".github/workflows/MavenBuild.yml", before()))));
        String baseline = before();
        var drift = List.of(
                baseline + "\n# changed upstream source\n",
                baseline.replace("fetch-depth: 0", "fetch-depth: 1"),
                baseline.replace("permissions: {}", "permissions: { contents: write }"),
                baseline.replace("submodules: ${{ inputs.submodules }}", "submodules: false"),
                baseline.replace("3d3c42e5aac5ba805825da76410c181273ba90b1", "0000000000000000000000000000000000000000"),
                baseline.replace("\n", "\r\n"));
        for (String changed : drift) {
            assertNotEquals(baseline, changed);
            assertThrows(IllegalStateException.class, () -> run(parse(Map.of(TARGET, changed))));
        }
    }

    @Test void duplicateAndNoncanonicalTargetPathsRefuse() throws Exception {
        var duplicate = parse(Map.of(TARGET, before()));
        duplicate.addAll(parse(Map.of(TARGET, before())));
        assertThrows(IllegalStateException.class, () -> run(duplicate));
        for (String alias : List.of(".github/./workflows/mavenBuild.yml",
                ".github/workflows/../workflows/mavenBuild.yml")) {
            assertThrows(IllegalStateException.class, () -> run(parse(Map.of(alias, before()))));
        }
        if (Path.of(TARGET).getFileSystem().getSeparator().equals("/")) {
            assertThrows(IllegalStateException.class,
                    () -> run(parse(Map.of(".github\\workflows\\mavenBuild.yml", before()))));
        }
    }

    @Test void unrelatedSourcesAndInputPermutationsArePreserved() throws Exception {
        var input = parse(withDecoys());
        assertEquals(Map.of(TARGET, after()), run(input));
        Collections.reverse(input);
        assertEquals(Map.of(TARGET, after()), run(input));
    }

    @Test void directNamedSerialAndTwoWorkerReplaysAgree() throws Exception {
        var expected = Map.of(TARGET, after());
        assertEquals(expected, run(new M3HashPinnedTextSnapshotRecipe(CRATE), parse(withDecoys())));
        assertEquals(expected, run(parse(withDecoys())));
        var trials = new ArrayList<Callable<Map<String, String>>>();
        for (int i = 0; i < 4; i++) trials.add(() -> run(parse(withDecoys())));
        try (var pool = Executors.newFixedThreadPool(2)) {
            for (var future : pool.invokeAll(trials)) assertEquals(expected, future.get());
        }
        assertEquals(expected, run(parse(withDecoys())));
    }
}
