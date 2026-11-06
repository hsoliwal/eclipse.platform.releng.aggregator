# Eclipse SDK superset composition (22 October 2026)

This review branch combines seven existing `hsoliwal` Eclipse forks and
retains the other five upstream Eclipse gitlinks at their original commits.
The complete, immutable mapping is [composition.tsv](composition.tsv).

## Authority

- Canonical generator:
  `hsoliwal/com.synexia`,
  `synexia-openrewrite-recipes/recipe-crates/m3-eclipse-composition-20261022`,
  named `com.synexia.eclipse.Composition20261022`.
- Actual Java21/OpenRewrite proof: **6/6** JUnit tests passed, exact source
  hashes and generated `.gitmodules` / `composition.tsv`.
- Gitlinks: twelve Git tree entries (`160000`) must match the
  associated manifest row SHA and declared remote URL.
- This aggregator is a source build assembler, not a production runtime
  dependency on the private Synexia recipe repository.

## Included review branches

| Module | Selected source | Receipt |
| --- | --- | --- |
| Eclipse Platform | `hsoliwal/eclipse.platform` Compare correction | PR #17 |
| Eclipse SWT | `hsoliwal/eclipse.platform.swt` host/fragment alignment | PR #246 |
| Eclipse UI/JFace | `hsoliwal/eclipse.platform.ui` marker selection repair | PR #43 |
| JDT Core, Debug, UI | respective `hsoliwal` fork masters | Current master pins |
| Equinox | `hsoliwal/equinox` master | Current master pin |
| JDT parent/binaries, PDE, Equinox binaries/p2 | existing upstream | Unchanged |

The three receiver commits above remain **draft PR** heads, not merged master.
An aggregator gitlink is a reviewed immutable commit, even when reached via
a receiver branch. These pins must be reassessed after child PR promotion.

## Product acceptance still required

1. A clean aggregator checkout with twelve initialized submodules passes
   the existing `M3EclipseComposition source` SHA/URL/index verifier
   using this manifest.
2. The entire Tycho reactor compiles, packages and generates API docs with
   JDK8/11/17/21/25 toolchains; external documentation TLS is verified.
3. SWT GTK/Win32/Cocoa natives, JNI, JFace/Nebula, JDT, Resources,
   Equinox/p2, PDE and headless workspace/marker/delta tests pass.
4. M3JDK21 integrated-image compatibility and public API/ABI baselines pass.
5. Pending UI PRs #27/#35/#37/#42 are reviewed for a superset merge; this
   branch does not silently merge, squash, override or delete them.

Keep the aggregator PR draft until the actual assembled SDK meets these gates.
The original 18 October composition remains historical evidence; this is
a new, versioned source manifest rather than an in-place rewrite.
