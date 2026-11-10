# Copyright (c) 2026 Synexia, Hitesh Soliwal (hsoliwal@gmail.com) and others.
# SPDX-License-Identifier: Apache-2.0 OR EPL-2.0
# Commit a set of local files onto a new branch through the Git Data API (no clone): one blob per file, one tree on top of
# the base commit's tree, one commit, one new ref (refused if the ref exists). Prints the commit SHA.
# Usage: python api_tree_commit.py <owner/repo> <base-sha> <branch> <message-file> <manifest.tsv>
#   manifest rows: <path in repo> TAB <local file>
import base64, json, subprocess, sys
repo, base, branch, msgf, manifest = sys.argv[1:6]
def gh(args, data=None):
    r = subprocess.run(['gh', 'api'] + args + (['--input', '-'] if data is not None else []),
                       input=(json.dumps(data) if data is not None else None), capture_output=True, text=True)
    if r.returncode: sys.exit('gh api %s failed: %s' % (args[0], r.stderr.strip()[:500]))
    return json.loads(r.stdout) if r.stdout.strip() else {}
tree = []
for row in open(manifest, encoding='utf-8'):
    row = row.rstrip('\n')
    if not row: continue
    path, local = row.split('\t')
    b = gh(['repos/%s/git/blobs' % repo], {'content': base64.b64encode(open(local, 'rb').read()).decode(), 'encoding': 'base64'})
    tree.append({'path': path, 'mode': '100644', 'type': 'blob', 'sha': b['sha']})
bt = gh(['repos/%s/git/commits/%s' % (repo, base)])['tree']['sha']
nt = gh(['repos/%s/git/trees' % repo], {'base_tree': bt, 'tree': tree})['sha']
who = {'name': 'Hitesh Soliwal', 'email': 'hsoliwal@gmail.com'}
c = gh(['repos/%s/git/commits' % repo], {'message': open(msgf, encoding='utf-8').read(), 'tree': nt, 'parents': [base],
                                          'author': who, 'committer': who})
gh(['repos/%s/git/refs' % repo, '-X', 'POST'], {'ref': 'refs/heads/' + branch, 'sha': c['sha']})
print(c['sha'], len(tree), 'files')
