<!-- SPDX-FileCopyrightText: 2026 Hitesh Soliwal and Contributors to the Synexia Project -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Eclipse shared CI: Windows Git long paths

This Synexia-owned recipe prepares one correction to the existing Eclipse
aggregator shared Maven workflow. It enables Git long paths on Windows before
Checkout, preserving every other workflow byte.

The observed Platform and UI Windows jobs failed at Checkout with Git exit 128
and `Filename too long`. Java setup, Maven setup and the Maven build were
skipped. Platform's reported directory was introduced by the forwarding mirror;
UI's reported directory was already present unchanged in its base. The retained
job evidence is under `evidence/baseline/`. It records those historical jobs,
not a hosted execution of this later correction.

## Exact recipe boundary

| Item | Identity |
| --- | --- |
| Named recipe | `com.synexia.eclipse.CiLongPaths20261019` |
| Existing Java owner | `com.synexia.rewrite.M3HashPinnedTextSnapshotRecipe` |
| Default owner source root | `${project.basedir}/../../src/main/java` |
| Shared Text owner blob | `cc5f86ab579d2f4b1b9bc4c26b4592d2d8142244` |
| Target repository | `hsoliwal/eclipse.platform.releng.aggregator` |
| Target source revision | `f1c1343f92f68a53dd3593fd3f98a3137e8003c0` |
| Only target path | `.github/workflows/mavenBuild.yml` |
| Preimage Git blob | `0416c8be3bef180616929288ad634e3b4c7d9515` |

The reviewed addition is a Windows-only step immediately before the existing
Checkout step. It runs `git config --global core.longpaths true` using the
workflow's inherited Windows `cmd` shell. Git for Windows documents this
configuration for its C-based operations:
https://gitforwindows.org/git-cannot-create-a-file-or-directory-with-a-long-path.html

There is no new registered workflow, trigger, matrix row, permission, action
pin, Java version, Maven version or gate. The scope, explicit invariants and
finite test cases are recorded in `CONTRACT.md` and `SPECTRUM.md`.

## Reproduce the real SDK qualification

Use Java 21 and Maven with the pinned dependencies declared in this crate's
POM. From the crate directory in the canonical source checkout:

```sh
mvn -B -ntp -Dmaterialize.dir=/absolute/path/to/workflow-output test
```

The POM compiles the four existing shared owner sources from their default
canonical location, then runs this crate's complete six-method JUnit suite.
The descriptor activates the existing class-backed TextSnapshot recipe through
the actual OpenRewrite SDK. A separate YAML check inspects real parsed Documents
trees and the inserted step's position, Windows condition and command. The
pinned YAML parser prints one additional whitespace-only line in the unchanged
matrix block for both the upstream preimage and the postimage. The test admits
only that measured 12-byte printer delta and its exact idempotence error kind.
Every actual TextSnapshot output byte remains subject to the reviewed hash and
the requirement that removing only the three inserted lines restores the source.

The materialized workflow is written from the SDK changeset, at
`/absolute/path/to/workflow-output/.github/workflows/mavenBuild.yml`. Merely
copying the template is not the materialization step. The execution receipt
binds source hashes, command, toolchain, raw Maven log, raw JUnit XML, result
count, output hash and unchanged protected source identities.

The initial baseline RED uses a no-op template and manifest. Its named SDK run
must fail the positive test because it emits zero changes. The original RED
manifest/template and raw report remain under `evidence/sdk-red/`; qualification
then advances the main template and its digest. The first full run exposed the
baseline YAML printer limitation described above. Its original assertions,
contract and raw reports remain under `evidence/sdk-yaml-printer-refusal/`, with
the actual baseline/postimage diagnosis under `evidence/parser-diagnostic/`.
The final full run is recorded under `evidence/sdk-green/`. An earlier offline
dependency refusal executed no tests and remains under `evidence/sdk-setup-refusal/`.

## Receiving gate and publication order

The SDK qualification establishes the exact reviewed workflow output,
fixed-point replay and bounded refusal behavior. It does not run Windows Git
checkout or any Eclipse Maven, native, Tycho or PDE build. The hosted Windows
checkout gate remains required after the corrected workflow is received.

The integration owner first publishes the shared workflow commit. A separate
exact caller recipe can then bind Platform/UI to that real commit. This crate
does not fabricate a future commit SHA or modify callers, composition gitlinks,
the original 317 proof files, shared owners, the global ledger or canonical home.

The workflow payload retains EPL-2.0. The first-party recipe/test/receipt material
is Apache-2.0; see `NOTICE`, `UPSTREAM-NOTICE` and the two preserved licenses.
