#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	analyze assortativity of the graph in terms of sentiment
'''
from igraph import *

import os

f_in_user_sentiment = "user_sentiment.tab"

#########################
f_in_graph = "threshold_mention_graphs/directed_threshold0.tab"
f_out_sent_graph = "directed_threshold0_sent_val.tab"
IN_DIR = "../../../DATA/mention_graph/"
f_out = "sentiment_assortativity_mention.txt"
#########################
#########################
X = "9"
f_in_graph_SR = "threshold_graphs/undir_threshold" + str(X) + ".tab"
f_out_sent_graph = "../../Gephi/SR/gephi_undir_threshold" + str(X) + "_edge_list.tab"
IN_DIR = "../../../DATA/SR_graphs/"
f_out_SR = "sentiment_assortativity_SR"  + str(X) + ".txt"
#########################


def read_in_mention_graph_with_sentiment():
	G = Graph.Read_Ncol(f_in_graph)

	f = open(f_in_user_sentiment, "r")

	for line in f:
		line = line[:-1].split('\t')
		vid = int(line[0])
		vsent = int(line[1])
		vsentval = float(line[2])
		try:
			G.vs.find(vid)["label"] = vid
			G.vs.find(vid)["sent_val"] = vsentval
			G.vs.find(vid)["sent"] = vsent
		except IndexError:
			continue

	to_delete_vertices = [v.index for v in G.vs if v["sent"] == None]
	G.delete_vertices(to_delete_vertices)
			
	# save only once
	save_graph_with_sentiment(G)

	return G

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
			G.vs.find(vid)["label"] = vid
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

def save_graph_with_sentiment(G):
	#G.write_edgelist(f_out_sent_graph)

	summary(G)
	f = open(f_out_sent_graph, 'w')
	f.write('Source' +  '\t' + 'Target' +  '\t' + 'type'  + '\n')
	for e in G.es:
		sid = e.source
		tid = e.target
		s = G.vs.find(sid)["label"] 
		t = G.vs.find(tid)["label"] 
		f.write(str(s) + '\t' + str(t) +  '\t' + 'undirected' + '\n')
		# print str(s) + '\t' + str(t) +  '\t' + 'undirected' + '\n'

def main():

	os.chdir(IN_DIR)

	# sys.stdout = open('f_out_mention', 'w')
	# G = read_in_mention_graph_with_sentiment()

	G = read_in_SR_graph_with_sentiment()
	summary(G)
	# this just confirms that the edge list is correct, and imported graph in Gephi will have less nodes due to these
	not_connected_nodes = G.vs(_degree_eq=0)
	print len(not_connected_nodes)

	sys.stdout = open(f_out_SR, 'w')
	summary(G)
	


	print "Degree assortativity is %f " % (G.assortativity_degree(directed=False))
	print "Sentiment (label) assortativity is %f " %  (G.assortativity("sent"))
	print "Sentiment (by value) assortativity is %f " %  (G.assortativity("sent_val"))

main()