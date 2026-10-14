# Eclipse SDK build cheat sheet

[Full guide](FORK_GUIDE.md) · [Root README](../README.md)

Use the aggregator root unless a command says otherwise. Baseline: JDK 25,
Maven 3.9.12+, Git, network access, and initialized submodules. CI-like BREE builds
also need the configured toolchains. Commands are not claimed to have been run.

## The first commands

```sh
git clone --recurse-submodules https://github.com/hsoliwal/eclipse.platform.releng.aggregator.git
cd eclipse.platform.releng.aggregator
mvn -version
git rev-parse HEAD
git submodule status --recursive
```

## Choose the scope

| Intent | Command | Evidence limit |
| --- | --- | --- |
| Initialize a non-recursive clone | `git submodule update --init --recursive` | Uses recorded gitlinks |
| Package products without running tests | `mvn clean verify -DskipTests --threads 1C` | No regression-test result |
| Full verification | `mvn clean verify` | Inspect actual test reports and skips |
| Linux UI test display | `xvfb-run -a mvn clean verify` | Requires installed Xvfb and native UI dependencies |
| BREE-aware verification | `mvn clean verify -Pbree-libs` | Requires matching installed JDK toolchains |
| Serial packaging diagnosis | `mvn clean verify -DskipTests` | Reduces concurrency; still skips tests |

A component repository build does not assemble the same products as this reactor.
Do not treat a `mvn test` invocation as equivalent to Tycho `verify`.

## See what will be built

```sh
cat .gitmodules
cat .mvn/maven.config
cat .mvn/extensions.xml
git submodule foreach --recursive 'git rev-parse HEAD'
git submodule foreach --recursive 'git status --short'
```

- `.mvn/maven.config` sets `aggregatorBuild=true`
- The checked-in extension is Tycho 5.0.4 at the documented source revision
- `.gitmodules` uses upstream URLs, not sibling hsoliwal forks
- `git submodule update --remote` changes the source-selection question; it is not baseline reproduction

## Find outputs and reports

```sh
find products/eclipse-sdk/target/products -maxdepth 2 -type f
find products/eclipse-platform/target/products -maxdepth 2 -type f
find sites/eclipse-platform-repository/target/repository -maxdepth 1 -type f
find . -path '*/target/surefire-reports/*' -type f
find . -path '*/target/apianalysis/*' -type f
```

Missing directories can mean the relevant stage did not complete. Compare file
timestamps with the run; old output is not evidence for the current commit.

## Inspect local changes safely

```sh
git status --short
git diff --stat
git diff --submodule=log
git clean -ndx
git submodule foreach --recursive 'git clean -ndx'
```

The last two commands are previews. Removing `-n`, adding destructive cleanup
flags, or using `reset --hard` can discard valuable files. A new checkout is often
the safer way to reproduce a clean build.

## Keep these concepts separate

| Concept | Meaning |
| --- | --- |
| Build JVM | Java reported by `mvn -version` |
| Bundle execution environment | Java/API contract requested by a bundle |
| BREE toolchains | Additional JDKs selected for execution-environment libraries |
| Gitlink | Exact commit recorded for a submodule |
| Target platform | Resolved Eclipse/p2 dependencies |
| SDK product | Assembled application distribution |
| Local package | Not automatically an official signed/released Eclipse build |
| Analysis receipt | Not a replacement for compile, test or runtime evidence |

## Before posting an issue

Include aggregator/submodule SHAs, dirty-state disclosure, OS/architecture,
Maven/JDK versions, full command, first relevant error, and report paths. State
which checks were skipped. Review logs for credentials before posting publicly.
