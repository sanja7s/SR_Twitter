#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from snap import *
from collections import defaultdict
import codecs

WORKING_FOLDER = "../../../DATA/mention_graph/threshold_mention_graphs"
OUT_FOLDER = "communities"

F_IN = "directed_threshold" + str(THRESHOLD) + ".tab"
F_OUT = OUT_FOLDER + "/communities" + str(THRESHOLD) +".tab"


def graphs_stats():
	print "Created directed graph, with: ", G.number_of_nodes(), "nodes; and: ", G.number_of_edges(), " edges."
	print "7 maximum degrees of nodes: ", sorted(nx.degree(G).values())[-7:]
	print "7 maximum indegrees of nodes: ", sorted(G.in_degree().values())[-7:]
	print "7 maximum outdegrees of nodes: ", sorted(G.out_degree().values())[-7:]
	print "Connected components: ", len(nx.connected_components(G.to_undirected()))
	i = 0
	print "7 maximum connected components: "
	for el in sorted(nx.connected_components(G.to_undirected()), key=lambda x: len(x), reverse=True):
		i+=1
		print len(el)
		if i==7: break
	#nx.draw(G)
	#plt.show()

def read_in_graph():
	return snap.LoadEdgeList(snap.PNGraph, F_IN, 0, 1)

def subgraph_SR(list_nodes):
	SR_lst = []
	for node1 in list_nodes:
		for node2 in list_nodes:
			k = (node1, node2)
			try:
				SR_lst.append(G_WITH_SR[k][1])
			except:
				KeyError
	return SR_lst

def save_communities():
	





G = read_in_graph_data()
