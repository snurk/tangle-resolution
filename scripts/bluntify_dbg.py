#!/usr/bin/env python
from __future__ import division
from __future__ import print_function

import sys

if len(sys.argv) < 2:
	print("Usage: %s <k>" % sys.argv[0])
	sys.exit(1)

ovl = int(sys.argv[1])

# graph from stdin
# graph to stdout

#assert ovl % 2 == 0
remove_overlap = ovl // 2

print("H\tVN:Z:1.0")

node_seqs = {}
has_edge = set()
for l in sys.stdin:
	parts = l.strip().split('\t')
	if l[0] == 'S':
		node_seqs[parts[1]] = parts[2]
	if l[0] == 'L':
		print("L\t%s\t%s\t%s\t%s\t%dM" % (parts[1], parts[2], parts[3], parts[4], ovl % 2))
		has_edge.add((parts[1], parts[2] == "+"))
		has_edge.add((parts[3], parts[4] == "-"))

for node in node_seqs:
	seq = node_seqs[node]
	assert len(seq) > 2 * remove_overlap
	if (node, True) in has_edge:
		seq = seq[:-remove_overlap]
	if (node, False) in has_edge:
		seq = seq[remove_overlap:]
	print("S\t" + node + "\t" + seq)
