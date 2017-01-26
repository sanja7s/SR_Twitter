#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	analyze assortativity of the graphs in terms of sentiment
'''
from igraph import *
import networkx as nx
import os

f_in_user_labels = "usr_num_CVs.tab"
#########################
# mention graph
#########################
f_in_graph = "threshold_mention_graphs/directed_threshold0.tab"
f_in_graph_weights = "threshold_mention_graphs/mention_graph_weights.dat"
f_out_sent_mention_graph = "directed_threshold0_sent_val.tab"
IN_DIR = "../../../DATA/mention_graph/"
f_out_mention = "sentiment_assortativity_mention_2.txt"
#########################

#########################
# SR
#########################
X = "4"
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

		r1 = G1.assortativity("val",directed=True)

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

		r1 = G1.assortativity("val",directed=False)

		ri.append(r1)
		if i%1000==0:
			print i, r1
		i += 1

		G1.add_edge(e.source, e.target)
	s = 0.0
	for r1 in ri:
		s += (r1-r)*(r1-r)
	return math.sqrt(s)

def mention_igraph_assortativity():
	os.chdir(IN_DIR)
	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	f = open(f_in_user_labels, "r")

	cnt = 0
	for line in f:
		(vid, val) = line.split('\t')
		val = int(val)
		v = G.vs.select(name = vid)
		v["val"] = val

	print cnt

	to_delete_vertices = [v.index for v in G.vs if v["val"] == None]
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	#print "Sentiment (by label) nominal assortativity is %f " %  (G.assortativity_nominal(types="val",directed=True))
	print "Sentiment (by label) assortativity is %f " %  (G.assortativity("val",directed=True))
	#print "Sentiment (by label) assortativity is %f " %  (G.assortativity(types1="sent",types2="sent",directed=True))

	#print "Sentiment (by value) assortativity is %f " %  (G.assortativity_nominal(types="sent_val",directed=True))
	#print "Sentiment (by value) assortativity is %f " %  (G.assortativity("val",directed=True))
	#print "Sentiment (by value) assortativity is %f " %  (G.assortativity(types1="sent_val",types2="sent_val",directed=True))

	r = G.assortativity("val",directed=True)
	s = jackknife_dir(G, r)
	print  "CVs DIR assortativity is %f and st. sign. is %f " % (r, s)

	###########################################

	G.to_undirected(mode='mutual')

	not_connected_nodes = G.vs(_degree_eq=0)

	to_delete_vertices = not_connected_nodes
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	r = G.assortativity("val",directed=False)
	s = jackknife_undir(G, r)
	print  "CVs MUTUAL assortativity is %f and st. sign. is %f " % (r, s)


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

def read_in_SR_graph_with_sentiment():

	G = Graph.Read_Ncol(f_in_graph_SR, directed=False)
	print f_in_graph_SR
	summary(G)

	f = open(f_in_user_sentiment, "r")
	for line in f:
		line = line[:-1].split('\t')
		vid = int(line[0])
		vsent = int(line[1])
		vsentval = float(line[2])
		try:
			G.vs.find(vid)["name"] = vid
			G.vs.find(vid)["sent_val"] = vsentval
			G.vs.find(vid)["sent"] = vsent
		except IndexError:
			continue

	summary(G)

	to_delete_vertices = [v.index for v in G.vs if v["sent"] == None]
	G.delete_vertices(to_delete_vertices)
			
	# save only once
	save_graph_with_sentiment(G)

	return G

def SR_igraph_assortativity():
	os.chdir(IN_DIR_SR)

	G = Graph.Read_Ncol(f_in_graph_SR, directed=False)
	print f_in_graph_SR
	summary(G)

	print "Degree assortativity UNWEIGHTED is %f " % \
	(G.assortativity_degree(directed=False))

	G = Graph.Read_Ncol(f_in_graph_SR_weights,names=True, directed=False, weights=True)
	print f_in_graph_SR
	summary(G)

	print "Degree assortativity DEFAULT is %f " % \
	(G.assortativity(directed=True,types1=G.strength(weights='weight')))
	print "Degree assortativity IN-OUT is %f " % \
	(G.assortativity(directed=True,types1=G.strength(weights='weight',mode=IN),types2=G.strength(weights='weight',mode=OUT)))
	print "Degree assortativity OUT-IN is %f " % \
	(G.assortativity(directed=True,types1=G.strength(weights='weight',mode=OUT),types2=G.strength(weights='weight',mode=IN)))
	print "Degree assortativity IN-IN is %f " % \
	(G.assortativity(directed=True,types1=G.strength(weights='weight',mode=IN),types2=G.strength(weights='weight',mode=IN)))
	print "Degree assortativity OUT-OUT is %f " % \
	(G.assortativity(directed=True,types1=G.strength(weights='weight',mode=OUT),types2=G.strength(weights='weight',mode=OUT)))

	f = open(f_in_user_sentiment, "r")
	cnt = 0
	for line in f:
		(vid, vsent, vsentval) = line[:-1].split('\t')
		vsent = int(vsent)
		vsentval = float(vsentval)
		v = G.vs.select(name = vid)
		v["sent_val"] = vsentval
		v["sent"] = vsent
		vsent_nominal = vsent
		if vsent_nominal == -1:
			vsent_nominal = 2
		v["sent_nominal"] = vsent_nominal

	print cnt

	to_delete_vertices = [v.index for v in G.vs if v["sent"] == None]
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	print "Sentiment (by label) nominal assortativity is %f " %  (G.assortativity_nominal(types="sent_nominal",directed=False))
	print "Sentiment (by label) assortativity is %f " %  (G.assortativity("sent",directed=False))
	#print "Sentiment (by label) assortativity is %f " %  (G.assortativity(types1="sent",types2="sent",directed=True))

	#print "Sentiment (by value) assortativity is %f " %  (G.assortativity_nominal(types="sent_val",directed=True))
	print "Sentiment (by value) assortativity is %f " %  (G.assortativity("sent_val",directed=False))
	#print "Sentiment (by value) assortativity is %f " %  (G.assortativity(types1="sent_val",types2="sent_val",directed=True))


	os.chdir("../")

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
mention_igraph_assortativity()

#SR_igraph_assortativity()
#SR_nx_assortativity()