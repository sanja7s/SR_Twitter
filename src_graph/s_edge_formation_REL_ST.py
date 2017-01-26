#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	from the month of edge formation, find the SR before, at the time and after
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
F_OUT = "mention/edge_formation_REL_ST_stats_STRICT.dat"

MONTHS =  ["5", "6", "7", "8", "9", "10", "11"]

#########################
# read from a file that is an edge list with weights
#########################
def read_in_MO_usr_deg(MO):
	#G = Graph.Read_Ncol('mention/' + MO + 'mention_edgelist_dir_w', directed=True, weights=True)
	f = open('mention/' + MO + 'mention_edges_monthly_SR', 'r') # 5mention_edges_monthly_SR
	#print G.summary()
	usr_MO_deg = defaultdict(int)
	for line in f:
		(u1,u2,sr,w1,w2) = line.split()
		usr_MO_deg[int(u1)] = int(w1)
		usr_MO_deg[int(u2)] = int(w2)
	return usr_MO_deg

def extract_edge_formation_REL_ST_with_STDEV():

	MO_MENT = defaultdict(int)
	for MO in MONTHS:
		MO_MENT[MO] = read_in_MO_usr_deg(MO).copy()

	output_file = open(F_OUT, 'w')
	cnt = 0

	TOT_BEFORE = []
	TOT_FORMATION = []
	TOT_AFTER = []
	with codecs.open(F_IN,'r', encoding='utf8') as input_file:
		for line in input_file:
			(userA, userB, MO_formation, MO_deletion) = line.split()
			MO_formation = int(MO_formation)
			MO_deletion = int(MO_deletion)
			if MO_formation == 4 or MO_formation >= 10:
				continue
			cnt += 1
			usrA = int(userA)
			usrB = int(userB)
			if userA < userB:
				u1 = userA
				u2 = userB
			else:
				u1 = userB
				u2 = userA

			MO_prior = MONTHS[int(MO_formation)-1-5]
			MO_prior = str(MO_prior)
			G = MO_MENT[MO_prior]
			popA = G[usrA]
			popB = G[usrB]
			prior = abs(popA - popB)

			MO_formation = str(MO_formation)
			G = MO_MENT[MO_formation]
			popA = G[usrA]
			popB = G[usrB]
			formation = abs(popA - popB)

			MO_after = MONTHS[int(MO_formation)+1-5]
			MO_after = str(MO_after)
			G = MO_MENT[MO_after]
			popA = G[usrA]
			popB = G[usrB]
			after = abs(popA - popB)

			TOT_AFTER.append(after)
			TOT_FORMATION.append(formation)
			TOT_BEFORE.append(prior)

			output_file.write(str(u1) + '\t' + str(u2) + '\t' + str(MO_formation) + '\t' + \
				str(prior)+ '\t' + str(formation)+ '\t' + str(after) + '\n')
	print "processed %d edges " % cnt
	cnt = float(cnt)

	TOT_BEFORE = np.array(TOT_BEFORE)
	TOT_FORMATION = np.array(TOT_FORMATION)
	TOT_AFTER = np.array(TOT_AFTER)

	avg_bef = np.mean(TOT_BEFORE)
	stdev_bef = np.std(TOT_BEFORE, dtype=np.float64)

	#print TOT_BEFORE

	avg_at = np.mean(TOT_FORMATION)
	stdev_at = np.std(TOT_FORMATION, dtype=np.float64)

	#print TOT_FORMATION

	avg_aft = np.mean(TOT_AFTER)
	stdev_aft = np.std(TOT_AFTER, dtype=np.float64)

	print "Average REL ST ACT %f and stdev %f before, at the time %f, %f and after %f, %f edges formation " % \
		(avg_bef, stdev_bef, avg_at, stdev_at, avg_aft, stdev_aft)

	print avg_bef, avg_at, avg_aft


extract_edge_formation_REL_ST_with_STDEV()
	









