#!/usr/bin/env bash
# Copyright (c) 2026 Synexia, Hitesh Soliwal (hsoliwal@gmail.com) and others.
# SPDX-License-Identifier: Apache-2.0 OR EPL-2.0
#
# G6: Eclipse SDK product build of hsoliwal/eclipse.platform.releng.aggregator at a given commit, on JDK 21, in one new
# directory: an NTFS VHDX inside the user-approved I:/m3-sdk-build-20261110 (I: is exFAT, 1 MB clusters), mounted at
# F:/m3-scratch/rel21/sdkmnt; local Maven repository shared with G5 (F:/m3-scratch/m2-eclipse).
#   stage clone  : depth-1 clone of the aggregator + every submodule at its pointer (SHA fetch)
#   stage check  : ECJ NLS / unused-import pre-check of every component (rows are reported, sources are not touched)
#   stage build  : mvn -B clean verify -DskipTests -fae (Maven Central first), Tycho localArtifacts ignored
# Usage: g6_sdk.sh <stage> <aggregator-sha>   logs in $D/logs; nothing written outside $D and the shared Maven repository
set -uo pipefail
STAGE="$1"; SHA="$2"; D=Z:; A=$D/a; L=$D/logs; M2=F:/m3-scratch/m2-eclipse; T=F:/m3-scratch/rel21/tools
mkdir -p "$D/tmp" "$L" "$D/home"
export TEMP=$D/tmp TMP=$D/tmp JAVA_HOME="C:/Program Files/Java/jdk-21"
export PATH="$(cygpath -u "$JAVA_HOME")/bin:$PATH" MAVEN_OPTS="-Xmx6g -Djava.io.tmpdir=$D/tmp -Duser.home=$D/home"
MVN=C:/ProgramData/chocolatey/lib/maven/apache-maven-3.9.14/bin/mvn
case "$STAGE" in
clone)
	git -c core.longpaths=true -c core.autocrlf=false clone -q --depth 1 --branch master \
		https://github.com/hsoliwal/eclipse.platform.releng.aggregator.git "$A" 2>&1 | tail -2
	git -C "$A" config core.longpaths true; git -C "$A" config core.autocrlf false
	[ "$(git -C "$A" rev-parse HEAD)" = "$SHA" ] || { echo "aggregator HEAD $(git -C "$A" rev-parse HEAD) != $SHA"; exit 1; }
	git -C "$A" -c core.longpaths=true -c core.autocrlf=false submodule update --init --depth 1 --jobs 4 2>&1 | grep -v -E 'Updating files|Receiving|Resolving' | tail -15
	git -C "$A" submodule status | tee "$L/submodules.txt"
	for s in $(git -C "$A" submodule status | awk '{print $2}'); do git -C "$A/$s" config core.longpaths true; done
	echo "checkout: $(git -C "$A" ls-files | wc -l) aggregator files" ;;
check)
	for s in eclipse.platform.swt eclipse.pde equinox.p2 eclipse.platform eclipse.platform.ui equinox eclipse.jdt.ui eclipse.jdt.core eclipse.jdt.debug; do
		bash "$T/ecj_precheck.sh" "$A/$s" "$L/ecj.$s" 2>&1 | tail -1; done ;;
build)
	t0=$(date +%s); echo "$(date +%T) build start ($(java -version 2>&1 | head -1))"
	( cd "$A" && "$MVN" -B -s "$T/settings-central-first.xml" clean verify -DskipTests -fae -nsu -Dtycho.localArtifacts=ignore \
		-Dmaven.repo.local="$M2" -Djava.io.tmpdir="$D/tmp" ${G6_EXTRA:-} ) > "$L/build.log" 2>&1
	rc=$?; st=$(grep -a -o -E 'BUILD (SUCCESS|FAILURE)' "$L/build.log" | tail -1)
	ok=$(grep -a -c -E '^\[INFO\] .* SUCCESS \[' "$L/build.log"); bad=$(grep -a -c -E '^\[INFO\] .* FAILURE \[' "$L/build.log")
	sk=$(grep -a -c -E '^\[INFO\] .* SKIPPED' "$L/build.log")
	printf 'aggregator\tstatus\trc\tseconds\tsuccess\tfailure\tskipped\n%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$SHA" "${st:-NO_RESULT}" "$rc" \
		"$(( $(date +%s) - t0 ))" "$ok" "$bad" "$sk" | tee "$L/build.result.tsv"
	grep -a -E '^\[ERROR\]' "$L/build.log" | awk '!seen[$0]++' > "$L/build.errors.txt" ;;
esac
