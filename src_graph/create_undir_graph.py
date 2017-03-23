#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	analyze assortativity of the graphs in terms of sentiment
'''
from igraph import *
import networkx as nx
import os
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os
import matplotlib.cm as cm
from collections import defaultdict
import matplotlib
from scipy.stats.stats import pearsonr

import seaborn as sns
sns.set(color_codes=True, font_scale=2) 

f_in_user_labels = "usr_num_CVs.tab"
##################
f_in_user_taxons = "user_taxons.tab"
f_in_user_concepts = "user_concepts.tab"
f_in_user_entities = "user_entities.tab"
f_in_num_tweets = "usr_num_tweets.tab"
#########################
#
f_in_user_sentiment = "user_sentiment.tab"
#
# mention graph
#########################
f_in_graph = "threshold_mention_graphs/directed_threshold0.tab"
f_in_graph_weights = "mention_graph_weights.dat"
f_out_sent_mention_graph = "directed_threshold0_sent_val.tab"
IN_DIR = "../../../DATA/CAPITAL/"

#########################

os.chdir(IN_DIR)

# one time call
def save_MUTUAL_graph():

	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	G.to_undirected(mode='mutual',combine_edges=sum)
	not_connected_nodes = G.vs(_degree_eq=0)
	to_delete_vertices = not_connected_nodes
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	fo = open('mutual_graph_weights', 'w')
	for edge in G.es:
		source_vertex_id = edge.source
		target_vertex_id = edge.target
		n1 = G.vs[source_vertex_id]
		n2 = G.vs[target_vertex_id]
		w = edge['weight']
		fo.write(str(n1['name']) + '\t' + str(n2['name']) + '\t' + str(w) + '\n')

# one time call
def save_MUTUAL_graph_with_SR():

	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	G.to_undirected(mode='mutual',combine_edges=sum)
	not_connected_nodes = G.vs(_degree_eq=0)
	to_delete_vertices = not_connected_nodes
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	mutual_edges = defaultdict(int)
	for edge in G.es:
		source_vertex_id = edge.source
		target_vertex_id = edge.target
		n1 = G.vs[source_vertex_id]['name']
		n2 = G.vs[target_vertex_id]['name']
		w = edge['weight']
		mutual_edges[(n1,n2)] = w


	SR_mutual_edges =  defaultdict(int)
	f = open('mention_graph_IDs_with_SR_weight.dat', 'r')
	for line in f:
		(uid11, uid22, SR, w) = line.split()
		if uid11 == uid22:
			continue
		if uid11 < uid22:
			uid1 = uid11
			uid2 = uid22
		else:
			uid2 = uid11
			uid1 = uid22
		SR = float(SR)
		w = int(w)
		if (uid1,uid2) in mutual_edges or (uid2,uid1) in mutual_edges:
			if not (uid1,uid2) in SR_mutual_edges:
				SR_mutual_edges[(uid1, uid2)] = SR
		else:
			print 'not in mutual'


	print len(SR_mutual_edges)
	print len(mutual_edges)

	fo = open('mutual_graph_SR_and_weights', 'w')
	for (uid1,uid2) in SR_mutual_edges:
		w = int(mutual_edges[(uid1,uid2)])
		if w == 0:
			w = int(mutual_edges[(uid2,uid1)])
			assert w > 0
		SR = SR_mutual_edges[(uid1,uid2)]
		fo.write(str(uid1) + '\t' + str(uid2) + '\t' +  str(SR) + '\t' +  str(w) + '\n')



def read_in_edge_weight_SR(file_name= 'undirected_mention_graph_with_SR_weight.dat'):
	f = open(file_name, 'r')
	s = defaultdict(float)
	i = 0
	for line in f:
		(u1, u2, ew, eSR) = line.split('\t')
		s[float(ew)] = float(eSR)
		i += 1
	print i
	return s

save_MUTUAL_graph_with_SR()


#read_in_edge_weight_SR()
	