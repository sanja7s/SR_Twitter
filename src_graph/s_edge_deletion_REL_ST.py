#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	from the month of edge deletion, find the SR before, at the time and after
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
F_OUT = "mention/edge_deletion_ST_INC_stats_STRICT.dat"

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

def extract_edge_deletion_REL_ST_with_STDEV():

	MO_MENT = defaultdict(int)
	for MO in MONTHS:
		MO_MENT[MO] = read_in_MO_usr_deg(MO).copy()

	output_file = open(F_OUT, 'w')
	cnt = 0

	TOT_BEFORE = []
	TOT_DELETION = []
	TOT_AFTER = []
	with codecs.open(F_IN,'r', encoding='utf8') as input_file:
		for line in input_file:
			(userA, userB, MO_formation, MO_deletion) = line.split()
			MO_formation = int(MO_formation)
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
			MO_prior = MONTHS[int(MO_deletion)-1-5]
			MO_prior = str(MO_prior)
			G = MO_MENT[MO_prior]
			popA = G[usrA]
			popB = G[usrB]
			prior = abs(popA - popB)

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
			TOT_DELETION.append(deletion)
			TOT_BEFORE.append(prior)

			output_file.write(str(u1) + '\t' + str(u2) + '\t' + str(MO_deletion) + '\t' + \
				str(prior)+ '\t' + str(deletion)+ '\t' + str(after) + '\n')
	print "processed %d edges " % cnt
	cnt = float(cnt)

	TOT_BEFORE = np.array(TOT_BEFORE)
	TOT_DELETION = np.array(TOT_DELETION)
	TOT_AFTER = np.array(TOT_AFTER)

	avg_bef = np.mean(TOT_BEFORE)
	stdev_bef = np.std(TOT_BEFORE, dtype=np.float64)

	#print TOT_BEFORE

	avg_at = np.mean(TOT_DELETION)
	stdev_at = np.std(TOT_DELETION, dtype=np.float64)

	#print TOT_DELETION

	avg_aft = np.mean(TOT_AFTER)
	stdev_aft = np.std(TOT_AFTER, dtype=np.float64)

	print "Average REL ST ACT %f and stdev %f before, at the time %f, %f and after %f, %f edges deletion " % \
		(avg_bef, stdev_bef, avg_at, stdev_at, avg_aft, stdev_aft)

	print avg_bef, avg_at, avg_aft

def extract_edge_deletion_SR_clean_with_STDEV():

	edges_MOs = defaultdict(int)
	monthly_SR = read_in_all_monthly_SR()

	output_file = open(F_OUT_CLEAN, 'w')

	cnt = 0

	TOT_SR_BEFORE = []
	TOT_SR_DELETION = []
	TOT_SR_AFTER = []

	with codecs.open(F_IN,'r', encoding='utf8') as input_file:
		for line in input_file:
			(userA, userB, MO_formation, MO_deletion) = line.split()
			MO_formation = int(MO_formation)
			MO_deletion = int(MO_deletion)
			if MO_deletion <= 6 or MO_deletion >= 10:
				continue

			if MO_formation != 4 and MO_formation < 10:
				continue

			cnt += 1

			userA = int(userA)
			userB = int(userB)

			if userA < userB:
				u1 = userA
				u2 = userB
			else:
				u1 = userB
				u2 = userA

			SR_before = 0
			SR_deletion = 0
			SR_after = 0
			i = 1
			N = 7

			MO = MONTHS[i]
			while int(MO) < MO_deletion:
				SR_before += monthly_SR[(u1, u2)][str(MO)]
				i += 1
				MO = MONTHS[i]

			SR_deletion = monthly_SR[(u1, u2)][str(MO_deletion)]

			i += 1
			while i < 6:
				MO = MONTHS[i]
				SR_after += monthly_SR[(u1, u2)][str(MO)]
				i += 1

			months_after = float(12 - int(MO_deletion) - 2)
			SR_after = SR_after / months_after if months_after > 0 else 0
			months_before = float(int(MO_deletion) - 2 - 4)
			SR_before = SR_before / months_before if months_before > 0 else 0

			assert months_before + months_after == 4

			TOT_SR_AFTER.append(SR_after)
			TOT_SR_DELETION.append(SR_deletion)
			TOT_SR_BEFORE.append(SR_before)

			#output_file.write(str(u1) + '\t' + str(u2) + '\t' + str(MO_deletion) + '\t' + \
			#	str(SR_before)+ '\t' + str(SR_deletion)+ '\t' + str(SR_after) + '\n')
	print "processed %d edges " % cnt
	cnt = float(cnt)

	TOT_SR_BEFORE = np.array(TOT_SR_BEFORE)
	TOT_SR_DELETION = np.array(TOT_SR_DELETION)
	TOT_SR_AFTER = np.array(TOT_SR_AFTER)

	avg_bef = np.mean(TOT_SR_BEFORE)
	stdev_bef = np.std(TOT_SR_BEFORE, dtype=np.float64)

	print TOT_SR_BEFORE

	avg_at = np.mean(TOT_SR_DELETION)
	stdev_at = np.std(TOT_SR_DELETION, dtype=np.float64)

	print TOT_SR_DELETION

	avg_aft = np.mean(TOT_SR_AFTER)
	stdev_aft = np.std(TOT_SR_AFTER, dtype=np.float64)

	print "Average SR %f and stdev %f before, at the time %f, %f and after %f, %f edges deletion " % \
		(avg_bef, stdev_bef, avg_at, stdev_at, avg_aft, stdev_aft)

extract_edge_deletion_REL_ST_with_STDEV()
	









