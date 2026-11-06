# Project/module records 2

> Inspected source revision: `55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c`. Source/manifest observation only; builds and tests were not run.

[Reference home](README.md) · [Selected contracts](CONTRACTS.md) · [Coverage](COVERAGE.md)

## U0031

### `eclipse.platform.releng/features/org.eclipse.rcp`

- Source: [eclipse.platform.releng/features/org.eclipse.rcp](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/tree/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/features/org.eclipse.rcp); implementation/build; activation must be checked below
- Discovery evidence: [.project](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/features/org.eclipse.rcp/.project), [feature.xml](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/features/org.eclipse.rcp/feature.xml)
- Reactor reachability: outside parsed non-profile module reachability; retained in scope
- Eclipse workspace identity: `org.eclipse.rcp (feature)`; natures: `org.eclipse.pde.FeatureNature`
- Distribution feature: `org.eclipse.rcp`; included plug-ins `org.eclipse.help`, `org.eclipse.ui`, `org.eclipse.ui.workbench`, `org.eclipse.update.configurator`, `org.eclipse.rcp`, `org.eclipse.ui.cocoa`; included features `org.eclipse.e4.rcp`
- Packaging/source configuration: [eclipse.platform.releng/features/org.eclipse.rcp/build.properties](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/features/org.eclipse.rcp/build.properties); observed property starts `bin.includes=feature.xml,feature.properties`. Continued values require reading the linked file
- No named Java declaration from the read source set is assigned to this metadata path by nearest-owner accounting; this does not make feature/product/resource content empty
- Semantic status: metadata accounted; behavior is specified only where [selected contracts](CONTRACTS.md) names an inspected implementation. A bundle name, export or lifecycle header alone does not prove API stability, thread safety or successful activation

## U0032

### `eclipse.platform.releng/features/org.eclipse.sdk`

- Source: [eclipse.platform.releng/features/org.eclipse.sdk](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/tree/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/features/org.eclipse.sdk); implementation/build; activation must be checked below
- Discovery evidence: [.project](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/features/org.eclipse.sdk/.project), [feature.xml](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/features/org.eclipse.sdk/feature.xml)
- Reactor reachability: outside parsed non-profile module reachability; retained in scope
- Eclipse workspace identity: `org.eclipse.sdk (feature)`; natures: `org.eclipse.pde.FeatureNature`
- Distribution feature: `org.eclipse.sdk`; included plug-ins `org.eclipse.sdk`, `org.eclipse.jdt.doc.isv`, `org.eclipse.platform.doc.isv`; included features `org.eclipse.platform`, `org.eclipse.jdt`, `org.eclipse.pde`, `org.eclipse.pde.spies`, `org.eclipse.help`, `org.eclipse.jdt.astview.feature`, `org.eclipse.jdt.jeview.feature`, `org.eclipse.jdt.bcoview.feature`
- Packaging/source configuration: [eclipse.platform.releng/features/org.eclipse.sdk/build.properties](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/features/org.eclipse.sdk/build.properties); observed property starts `bin.includes=feature.xml,feature.properties`. Continued values require reading the linked file
- No named Java declaration from the read source set is assigned to this metadata path by nearest-owner accounting; this does not make feature/product/resource content empty
- Semantic status: metadata accounted; behavior is specified only where [selected contracts](CONTRACTS.md) names an inspected implementation. A bundle name, export or lifecycle header alone does not prove API stability, thread safety or successful activation

## U0033

### `eclipse.platform.releng/features/org.eclipse.sdk.examples-feature`

- Source: [eclipse.platform.releng/features/org.eclipse.sdk.examples-feature](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/tree/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/features/org.eclipse.sdk.examples-feature); example/template (path classification)
- Discovery evidence: [.project](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/features/org.eclipse.sdk.examples-feature/.project), [feature.xml](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/features/org.eclipse.sdk.examples-feature/feature.xml)
- Reactor reachability: outside parsed non-profile module reachability; retained in scope
- Eclipse workspace identity: `org.eclipse.sdk.examples-feature`; natures: `org.eclipse.pde.FeatureNature`
- Distribution feature: `org.eclipse.sdk.examples`; included plug-ins `org.eclipse.compare.examples`, `org.eclipse.compare.examples.xml`, `org.eclipse.debug.examples.core`, `org.eclipse.debug.examples.ui`, `org.eclipse.jface.examples.databinding`, `org.eclipse.swt.examples`, `org.eclipse.swt.examples.views`, `org.eclipse.swt.examples.browser.demos`, `org.eclipse.swt.examples.launcher`, `org.eclipse.ui.examples.javaeditor`, `org.eclipse.ui.examples.multipageeditor`, `org.eclipse.ui.examples.propertysheet`, `org.eclipse.ui.examples.readmetool`, `org.eclipse.ui.examples.contributions`, `org.eclipse.ui.examples.undo`, `org.eclipse.ui.examples.views.properties.tabbed.article`, `org.eclipse.ui.examples.fieldassist`, `org.eclipse.ui.examples.filesystem`, `org.eclipse.team.examples.filesystem`, `org.eclipse.swt.examples.ole.win32`, `org.eclipse.sdk.examples`, `org.eclipse.ui.genericeditor.examples`, `org.eclipse.ui.examples.uriSchemeHandler`; included features none declared
- Packaging/source configuration: [eclipse.platform.releng/features/org.eclipse.sdk.examples-feature/build.properties](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/features/org.eclipse.sdk.examples-feature/build.properties); observed property starts `bin.includes = feature.xml,\`. Continued values require reading the linked file
- No named Java declaration from the read source set is assigned to this metadata path by nearest-owner accounting; this does not make feature/product/resource content empty
- Semantic status: metadata accounted; behavior is specified only where [selected contracts](CONTRACTS.md) names an inspected implementation. A bundle name, export or lifecycle header alone does not prove API stability, thread safety or successful activation

## U0034

### `eclipse.platform.releng/features/org.eclipse.test-feature`

- Source: [eclipse.platform.releng/features/org.eclipse.test-feature](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/tree/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/features/org.eclipse.test-feature); test or test fixture (path classification)
- Discovery evidence: [.project](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/features/org.eclipse.test-feature/.project), [feature.xml](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/features/org.eclipse.test-feature/feature.xml)
- Reactor reachability: outside parsed non-profile module reachability; retained in scope
- Eclipse workspace identity: `org.eclipse.test-feature`; natures: `org.eclipse.pde.FeatureNature`
- Distribution feature: `org.eclipse.test`; included plug-ins `org.eclipse.test`, `org.eclipse.test.performance`, `org.eclipse.test.performance.win32`, `org.eclipse.core.tests.harness`, `org.eclipse.ui.tests.harness`; included features none declared
- Packaging/source configuration: [eclipse.platform.releng/features/org.eclipse.test-feature/build.properties](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.releng/features/org.eclipse.test-feature/build.properties); observed property starts `bin.includes =\`. Continued values require reading the linked file
- No named Java declaration from the read source set is assigned to this metadata path by nearest-owner accounting; this does not make feature/product/resource content empty
- Semantic status: metadata accounted; behavior is specified only where [selected contracts](CONTRACTS.md) names an inspected implementation. A bundle name, export or lifecycle header alone does not prove API stability, thread safety or successful activation

## U0035

### `eclipse.platform.swt`

- Source: [eclipse.platform.swt](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.swt); implementation/build; activation must be checked below
- Discovery evidence: parent module declaration; no local descriptor
- Reactor reachability: reachable through parsed non-profile module declarations
- Boundary: gitlink at `6e0937b7db830bd1491ee4711497cf1ac8be1270`; child contents and inherited effective model are not part of this tree inventory
- No named Java declaration from the read source set is assigned to this metadata path by nearest-owner accounting; this does not make feature/product/resource content empty
- Semantic status: metadata accounted; behavior is specified only where [selected contracts](CONTRACTS.md) names an inspected implementation. A bundle name, export or lifecycle header alone does not prove API stability, thread safety or successful activation

## U0036

### `eclipse.platform.ui`

- Source: [eclipse.platform.ui](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/eclipse.platform.ui); implementation/build; activation must be checked below
- Discovery evidence: parent module declaration; no local descriptor
- Reactor reachability: reachable through parsed non-profile module declarations
- Boundary: gitlink at `e71f29b260dd0ace91ee9b7e9d95dfa3fc99accf`; child contents and inherited effective model are not part of this tree inventory
- No named Java declaration from the read source set is assigned to this metadata path by nearest-owner accounting; this does not make feature/product/resource content empty
- Semantic status: metadata accounted; behavior is specified only where [selected contracts](CONTRACTS.md) names an inspected implementation. A bundle name, export or lifecycle header alone does not prove API stability, thread safety or successful activation

## U0037

### `equinox`

- Source: [equinox](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/equinox); implementation/build; activation must be checked below
- Discovery evidence: parent module declaration; no local descriptor
- Reactor reachability: reachable through parsed non-profile module declarations
- Boundary: gitlink at `66584d130d22951aac8f42079948fe3c757d64ca`; child contents and inherited effective model are not part of this tree inventory
- No named Java declaration from the read source set is assigned to this metadata path by nearest-owner accounting; this does not make feature/product/resource content empty
- Semantic status: metadata accounted; behavior is specified only where [selected contracts](CONTRACTS.md) names an inspected implementation. A bundle name, export or lifecycle header alone does not prove API stability, thread safety or successful activation

## U0038

### `equinox.p2`

- Source: [equinox.p2](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/equinox.p2); implementation/build; activation must be checked below
- Discovery evidence: parent module declaration; no local descriptor
- Reactor reachability: reachable through parsed non-profile module declarations
- Boundary: gitlink at `bc7e3d0756a893e3865b0ed00ba8f9448d9cbbc1`; child contents and inherited effective model are not part of this tree inventory
- No named Java declaration from the read source set is assigned to this metadata path by nearest-owner accounting; this does not make feature/product/resource content empty
- Semantic status: metadata accounted; behavior is specified only where [selected contracts](CONTRACTS.md) names an inspected implementation. A bundle name, export or lifecycle header alone does not prove API stability, thread safety or successful activation

## U0039

### `oomph`

- Source: [oomph](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/tree/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/oomph); implementation/build; activation must be checked below
- Discovery evidence: [.project](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/oomph/.project)
- Reactor reachability: outside parsed non-profile module reachability; retained in scope
- Eclipse workspace identity: `org.eclipse.platform.sdk.setup`; natures: 
- No named Java declaration from the read source set is assigned to this metadata path by nearest-owner accounting; this does not make feature/product/resource content empty
- Semantic status: metadata accounted; behavior is specified only where [selected contracts](CONTRACTS.md) names an inspected implementation. A bundle name, export or lifecycle header alone does not prove API stability, thread safety or successful activation

## U0040

### `products`

- Source: [products](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/tree/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products); implementation/build; activation must be checked below
- Discovery evidence: [.project](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products/.project), [pom.xml](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products/pom.xml)
- Reactor reachability: reachable through parsed non-profile module declarations
- Eclipse workspace identity: `eclipse.platform.releng.products`; natures: 
- Declared Maven coordinates: `org.eclipse:products:4.42.0-SNAPSHOT`; packaging `pom`; parent `org.eclipse:eclipse-platform-parent:4.42.0-SNAPSHOT`, relative path `../eclipse-platform-parent`
- Aggregates: [`products/eclipse-platform`](projects-02.md#u0041) (non-profile declaration), [`products/eclipse-sdk`](projects-02.md#u0042) (non-profile declaration), [`products/equinox-launcher`](projects-02.md#u0043) (non-profile declaration), [`products/equinox-starterkit`](projects-02.md#u0044) (non-profile declaration)
- No named Java declaration from the read source set is assigned to this metadata path by nearest-owner accounting; this does not make feature/product/resource content empty
- Semantic status: metadata accounted; behavior is specified only where [selected contracts](CONTRACTS.md) names an inspected implementation. A bundle name, export or lifecycle header alone does not prove API stability, thread safety or successful activation

## U0041

### `products/eclipse-platform`

- Source: [products/eclipse-platform](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/tree/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products/eclipse-platform); implementation/build; activation must be checked below
- Discovery evidence: parent module declaration; no local descriptor
- Reactor reachability: reachable through parsed non-profile module declarations
- Packaging/source configuration: [products/eclipse-platform/build.properties](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products/eclipse-platform/build.properties); observed property starts `pom.model.property.product.id = org.eclipse.platform.ide`; `pom.model.property.product.rootFolder = eclipse`; `pom.model.property.product.rootFolder.macosx = Eclipse.app`; `pom.model.property.repository.includeAllSources = true`; `pom.model.property.eclipse.signing.skip = false`. Continued values require reading the linked file
- No named Java declaration from the read source set is assigned to this metadata path by nearest-owner accounting; this does not make feature/product/resource content empty
- Semantic status: metadata accounted; behavior is specified only where [selected contracts](CONTRACTS.md) names an inspected implementation. A bundle name, export or lifecycle header alone does not prove API stability, thread safety or successful activation

## U0042

### `products/eclipse-sdk`

- Source: [products/eclipse-sdk](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/tree/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products/eclipse-sdk); implementation/build; activation must be checked below
- Discovery evidence: parent module declaration; no local descriptor
- Reactor reachability: reachable through parsed non-profile module declarations
- Packaging/source configuration: [products/eclipse-sdk/build.properties](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products/eclipse-sdk/build.properties); observed property starts `pom.model.property.product.id = org.eclipse.sdk.ide`; `pom.model.property.product.rootFolder = eclipse`; `pom.model.property.product.rootFolder.macosx = Eclipse.app`; `pom.model.property.repository.includeAllSources = true`; `pom.model.property.product.installSources = true`; `pom.model.property.eclipse.signing.skip = false`. Continued values require reading the linked file
- No named Java declaration from the read source set is assigned to this metadata path by nearest-owner accounting; this does not make feature/product/resource content empty
- Semantic status: metadata accounted; behavior is specified only where [selected contracts](CONTRACTS.md) names an inspected implementation. A bundle name, export or lifecycle header alone does not prove API stability, thread safety or successful activation

## U0043

### `products/equinox-launcher`

- Source: [products/equinox-launcher](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/tree/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products/equinox-launcher); implementation/build; activation must be checked below
- Discovery evidence: parent module declaration; no local descriptor
- Reactor reachability: reachable through parsed non-profile module declarations
- Packaging/source configuration: [products/equinox-launcher/build.properties](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products/equinox-launcher/build.properties); observed property starts `pom.model.property.product.id = equinox-launcher`; `pom.model.property.product.rootFolder = eclipse`; `pom.model.property.product.rootFolder.macosx = Eclipse.app`. Continued values require reading the linked file
- No named Java declaration from the read source set is assigned to this metadata path by nearest-owner accounting; this does not make feature/product/resource content empty
- Semantic status: metadata accounted; behavior is specified only where [selected contracts](CONTRACTS.md) names an inspected implementation. A bundle name, export or lifecycle header alone does not prove API stability, thread safety or successful activation

## U0044

### `products/equinox-starterkit`

- Source: [products/equinox-starterkit](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/tree/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products/equinox-starterkit); implementation/build; activation must be checked below
- Discovery evidence: parent module declaration; no local descriptor
- Reactor reachability: reachable through parsed non-profile module declarations
- Packaging/source configuration: [products/equinox-starterkit/build.properties](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/products/equinox-starterkit/build.properties); observed property starts `pom.model.property.product.id = org.eclipse.rt.osgistarterkit.product`; `pom.model.property.product.rootFolder = rt`; `pom.model.property.product.rootFolder.macosx = Rt.app`; `pom.model.property.eclipse.signing.skip = false`. Continued values require reading the linked file
- No named Java declaration from the read source set is assigned to this metadata path by nearest-owner accounting; this does not make feature/product/resource content empty
- Semantic status: metadata accounted; behavior is specified only where [selected contracts](CONTRACTS.md) names an inspected implementation. A bundle name, export or lifecycle header alone does not prove API stability, thread safety or successful activation

## U0045

### `scripts`

- Source: [scripts](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/tree/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/scripts); implementation/build; activation must be checked below
- Discovery evidence: [.project](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/scripts/.project)
- Reactor reachability: outside parsed non-profile module reachability; retained in scope
- Eclipse workspace identity: `eclipse.platform.releng.scripts`; natures: `org.eclipse.jdt.core.javanature`
- Owns declared Java namespaces: [`utilities`](packages-01.md#p0012)
- Semantic status: metadata accounted; behavior is specified only where [selected contracts](CONTRACTS.md) names an inspected implementation. A bundle name, export or lifecycle header alone does not prove API stability, thread safety or successful activation

## U0046

### `sites`

- Source: [sites](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/tree/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/sites); implementation/build; activation must be checked below
- Discovery evidence: [.project](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/sites/.project), [pom.xml](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/sites/pom.xml)
- Reactor reachability: reachable through parsed non-profile module declarations
- Eclipse workspace identity: `eclipse.platform.releng.sites`; natures: 
- Declared Maven coordinates: `org.eclipse:sites:4.42.0-SNAPSHOT`; packaging `pom`; parent `org.eclipse:eclipse-platform-parent:4.42.0-SNAPSHOT`, relative path `../eclipse-platform-parent`
- Aggregates: [`sites/eclipse-platform-repository`](projects-02.md#u0048) (non-profile declaration), [`sites/eclipse-junit-tests`](projects-02.md#u0047) (non-profile declaration), [`sites/equinox-sdk-repository`](projects-02.md#u0049) (non-profile declaration)
- No named Java declaration from the read source set is assigned to this metadata path by nearest-owner accounting; this does not make feature/product/resource content empty
- Semantic status: metadata accounted; behavior is specified only where [selected contracts](CONTRACTS.md) names an inspected implementation. A bundle name, export or lifecycle header alone does not prove API stability, thread safety or successful activation

## U0047

### `sites/eclipse-junit-tests`

- Source: [sites/eclipse-junit-tests](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/tree/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/sites/eclipse-junit-tests); implementation/build; activation must be checked below
- Discovery evidence: [pom.xml](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/sites/eclipse-junit-tests/pom.xml)
- Reactor reachability: reachable through parsed non-profile module declarations
- Declared Maven coordinates: `org.eclipse:eclipse-junit-tests:4.42.0-SNAPSHOT`; packaging `eclipse-repository`; parent `org.eclipse:sites:4.42.0-SNAPSHOT`, relative path `omitted; effective parent convention applies`
- No named Java declaration from the read source set is assigned to this metadata path by nearest-owner accounting; this does not make feature/product/resource content empty
- Semantic status: metadata accounted; behavior is specified only where [selected contracts](CONTRACTS.md) names an inspected implementation. A bundle name, export or lifecycle header alone does not prove API stability, thread safety or successful activation

## U0048

### `sites/eclipse-platform-repository`

- Source: [sites/eclipse-platform-repository](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/tree/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/sites/eclipse-platform-repository); implementation/build; activation must be checked below
- Discovery evidence: parent module declaration; no local descriptor
- Reactor reachability: reachable through parsed non-profile module declarations
- Packaging/source configuration: [sites/eclipse-platform-repository/build.properties](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/sites/eclipse-platform-repository/build.properties); observed property starts `pom.model.property.repository.name = Eclipse ${releaseVersion}`; `pom.model.property.repository.includeAllDependencies = true`; `pom.model.property.repository.includeAllSources = true`; `pom.model.property.eclipse.signing.skip = false`. Continued values require reading the linked file
- No named Java declaration from the read source set is assigned to this metadata path by nearest-owner accounting; this does not make feature/product/resource content empty
- Semantic status: metadata accounted; behavior is specified only where [selected contracts](CONTRACTS.md) names an inspected implementation. A bundle name, export or lifecycle header alone does not prove API stability, thread safety or successful activation

## U0049

### `sites/equinox-sdk-repository`

- Source: [sites/equinox-sdk-repository](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/tree/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/sites/equinox-sdk-repository); implementation/build; activation must be checked below
- Discovery evidence: parent module declaration; no local descriptor
- Reactor reachability: reachable through parsed non-profile module declarations
- Packaging/source configuration: [sites/equinox-sdk-repository/build.properties](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/sites/equinox-sdk-repository/build.properties); observed property starts `pom.model.property.repository.name = Equinox and Eclipse p2 ${releaseVersion}`; `pom.model.property.repository.includeAllDependencies = false`; `pom.model.property.repository.includeAllSources = true`; `pom.model.property.eclipse.signing.skip = false`. Continued values require reading the linked file
- No named Java declaration from the read source set is assigned to this metadata path by nearest-owner accounting; this does not make feature/product/resource content empty
- Semantic status: metadata accounted; behavior is specified only where [selected contracts](CONTRACTS.md) names an inspected implementation. A bundle name, export or lifecycle header alone does not prove API stability, thread safety or successful activation

