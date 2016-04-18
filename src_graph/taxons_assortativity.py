#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	analyze assortativity of the graphs in terms of sentiment
'''
from igraph import *
import networkx as nx
import os

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

	print "nominal assortativity is %f " %  (G.assortativity_nominal(types="att",directed=True))
	print "label assortativity is %f " %  (G.assortativity(types1="att",types2="att",directed=True))
	print "label assortativity is %f " %  (G.assortativity("att",directed=True))

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
mention_igraph_assortativity(f_in_user_entities)

#SR_igraph_assortativity(f_in_user_concepts)
#SR_nx_assortativity()

