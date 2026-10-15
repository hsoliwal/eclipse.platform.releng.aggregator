<!-- fork-homepage-detail:v1:start -->
# Eclipse SDK aggregator: assemble the complete development platform

This repository joins the Eclipse Platform, SWT, UI, JDT, PDE and Equinox
components into an Eclipse SDK build, products and p2 update site. It is the
integration checkout for release engineering and full-SDK verification. Develop
an isolated component change in its owning repository first, then integrate its
exact revision here.

[Build map](#sdk-build-map) · [Concepts](#sdk-key-concepts) ·
[Quickstart](#sdk-quickstart) · [Example](#sdk-worked-example) ·
[Detailed reference](docs/source-reference/README.md)

## SDK build map

| Area | Responsibility |
| --- | --- |
| [.gitmodules](.gitmodules) | Component repository URLs and checkout locations |
| [pom.xml](pom.xml) | Top-level Maven reactor and assembly order |
| [eclipse-platform-parent/](eclipse-platform-parent/) | Shared Maven/Tycho, toolchain and verification configuration |
| [eclipse.platform.releng.prereqs.sdk/](eclipse.platform.releng.prereqs.sdk/) | Prerequisite target-platform definition |
| [products/](products/) | Eclipse Platform and SDK product assembly |
| [sites/](sites/) | p2 repository and site assembly |
| [RELENG.md](RELENG.md) and [RELEASE.md](RELEASE.md) | Build operations and release checklist |

## SDK key concepts

- **Aggregator:** coordinates component builds and packaging; it does not replace
  the source ownership of SWT, JDT, PDE or other projects.
- **Submodule / gitlink:** a component checkout at a commit recorded by the parent
  repository. A recursive clone uses those recorded commits, not every latest tip.
- **Reactor:** Maven's set of modules participating in this build.
- **Target platform:** the Eclipse dependencies Tycho resolves for compilation
  and execution; it is different from the JDK that launches Maven.
- **Product / p2 repository:** a runnable Eclipse distribution versus an update
  repository containing installable bundles and features.
- **BREE:** a bundle's required execution environment. The build JDK and BREE are
  distinct inputs; use the documented toolchains for the `bree-libs` lane.

## SDK fork status

This is [hsoliwal's downstream fork](https://github.com/hsoliwal/eclipse.platform.releng.aggregator)
of the [Eclipse SDK aggregator](https://github.com/eclipse-platform/eclipse.platform.releng.aggregator).
The inspected [.gitmodules](.gitmodules) still uses upstream component URLs.
Cloning this fork does not automatically include changes in the sibling hsoliwal
component forks. The [coverage ledger](docs/source-reference/COVERAGE.md) documents
the inspected source boundaries; an inventory or opt-in research lane is not an
SDK compatibility, release or performance qualification.

## SDK quickstart

The retained build instructions below require **Java 25+ and Maven 3.9.12+**.
Also provide Git, network access to component/Maven/p2 repositories, sufficient
disk space and the native/display prerequisites of the selected test platforms.
For an IDE workspace see [the Oomph setup](oomph/PlatformSDKConfiguration.setup).

```sh
git clone --recurse-submodules https://github.com/hsoliwal/eclipse.platform.releng.aggregator.git
cd eclipse.platform.releng.aggregator
git rev-parse HEAD
git submodule status --recursive
java -version
mvn -version
mvn clean verify
```

The full test build can be lengthy. Commands here describe the checked-in entry
points; this homepage update did not run the SDK build or its tests.

## SDK command cheat sheet

```sh
# Review the recorded component commits and local differences.
git submodule status --recursive
git diff --submodule=log
# Initialize missing component checkouts at the recorded commits.
git submodule update --init --recursive
# Packaging lane only: skipped tests must be reported as skipped.
mvn clean verify -DskipTests --threads 1C
```

After a successful assembly, inspect `products/eclipse-sdk/target/products`,
`products/eclipse-platform/target/products` and
`sites/eclipse-platform-repository/target/repository`.
Missing submodules, dependency-resolution failures and failing tests are different
failure boundaries. Do not use destructive cleanup commands as routine setup;
the existing cleanup section below explains their data-loss consequences.

## SDK worked example

**Check whether an SDK build really contains a sibling SWT change.**

1. Read `.gitmodules` to identify the SWT checkout and its remote.
2. Read `git submodule status --recursive` and record its actual SWT commit.
   A leading `-` means uninitialized, `+` means a different checkout commit and
   `U` indicates a merge conflict.
3. Compare that exact commit with the intended SWT change. The aggregator's fork
   name and a successful recursive clone do not establish inclusion.
4. If integration changes are needed, review the component commit and parent
   gitlink change explicitly. Keep the component test evidence with the SDK run.
5. After building, verify both the assembled product and test reports; a produced
   archive with skipped tests is packaging evidence only.

Use [the source reference](docs/source-reference/README.md) for module/package
navigation and [RELEASE.md](RELEASE.md) before release work. Original upstream
build, contribution and licensing documentation is retained below.

> Source tour checked at [`98a846bf6264`](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/tree/98a846bf62648d30bb7871e3c8a61d6888761f25). Commands describe that revision; recheck build configuration when changing revisions. Build/UI/performance verification was not run for this README update.

---

<!-- fork-homepage-detail:v1:end -->

## M3 direction in this fork

M3 is based on the idea that shared immutable structure and indexed metadata can
provide a basis for reusable computation. The programme starts with M3 String,
regex, and precompute in M3JDK21, then collections and SWT/Eclipse integration.

This Eclipse SDK aggregator fork provides a target for assembling and evaluating the Eclipse integration work across product builds. Runtime proposals need to be assessed in the resulting SDK, not only in isolated benchmarks.

**Explore the idea:** [M3 technical design paper](https://github.com/hsoliwal/M3jdk21/blob/master/m3/papers/M3_SHARED_STRUCTURE_AND_REUSABLE_COMPUTATION.md) ·
[Programme goals and roadmap](https://github.com/hsoliwal/M3jdk21#project-goals-and-plan).
The paper explains the proposed architecture, cost tradeoffs, and evaluation plan.
Readers are invited to examine the work and contribute representative workloads.

This section describes the direction of the hsoliwal fork. Upstream documentation
follows below; upstream authorship, licenses, and project identity remain intact.

---

## Fork checkout and repository boundaries

This is the [hsoliwal fork](https://github.com/hsoliwal/eclipse.platform.releng.aggregator)
of the [upstream Eclipse SDK aggregator](https://github.com/eclipse-platform/eclipse.platform.releng.aggregator).
To inspect or build this fork's recorded revision:

```sh
git clone --recurse-submodules https://github.com/hsoliwal/eclipse.platform.releng.aggregator.git
cd eclipse.platform.releng.aggregator
```

**The submodules still point to upstream repositories.** See
[.gitmodules](.gitmodules): Platform, SWT, Platform UI, JDT, PDE and Equinox
URLs are upstream URLs. A recursive clone checks out the submodule commits
recorded by this aggregator; it does not automatically select the latest
`master` commits or the corresponding `hsoliwal` forks. If evaluating changes
from sibling forks, record the exact component revisions and integration
changes separately rather than assuming they are included.

The [root reactor](pom.xml) ties together these distinct areas:

- [eclipse-platform-parent/](eclipse-platform-parent/): shared Maven/Tycho configuration
- [eclipse.platform.releng.prereqs.sdk/](eclipse.platform.releng.prereqs.sdk/):
  SDK prerequisite target definition
- Component submodules: Platform, SWT, UI, JDT, PDE and Equinox source
- [eclipse.platform.common/](eclipse.platform.common/) and
  [eclipse.platform.releng/](eclipse.platform.releng/): shared documentation and releng content
- [products/](products/) and [sites/](sites/): product and p2 repository assembly

Use this repository for SDK integration and packaging. A component-only change
is usually easier to develop and test in the owning component repository first.
For the full development workspace, inspect
[oomph/PlatformSDKConfiguration.setup](oomph/PlatformSDKConfiguration.setup).
For release work, distinguish [RELENG.md](RELENG.md) from the
[release checklist](RELEASE.md).

Fork-specific integration changes belong in
[hsoliwal/eclipse.platform.releng.aggregator pull requests](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/pulls).
The upstream clone and contribution instructions below remain available for
upstream Eclipse development. Preserve the existing [LICENSE](LICENSE) and
[NOTICE](NOTICE) and the individual components' notices.

Aggregator repo for Eclipse SDK builds
======================================

This repo is used to build the Eclipse SDK which contains the framework for Eclipse based applications, the Java® development tools (JDT™) and the Plug-in Development Environment (PDE™).
To clone it, it is recommended to use one of the URLs found on this website: 
- https://github.com/eclipse-platform/eclipse.platform.releng.aggregator

An anonymous clone can be done via the following command:
```
git clone --recurse-submodules https://github.com/eclipse-platform/eclipse.platform.releng.aggregator.git
```
It will also clone all submodules.

How to build the Eclipse SDK
----------------------------
For a complete build run the following command from the root of this repository:
```
mvn clean verify
```
But this will result in a significant runtime of up to 10 hours, mainly due to test executions.
Skipping tests and building in parallel can reduce runtime substantially (the upstream estimate is about 10–20 minutes, depending on the computer). This is a packaging/build check, not a passing test run:
```
mvn clean verify -DskipTests --threads 1C
```

After a successful build, the `Eclipse-SDK` and `Eclipse-Platform` products are located at
```
products/eclipse-sdk/target/products
products/eclipse-platform/target/products
```
and the assembled P2 update-site is at
```
sites/eclipse-platform-repository/target/repository
```

To update your local clone and all it's submodules to the latest state run:
```
git checkout master
git pull --recurse-submodules
git submodule update
```
Use a clean working tree for a reproducible build. **The cleanup commands below are destructive:** `git clean -f -d -x` removes untracked and ignored files, including local build outputs, and `git reset --hard HEAD` discards tracked edits. They affect the submodules as well as the aggregator. Only use this cleanup in a disposable checkout or after preserving all work you need; it is not a required setup step.
```
git submodule foreach git clean -f -d -x
git submodule foreach git reset --hard HEAD
git clean -f -d -x
git reset --hard HEAD
```

Build with custom compiler
--------------------------

To compile the build itself with a custom compiler perform the following step after cloning the submodules:

```
# compile local version
mvn clean install -f eclipse.jdt.core/org.eclipse.jdt.core.compiler.batch -DlocalEcjVersion=99.99

# run build with local compiler
mvn clean verify -DskipTests=true -Dcbi-ecj-version=99.99
```

Build requirements
------------------

The build commands require the installation and setup of Java 25 or higher and Maven version 3.9.12 or higher.
See also the complete instructions on the [Platform Build wiki](https://github.com/eclipse-platform/eclipse.platform.releng.aggregator/wiki/Platform-Build). 
Note, it is highly recommended to use toolchains.xml and `-Pbree-libs` as described in [Using BREE Libs](https://github.com/eclipse-platform/eclipse.platform.releng.aggregator/wiki/Platform-Build#using-bree-libs).

Integration builds
------------------

The integrations (nightly) build jobs are hosted on Jenkins instance https://ci.eclipse.org/releng/job/builds/.

The job with the highest release number is the one that builds nightly SDK build, like `I-build-4.41` job for 4.41 SDK.

- The build artifacts and test results are accessible at https://download.eclipse.org/eclipse/downloads/
- If the tests fail to start, test jobs for each platform can be found at https://ci.eclipse.org/releng/job/automated-tests
- If the build is successful but relevant functionality is severely broken and the build shouldn't be used,
  the build can be marked as *unstable* using the [Mark build](https://ci.eclipse.org/releng/job/builds/job/mark-build) job.
- Daily Maven snapshots are provided by the [Deploy to Maven repository](https://ci.eclipse.org/releng/job/releng/job/deploy-maven) job
and are available at https://repo.eclipse.org/content/repositories/eclipse-snapshots/

The [Eclipse RelEng and build calendar](https://download.eclipse.org/eclipse/downloads/#releng-calendar) provides an overview of all scheduled builds and release related events.

Milestone and release tasks
-----------------
See [Releng-Tasks 2.1](RELEASE.md) (includes links to schedule, calendar etc)

How to contribute
-----------------
Contributions to Eclipse Platform are most welcome. There are many ways to contribute,
from entering high quality bug reports, to contributing code or documentation changes.
For a complete guide, see https://github.com/eclipse-platform/.github/blob/main/CONTRIBUTING.md.

Additional informations
-----------------------

Eclipse Platform Project committers should also read [Automated Platform Builds](https://github.com/eclipse-platform/eclipse.platform.releng.aggregator/wiki/Platform-Build-Automated).

Release Engineers should also be familiar with other documents on the [Releng Wiki](https://github.com/eclipse-platform/eclipse.platform.releng.aggregator/wiki).

License
-------

[Eclipse Public License (EPL) v2.0][2]

[2]: https://www.eclipse.org/legal/epl-2.0/

## Pinned project, module and package reference

The [source reference](docs/source-reference/README.md) maps every metadata-backed project/module path and recognized Java namespace at the documented revision. It includes selected build/API/lifecycle contracts and an explicit [coverage ledger](docs/source-reference/COVERAGE.md). Structural accounting is not a claim of complete package semantics, successful builds or verified M3 integration.
