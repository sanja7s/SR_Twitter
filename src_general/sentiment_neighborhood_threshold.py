#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import matplotlib
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os
import matplotlib.cm as cm
from collections import defaultdict
from igraph import *

font = {'family' : 'monospace',
		'variant' : 'normal',
        'weight' : 'light',
        'size'   : 7}

matplotlib.rc('font', **font)

IN_DIR = "../../../DATA/taxonomy_stats/"
f_sent_in = "sentiment/user_sentiment.tab"
f_weighted_edges_in = "sentiment/mention_graph_weights.dat"

def read_in_recip():

	f = open(f_sent_in, "r")
	G = Graph.Read_Ncol(f_weighted_edges_in,names=True, directed=True, weights=True)
	summary(G)
	G.to_undirected(mode="mutual", combine_edges=min)
	summary(G)

	G.simplify(multiple=False, loops=True)
	summary(G)

	cnt = 0
	for line in f:
		(vid, vsent, vsentval) = line[:-1].split('\t')
		vsentval = float(vsentval)
		v = G.vs.select(name = vid)
		v["sent"] = vsentval
		cnt += 1
	print cnt

	to_delete_vertices = [v.index for v in G.vs if v["sent"] == None]
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	return G

#########################################################################
def pairwise_assortativity(G):

	sa = []
	ne = []
	xaxis = []
	f = open('sentiment/pairwise_assortativity.tab', 'w')

	for threshold in np.arange(1, 25):
		s, n = threshold_pairwise_assortativity(G, threshold)
		sa.append(s)
		ne.append(n)
		xaxis.append(threshold)
		f.write(str(threshold) + '\t' + str(s) + '\t' + str(n) + '\n')
	
	#plot_SA(xaxis, sa, ne, 'pairwise_assortativity_v4.png')
	return xaxis, sa, ne

def threshold_pairwise_assortativity(G, threshold):

	print "stats for %d" % threshold
	summary(G)
	to_delete_edges = [e.index for e in G.es if float(e["weight"]) <= threshold]
	G.delete_edges(to_delete_edges)
	# just a check
	not_connected_nodes = G.vs(_degree_eq=0)
	print len(not_connected_nodes)
	G.delete_vertices(not_connected_nodes)
	summary(G)

	#r = G.assortativity(directed=False,types1=G.strength(weights='weight'))
	r = G.assortativity("sent", directed=False)

	print "Sentmiment value assortativity for threshold %d is %f " % (threshold, r)
	N = G.ecount() # - len(not_connected_nodes)
	return r, N

def plot_SA(xaxis, sa, ne, img_out_plot):
	
	x = np.array(xaxis)
	y = np.array(sa)
	y1 = np.log(np.array(ne))

	fig, ax1 = plt.subplots()
	ax1.plot(x, y, 'cp-')
	ax1.set_xlabel('# mention threshold')
	# Make the y-axis label and tick labels match the line color.
	ax1.set_ylabel('pairwise assortativity', color='c')
	for tl in ax1.get_yticklabels():
	    tl.set_color('c')

	ax2 = ax1.twinx()
	ax2.plot(x, y1, 'rd-')
	ax2.set_ylabel('log(# edges)', color='r')
	#ax2.set_yscale("log")
	for tl in ax2.get_yticklabels():
	    tl.set_color('r')

	plt.grid(True)
	plt.title('Sentiment pairwise assortativity')
	#plt.legend(bbox_to_anchor=(0, 1), bbox_transform=plt.gcf().transFigure)

	plt.savefig('sentiment/' + img_out_plot,format='png',dpi=200)

#########################################################################
def neighborhood_assortativity(G):

	sa = []
	ne = []
	xaxis = []
	f = open('sentiment/neighborhood/neighborhood_assortativity.tab', 'w')

	for threshold in np.arange(1, 25):
		s, n = threshold_neighborhood_assortativity(G, threshold)
		sa.append(s)
		ne.append(n)
		xaxis.append(threshold)
		f.write(str(threshold) + '\t' + str(s) + '\t' + str(n) + '\n')
	
	#plot_SA_neighborhood(xaxis, sa, ne, 'neighborhood_assortativity_v2.png')
	return xaxis, sa, ne

def threshold_neighborhood_assortativity(G, threshold):

	print "stats for %d" % threshold
	summary(G)
	to_delete_edges = [e.index for e in G.es if float(e["weight"]) <= threshold]
	G.delete_edges(to_delete_edges)
	# just a check
	not_connected_nodes = G.vs(_degree_eq=0)
	print len(not_connected_nodes)
	G.delete_vertices(not_connected_nodes)
	summary(G)

	neighborhood_sent = []
	self_sent = []
	no_neighbors = []
	cnt_no_neighbors = 0
	for v in G.vs:
		nb = G.neighbors(v.index)
		NS = G.vs.select(nb)["sent"]
		if NS == []:
			cnt_no_neighbors += 1
			print v.index, nb
			no_neighbors.append(v.index)
			continue
		ns = np.array(NS)
		ns_mean = np.average(ns)
		self_sent.append(v["sent"])
		neighborhood_sent.append(ns_mean)
	print cnt_no_neighbors

	neighborhood_sent = np.array(neighborhood_sent)
	self_sent = np.array(self_sent)

	return np.corrcoef(self_sent, neighborhood_sent)[1,0], neighborhood_sent.size

def plot_SA_neighborhood(xaxis, sa, ne, img_out_plot):
	
	x = np.array(xaxis)
	y = np.array(sa)
	y1 = np.log(np.array(ne))

	fig, ax1 = plt.subplots()
	ax1.plot(x, y, 'gp-')
	ax1.set_xlabel('# mention threshold')
	# Make the y-axis label and tick labels match the line color.
	ax1.set_ylabel('neighborhood assortativity', color='g')
	for tl in ax1.get_yticklabels():
	    tl.set_color('g')

	ax2 = ax1.twinx()
	ax2.plot(x, y1, 'md-')
	ax2.set_ylabel('log(# edges)', color='m')
	#ax2.set_yscale("log", nonposy='clip')
	for tl in ax2.get_yticklabels():
	    tl.set_color('m')

	plt.grid(True)
	plt.title('Sentiment neighborhood assortativity')
	#plt.legend(bbox_to_anchor=(0, 1), bbox_transform=plt.gcf().transFigure)

	plt.savefig('sentiment/neighborhood/' + img_out_plot,format='png',dpi=200)
#########################################################################

def plot_SA_both(xaxis, sa, ne, nsa, nne, img_out_plot):
	
	x = np.array(xaxis)
	y = np.array(sa)
	y1 = np.log(np.array(ne))

	yn = np.array(nsa)
	yn1 = np.log(np.array(nne))

	fig, ax1 = plt.subplots()
	ax1.plot(x, y, 'gp-', label='pairwise assortativity')
	ax1.plot(x, yn, 'gd-', label='neighborhood assortativity')
	ax1.set_xlabel('# mention threshold')
	# Make the y-axis label and tick labels match the line color.
	ax1.set_ylabel('assortativity', color='g')
	for tl in ax1.get_yticklabels():
	    tl.set_color('g')

	plt.legend()

	ax2 = ax1.twinx()
	ax2.plot(x, y1, 'mp-', label='# edges (pairwise)')
	ax2.plot(x, yn1, 'md-', label='# edges (neighborhood)')
	ax2.set_ylabel('log(# edges)', color='m')
	#ax2.set_yscale("log", nonposy='clip')
	for tl in ax2.get_yticklabels():
	    tl.set_color('m')

	plt.legend(loc=2)
	plt.grid(True)
	plt.title('Sentiment parwise and neighborhood assortativity')
	#plt.legend(bbox_to_anchor=(0, 1), bbox_transform=plt.gcf().transFigure)

	plt.savefig('sentiment/both/' + img_out_plot,format='png',dpi=200)

def main_pairwise():
	os.chdir(IN_DIR)
	G = read_in_recip()
	pairwise_assortativity(G) 
#main_pairwise()

def main_neighborhood():
	os.chdir(IN_DIR)
	G = read_in_recip()
	neighborhood_assortativity(G) 
#main_neighborhood()

def main():
	os.chdir(IN_DIR)

	G = read_in_recip()
	xaxis, sa, ne = pairwise_assortativity(G)

	G = read_in_recip()
	nxaxis, nsa, nne = neighborhood_assortativity(G) 

	plot_SA_both(xaxis, sa, ne, nsa, nne, 'sentimen_assortativity_v3.png')

main()