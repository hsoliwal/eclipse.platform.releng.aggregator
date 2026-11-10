# Copyright (c) 2026 Synexia, Hitesh Soliwal (hsoliwal@gmail.com) and others.
# SPDX-License-Identifier: Apache-2.0 OR EPL-2.0
# One exact byte replacement in one file of a GitHub repository, committed on a new branch from master through the
# contents API (no clone). Refuses unless the old text occurs exactly once. Prints the new commit SHA.
# Usage: python api_line_fix.py <owner/repo> <branch> <path> <old> <new> <message>
import base64, json, subprocess, sys
repo, branch, path, old, new, msg = sys.argv[1:7]
def gh(args, data=None):
    r = subprocess.run(['gh', 'api'] + args + (['--input', '-'] if data is not None else []),
                       input=(json.dumps(data) if data is not None else None), capture_output=True, text=True)
    if r.returncode: sys.exit('gh api %s failed: %s' % (args[0], r.stderr.strip()))
    return json.loads(r.stdout) if r.stdout.strip() else {}
master = gh(['repos/%s/commits/master' % repo])['sha']
gh(['repos/%s/git/refs' % repo, '-X', 'POST'], {'ref': 'refs/heads/' + branch, 'sha': master})
from urllib.parse import quote
c = gh(['repos/%s/contents/%s?ref=%s' % (repo, quote(path), branch)])
body = base64.b64decode(c['content'])
o, n = old.encode('utf-8'), new.encode('utf-8')
if body.count(o) != 1: sys.exit('refused: %d occurrences' % body.count(o))
body = body.replace(o, n)
who = {'name': 'Hitesh Soliwal', 'email': 'hsoliwal@gmail.com'}
r = gh(['repos/%s/contents/%s' % (repo, quote(path)), '-X', 'PUT'],
       {'message': msg, 'content': base64.b64encode(body).decode(), 'sha': c['sha'], 'branch': branch,
        'author': who, 'committer': who})
print(master, r['commit']['sha'])
