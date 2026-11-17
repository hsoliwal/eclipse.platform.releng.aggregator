# Downstream Eclipse fork release source closure

Status: **SOURCE-PREFLIGHT ONLY — NOT RELEASE-ADMITTED**.

This downstream Eclipse Platform aggregator owns the checked-in Git submodule
*revisions* used for an SDK candidate. Its `.gitmodules` records the configured
fork remotes and optional tracking branches; the recorded gitlinks, not those
branch tips, determine the exact checkout. An all-green source preflight does
not assert that a component was compiled, tested or successfully launched.

## Managed component closure (schema v1)

| Aggregator path | Approved fork | Tracking branch |
| --- | --- | --- |
| `eclipse.jdt` | `hsoliwal/eclipse.jdt` | `master` |
| `eclipse.jdt.core` | `hsoliwal/eclipse.jdt.core` | `master` |
| `eclipse.jdt.core.binaries` | `hsoliwal/eclipse.jdt.core.binaries` | `master` |
| `eclipse.jdt.debug` | `hsoliwal/eclipse.jdt.debug` | `master` |
| `eclipse.jdt.ui` | `hsoliwal/eclipse.jdt.ui` | `master` |
| `eclipse.pde` | `hsoliwal/initiative31-eclipse.pde` | `master` |
| `eclipse.platform` | `hsoliwal/eclipse.platform` | `master` |
| `eclipse.platform.swt` | `hsoliwal/eclipse.platform.swt` | `master` |
| `eclipse.platform.ui` | `hsoliwal/eclipse.platform.ui` | `master` |
| `equinox` | `hsoliwal/equinox` | `master` |
| `equinox.binaries` | `hsoliwal/equinox.binaries` | `master` |
| `equinox.p2` | `hsoliwal/p2` | `master` |

`equinox.binaries` is a pinned native executable and launcher-library input.
Its repository has no root Maven POM. The `equinox` reactor consumes those
files through `equinox.binaries.loc`; the other eleven managed components
are declared reactor modules. The binary input retains every fork URL,
tracking branch, gitlink and optional checkout-identity check.

`org.eclipse.jface`, JFace text, JFace data binding, and Eclipse 4 Application
Model (`org.eclipse.e4.ui.model.workbench`) live inside the `eclipse.platform.ui`
component. They keep their established OSGi identities and APIs. Standalone
`hsoliwal/eclipse.platform.text` is not a separate gitlink of this aggregator;
its source must not silently be substituted for the Platform UI build input.

## Reproducible source gate

Run from a Git checkout of the aggregator:

```sh
python3 -m unittest discover -s scripts/tests -p 'test_fork_source_preflight.py' -v
python3 scripts/fork_source_preflight.py --root .
# After initializing the selected gitlinks, also verify checkout identity:
python3 scripts/fork_source_preflight.py --root . --require-checkout
```

The standard gate verifies the committed `.gitmodules` and `pom.xml` anchors,
the exact 12 fork URLs and tracking branch declarations, the eleven managed
reactor modules, the separate Equinox binary-input role, and each pinned
40-character gitlink at `HEAD`. It rejects missing,
renamed, unexpected or unpinned components, and dirty local anchor files.
The optional checkout gate also verifies that every initialized submodule's
current commit equals its parent gitlink. It does **not** fetch or move source,
resolve remote branch tips, or modify submodule configuration. In CI use
`git submodule update --init --recursive` only after first inspecting source
pins, and do not add `--remote` to a reproducibility build.

The program emits one deterministic JSON report with `source_closure_passed`,
`release_admitted: false`, the parent commit, checked pins and error strings.
It fails with nonzero exit code on source closure drift. Even a successful run
must never be interpreted as a product release authorization or a semantic
content-equivalence claim; equality is established only for the compared Git
commit identifiers. No artifact signature or provenance is authenticated.

## Independent product-release gates

**Release is held** until there is a final, immutable aggregator commit and
component gitlink set with verified evidence for all claimed deliverables:

1. Tycho/Maven reactor `clean verify` on supported build JDKs, with platform
   API Tools/Javadoc/OSGi resolution and unsuppressed, source-bound test results.
2. SWT cross-platform native/JNI ABI and resource/UI tests for GTK3 X11,
   GTK4 X11, GTK4 Wayland, Windows, macOS Intel and macOS ARM. SWT's own
   preparation documents define stronger backend-specific evidence requirements.
3. JFace viewers, databinding and text; Eclipse 4 Application Model, RCP,
   workbench, command and lifecycle tests, including actual UI harness runs.
4. Equinox OSGi framework activation, p2 resolver and PDE/JDT integration,
   followed by SDK product installation and launch on each advertised OS/arch.
5. API and binary compatibility against an explicit upstream baseline,
   preserving `org.eclipse.*` package names, bundle IDs and extension points.
   Any change to public interfaces or native signatures requires independent
   approval rather than an implicit fork rename.
6. Release manifest covering repository+commit pairs, actual test/coverage
   denominators and exclusions, build logs, native artifact SHA-256 hashes,
   license/NOTICE and donor provenance, SBOM, signature, and publishing
   authorization. Source/file presence is not execution coverage.

Existing upstream workflows or historical passing jobs cannot qualify a new
fork candidate. Avoid publication, tag creation, signing and automatic merge
until the required gates are actually green for the final release commit.
