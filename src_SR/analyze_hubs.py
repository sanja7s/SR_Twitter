#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	analyze hubs of SR networks
'''
from igraph import *
import codecs
import os


IN_DIR = "../../../DATA/CV"
#########################################################
X = "6"
#########################################################
# TOP USER lists
#########################################################
TOP_GROUP = "hubs_SR_0." + str(X) + "/"
DIR_top_users = "TOP_users/" + str(TOP_GROUP)
PREFIX = "100_top_"

#########################
f_in_graph_SR = DIR_top_users + "undir_threshold" + str(X) + ".tab"
f_out_graph = DIR_top_users + "hubs_" + str(X) + "_edge_list.tab"
#########################


def read_in_SR_graph():
	G = Graph.Read_Ncol(f_in_graph_SR, directed=False)
	return G

def read_in_weighted_SR_graph():
	G=Graph.Read_Ncol(f_in_graph_SR_weights,names=True,directed=False, weights=True)
	return G

def save_nodes_weighted_degree():
	G = read_in_weighted_SR_graph()

def read_in_hubs():

	user_ids = []
	for top_users_file in os.listdir(DIR_top_users):
		if not top_users_file.startswith(PREFIX):
			continue
		with codecs.open(os.path.join(DIR_top_users, top_users_file),'r', encoding='utf8') as f:
			for line in f:
				line = line.split()
				user_id = int(line[0])
				user_ids.append(user_id)
	print "Read in hubs ", len(user_ids)

	return user_ids

def susbet_hubs_graph(G):

	print "Prior to subsetting hubs "
	summary(G)

	hubs = read_in_hubs()

	to_delete_vertices = [v.index for v in G.vs if int(v["name"]) not in hubs]

	print "To delete vertices ", len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)

	print "After subsetting hubs "
	summary(G)
			
	# save only once
	save_hubs_graph(G)

	return G

def save_hubs_graph(G):
	#G.write_edgelist(f_out_sent_graph)
	f = open(f_out_graph, 'w')
	f.write('Source' +  '\t' + 'Target' +  '\t' + 'type'  + '\n')
	for e in G.es:
		sid = e.source
		tid = e.target
		s = G.vs.find(sid)["name"] 
		t = G.vs.find(tid)["name"] 
		f.write(str(s) + '\t' + str(t) +  '\t' + 'undirected' + '\n')

def main():

	os.chdir(IN_DIR)

	G = read_in_SR_graph()
	# this just confirms that the edge list is correct, and imported graph in Gephi will have less nodes due to these
	#not_connected_nodes = G.vs(_degree_eq=0)
	#print len(not_connected_nodes)
	G_hubs = susbet_hubs_graph(G)

main()