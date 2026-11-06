# Eclipse SDK aggregator: build hierarchy and selected implementation contracts

## Scope, revision and evidence

This guide describes `hsoliwal/eclipse.platform.releng.aggregator` at PR #6 head **`55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c`**. It is an editorial source inspection, not a build report. The fork retains Eclipse SDK aggregation, documentation, product assembly and release-engineering sources. Its introductory M3 direction is a proposal/evaluation context, not evidence that M3 runtime behavior is implemented throughout the SDK. [Revision][revision] · [README][readme]

Evidence comprises the pinned recursive Git tree, checked-in POMs/manifests/build properties, selected complete Java implementation bodies and their checked-in tests, plus pinned target/product/category/assembly definitions. The implementation discussion is deliberately selective; it does not claim to specify every Java class, script, native binary or component submodule. A filename or exported package alone is not a behavioral contract.

**Build: NOT RUN. Tests: NOT RUN. Runtime/UI/native execution: NOT RUN.** No Maven invocation, repository script, installation, signing, deployment or source/configuration change was performed for this guide. Described outputs and failure paths are source-derived expectations, not observed artifacts or passing checks.

Eclipse Foundation, IBM, Red Hat, vogella, Hannes Wellmann and other contributor attributions remain attached to their respective sources. The root license/notice and individual file/component licenses remain authoritative; for example, the principal POM headers identify EDL terms while many Java sources identify EPL-2.0. This guide does not relicense those materials. [License][license] · [Notice][notice]

## 1. Four different relationships in the build

1. **Git ownership:** a gitlink records another repository's exact commit. Its contents are not ordinary files owned by this aggregator commit.
2. **Maven aggregation:** `<modules>` puts projects into the reactor. The root declares 17 direct entries, including six directories owned here and eleven gitlink paths.
3. **Maven inheritance:** `<parent>` supplies shared configuration. The root `org.eclipse.platform:platform-aggregator:4.42.0-SNAPSHOT` is a `pom` aggregator with no parent declaration; it is not the common inherited parent.
4. **OSGi/p2 composition:** bundle manifests, features, target definitions, products and categories supply runtime/dependency/installation relationships. These are not interchangeable with Maven modules. [Root reactor][root-pom] · [Shared parent][parent-pom]

The root module sequence is `eclipse-platform-parent`, `eclipse.platform.releng.prereqs.sdk`, the five JDT gitlinks, PDE, Platform, Platform UI, common documentation, SWT, Equinox, p2, releng, products and sites. Maven/Tycho resolves actual reactor dependencies; the textual list is not evidence that each module executes strictly in that order under parallel builds. [Root reactor][root-pom]

The checked-in local child POMs for prerequisites, common, releng, products and sites inherit `org.eclipse:eclipse-platform-parent:4.42.0-SNAPSHOT`, using `../eclipse-platform-parent`. `sites/eclipse-junit-tests` instead inherits `org.eclipse:sites` at that version; the ISV documentation POMs inherit `eclipse.platform.common`. Those are real parent edges. Component-internal parent edges must be inspected at each gitlink's recorded revision rather than inferred from this root list. [Prerequisites][prereqs-pom] · [Common][common-pom] · [Releng][releng-pom] · [Products][products-pom] · [Sites][sites-pom]

### Top-level role map

| Area | Role evidenced in this checkout |
| --- | --- |
| `pom.xml`, `.mvn/` | Reactor entry point, Tycho build extension and aggregator-mode property |
| `eclipse-platform-parent/` | Shared compiler, target, packaging, test, baseline and optional release-tool configuration |
| `eclipse.platform.releng.prereqs.sdk/` | `eclipse-target-definition` artifact and external prerequisite target |
| Twelve gitlink paths below | Separately owned component/binary revisions; eleven appear directly in the reactor |
| `eclipse.platform.common/` | Five declared documentation/tips modules and sibling-component source paths for generated reference docs |
| `eclipse.platform.releng/` | Releng bundles/features, including test harness and performance support |
| `products/` | Four product assemblies driven by `.product` and pomless `build.properties` inputs |
| `sites/` | Three repository/test-distribution modules; also checked-in website assets and calendar outside that module list |
| `scripts/` | JDK-only source-code programs for releng/testing; not a root Maven module |
| `production/` | Production/test bootstrap material, referenced by Jenkins and the test assembly |
| `oomph/` | Developer-workspace setup referenced by README; not a root Maven module |
| `.m3/` | Additive intake/recipe overlay, absent from the default root module list |
| `jobs/` | Checked-in Jenkins job definitions and shared Groovy support; not a root reactor module |
| `cje-production/` | Checked-in container definitions, build properties and macOS notarization script; not a root reactor module |
| `.github/`, `.settings/` | Workflow/dependency-bot files and Eclipse workspace preferences respectively; not reactor modules |

These roles are grounded in the root/child POMs, [script README][scripts-readme], [Jenkinsfile][jenkins], [test assembly][test-assembly] and [checkout README][readme]. For `jobs/`, `cje-production/`, `.github/` and `.settings/`, the table records tree-level file categories only; their individual execution behavior is outside this guide’s implementation review. [Pinned tree][tree] Presence under the repository root does not itself make an area a default build module.

## 2. The twelve gitlink boundaries

The tree records mode `160000` entries at the following commits. `.gitmodules` points all twelve at upstream Eclipse repositories and declares `branch = master`; that branch hint does not replace the recorded gitlink SHA during an ordinary recursive checkout. A clone of this fork does not automatically consume sibling `hsoliwal` forks. [Git tree][tree] · [Submodule declarations][gitmodules]

| Path | Upstream repository | Recorded commit |
| --- | --- | --- |
| `eclipse.jdt` | `eclipse-jdt/eclipse.jdt` | `36db39a9a02496f1feb6f7d5d7a589c6a7280f03` |
| `eclipse.jdt.core` | `eclipse-jdt/eclipse.jdt.core` | `ae59b256b63e69cc67391fab13ddb8ec42b26a25` |
| `eclipse.jdt.core.binaries` | `eclipse-jdt/eclipse.jdt.core.binaries` | `987122d226c7ee6b501d8bc67a2bcda034f2fd6f` |
| `eclipse.jdt.debug` | `eclipse-jdt/eclipse.jdt.debug` | `ef201028f40e2fd41795fff965fd196f47cd4753` |
| `eclipse.jdt.ui` | `eclipse-jdt/eclipse.jdt.ui` | `99a1a338afacd54532825213f184f7191db61b31` |
| `eclipse.pde` | `eclipse-pde/eclipse.pde` | `56e5443583f4078624f8a2a4299495ea610bea11` |
| `eclipse.platform` | `eclipse-platform/eclipse.platform` | `8fa7d88c3a6c625d90cc8a43c25e5327ba9fcb71` |
| `eclipse.platform.swt` | `eclipse-platform/eclipse.platform.swt` | `6e0937b7db830bd1491ee4711497cf1ac8be1270` |
| `eclipse.platform.ui` | `eclipse-platform/eclipse.platform.ui` | `e71f29b260dd0ace91ee9b7e9d95dfa3fc99accf` |
| `equinox` | `eclipse-equinox/equinox` | `66584d130d22951aac8f42079948fe3c757d64ca` |
| `equinox.binaries` | `eclipse-equinox/equinox.binaries` | `71ca93aa517069ffe41c9470ca4d232e305f50dc` |
| `equinox.p2` | `eclipse-equinox/p2` | `bc7e3d0756a893e3865b0ed00ba8f9448d9cbbc1` |

**Important exception:** `equinox.binaries` is a gitlink but is absent from the root `<modules>` list. Do not describe all twelve as direct Maven reactor modules or assume its absence means its binaries are irrelevant to other components. Determining its downstream use requires component-source inspection. [Root reactor][root-pom]

For reproducibility, retain the aggregator SHA, all gitlink SHAs and any deliberate component overrides. The tree alone does not establish that component directories have been initialized, that remote dependency artifacts remain available, or that an assembled SDK contains an unrecorded fork change.

## 3. Shared parent and activation contract

`.mvn/extensions.xml` selects `org.eclipse.tycho:tycho-build:5.0.4`; `.mvn/maven.config` supplies `-DaggregatorBuild=true`. This extension matters for pomless projects: many checked-in bundles/features/products/sites have manifests or product/category descriptors and model-adjusting `build.properties`, rather than individual POM files. Generated/polyglot Maven models are build metadata, not additional checked-in application implementations. [Extension][mvn-extension] · [Maven config][mvn-config]

The shared parent also pins `tycho.version=5.0.4`, `cbi-plugins.version=1.5.7` and `surefire.version=3.5.6`. Its release metadata describes the 4.42 stream and 2026-12 branding. `buildType` defaults to `I`; `buildId` concatenates that type with the formatted Maven build timestamp. These defaults are configurable inputs, not a claim that this documentation review produced an integration build. [Parent properties][parent-properties]

### Always-declared build behavior versus managed configuration

- Under `<build><plugins>`, the parent declares the Tycho Maven extension, prerequisite target selection, source-bundle generation, baseline-version comparison and API-description generation. The filtered `saveproperties` resource-copy execution is explicitly `inherited=false`.
- `<pluginManagement>` supplies versions/configuration for compiler, packaging, Surefire, p2, director, documentation and maintenance tools. Merely appearing there does not mean a tool runs in every project; a lifecycle binding, child declaration or explicit invocation must use it.
- Compiler configuration selects ECJ from `cbi-ecj-version=[3.39,)`, uses project settings, enables Javadoc analysis and writes XML compile logs to `${project.build.directory}/compilelogs`. `-proceedOnError` in compiler arguments does not establish a successful Maven result.
- Packaging derives timestamps with JGit, generates source references, ignores POM/polyglot/gitignore/Markdown changes for that timestamp calculation, and adds generated `.api_description` content. Dirty-tree handling defaults to `ignore`; this is not a clean-checkout guarantee.
- Managed Tycho Surefire enables assertions, combines four configurable argument fragments and passes `eclipse.test.screenshot_directory`. Mac-specific first-thread arguments are activated separately.
- Managed p2 baseline comparison uses `warnCommon`, comparator repositories and ignored signature-file patterns. This is distinct from the separate version-bump comparison goal and from API verification. [Parent build/plugins][parent-build] · [Managed plugins][parent-managed]

The parent target is `org.eclipse:eclipse-sdk-prereqs:4.42.0-SNAPSHOT`. Eight target environments are declared: Linux GTK on x86_64, ppc64le, riscv64 and aarch64; Windows on x86_64 and aarch64; macOS Cocoa on x86_64 and aarch64. This is target resolution/assembly configuration, not evidence of test execution on eight machines. [Target selection][parent-target]

The target file supplies versioned p2 units from Orbit, EMF, ECF, the CBI license repository and CDT, plus Maven dependencies. Maven locations declare compile scope, no transitive dependency-depth traversal, source inclusion and `missingManifest=error`; p2 locations request all platforms, source inclusion and slicer mode. Test dependencies and shipping prerequisites are mixed within this build-resolution input, so target membership alone does not prove inclusion in a shipped product. [Prerequisite target][prereqs-target]

### Activation and default-value ledger

| Control | Actual checked-in behavior |
| --- | --- |
| `skipTests` | Parent default is `false`; README's faster example and Jenkins explicitly set it true |
| `build-individual-bundles` | Activates when the `aggregatorBuild` property is absent, adding an Eclipse p2 repository; presence is the test, not a boolean-value comparison |
| `jdt-y-build` | Activates for environment property `BUILD_TYPE=Y`, switching the comparator repository to Y builds |
| `skip-baseline-comparision-of-tests` | Exact profile spelling; activates for `packaging=eclipse-test-plugin`, forcing version-baseline checking off |
| `skip-javadoc-of-tests` | Same packaging condition; sets `maven.javadoc.skip=true` |
| Version-baseline checking | `compare-version-with-baselines.skip=true` by default; Jenkins overrides it to false |
| `eclipse-sign` | Opt-in profile, without an automatic activation declaration; adds signing-related executions |
| `bree-libs` | Opt-in profile connecting compiler `useJDK` to the default `BREE` property |
| `dependency-check`, `api-check` | Optional check profiles; API verification is explicitly not active by default |
| `update-branding-plugins-about.mappings` | Activates when the project has `about.mappings`, filters it into `target` and packages that generated copy |
| `macos` | OS-family activation supplies `-XstartOnFirstThread` to Surefire |
| `javadoc`, `checkstyle`, `javac`, `p2-repository-modification` | Optional profiles; `javac` also disables baseline comparison/replacement behavior |

Source: [parent profiles][parent-profiles]. `api-check` verification uses the previous-release baseline, honors `skipAPIAnalysis`, sets `skipIfReplaced=false` and `runAsJob=false`. It is separate from the ordinary API-description `generate` execution. Likewise, managed `generate-repo-report` and `generate-api-report` use `<phase>none</phase>` to require explicit invocation. A default build should not be described as having run these reports. [Managed reports][parent-reports]

### Java versions are separate contracts

README requires Java 25+ and Maven 3.9.12+ for the build, and Jenkins selects a JDK 25 tool. The parent also has `java.version=17`, managed Javadoc source 25 and an Eclipse-run execution environment of JavaSE-25. Bundle BREEs vary: performance support is JavaSE-17, the test harness is JavaSE-21, and Platform documentation tips are JavaSE-25. Do not flatten these into a single minimum runtime version for every bundle. [README requirements][readme] · [Parent][parent-pom] · [Performance manifest][perf-manifest] · [Harness manifest][test-manifest] · [Tips manifest][tips-manifest]

## 4. Product and repository inputs, outputs and signing

`products/pom.xml` declares `eclipse-platform`, `eclipse-sdk`, `equinox-launcher` and `equinox-starterkit`. Their `build.properties` adjust the pomless model; their `.product` files describe composition. The products parent defaults both `product.installSources` and `repository.includeAllSources` to false, and explicitly warns that source installation requires source inclusion in the repository. [Products parent][products-pom]

| Product | Composition and model changes |
| --- | --- |
| Eclipse Platform | ID `org.eclipse.platform.ide`; Platform + p2 user UI features; repository sources enabled, installation of sources left at the parent default |
| Eclipse SDK | ID `org.eclipse.sdk.ide`; SDK + p2 user UI, with e4 core tools, tips and terminal installed as roots; enables repository sources and source installation |
| Equinox launcher | ID `equinox-launcher`; mixed product containing the executable feature; `.product` has `includeLaunchers=false` |
| OSGi Starter Kit | ID `org.eclipse.rt.osgistarterkit.product`; Equinox core and p2 core/extras; console/no-exit startup and `eclipse.ignoreApp=true` |

The Platform and SDK products explicitly set `-Dosgi.requiredJavaVersion=25`, first-thread macOS arguments and enabled 4.42/2026-12 update locations. Those product runtime arguments are different from the BREE of individual bundles. Platform/SDK root folders are `eclipse` and `Eclipse.app`; the Starter Kit uses `rt` and `Rt.app`. [Platform product][platform-product] · [SDK product][sdk-product] · [Launcher product][launcher-product] · [Starter Kit product][starter-product] · [SDK properties][product-properties] · [Platform properties][platform-properties] · [Launcher properties][launcher-properties] · [Starter Kit properties][starter-properties]

Managed p2 repository assembly includes all product dependencies. Director materialization uses `SDKProfile`, `source=repository`, configurable source installation and `parallel=true`; the `materialize-products` execution is placed at `prepare-package` so repository PGP signing precedes materialization and Windows/macOS signing follows it. The POM comment identifies its use from generated pomless-product models. This is product-materialization concurrency, not an API thread-safety promise. [Products parent][products-pom]

Within the optional `eclipse-sign` profile, Windows and macOS signing run at `package`; PGP signing runs at `prepare-package`; signed macOS DMG packaging is configured at `pre-integration-test`. Product/site parents default `eclipse.signing.skip=true` inside that profile, while selected child properties set it false. Platform, SDK and Starter Kit opt in through their child values; launcher properties do not. A child `skip=false` does not independently activate the signing profile. [Products signing][products-signing] · [Sites signing][sites-pom]

Windows signing searches `${project.build.directory}/products/${product.id}/win32/`; macOS signing searches the corresponding `macosx/` tree and uses shared entitlements. Timeouts are 300 seconds for macOS signing and 600 seconds for DMG packaging; `macSigner.forceContinue` defaults false. Parent JAR signing uses `DO_NOT_RESIGN` and a 120-second timeout. These are consequential release operations; this guide neither ran nor authorized them. [Products signing][products-signing] · [Parent profiles][parent-profiles]

`sites/pom.xml` declares three modules. `eclipse-platform-repository` includes all dependencies and sources, with SDK/Platform IUs, JDT/PDE/RCP/Equinox features and selected tests/tools from its category descriptor. `equinox-sdk-repository` includes sources but not all dependencies, with Equinox SDK, p2 SDK and core-runtime features as inputs. Category membership is repository content selection, not a statement that every entry is installed in every product. [Platform category][platform-category] · [Equinox category][equinox-category] · [Platform-site properties][site-properties] · [Equinox-site properties][equinox-site-properties]

`sites/eclipse-junit-tests` is an explicit `eclipse-repository` POM with both source and dependency inclusion disabled. At `package`, the CBI plugin writes `target/resources/finalPluginsVersions.properties` and `target/resources/test.properties`; Maven Assembly combines those generated files, checked-in test scripts and the repository ZIP under `eclipse-testing/`. The inner repository ZIP is renamed `eclipse-junit-tests-${buildId}.zip`. This assembles a test distribution; it does not itself prove the tests ran. [Test-site POM][test-site-pom] · [Assembly descriptor][test-assembly]

README names successful local-build output locations: `products/eclipse-sdk/target/products`, `products/eclipse-platform/target/products` and `sites/eclipse-platform-repository/target/repository`. Production download filenames used by reporting tools are a later publishing contract, not necessarily the raw local Maven filenames. [README outputs][readme] · [Drop generator][drop-generator]

## 5. Documentation is both authored input and generated build content

The common POM declares five modules: Platform ISV docs, Platform user docs, Platform doc tips, JDT ISV docs and JDT user docs. `bundles/org.eclipse.jdt.tips.user` exists with source/metadata but is not in this POM's declared module list; directory discovery must not silently turn it into a default-reactor member. [Common POM][common-pom]

Both ISV-doc POMs activate `build-docs` by absence of the deliberately named `longnotexistingproperty`, rather than ordinary `activeByDefault`. This keeps their usual activation from depending on whether another profile was selected. Their schema-to-HTML executions read component `plugin.xml`/schemas through relative paths into sibling gitlinks, so a partial checkout can be inadequate even for a documentation build. [Platform ISV POM][platform-doc-pom] · [JDT ISV POM][jdt-doc-pom]

The Platform ISV build generates extension-point docs during `process-resources`, copies example resources into `samples`, produces Javadoc at `process-classes`, then copies generated API docs into `reference/api` at `prepare-package`. JDT schema generation and Platform-doc unpacking run at `process-resources`; JDT Javadoc and its copy run at `prepare-package`. Both Javadoc executions explicitly use `failOnError=true`, overriding the parent's general relaxed Javadoc default for these executions. [Platform ISV POM][platform-doc-pom] · [JDT ISV POM][jdt-doc-pom]

Some generated documentation is copied under the source project's `reference/` directories, not only under `target/`. Platform ISV `clean` also has configured deletions for `index`, generated API/extension-point content and samples, with selected authored indexes excluded. Distinguish authored entry pages from build-generated content before treating a documentation diff as a source change. These clean operations were inspected, not executed. [Platform ISV POM][platform-doc-pom]

## 6. Selected exported test-harness contracts

`org.eclipse.test` is shipped as an `eclipse-plugin` support bundle even though it supplies testing machinery; its build properties explicitly override that packaging. It exports `org.eclipse.test` and imports bounded JUnit 5/Platform 1 package versions. This is different from a project packaged as `eclipse-test-plugin`, which triggers the parent test-only profiles. [Harness build properties][test-build] · [Harness manifest][test-manifest]

### `EclipseTestRunner`: arguments, class loaders and result ownership

- `run(String[])` accepts a first positional test-class name, or paired flags such as `-classname`, `-testpluginname` and `-resultpath`. Multi-suite mode requires both comma-separated `-classesnames` and `-testpluginsnames`.
- Multi-suite class and plug-in arrays are paired by index; the code does not validate equal lengths before indexing. Missing a single-mode class name throws `IllegalArgumentException`.
- `propsfile=` reads an Ant-style properties file; system properties overlay those values. Optional `-timeout` starts a timeout-dump timer, using `-junitReportOutput/timeoutScreens` or `timeoutScreens` as its output directory.
- Each suite is selected by class name through a JUnit Platform launcher. Class-loader construction combines the test bundle with available engine bundles; an explicit missing bundle yields a diagnostic `IllegalArgumentException` from package-private `ClassLoaderTools`.
- The runner temporarily changes the current thread's context class loader, creates the launcher after setting the engine loader, then switches to the test loader and restores the original in `finally`.
- Engine discovery intentionally excludes service-provider bundles whose major version is 6 or higher; the source explains the JUnit type-identity mismatch this avoids.
- Results use `LegacyXmlResultFormatter`. `SUCCESS=0`, `FAILURES=1` and `ERRORS=2`; observed JUnit `FAILED` events produce 1, caught output/formatter `IOException` produces 2. Other unchecked failures are not uniformly converted to 2.
- A result directory gets `TEST-<class>.xml`; multi-suite mode always resolves that filename below the supplied path. With no path, the returned output stream is `System.out`, included in the runner's try-with-resources block. Callers embedding the runner should account for that stream ownership rather than assume stdout remains open.

Source: [complete runner][test-runner] · [class-loader helper][classloader]. The thread-context restoration is a concrete local guarantee; it does not make the entire OSGi/UI test infrastructure safe for arbitrary concurrent invocation.

`CoreTestApplication.start` obtains application arguments, but its `run` method uses `Platform.getCommandLineArgs()` rather than the passed value. Its retained `processCommandLine` helper recognizes `-deltas`, yet the normal `run` path does not invoke that helper. `UITestApplication` selects `-testApplication` or `org.eclipse.ui.ide.workbench`, attaches itself to `PlatformUI.getTestableObject()`, starts the selected application, then delegates test execution through `TestableObject.runTest`. An `IOException` in that callback is printed and can leave the initialized result `-1`; `stop()` is empty in both applications. [Core application][core-app] · [UI application][ui-app]

### Screenshot ownership and external process effects

`Screenshots.onFailure(Supplier<Widget>)` is a JUnit 4 `TestWatcher`: on failure it captures an image and attaches the filename as a suppressed throwable; on completion it disposes the supplied widget even after a successful test. Its contract tells callers not to dispose that widget in `@After`, because capture must occur first. Disposal happens directly in the rule callback; it does not marshal SWT operations onto another thread. [Screenshot support][screenshots]

Output-directory precedence is `-junitReportOutput`, then system property `eclipse.test.screenshot_directory`, then `java.io.tmpdir`. Filenames combine test class and supplied name. `AwtScreenshot` starts a separate Java process, captures the desktop through AWT Robot, forwards stdout/stderr using helper threads, waits up to 15 seconds, then destroys a still-live process and throws. Nonzero child exit also becomes a runtime failure. Screenshot support therefore needs a usable graphical environment and has process/filesystem effects; it is not a pure formatter. [Screenshots][screenshots] · [AWT implementation][awt-screenshot]

## 7. Performance API: lifecycle, selection and limits

`org.eclipse.test.performance` exports the public-facing performance package and several packages whose names contain `internal`, including its tests. Export visibility must not be read as a promise that all of those internal types are stable client extension points. `Performance` and `PerformanceMeter` explicitly say clients should not subclass them. [Performance manifest][perf-manifest] · [Public facade][performance] · [Meter API][meter-api]

The documented meter protocol is: create one meter for a scenario; repeat `start` → measured operation → `stop`; `commit` exactly once before analysis; finally `dispose` exactly once. No method may be used after disposal, and no new measurement may begin after commit. These are caller obligations; the selected implementations do not uniformly enforce a complete state machine. [Meter API][meter-api]

Factory selection first tries the `PerformanceMeterFactory` system property, then the plug-in debug option, then `OSPerformanceMeterFactory`. An OSGi class name may use `bundleName:className`; outside a running Platform it uses normal class loading. Several reflection errors are logged before falling back. The lazily cached factory means changing the property after first use does not necessarily replace an existing factory. [Performance factory selection][performance]

The internal factory uses a static unsynchronized `HashSet` of scenario names. Creating a duplicate throws `IllegalArgumentException`; disposal does not remove the name from that registry. Scenario uniqueness is therefore wider than the lifetime of a particular meter. The lazy `Performance` singleton, factory registry and meter lists do not supply a general concurrent-use guarantee. [Factory implementation][meter-factory] · [Internal meter][internal-meter]

`PerformanceTestCaseJunit5` obtains a meter in `@BeforeEach` using the test class plus `TestInfo.getDisplayName()`, and disposes it in `@AfterEach`. Repeated/custom display names can therefore matter to scenario identity; they are not replaced by a universally unique invocation identifier in this code. The helper delegates actual start/stop/commit/assert calls through its shared base class. [JUnit 5 adapter][perf-junit5] · [Shared adapter base][perf-base]

### Measurement and persistence behavior

- `OSPerformanceMeter` appends `BEFORE` and `AFTER` snapshots containing dimension/scalar maps. `getSample()` collects global run information and returns a new sample; after disposal it returns null.
- `InternalPerformanceMeter.commit()` attaches summary/comment metadata and optionally prints statistics. `InternalPrintCsvPerformanceResults` opens its configured file in overwrite mode; the output is tab-separated despite the property's CSV name.
- `InternalWriteRawPerformanceData` opens an append-mode object stream and writes scenario ID, variations and sample. These optional I/O failures are caught and printed, not rethrown as a persistence-success guarantee.
- The selected `commit()` body does not write to a results database. Its API documentation allows implementations to persist data, but that abstract possibility is not evidence of database persistence here.
- `SystemTimePerformanceMeter` uses `System.currentTimeMillis()`, checks equal start/stop list sizes and prints durations in its override of `commit()`. It does not call the superclass commit routine, so it does not inherit those optional output side effects merely by subclassing it.

Sources: [OS meter][os-meter] · [Internal meter][internal-meter] · [System-time meter][system-meter]. Callers own meter disposal and must distinguish an output path being configured from an output file having been written successfully.

Linux measurement reads `/proc/self/stat`, `/proc/self/statm` and the output of `free -b`; its checked-in constants use page size 4096 and jiffy multiplier 10. Windows consults native counters only when the native support is loaded; macOS attempts `perf_3_1_0` and can continue without it. Linux/macOS elapsed-process time also depends on usable `eclipse.startTime`. Missing sources can reduce available dimensions, so cross-platform numbers should not be assumed to have identical coverage. The monitor collection methods synchronize selected operations, but this does not synchronize each meter's mutable sample list. [Linux monitor][linux-monitor] · [Windows monitor][windows-monitor] · [macOS monitor][mac-monitor]

### Exact limitation of the inspected assertion path

`Performance.assertPerformance()` constructs a relative checker for `ELAPSED_PROCESS` with an upper factor of 1.10. **At this pinned revision, the selected `Evaluator.evaluate()` implementation does not actually invoke its collected checkers against baseline measurements.** It checks configuration/reference keys, accepts internal meters, asserts a non-null sample, collects dimensions and session data, and then reaches the end of the method. Missing reference keys or absent session data can return early. [Facade assertion setup][performance] · [Complete evaluator body][evaluator]

This conclusion is confined to that facade/default-evaluator path and those complete source bodies. It does not claim that all Eclipse performance tooling, every other evaluator, native monitor or external reporting service lacks checks. Do not use a nonthrowing call through this inspected path as standalone proof of an enforced 10% regression threshold.

The checked-in `PerformanceMeterFactoryTest` verifies an OS-meter selection; `SimplePerformanceMeterTest` exercises create/start/stop/commit/dispose; package-private `TestPerformanceMeter` supplies deterministic sample data. These are test sources and useful examples of intended use, not executed validation in this review, and those two tests do not establish that the default evaluator rejects a regression. [Factory test][factory-test] · [Lifecycle test][meter-test] · [Test fixture][meter-fixture]

## 8. Selected reporting tools: inputs are not test execution

The scripts README defines these Java sources as source-code programs with no external dependencies beyond the JDK. Several use modern source-program forms. They are separate from the exported OSGi testing packages and are not root reactor modules merely because they end in `.java`. [Scripts README][scripts-readme]

### `BuildDropDataGenerator`

The actual required JVM property is `dropDirectory`, resolved through `toRealPath()`; the leading comment's shorter `directory` spelling is not the implemented lookup. The first argument selects `mainEclipse`, `mainEquinox` or `buildLogs`; unknown modes throw `IllegalArgumentException`. Main Eclipse mode also reads `gitBaselineTag` and `gitReposChanged`. Missing required properties fail through `OS.readProperty`. [Drop generator][drop-generator] · [OS utility][os-util]

Main modes consume `buildproperties.properties`, scan drop files, classify expected artifact filename families and produce `buildproperties.json` plus `<client>-<buildId>-checksums`. `buildLogs` scans `buildlogs` and writes `buildlogs/logs.json`. SHA-512 values are computed from file contents; these are integrity hashes, not signing or provenance verification. Timestamp parsing requires `[A-Z]yyyyMMdd-HHmm` and uses UTC. The preceding-release label helper rejects a zero minor version. Required named artifacts are looked up directly, so incomplete staging can fail rather than emit a friendly missing-artifact record. [Drop generator][drop-generator]

`OS.listFileTree` closes its walk stream, returns relative paths mapped to size/hash records and wraps per-file I/O failures as `UncheckedIOException`. Hashing reads 8192-byte blocks and uses a thread-local digest in that caller. The public hash helper accepts a caller-supplied digest, so the caller controls its state/ownership; this helper should not be described as validating trust. [OS utility][os-util]

### `CompilerSummaryGenerator`

The generator reads `${dropDirectory}/compilelogs`, walks regular `.xml` files and writes `compilelogs/logs.json`. It counts `WARNING`, `INFO` and task counts, omitting all-zero entries and sorting paths. Duplicate paths trigger `IllegalStateException`. Crucially, its switch does not count `ERROR` severity, so an empty summary does not prove compilation was error-free. Parser/filesystem exceptions can propagate out of the entry point. [Compiler summary][compiler-generator]

### `TestResultsGenerator`

Required properties are `testManifestFile`, `xmlDirectory` and comma-separated `testsConfigExpected`. It expands configuration names into expected OS/window-system/architecture/Java filename suffixes, reads matching XML files in the immediate directory, and totals each `testsuite` element's `errors` plus `failures`. It records suites and writes sibling `<shortConfig>-summary.json` files. Filename/configuration formats are structural inputs; unsupported OS names throw `IllegalArgumentException`. [Test-results generator][test-generator]

The per-file negative error codes are `-1` missing, `-2` empty, `-3` no `testsuite`, `-4` I/O failure, `-5` SAX failure and `-6` parser-configuration failure. These must not be treated as zero successes. Missing expected logs are warnings, and newly discovered tests absent from the manifest produce `addToTestManifest.xml`. That file is a generated suggestion, not an automatic edit of the authoritative manifest. [Test-results generator][test-generator]

Expected per-test logs are expanded only across configurations where some result files were found; an entirely absent configuration produces a warning. The generator does not run tests and does not universally convert missing coverage into a failing process exit. Review its warnings and input coverage alongside the JSON rather than equating a report file's existence with a complete test pass. [Test-results generator][test-generator]

### Shared XML/JSON utilities

`XmlProcessorFactoryRelEng` disables external-general and external-parameter entities, installs an empty entity resolver and uses a synchronized parse method around a shared factory. Each call creates a builder and parses the supplied file; checked parser/I/O/SAX failures remain visible. This implementation avoids remote DTD retrieval without claiming that every XML construct is rejected. [XML utility][xml-util]

`utilities.JSON` explicitly describes itself as an incomplete write-only helper. Objects preserve insertion order; `add` throws for duplicate non-null entries, after the map replacement has occurred. Arrays copy the incoming list into a mutable list. String values and object keys are printed without general JSON escaping, so callers cannot treat it as a safe serializer for arbitrary text containing quotes, backslashes or control characters. File output is direct, not a transactional temporary-file replacement. These limitations apply to this internal writer, not to every JSON library used by Eclipse. [JSON utility][json-util]

## 9. Selected documentation-tips implementation

`HtmlTableTipProvider` reads `tips/platform_tips.html` from the installed `org.eclipse.platform.doc.user` bundle using a UTF-8 reader, closes that reader, converts rows through `HtmlExtractor`, and replaces its tip list. `IOException` becomes an error `IStatus`; missing bundle/entry assumptions are not comprehensively guarded as ordinary status failures. Its icon is cached lazily; no synchronization or substantive disposal implementation is provided here. The containing manifest does not export this package, despite the classes being public Java types. [Provider][tip-provider] · [Tips manifest][tips-manifest]

`HtmlExtractor` parses table rows, treats first/last `td` cells as subject/content, creates tips with a fixed 27 June 2018 date used for stable read-state identity, and replaces image references with bundle-resource base64 data. No rows yields an empty list. Rows without expected cells, malformed `PLUGINS_ROOT` references or missing bundles are outside its guarded happy path; a missing image entry is logged as a warning. This is packaged-document transformation, not a general HTML sanitizer or web crawler. [Extractor][tip-extractor]

## 10. Release tests and evidence boundaries

`org.eclipse.releng.tests` sets `skipTests=true` in its pomless properties. Its `BuildTests` methods additionally call `assumeFalse(isMavenRun())`, with Maven detected by `MAVEN_CMD_LINE_ARGS`. These checks inspect installed feature/plugin metadata, product versions, Javadoc logs and published signing/comparator reports. Some are network-dependent and require properties such as `buildId`; they are not ordinary isolated unit tests. [Releng-test properties][releng-test-build] · [BuildTests][build-tests]

The checked-in Jenkins pipeline builds a local ECJ version, then invokes parallel `verify` with `bree-libs`, `skipTests=true` and baseline-version comparison enabled. It separately deploys parent/target artifacts on selected branches and deploys bootstrap scripts under further conditions. This source establishes what that pipeline requests, not that this PR has a green run or that every nightly/release job is described by this one file. [Jenkinsfile][jenkins]

The `.m3/atom-pattern/pom.xml` declares a separate `com.synexia.verification:m3-hierarchy-recipe:0.1.0-hierarchy1` dependency and an exec entry point. It has no parent edge reparenting the Eclipse build and is absent from the root reactor list. Its README explicitly separates intake receipts from compilation, tests, UI parity and semantic-equivalence gates. No claim of applied M3 runtime optimization, completed absorption, JNI admission or passing SDK evaluation follows from the overlay's presence. [Overlay POM][m3-pom] · [Overlay README][m3-readme] · [Root reactor][root-pom]

For future validation, keep separate records for dependency resolution, packaging outputs, tests actually executed, skipped tests, native/UI execution, report generation and release publication. A successful skipped-test packaging build, generated API metadata, a populated download JSON file and a runtime correctness result answer different questions. This guide supplies the source map for those distinctions; every execution status in this review remains **NOT RUN**.

<!-- All repository-file references below are pinned to the inspected PR head. -->

[revision]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/commit/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c
[readme]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/README.md
[license]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/LICENSE
[notice]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/NOTICE
[root-pom]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/pom.xml
[parent-pom]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse-platform-parent/pom.xml
[prereqs-pom]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng.prereqs.sdk/pom.xml
[common-pom]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.common/pom.xml
[releng-pom]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/pom.xml
[products-pom]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products/pom.xml
[sites-pom]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/sites/pom.xml
[scripts-readme]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/scripts/README.md
[jenkins]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/Jenkinsfile
[test-assembly]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/sites/eclipse-junit-tests/src/main/assembly/assembly.xml
[tree]: https://api.github.com/repos/hsoliwal/eclipse.platform.releng.aggregator/git/trees/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c?recursive=1
[gitmodules]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/.gitmodules
[mvn-extension]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/.mvn/extensions.xml
[mvn-config]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/.mvn/maven.config
[parent-properties]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse-platform-parent/pom.xml#L24-L139
[parent-build]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse-platform-parent/pom.xml#L182-L330
[parent-managed]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse-platform-parent/pom.xml#L331-L891
[parent-target]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse-platform-parent/pom.xml#L190-L251
[prereqs-target]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng.prereqs.sdk/eclipse-sdk-prereqs.target
[parent-profiles]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse-platform-parent/pom.xml#L892-L1250
[parent-reports]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse-platform-parent/pom.xml#L505-L584
[perf-manifest]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test.performance/META-INF/MANIFEST.MF
[test-manifest]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test/META-INF/MANIFEST.MF
[tips-manifest]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.common/bundles/org.eclipse.platform.doc.tips/META-INF/MANIFEST.MF
[platform-product]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products/eclipse-platform/platform.product
[sdk-product]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products/eclipse-sdk/sdk.product
[launcher-product]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products/equinox-launcher/equinox-sdk.product
[starter-product]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products/equinox-starterkit/EclipseRTOSGiStarterKit.product
[product-properties]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products/eclipse-sdk/build.properties
[platform-properties]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products/eclipse-platform/build.properties
[launcher-properties]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products/equinox-launcher/build.properties
[starter-properties]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products/equinox-starterkit/build.properties
[products-signing]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products/pom.xml#L97-L203
[platform-category]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/sites/eclipse-platform-repository/category.xml
[equinox-category]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/sites/equinox-sdk-repository/category.xml
[site-properties]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/sites/eclipse-platform-repository/build.properties
[equinox-site-properties]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/sites/equinox-sdk-repository/build.properties
[test-site-pom]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/sites/eclipse-junit-tests/pom.xml
[drop-generator]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/scripts/releng/BuildDropDataGenerator.java
[platform-doc-pom]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.common/bundles/org.eclipse.platform.doc.isv/pom.xml
[jdt-doc-pom]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.common/bundles/org.eclipse.jdt.doc.isv/pom.xml
[test-build]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test/build.properties
[test-runner]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test/src/org/eclipse/test/EclipseTestRunner.java
[classloader]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test/src/org/eclipse/test/ClassLoaderTools.java
[core-app]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test/src/org/eclipse/test/CoreTestApplication.java
[ui-app]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test/src/org/eclipse/test/UITestApplication.java
[screenshots]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test/src/org/eclipse/test/Screenshots.java
[awt-screenshot]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test/src/org/eclipse/test/AwtScreenshot.java
[performance]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test.performance/src/org/eclipse/test/performance/Performance.java
[meter-api]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test.performance/src/org/eclipse/test/performance/PerformanceMeter.java
[perf-junit5]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test.performance/src/org/eclipse/test/performance/PerformanceTestCaseJunit5.java
[perf-base]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test.performance/src/org/eclipse/test/performance/AbstractPerformanceTestCase.java
[meter-factory]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test.performance/src/org/eclipse/test/internal/performance/PerformanceMeterFactory.java
[internal-meter]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test.performance/src/org/eclipse/test/internal/performance/InternalPerformanceMeter.java
[os-meter]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test.performance/src/org/eclipse/test/internal/performance/OSPerformanceMeter.java
[system-meter]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test.performance/src/org/eclipse/test/internal/performance/SystemTimePerformanceMeter.java
[linux-monitor]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test.performance/src/org/eclipse/test/internal/performance/PerformanceMonitorLinux.java
[windows-monitor]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test.performance/src/org/eclipse/test/internal/performance/PerformanceMonitorWindows.java
[mac-monitor]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test.performance/src/org/eclipse/test/internal/performance/PerformanceMonitorMac.java
[evaluator]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test.performance/src/org/eclipse/test/internal/performance/eval/Evaluator.java
[factory-test]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test.performance/src/org/eclipse/test/internal/performance/tests/PerformanceMeterFactoryTest.java
[meter-test]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test.performance/src/org/eclipse/test/internal/performance/tests/SimplePerformanceMeterTest.java
[meter-fixture]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.test.performance/src/org/eclipse/test/internal/performance/tests/TestPerformanceMeter.java
[os-util]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/scripts/releng/utilities/OS.java
[compiler-generator]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/scripts/releng/CompilerSummaryGenerator.java
[test-generator]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/scripts/releng/TestResultsGenerator.java
[xml-util]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/scripts/releng/utilities/XmlProcessorFactoryRelEng.java
[json-util]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/scripts/releng/utilities/JSON.java
[tip-provider]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.common/bundles/org.eclipse.platform.doc.tips/src/org/eclipse/platform/doc/tips/HtmlTableTipProvider.java
[tip-extractor]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.common/bundles/org.eclipse.platform.doc.tips/src/org/eclipse/platform/doc/tips/HtmlExtractor.java
[releng-test-build]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.releng.tests/build.properties
[build-tests]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/bundles/org.eclipse.releng.tests/src/org/eclipse/releng/tests/BuildTests.java
[m3-pom]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/.m3/atom-pattern/pom.xml
[m3-readme]: https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/.m3/atom-pattern/README.md
