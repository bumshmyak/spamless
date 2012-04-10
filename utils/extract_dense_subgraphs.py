#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import collections
import random
import pickle
import networkx as nx

def shingle(elements, s, coefficients, p):
    z = []
    hashes = [hash(x) for x in elements]
    for c in coefficients:
        y = [(c[0] * h + c[1]) % p for h in hashes]
        z.append(hash(str(sorted(y)[:s])))
    return z

def shingle2(G, s1, c1, s2, c2):
    p = 18446744073709551557 # 2^64 - 59
    coefficients1 = [(random.randint(2, p - 1), random.randint(2, p - 1)) for i in xrange(c1)]
    coefficients2 = [(random.randint(2, p - 1), random.randint(2, p - 1)) for i in xrange(c2)]
    
    shingle_vertices = {}
    for v in nx.nodes_iter(G):
        for sh in shingle(G.successors(v), s1, coefficients1, p):
            shingle_vertices.setdefault(sh, []).append(v)
                
    metashingle_shingles = {}
    for sh, vertices in shingle_vertices.iteritems():
        for metash in shingle(vertices, s2, coefficients2, p):
            metashingle_shingles.setdefault(metash, []).append(sh)

    return shingle_vertices, metashingle_shingles


def CC(key_values):
    p = {}
    for key, values in key_values.iteritems():
         for v in values:
             p[v] = v

    def Find(v):
        if p[v] != v:
            p[v] = Find(p[v])
        return p[v]

    for key, values in key_values.iteritems():
        r = Find(values[0])
        for v in values[1:]:
            p[Find(v)] = r

    clusters = {}
    for v, r in p.iteritems():
        clusters.setdefault(r, []).append(v)

    return [components for key, components in clusters.iteritems()]

def get_dense_subgraphs(G):
    s1, c1 = (4, 16)
    s2, c2 = (4, 16)
    shingle_vertices, metashingle_shingles = shingle2(G, s1, c1, s2, c2)
    components = CC(metashingle_shingles)
    clusters = []
    for c in components:
        cluster = set([])
        for sh in c:
            cluster |= set(shingle_vertices[sh])
        clusters.append(cluster)
        
    return clusters

def get_subgraph(G, vertices):
    H = nx.DiGraph()
    H.add_nodes_from(vertices)
    for u in vertices:
        for v in G.successors(u):
            if v in vertices:
                H.add_edge(u, v, weight=G[u][v]['weight'])
    return H

G = nx.read_gpickle(sys.argv[1])

#clusters = get_dense_subgraphs(G)
#print len(clusters)
#pickle.dump(clusters, open(sys.argv[2], 'w'))
clusters = pickle.load(open(sys.argv[2], 'r'))

res = set([])
for c in clusters:
    if 20 <= len(c) <= 1000:
        res |= set(c)

nx.write_gexf(get_subgraph(G, res), sys.argv[3])


                
    



