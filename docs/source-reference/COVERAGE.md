# Coverage and verification ledger

> Inspected source revision: `55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c`. Source/manifest observation only; builds and tests were not run.

[Reference home](README.md) · [Selected contracts](CONTRACTS.md) · [Coverage](COVERAGE.md)

## Exact structural denominators

| Observation | Count |
| --- | ---: |
| entries | 3516 |
| blobs | 3170 |
| gitlinks | 12 |
| java_files | 70 |
| java_files_read | 70 |
| java_paths_unread | 0 |
| java_source_directories | 13 |
| unique_java_blobs_unread | 0 |
| java_blob_reads | 70 |
| namespaces | 12 |
| namespace_directory_origins | 12 |
| no_recognized_package | 6 |
| metadata_unit_paths | 49 |
| workspace_descriptors | 25 |
| pom_files | 13 |
| bundle_manifests | 13 |
| feature_descriptors | 5 |
| parsed_module_edges | 31 |
| non_profile_reachable | 32 |
| additional_source_files | 19 |

Counts refer to this repository tree only. Files under gitlinks are not expanded; their recorded commit boundaries remain explicit. Workspace, POM, bundle, feature and module-path counts overlap and must not be added as independent projects. Repeated namespaces in fixtures/tests are retained with their separate origins. Neither a manifest nor a Java filename is proof that a type is public API.

## Inventory method

1. Read the pinned root tree, then each top-level subtree recursively. Every returned subtree was non-truncated; gitlinks remain separate commit references.
2. Read every tracked POM, `.project`, bundle `MANIFEST.MF`, `feature.xml` and `build.properties`; retain parent/module/profile edges and OSGi qualifiers. Parse source ownership by the nearest descriptor/module path, not by a package name guess.
3. Read every tracked `.java` file, deduplicating identical blobs for transport but retaining all paths. Verify decoded content against Git blob SHA-1 by UTF-8 or, when needed, lossless Latin-1 reconstruction; this checks the reconstructed bytes rather than assuming the connector returned raw bytes. Remove comments/literals for lexical package/import accounting. This is not a Java compiler and does not process Unicode escapes, annotation semantics, bytecode or embedded template languages.
4. Inventory additional source/script suffixes separately. Preserve existing native package docs and link them; this Markdown pass does not modify source comments or generate native package Javadoc.
5. Distinguish all parsed non-profile Maven declarations from effective activation. `.mvn` flags, inherited POMs, pomless Tycho model generation and profiles can alter the effective reactor. The selected build guide explains observed configuration; Maven was not executed.

## Verification status

- Complete tree traversal: tracked-path inventory complete within the pinned Git tree; no truncated subtree accepted
- Source/metadata byte verification: all fetched bodies used for this inventory reconstruct to recorded Git blob hashes (UTF-8 or lossless Latin-1)
- Semantic API/lifecycle documentation: selected implementations only, not all packages or members
- Native package/source documentation: existing files linked; additions and reconciliation remain open
- Repository build, lint, tests, UI/native execution, generated Javadoc and effective Maven model: NOT RUN; repository execution was outside this editorial pass
- Documentation links and remote commit/readback checks: recorded separately in the PR delivery; source links here are immutable snapshot references

## Remaining work

Substantive package-by-package API/error/state/resource/threading review remains necessary beyond the named selected contracts. Complete any outstanding named-package declaration reads, then read non-Java/embedded programs, generated and binary inputs, inherited configuration and separately owned gitlinks at their own revisions. Then execute the applicable build/API/tests in an authorized environment and retain exact receipts. Inventory completeness must never be reported as complete semantics, compatibility, performance, M3 proof, release readiness or a passing test run.

M3 research directions in fork prose remain proposed/evaluative context. The inventories do not establish implementation of named IRs, proof engines, deterministic promotion, or runtime integration. Upstream identity, existing notices and file-level license terms remain unchanged.
