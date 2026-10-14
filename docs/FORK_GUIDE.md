# Building an Eclipse SDK from this fork

The SDK is the place where Platform, JDT, PDE, SWT and Equinox meet. This guide
explains how the aggregator assembles those projects, which source revisions you
actually build, and how to separate packaging evidence from test evidence.

[Command cheat sheet](COMMAND_CHEATSHEET.md) · [Original build instructions](../README.md) ·
[Release engineering](../RELENG.md) · [Release tasks](../RELEASE.md)

## Choosing the right repository

| Goal | Use |
| --- | --- |
| Assemble Eclipse SDK or Platform products | This aggregator |
| Change/test workspace resources or jobs | The [Platform component fork](https://github.com/hsoliwal/eclipse.platform) |
| Change/test workbench behavior | The [Platform UI fork](https://github.com/hsoliwal/eclipse.platform.ui) |
| Investigate plug-in tooling | PDE's component repository; this aggregator supplies SDK integration |
| Run an installed Eclipse IDE | An appropriate published Eclipse distribution, rather than a source checkout |

The root [pom.xml](../pom.xml) combines a parent POM, prerequisite target platform,
component repositories, product definitions and p2 sites. A **submodule** records a
commit from another Git repository. A **target platform** supplies dependencies
used by Tycho. A **product** describes an application distribution. A **p2 site**
is an installable repository of Eclipse artifacts.

## Understanding this fork

This is `hsoliwal/eclipse.platform.releng.aggregator`, derived from
[`eclipse-platform/eclipse.platform.releng.aggregator`](https://github.com/eclipse-platform/eclipse.platform.releng.aggregator).
Existing downstream additions frame it as an integration/evaluation target for M3
work and add [atom/pattern analysis configuration](../.m3/atom-pattern/README.md),
a [content-bound analysis runner](../.m3/atomize-patternize/README.md),
[convergence notes](../SYNEXIA_CONVERGENCE_MODEL.md), and
[rights/provenance notes](../M3-SYNEXIA-RIGHTS.md).

Those additions do not establish a tested M3 SDK or a runtime speedup. Analysis
receipts, a completed package build, regression tests and desktop compatibility
measurements are different kinds of evidence.

**Important:** the inspected [.gitmodules](../.gitmodules) still names upstream
Eclipse repositories. Cloning this fork recursively does **not** automatically
substitute the other `hsoliwal` forks. The recorded gitlink SHAs choose the source
revisions; a submodule's `branch = master` does not turn a normal checkout into
"always build the newest master."

## Preparing the toolchain

The inspected [README build requirements](../README.md#build-requirements) specify
**Java 25 or newer and Maven 3.9.12 or newer**. The [Jenkinsfile](../Jenkinsfile)
launches Maven using JDK 25; the checked-in
[reusable Maven workflow](../.github/workflows/mavenBuild.yml) selects Maven
**3.9.16** by default and configures Java 11, 17, 21 and 25 toolchains.

Use JDK 25 for a straightforward matching setup rather than assuming that a newer
JDK is already validated. Check the current revision if you choose a different JDK.
The [Tycho extension](../.mvn/extensions.xml) is **5.0.4**, and the reactor and
[parent POM](../eclipse-platform-parent/pom.xml) are in the **4.42.0-SNAPSHOT** line.

A lower `java.version` property or an individual bundle's execution environment
is not the same as the JDK required to launch the aggregate build. For
`-Pbree-libs`, follow the upstream
[BREE toolchain instructions](https://github.com/eclipse-platform/eclipse.platform.releng.aggregator/wiki/Platform-Build#using-bree-libs).
That profile can require multiple installed JDKs even when Maven launches on 25.

Also plan for network downloads, a substantial checkout/cache/output footprint,
and native/display dependencies for UI tests. Build time varies with the host,
cache, network and selected tests; this guide makes no elapsed-time promise.

```sh
git --version
java -version
mvn -version
```

## Cloning the recorded sources

Use a new directory to avoid disturbing another checkout:

```sh
git clone --recurse-submodules \
  https://github.com/hsoliwal/eclipse.platform.releng.aggregator.git
cd eclipse.platform.releng.aggregator

git rev-parse HEAD
git status --short
git submodule status --recursive
```

If you already cloned without submodules, initialize the recorded revisions:

```sh
git submodule update --init --recursive
```

In `git submodule status`, a leading `-` means uninitialized, `+` means the checked
out commit differs from the superproject's recorded commit, and `U` indicates a
conflict. Investigate those states before calling a build reproducible.

Avoid `git submodule update --remote` for a baseline reproduction: it moves toward
remote branch tips rather than checking out the committed gitlinks.

## Building products first

From the aggregator root, a package-oriented first build can skip test execution:

```sh
mvn clean verify -DskipTests --threads 1C
```

This is an existing upstream-supported build shape, not a test gate. `1C` requests
one Maven thread per CPU core and can increase memory use. Remove `--threads 1C`
when investigating a failure or on a constrained machine.

After a successful build, inspect the locations documented by the root README:

| Output | Path |
| --- | --- |
| Eclipse SDK products | `products/eclipse-sdk/target/products` |
| Eclipse Platform products | `products/eclipse-platform/target/products` |
| Assembled p2 site | `sites/eclipse-platform-repository/target/repository` |

The [products reactor](../products/pom.xml) and [sites reactor](../sites/pom.xml)
explain their membership and packaging. Some children are pomless; a missing
child `pom.xml` does not imply a missing product definition.

```sh
find products/eclipse-sdk/target/products -maxdepth 2 -type f
find sites/eclipse-platform-repository/target/repository -maxdepth 1 -type f
```

Do not treat leftover output from a previous build as success. Check the reactor
summary, return status and output timestamps. Local packaging does not itself
publish, sign or qualify an official Eclipse release.

## Running verification

For the broader verification build, remove the skip flag:

```sh
mvn clean verify
```

On Linux, UI tests may require Xvfb and the native libraries appropriate to the
selected SWT platform. If Xvfb is installed and configured, a headless-display
invocation is:

```sh
xvfb-run -a mvn clean verify
```

For a toolchain-configured BREE run, add `-Pbree-libs`. API and Javadoc checks have
additional baseline/tooling needs; inspect the parent and reusable workflow before
claiming local CI equivalence. Component tests often provide a faster diagnosis
than restarting the entire aggregate reactor.

Find the evidence, rather than inferring it from a green packaging step:

```sh
find . -path '*/target/surefire-reports/*' -type f
find . -path '*/target/apianalysis/*' -type f
find . -path '*/target/compilelogs/*' -type f
```

Some CI commands deliberately ignore individual test failures for report collection.
A build with skipped or ignored failures is not evidence that all tests passed.

## Recording an SDK experiment

A useful experiment answers "Which exact source combination produced this SDK?"
Capture the aggregator and every checked-out submodule before comparing behavior:

```sh
git rev-parse HEAD
git submodule status --recursive
git submodule foreach --recursive 'git status --short'
mvn -version
```

For a downstream-component experiment, make the component choice explicit in a
separate experimental checkout/branch, record the remote and exact commit, and
review the resulting gitlink diff. Do not silently replace submodule URLs or
claim that the ordinary recursive clone includes a fork-specific implementation.
This guide intentionally leaves the repository's submodule configuration intact.

A report should state:

1. Aggregator SHA and component gitlink SHAs, plus any dirty files
2. OS/architecture, build JDK, BREE toolchains and Maven version
3. Exact command, profiles, skipped checks and target-platform inputs
4. Product produced, tests actually executed and failures/skips
5. For comparisons, the baseline product, workload and measurement method

For desktop smoke checks, use a disposable workspace and record the exact product
archive/platform. Confirm startup and the feature you changed before generalizing
to compatibility. Building an archive is not proof of UI or native behavior.

## Troubleshooting without destroying work

| Symptom | First check |
| --- | --- |
| Missing module or empty component directory | `git submodule status --recursive`; initialize recorded submodules |
| Submodule unexpectedly differs | Local changes and recorded gitlink; do not reset blindly |
| Java/compiler error | `mvn -version`, JDK 25 selection, toolchain IDs and current parent |
| Toolchain not found | Installed JDK paths and BREE toolchain configuration |
| Parent/p2 artifact cannot resolve | Exact coordinate and repository URL, network/proxy, snapshot availability |
| No display/native SWT error | Display server and host libraries, then selected test platform |
| Memory pressure under parallel build | Retry serially and inspect Maven/OS memory limits |
| Package exists but tests are absent | Skip flags, reactor summary and actual report timestamps |
| Local change seems absent | Component SHA, reactor inclusion and baseline-replacement warning |

The upstream README retains historical cleanup commands. `git clean -f -d -x`
and `git reset --hard` can remove untracked/ignored files and discard work.
Prefer a separate clean checkout. If investigating cleanup, inspect `git status`
and dry-run `git clean -ndx` first; never use destructive cleanup as a casual first
troubleshooting step.

## Navigating and contributing

- [Root reactor](../pom.xml): build membership
- [Shared parent](../eclipse-platform-parent/pom.xml): versions, profiles and plugins
- [Submodule definitions](../.gitmodules): source repositories
- [Product configuration](../products) and [site configuration](../sites): outputs
- [Releng guide](../RELENG.md) and [release checklist](../RELEASE.md): maintainer workflows
- [Fork issues](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/issues): fork-specific findings
- [Contribution instructions](../CONTRIBUTING.md): upstream contributor requirements

Do not use release/deploy/signing jobs as a local quick start. Preserve
[LICENSE](../LICENSE), [NOTICE](../NOTICE), upstream identity and file-level notices.

## Evidence and maintenance

Reviewed on **2026-10-14** at
[`80804ff181a2`](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/tree/80804ff181a2261c4a98a6377718b10cc1093903).
The inspected downstream comparison contains `.m3` analysis/provenance material
and README framing; it does not change the upstream submodule URLs.
Commands and paths were checked against repository configuration. The SDK build,
tests and launch checks were **not executed** for this documentation update.
