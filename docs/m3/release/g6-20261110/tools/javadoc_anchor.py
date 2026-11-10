# Copyright (c) 2026 Synexia, Hitesh Soliwal (hsoliwal@gmail.com) and others.
# SPDX-License-Identifier: Apache-2.0 OR EPL-2.0
# CNPCDA repair for a `//FLLDCIM:` anchor that a marks pass wrote inside a Javadoc comment line (` * <ul> //FLLDCIM: ...`):
# javadoc renders it as text and doclint can reject it ("text not allowed in <ul> element"). The anchor moves, unchanged,
# to its own line comment just above the `/**` that opens that Javadoc (same indentation); the Javadoc line keeps its text.
# Usage: python javadoc_anchor.py <file> <line>    (1-based line of the Javadoc line holding the anchor)
import re, sys
path, ln = sys.argv[1], int(sys.argv[2])
raw = open(path, 'rb').read()
lines = raw.split(b'\n')
i = ln - 1
m = re.match(rb'^(\s*\*.*?)\s*(//FLLDCIM:[^\r]*)(\r?)$', lines[i])
if not m: sys.exit('refused: no anchor in a comment line at %d' % ln)
j = i
while j >= 0 and not lines[j].lstrip().startswith(b'/**'):
    j -= 1
if j < 0 or i - j > 400: sys.exit('refused: no opening /** above line %d' % ln)
cr = m.group(3)
indent = re.match(rb'^(\s*)', lines[j]).group(1)
lines[i] = m.group(1).rstrip() + cr
lines.insert(j, indent + m.group(2).rstrip() + cr)
open(path, 'wb').write(b'\n'.join(lines))
print('moved anchor from line %d to line %d' % (ln, j + 1))
