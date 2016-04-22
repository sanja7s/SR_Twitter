#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	from the month of edge formation, find the SR before, at the time and after
"""
from collections import defaultdict
import codecs
import os
import json

IN_DIR = "../../../DATA/General/"
os.chdir(IN_DIR)

F_IN = "mention/edge_formation_deletion_MOs.dat"
F_OUT = "mention/edge_formation_and_deletion_SR_stats_STRICT.dat"

MONTHS =  ["5", "6", "7", "8", "9", "10", "11"]

def extract_edge_formation_and_deletion_SR():

	edges_MOs = defaultdict(int)
	monthly_SR = read_in_all_monthly_SR()

	output_file = open(F_OUT, 'w')

	cnt = 0

	TOT_SR_BEFORE = 0
	TOT_SR_FORMATION = 0
	TOT_SR_MID = 0
	TOT_SR_DELETION = 0
	TOT_SR_AFTER = 0

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

			i = 1
			N = 7
			MO = MONTHS[i]
			while int(MO) < MO_formation:
				SR_before += monthly_SR[(u1, u2)][str(MO)]
				i += 1
				MO = MONTHS[i]

			SR_formation = monthly_SR[(u1, u2)][str(MO_formation)]

			#i += 1
			while i < MO_deletion-5+1:
				MO = MONTHS[i]
				SR_mid += monthly_SR[(u1, u2)][str(MO)]
				i += 1

			SR_deletion = monthly_SR[(u1, u2)][str(MO_deletion)]

			"""
			if MO_formation == MO_deletion:
				assert i - 1 == MO_deletion - 5
				SR_mid += SR_formation
				assert SR_formation == SR_deletion
			"""

			i += 1
			while i < 6:
				MO = MONTHS[i]
				SR_after += monthly_SR[(u1, u2)][str(MO)]
				i += 1

			months_before = float(int(MO_formation) - 2 - 4)
			SR_before = SR_before / months_before if months_before > 0 else 0

			months_mid = float(int(MO_deletion) - int(MO_formation) + 1)
			SR_mid = SR_mid / months_mid 

			months_after = float(12 - int(MO_deletion) - 2)
			SR_after = SR_after / months_after if months_after > 0 else 0

			print months_before, months_mid, months_after
			assert months_before + months_after + months_mid == 5

			TOT_SR_BEFORE += SR_before
			TOT_SR_FORMATION += SR_formation
			TOT_SR_MID += SR_mid
			TOT_SR_DELETION += SR_deletion
			TOT_SR_AFTER += SR_after
			
			output_file.write(str(u1) + '\t' + str(u2) + '\t' + str(MO_formation) + '\t' + \
				str(SR_before)+ '\t' + str(SR_formation)+ '\t' + str(SR_mid) + '\t' + \
				str(SR_deletion)+ '\t' + str(SR_after) + '\n')
	print "processed %d edges " % cnt
	cnt = float(cnt)
	print "Average SR before %f, at the time %f of formation, in the middle %f, at deletion %f and after %f edges formation " % \
		(TOT_SR_BEFORE/cnt, TOT_SR_FORMATION/cnt, TOT_SR_MID/cnt, \
			TOT_SR_DELETION/cnt, TOT_SR_AFTER/cnt)

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


extract_edge_formation_and_deletion_SR()
	









