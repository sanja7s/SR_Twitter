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

IN_DIR = "../../../DATA/General/"
os.chdir(IN_DIR)

F_IN = "mention/edge_formation_deletion_MOs.dat"
F_OUT = "mention/edge_deletion_SR_stats_STRICT.dat"

MONTHS =  ["5", "6", "7", "8", "9", "10", "11"]


def read_in_all_monthly_SR():

	monthly_SR = defaultdict(dict)

	for MO in MONTHS:
		f_in_SR = "monthly_SR_change_list_of_users/" + str(MO) + "mention_edges_monthly_SR"
		f = open(f_in_SR, 'r')
		for line in f:
			(u1, u2, SR, w1, w2) = line.split()
			userA = int(u1)
			userB = int(u2)
			if userA == userB:
				#print userA
				continue
			SR = float(SR)
			if SR == 1:
				print userA, userB, SR
				#continue
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


def calculate_monthly_avg_SR_no_self_loops():
	monthly_SR = read_in_all_monthly_SR()

	avg_May = []
	avg_June = []
	avg_July = []
	avg_Aug = []
	avg_Sept = []
	avg_Oct = []
	avg_Nov = []

	cnt_edge = 0.0

	for edge in monthly_SR:
		avg_May.append(monthly_SR[edge]["5"])
		avg_June.append(monthly_SR[edge]["6"])
		avg_July.append(monthly_SR[edge]["7"])
		avg_Aug.append(monthly_SR[edge]["8"])
		avg_Sept.append(monthly_SR[edge]["9"])
		avg_Oct.append(monthly_SR[edge]["10"])
		avg_Nov.append(monthly_SR[edge]["11"])
		cnt_edge += 1

	avg_May = np.array(avg_May)
	avg_June = np.array(avg_June)
	avg_July = np.array(avg_July)
	avg_Aug = np.array(avg_Aug)
	avg_Sept = np.array(avg_Sept)
	avg_Oct = np.array(avg_Oct)
	avg_Nov = np.array(avg_Nov)

	avgM = np.mean(avg_May)
	avgJ = np.mean(avg_June)
	avgJ2 = np.mean(avg_July)
	avgA = np.mean(avg_Aug)
	avgS = np.mean(avg_Sept)
	avgO = np.mean(avg_Oct)
	avgN = np.mean(avg_Nov)

	stdevM = np.std(avg_May)
	stdevJ = np.std(avg_June)
	stdevJ2 = np.std(avg_July)
	stdevA = np.std(avg_Aug)
	stdevS = np.std(avg_Sept)
	stdevO = np.std(avg_Oct)
	stdevN = np.std(avg_Nov)

	print '%f, %f, %f, %f, %f, %f, %f' % (avgM, avgJ, avgJ2, avgA, avgS, avgO, avgN)
	print '%f, %f, %f, %f, %f, %f, %f' % (stdevM, stdevJ, stdevJ2, stdevA, stdevS, stdevO, stdevN)

calculate_monthly_avg_SR_no_self_loops()
	









