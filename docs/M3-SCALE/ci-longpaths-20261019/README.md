<!-- SPDX-FileCopyrightText: 2026 Hitesh Soliwal and Contributors to the Synexia Project -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Eclipse shared Maven workflow: Windows Git long paths

This receiver adds a Windows-only Git setup step immediately before Checkout in
the existing shared Maven workflow. Its source is the actual output of
`com.synexia.eclipse.CiLongPaths20261019`, qualified with the unchanged canonical
`M3HashPinnedTextSnapshotRecipe` through OpenRewrite 8.17.1.

The retained Platform and UI Windows jobs stopped during Checkout with
`Filename too long` and Git exit 128. Java setup, Maven setup and the builds were
skipped. The [original checkout evidence](canonical/synexia-openrewrite-recipes/recipe-crates/m3-eclipse-ci-longpaths-20261019/evidence/baseline/README.md)
records those historical failures. **Hosted Windows checkout with this correction
remains a pending receiving gate.**

## Exact workflow change

The [existing workflow](../../../.github/workflows/mavenBuild.yml) gains only:

```yaml
    - name: Enable long paths on Windows
      if: runner.os == 'Windows'
      run: git config --global core.longpaths true
```

These three lines add 125 bytes before the original Checkout step. The new step
uses the workflow's inherited Windows `cmd` shell. Removing the exact insertion
restores every original workflow byte. Existing workflow registration, permissions,
inputs, triggers, action pins, matrix, profiles, build commands and upload steps
retain their original source bytes.

| Binding | Identity |
|---|---|
| Receiver base | `hsoliwal/eclipse.platform.releng.aggregator` at `f1c1343f92f68a53dd3593fd3f98a3137e8003c0` |
| Base tree | `c026b445d1bca3a540c75d948e37c4a737d51fe8` |
| Original workflow | 3,238 bytes; Git blob `0416c8be3bef180616929288ad634e3b4c7d9515` |
| Actual SDK workflow output | 3,363 bytes; Git blob `d6d1096b7f38bb975fa3c9e3e6c0ef47a9166fbf` |
| Output SHA-256 | `23522344c0010e850bdc279312e9c0ebf546f0af97162e51d59024d533d4c0d9` |

## Published canonical source

All 48 mirrored source files and the output's recipe binding point to
[hsoliwal/com.synexia at `83759bbb74ce7775fd967cd918927c823f78c161`](https://github.com/hsoliwal/com.synexia/tree/83759bbb74ce7775fd967cd918927c823f78c161/synexia-openrewrite-recipes/recipe-crates/m3-eclipse-ci-longpaths-20261019),
canonical tree `d5a91a30b9853d555463ff59ff66844b1136d07d`. The mirror contains all **44 frozen crate files**
and exactly **four unchanged shared SDK owners**. The recorded qualification
predates publication; its historical source pins, failure snapshots, tool output
and original attribution remain byte-for-byte intact.

The directory structure keeps the original `synexia-openrewrite-recipes` layout,
including the POM's `${project.basedir}/../../src/main/java` default. The public
mirror therefore supplies the source owners at the original relative location.

[SOURCE_RECEIPT.json](SOURCE_RECEIPT.json) records every canonical path, publication
commit and tree, Git blob, SHA-256, license and original lineage. The complete
nine-column origin record is preserved for each of the 44 crate files; the public
notice and license mappings are separate. [FILE_PROVENANCE.tsv](FILE_PROVENANCE.tsv)
also covers the three receiver metadata files, whose identities are supplied by
the receiver Git tree without circular self hashes or an invented future commit.

This is a closed **52-blob** change set: 44 crate files, four SDK owners, one
workflow output and three scoped metadata files. The existing 37-entry composition
receiver, all twelve gitlinks, `.gitmodules`, and the composition TSV retain their
base identities. There are 51 new documentation paths and one modified workflow.

## Recorded qualification and its limits

| Preserved execution | Result | Meaning |
|---|---|---|
| Initial SDK RED | 1 test, 1 expected failure, 0 errors or skips | A sealed no-op template caused the real named recipe to emit zero changes; the positive one-output assertion failed |
| First corrected suite | 6 tests, 2 failures, 0 errors or skips | The auxiliary YAML printer did not reproduce the original formatting; the same issue was then measured in the untouched upstream workflow |
| Final SDK suite | **6 tests, 0 failures, errors or skips; exit 0** | Exact output, fixed point, bounded refusals, unrelated sources, aliases, order and independent worker replay qualified |

The [final raw Maven log, JUnit XML and receipt](canonical/synexia-openrewrite-recipes/recipe-crates/m3-eclipse-ci-longpaths-20261019/evidence/sdk-green/)
are preserved alongside the [legitimate RED](canonical/synexia-openrewrite-recipes/recipe-crates/m3-eclipse-ci-longpaths-20261019/evidence/sdk-red/),
the [original YAML assertion refusal](canonical/synexia-openrewrite-recipes/recipe-crates/m3-eclipse-ci-longpaths-20261019/evidence/sdk-yaml-printer-refusal/)
and the earlier offline setup refusal, which executed no tests.

The pinned real YAML parser returns a parse-to-print idempotence error containing
a genuine YAML Documents tree for both the original and corrected workflow.
Its printer inserts the **same exact 12-byte delta** in each: one line containing
eleven spaces and LF after the unique unchanged `matrix.config` declaration.
The [baseline and postimage diagnosis](canonical/synexia-openrewrite-recipes/recipe-crates/m3-eclipse-ci-longpaths-20261019/evidence/parser-diagnostic/printer-delta.json)
records this limit. The final test admits only that exact error kind and delta,
then inspects the parsed step, Windows condition, command and position. It makes
no YAML byte-round-trip claim. The actual TextSnapshot workflow bytes remain
bound to their exact hash and the three-line-only restoration check.

Receiver preparation checks file identities, source binding, provenance, modes
and the closed change set. It runs no tests or compilers. The retained SDK results
do not establish hosted Windows Git checkout, an Eclipse Maven/Tycho/PDE build,
or whole-Eclipse acceptance.

## Reproduce the SDK source qualification

With Java 21 and Maven, run from the receiver repository root:

```sh
cd docs/M3-SCALE/ci-longpaths-20261019/canonical/synexia-openrewrite-recipes/recipe-crates/m3-eclipse-ci-longpaths-20261019
mvn -B -ntp -Dmaterialize.dir=/absolute/path/to/workflow-output test
```

The unchanged POM pins the SDK/test dependencies and compiles the four mirrored
owners from their default relative location. The positive test writes the actual
SDK changeset result to
`/absolute/path/to/workflow-output/.github/workflows/mavenBuild.yml`.
The original recorded run used Temurin 21.0.12.1+1 and Maven 3.9.12; its exact
offline command, inputs and hashes are in the mirrored execution receipt.
This preparation did not repeat that command or copy a template in place of
the already-materialized SDK output.

## Caller publication order

The shared workflow receiver must have an actual immutable public commit first.
A **separate caller recipe** can then bind Platform and UI to that commit.
This packet supplies no caller rewrite or guessed future SHA. It contains no
gitlink edits, extra workflows, new permissions or new build profiles.

## License and notice mapping

The original and corrected workflow retain EPL-2.0. The recipe, its first-party
proof material, shared source owners and this receiver metadata use Apache-2.0.
The full [EPL license](canonical/synexia-openrewrite-recipes/recipe-crates/m3-eclipse-ci-longpaths-20261019/LICENSE-EPL-2.0),
[Apache license](canonical/synexia-openrewrite-recipes/recipe-crates/m3-eclipse-ci-longpaths-20261019/LICENSE-APACHE-2.0),
[crate NOTICE](canonical/synexia-openrewrite-recipes/recipe-crates/m3-eclipse-ci-longpaths-20261019/NOTICE) and
[original upstream NOTICE](canonical/synexia-openrewrite-recipes/recipe-crates/m3-eclipse-ci-longpaths-20261019/UPSTREAM-NOTICE) are exact copies.
Original source headers remain intact. The four existing owner lineage records
retain their historical notice reference, mapped to the
[immutable public UI owner notice](https://github.com/hsoliwal/eclipse.platform.ui/blob/52f64fe74beb3f8763cefd28651c5d5ab01d5d92/docs/M3-SCALE/runtime-forwarding-20261018/canonical/synexia-openrewrite-recipes/recipe-crates/m3-jface-forwarding-gate-20261018/NOTICE).
The recipe's license does not relicense its workflow payload; recorded build
output retains the original tool messages and evidence timestamps.
