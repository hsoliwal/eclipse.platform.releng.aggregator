<!-- SPDX-FileCopyrightText: 2026 Hitesh Soliwal and Contributors to the Synexia Project -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Frozen composition contract

- The aggregator preimage is `0f1cb47ce80d9cf91fbb3ec4cbeccfcd366691b9`.
- Exactly the existing twelve top-level SDK modules remain selected.
- Only `eclipse.platform`, `eclipse.platform.swt` and `eclipse.platform.ui` select
  the user's public forks. Their new commit IDs must already exist in those forks.
- The other nine module URLs and Git object entries remain byte-for-byte pinned.
- The text recipe may emit only root `.gitmodules` and
  `docs/M3-SCALE/composition-20261018/composition.tsv`.
- Missing or drifted required preimages, duplicate targets, occupied additions
  and template digest drift fail before any recipe result is admitted.
- Exact postimages are a fixed point. Unrelated source is preserved.
- Git object updates use normal Git operations after the exact three old/new
  entries are reviewed. Git internals are outside the text recipe's scope.
- The read-only source verifier requires twelve actual initialized, clean
  worktrees whose HEADs, index gitlinks and declared URLs agree with the manifest.
- The report verifier requires one actual passing named JFace method. It applies
  bounded reads and secure XML parsing; absent, skipped or failed native work
  cannot satisfy that contract.
- This composition adds no product wrapper, parallel widget tree, runtime loader
  or dependency on a private Synexia artifact.
