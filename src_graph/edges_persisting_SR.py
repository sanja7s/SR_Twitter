#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	from the data of edge formation/deletion, find the persisting edges and their monthly SR
"""
from collections import defaultdict
import codecs
import os
import json
import numpy as np

IN_DIR = "../../../DATA/General/"
os.chdir(IN_DIR)

F_IN = "mention/edge_formation_deletion_MOs.dat"

MONTHS =  ["5", "6", "7", "8", "9", "10", "11"]

def extract_edges_persisting_SR_with_STDEV():

	monthly_SR = read_in_all_monthly_SR()
	#output_file = open(F_OUT, 'w')

	cnt = 0
	SR = defaultdict(list)

	with codecs.open(F_IN,'r', encoding='utf8') as input_file:
		for line in input_file:
			(userA, userB, MO_formation, MO_deletion) = line.split()
			MO_formation = int(MO_formation)
			if MO_formation != 4:
				continue			
			MO_deletion = int(MO_deletion)
			if MO_deletion != 12:
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

			i = 1
			N = 7
			MO = MONTHS[i]
			while i < N-1:
				SR[MO].append(monthly_SR[(u1, u2)][str(MO)])
				i += 1
				#print i, MO
				MO = MONTHS[i]

	print "processed %d edges " % cnt
	cnt = float(cnt)

	for MO in MONTHS[:-1]:
		SR[MO] = np.array(SR[MO])
		avgSR = np.nanmean(SR[MO])
		avgSTD = np.nanstd(SR[MO])
		print SR[MO]
		print "Average SR, stdev %f, %f, at the time %s " % \
		(avgSR, avgSTD, MO)

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


extract_edges_persisting_SR_with_STDEV()
	









