#!/usr/bin/env bash
# Copyright (c) 2026 Synexia, Hitesh Soliwal (hsoliwal@gmail.com) and others.
# SPDX-License-Identifier: Apache-2.0 OR EPL-2.0
#
# Java-level census of one aggregator submodule at its gitlink commit, without a full clone: depth-1 blobless fetch
# of the commit, sparse checkout of the metadata files only (one batched blob fetch), then grep.
# Usage: sub_bree.sh <name> <url> <sha>   -> rows: name TAB kind TAB path TAB match   (kind: bree22|pin22)
set -euo pipefail
N="$1"; U="$2"; S="$3"; D=F:/m3-scratch/rel21/sub/$N; export TEMP=F:/m3-scratch/tmp TMP=F:/m3-scratch/tmp
if [ ! -d "$D/.git" ]; then
	git init -q "$D"; git -C "$D" config core.longpaths true; git -C "$D" remote add origin "$U"
fi
git -C "$D" fetch -q --depth 1 --filter=blob:none --no-tags origin "$S"
git -C "$D" sparse-checkout set --no-cone '*/META-INF/MANIFEST.MF' '*pom.xml' '*.product' '*.classpath' '*org.eclipse.jdt.core.prefs' '*build.properties' >/dev/null
git -C "$D" -c advice.detachedHead=false checkout -q "$S"
{ git -C "$D" grep -n -P 'Bundle-RequiredExecutionEnvironment:.*JavaSE-2[2-9]' -- '*MANIFEST.MF' | sed "s|^|$N\tbree22\t|" || true
  git -C "$D" grep -n -P '<(maven\.compiler\.(release|source|target)|release)>2[2-9]<|<executionEnvironment>JavaSE-2[2-9]<|requiredJavaVersion=2[2-9]|jre\.compilation\.profile\s*=\s*JavaSE-2[2-9]' \
	-- '*pom.xml' '*.product' '*build.properties' | sed "s|^|$N\tpin22\t|" || true
} | tr -d '\r'
echo "$N $S manifests=$(git -C "$D" ls-files -- '*META-INF/MANIFEST.MF' | wc -l)" >&2
