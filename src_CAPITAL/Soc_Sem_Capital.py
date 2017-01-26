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

font = {'family' : 'sans-serif',
		'variant' : 'normal',
		'weight' : 'light',
		'size'   : 14}

matplotlib.rc('font', **font)

f_in_user_labels = "usr_num_CVs.tab"
##################
f_in_user_taxons = "user_taxons.tab"
f_in_user_concepts = "user_concepts.tab"
f_in_user_entities = "user_entities.tab"
f_in_num_tweets = "usr_num_tweets.tab"
#########################
#
f_in_user_sentiment = "user_sentiment.tab"
#
# mention graph
#########################
f_in_graph = "threshold_mention_graphs/directed_threshold0.tab"
f_in_graph_weights = "threshold_mention_graphs/mention_graph_weights.dat"
f_out_sent_mention_graph = "directed_threshold0_sent_val.tab"
IN_DIR = "../../../DATA/mention_graph/"
f_out_mention = "sentiment_assortativity_mention_2.txt"
#########################





def social_capital_vs_sentiment():
	os.chdir(IN_DIR)
	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	f = open(f_in_user_sentiment, "r")

	soc_cap = []
	soc_cap_int = []
	sem_cap = []

	ierror = 0

	cnt = 0
	for line in f:
		(vid, vn, val) = line.split('\t')
		val = float(val)
		v = G.vs.select(name = vid)
		cnt += 1
		v["val"] = val
		try:
			d = G.degree(v[0].index)
			wd = G.strength(v[0].index, weights='weight')
			if d < 1000:
				soc_cap.append(d) 
				soc_cap_int.append(wd)
				sem_cap.append(val)
		except IndexError:
				ierror += 1


	print cnt, ierror

	to_delete_vertices = [v.index for v in G.vs if v["val"] == None]
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	#print "Sent nominal assortativity is %f " %  (G.assortativity_nominal(types="val",directed=True))
	print "Sent assortativity is %f " %  (G.assortativity("val",directed=True))
	print "Sent assortativity UNDIR is %f " %  (G.assortativity("val",directed=False))

	plot_capitals(soc_cap, sem_cap)
	plot_capitals(soc_cap_int, sem_cap)


def social_capital_vs_CVs():
	os.chdir(IN_DIR)
	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	f = open(f_in_user_labels, "r")

	soc_cap = []
	soc_cap_int = []
	sem_cap = []

	CAPs_vol = defaultdict(int)

	ierror = 0

	cnt = 0
	for line in f:
		(vid, val) = line.split('\t')
		val = int(val)
		v = G.vs.select(name = vid)
		cnt += 1
		v["val"] = val
		try:
			d = G.degree(v[0].index)
			wd = G.strength(v[0].index, weights='weight')
			if d < 1000:
				soc_cap.append(d) 
				soc_cap_int.append(wd)
				sem_cap.append(val)
		except IndexError:
				ierror += 1

	print cnt, ierror

	to_delete_vertices = [v.index for v in G.vs if v["val"] == None]
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)


	plot_capitals(soc_cap, sem_cap)
	plot_capitals(soc_cap_int, sem_cap)


def social_capital_vs_concepts():
	os.chdir(IN_DIR)
	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	f = open(f_in_user_concepts, "r")

	soc_cap = []
	soc_cap_int = []
	sem_cap = []

	ierror = 0

	cnt = 0
	for line in f:
		(vid, val) = line.split('\t')
		val = int(val)
		v = G.vs.select(name = vid)
		cnt += 1
		v["val"] = val
		try:
			d = G.degree(v[0].index, mode=IN)
			wd = G.strength(v[0].index, weights='weight', mode=IN)
			if d < 1000:
				soc_cap.append(d) 
				soc_cap_int.append(wd)
				sem_cap.append(val)
		except IndexError:
				ierror += 1


	print cnt, ierror

	to_delete_vertices = [v.index for v in G.vs if v["val"] == None]
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	print "CV nominal assortativity is %f " %  (G.assortativity_nominal(types="val",directed=True))
	print "CV assortativity is %f " %  (G.assortativity("val",directed=True))
	print "CV assortativity UNDIR is %f " %  (G.assortativity("val",directed=False))

	plot_capitals(soc_cap, sem_cap)
	plot_capitals(soc_cap_int, sem_cap)

def social_capital_vs_entities():
	os.chdir(IN_DIR)
	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	f = open(f_in_user_entities, "r")

	soc_cap = []
	soc_cap_int = []
	sem_cap = []

	ierror = 0

	cnt = 0
	for line in f:
		(vid, val) = line.split('\t')
		val = int(val)
		v = G.vs.select(name = vid)
		cnt += 1
		v["val"] = val
		try:
			d = G.degree(v[0].index)
			wd = G.strength(v[0].index, weights='weight')
			if d < 1000:
				soc_cap.append(d) 
				soc_cap_int.append(wd)
				sem_cap.append(val)
		except IndexError:
				ierror += 1


	print cnt, ierror

	to_delete_vertices = [v.index for v in G.vs if v["val"] == None]
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	print "CV nominal assortativity is %f " %  (G.assortativity_nominal(types="val",directed=True))
	print "CV assortativity is %f " %  (G.assortativity("val",directed=True))
	print "CV assortativity UNDIR is %f " %  (G.assortativity("val",directed=False))

	plot_capitals(soc_cap, sem_cap)
	plot_capitals(soc_cap_int, sem_cap)


def plot_capitals(x, y):
	plt.scatter(x,y,color='darkorchid')
	plt.show()

#social_capital_vs_CVs()

#social_capital_vs_concepts()

#social_capital_vs_entities()

social_capital_vs_sentiment()