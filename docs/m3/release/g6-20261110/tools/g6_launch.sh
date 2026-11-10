#!/usr/bin/env bash
# Copyright (c) 2026 Synexia, Hitesh Soliwal (hsoliwal@gmail.com) and others.
# SPDX-License-Identifier: Apache-2.0 OR EPL-2.0
#
# G6 evidence after the SDK build: sha256 of every product archive, and two headless launches of the materialized
# win32.x86_64 SDK product on JDK 21 (configuration, workspace and user.home inside the build volume):
#   1. -application org.eclipse.equinox.p2.director -listInstalledRoots -profile SDKProfile
#   2. -version (launcher + framework), headless, bounded by a timeout
# Usage: g6_launch.sh <build-root>   (e.g. Z:)   -> <root>/logs/{products.sha256,launch-*.txt,eclipseproduct.txt,eclipse.ini}
set -uo pipefail
D="$1"; PROD="${2:-eclipse-sdk}"; A=$D/a; L=$D/logs; J="C:/Program Files/Java/jdk-21"
P=$A/products/$PROD/target/products
( cd "$A/products" && find . -path '*/target/products/*' -maxdepth 4 -type f \( -name '*.zip' -o -name '*.tar.gz' -o -name '*.dmg' \) -print0 \
	| xargs -0 sha256sum ) | tee "$L/products.sha256"
X=$(find "$P" -maxdepth 5 -type d -path '*win32/win32/x86_64*' | head -1)
[ -f "$X/eclipse/eclipsec.exe" ] && X="$X/eclipse"  # products with a root folder
[ -n "$X" ] && [ -f "$X/eclipsec.exe" ] || { echo "no materialized win32.x86_64 SDK product under $P"; ls -R "$P" | head -20; exit 1; }
echo "product dir: $X"
cp "$X/eclipse.ini" "$L/eclipse.ini"; cat "$X/.eclipseproduct" > "$L/eclipseproduct.txt" 2>/dev/null || true
mkdir -p "$D/launch/home"
# the product's own configuration area is kept (its config.ini names the p2 profile and data area); workspace and
# user.home stay inside the build volume
PROF=$(ls "$X/p2/org.eclipse.equinox.p2.engine/profileRegistry" 2>/dev/null | sed -n 's/\.profile$//p' | head -1)
cp "$X/configuration/config.ini" "$L/config.$PROD.ini" 2>/dev/null || true
COMMON=(-nosplash -consoleLog -vm "$J/bin/javaw.exe" -data "$D/launch/ws-$PROD")
VMA=(-vmargs "-Duser.home=$D/launch/home" -Djava.io.tmpdir=$D/tmp)
{ echo "\$ eclipsec ${COMMON[*]} -application org.eclipse.equinox.p2.director -listInstalledRoots -profile ${PROF:-SDKProfile}"; \
  timeout 600 "$X/eclipsec.exe" "${COMMON[@]}" -application org.eclipse.equinox.p2.director -listInstalledRoots -profile "${PROF:-SDKProfile}" "${VMA[@]}" 2>&1; \
  echo "exit=$?"; } | tr -d '\r' | tee "$L/launch-$PROD-listInstalledRoots.txt"
{ echo "\$ eclipsec ${COMMON[*]} -version -application org.eclipse.equinox.p2.director"; \
  timeout 300 "$X/eclipsec.exe" "${COMMON[@]}" -version -application org.eclipse.equinox.p2.director "${VMA[@]}" 2>&1; \
  echo "exit=$?"; } | tr -d '\r' | tee "$L/launch-$PROD-version.txt"
cp "$X/eclipse.ini" "$L/eclipse.$PROD.ini"; cat "$X/.eclipseproduct" > "$L/eclipseproduct.$PROD.txt" 2>/dev/null || true
"$J/bin/java" -version 2>&1 | tr -d '\r' > "$L/launch-java-version.txt"
