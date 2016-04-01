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
import matplotlib.pyplot as plt
#########################
X = "0.2"
"""
#for RANDOM v1
f_in_graph_SR = "random_v1_threshold_graphs/rnd_SR_" + str(X) #+ "_1K"
IN_DIR = "../../../DATA/SR_graphs/"
f_out_plot_res = "random_v1_threshold_graphs/plot_da_rnd_v1_0.2.txt"
img_out_plot = "random_v1_threshold_graphs/da_rnd_v1.png"
"""
#for RANDOM v2
f_in_graph_SR = "random_v2_threshold_graphs/" + str(X) + "_rnd2_SR"
IN_DIR = "../../../DATA/SR_graphs/"
f_out_plot_res = "random_v2_threshold_graphs/plot_da_rnd_v2_0.2.txt"
img_out_plot = "random_v2_threshold_graphs/da_rnd_v2.png"
"""
#for RANDOM v27s (v22)
f_in_graph_SR = "random_v2_threshold_graphs/" + str(X) + "_rnd27s_SR"
IN_DIR = "../../../DATA/SR_graphs/"
f_out_plot_res = "random_v2_threshold_graphs/plot_da_rnd_v27s_0.2.txt"
img_out_plot = "random_v2_threshold_graphs/da_rnd_v27s.png"
"""
"""
# for ORIGINAL
f_in_graph_SR = "threshold_graphs/filter_IDs_SR_0.2"
IN_DIR = "../../../DATA/SR_graphs/"
f_out_plot_res = "threshold_graphs/plot_da_0.2.txt"
img_out_plot = "threshold_graphs/da.png"
"""
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
	print "Degree assortativity for threshold %2f is %f " % (threshold, r)
	print 
	return r

def plot_DA(xaxis, da):
	x = np.array(xaxis)
	y = np.array(da)
	plt.plot(x, y, 'g')
	plt.grid(True)
	plt.title('Randomized SR network (no scaling)')
	#plt.legend(bbox_to_anchor=(0, 1), bbox_transform=plt.gcf().transFigure)
	plt.ylabel('degree assortativity')
	plt.xlabel('SR threshold')
	plt.savefig(img_out_plot,format='png',dpi=440)


def main():
	os.chdir(IN_DIR)
	da = []
	xaxis = []

	G = read_in_SR_graph()

	f = open(f_out_plot_res, "w")
	for threshold in np.arange(0.2, 1, 0.01):
		s = degree_assortativity(G, threshold)
		da.append(s)
		xaxis.append(threshold)
		f.write(str(threshold) + '\t'+ str(s) + '\n')
	plot_DA(xaxis, da)

main()