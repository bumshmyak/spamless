#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def get_host_ids(filename):
    f = open(filename, 'r')
    res = []
    for line in f:
        line = line.strip('\r\n')
        res.append(int(line))
    return res

n = int(sys.argv[1])
k = int(sys.argv[2])
spam = set(get_host_ids(sys.argv[3]))
nonspam = set(get_host_ids(sys.argv[4]))

y = 1.0 / (k * len(nonspam) + n - len(spam) - len(nonspam))
x = k * y

for i in xrange(n):
    if i in spam:
        print 0
    elif i in nonspam:
        print x
    else:
        print y

    

