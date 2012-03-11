#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

features_file = open(sys.argv[1], 'r')

for line in features_file:
    features = line.strip('\r\n').split(',')
    print ' '.join(features[2:])



    
