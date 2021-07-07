#!/usr/bin/env python
from __future__ import division
from __future__ import print_function

import argparse
import fileinput

def pathstr(p):
	return "".join(p)

def reverse(n):
	return (">" if n[0] == '<' else '<') + n[1:]

parser = argparse.ArgumentParser(description="Connection filter (graph read from standard input)")
parser.add_argument("--min-weight", type=int, default=5, help="Minimal evidence required to consider removing alternatives (default 5)")
parser.add_argument("--gap-ratio", type=float, default=0.5, help="Removing connection if evidence ratio against best alternative is lower than threshold (default 0.5)")
args = parser.parse_args()

connectors = {}

connections = []

for line in fileinput.input():
	l = line.strip() + ">"
	last_break = 0
	path = []
	for i in range(1, len(l)):
		if l[i] == '<' or l[i] == '>':
			path.append(l[last_break:i])
			last_break = i
	assert len(path) >= 2
	fwkey = path[0]
	bwkey = reverse(path[-1])
	if fwkey not in connectors: connectors[fwkey] = {}
	if bwkey not in connectors[fwkey]: connectors[fwkey][bwkey] = []
	connectors[fwkey][bwkey].append(len(connections))
	if bwkey not in connectors: connectors[bwkey] = {}
	if fwkey not in connectors[bwkey]: connectors[bwkey][fwkey] = []
	connectors[bwkey][fwkey].append(len(connections))
	connections.append(path)

forbidden = set()

for fwpos in connectors:
	max_coverage = 0
	for bwpos in connectors[fwpos]:
		max_coverage = max(max_coverage, len(connectors[fwpos][bwpos]))

	if max_coverage < args.min_weight:
		continue

	for bwpos in connectors[fwpos]:
		if 1. * len(connectors[fwpos][bwpos]) < args.gap_ratio * max_coverage - 0.01:
			for j in connectors[fwpos][bwpos]:
				forbidden.add(j)

for i in range(0, len(connections)):
	if i in forbidden: continue
	print(pathstr(connections[i]))
