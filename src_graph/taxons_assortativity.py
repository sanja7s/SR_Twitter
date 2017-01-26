#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	analyze assortativity of the graphs in terms of sentiment
'''
from igraph import *
import networkx as nx
import os
import random

f_in_user_taxons = "user_taxons.tab"
f_in_user_concepts = "user_concepts.tab"
f_in_user_entities = "user_entities.tab"
f_in_num_tweets = "usr_num_tweets.tab"
#########################
# mention graph
#########################
f_in_graph = "threshold_mention_graphs/directed_threshold0.tab"
f_in_graph_weights = "threshold_mention_graphs/mention_graph_weights.dat"
IN_DIR = "../../../DATA/mention_graph/"
#########################

#########################
# SR
#########################
X = "8"
f_in_graph_SR = "threshold_graphs/undir_threshold" + str(X) + ".tab"
f_in_graph_SR_weights = "filter_IDs_SR_0." + str(X)
#f_out_sent_SR_graph = "../../Gephi/SR/gephi_undir_threshold" + str(X) + "_edge_list.tab"
IN_DIR_SR = "../../../DATA/SR_graphs/"
f_out_SR = "sentiment_assortativity_SR"  + str(X) + ".txt"
#########################


def jackknife_dir(G, r):
	ri = []
	G1 = G.copy()
	print len(G.es)
	i = 0
	for e in G.es:
		G1.delete_edges((e.source, e.target))

		r1 = G1.assortativity("att",directed=True)

		ri.append(r1)
		if i%1000==0:
			print i, r1
		i += 1

		G1.add_edge(e.source, e.target)
	s = 0.0
	for r1 in ri:
		s += (r1-r)*(r1-r)
	return math.sqrt(s)

def jackknife_undir(G, r):
	ri = []
	G1 = G.copy()
	print len(G.es)
	i = 0
	for e in G.es:
		G1.delete_edges((e.source, e.target))

		r1 = G1.assortativity("att",directed=False)

		ri.append(r1)
		if i%1000==0:
			print i, r1
		i += 1

		G1.add_edge(e.source, e.target)
	s = 0.0
	for r1 in ri:
		s += (r1-r)*(r1-r)
	return math.sqrt(s)

def mention_igraph_assortativity(filename):
	os.chdir(IN_DIR)
	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	f = open(filename, "r")

	for line in f:
		(vid, val) = line.split('\t')
		val = int(val)
		v = G.vs.select(name = vid)
		v["att"] = val

	to_delete_vertices = [v.index for v in G.vs if v["att"] == None]
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	#print "nominal assortativity is %f " %  (G.assortativity_nominal(types="att",directed=True))
	#print "label assortativity is %f " %  (G.assortativity(types1="att",types2="att",directed=True))
	print "label assortativity is %f " %  (G.assortativity("att",directed=True))

	r = G.assortativity("att",directed=True)
	s = jackknife_dir(G, r)
	print filename + " DIR assortativity is %f and st. sign. is %f " % (r, s)

	###########################################

	G.to_undirected(mode='mutual')

	not_connected_nodes = G.vs(_degree_eq=0)

	to_delete_vertices = not_connected_nodes
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	r = G.assortativity("att",directed=False)
	s = jackknife_undir(G, r)
	print filename + " MUTUAL assortativity is %f and st. sign. is %f " % (r, s)

def mention_igraph_assortativity_randomize(filename):
	os.chdir(IN_DIR)
	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	#print "Randomize vertices"
	#s = G.vs["name"]
	#random.shuffle(s)
	#G.vs["name"] = s
	#summary(G)

	f = open(filename, "r")
	for line in f:
		(vid, val) = line.split('\t')
		val = int(val)
		v = G.vs.select(name = vid)
		v["att"] = val

	print "Randomize attr labels"
	s = G.vs["att"]
	random.shuffle(s)
	G.vs["att"] = s
	summary(G)

	to_delete_vertices = [v.index for v in G.vs if v["att"] == None]
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	#print "nominal assortativity is %f " %  (G.assortativity_nominal(types="att",directed=True))
	#print "label assortativity is %f " %  (G.assortativity(types1="att",types2="att",directed=True))
	print "label assortativity is %f " %  (G.assortativity("att",directed=True))

	

def testing_mention_igraph_assortativity(filename):
	os.chdir(IN_DIR)
	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	f = open(filename, "r")

	ierror = 0

	for line in f:
		(vid, val) = line.split('\t')
		val = int(val)
		v = G.vs.select(name = vid)
		v["att"] = val
		try:
			d = G.degree(v[0].index)
			d_out = G.degree(v[0].index,mode=OUT, loops=False)
			wd = G.strength(v[0].index, weights='weight')
			wd_out = G.strength(v[0].index, weights='weight',mode=OUT, loops=False)
			print val, d, wd, d_out, wd_out
		except IndexError:
				ierror += 1

	print 'skipped nodes ', ierror

	to_delete_vertices = [v.index for v in G.vs if v["att"] == None]
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	print "nominal assortativity is %f " %  (G.assortativity_nominal(types="att",directed=True))
	print "label assortativity is %f " %  (G.assortativity(types1="att",types2="att",directed=True))
	print "label assortativity is %f " %  (G.assortativity("att",directed=True))
	# testing
	print "OUT-OUT degree assortativity is %f " %  (G.assortativity(types1=G.degree(mode=OUT, loops=False),types2=G.degree(mode=OUT, loops=False),directed=True))

def mention_nx_assortativity():
	os.chdir(IN_DIR)

	MENT=nx.read_edgelist(f_in_graph_weights, create_using=nx.DiGraph(), data=(('weight',int),))
	print(len(MENT.nodes(data=True)))

	cnt = 0
	d=defaultdict(int)
	d_val = defaultdict(int)
	d1 = defaultdict(int)
	with open(f_in_user_sentiment) as f:
	    for line in f:
	        (uid, label, val) = line.split()
	        uid = unicode(uid)
	        d1[uid]= int(float(val)*10000)
	        if uid in MENT.nodes():
	        	d[uid]= int(float(val)*10000)
	        	d_val[uid] = int(label)
	        else:
	        	cnt += 1
	print "Number of nodes for which we have sentminet but are not in the mention graph is ", cnt

	cnt = 0
	for node in MENT.nodes():
		if not node in d1:
			cnt += 1
			MENT.remove_node(node)
	print "Number of nodes that do not have sentminet value, so we remove them from the mention graph", cnt

	nx.set_node_attributes(MENT, 'sentiment' , d)
	nx.set_node_attributes(MENT, 'sentiment_val' , d_val)
	print "Final number of nodes in the graph ", (len(MENT.nodes(data=True)))
	print "Sentiment (by label) nominal numeric assortativity is %f " % nx.numeric_assortativity_coefficient(MENT, 'sentiment')
	print "Sentiment (by value) numeric assortativity is %f " % nx.numeric_assortativity_coefficient(MENT, 'sentiment_val')

def SR_igraph_assortativity(filename):
	os.chdir(IN_DIR_SR)

	G = Graph.Read_Ncol(f_in_graph_SR_weights,names=True, directed=False, weights=True)
	summary(G)

	f = open(filename, "r")
	for line in f:
		(vid, val) = line.split('\t')
		val = int(val)
		v = G.vs.select(name = vid)
		v["att"] = val


	to_delete_vertices = [v.index for v in G.vs if v["att"] == None]
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	print "nominal assortativity is %f " %  (G.assortativity_nominal(types="att",directed=False))
	print "label assortativity is %f " %  (G.assortativity("att",directed=False))

def SR_nx_assortativity():
	#os.chdir("SR_graphs")
	os.chdir(IN_DIR_SR)

	SR=nx.read_edgelist(f_in_graph_SR, create_using=nx.Graph()) #, data=(('weight',int),))
	print(len(SR.nodes(data=True)))

	print "Degree assortativity of UNWEIGHTED is %f " % nx.degree_assortativity_coefficient(SR)
	#print "Sentiment (by value) numeric assortativity is %f " % nx.numeric_assortativity_coefficient(MENT, 'sentiment_val')


	SR=nx.read_edgelist(f_in_graph_SR, create_using=nx.Graph(), data=(('weight',int),))
	print(len(SR.nodes(data=True)))
	print "Degree assortativity of WEIGHTED is %f " % nx.degree_assortativity_coefficient(SR, weight='weight')

	cnt = 0
	d=defaultdict(int)
	d_val = defaultdict(int)
	d1 = defaultdict(int)
	with open(f_in_user_sentiment) as f:
	    for line in f:
	        (uid, label, val) = line.split()
	        uid = unicode(uid)
	        d1[uid]= int(float(val)*10000)
	        if uid in SR.nodes():
	        	d[uid]= int(float(val)*10000)
	        	d_val[uid] = int(label)
	        else:
	        	cnt += 1
	print "Number of nodes for which we have sentminet but are not in the mention graph is ", cnt
	cnt = 0
	for node in SR.nodes():
		if not node in d1:
			cnt += 1
			SR.remove_node(node)
	print "Number of nodes that do not have sentiment value, so we remove them from the mention graph", cnt
	nx.set_node_attributes(SR, 'sentiment' , d)
	nx.set_node_attributes(SR, 'sentiment_val' , d_val)
	print "Final number of nodes in the graph ", (len(SR.nodes(data=True)))

	print "Sentiment (by label) nominal numeric assortativity is %f " % nx.numeric_assortativity_coefficient(SR, 'sentiment')
	print "Sentiment (by value) numeric assortativity is %f " % nx.numeric_assortativity_coefficient(SR, 'sentiment_val')

#mention_nx_assortativity()
#mention_igraph_assortativity(f_in_user_entities)

#testing_mention_igraph_assortativity(f_in_num_tweets)
#SR_igraph_assortativity(f_in_user_concepts)
#SR_nx_assortativity()


#mention_igraph_assortativity(f_in_user_concepts)

#mention_igraph_assortativity(f_in_user_taxons)

mention_igraph_assortativity_randomize(f_in_user_concepts)