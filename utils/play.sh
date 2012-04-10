#!/bin/bash

#./gen_personalization.py 114529 1 ../data/spam_hosts.txt ../data/nonspam_hosts.txt > ../data/personalization.txt
#./calc_pagerank ../data/uk-2007-05.hostgraph_weighted.graph.txt > ../data/pagerank.txt

./net.py ../data/pickled_hostgraph.txt \
		../data/spam_hosts.txt \
		../data/nonspam_hosts.txt \
		../data/pr_ordered_hosts.txt \
		../data/gov_hosts.txt \
		../data/webspam-uk2007-set1-1.0/WEBSPAM-UK2007-hostnames.txt \
		../data/subgraph.gexf \
    ../data/escorts.txt

