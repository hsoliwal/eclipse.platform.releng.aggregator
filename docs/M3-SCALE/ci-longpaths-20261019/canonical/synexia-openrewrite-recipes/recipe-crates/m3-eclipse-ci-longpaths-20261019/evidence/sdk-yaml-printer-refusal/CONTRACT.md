<!-- SPDX-FileCopyrightText: 2026 Hitesh Soliwal and Contributors to the Synexia Project -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Eclipse shared CI: Windows checkout contract

This crate owns one reviewed YAML correction in the existing shared workflow:
`.github/workflows/mavenBuild.yml` in `hsoliwal/eclipse.platform.releng.aggregator`.
The receiver preimage is commit `f1c1343f92f68a53dd3593fd3f98a3137e8003c0`,
Git blob `0416c8be3bef180616929288ad634e3b4c7d9515`.

The named recipe `com.synexia.eclipse.CiLongPaths20261019` composes the existing
`com.synexia.rewrite.M3HashPinnedTextSnapshotRecipe`; its shared source is unchanged.
An exact one-row manifest permits only this existing workflow. No absent-before
workflow or new registered control plane is admitted.

## Frozen change

Immediately before the build job's existing Checkout step, insert:

```yaml
    - name: Enable long paths on Windows
      if: runner.os == 'Windows'
      run: git config --global core.longpaths true
```

The step inherits the workflow's existing `cmd` shell on Windows. Its condition
excludes Linux and macOS. Removing those exact three lines must reproduce every
original byte, including permissions, workflow-call inputs, matrix, action pins,
fetch depth, submodule input, Java versions, Maven version and goals, profiles,
baseline/API checks, test execution and artifact upload.

The command configures Git in the temporary hosted runner before checkout. It
does not alter the repository's recorded Git configuration, product source,
public API, gitlinks, or the existing 317 qualified crate files.

## Qualification

The finite Java 21/OpenRewrite SDK suite checks the named and direct existing
owner, exact output, native YAML parser round trip, fixed point, missing/drifted
source, duplicates and path aliases, unrelated sources, input permutations, and
serial/two-worker replay. Output is materialized only from SDK changeset results.
The baseline RED uses the same named SDK recipe with a sealed no-op postimage;
the positive test must fail because no correction is emitted. Its log/XML is
retained before the manifest and postimage advance to the reviewed correction.

This is a recipe and workflow-source qualification. The retained Windows jobs
failed during Checkout with Git exit 128 and `Filename too long`; Java/Maven
setup and builds were skipped. A hosted Windows checkout of the corrected
shared workflow is a separate receiving gate. Linux/macOS/Windows Maven,
Tycho/PDE and whole-Eclipse acceptance are not established by this crate.

## Source and rights

The upstream workflow, exact preimage and reviewed postimage retain Eclipse
Platform's EPL-2.0 license and NOTICE. The first-party recipe descriptor, test,
Maven proof configuration and receipts are Apache-2.0. The recipe's license
does not relicense its workflow payload. This is maintenance of already-public
shared build logic, with no new invention-specific disclosure.

Git for Windows documents `core.longpaths` for C-based Git operations:
https://gitforwindows.org/git-cannot-create-a-file-or-directory-with-a-long-path.html
This setting is not a claim that every Windows tool can handle every long path.

## Publication order

The integration owner publishes the shared workflow commit first. A separate
exact caller recipe then pins Platform/UI to that real immutable commit. This
crate owns no caller rewrite, circular future commit pin, remote ref, or merge.
