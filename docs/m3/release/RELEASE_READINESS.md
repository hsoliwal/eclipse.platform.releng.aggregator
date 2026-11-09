# Release readiness for M3JDK21 (Java 21): eclipse.platform.releng.aggregator

Measured on 2026-11-09 against fork master `4fc0258ca6593077562750a8e22984f9987382a0` (upstream master `88da1d9dca4c`).
Tools and raw evidence: [`docs/m3/jdk21/release-20261109`](../jdk21/release-20261109/). Every gate ran locally on CPU; fork CI runs are not counted
(startup failures and queue starvation on this account, 2026-11).

| # | Gate | Verdict | Evidence |
| --- | --- | --- | --- |
| G1 | No Java 22+ requirement on master: BREE above JavaSE-21 (0), build/IDE pins above 21 (0), unnamed `_` (0), `import module` (0) | PASS; 7 exempt rows (EXEMPT.tsv, CENSUS_EXEMPT.tsv) | CENSUS.tsv (code view; hits inside strings, text blocks and comments: CENSUS_MASKED.tsv) |
| G2 | Java-21 compile gate: JDK 25 javac `--release 21` minus `--release 25` over 3 bundles (16 files, 3 roots); 0 baseline rows cancel | PASS (residue 0) | GATE_RESIDUE.tsv, GATE_SUMMARY.tsv |
| G2b | Parse gate: every tracked Java source (61 files, test bundles included, test-input folders excluded), JDK 25 javac `--release 21` stopped after parsing | PASS | PARSE_GATE.tsv |
| G3 | Recipe fixed point (`apply_jdk21.sh` + `apply_jdk21_pins.sh` change nothing on master) | PASS | RECIPE_CHANGES.tsv |
| G4 | Metadata consistent: Tycho bundle/feature versions match their pom, no EE above 21 in a Java-21 bundle | PASS | META.tsv |
| G5 | Full Tycho build of this repository on JDK 21 (`mvn -B clean verify -DskipTests`, fork parent + SDK target from the fork aggregator, other components from the upstream 4.42 I-build repository) | PENDING | not run yet |
| G6 | Eclipse SDK product build and launch on JDK 21 | PENDING | aggregator verdict, eclipse.platform.releng.aggregator docs/m3/release/RELEASE_READINESS.md |

## SDK level (all forks, measured 2026-11-09)

| Fork | Master | Java-21 gate on master | PR (draft) |
| --- | --- | --- | --- |
| eclipse.jdt.debug | 6a67f7d657f4 | PASS (residue 0, parse 0) | hsoliwal/eclipse.jdt.debug#20 (docs) |
| equinox | ad07c8a70da6 | FAIL: org.eclipse.equinox.security.linux on java.lang.foreign (residue 175) | hsoliwal/equinox#3 (JNA fill, residue 0) |
| eclipse.platform | 483f12644479 | FAIL: org.eclipse.core.filesystem on java.lang.foreign (residue 255) | hsoliwal/eclipse.platform#32 (JNA fill, residue 0) |
| eclipse.platform.ui | 0b550d6e3d94 | PASS (residue 0, parse 0) | hsoliwal/eclipse.platform.ui#59 (docs) |
| eclipse.jdt.ui | 85eadeb77ddc | FAIL: 2 test bundles do not parse (anchors after `"""`, 10 rows) | hsoliwal/eclipse.jdt.ui#19 (anchor repair, residue 0) |
| eclipse.jdt.core | f7fdb967a6bd | see its PR | hsoliwal/eclipse.jdt.core (gate running) |
| eclipse.platform.releng.aggregator | 4fc0258ca659 | PASS (3 bundles residue 0, parse 0; scripts/ exempt) | this PR |
| org.eclipse.emf, gef-classic | c7af8f211b39, a98142b17e26 | not SDK submodules; no Java 22+ bundle upstream (0 gated) | see their PRs |

### Submodules (gitlinks of master `4fc0258ca659`)

| Submodule | Remote | Gitlink | vs fork/upstream master | Java level at gitlink |
| --- | --- | --- | --- | --- |
| eclipse.platform.swt | hsoliwal fork | 5cd3795d948e | 119 commits behind fork master 378a99d34612; candidate PR hsoliwal/eclipse.platform.swt#325 head 64453d9bc00c is 39 ahead | org.eclipse.swt 3.138.0.qualifier, JavaSE-21, 0 of 53 manifests above 21; MANIFEST.MF files identical at gitlink, master and candidate |
| eclipse.platform.ui | hsoliwal fork | 783d04c1b2fe | 4 behind master | gate PASS on master |
| eclipse.platform | hsoliwal fork | c26284637e31 | 1 behind master | FFM residue until PR #32 |
| equinox | hsoliwal fork | ad07c8a70da6 | = master | FFM residue until PR #3 |
| eclipse.jdt.core / .debug / .ui | hsoliwal forks | a0c392388 / 046c97707 / f4ea08861 | 1 behind master each | see table above |
| eclipse.pde | upstream eclipse-pde | ba6a5d6f2f45 | 10 behind upstream master | 0 of 404 manifests above JavaSE-21, no 22+ pins |
| equinox.p2 | upstream eclipse-equinox/p2 | bc63431121cc | 2 behind upstream master | 0 of 94 manifests above JavaSE-21 |
| eclipse.jdt | upstream | 28561c3c115d | = upstream master | 0 |
| eclipse.jdt.core.binaries, equinox.binaries | upstream | 987122d226c7, 7a1125f75ed9 | binaries | no Java sources |

SWT alignment: every fork requires `org.eclipse.swt` with a lower bound of at most 3.135.0; the gitlink, SWT master and the
SWT candidate all carry 3.138.0, so the version is aligned. The gitlink itself lags SWT master by 119 commits.

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
