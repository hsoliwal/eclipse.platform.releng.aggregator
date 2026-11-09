# Release readiness for M3JDK21 (Java 21): eclipse.platform.releng.aggregator

Measured on 2026-11-09 against fork master `4fc0258ca6593077562750a8e22984f9987382a0` (upstream master `88da1d9dca4c`).
Tools and raw evidence: [`docs/m3/jdk21/release-20261109`](../jdk21/release-20261109/). Every gate ran locally on CPU; fork CI runs are not counted
(startup failures and queue starvation on this account, 2026-11).

| # | Gate | Verdict | Evidence |
| --- | --- | --- | --- |
| G1 | No Java 22+ requirement on master: BREE above JavaSE-21 (0), build/IDE pins above 21 (0), unnamed `_` (0), `import module` (0) | PASS; 7 exempt rows (EXEMPT.tsv, CENSUS_EXEMPT.tsv) | CENSUS.tsv (code view; hits inside strings, text blocks and comments: CENSUS_MASKED.tsv) |
| G2 | Java-21 compile gate: JDK 25 javac `--release 21` minus `--release 25` over 3 bundles (0 files, 3 roots); 0 baseline rows cancel | PASS (residue 0) | GATE_RESIDUE.tsv, GATE_SUMMARY.tsv |
| G2b | Parse gate: every tracked Java source (0 files, test bundles included, test-input folders excluded), JDK 25 javac `--release 21` stopped after parsing | PASS | PARSE_GATE.tsv |
| G3 | Recipe fixed point (`apply_jdk21.sh` + `apply_jdk21_pins.sh` change nothing on master) | PASS | RECIPE_CHANGES.tsv |
| G4 | Metadata consistent: Tycho bundle/feature versions match their pom, no EE above 21 in a Java-21 bundle | PASS | META.tsv |
| G5 | Tycho builds of the six SDK forks on JDK 21 (this repository has no own code bundle above Java 21 to build separately) | PASS 6/6 | g5/*.result.tsv; per-fork PRs; table below |
| G6 | Eclipse SDK product build and headless launch on JDK 21 | HOLD (disk) | F: free 9.1 GB, need 13.1 GB; section G6 below |

## SDK level (all forks, measured 2026-11-09)

| Fork | Master | Java-21 gate on master | G5 Tycho build on JDK 21.0.9 (PR head) | PR (draft) |
| --- | --- | --- | --- | --- |
| eclipse.jdt.debug | 6a67f7d657f4 | PASS (residue 0, parse 0) | PASS 7/7 modules, 245 s (7 ECJ NLS errors fixed first) | hsoliwal/eclipse.jdt.debug#20 |
| equinox | ad07c8a70da6 | FAIL: security.linux on java.lang.foreign (residue 175) | PASS 71/71, 128 s (JNA fill; needs equinox.binaries next to it) | hsoliwal/equinox#3 |
| eclipse.platform | 483f12644479 | FAIL: core.filesystem on java.lang.foreign (residue 255) | PASS 124/124, 250 s (JNA fill + 3 NLS fixes) | hsoliwal/eclipse.platform#32 |
| eclipse.platform.ui | 0b550d6e3d94 | PASS (residue 0, parse 0) | PASS 115/115, 515 s, against SWT RC 4eed16810f8f (17 NLS + 5 unused imports fixed) | hsoliwal/eclipse.platform.ui#59 |
| eclipse.jdt.ui | 85eadeb77ddc | FAIL: 2 test bundles do not parse (anchors after `"""`) | PASS 22/22, 372 s (anchor repair + 12 NLS fixes) | hsoliwal/eclipse.jdt.ui#19 |
| eclipse.jdt.core | f7fdb967a6bd | FAIL: jdt.core.tests.compiler does not parse (32 anchors after `"""`) | PASS 17/17, 236 s, first attempt | hsoliwal/eclipse.jdt.core#18 |
| eclipse.platform.releng.aggregator | 4fc0258ca659 | PASS (3 bundles residue 0, parse 0; scripts/ exempt) | G6 below | this PR |
| org.eclipse.emf, gef-classic | c7af8f211b39, a98142b17e26 | PASS (no Java 22+ bundle upstream, parse 0) | not in the G5 order | hsoliwal/org.eclipse.emf#3, hsoliwal/gef-classic#24 |

Every G5 build: `mvn -B clean verify -DskipTests -fae` on Oracle JDK 21.0.9 (Maven 3.9.14), fork eclipse-platform-parent
and eclipse-sdk-prereqs.target installed from this fork, other components from the upstream 4.42 I-build repository,
shared local repository F:/m3-scratch/m2-eclipse. Before each build `ecj_precheck.sh` runs the build's ECJ (3.47) with each
bundle's NLS / unused-import error settings and `fix_nls_tags.sh` / `fix_unused_imports.sh` apply its rows; on the masters it
reproduces every such row the builds found (jdt.debug 7, platform 3, platform.ui 22, jdt.ui 1).

Recipes behind the NLS rows (CNPCDA anchors next to the fixed lines, lane PR bodies): **M3LinearStringBuilderRecipe**
(strings lane L1, crate `recipes/recipe-crates/m3-eclipse-strings-lane-20261023`, anchors `M14/M33 M3STRING_COMPOSITE`)
writes `"" + x` without `//$NON-NLS-1$`; **M3HoistConstantPatternCompileRecipe** and
**M3HoistConstantStringRegexCallsRecipe** (regex lane L1/L1b, crate `recipes/recipe-crates/m3-eclipse-regex-lane-20261023`,
anchor `M12 REGEX_PRECOMPUTE CALL`) hoist literals into `Pattern` fields without a tag and leave the old tags at the call
site. The platform.ui rows (M3SparseExtents, M3HeapGrowth, M3Marker*, M3ViewersTest, M3SparseExtentsTest) are fork-added
M3 classes, not recipe output.

### SWT

platform.ui master needs SWT fork API (`SWT.PartVisible`, `Control.isPartVisible()` in org.eclipse.ui.workbench
M3PartVisibility), absent from the upstream I-build SWT. G5 of platform.ui used the SWT release candidate,
hsoliwal/eclipse.platform.swt `m3/release-candidate-20261109` (PR #335) at **4eed16810f8f2b06d267d71c957021a7dc4aafbd**, built
on JDK 21.0.9 (org.eclipse.swt + the 8 fragments of eclipse-platform-parent, 9/9 BUILD SUCCESS) and resolved as
org.eclipse.swt 3.138.0.v20261109-1202. The SWT gitlink of this aggregator (5cd3795d948e) predates that API; it should move
to the SWT release commit together with the fork gitlinks after the fork PRs merge.

### Submodules (gitlinks of master `4fc0258ca659`)

| Submodule | Remote | Gitlink | vs fork/upstream master | Java level at gitlink |
| --- | --- | --- | --- | --- |
| eclipse.platform.swt | hsoliwal fork | 5cd3795d948e | 119 commits behind fork master; the SWT RC (4eed16810f8f) carries the API platform.ui needs | org.eclipse.swt 3.138.0.qualifier, JavaSE-21, 0 of 53 manifests above 21 |
| eclipse.platform.ui | hsoliwal fork | 783d04c1b2fe | 4 behind master | gate PASS on master |
| eclipse.platform | hsoliwal fork | c26284637e31 | 1 behind master | FFM residue until PR #32 |
| equinox | hsoliwal fork | ad07c8a70da6 | = master | FFM residue until PR #3 |
| eclipse.jdt.core / .debug / .ui | hsoliwal forks | a0c392388 / 046c97707 / f4ea08861 | 1 behind master each | see table above |
| eclipse.pde | upstream eclipse-pde | ba6a5d6f2f45 | 10 behind upstream master | 0 of 404 manifests above JavaSE-21, no 22+ pins |
| equinox.p2 | upstream eclipse-equinox/p2 | bc63431121cc | 2 behind upstream master | 0 of 94 manifests above JavaSE-21 |
| eclipse.jdt | upstream | 28561c3c115d | = upstream master | 0 |
| eclipse.jdt.core.binaries, equinox.binaries | upstream | 987122d226c7, 7a1125f75ed9 | binaries | no Java sources |

SWT version: every fork requires `org.eclipse.swt` with a lower bound of at most 3.135.0; gitlink, SWT master and the RC all
carry 3.138.0.

### Products and target platform

| Item | Fork | Upstream master |
| --- | --- | --- |
| products/eclipse-sdk/sdk.product `-Dosgi.requiredJavaVersion` | 21 | 25 |
| products/eclipse-platform/platform.product `-Dosgi.requiredJavaVersion` | 21 | 25 |
| equinox-sdk.product, EclipseRTOSGiStarterKit.product | no Java requirement | no Java requirement |
| eclipse-platform-parent: Tycho 5.0.4, no requireJavaVersion enforcer, EE JavaSE-21 in the tycho-eclipse-plugin config | consistent | |
| eclipse-sdk-prereqs.target: com.sun.jna 5.19.1 (needed by the two JNA fills) | present | present |
| README "Build requirements: Java 25 or higher" | inconsistent with M3JDK21 (doc only, not changed here) | |

`scripts/` (releng CI tooling run by jobs/builds/*.jenkinsfile as multi-file source programs, JEP 458, JDK 22+) keeps
JavaSE-25 and three unnamed lambdas; it is not part of the Maven/Tycho product build and is listed in EXEMPT.tsv.

## G6: Eclipse SDK product build and launch on JDK 21 - HOLD (disk)

Rule for this run: attempt G6 only with at least 12 GB free on F: (the only approved drive). Measured after G5 and after
deleting every clone, target/ and temp directory of this lane (F:/m3-scratch/m2-eclipse kept): **F: free 9.1 GB
(9318 MB of 117312 MB)**. G6 was not started.

Measured need of `mvn -B clean verify -DskipTests` of this aggregator with the six fork PR heads + SWT RC 4eed16810f8f:

| Part | Size | Source of the number |
| --- | --- | --- |
| Component checkouts (12 submodules, depth 1) | 1.2 GB | git ls-tree of the checked-out trees (0.89 GB) + pack sizes |
| Module target/ directories (~650 modules) | 1.7 GB | G5 measured 737 MB for 278 modules (platform 313, platform.ui 193, jdt.ui 124, jdt.core 107 MB) = 2.65 MB/module |
| SDK product, 8 environments | 4.6 GB | upstream I20261108-2300: SDK archive 287 MB per environment, plus the materialized product directory of about the same size |
| Platform product, 8 environments | 1.4 GB | upstream I20261108-2300: 86 MB per environment, archive + directory |
| p2 repository site | 0.7 GB | upstream repository-I20261108-2300.zip 363 MB, zip + directory |
| Local Maven/p2 repository growth | 0.5 GB | F:/m3-scratch/m2-eclipse is 853 MB after G5 |
| **Total** | **10.1 GB** | plus the 3 GB floor kept free on F: = **13.1 GB needed vs 9.1 GB free** |

Time: G5 compiled 356 fork modules in 1,746 s of build time; the full reactor (~650 modules) plus product assembly for 8
environments fits the 2-hour budget. Disk is the only blocker.

Where the rest of F: is: see `F_USAGE.tsv` next to this file (largest directories on F:, MB).

User actions to release G6: free at least 4 GB more on F: (or approve another drive), merge the fork PRs, move the
submodule gitlinks to the merged masters and to the SWT release commit, then run G6 (SDK product build, then
`eclipse -nosplash -application org.eclipse.equinox.p2.director -listInstalledRoots` on JDK 21).

## Re-run

```bash
git clone --depth 1 https://github.com/hsoliwal/eclipse.platform.releng.aggregator.git && git -C eclipse.platform.releng.aggregator remote add upstream <upstream>
git -C eclipse.platform.releng.aggregator fetch --depth 1 --filter=blob:none upstream master:refs/remotes/upstream/master
bash docs/m3/jdk21/release-20261109/gate_master.sh eclipse.platform.releng.aggregator    # paths at the top of the script; JAVAC = JDK 25 javac
bash docs/m3/jdk21/release-20261109/meta_check.sh eclipse.platform.releng.aggregator > META.tsv
```

The gate compiles every bundle that upstream master declares JavaSE-22 or newer, plus the 2026-10-20 list, against the
newest jar of every bundle in a p2 pool. Errors in both runs are classpath noise (APIs newer than the pool); what remains
after `--release 21` is the Java 22+ residue and must be empty.
