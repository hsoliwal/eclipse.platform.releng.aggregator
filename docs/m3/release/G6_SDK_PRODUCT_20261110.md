# G6: Eclipse SDK product build and headless launch on JDK 21 (2026-11-10)

Aggregator: hsoliwal/eclipse.platform.releng.aggregator master **9948656c21a11563d89186c61ff92319702e5338** (#17). All 12
submodules come from hsoliwal forks (see `g6-20261110/submodules.final.txt`), at their pinned commits:
eclipse.jdt 28561c3c115d, eclipse.jdt.core 617d2cc38309, eclipse.jdt.core.binaries 987122d226c7, eclipse.jdt.debug
6b077f8147ef, eclipse.jdt.ui 785cf01205b0, eclipse.pde ba6a5d6f2f45 (hsoliwal/initiative31-eclipse.pde, branch
upstream-master), eclipse.platform 776e96e6c8f4, eclipse.platform.swt b4579e0a346e, eclipse.platform.ui 38238345c75c,
equinox 7ed67c081fca, equinox.binaries 7a1125f75ed9, equinox.p2 bc63431121cc.

Build: `mvn -B clean verify -DskipTests -fae -nsu -Dtycho.localArtifacts=ignore -Dosgi.os=linux -Dosgi.ws=gtk
-Dosgi.arch=x86_64` (Maven 3.9.14, Tycho 5.0.4) on Oracle JDK **21.0.9**, local repository F:/m3-scratch/m2-eclipse,
Maven Central first (`settings-central-first.xml`). Products for all 8 environments of eclipse-platform-parent.

Where: one expandable NTFS VHDX inside the user-approved directory I:/m3-sdk-build-20261110 (I: is exFAT with 1 MB
allocation units: every one of the 86,857 checkout files takes at least 1 MB, so a first plain clone filled I: at about
19k files and was deleted), mounted as a temporary drive letter for the run, detached and deleted afterwards.

## Result: PASS for the SDK product (build + headless launch on JDK 21)

| Item | Result | Evidence |
| --- | --- | --- |
| Eclipse SDK product (org.eclipse.sdk.ide), 8 environments | BUILD SUCCESS (14:53 min) | `g6-20261110/products.sha256` (win32.x86_64 zip `766586e691b39aa18945e456379a3086bbf9db99e58dd531db2456a82dbd9d8c`) |
| Eclipse Platform product, equinox-launcher, OSGi Starter Kit, eclipse-platform-repository | BUILD SUCCESS | `products.sha256`, `build.log.gz` |
| Reactor (attempt 6) | 530 modules ok, 3 failed, 3 skipped, 5984 s | `build.result.tsv`, `BUILD_ATTEMPTS.tsv` |
| Failed modules (no product depends on them) | org.eclipse.swt.tests, org.eclipse.equinox.p2.tests, equinox-sdk-repository | section "Not fixed here" |
| Headless launch, SDK win32.x86_64, JDK 21.0.9: `eclipsec -nosplash -consoleLog -vm <jdk-21>/bin/javaw.exe -application org.eclipse.equinox.p2.director -listInstalledRoots -profile SDKProfile` | exit 0; roots `org.eclipse.sdk.ide/4.42.0.I20261110-1028`, `org.eclipse.e4.core.tools.feature.feature.group`, `org.eclipse.terminal.feature.feature.group`, `org.eclipse.tips.feature.feature.group` | `launch-eclipse-sdk-listInstalledRoots.txt` |
| `-version` launch (same product) | the p2 director has no `-version` option (exit 13), but the session header records `eclipse.buildId=4.42.0.I20261110-1028`, `java.version=21.0.9`, `OS=win32, ARCH=x86_64, WS=win32` | `launch-eclipse-sdk-version.txt` |
| Product Java requirement | eclipse.ini `-Dosgi.requiredJavaVersion=21` | `eclipse.eclipse-sdk.ini` |
| Eclipse Platform product, same launch | exit 0; `org.eclipse.platform.ide/4.42.0.I20261110-1028` | `launch-eclipse-platform-listInstalledRoots.txt` |

## Fixes the SDK build needed on JDK 21

| # | Where | Problem on JDK 21 | Fix | PR |
| --- | --- | --- | --- | --- |
| 1 | eclipse-platform-parent/pom.xml, tycho-document-bundle-plugin | `pdeToolsRepository` = the 4.42 I-builds; their PDE schema tools need org.eclipse.core.filesystem 1.12.0.v20261023 (JavaSE-25) and do not resolve on JDK 21 (`schema-to-html` in org.eclipse.platform.doc.isv) | tools from the previous release `${previous-release.baseline}` (4.41 R, Java 21) | this PR |
| 2 | eclipse-platform-parent/pom.xml, maven-javadoc-plugin | `<source>25</source>`: javadoc 21 `invalid source release: 25` | `<source>21</source>`; the pins recipe now covers `<source>2x</source>` (apply_jdk21_pins.sh, census in gate_master.sh) | this PR |
| 3 | eclipse.platform.ui M3SparseExtents.java:23 | doclint `reference not found`: `{@link M3ScrollMetrics}` (no such class) | `{@code M3ScrollMetrics}` | hsoliwal/eclipse.platform.ui#63 |
| 4 | eclipse.platform.swt Button.java:314 (win32) | doclint `unknown tag: String`: `@return ArrayList<String> styles` (not upstream) | `{@code ArrayList<String>}` | hsoliwal/eclipse.platform.swt#341 |
| 5 | eclipse.jdt.core ASTNode.java:1887 | doclint `text not allowed in <ul> element`: a `//FLLDCIM:` anchor inside the Javadoc | anchor moved above the `/**` | hsoliwal/eclipse.jdt.core#19 |
| 6 | build environment | on Windows the reactor builds org.eclipse.swt.svg before the win32 fragment (it orders only the GTK x86_64 fragment ahead, as on the upstream Linux CI) | compile environment set to linux/gtk/x86_64 (`-Dosgi.os/ws/arch`); products still for all 8 environments | (build option) |

Fixes 3 to 5 were applied in the build tree on top of the pinned commits (diff in `g6-20261110/build-tree.diff`); fixes 1
and 2 are this PR's change to eclipse-platform-parent/pom.xml.

## Attempts

| Attempt | Status | Seconds | ok / failed / skipped | Stopped at | Fix |
| --- | --- | --- | --- | --- | --- |
| 1 | FAILURE | 1256 | 252 / 1 / 283 | org.eclipse.swt.svg compiled before the win32 SWT fragment (Windows reactor order) | `-Dosgi.os=linux -Dosgi.ws=gtk -Dosgi.arch=x86_64` |
| 2 | FAILURE | 1752 | 515 / 4 / 17 | doc.isv `schema-to-html`: PDE tools from the 4.42 I-build need JavaSE-25 | pdeToolsRepository -> 4.41 release |
| 3 | FAILURE | 1700 | 515 / 4 / 17 | doc.isv javadoc: `invalid source release: 25` | javadoc `<source>21</source>` |
| 4 | stopped | - | - | doc.isv javadoc doclint: M3SparseExtents, SWT Button | platform.ui #63, SWT #341 |
| 5 | stopped | - | - | jdt.doc.isv javadoc doclint: anchor inside ASTNode Javadoc | jdt.core #19 |
| 6 | FAILURE (non-product modules only) | 5984 | 530 / 3 / 3 | swt.tests, equinox.p2.tests, equinox-sdk-repository | see below |

Raw: `g6-20261110/BUILD_ATTEMPTS.tsv`, attempt-6 log `build.log.gz`, its `[ERROR]` rows `build.errors.txt.gz`.

## Not fixed here (recorded for their owners)

| Module | Rows | Cause | Owner / next step |
| --- | --- | --- | --- |
| org.eclipse.swt.tests | 3,531 ECJ errors | fork test classes use SWT internal packages that the SWT bundles do not export (`Access restriction ... not accessible`, e.g. internal.render, internal.m3.collections, internal.gpu), some of them win32-only (unresolved when compiled for linux/gtk); plus 7 Javadoc errors (`'public' visibility for malformed doc comments hides this 'default' reference`) | SWT lane: export the internal test packages (x-friends) or move the tests; Javadoc rows: SWT PR (doc-only) |
| org.eclipse.equinox.p2.tests, equinox-sdk-repository | resolution | `org.eclipse.swt 3.138.0 requires 'eclipse.swt; (&(implementation=native)(version=3.135.100))'` not satisfied in the win32 (p2.tests materialize-products) and linux/ppc64le (repository) contexts, via org.eclipse.equinox.p2.installer 1.5.0.v20261028-0714 (built in this reactor; its qualifier is the git date of the p2 pointer) | under investigation, see the follow-up note below |
