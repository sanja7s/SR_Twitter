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
import pandas as pd

import seaborn as sns
sns.set(color_codes=True, font_scale=2) 
sns.set_style('whitegrid')

import pandas as pd
from scipy import stats, integrate

f_in_user_labels = "usr_num_CVs.tab"
##################
f_in_user_taxons = "user_taxons.tab"
f_in_user_concepts = "user_concepts.tab"
f_in_user_entities = "user_entities.tab"
f_in_num_tweets = "usr_num_tweets.tab"
#########################
#
f_in_user_sentiment = "user_sentiment.tab"
# mention graph
#########################
f_in_graph = "threshold_mention_graphs/directed_threshold0.tab"
f_in_graph_weights = "threshold_mention_graphs/mention_graph_weights.dat"
f_out_sent_mention_graph = "directed_threshold0_sent_val.tab"
IN_DIR = "../../../DATA/CAPITAL/"
f_out_mention = "sentiment_assortativity_mention_2.txt"
#########################

f_in_graph_weights = "mention_graph_weights.dat"

os.chdir(IN_DIR)

#########################
# read from a file that is an edge list with weights
#########################
def read_in_graph():
	# for mention and convultion it is directed
	G = Graph.Read_Ncol(f_in_graph_weights, names=True, directed=True, weights=True)
	# for reciprocal it is undirected
	#G = Graph.Read_Ncol(f_in_graph, directed=False, weights=True)
	print f_in_graph
	return G

def read_BI():
	return pd.read_csv('BI_indexR_full.txt',\
		encoding='utf-8', delim_whitespace=1)

def BI_capital_assort():
	bi = read_BI()
	print max(bi['bi']), min(bi['bi'])
	G = read_in_graph()
	bidict = bi.set_index('id')['bi'].to_dict()
	for el in bidict:
		if bidict[el] > 1:
			bidict[el] = 1
		v = G.vs.select(name = str(el))
		print el, v
		v["bi"] = bidict[el] 

	to_delete_vertices = [v.index for v in G.vs if v["bi"] == None]
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	G.to_undirected(mode='mutual')
	not_connected_nodes = G.vs(_degree_eq=0)
	to_delete_vertices = not_connected_nodes
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	print "UNDIR BI assortativity is %f " %  (G.assortativity("bi",directed=False))

	

BI_capital_assort()

