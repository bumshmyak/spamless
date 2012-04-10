#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import collections
import networkx as nx

def get_host_ids(filename):
    f = open(filename, 'r')
    res = []
    for line in f:
        line = line.strip('\r\n')
        res.append(int(line))
    return res

def get_dist1_vertices(G, vertices):
    dist1_vertices = set([])
    for u in vertices:
        dist1_vertices |= set(G.successors(u))
        
    return dist1_vertices

def get_subgraph(G, vertices):
    H = nx.DiGraph()
    H.add_nodes_from(vertices)
    for u in vertices:
        for v in G.successors(u):
            if v in vertices:
                H.add_edge(u, v, weight=G[u][v]['weight'])
    return H

def get_fb(G, vertices, threshold = 1):
    fb = set([])
    vertices_dist1 = get_dist1_vertices(G, vertices)
    for v in vertices_dist1:
        t = 0
        for u in G.successors(v):
            if u in vertices:
                t += 1
        if t >= threshold:
            fb.add(v)

    return fb

def get_specified_outdegree_vertices(G, a, b):
    res = []
    for v in G.nodes_iter():
        m = len(G.successors(v))
        if a <= m and m <= b:
            res.append(v)
    return res

def get_outdegree_histogram(G):
    res = collections.Counter()
    for v in G.nodes_iter():
        res[len(G.successors(v))] += 1
    return res

def read_hostnames(filename):
    id2name = {}
    for line in open(filename, 'r'):
        line = line.strip('\r\n')
        id, name = line.split(' ')
        id2name[int(id)] = name
    return id2name

id2name = read_hostnames(sys.argv[6])
G = nx.read_gpickle(sys.argv[1])

print "nodes", G.number_of_nodes()
print "edges", G.number_of_edges()

spam = set(get_host_ids(sys.argv[2]))
nonspam = set(get_host_ids(sys.argv[3]))
pr = set(get_host_ids(sys.argv[4])[:500])
gov = set(get_host_ids(sys.argv[5]))
escorts = set(get_host_ids(sys.argv[8]))

print "escorts & spam", len(escorts & spam)
for s in escorts & spam:
    print s, id2name[s]

print "escorts & nonspam", len(escorts & nonspam)
for s in escorts & nonspam:
    print s, id2name[s]

isolates = set(nx.isolates(G))

print "isolates", len(isolates)
print "spam", len(spam)
print "nonspam", len(nonspam)
print "pr", len(pr)
print "gov", len(gov)

spam_dist1 = get_dist1_vertices(G, spam)
nonspam_dist1 = get_dist1_vertices(G, nonspam)
pr_dist1 = get_dist1_vertices(G, pr)
gov_dist1 = get_dist1_vertices(G, gov)

print "spam_dist1", len(spam_dist1)
print "nonspam_dist1", len(nonspam_dist1)
print "pr_dist1", len(pr_dist1)
print "gov_dist1", len(gov_dist1)

print "spam & spam_dist1", len(spam & spam_dist1)
print "spam & nonspam_dist1", len(spam & nonspam_dist1)
print "spam & pr_dist1", len(spam & pr_dist1)
print "spam & gov_dist1", len(spam & gov_dist1)
print "spam & isolates", len(spam & isolates)
print "nonspam & isolates", len(nonspam & isolates)

pr_gov = pr & gov
pr_gov_dist1 = get_dist1_vertices(G, pr_gov)

print "pr_gov", len(pr_gov)
print "pr_gov_dist1", len(pr_gov_dist1)
print "spam & pr_gov_dist1", len(spam & pr_gov_dist1)

print "links from good to spam:"
for v in pr_gov_dist1:
    if v in spam:
        for u in pr_gov:
            if v in G.successors(u):
                print id2name[u], id2name[v]

fb_spam = get_fb(G, spam)
fb_fb_spam = get_fb(G, fb_spam | spam, 10)
print "fb_spam", len(fb_spam)
print "spam | fb_spam", len(spam | fb_spam)
print "fb_fb_spam", len(fb_fb_spam)
print "spam | fb_spam | fb_fb_spam", len(spam | fb_spam | fb_fb_spam)

#nx.write_gexf(get_subgraph(G, spam | fb_spam | fb_fb_spam), sys.argv[7])
#nx.write_gexf(get_subgraph(G, pr_gov), sys.argv[7])
#components = nx.strongly_connected_components(G)
#print len(components)
#print [len(c) for c in components if len(c) > 1]

print "grand spammer", id2name[100812], len(G.successors(100812))

print "fb_spam_nonspam", len(fb_spam & nonspam)
print "fb_spam_pr_gov", len(fb_spam & pr_gov)

#outdegree = set(get_specified_outdegree_vertices(G, 25, 35))
#print "outdegree", len(outdegree)
#nx.write_gexf(get_subgraph(G, outdegree), sys.argv[7])

