#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	from the month of edge deletion, find the SR before, at the time and after
"""
from collections import defaultdict
import codecs
import os
import json

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

	avg_May = 0
	avg_June = 0
	avg_July = 0
	avg_Aug = 0
	avg_Sept = 0
	avg_Oct = 0
	avg_Nov = 0

	cnt_edge = 0.0

	for edge in monthly_SR:
		avg_May += monthly_SR[edge]["5"]
		avg_June += monthly_SR[edge]["6"]
		avg_July += monthly_SR[edge]["7"]
		avg_Aug += monthly_SR[edge]["8"]
		avg_Sept += monthly_SR[edge]["9"]
		avg_Oct += monthly_SR[edge]["10"]
		avg_Nov += monthly_SR[edge]["11"]
		cnt_edge += 1

	print "Average edge SR (no self loops) is %f %f %f %f %f %f %f" % \
		(avg_May/cnt_edge, avg_June/cnt_edge, avg_July/cnt_edge, avg_Aug/cnt_edge, avg_Sept/cnt_edge, avg_Oct/cnt_edge, avg_Nov/cnt_edge)

calculate_monthly_avg_SR_no_self_loops()
	









