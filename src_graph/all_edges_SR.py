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



def read_in_all_monthly_SR():

	monthly_SR = defaultdict(dict)
	cnt_links = 0
	for MO in MONTHS:
		cnt_MO_links = 0
		f_in_SR = "monthly_SR_change_list_of_users/" + str(MO) + "mention_edges_monthly_SR"
		f = open(f_in_SR, 'r')
		for line in f:
			(u1, u2, SR, w1, w2) = line.split()
			userA = int(u1)
			userB = int(u2)
			SR = float(SR)
			#if int(w1) == 0 or int(w2) == 0:
				#print line
				#continue
			if userA < userB:
				u1 = userA
				u2 = userB
			else:
				u1 = userB
				u2 = userA
			if not (u1, u2) in monthly_SR:
				cnt_links += 1
				cnt_MO_links += 1
				monthly_SR[(u1, u2)] = {"5":0, "6":0, "7":0, "8":0, "9":0, "10":0, "11":0}
			if monthly_SR[(u1, u2)][MO] == 0:
				monthly_SR[(u1, u2)][MO] = SR
			else:
				assert monthly_SR[(u1, u2)] == SR
		f.close()
	print cnt_links
	return monthly_SR

def find_MO_avg_SR():

	monthly_SR = read_in_all_monthly_SR()

	for MO in MONTHS:
		mo_avg = []
		for up in monthly_SR:
			mo_avg.append(monthly_SR[up][MO])
		MO_AVG_fin = np.mean(np.array(mo_avg))
		print MO, len(mo_avg), MO_AVG_fin

find_MO_avg_SR()

	









