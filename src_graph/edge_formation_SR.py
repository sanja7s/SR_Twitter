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

IN_DIR = "../../../DATA/General/"
os.chdir(IN_DIR)

F_IN = "mention/edge_formation_deletion_MOs.dat"
F_OUT = "mention/edge_formation_SR_stats_STRICT.dat"

F_OUT_CLEAN = "mention/edge_formation_SR_stats_STRICT_CLEAN.dat"

MONTHS =  ["5", "6", "7", "8", "9", "10", "11"]

def extract_edge_formation_SR():

	edges_MOs = defaultdict(int)
	monthly_SR = read_in_all_monthly_SR()

	output_file = open(F_OUT, 'w')

	cnt = 0

	TOT_SR_BEFORE = 0
	TOT_SR_FORMATION = 0
	TOT_SR_AFTER = 0

	with codecs.open(F_IN,'r', encoding='utf8') as input_file:
		for line in input_file:
			(userA, userB, MO_formation, MO_deletion) = line.split()
			MO_formation = int(MO_formation)
			if MO_formation == 4 or MO_formation >= 10:
				continue
			# remove or no
			if MO_deletion >= 6 and MO_deletion <= 10:
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
			SR_after = 0
			i = 1
			N = 7

			MO = MONTHS[i]
			while int(MO) < MO_formation:
				SR_before += monthly_SR[(u1, u2)][str(MO)]
				i += 1
				MO = MONTHS[i]

			SR_formation = monthly_SR[(u1, u2)][str(MO_formation)]

			i += 1
			while i < 6:
				MO = MONTHS[i]
				SR_after += monthly_SR[(u1, u2)][str(MO)]
				i += 1

			months_after = float(12 - int(MO_formation) - 2)
			SR_after = SR_after / months_after if months_after > 0 else 0
			months_before = float(int(MO_formation) - 2 - 4)
			SR_before = SR_before / months_before if months_before > 0 else 0

			assert months_before + months_after == 4

			TOT_SR_AFTER += SR_after
			TOT_SR_FORMATION += SR_formation
			TOT_SR_BEFORE += SR_before

			output_file.write(str(u1) + '\t' + str(u2) + '\t' + str(MO_formation) + '\t' + \
				str(SR_before)+ '\t' + str(SR_formation)+ '\t' + str(SR_after) + '\n')
	print "processed %d edges " % cnt
	cnt = float(cnt)
	print "Average SR before %f, at the time %f and after %f edges formation " % \
		(TOT_SR_BEFORE/cnt, TOT_SR_FORMATION/cnt, TOT_SR_AFTER/cnt)

def extract_edge_formation_SR_clean():

	edges_MOs = defaultdict(int)
	monthly_SR = read_in_all_monthly_SR()

	output_file = open(F_OUT_CLEAN, 'w')

	cnt = 0

	TOT_SR_BEFORE = 0
	TOT_SR_FORMATION = 0
	TOT_SR_AFTER = 0

	with codecs.open(F_IN,'r', encoding='utf8') as input_file:
		for line in input_file:
			(userA, userB, MO_formation, MO_deletion) = line.split()
			MO_formation = int(MO_formation)

			MO_deletion = int(MO_deletion)

			if MO_formation == 4 or MO_formation >= 10:
				continue

			if MO_deletion > 6 and MO_deletion < 10:
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
			SR_after = 0
			i = 1
			N = 7

			MO = MONTHS[i]
			while int(MO) < MO_formation:
				SR_before += monthly_SR[(u1, u2)][str(MO)]
				i += 1
				MO = MONTHS[i]

			SR_formation = monthly_SR[(u1, u2)][str(MO_formation)]

			i += 1
			while i < 6:
				MO = MONTHS[i]
				SR_after += monthly_SR[(u1, u2)][str(MO)]
				i += 1

			months_after = float(12 - int(MO_formation) - 2)
			SR_after = SR_after / months_after if months_after > 0 else 0
			months_before = float(int(MO_formation) - 2 - 4)
			SR_before = SR_before / months_before if months_before > 0 else 0

			assert months_before + months_after == 4

			TOT_SR_AFTER += SR_after
			TOT_SR_FORMATION += SR_formation
			TOT_SR_BEFORE += SR_before

			output_file.write(str(u1) + '\t' + str(u2) + '\t' + str(MO_formation) + '\t' + \
				str(SR_before)+ '\t' + str(SR_formation)+ '\t' + str(SR_after) + '\n')
	print "processed %d edges " % cnt
	cnt = float(cnt)
	print "Average SR before %f, at the time %f and after %f edges formation " % \
		(TOT_SR_BEFORE/cnt, TOT_SR_FORMATION/cnt, TOT_SR_AFTER/cnt)

def extract_edge_formation_SR_with_STDEV():

	edges_MOs = defaultdict(int)
	monthly_SR = read_in_all_monthly_SR()

	output_file = open(F_OUT_CLEAN, 'w')

	cnt = 0

	TOT_SR_BEFORE = []
	TOT_SR_FORMATION = []
	TOT_SR_AFTER = []

	with codecs.open(F_IN,'r', encoding='utf8') as input_file:
		for line in input_file:
			(userA, userB, MO_formation, MO_deletion) = line.split()
			MO_formation = int(MO_formation)
			MO_deletion = int(MO_deletion)
			if MO_formation == 4 or MO_formation >= 10:
				continue
			# remove or no
			#if not(MO_deletion <= 11):
			#	continue

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
			SR_after = 0
			i = 1
			N = 7

			MO = MONTHS[i]
			while int(MO) < MO_formation:
				SR_before += monthly_SR[(u1, u2)][str(MO)]
				i += 1
				MO = MONTHS[i]

			SR_formation = monthly_SR[(u1, u2)][str(MO_formation)]

			i += 1
			while i < 6:
				MO = MONTHS[i]
				SR_after += monthly_SR[(u1, u2)][str(MO)]
				i += 1

			months_after = float(12 - int(MO_formation) - 2)
			SR_after = SR_after / months_after if months_after > 0 else 0
			months_before = float(int(MO_formation) - 2 - 4)
			SR_before = SR_before / months_before if months_before > 0 else 0

			assert months_before + months_after == 4

			TOT_SR_AFTER.append(SR_after)
			TOT_SR_FORMATION.append(SR_formation)
			TOT_SR_BEFORE.append(SR_before)

			#output_file.write(str(u1) + '\t' + str(u2) + '\t' + str(MO_formation) + '\t' + \
			#	str(SR_before)+ '\t' + str(SR_formation)+ '\t' + str(SR_after) + '\n')
	print "processed %d edges " % cnt
	cnt = float(cnt)

	TOT_SR_BEFORE = np.array(TOT_SR_BEFORE)
	TOT_SR_FORMATION = np.array(TOT_SR_FORMATION)
	TOT_SR_AFTER = np.array(TOT_SR_AFTER)

	avg_bef = np.mean(TOT_SR_BEFORE)
	stdev_bef = np.std(TOT_SR_BEFORE)

	avg_at = np.mean(TOT_SR_FORMATION)
	stdev_at = np.std(TOT_SR_FORMATION)

	avg_aft = np.mean(TOT_SR_AFTER)
	stdev_aft = np.std(TOT_SR_AFTER)

	print "Average SR %f and stdev %f before, at the time %f, %f and after %f, %f edges formation " % \
		(avg_bef, stdev_bef, avg_at, stdev_at, avg_aft, stdev_aft)

	print
	print avg_bef, avg_at, avg_aft
	print stdev_bef, stdev_at, stdev_aft


def extract_edge_formation_SR_clean_with_STDEV():

	edges_MOs = defaultdict(int)
	monthly_SR = read_in_all_monthly_SR()

	output_file = open(F_OUT_CLEAN, 'w')

	cnt = 0

	TOT_SR_BEFORE = []
	TOT_SR_FORMATION = []
	TOT_SR_AFTER = []

	with codecs.open(F_IN,'r', encoding='utf8') as input_file:
		for line in input_file:
			(userA, userB, MO_formation, MO_deletion) = line.split()
			MO_formation = int(MO_formation)

			MO_deletion = int(MO_deletion)

			if MO_formation == 4 or MO_formation >= 10:
				continue

			#if MO_deletion > 6 and MO_deletion < 10:
			#	continue

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
			SR_after = 0
			i = 1
			N = 7

			MO = MONTHS[i]
			while int(MO) < MO_formation:
				SR_before += monthly_SR[(u1, u2)][str(MO)]
				i += 1
				MO = MONTHS[i]

			SR_formation = monthly_SR[(u1, u2)][str(MO_formation)]

			i += 1
			while i < 6:
				MO = MONTHS[i]
				SR_after += monthly_SR[(u1, u2)][str(MO)]
				i += 1

			months_after = float(12 - int(MO_formation) - 2)
			SR_after = SR_after / months_after if months_after > 0 else 0
			months_before = float(int(MO_formation) - 2 - 4)
			SR_before = SR_before / months_before if months_before > 0 else 0

			assert months_before + months_after == 4

			TOT_SR_AFTER.append(SR_after)
			TOT_SR_FORMATION.append(SR_formation)
			TOT_SR_BEFORE.append(SR_before)

			#output_file.write(str(u1) + '\t' + str(u2) + '\t' + str(MO_formation) + '\t' + \
			#	str(SR_before)+ '\t' + str(SR_formation)+ '\t' + str(SR_after) + '\n')
	print "processed %d edges " % cnt
	cnt = float(cnt)

	TOT_SR_BEFORE = np.array(TOT_SR_BEFORE)
	TOT_SR_FORMATION = np.array(TOT_SR_FORMATION)
	TOT_SR_AFTER = np.array(TOT_SR_AFTER)

	avg_bef = np.mean(TOT_SR_BEFORE)
	stdev_bef = np.std(TOT_SR_BEFORE)

	avg_at = np.mean(TOT_SR_FORMATION)
	stdev_at = np.std(TOT_SR_FORMATION)

	avg_aft = np.mean(TOT_SR_AFTER)
	stdev_aft = np.std(TOT_SR_AFTER)

	print "Average SR %f and stdev %f before, at the time %f, %f and after %f, %f edges formation " % \
		(avg_bef, stdev_bef, avg_at, stdev_at, avg_aft, stdev_aft)

def read_in_all_monthly_SR():

	monthly_SR = defaultdict(dict)

	for MO in MONTHS:
		f_in_SR = "monthly_SR_change_list_of_users/" + str(MO) + "mention_edges_monthly_SR"
		f = open(f_in_SR, 'r')
		for line in f:
			(u1, u2, SR, w1, w2) = line.split()
			userA = int(u1)
			userB = int(u2)
			SR = float(SR)
			if userA < userB:
				u1 = userA
				u2 = userB
			else:
				u1 = userB
				u2 = userA
			if not (u1, u2) in monthly_SR:
				monthly_SR[(u1, u2)] = {"5":0, "6":0, "7":0, "8":0, "9":0, "10":0, "11":0}
			if monthly_SR[(u1, u2)][MO] == 0:
				monthly_SR[(u1, u2)][MO] = SR
			else:
				assert monthly_SR[(u1, u2)] == SR
		f.close()

	return monthly_SR


extract_edge_formation_SR_with_STDEV()
	









