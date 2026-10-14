# Source reference: eclipse.platform.releng.aggregator

> Inspected source revision: `55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c`. Source/manifest observation only; builds and tests were not run.

This reference separates repository ownership, Eclipse workspace projects, Maven aggregation, OSGi bundles, features and Java source namespaces. The linked inventories account for the pinned tracked tree without treating every descriptor as an active product module. Names and imports establish structure; [selected contracts](CONTRACTS.md) explain inspected behavior.

## Start here

- [Build, ownership and selected API/lifecycle contracts](CONTRACTS.md)
- [Coverage, method and verification gaps](COVERAGE.md)
- [Other language surfaces and Java files without recognized package declarations](OTHER-SOURCES.md)
- [Repository introduction](../../README.md), [LICENSE](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/LICENSE) and [NOTICE](https://github.com/hsoliwal/eclipse.platform.releng.aggregator/blob/55bf9d0a12bb2b80c5e79d7382e7d9b04d074c3c/NOTICE)

## Every metadata-backed project/module path

- [`.`](projects-01.md#u0001)
- [`.m3/atom-pattern`](projects-01.md#u0002)
- [`eclipse-platform-parent`](projects-01.md#u0003)
- [`eclipse.jdt`](projects-01.md#u0004)
- [`eclipse.jdt.core`](projects-01.md#u0005)
- [`eclipse.jdt.core.binaries`](projects-01.md#u0006)
- [`eclipse.jdt.debug`](projects-01.md#u0007)
- [`eclipse.jdt.ui`](projects-01.md#u0008)
- [`eclipse.pde`](projects-01.md#u0009)
- [`eclipse.platform`](projects-01.md#u0010)
- [`eclipse.platform.common`](projects-01.md#u0011)
- [`eclipse.platform.common/bundles/org.eclipse.jdt.doc.isv`](projects-01.md#u0012)
- [`eclipse.platform.common/bundles/org.eclipse.jdt.doc.user`](projects-01.md#u0013)
- [`eclipse.platform.common/bundles/org.eclipse.jdt.tips.user`](projects-01.md#u0014)
- [`eclipse.platform.common/bundles/org.eclipse.platform.doc.isv`](projects-01.md#u0015)
- [`eclipse.platform.common/bundles/org.eclipse.platform.doc.tips`](projects-01.md#u0016)
- [`eclipse.platform.common/bundles/org.eclipse.platform.doc.user`](projects-01.md#u0017)
- [`eclipse.platform.releng`](projects-01.md#u0018)
- [`eclipse.platform.releng.prereqs.sdk`](projects-01.md#u0019)
- [`eclipse.platform.releng/bundles`](projects-01.md#u0020)
- [`eclipse.platform.releng/bundles/org.eclipse.rcp`](projects-01.md#u0021)
- [`eclipse.platform.releng/bundles/org.eclipse.releng.tests`](projects-01.md#u0022)
- [`eclipse.platform.releng/bundles/org.eclipse.sdk.examples`](projects-01.md#u0023)
- [`eclipse.platform.releng/bundles/org.eclipse.sdk.tests`](projects-01.md#u0024)
- [`eclipse.platform.releng/bundles/org.eclipse.test`](projects-01.md#u0025)
- [`eclipse.platform.releng/bundles/org.eclipse.test.performance`](projects-01.md#u0026)
- [`eclipse.platform.releng/bundles/org.eclipse.test.performance.win32`](projects-01.md#u0027)
- [`eclipse.platform.releng/deploy-to-maven`](projects-01.md#u0028)
- [`eclipse.platform.releng/features`](projects-01.md#u0029)
- [`eclipse.platform.releng/features/org.eclipse.platform-feature`](projects-01.md#u0030)
- [`eclipse.platform.releng/features/org.eclipse.rcp`](projects-02.md#u0031)
- [`eclipse.platform.releng/features/org.eclipse.sdk`](projects-02.md#u0032)
- [`eclipse.platform.releng/features/org.eclipse.sdk.examples-feature`](projects-02.md#u0033)
- [`eclipse.platform.releng/features/org.eclipse.test-feature`](projects-02.md#u0034)
- [`eclipse.platform.swt`](projects-02.md#u0035)
- [`eclipse.platform.ui`](projects-02.md#u0036)
- [`equinox`](projects-02.md#u0037)
- [`equinox.p2`](projects-02.md#u0038)
- [`oomph`](projects-02.md#u0039)
- [`products`](projects-02.md#u0040)
- [`products/eclipse-platform`](projects-02.md#u0041)
- [`products/eclipse-sdk`](projects-02.md#u0042)
- [`products/equinox-launcher`](projects-02.md#u0043)
- [`products/equinox-starterkit`](projects-02.md#u0044)
- [`scripts`](projects-02.md#u0045)
- [`sites`](projects-02.md#u0046)
- [`sites/eclipse-junit-tests`](projects-02.md#u0047)
- [`sites/eclipse-platform-repository`](projects-02.md#u0048)
- [`sites/equinox-sdk-repository`](projects-02.md#u0049)

## Recognized named Java namespaces in the read source set

- [`org.eclipse.jdt.tips.user.internal`](packages-01.md#p0001)
- [`org.eclipse.perfmsr.core`](packages-01.md#p0002)
- [`org.eclipse.platform.doc.tips`](packages-01.md#p0003)
- [`org.eclipse.releng.tests`](packages-01.md#p0004)
- [`org.eclipse.test`](packages-01.md#p0005)
- [`org.eclipse.test.internal.performance`](packages-01.md#p0006)
- [`org.eclipse.test.internal.performance.data`](packages-01.md#p0007)
- [`org.eclipse.test.internal.performance.db`](packages-01.md#p0008)
- [`org.eclipse.test.internal.performance.eval`](packages-01.md#p0009)
- [`org.eclipse.test.internal.performance.tests`](packages-01.md#p0010)
- [`org.eclipse.test.performance`](packages-01.md#p0011)
- [`utilities`](packages-01.md#p0012)

## Every Java-bearing source directory

- [Source-directory records 1–13](source-directories-01.md)
