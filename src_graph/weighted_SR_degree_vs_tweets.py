#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	analyze hubs of SR networks
'''
from igraph import *
import codecs
import os
import networkx as nx
from collections import defaultdict, OrderedDict
import numpy as np
import matplotlib.pyplot as plt

IN_DIR = "../../../DATA/SR_graphs"
#########################################################

#########################
#f_in_graph_SR_weights = "ALL_SR.weighted_edge_list"
f_in_graph_SR_weights = "filter_IDs_SR_0.6" 
f_out_graph = "0.6_node_weighted_degree.tab"
#f_out_graph_nx = "nx_node_weighted_degree.tab"
#########################



def read_in_weighted_SR_graph():
	G=Graph.Read_Ncol(f_in_graph_SR_weights,names=True,directed=False, weights=True)

	summary(G)
	return G

def read_nx_g():
	G2 = nx.read_edgelist(f_in_graph_SR_weights,nodetype=int,data=(('weight',float),),create_using=nx.DiGraph())
	return G2

def save_nodes_weighted_degree():
	G = read_in_weighted_SR_graph()
	#s = G.strength(G.vs,weights='weight',loops=False)
	f = open(f_out_graph, 'w')
	for el in G.vs:
		f.write(str(el["name"]) + '\t' + str(G.strength(el.index,weights='weight')) + '\n')

def save_nx_weighted_degree():
	G = read_nx_g()
	f = open(f_out_graph_nx, 'w')
	for el in G.nodes_iter():
		f.write(str(el) + '\t' + str(G.degree(el, weight='weight')) + '\n')

def plot_weighted_SR_deg_vs_tweets():
	f1_in = "node_weighted_degree_SR_0.6.tab"
	f2_in = "usr_num_tweets.tab"

	fig_name = "weighted_deg_vs_tweets.0.6_loglog.png"

	weighted_deg = defaultdict(int)
	f1 = open(f1_in, "r")
	for line in f1:
		line = line.split()
		uid = line[0]
		wd = float(line[1])
		weighted_deg[uid] = wd

	print max(weighted_deg.values())

	usr_tweets = defaultdict(int)
	f2 = open(f2_in, "r")
	for line in f2:
		line = line.split()
		uid = line[0]
		tw = int(line[1])
		usr_tweets[uid] = tw
	
	data = defaultdict(int)
	for uid in usr_tweets:
		data[usr_tweets[uid]] = weighted_deg[uid]

	D = OrderedDict(sorted(data.items(), key=lambda x: x[0], reverse=False))

	N = len(D)
	x = np.array(D.keys())
	y = np.array(D.values())
	plt.loglog(x, y, "*g", label="# tweets vs. degree")
	plt.grid(True)
	plt.title('')
	plt.legend()
	plt.savefig(fig_name,format='png',dpi=440)

def plot_weighted_SR_deg_vs_tweets_Igor():
	f1_in = "wcentrality_0.6.wdeg"
	f2_in = "usr_num_tweets.tab"

	fig_name = "I_weighted_deg_vs_tweets.0.6_loglog.png"
	fig2_name = "I_weighted_deg_vs_tweets.0.6.png"

	weighted_deg = defaultdict(int)
	f1 = open(f1_in, "r")
	f1.readline()
	f1.readline()
	f1.readline()
	for line in f1:
		line = line.split()
		uid = line[0]
		wd = float(line[3])
		weighted_deg[uid] = wd

	print max(weighted_deg.values())

	usr_tweets = defaultdict(int)
	f2 = open(f2_in, "r")
	for line in f2:
		line = line.split()
		uid = line[0]
		tw = int(line[1])
		usr_tweets[uid] = tw
	
	data = defaultdict(int)
	for uid in usr_tweets:
		data[usr_tweets[uid]] = weighted_deg[uid]

	D = OrderedDict(sorted(data.items(), key=lambda x: x[0], reverse=False))
	N = len(D)
	x = np.array(D.keys())
	y = np.array(D.values())
	# v1
	plt.loglog(x, y, "*g", label="# tweets vs. degree")
	plt.grid(True)
	plt.title('')
	plt.legend()
	plt.savefig(fig_name,format='png',dpi=440)
	# v2
	plt.clf()
	plt.plot(x, y, "*g", label="# tweets vs. degree")
	plt.grid(True)
	plt.title('')
	plt.legend()
	plt.savefig(fig2_name,format='png',dpi=440)

def main():

	os.chdir(IN_DIR)
	#save_nodes_weighted_degree()
	#save_nx_weighted_degree()

	#
	# call us after the others
	#
	#plot_weighted_SR_deg_vs_tweets()

	plot_weighted_SR_deg_vs_tweets_Igor()

main()