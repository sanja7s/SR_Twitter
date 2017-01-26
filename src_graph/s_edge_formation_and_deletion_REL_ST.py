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
F_OUT = "mention/edge_formation_and_deletion_SR_stats_STRICT777.dat"

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

def extract_edge_formation_and_deletion_REL_ST_with_STDEV():

	MO_MENT = defaultdict(int)
	for MO in MONTHS:
		MO_MENT[MO] = read_in_MO_usr_deg(MO).copy()

	edges_MOs = defaultdict(int)

	output_file = open(F_OUT, 'w')

	cnt = 0

	TOT_SR_BEFORE = 0
	TOT_SR_FORMATION = 0
	TOT_SR_MID = 0
	TOT_SR_DELETION = 0
	TOT_SR_AFTER = 0

	TOT_BEFORE = []
	TOT_DELETION = []
	TOT_AFTER = []
	TOT_FORMATION = []
	TOT_MID = []

	with codecs.open(F_IN,'r', encoding='utf8') as input_file:
		for line in input_file:
			(userA, userB, MO_formation, MO_deletion) = line.split()
			MO_formation = int(MO_formation)
			if MO_formation == 4 or MO_formation >= 10:
				continue			
			MO_deletion = int(MO_deletion)
			if MO_deletion <= 6 or MO_deletion >= 10:
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

			SR_before = 0
			SR_formation = 0
			SR_mid = 0
			SR_deletion = 0
			SR_after = 0


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

			i = int(MO_formation)- 5 + 1
			#N = 7
			#MO = MONTHS[i]
			while i < MO_deletion-5+1:
				MO = MONTHS[i]
				G = MO_MENT[MO]
				popA = G[usrA]
				popB = G[usrB]
				diff = abs(popA - popB)
				TOT_MID.append(diff)
				i += 1


			MO_deletion = str(MO_deletion)
			G = MO_MENT[MO_deletion]
			popA = G[usrA]
			popB = G[usrB]
			deletion = abs(popA - popB)

			MO_after = MONTHS[int(MO_deletion)+1-5]
			MO_after = str(MO_after)
			G = MO_MENT[MO_after]
			popA = G[usrA]
			popB = G[usrB]
			after = abs(popA - popB)

			TOT_AFTER.append(after)
			TOT_FORMATION.append(formation)
			TOT_BEFORE.append(prior)
			TOT_DELETION.append(deletion)

	avg_bef = np.mean(TOT_BEFORE)
	stdev_bef = np.std(TOT_BEFORE, dtype=np.float64)

	#print TOT_BEFORE

	avg_form = np.mean(TOT_FORMATION)
	stdev_form = np.std(TOT_FORMATION, dtype=np.float64)

	#print TOT_FORMATION

	avg_mid = np.mean(TOT_MID)
	stdev_mid = np.std(TOT_MID, dtype=np.float64)

	#print TOT_MID

	avg_del = np.mean(TOT_DELETION)
	stdev_del = np.std(TOT_DELETION, dtype=np.float64)

	#print TOT_DELETION

	avg_aft = np.mean(TOT_AFTER)
	stdev_aft = np.std(TOT_AFTER, dtype=np.float64)

	#print TOT_AFTER

			
	print "processed %d edges " % cnt
	cnt = float(cnt)


	print "Average REL ST ACT, stdev before %f, %f, at the time %f, %f of formation, in the middle %f, %f, at deletion %f, %f and after %f, %f edges formation " % \
		(avg_bef, stdev_bef, avg_form, stdev_form, avg_mid, stdev_mid, avg_del, stdev_del, avg_aft, stdev_aft)

	print avg_bef, avg_form, avg_mid, avg_del, avg_aft



extract_edge_formation_and_deletion_REL_ST_with_STDEV()
	









