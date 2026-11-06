<!-- SPDX-FileCopyrightText: 2026 Hitesh Soliwal and Contributors to the Synexia Project -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Retained Windows checkout observations

`windows-failure-diagnosis.json` is the retained read-only GitHub plugin result
analysis observed on 2026-10-18. The two excerpts preserve its original selected
timestamped job-log lines, with LF line endings. This continuation restored the
record from retained tool results after the scratch filesystem reset; it did
not rerun the jobs or repeat their source/base comparisons.

- Platform: https://github.com/hsoliwal/eclipse.platform/actions/runs/39132434527/job/117690162562
- UI: https://github.com/hsoliwal/eclipse.platform.ui/actions/runs/39132706917/job/117690950893

Both jobs failed in Checkout; no Java/Maven build result is available from them.
The current workflow preimage used by the corrective recipe is independently
pinned to the aggregator fork's `f1c1343f92f68a53dd3593fd3f98a3137e8003c0`
revision. These historical logs do not claim that this exact later workflow
blob was the workflow revision executed by the earlier jobs.
