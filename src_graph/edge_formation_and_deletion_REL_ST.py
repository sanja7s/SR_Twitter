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
def read_in_MO_graph(MO):
	G = Graph.Read_Ncol('mention/' + MO + '_MENT_weight_dir_self_loops', directed=True, weights=True)
	print G.summary()
	return G

def read_in_MO_graph_MUTUAL_UNW(MO):
	G = Graph.Read_Ncol('mention/' + MO + '_MENT_weight_dir_self_loops', directed=True, weights=True)
	G.to_undirected(mode="mutual", combine_edges='ignore')
	print G.summary()
	return G

def extract_edge_formation_and_deletion_REL_ST_with_STDEV_POP():

	MO_MENT = defaultdict(int)
	for MO in MONTHS:
		MO_MENT[MO] = read_in_MO_graph(MO).copy()

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
			userA = int(userA)
			userB = int(userB)
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
			nA = G.vs.select(name = str(u1))
			nB = G.vs.select(name = str(u2))
			try:
				popA = G.strength(nA[0].index, mode=IN, weights='weight')
			except IndexError:
				popA = 0 
			try:
				popB = G.strength(nB[0].index, mode=IN, weights='weight')
			except IndexError:
				popB = 0 
			prior = abs(popA - popB)


			MO_formation = str(MO_formation)
			G = MO_MENT[MO_formation]
			nA = G.vs.select(name = str(u1))
			nB = G.vs.select(name = str(u2))
			try:
				popA = G.strength(nA[0].index, mode=IN, weights='weight')
			except IndexError:
				popA = 0 
				print u1, u2, MO_formation
			try:
				popB = G.strength(nB[0].index, mode=IN, weights='weight')
			except IndexError:
				popB = 0 
				print u2, u1, MO_formation
			formation = abs(popA - popB)

			i = int(MO_formation)- 5 + 1
			#N = 7
			#MO = MONTHS[i]
			while i < MO_deletion-5+1:
				MO = MONTHS[i]
				G = MO_MENT[MO]
				nA = G.vs.select(name = str(u1))
				nB = G.vs.select(name = str(u2))
				try:
					popA = G.strength(nA[0].index, mode=IN, weights='weight')
				except IndexError:
					popA = 0 
				try:
					popB = G.strength(nB[0].index, mode=IN, weights='weight')
				except IndexError:
					popB = 0 
				diff = abs(popA - popB)
				TOT_MID.append(diff)
				i += 1


			MO_deletion = str(MO_deletion)
			G = MO_MENT[MO_deletion]
			nA = G.vs.select(name = str(u1))
			nB = G.vs.select(name = str(u2))
			popA = G.strength(nA[0].index, mode=IN, weights='weight')
			popB = G.strength(nB[0].index, mode=IN, weights='weight')
			deletion = abs(popA - popB)

			"""
			if MO_formation == MO_deletion:
				assert i - 1 == MO_deletion - 5
				SR_mid += SR_formation
				assert SR_formation == SR_deletion
			"""

			MO_after = MONTHS[int(MO_deletion)+1-5]
			MO_after = str(MO_after)
			G = MO_MENT[MO_after]
			nA = G.vs.select(name = str(u1))
			nB = G.vs.select(name = str(u2))
			try:
				popA = G.strength(nA[0].index, mode=IN, weights='weight')
			except IndexError:
				popA = 0 
			try:
				popB = G.strength(nB[0].index, mode=IN, weights='weight')
			except IndexError:
				popB = 0 
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


	print "Average REL ST POP, stdev before %f, %f, at the time %f, %f of formation, in the middle %f, %f, at deletion %f, %f and after %f, %f edges formation " % \
		(avg_bef, stdev_bef, avg_form, stdev_form, avg_mid, stdev_mid, avg_del, stdev_del, avg_aft, stdev_aft)
	print 
	print avg_bef, avg_form, avg_mid, avg_del, avg_aft
	print stdev_bef, stdev_form, stdev_mid, stdev_del, stdev_aft


def extract_edge_formation_and_deletion_REL_ST_with_STDEV_ACT():

	MO_MENT = defaultdict(int)
	for MO in MONTHS:
		MO_MENT[MO] = read_in_MO_graph(MO).copy()

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
			userA = int(userA)
			userB = int(userB)
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
			nA = G.vs.select(name = str(u1))
			nB = G.vs.select(name = str(u2))
			try:
				popA = G.strength(nA[0].index, mode=OUT, weights='weight')
			except IndexError:
				popA = 0 
			try:
				popB = G.strength(nB[0].index, mode=OUT, weights='weight')
			except IndexError:
				popB = 0 
			prior = abs(popA - popB)


			MO_formation = str(MO_formation)
			G = MO_MENT[MO_formation]
			nA = G.vs.select(name = str(u1))
			nB = G.vs.select(name = str(u2))
			try:
				popA = G.strength(nA[0].index, mode=OUT, weights='weight')
			except IndexError:
				popA = 0 
				print u1, u2, MO_formation
			try:
				popB = G.strength(nB[0].index, mode=OUT, weights='weight')
			except IndexError:
				popB = 0 
				print u2, u1, MO_formation
			formation = abs(popA - popB)

			i = int(MO_formation)- 5 + 1
			#N = 7
			#MO = MONTHS[i]
			while i < MO_deletion-5+1:
				MO = MONTHS[i]
				G = MO_MENT[MO]
				nA = G.vs.select(name = str(u1))
				nB = G.vs.select(name = str(u2))
				try:
					popA = G.strength(nA[0].index, mode=OUT, weights='weight')
				except IndexError:
					popA = 0 
				try:
					popB = G.strength(nB[0].index, mode=OUT, weights='weight')
				except IndexError:
					popB = 0 
				diff = abs(popA - popB)
				TOT_MID.append(diff)
				i += 1


			MO_deletion = str(MO_deletion)
			G = MO_MENT[MO_deletion]
			nA = G.vs.select(name = str(u1))
			nB = G.vs.select(name = str(u2))
			popA = G.strength(nA[0].index, mode=OUT, weights='weight')
			popB = G.strength(nB[0].index, mode=OUT, weights='weight')
			deletion = abs(popA - popB)

			"""
			if MO_formation == MO_deletion:
				assert i - 1 == MO_deletion - 5
				SR_mid += SR_formation
				assert SR_formation == SR_deletion
			"""

			MO_after = MONTHS[int(MO_deletion)+1-5]
			MO_after = str(MO_after)
			G = MO_MENT[MO_after]
			nA = G.vs.select(name = str(u1))
			nB = G.vs.select(name = str(u2))
			try:
				popA = G.strength(nA[0].index, mode=OUT, weights='weight')
			except IndexError:
				popA = 0 
			try:
				popB = G.strength(nB[0].index, mode=OUT, weights='weight')
			except IndexError:
				popB = 0 
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
	print 
	print avg_bef, avg_form, avg_mid, avg_del, avg_aft
	print stdev_bef, stdev_form, stdev_mid, stdev_del, stdev_aft


def extract_edge_formation_and_deletion_REL_ST_with_STDEV_MUTUAL_UNW():

	MO_MENT = defaultdict(int)
	for MO in MONTHS:
		MO_MENT[MO] = read_in_MO_graph_MUTUAL_UNW(MO).copy()
	edges_MOs = defaultdict(int)

	output_file = open(F_OUT, 'w')

	cnt = 0

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
			userA = int(userA)
			userB = int(userB)
			if userA < userB:
				u1 = userA
				u2 = userB
			else:
				u1 = userB
				u2 = userA

			MO_prior = MONTHS[int(MO_formation)-1-5]
			MO_prior = str(MO_prior)
			G = MO_MENT[MO_prior]
			nA = G.vs.select(name = str(u1))
			nB = G.vs.select(name = str(u2))
			try:
				popA = G.degree(nA[0].index,)
			except IndexError:
				popA = 0 
			try:
				popB = G.degree(nB[0].index)
			except IndexError:
				popB = 0 
			prior = abs(popA - popB)


			MO_formation = str(MO_formation)
			G = MO_MENT[MO_formation]
			nA = G.vs.select(name = str(u1))
			nB = G.vs.select(name = str(u2))
			try:
				popA = G.degree(nA[0].index)
			except IndexError:
				popA = 0 
				print u1, u2, MO_formation
			try:
				popB = G.degree(nB[0].index)
			except IndexError:
				popB = 0 
				print u2, u1, MO_formation
			formation = abs(popA - popB)

			i = int(MO_formation)- 5 + 1
			#N = 7
			#MO = MONTHS[i]
			while i < MO_deletion-5+1:
				MO = MONTHS[i]
				G = MO_MENT[MO]
				nA = G.vs.select(name = str(u1))
				nB = G.vs.select(name = str(u2))
				try:
					popA = G.degree(nA[0].index)
				except IndexError:
					popA = 0 
				try:
					popB = G.degree(nB[0].index)
				except IndexError:
					popB = 0 
				diff = abs(popA - popB)
				TOT_MID.append(diff)
				i += 1


			MO_deletion = str(MO_deletion)
			G = MO_MENT[MO_deletion]
			nA = G.vs.select(name = str(u1))
			nB = G.vs.select(name = str(u2))
			popA = G.degree(nA[0].index)
			popB = G.degree(nB[0].index)
			deletion = abs(popA - popB)

			"""
			if MO_formation == MO_deletion:
				assert i - 1 == MO_deletion - 5
				SR_mid += SR_formation
				assert SR_formation == SR_deletion
			"""

			MO_after = MONTHS[int(MO_deletion)+1-5]
			MO_after = str(MO_after)
			G = MO_MENT[MO_after]
			nA = G.vs.select(name = str(u1))
			nB = G.vs.select(name = str(u2))
			try:
				popA = G.degree(nA[0].index)
			except IndexError:
				popA = 0 
			try:
				popB = G.degree(nB[0].index)
			except IndexError:
				popB = 0 
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


	print "Average REL ST MUTUAL CONT, stdev before %f, %f, at the time %f, %f of formation, in the middle %f, %f, at deletion %f, %f and after %f, %f edges formation " % \
		(avg_bef, stdev_bef, avg_form, stdev_form, avg_mid, stdev_mid, avg_del, stdev_del, avg_aft, stdev_aft)
	print 
	print avg_bef, avg_form, avg_mid, avg_del, avg_aft
	print stdev_bef, stdev_form, stdev_mid, stdev_del, stdev_aft


#extract_edge_formation_and_deletion_REL_ST_with_STDEV()
#extract_edge_formation_and_deletion_REL_ST_with_STDEV_ACT()
extract_edge_formation_and_deletion_REL_ST_with_STDEV_MUTUAL_UNW()

	









