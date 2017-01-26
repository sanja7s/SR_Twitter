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

import seaborn as sns
sns.set(color_codes=True)

sns.set(font_scale=2) 

from scipy.stats.stats import pearsonr

font = {'family' : 'sans-serif',
		'variant' : 'normal',
		'weight' : 'light',
		'size'   : 20}

matplotlib.rc('font', **font)

f_in_user_labels = "usr_num_CVs.tab"
##################
f_in_user_taxons = "user_taxons.tab"
f_in_user_concepts = "user_concepts.tab"
f_in_user_entities = "user_entities.tab"
#########################
#
f_in_user_sentiment = "user_sentiment.tab"
#
# mention graph
#########################
f_in_graph_weights = "mention_graph_weights.dat"
########################
IN_DIR = "../../../DATA/CAPITAL/"
os.chdir(IN_DIR)
	
def read_node_inconsistency_2graph(filename='status_inconsistency'):
	print 'Reading in inconsistency node attributes to G '
	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)
	f = open(filename, "r")

	for line in f:
		(vid, val) = line.split('\t')
		val = float(val)
		v = G.vs.select(name = vid)
		v["att"] = val

	to_delete_vertices = [v.index for v in G.vs if v["att"] == None]
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)	
	return G

def read_in_edge_weight_SR(file_name= 'undirected_mention_graph_with_SR_weight.dat'):
	f = open(file_name, 'r')
	s = defaultdict(float)
	for line in f:
		(u1, u2, ew, eSR) = line.split('\t')
		s[float(ew)] = float(eSR)
	return s


def read_in_edge_weight_inconsistency(file_name= 'weight_inconsistency_on_edge_float.dat'):
	f = open(file_name, 'r')
	s = defaultdict(float)
	for line in f:
		(ew, einc) = line.split('\t')
		s[float(ew)] = float(einc)
	return s

def plot_edge_weight_vs_SR():
	s = read_in_edge_weight_SR()

	w = []
	inc = []
	
	for el in s:
		# weight
		w.append(el)
		# inconsistency
		einc = s[el]
		inc.append(einc)

	w=np.array(w)
	inc=np.array(inc)
	print np.corrcoef(w,inc)

	print pearsonr(w, inc)

	ylabel = 'communication intensity'
	xlabel = 'edge SR'

	plt.clf()
	with sns.axes_style("white"):
		g = sns.jointplot(x=inc, y=w, kind="scatter", color="yellow", xlim=(-0.07,1.07)).set_axis_labels(xlabel, ylabel)

	#plt.tight_layout()
	
	#plt.grid(True)
	plt.savefig( 'undir_edge_weight_vs_SR_scatter.eps', dpi=500, bbox_inches='tight')


"""
	Not to do now
"""
def corr_edge_incon_SR():

	SR1 = read_in_edge_weight_SR()
	inc1 = read_in_edge_weight_inconsistency()

	SR=np.array(SR)
	inc=np.array(inc)
	print np.corrcoef(SR,inc)

#plot_edge_weight_vs_SR()
