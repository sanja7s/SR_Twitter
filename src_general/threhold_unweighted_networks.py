#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
	In order to apply some community detection algorithms, we need unweighted networks. So we experiment by thresholding the SR amd mention networks
	with different thresholds.
	V1: directed mention network with a threshold on mentions on the directed edge
	V2: 
	# SR thresholds 0.6 (>thresholds there is an edge, <0.6 no edge) 
"""

from collections import defaultdict
import codecs
import glob, os

THRESHOLD = 20

WORKING_FOLDER = "../../../DATA/mention_graph/"
OUT_FOLDER = "threshold_mention_graphs"

F_IN = "graph_20_tweets_IDs.dat"
F_OUT = OUT_FOLDER + "/directed_threshold" + str(THRESHOLD) +".tab"

#G = nx.DiGraph()
#G_WITH_SR = GG.read_in_graph_with_SR()

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

def threshold_graph_v1():

	os.chdir(WORKING_FOLDER)

	input_file = codecs.open(F_IN, 'r', encoding='utf8')
	output_file = codecs.open(F_OUT, 'w', encoding='utf8')

	for line in input_file:
		line = line.split()
		usr1 = line[0]
		usr2 = line[1]
		weight = int(line[2])
		if weight > THRESHOLD:
			output_file.write(usr1 + '\t' + usr2 + '\n') 
	input_file.close()
	output_file.close()

threshold_graph_v1()

