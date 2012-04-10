#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

test_file = open(sys.argv[1], 'r')
predictions_file = open(sys.argv[2], 'r')

id2prediction = {}
for line in predictions_file:
    host_id, host_prediction = line.strip('\r\n').split(',')
    id2prediction[host_id] = host_prediction

for line in test_file:
    items = line.strip('\r\n').split(' ')
    host_id = items[0]
    host_prediction = float(items[1])
    host_label = 0
    if host_prediction == 0.5:
        continue
    if host_prediction > 0.5:
        host_label = 1
    
    print host_label, id2prediction[host_id]
    
