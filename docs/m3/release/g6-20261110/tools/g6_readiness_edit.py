# Copyright (c) 2026 Synexia, Hitesh Soliwal (hsoliwal@gmail.com) and others.
# SPDX-License-Identifier: Apache-2.0 OR EPL-2.0
# Rewrites the aggregator RELEASE_READINESS.md for the G6 result: G6 row, the submodule URL table (all 12 components are
# hsoliwal forks since master 9948656c21a1, so the "still upstream" HOLD rows go), and a dated G6 result block.
# Usage: python g6_readiness_edit.py <readiness.md> <g6-row-verdict> <g6-row-evidence> <g6-section-file>
import sys
p, verdict, evidence, section = sys.argv[1:5]
s = open(p, encoding='utf-8', newline='').read()
lines = s.split('\n')
out = []
skip = False
for l in lines:
    if l.startswith('| G6 |'):
        l = '| G6 | Eclipse SDK product build and headless launch on JDK 21 | %s | %s |' % (verdict, evidence)
    if l.startswith('### Submodule URLs (.gitmodules)'):
        skip = True
        out.append(l)
        out.append('')
        out.append('Since aggregator master 9948656c21a1 (#17) every submodule URL is an hsoliwal fork; the pinned commits did not change.')
        out.append('')
        out.append('| Submodule | URL | Pointer |')
        out.append('| --- | --- | --- |')
        for path, url, ptr in [
            ('eclipse.jdt', 'hsoliwal/eclipse.jdt', '28561c3c115d'),
            ('eclipse.jdt.core', 'hsoliwal/eclipse.jdt.core', '617d2cc38309'),
            ('eclipse.jdt.core.binaries', 'hsoliwal/eclipse.jdt.core.binaries', '987122d226c7'),
            ('eclipse.jdt.debug', 'hsoliwal/eclipse.jdt.debug', '6b077f8147ef'),
            ('eclipse.jdt.ui', 'hsoliwal/eclipse.jdt.ui', '785cf01205b0'),
            ('eclipse.pde', 'hsoliwal/initiative31-eclipse.pde (branch upstream-master)', 'ba6a5d6f2f45'),
            ('eclipse.platform', 'hsoliwal/eclipse.platform', '776e96e6c8f4'),
            ('eclipse.platform.swt', 'hsoliwal/eclipse.platform.swt', 'b4579e0a346e'),
            ('eclipse.platform.ui', 'hsoliwal/eclipse.platform.ui', '38238345c75c'),
            ('equinox', 'hsoliwal/equinox', '7ed67c081fca'),
            ('equinox.binaries', 'hsoliwal/equinox.binaries', '7a1125f75ed9'),
            ('equinox.p2', 'hsoliwal/p2', 'bc63431121cc')]:
            out.append('| %s | %s | %s |' % (path, url, ptr))
        out.append('')
        continue
    if skip:
        if l.startswith('## ') or l.startswith('### '):
            skip = False
        else:
            continue
    if l.startswith('## G6: Eclipse SDK product build and launch on JDK 21'):
        out.append(open(section, encoding='utf-8', newline='').read().rstrip('\n'))
        out.append('')
        out.append('### Earlier record (2026-11-09 and 2026-11-10 morning)')
        continue
    out.append(l)
open(p, 'w', encoding='utf-8', newline='').write('\n'.join(out))
