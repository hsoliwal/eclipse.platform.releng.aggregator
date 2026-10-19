<!-- SPDX-FileCopyrightText: 2026 Hitesh Soliwal and Contributors to the Synexia Project -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Frozen workflow qualification spectrum

Only `.github/workflows/mavenBuild.yml` is an admitted target. The proof is
an actual OpenRewrite 8.17.1 SDK run of the existing TextSnapshot owner,
with its named recipe descriptor and exact classpath manifest.

| JUnit method | Bounded cases and external observation |
| --- | --- |
| `namedRecipeCorrectsWindowsCheckoutAndMaterializes` | Exactly one changed path; literal reviewed postimage digest; one Windows-only setup immediately before Checkout; removing the three inserted lines restores every original byte; native YAML parse/round trip; optional file materialization from the SDK result only. |
| `reviewedPostimageIsFixedPointAndManifestIsClosed` | One exact target and preimage; named and direct-owner replay of the reviewed postimage both produce zero changes. |
| `missingAndDriftedWorkflowRefuse` | Missing source, differently cased target path, then six byte-drift cases: appended comment, fetch depth, permissions, submodule input, action pin and CRLF conversion. |
| `duplicateAndNoncanonicalTargetPathsRefuse` | Duplicate target, dot alias, parent-traversal alias; on the executing POSIX host, a literal-backslash alias also refuses. |
| `unrelatedSourcesAndInputPermutationsArePreserved` | Real target plus another workflow and YAML carrying code-looking text; forward and reverse input order have the same closed one-result set. |
| `directNamedSerialAndTwoWorkerReplaysAgree` | One direct-owner run, named serial run, four independent trials on two workers, then serial replay; every emitted byte agrees. |

The retained initial RED is a no-op recipe postimage, so the first positive
test fails at its required one-result assertion. The full GREEN is the six
methods above after only the template and its manifest digest are corrected.
No old Eclipse runtime, native, ABI or recipe proof is reexecuted by this crate.

The original Windows `Filename too long` failures remain distinct historical
observations. These tests do not emulate Windows, run Git checkout, evaluate
hosted Actions, or establish Maven/Tycho/PDE acceptance of a receiving product.
