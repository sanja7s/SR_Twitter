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
# for reciprocal graph
#f_in_graph = "recip_net_final" 
#f_in_graph = "resulting_graph"  
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
img_out_plot_UNDIR_W_all = "threshold_mention_graphs/da_weighted_undir_all_3007.eps"
img_out_plot_UNDIR_W_mutual = "threshold_mention_graphs/da_weighted_undir_mutual_3007.eps"
img_out_plot_UNDIR = "threshold_mention_graphs/da_weighted_UNDIR_3007.eps"
img_out_plot_DEFAULT = "threshold_mention_graphs/da_weighted_DEFAULT_3007s.eps"
img_out_plot_IN_OUT = "threshold_mention_graphs/da_weighted_IN_OUT_3007s.eps"
img_out_plot_IN_IN = "threshold_mention_graphs/da_weighted_IN_IN_3007s.eps"
img_out_plot_OUT_IN = "threshold_mention_graphs/da_weighted_OUT_IN_3007s.eps"
img_out_plot_OUT_OUT = "threshold_mention_graphs/da_weighted_OUT_OUT_3007s.eps"
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

def jackknife_da_dir(G, r, dir, t1, t2, weighted=False):
	ri = []
	G1 = G.copy()
	print len(G.es)
	i = 0
	for e in G.es:
		G1.delete_edges((e.source, e.target))
		if weighted:
			r1 = G1.assortativity(directed=dir,types1=G1.strength(weights='weight',mode=t1),types2=G1.strength(weights='weight',mode=t2))
		else:
			r1 = G1.assortativity(directed=dir,types1=G1.degree(mode=t1, loops=False),types2=G1.degree(mode=t2, loops=False))
		ri.append(r1)
		if i%1000==0:
			print i, r1
		i += 1
		if weighted:
			G1.add_edge(e.source, e.target, weight=e["weight"])
		else:
			G1.add_edge(e.source, e.target)
	s = 0.0
	for r1 in ri:
		s += (r1-r)*(r1-r)
	return math.sqrt(s)

def jackknife_da_undir(G, r, weighted):
	ri = []
	G1 = G.copy()
	print len(G.es)
	i = 0
	for e in G.es:
		G1.delete_edges((e.source, e.target))
		if weighted:
			r1 = G1.assortativity(directed=False, types1=G.strength(weights='weight'))
		else:
			r1 = G1.assortativity_degree(directed=False)
		ri.append(r1)
		if i%1000==0:
			print i, r1
		i += 1
		if weighted:
			G1.add_edge(e.source, e.target, weight=e["weight"])
		else:
			G1.add_edge(e.source, e.target)
	s = 0.0
	for r1 in ri:
		s += (r1-r)*(r1-r)
	return math.sqrt(s)


#########################
# for a given threshold, remove the edges with smaller # of tweets
# and operate on that network to find the degree assortativity
# apply jackknife method to evaluate statistical significance of the assort
#########################
def degree_assortativity_statistical_significance_undir_colapsed_unw(G, threshold):

	# UNDIRECTED COLLAPSED UNWEIGHTED
	# here we create a deep copy of G
	G_undir_unweighted = G.copy()
	# this copy is then transformed into single edges (no weight) undirected graph
	G_undir_unweighted.to_undirected(mode="collapse", combine_edges='ignore')
	r_UNDIR_UNW = G_undir_unweighted.assortativity_degree(directed=False)
	s_UNDIR_UNW = jackknife_da_undir(G_undir_unweighted, r_UNDIR_UNW, False)
	print "UNDIRECTED UNWEIGHTED collapsed to 1: %f and stdev %f " % (r_UNDIR_UNW, s_UNDIR_UNW)

def degree_assortativity_statistical_significance_undir_mutual_unw(G, threshold):
	# UNDIRECTED MUTUAL UNWEIGHTED
	# here we create a deep copy of G
	G_undir_unweighted_mutual = G.copy()
	# this copy is then transformed into single edges (no weight) undirected graph
	G_undir_unweighted_mutual.to_undirected(mode="mutual", combine_edges='ignore')
	r_UNDIR_UNW_mutual = G_undir_unweighted_mutual.assortativity_degree(directed=False)
	s_UNDIR_UNW_mutual = jackknife_da_undir(G_undir_unweighted_mutual, r_UNDIR_UNW_mutual, False)
	print "UNDIRECTED MUTUAL UNWEIGHTED %f and stdev %f " % (r_UNDIR_UNW_mutual, s_UNDIR_UNW_mutual)

def degree_assortativity_statistical_significance_undir_mutual_weighted(G, threshold):
	# UNDIR MUTUAL WEIGHTED SUM 
	# and one more copy
	G_undir_weighted = G.copy()
	# this one is undirected weighted having the weight of only mutual communication
	G_undir_weighted.to_undirected(mode="mutual", combine_edges=sum)
	r_UNDIR_WEIGHTED_mutual = G_undir_weighted.assortativity(directed=False, types1=G_undir_weighted.strength(weights='weight'))
	s_UNDIR_WEIGHTED_mutual = jackknife_da_undir(G_undir_weighted, r_UNDIR_WEIGHTED_mutual, weighted=True)
	print "UNDIRECTED MUTUAL WEIGHTED (sum mutual): %f stdev %f" % (r_UNDIR_WEIGHTED_mutual, s_UNDIR_WEIGHTED_mutual)

def degree_assortativity_statistical_significance_undir_colapsed_weighted(G, threshold):

	# UNDIR WEIGHTED COLAPSED SUM ALL
	# another copy of G
	G_undir_weighted = G.copy()
	# this one is transformed to undirected with sum of all edges weight
	G_undir_weighted.to_undirected(mode="collapse", combine_edges=sum)
	r_UNDIR_WEIGHTED_all = G_undir_weighted.assortativity(directed=False, types1=G_undir_weighted.strength(weights='weight'))
	s_UNDIR_WEIGHTED_all = jackknife_da_undir(G_undir_weighted, r_UNDIR_WEIGHTED_all, weighted=True)
	print "UNDIRECTED WEIGHTED (sum all) is %f and stdev %f " % (r_UNDIR_WEIGHTED_all, s_UNDIR_WEIGHTED_all)

	# DIRECTED UNWEIGHTED
	#r_UNW = G.assortativity_degree(directed=True)
	#print "Degree assortativity DIRECTED UNWEIGHTED is %f " % (r_UNW)

	# DIRECTED COLAPSED UNWEIGHTED -- THIS IS A CHECK
	#G_dir_unweighted = G.copy()
	# this copy is then transformed into single edges (no weight) undirected graph
	#G_dir_unweighted.simplify()
	#r_DIR_UNW = G_dir_unweighted.assortativity_degree(directed=True)
	#print "Degree assortativity DIRECTED UNWEIGHTED collapsed to 1 is %f " % (r_DIR_UNW)

	# DIRECTED COLAPSED UNWEIGHTED -- THIS IS A CHECK
	#G_dir_unweighted2 = G.copy()
	# this copy is then transformed into single edges (no weight) undirected graph
	#G_dir_unweighted2.simplify(loops=False)
	#r_DIR_UNW2 = G_dir_unweighted2.assortativity_degree(directed=True)
	#print "Degree assortativity DIRECTED UNWEIGHTED loops false is %f " % (r_DIR_UNW2)
	# degree(vertices, mode=ALL, loops=True)

def degree_assortativity_statistical_significance_IN_OUT_unw(G, threshold):
	# IN OUT no weights etc.
	r_IN_OUT_unw = G.assortativity(directed=True,types1=G.degree(mode=IN, loops=False),types2=G.degree(mode=OUT, loops=False))
	s_IN_OUT_unw = jackknife_da_dir(G, r_IN_OUT_unw, True, t1=IN, t2=OUT)
	print "IN-OUT unweighted is %f and expected stdev %f " % (r_IN_OUT_unw, s_IN_OUT_unw)

	#r_IN_OUT_unw2 = G.assortativity(directed=True,types1=G.degree(mode=IN, loops=False),types2=G.degree(mode=OUT, loops=False))
	#s_IN_OUT_unw2 = jackknife_da_dir(G, r_IN_OUT_unw, True, t1=IN, t2=OUT)
	#print "Degree assortativity IN-OUT unweighted TEST is %f " % (r_IN_OUT_unw2)

def degree_assortativity_statistical_significance_OUT_IN_unw(G, threshold):
	r_OUT_IN_unw = G.assortativity(directed=True,types1=G.degree(mode=OUT, loops=False),types2=G.degree(mode=IN, loops=False))
	s_OUT_IN_unw = jackknife_da_dir(G, r_OUT_IN_unw, True, t1=OUT, t2=IN)
	print "OUT-IN unweighted is %f and expected stdev is %f " % (r_OUT_IN_unw, s_OUT_IN_unw)
	#print "Degree assortativity IN-OUT unweighted TEST is %f " % (r_IN_OUT_unw2)

def degree_assortativity_statistical_significance_IN_IN_unw(G, threshold):
	r_IN_IN_unw = G.assortativity(directed=True,types1=G.degree(mode=IN, loops=False),types2=G.degree(mode=IN, loops=False))
	s_IN_IN_unw = jackknife_da_dir(G, r_IN_IN_unw, True, t1=IN, t2=IN)
	print "IN-IN unweighted is %f and expected stdev is %f " % (r_IN_IN_unw, s_IN_IN_unw)

def degree_assortativity_statistical_significance_OUT_OUT_unw(G, threshold):
	r_OUT_OUT_unw = G.assortativity(directed=True,types1=G.degree(mode=OUT, loops=False),types2=G.degree(mode=OUT, loops=False))
	s_OUT_OUT_unw = jackknife_da_dir(G, r_OUT_OUT_unw, True, t1=OUT, t2=OUT)
	print "OUT-OUT unweighted is %f and expected stdev is %f " % (r_OUT_OUT_unw, s_OUT_OUT_unw)

	##########################################################

	# UNDIR WEIGHTED SUM ALL
	# another copy of G
	#G_undir_weighted = G.copy()
	# this one is transformed to undirected with sum of all edges weight
	#G_undir_weighted.to_undirected(mode="collapse", combine_edges=sum)
	#r_UNDIR_WEIGHTED_all = G_undir_weighted.assortativity(directed=False, types1=G_undir_weighted.strength(weights='weight'))
	#print "Degree assortativity UNDIRECTED WEIGHTED (sum all) is %f " % (r_UNDIR_WEIGHTED_all)

def degree_assortativity_statistical_significance_IN_OUT(G, threshold):
	r_IN_OUT = G.assortativity(directed=True,types1=G.strength(weights='weight',mode=IN),types2=G.strength(weights='weight',mode=OUT))
	s_IN_OUT = jackknife_da_dir(G, r_IN_OUT, True, t1=IN, t2=OUT, weighted=True)
	print "Degree assortativity IN-OUT is %f and stdev %f  " % (r_IN_OUT, s_IN_OUT)

def degree_assortativity_statistical_significance_OUT_IN(G, threshold):
	r_OUT_IN = G.assortativity(directed=True,types1=G.strength(weights='weight',mode=OUT),types2=G.strength(weights='weight',mode=IN))
	s_OUT_IN = jackknife_da_dir(G, r_OUT_IN, True, t1=OUT, t2=IN, weighted=True)
	print "Degree assortativity OUT-IN is %f and stdev %f  " % (r_OUT_IN, s_OUT_IN)

def degree_assortativity_statistical_significance_IN_IN(G, threshold):
	r_IN_IN = G.assortativity(directed=True,types1=G.strength(weights='weight',mode=IN),types2=G.strength(weights='weight',mode=IN))
	s_IN_IN = jackknife_da_dir(G, r_IN_IN, True, t1=IN, t2=IN, weighted=True)
	print "Degree assortativity IN-IN is %f and stdev %f " % (r_IN_IN, s_IN_IN)

def degree_assortativity_statistical_significance_OUT_OUT(G, threshold):
	r_OUT_OUT = G.assortativity(directed=True,types1=G.strength(weights='weight',mode=OUT),types2=G.strength(weights='weight',mode=OUT))
	s_OUT_OUT = jackknife_da_dir(G, r_OUT_OUT, True, t1=OUT, t2=OUT, weighted=True)
	print "Degree assortativity OUT-OUT is %f and stdev %f " % (r_OUT_OUT, s_OUT_OUT)

	#return r_UNDIR_WEIGHTED_all, r_UNDIR_WEIGHTED_mutual, r_IN_OUT, r_OUT_IN, r_IN_IN, r_OUT_OUT


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
	G.simplify(loops=False, combine_edges='sum')
	summary(G)

	# UNDIRECTED COLLAPSED UNWEIGHTED
	# here we create a deep copy of G
	G_undir_unweighted = G.copy()
	# this copy is then transformed into single edges (no weight) undirected graph
	G_undir_unweighted.to_undirected(mode="collapse", combine_edges='ignore')
	r_UNDIR_UNW = G_undir_unweighted.assortativity_degree(directed=False)
	print "Degree assortativity UNDIRECTED UNWEIGHTED collapsed to 1 is %f " % (r_UNDIR_UNW)

	# UNDIRECTED MUTUAL UNWEIGHTED
	# here we create a deep copy of G
	G_undir_unweighted_mutual = G.copy()
	# this copy is then transformed into single edges (no weight) undirected graph
	G_undir_unweighted_mutual.to_undirected(mode="mutual", combine_edges='ignore')
	r_UNDIR_UNW_mutual = G_undir_unweighted_mutual.assortativity_degree(directed=False)
	print "Degree assortativity UNDIRECTED MUTUAL UNWEIGHTED %f " % (r_UNDIR_UNW_mutual)

	# DIRECTED UNWEIGHTED
	#r_UNW = G.assortativity_degree(directed=True)
	#print "Degree assortativity DIRECTED UNWEIGHTED is %f " % (r_UNW)

	# DIRECTED COLAPSED UNWEIGHTED -- THIS IS A CHECK
	G_dir_unweighted = G.copy()
	# this copy is then transformed into single edges (no weight) undirected graph
	G_dir_unweighted.simplify()
	#r_DIR_UNW = G_dir_unweighted.assortativity_degree(directed=True)
	#print "Degree assortativity DIRECTED UNWEIGHTED collapsed to 1 is %f " % (r_DIR_UNW)

	# DIRECTED COLAPSED UNWEIGHTED -- THIS IS A CHECK
	G_dir_unweighted2 = G.copy()
	# this copy is then transformed into single edges (no weight) undirected graph
	#G_dir_unweighted2.simplify(loops=False)
	#r_DIR_UNW2 = G_dir_unweighted2.assortativity_degree(directed=True)
	#print "Degree assortativity DIRECTED UNWEIGHTED loops false is %f " % (r_DIR_UNW2)
	# degree(vertices, mode=ALL, loops=True)

	r_IN_OUT_unw = G.assortativity(directed=True,types1=G.degree(mode=IN, loops=False),types2=G.degree(mode=OUT, loops=False))
	#s_IN_OUT_unw = jackknife_da_dir(G, r_IN_OUT_unw, True, t1=IN, t2=OUT)
	#print "Degree assortativity IN-OUT unweighted is %f and expected stdev %f " % (r_IN_OUT_unw, s_IN_OUT_unw)

	#r_IN_OUT_unw2 = G.assortativity(directed=True,types1=G.degree(mode=IN, loops=False),types2=G.degree(mode=OUT, loops=False))
	#s_IN_OUT_unw2 = jackknife_da_dir(G, r_IN_OUT_unw, True, t1=IN, t2=OUT)
	#print "Degree assortativity IN-OUT unweighted TEST is %f " % (r_IN_OUT_unw2)

	r_OUT_IN_unw = G.assortativity(directed=True,types1=G.degree(mode=OUT, loops=False),types2=G.degree(mode=IN, loops=False))
	#s_OUT_IN_unw = jackknife_da_dir(G, r_OUT_IN_unw, True, t1=OUT, t2=IN)
	#print "Degree assortativity OUT-IN unweighted is %f and expected stdev is %f " % (r_OUT_IN_unw, s_OUT_IN_unw)

	r_IN_IN_unw = G.assortativity(directed=True,types1=G.degree(mode=IN, loops=False),types2=G.degree(mode=IN, loops=False))
	#s_IN_IN_unw = jackknife_da_dir(G, r_IN_IN_unw, True, t1=IN, t2=IN)
	#print "Degree assortativity IN-IN unweighted is %f and expected stdev is %f " % (r_IN_IN_unw, s_IN_IN_unw)

	r_OUT_OUT_unw = G.assortativity(directed=True,types1=G.degree(mode=OUT, loops=False),types2=G.degree(mode=OUT, loops=False))
	#s_OUT_OUT_unw = jackknife_da_dir(G, r_OUT_OUT_unw, True, t1=OUT, t2=OUT)
	#print "Degree assortativity OUT-OUT unweighted is %f and expected stdev is %f " % (r_OUT_OUT_unw, s_OUT_OUT_unw)

	##########################################################

	# UNDIR WEIGHTED SUM ALL
	# another copy of G
	G_undir_weighted = G.copy()
	# this one is transformed to undirected with sum of all edges weight
	G_undir_weighted.to_undirected(mode="collapse", combine_edges=sum)
	r_UNDIR_WEIGHTED_all = G_undir_weighted.assortativity(directed=False, types1=G_undir_weighted.strength(weights='weight'))
	print "Degree assortativity UNDIRECTED WEIGHTED (sum all) is %f " % (r_UNDIR_WEIGHTED_all)

	# UNDIR WEIGHTED SUM MUTUAL
	# and one more copy
	G_undir_weighted = G.copy()
	# this one is undirected weighted having the weight of only mutual communication
	G_undir_weighted.to_undirected(mode="mutual", combine_edges=sum)
	r_UNDIR_WEIGHTED_mutual = G_undir_weighted.assortativity(directed=False, types1=G_undir_weighted.strength(weights='weight'))
	print "Degree assortativity UNDIRECTED WEIGHTED (sum mutual) is %f " % (r_UNDIR_WEIGHTED_mutual)

	r_IN_OUT = G.assortativity(directed=True,types1=G.strength(weights='weight',mode=IN),types2=G.strength(weights='weight',mode=OUT))
	print "Degree assortativity IN-OUT is %f " % (r_IN_OUT)
	r_OUT_IN = G.assortativity(directed=True,types1=G.strength(weights='weight',mode=OUT),types2=G.strength(weights='weight',mode=IN))
	print "Degree assortativity OUT-IN is %f " % (r_OUT_IN)
	r_IN_IN = G.assortativity(directed=True,types1=G.strength(weights='weight',mode=IN),types2=G.strength(weights='weight',mode=IN))
	print "Degree assortativity IN-IN is %f " % (r_IN_IN)
	r_OUT_OUT = G.assortativity(directed=True,types1=G.strength(weights='weight',mode=OUT),types2=G.strength(weights='weight',mode=OUT))
	print "Degree assortativity OUT-OUT is %f " % (r_OUT_OUT)

	return r_UNDIR_WEIGHTED_all, r_UNDIR_WEIGHTED_mutual, r_IN_OUT, r_OUT_IN, r_IN_IN, r_OUT_OUT

def plot_DA(xaxis, da, img_out, lab="", col ="g"):
	x = np.array(xaxis)
	y = np.array(da)
	fig = plt.gcf()
	fig.set_size_inches(8.3,6.5)
	plt.plot(x, y, col, label=lab, hold=True)
	plt.grid(False)
	#plt.title('Convolution mention with SR network')
	plt.ylabel('weighted degree assortativity')
	plt.xlabel('min communication intensity (# of mentions)')
	#leg = plt.legend(bbox_to_anchor=(0.152, 1.152),frameon=True)
	# Place a legend above this legend, expanding itself to
	# fully use the given bounding box.
	leg = plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
	#leg.get_frame().set_linewidth(0.0)
	#leg.get_frame().set_edgecolor('gray')
	#plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
	#       ncol=2, mode="expand", borderaxespad=0.)
	#plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
	#plt.tight_layout()
	plt.savefig(img_out, bbox_extra_artists=(leg,), \
		bbox_inches='tight',format='eps',dpi=440)
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
	da_UNDIR_weighted_all = []
	da_UNDIR_WEIGHTED_mutual = []
	da_DEFAULT = []
	da_IN_OUT = []
	da_OUT_IN = []
	da_IN_IN = []
	da_OUT_OUT = []
	xaxis =  []
	
	G = read_in_graph()

	#f_UNW = open(f_out_plot_res, "w")
	for threshold in np.arange(0, 300, 1):
		r_UNDIR_WEIGHTED_all, r_UNDIR_WEIGHTED_mutual, r_IN_OUT, r_OUT_IN, r_IN_IN, r_OUT_OUT \
		= degree_assortativity_complex(G, threshold)
		da_UNDIR_weighted_all.append(r_UNDIR_WEIGHTED_all)
		da_UNDIR_WEIGHTED_mutual.append(r_UNDIR_WEIGHTED_mutual)
		#da_DEFAULT.append(r_DEFAULT)
		da_IN_OUT.append(r_IN_OUT)
		da_OUT_IN.append(r_OUT_IN)
		da_IN_IN.append(r_IN_IN)
		da_OUT_OUT.append(r_OUT_OUT)
		xaxis.append(threshold)
		#f_UNW.write(str(threshold) + '\t'+ str(s) + '\n')

	plot_DA(xaxis, da_UNDIR_weighted_all, img_out_plot_UNDIR_W_all, "undir all", col ="r-")
	plot_DA(xaxis, da_UNDIR_WEIGHTED_mutual, img_out_plot_UNDIR_W_mutual, "undir mutual", col ="c-")
	plot_DA(xaxis, da_IN_OUT, img_out_plot_IN_OUT, "in_out", col="g.")
	plot_DA(xaxis, da_OUT_IN, img_out_plot_OUT_IN, "out_in", col="b.")
	plot_DA(xaxis, da_IN_IN, img_out_plot_IN_IN , "in_in", col="m.")
	plot_DA(xaxis, da_OUT_OUT, img_out_plot_OUT_OUT, "out_out", col="y.")

main_complex()
#main()
#randomize()

def main_statistical_significance():
	os.chdir(IN_DIR)
	G = read_in_graph()
	print 'stats of the network '
	summary(G)
	#to_delete_edges = [e.index for e in G.es if int(e["weight"]) <= threshold]
	#G.delete_edges(to_delete_edges)
	# just a check
	#not_connected_nodes = G.vs(_degree_eq=0)
	#print len(not_connected_nodes)
	print 'stats of the network after simplification '
	G.simplify(loops=False, combine_edges='sum')
	summary(G)

	for threshold in np.arange(0, 1, 1):
		#degree_assortativity_statistical_significance_undir_weighted(G, threshold)
		#degree_assortativity_statistical_significance_undir_mutual(G, threshold)
		#degree_assortativity_statistical_significance_undir_unw(G, threshold)
		#degree_assortativity_statistical_significance_undir_colapsed_weighted(G, threshold)
		#
		#degree_assortativity_statistical_significance_OUT_OUT_unw(G, threshold)
		degree_assortativity_statistical_significance_IN_IN_unw(G, threshold)
		#degree_assortativity_statistical_significance_IN_OUT_unw(G, threshold)
		#degree_assortativity_statistical_significance_OUT_IN_unw(G, threshold)
		#
		#degree_assortativity_statistical_significance_OUT_OUT(G, threshold)
		#degree_assortativity_statistical_significance_IN_IN(G, threshold)
		#degree_assortativity_statistical_significance_IN_OUT(G, threshold)
		#degree_assortativity_statistical_significance_OUT_IN(G, threshold)		

#main_statistical_significance()