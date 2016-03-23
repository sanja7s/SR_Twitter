#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	analyze assortativity of the graph in terms of degree only
	also, go through different thresholds and find the map:
	threshold -> degree_assortativity 
'''
from igraph import *
import os
import numpy as np
#########################
X = "0.4"
"""
#for RANDOM v1
f_in_graph_SR = "random_v1_threshold_graphs/rnd_SR_" + str(X) #+ "_1K"
IN_DIR = "../../../DATA/SR_graphs/"
f_out_plot_res = "random_v1_threshold_graphs/plot_da_rnd_v1.txt"
"""
# for ORIGINAL
f_in_graph_SR = "threshold_graphs/filter_IDs_SR_0.4"
IN_DIR = "../../../DATA/SR_graphs/"
f_out_plot_res = "threshold_graphs/plot_da.txt"
#########################

#########################
# read from a file that is an edge list with SR weights
#########################
def read_in_SR_graph():
	G = Graph.Read_Ncol(f_in_graph_SR, directed=False, weights=True)
	print f_in_graph_SR
	return G

#########################
# for a given threshold, remove the edges with smaller SR
# and operate on that network to find the degree assortativity
#########################
def degree_assortativity(G, threshold):
	print "stats for %.2f" % threshold
	summary(G)
	to_delete_edges = [e.index for e in G.es if float(e["weight"]) <= threshold]
	G.delete_edges(to_delete_edges)
	# just a check
	not_connected_nodes = G.vs(_degree_eq=0)
	print len(not_connected_nodes)
	summary(G)

	#f_out_SR = "random_v1_threshold_graphs/" + str(threshold) + "_da_rnd_v1.txt"
	#sys.stdout = open(f_out_SR, 'w')
	#summary(G)
	r = G.assortativity_degree(directed=False)
	print "Degree assortativity is %f " % (r)
	print 
	return r

def main():
	os.chdir(IN_DIR)
	da = []
	xaxis = []

	G = read_in_SR_graph()

	f = open(f_out_plot_res, "w")
	for threshold in np.arange(0.4, 1, 0.01):
		s = degree_assortativity(G, threshold)
		da.append(s)
		xaxis.append(threshold)
		f.write(str(threshold) + '\t'+ str(s) + '\n')

main()