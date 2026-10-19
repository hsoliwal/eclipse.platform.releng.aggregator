<!-- SPDX-FileCopyrightText: 2026 Hitesh Soliwal and Contributors to the Synexia Project -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# M3 Eclipse composition receiver

This receiver selects three published public forks inside the existing twelve-module
Eclipse SDK composition. It starts from
[`hsoliwal/eclipse.platform.releng.aggregator` at `0f1cb47ce80d9cf91fbb3ec4cbeccfcd366691b9`](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/tree/0f1cb47ce80d9cf91fbb3ec4cbeccfcd366691b9).
The two text files are actual results of the canonical OpenRewrite recipe
`com.synexia.eclipse.Composition20261018`. Three separate Git tree entries select
the published receiver commits.

## Selected public receivers

| Existing module | Selected commit | Public review |
|---|---|---|
| `eclipse.platform` | `52f3d67e43402c5a65207109c2b37b68b5bbd74e` | [Platform PR 14](https://github.com/hsoliwal/eclipse.platform/pull/14) |
| `eclipse.platform.ui` | `52f64fe74beb3f8763cefd28651c5d5ab01d5d92` | [UI PR 17](https://github.com/hsoliwal/eclipse.platform.ui/pull/17) |
| `eclipse.platform.swt` | `422fb369629ba47fc5c5c6ddf01794b6d7c79f42` | [Existing SWT receiver](https://github.com/hsoliwal/eclipse.platform.swt/tree/422fb369629ba47fc5c5c6ddf01794b6d7c79f42) |

[composition.tsv](composition.tsv) records all twelve module paths, declared URLs,
and exact commit IDs. The other nine URLs and gitlinks remain at their original
aggregator pins. The root Maven module selection is unchanged.

Platform's receiver supplies the internal array owner for all seven `MultiRule`
operations. UI supplies packed storage for the two selected Commands registries
and the required JFace tree-forwarding gate. The selected UI and SWT commits also
retain the existing JFace array and SWT tree owners. The receiver source and proof
details remain in the linked public forks. The callback-sensitive Commands traversal
map remains preserved after its broader substitution failed a reentrant-order test.

## Text results and Git object entries

The text recipe emits exactly two files:

- Root `.gitmodules`, changing only the three selected repository URLs.
- `docs/M3-SCALE/composition-20261018/composition.tsv`, adding the sealed twelve-row
  composition descriptor.

Their original preimages, admitted postimages, resource hashes and actual emitted
bytes are recorded in [SOURCE_RECEIPT.json](SOURCE_RECEIPT.json) and the canonical
crate's manifest and recipe receipt. Missing or drifted preimages, occupied
additions, duplicate paths, and resource digest drift refuse admission. Applying
the recipe to the exact postimages is a fixed point.

The three selected module paths use Git mode `160000`, type `commit`. They are
separate Git tree entries in the receiver payload. They are not text outputs, and
the recipe does not run Git, edit an index, initialize submodules, or fetch sources.
The preparation receipt records their exact old and new commit IDs and separately
verifies the nine unchanged entries.

## Frozen canonical source mirror

The `canonical/` directory retains the original `synexia-openrewrite-recipes`
layout: the complete `m3-eclipse-composition-20261018` crate and the four shared
Java/Text snapshot and scope owners. This preserves the recipe POM's exact
`${project.basedir}/../../src/main/java` default. No private binary dependency is
needed to resolve those source owners.

The complete source mirror and both output recipe sources are bound to
[hsoliwal/com.synexia at `06388d86767d4baa86c5461b755421415b14278d`](https://github.com/hsoliwal/com.synexia/tree/06388d86767d4baa86c5461b755421415b14278d/synexia-openrewrite-recipes),
canonical source tree `40476b70b1426b32f41e9d97a686c46fa7bba486`. The source receipt and
scoped provenance bind all 31 source/output references to this publication.
Historical pins and raw execution evidence remain unchanged.

The mirror contains 25 crate files and four SDK owners. Together with
the two emitted files, three scoped metadata files and three gitlinks, this is a
closed 37-entry receiver change set. Runtime binaries, compilation
targets, dependency caches, and private global policy/provenance files are excluded.
Historical source pins and execution records inside the mirrored crate remain
unchanged.

## Recorded qualification

| Evidence | Recorded result | Scope |
|---|---|---|
| Composition recipe SDK | 5 tests; zero failures, errors, or skips | Actual OpenRewrite 8.17.1 execution on Java 21; both output files match the admitted postimages |
| Existing composition verifier | 46 tests; zero failures, errors, or skips | Preserved verifier contract tests; the six frozen source/proof files remain unchanged |
| Existing native JFace gate | 1 test; zero failures, errors, or skips; report verifier exit 0 | The exact named method on the genuine GTK3/Xvfb runtime recorded by the UI receiver |

The native result is linked to the published
[UI proof at `52f64fe74beb3f8763cefd28651c5d5ab01d5d92`](https://github.com/hsoliwal/eclipse.platform.ui/blob/52f64fe74beb3f8763cefd28651c5d5ab01d5d92/docs/M3-SCALE/runtime-forwarding-20261018/canonical/synexia-openrewrite-recipes/recipe-crates/m3-jface-forwarding-gate-20261018/evidence/native/native-green/native-jface.json)
and its
[original Surefire XML](https://github.com/hsoliwal/eclipse.platform.ui/blob/52f64fe74beb3f8763cefd28651c5d5ab01d5d92/docs/M3-SCALE/runtime-forwarding-20261018/canonical/synexia-openrewrite-recipes/recipe-crates/m3-jface-forwarding-gate-20261018/evidence/native/native-green/TEST-org.eclipse.jface.tests.viewers.M3TreeForwardingTest.xml).
The method is
`org.eclipse.jface.tests.viewers.M3TreeForwardingTest#testExpandedStateDelegatesToSwtWithoutWalkingColdVirtualSiblings`.
The composition mirror retains the canonical pointers and exact evidence hashes;
it does not copy or rerun the raw native proof.

Receiver preparation checks source identity, provenance, preimages, the closed
path set and Git entries. It runs no tests. The forty-six verifier checks establish
the verifier's behavior against its fixtures. They do not establish acceptance of
an initialized twelve-module product checkout. The full Tycho/PDE SDK, the actual
twelve-worktree source gate, other native configurations, and complete Eclipse
runtime migration remain separate qualification boundaries.

## Reproduction

Use genuine Java 21, Maven and the dependencies pinned by the mirrored POM and
source receipts. From the mirrored composition crate, the existing commands are:

```sh
mvn -B -ntp test -Dmaterialize.dir=/absolute/empty-output
mvn -B -ntp -f proof/pom.xml test
```

Review the two actual `RecipeRun` outputs and the three Git object entries before
constructing a fresh receiving tree. After initializing the twelve selected
submodules in a clean aggregator checkout, the existing read-only source gate is:

```sh
java -cp proof/target/classes M3EclipseComposition source \
  /absolute/aggregator \
  /absolute/aggregator/docs/M3-SCALE/composition-20261018/composition.tsv
```

It requires actual initialized clean worktrees with the expected HEADs, index
gitlinks and declared URLs. Run the separate `reports` command on genuine native
test reports when performing a fresh acceptance run. Missing, failed, errored or
skipped evidence for the named method cannot satisfy that report contract.
The [canonical crate README](canonical/synexia-openrewrite-recipes/recipe-crates/m3-eclipse-composition-20261018/README.md)
retains the complete verifier instructions and evidence boundaries.

## Provenance and review

[FILE_PROVENANCE.tsv](FILE_PROVENANCE.tsv) retains the exact scoped canonical
origin records and adds the receiver mapping and content hashes. The adapted
Eclipse `.gitmodules` sources preserve their EPL-2.0 provenance. The canonical
recipe owners, verifier and independently authored metadata retain their existing
Apache-2.0 attribution. Both full license texts and the crate notice are copied
exactly. Gitlink commit references are described separately in the source receipt;
their repositories retain their own notices.

The complete copied-index `git diff --check` reports 22 inherited whitespace findings in 3 exact license/raw-evidence files. Their canonical bytes are preserved.
The authored metadata, two outputs, three gitlinks and all remaining paths
pass the same check. No whitespace policy is changed.

The real Git index remains untouched during receiver preparation. A separate
copied index permits review of the complete blob and gitlink path set. The receiver
commit versions its three authored metadata files without a circular self-hash
claim in their own provenance rows.
