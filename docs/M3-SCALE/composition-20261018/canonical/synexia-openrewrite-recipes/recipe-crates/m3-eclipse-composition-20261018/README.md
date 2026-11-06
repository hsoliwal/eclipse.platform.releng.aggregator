<!-- SPDX-FileCopyrightText: 2026 Hitesh Soliwal and Contributors to the Synexia Project -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Eclipse fork composition

This crate selects the existing Eclipse SDK modules with the verified M3 Platform,
SWT and UI receivers. It uses the existing hash-pinned text recipe for the root
submodule URLs and the exact composition manifest. The Git object entries for the
three selected receiver commits are recorded separately in `SOURCE_PINS.json`.

The other nine SDK gitlinks retain their original commits and URLs. This is build
composition; it does not replace their implementations or establish a complete
Eclipse runtime migration.

## Runtime ownership selected by this composition

| Area | M3 implementation | Eclipse surface |
| --- | --- | --- |
| Jobs compound rules | Internal stateless `M3Rules` array algorithms | All seven `MultiRule` operations forward, with the existing final child array |
| Commands category and parameter-type registries | Existing packed primitive-index map implementation | Two private point-lookup registries use M3 storage |
| JFace arrays | Existing `M3ViewerArrays` owner | Five existing viewer facades forward fourteen call sites |
| SWT tree operations | Existing SWT M3 tree residency and projection owners | Existing SWT `Tree` and `TreeItem` instances retain widget and native lifetime ownership |

The callback-sensitive command traversal map is preserved. Its broader substitution
failed a reentrant callback-order contract. The selected registries have independent
contract, API, compiler and real Equinox evidence in their canonical crate.

## Execute the existing checks

The recipe qualification uses Java 21, Maven and OpenRewrite 8.17.1:

```sh
mvn -B -ntp -f pom.xml test -Dmaterialize.dir=/absolute/empty/output
mvn -B -ntp -f proof/pom.xml test
```

The first command emits only real SDK recipe results. Review those results and the
three exact Git object entries before updating an aggregator worktree. The recipe
never executes Git, fetches repositories, changes Git configuration or edits an index.

The recovered Java verifier is read-only. Run its source gate on an actual clean
aggregator checkout after initializing its twelve pinned submodules:

```sh
java -cp proof/target/classes M3EclipseComposition source \
  /absolute/aggregator \
  /absolute/aggregator/docs/M3-SCALE/composition-20261018/composition.tsv
java -cp proof/target/classes M3EclipseComposition reports \
  /absolute/native-jface-report-directory
```

The report gate requires exactly one passing
`org.eclipse.jface.tests.viewers.M3TreeForwardingTest#testExpandedStateDelegatesToSwtWithoutWalkingColdVirtualSiblings`.
It refuses missing, failed, errored or skipped evidence for that method. The UI
receiver's `m3-forwarding` profile enables the required method checks in the forked
test VM. The report directory must contain the genuine test-run output.

## Evidence boundaries

The verifier's forty-six tests were rerun with Java 21 and all passed, with no
failures, errors or skips. These test the verifier against its contract fixtures;
they are not a claim that all twelve product worktrees were initialized and tested.

`SOURCE_PINS.json` binds the exact published receiver heads and points to the
existing native evidence in the JFace gate crate at canonical runtime source
commit `9a04e7cf94e2b47570fed61ed508e50dcd80edb1`. Its original
`evidence/native/native-green/native-jface.json` records one passing native method
and a successful execution of this verifier's `reports` command. The corresponding
original XML is referenced by its exact content hash. This composition does not
rerun or duplicate that native proof.

Complete Tycho/PDE SDK acceptance requires the actual target platform and
initialized source tree. The twelve-worktree source gate remains a separate
receiver check. Do not treat a recipe fixed point, a source selector, old evidence,
or a zero-job CI run as that acceptance.
