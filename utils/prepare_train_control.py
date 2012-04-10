#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def extract_features(filename):
    features_file = open(filename, 'r')
    id2features = {}
    for line in features_file:
        features = line.strip('\r\n').split(',')
        id2features[features[0]] = ' '.join(features[2:])
    return id2features

id2features = extract_features(sys.argv[1])

if len(sys.argv) == 3:
    train_file = open(sys.argv[2], 'r')
    for line in train_file:
        items = line.strip('\r\n').split(' ')
        print str(items[1]) + ' ' + id2features[items[0]]
else:
    id = 0
    for line in open(sys.argv[1], 'r'):
        print id2features[str(id)]
        id += 1

    


    
