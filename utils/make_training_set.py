#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

train_file = open(sys.argv[1], 'r')
features_file = open(sys.argv[2], 'r')

id2features = {}
for line in features_file:
    features = line.strip('\r\n').split(',')
    id2features[features[0]] = ' '.join(features[2:])

for line in train_file:
    items = line.strip('\r\n').split(' ')
    print str(items[2]) + ' ' + id2features[items[0]]


    
