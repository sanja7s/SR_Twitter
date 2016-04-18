#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	analyze reciprocity of the directed mention graph
'''
from igraph import *
import os

#########################
# mention graph
#########################
f_in_graph = "threshold_mention_graphs/directed_threshold0.tab"
f_in_graph_weights = "threshold_mention_graphs/mention_graph_weights.dat"
IN_DIR = "../../../DATA/mention_graph/"
#########################


def mention_igraph_reciprocity():
	os.chdir(IN_DIR)
	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	print G.reciprocity()



mention_igraph_reciprocity()