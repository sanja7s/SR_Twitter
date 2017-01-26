#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	from the data of edge formation/deletion, find the persisting edges and their monthly REL ST
"""
from collections import defaultdict
import codecs
import os
import json
import numpy as np
from igraph import *

IN_DIR = "../../../DATA/General/"
os.chdir(IN_DIR)

F_IN = "mention/edge_formation_deletion_MOs.dat"

MONTHS =  ["5", "6", "7", "8", "9", "10", "11"]

#########################
# read from a file that is an edge list with weights
#########################
def read_in_MO_graph(MO):
	G = Graph.Read_Ncol('mention/' + MO + '_MENT_weight_dir_self_loops', directed=True, weights=True)
	print G.summary()
	return G


def read_in_MO_graph_MUTUAL_UNW(MO):
	G = Graph.Read_Ncol('mention/' + MO + '_MENT_weight_dir_self_loops', directed=True, weights=True)
	G.to_undirected(mode="mutual", combine_edges='ignore')
	print G.summary()
	return G

def extract_edges_per_MO_REL_ST_with_STDEV_POP():

	MO_MENT = defaultdict(int)
	for MO in MONTHS:
		MO_MENT[MO] = read_in_MO_graph(MO).copy()

	cnt = 0
	TOT = defaultdict(list)

	i = 0
	N = 7
	MO = MONTHS[i]
	while i < N-1:
		G = MO_MENT[MO]
		for e in G.es:
			src_id = e.source
			dest_id = e.target
			try:
				popA = G.strength(src_id, mode=IN, weights='weight')
			except IndexError:
				popA = 0 
			try:
				popB = G.strength(dest_id, mode=IN, weights='weight')
			except IndexError:
				popB = 0 
			diff = abs(popA - popB)
			TOT[MO].append(diff)
		i += 1
		MO = MONTHS[i]


	print "processed %d edges " % cnt
	cnt = float(cnt)

	for MO in MONTHS[:-1]:
		TOT[MO] = np.array(TOT[MO])
		avg = np.nanmean(TOT[MO])
		std = np.nanstd(TOT[MO])
		print TOT[MO]
		print "Average REL ST POP, stdev %f, %f, at the time %s " % \
		(avg, std, MO)

def extract_edges_per_MO_REL_ST_with_STDEV_ACT():

	MO_MENT = defaultdict(int)
	for MO in MONTHS:
		MO_MENT[MO] = read_in_MO_graph(MO).copy()

	cnt = 0
	TOT = defaultdict(list)

	i = 0
	N = 7
	MO = MONTHS[i]
	while i < N-1:
		G = MO_MENT[MO]
		for e in G.es:
			src_id = e.source
			dest_id = e.target

			#userA = G.vs[src_id]['name']
			#uesrB = G.vs[dest_id]['name']

			try:
				popA = G.strength(src_id, mode=OUT, weights='weight')
			except IndexError:
				popA = 0 
			try:
				popB = G.strength(dest_id, mode=OUT, weights='weight')
			except IndexError:
				popB = 0 
			diff = abs(popA - popB)
			TOT[MO].append(diff)
		i += 1
		MO = MONTHS[i]


	print "processed %d edges " % cnt
	cnt = float(cnt)

	for MO in MONTHS[:-1]:
		TOT[MO] = np.array(TOT[MO])
		avg = np.nanmean(TOT[MO])
		std = np.nanstd(TOT[MO])
		print TOT[MO]
		print "Average REL ST ACT, stdev %f, %f, at the time %s " % \
		(avg, std, MO)

def extract_edges_per_MO_REL_ST_with_STDEV_MUTUAL_UNW():

	MO_MENT = defaultdict(int)
	for MO in MONTHS:
		MO_MENT[MO] = read_in_MO_graph_MUTUAL_UNW(MO).copy()

	cnt = 0
	TOT = defaultdict(list)

	i = 0
	N = 7
	MO = MONTHS[i]
	while i < N-1:
		G = MO_MENT[MO]
		for e in G.es:
			src_id = e.source
			dest_id = e.target

			try:
				popA = G.degree(src_id)
			except IndexError:
				popA = 0 
			try:
				popB = G.degree(dest_id)
			except IndexError:
				popB = 0 
			diff = abs(popA - popB)
			if diff == 552:
				userA = G.vs[src_id]['name']
				uesrB = G.vs[dest_id]['name']
				print popA, popB
				print userA, uesrB 
			TOT[MO].append(diff)
		i += 1
		MO = MONTHS[i]


	print "processed %d edges " % cnt
	cnt = float(cnt)

	for MO in MONTHS[:-1]:
		TOT[MO] = np.array(TOT[MO])
		avg = np.mean(TOT[MO])
		std = np.std(TOT[MO])
		print TOT[MO]
		print "Average REL ST MUTUAL CONTACTS, stdev %f, %f, at the time %s " % \
		(avg, std, MO)



extract_edges_per_MO_REL_ST_with_STDEV_MUTUAL_UNW()
	









