#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from collections import defaultdict

IN_DIR = "../../../DATA/mention_graph/"
f_weighted_edges_in = "mention_graph_weights.dat"
f_recip_weighted_edges_out = "recip_mention_graph_weights.dat"
f_recip_weighted_edges_out_simmetrical = "recip_mention_graph_weights_simmetrical.dat"

def create_reciprocal_weighted():

	os.chdir(IN_DIR)

	f = open(f_weighted_edges_in, 'r') 
	f_out = open(f_recip_weighted_edges_out, 'w') 

	dir_edges = defaultdict(int) 

	for line in f:
		(uid1, uid2, w) = line.split()
		uid1 = int(uid1)
		uid2 = int(uid2)
		w = int(w)
		dir_edges[(uid1, uid2)] = w

	recip_edges = defaultdict(int)
	for edge in dir_edges:
		u1, u2 = edge[0], edge[1]
		if (u2, u1) in dir_edges:
			if u2 < u1:
				u1, u2 = u2, u1
			recip_edges[(u1, u2)] += dir_edges[edge]

	for (u1, u2) in recip_edges:
		w = recip_edges[(u1, u2)]
		f_out.write(str(u1) + '\t' + str(u2) + '\t' + str(w) + '\n')

def create_reciprocal_weighted_simmetrical():

	os.chdir(IN_DIR)

	f = open(f_weighted_edges_in, 'r') 
	f_out = open(f_recip_weighted_edges_out_simmetrical, 'w') 

	dir_edges = defaultdict(int) 

	for line in f:
		(uid1, uid2, w) = line.split()
		uid1 = int(uid1)
		uid2 = int(uid2)
		w = int(w)
		dir_edges[(uid1, uid2)] = w

	recip_edges = defaultdict(int)
	for edge in dir_edges:
		u1, u2 = edge[0], edge[1]
		if u1 < u2:
			if (u2, u1) in dir_edges and (u1, u2) in dir_edges:
				recip_edges[(u1, u2)] = dir_edges[(u1, u2)]
				recip_edges[(u2, u1)] = dir_edges[(u2, u1)]

	for (u1, u2) in recip_edges:
		w = recip_edges[(u1, u2)]
		f_out.write(str(u1) + '\t' + str(u2) + '\t' + str(w) + '\n')

#create_reciprocal_weighted()
create_reciprocal_weighted_simmetrical()