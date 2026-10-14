# Eclipse SDK build exploration and quick reference

This repository coordinates the source repositories, parent build configuration,
products and p2 sites that make up an Eclipse SDK build. Start with the preserved
[root README](../README.md) for full build instructions, [RELENG](../RELENG.md)
for Jenkins administration, and [RELEASE](../RELEASE.md) for release procedures.
This guide is for local source/build exploration, not permission to publish releases.

## Understand the layers

| Layer | Source of truth | What it determines |
| --- | --- | --- |
| Checked-out component revisions | Git submodule entries and [.gitmodules](../.gitmodules) | Which source commits and remotes are used |
| Reactor membership | [pom.xml](../pom.xml) | Parent, prerequisites, JDT, PDE, Platform, Equinox, products and sites |
| Shared build behavior | [eclipse-platform-parent](../eclipse-platform-parent/pom.xml) | Tycho configuration, profiles and common dependencies |
| Installable products | [products](../products/pom.xml) | SDK, Platform and launcher product assembly |
| Update repositories | [sites](../sites) | p2 repository composition |
| Release automation | [jobs](../jobs), [production](../production) | CI orchestration and publication, separate from a local build |

A fork of the aggregator does not automatically use the owner's forks of every
component. The checked-in .gitmodules currently points to upstream Eclipse
repositories. A submodule's recorded gitlink selects its revision; its `branch`
setting does not make ordinary checkout track the latest remote branch.

## Prerequisites

The [README](../README.md) specifies Java 25 or higher and Maven 3.9.12 or higher.
[extensions.xml](../.mvn/extensions.xml) selects Tycho 5.0.4, and
[maven.config](../.mvn/maven.config) sets `aggregatorBuild=true`.
Use the README's linked BREE/toolchains instructions when enabling `bree-libs`;
the build JVM and the execution environments of individual bundles are different
inputs. Plan for Maven/p2 network downloads, sufficient disk space and a graphical
display for UI tests. Product assembly can resolve platform-specific artifacts
without establishing that the product was tested on every listed platform.

## Command cheat sheet

These commands come from the repository's documented build and Git layout. They
were not executed for this documentation change.

```sh
git clone --recurse-submodules https://github.com/hsoliwal/eclipse.platform.releng.aggregator.git
cd eclipse.platform.releng.aggregator
java -version
mvn -version
git status --short
git submodule status --recursive
# Inspect configured component sources without changing them.
git config --file .gitmodules --get-regexp '^submodule\..*\.url$'
# Assembly smoke build; explicitly skips test execution.
mvn clean verify -DskipTests --threads 1C
# Full verify, with its much larger runtime and environment requirements.
mvn clean verify
```

For an existing checkout with uninitialized modules, inspect local changes first,
then use `git submodule update --init --recursive` to restore the recorded module
revisions. Do not substitute `--remote` if your goal is to reproduce the recorded
source set. Avoid destructive reset/clean commands as a default troubleshooting
step; preserve local work and diagnose the first failing module.

## Worked exploration: what source goes into the SDK?

1. Locate the `eclipse.platform.ui` stanza in [.gitmodules](../.gitmodules).
   Compare its URL with the source checkout you intended to evaluate.
2. Inspect the recorded revision with
   `git ls-tree HEAD eclipse.platform.ui`, then compare
   `git -C eclipse.platform.ui rev-parse HEAD`.
   This checks checkout identity; it is not a test of UI behavior or content parity.
3. Follow the root POM's `products` module to [products/pom.xml](../products/pom.xml).
   It lists Eclipse Platform, SDK, launcher and starterkit products and configures
   p2 director materialization.
4. Inspect the matching product and site definitions before interpreting output.
   The README identifies these successful-build locations:
   - `products/eclipse-sdk/target/products`
   - `products/eclipse-platform/target/products`
   - `sites/eclipse-platform-repository/target/repository`
5. Record the aggregator revision and all participating component revisions next
   to your results. If evaluating a downstream component, make its inclusion an
   explicit separately reviewed change; do not infer it from the aggregator's owner.

## Interpreting results

- A `-DskipTests` assembly can check packaging but cannot establish passed tests.
- Inspect test XML, compiler diagnostics and API reports for participating modules.
  A completed build job and available artifacts do not imply every gate passed.
- A source revision present in Git ancestry is not proof that its complete file
  contents survive later merges. Compare relevant trees/diffs when making a
  content-parity claim.
- A successfully built SDK does not establish runtime compatibility, responsiveness
  or a performance improvement. Launch and test representative workloads on the
  target OS/JDK and retain environment details.
- Signing, deployment and release jobs have external effects. Follow the existing
  release procedures and obtain the relevant authority before running them.

Keep upstream notices and attribution intact. Fork-specific experimental goals in
the README are proposals; use measured results and reproducible source inputs
before making acceptance or performance claims.
