#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
'''
from igraph import *
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math

font = {'family' : 'sans-serif',
		'variant' : 'normal',
		'weight' : 'light',
		'size'   : 14}

matplotlib.rc('font', **font)

#########################
# for original mention graph
f_in_graph = "mention_graph_weights.dat"
IN_DIR = "../../../DATA/mention_graph/"
os.chdir(IN_DIR)
# read from a file that is an edge list with weights
#########################
def read_in_graph():
	# for mention it is directed
	G = Graph.Read_Ncol(f_in_graph, directed=True, weights=True)
	# for reciprocal it is undirected
	print f_in_graph
	print G.summary()

	# UNDIR MUTUAL WEIGHTED SUM 
	# and one more copy
	G_mutual = G.copy()
	# this one is undirected weighted
	G_mutual.to_undirected(mode="mutual")
	G_mutual.simplify()
	not_connected_nodes = G_mutual.vs(_degree_eq=0)
	print len(not_connected_nodes)
	print G_mutual.summary()
	return G_mutual

def save_input_for_AGM():
	G = read_in_graph()
	os.chdir('AGM7s')
	f_edgelist = 'MENT_edgelist_4AGM'
	f_nodelabel = 'MENT_nodelabel_4AGM'
	f1 = open(f_edgelist, 'w')
	f2 = open(f_nodelabel, 'w')
	for e in G.es:
		src_id = e.source
		dest_id = e.target
		#src = G.vs[src_id]['name']
		#dest = G.vs[dest_id]['name']
		f1.write(str(src_id) + '\t' + str(dest_id) + '\n')

	for n in G.vs:
		node = G.vs[n.index]['name']
		f2.write(str(n.index) + '\t' + str(node) + '\n')

save_input_for_AGM()
