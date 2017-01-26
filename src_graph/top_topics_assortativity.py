#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	analyze assortativity of the graph in terms of taxonomies
'''
from igraph import *
import os
import random

f_in_user_taxonomy = "tweets_taxonomy_clean.JSON"

#########################
# mention graph
#########################
f_in_graph_weights = "threshold_mention_graphs/mention_graph_weights.dat"
IN_DIR = "../../../DATA/mention_graph/"
#########################
f_out_ment = "topic_assortativity_mention.txt"
f_out_ment_rand = "topic_assortativity_mention_randomized_graph.txt"
#########################
f_in_user_topics = "user_score_for_top_topics.tab"
#########################
#X = "9"
#f_in_graph_SR = "threshold_graphs/undir_threshold" + str(X) + ".tab"
#f_out_SR_sent_graph = "../../Gephi/SR/gephi_undir_threshold" + str(X) + "_edge_list.tab"
#IN_DIR_SR = "../../../DATA/SR_graphs/"
#f_out_SR = "sentiment_assortativity_SR"  + str(X) + ".txt"
#########################

def jackknife_dir(G, r, att):
	ri = []
	G1 = G.copy()
	print len(G.es)
	i = 0
	for e in G.es:
		G1.delete_edges((e.source, e.target))

		r1 = G1.assortativity(att,directed=True)

		ri.append(r1)
		#if i%1000==0:
		#	print i, r1
		i += 1

		G1.add_edge(e.source, e.target)
	s = 0.0
	for r1 in ri:
		s += (r1-r)*(r1-r)
	return math.sqrt(s)

def jackknife_undir(G, r, att):
	ri = []
	G1 = G.copy()
	print len(G.es)
	i = 0
	for e in G.es:
		G1.delete_edges((e.source, e.target))

		r1 = G1.assortativity(att,directed=False)

		ri.append(r1)
		#if i%1000==0:
		#	print i, r1
		i += 1

		G1.add_edge(e.source, e.target)
	s = 0.0
	for r1 in ri:
		s += (r1-r)*(r1-r)
	return math.sqrt(s)

def mention_igraph_assortativity():
	#sys.stdout = open(f_out_ment, 'w')
	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	f = open(f_in_user_topics, "r")

	for line in f:
		(vid, music, movies, sex, humor, school) = line.split('\t')
		music = float(music)
		movies = float(movies)
		sex = float(sex)
		humor = float(humor)
		school = float(school)
		v = G.vs.select(name = vid)
		v["music"] = music
		v["movies"] = movies
		v["sex"] = sex
		v["humor"] = humor
		v["school"] = school

	to_delete_vertices = [v.index for v in G.vs if v["music"] == None]
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	"""
	for att in ["music", "movies", "sex", "humor", "school"]:
		print
		print att
		#print  "label assortativity is %f " %  (G.assortativity(types1=att,types2=att,directed=True))
		#print "label assortativity is %f " %  (G.assortativity(att,directed=True))
		 

		r = G.assortativity(att,directed=True)
		s = jackknife_dir(G, r, att)
		print att + " DIR assortativity is %f and st. dev. is %f " % (r, s)

	"""
	###########################################

	G.to_undirected(mode='mutual')

	not_connected_nodes = G.vs(_degree_eq=0)

	to_delete_vertices = not_connected_nodes
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	for att in ["music", "movies", "sex", "humor", "school"]:
		print
		print att
		r = G.assortativity(att,directed=False)
		s = jackknife_undir(G, r, att)
		print att + " MUTUAL assortativity is %f and st. sign. is %f " % (r, s)

def mention_igraph_assortativity_randomize():
	sys.stdout = open(f_out_ment_rand, 'w')
	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	print "Randomize vertices"
	s = G.vs["name"]
	random.shuffle(s)
	G.vs["name"] = s
	summary(G)

	f = open(f_in_user_topics, "r")
	for line in f:
		(vid, music, movies, sex, humor, school) = line.split('\t')
		music = float(music)
		movies = float(movies)
		sex = float(sex)
		humor = float(humor)
		school = float(school)
		v = G.vs.select(name = vid)
		v["music"] = music
		v["movies"] = movies
		v["sex"] = sex
		v["humor"] = humor
		v["school"] = school

	to_delete_vertices = [v.index for v in G.vs if v["music"] == None]
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	for att in ["music", "movies", "sex", "humor", "school"]:
		print att
		print  "label assortativity is %f " %  (G.assortativity(types1=att,types2=att,directed=True))
		print "label assortativity is %f " %  (G.assortativity(att,directed=True))
		print 
	

def main():

	os.chdir(IN_DIR)
	print 'START'
	mention_igraph_assortativity()
	#mention_igraph_assortativity_randomize()

main()