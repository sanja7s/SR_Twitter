#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	analyze assortativity of the graph in terms of taxonomies
'''
from igraph import *

import os

f_in_user_taxonomy = "tweets_taxonomy_clean.JSON"

#########################
f_in_mention_graph = "threshold_mention_graphs/mention_graph_weights.dat"
#f_out_ment_sent_graph = "directed_threshold0_sent_val.tab"
IN_DIR_ment = "../../../DATA/mention_graph/"
f_out_ment = "sentiment_assortativity_mention.txt"
#########################
#########################
X = "9"
f_in_graph_SR = "threshold_graphs/undir_threshold" + str(X) + ".tab"
f_out_SR_sent_graph = "../../Gephi/SR/gephi_undir_threshold" + str(X) + "_edge_list.tab"
IN_DIR_SR = "../../../DATA/SR_graphs/"
f_out_SR = "sentiment_assortativity_SR"  + str(X) + ".txt"
#########################


def read_in_mention_graph():
	G = Graph.Read_Ncol(f_in_mention_graph,names=True, directed=True, weights=True)
	return G


def main():

	os.chdir(IN_DIR)

	sys.stdout = open(f_out_ment, 'w')
	G = read_in_mention_graph_with_sentiment()

	print "Degree assortativity is %f " % (G.assortativity_degree(directed=False))
	print "Sentiment (label) assortativity is %f " %  (G.assortativity("sent"))
	print "Sentiment (by value) assortativity is %f " %  (G.assortativity("sent_val"))

main()