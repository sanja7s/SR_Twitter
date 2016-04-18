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
# for original mention graph
#f_in_graph = "mention_graph_weights.dat"
# for reciprocal graph
#f_in_graph = "recip_net_final" 
f_in_graph = "resulting_graph"  
IN_DIR = "../../../DATA/mention_graph/"
#f_out_plot_res = "threshold_mention_graphs/plot_da.txt"
#f_out_plot_res = "threshold_mention_graphs/plot_da_recip.txt"
f_out_plot_res = "threshold_mention_graphs/plot_da_conv.txt"
#f_out_plot_res_rnd = "threshold_mention_graphs/plot_da_rnd.txt"
#img_out_plot = "threshold_mention_graphs/da_weighted.png"
#img_out_plot = "threshold_mention_graphs/da_weighted_recip.png"
img_out_plot = "threshold_mention_graphs/da_weighted_conv.png"
#img_out_plot_rnd = "threshold_mention_graphs/da_weighted_rnd.png"
#########################
img_out_plot_UNW = "threshold_mention_graphs/da_weighted_UNW.png"
img_out_plot_DEFAULT = "threshold_mention_graphs/da_weighted_DEFAULT.png"
img_out_plot_IN_OUT = "threshold_mention_graphs/da_weighted_IN_OUT.png"
img_out_plot_IN_IN = "threshold_mention_graphs/da_weighted_IN_IN.png"
img_out_plot_OUT_IN = "threshold_mention_graphs/da_weighted_OUT_IN.png"
img_out_plot_OUT_OUT = "threshold_mention_graphs/da_weighted_OUT_OUT_conv.png"
#########################
# read from a file that is an edge list with weights
#########################
def read_in_graph():
	# for mention and convultion it is directed
	G = Graph.Read_Ncol(f_in_graph, directed=True, weights=True)
	# for reciprocal it is undirected
	#G = Graph.Read_Ncol(f_in_graph, directed=False, weights=True)
	print f_in_graph
	return G

#########################
# for a given threshold, remove the edges with smaller # of tweets
# and operate on that network to find the degree assortativity
#########################
def degree_assortativity(G, threshold):
	print "stats for %d" % threshold
	summary(G)
	to_delete_edges = [e.index for e in G.es if int(e["weight"]) <= threshold]
	G.delete_edges(to_delete_edges)
	# just a check
	not_connected_nodes = G.vs(_degree_eq=0)
	print len(not_connected_nodes)
	summary(G)

	# for mention and convultion it is directed
	r = G.assortativity(directed=True,types1=G.strength(weights='weight'))
	# for reciprocal it is undirected
	#r = G.assortativity(directed=False,types1=G.strength(weights='weight'))

	print "Degree assortativity for threshold %d is %f " % (threshold, r)
	print 
	return r

#########################
# for a given threshold, remove the edges with smaller # of tweets
# and operate on that network to find the degree assortativity
#########################
def degree_assortativity_complex(G, threshold):
	print "stats for %d" % threshold
	summary(G)
	to_delete_edges = [e.index for e in G.es if int(e["weight"]) <= threshold]
	G.delete_edges(to_delete_edges)
	# just a check
	not_connected_nodes = G.vs(_degree_eq=0)
	print len(not_connected_nodes)
	summary(G)

	#r = G.assortativity(directed=True,types1=G.strength(weights='weight'))
	r_UNW = G.assortativity_degree(directed=True)
	print "Degree assortativity UNWEIGHTED is %f " % (r_UNW)
	r_DEFAULT = G.assortativity(directed=True,types1=G.strength(weights='weight'))
	print "Degree assortativity DEFAULT is %f " % (r_DEFAULT)
	r_IN_OUT = G.assortativity(directed=True,types1=G.strength(weights='weight',mode=IN),types2=G.strength(weights='weight',mode=OUT))
	print "Degree assortativity IN-OUT is %f " % (r_IN_OUT)
	r_OUT_IN = G.assortativity(directed=True,types1=G.strength(weights='weight',mode=OUT),types2=G.strength(weights='weight',mode=IN))
	print "Degree assortativity OUT-IN is %f " % (r_OUT_IN)
	r_IN_IN = G.assortativity(directed=True,types1=G.strength(weights='weight',mode=IN),types2=G.strength(weights='weight',mode=IN))
	print "Degree assortativity IN-IN is %f " % (r_IN_IN)
	r_OUT_OUT = G.assortativity(directed=True,types1=G.strength(weights='weight',mode=OUT),types2=G.strength(weights='weight',mode=OUT))
	print "Degree assortativity OUT-OUT is %f " % (r_OUT_OUT)

	return r_UNW, r_DEFAULT, r_IN_OUT, r_OUT_IN, r_IN_IN, r_OUT_OUT

def plot_DA(xaxis, da, img_out, lab="", col ="g"):
	x = np.array(xaxis)
	y = np.array(da)
	plt.plot(x, y, col, label=lab, hold=True)
	plt.grid(True)
	plt.title('Convolution mention with SR network')
	plt.ylabel('degree assortativity')
	plt.xlabel('# of tweets threshold')
	plt.legend(bbox_to_anchor=(1, 1), bbox_transform=plt.gcf().transFigure)
	plt.savefig(img_out,format='png',dpi=440)
	#plt.clf()

# does nto work for now
def randomize():
	os.chdir(IN_DIR)
	da = []
	xaxis = []

	G = read_in_graph()

	G1 = G.permute_vertices(np.random.permutation(G.vcount()).tolist())

	f = open(f_out_plot_res_rnd, "w")
	for threshold in np.arange(0, 100, 1):
		s = degree_assortativity(G1, threshold)
		da.append(s)
		xaxis.append(threshold)
		f.write(str(threshold) + '\t'+ str(s) + '\n')
	plot_DA(xaxis, da, img_out_plot_rnd)

def main():
	os.chdir(IN_DIR)
	da = []
	xaxis = []

	G = read_in_graph()

	f = open(f_out_plot_res, "w")
	for threshold in np.arange(0, 100, 1):
		s = degree_assortativity(G, threshold)
		da.append(s)
		xaxis.append(threshold)
		f.write(str(threshold) + '\t'+ str(s) + '\n')
	plot_DA(xaxis, da, img_out_plot)

def main_complex():
	os.chdir(IN_DIR) 
	da_UNW = []
	da_DEFAULT = []
	da_IN_OUT = []
	da_OUT_IN = []
	da_IN_IN = []
	da_OUT_OUT = []
	xaxis =  []
	
	G = read_in_graph()

	#f_UNW = open(f_out_plot_res, "w")
	for threshold in np.arange(0, 100, 1):
		r_UNW, r_DEFAULT, r_IN_OUT, r_OUT_IN, r_IN_IN, r_OUT_OUT = degree_assortativity_complex(G, threshold)
		da_UNW.append(r_UNW)
		da_DEFAULT.append(r_DEFAULT)
		da_IN_OUT.append(r_IN_OUT)
		da_OUT_IN.append(r_OUT_IN)
		da_IN_IN.append(r_IN_IN)
		da_OUT_OUT.append(r_OUT_OUT)
		xaxis.append(threshold)
		#f_UNW.write(str(threshold) + '\t'+ str(s) + '\n')

	plot_DA(xaxis, da_UNW, img_out_plot_UNW, "UNW", col ="r")
	#plot_DA(xaxis, da_DEFAULT, img_out_plot_DEFAULT)
	plot_DA(xaxis, da_IN_OUT, img_out_plot_IN_OUT, "IN_OUT", col="g")
	plot_DA(xaxis, da_OUT_IN, img_out_plot_OUT_IN, "OUT_IN", col="b")
	plot_DA(xaxis, da_IN_IN, img_out_plot_IN_IN , "IN_IN", col="m")
	plot_DA(xaxis, da_OUT_OUT, img_out_plot_OUT_OUT, "OUT_OUT", col="y")

main_complex()
#main()
#randomize()