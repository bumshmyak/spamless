#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import networkx as nx

input_file = open(sys.argv[1], 'r')

G = nx.DiGraph()
host_count = int(input_file.readline())
G.add_nodes_from(xrange(host_count))

u = 0
for line in input_file:
    line = line.strip('\r\n')
    if line:
        for edge in line.split(' '):
            v, w = [int(t) for t in edge.split(':')]
            G.add_edge(u, v, weight=w)
    u += 1

print G.number_of_nodes()
print G.number_of_edges()
nx.write_gpickle(G, sys.argv[2])
        

