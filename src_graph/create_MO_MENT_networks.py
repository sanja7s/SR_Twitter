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

IN_DIR = "../../../DATA/General/MO_MENT_networks"
os.chdir(IN_DIR)

F_IN = "mention_edges_monthly_SR"
F_OUT = "mention_network_dir_w"

MONTHS =  ["5", "6", "7", "8", "9", "10", "11"]

def read_in_monthly_mentions(MO):
	monthly_ment = defaultdict(dict)
	f_in = str(MO) + "mention_edges_monthly_SR"
	f = open(f_in, 'r')
	for line in f:
		(u1, u2, SR, w1, w2) = line.split()
		userA = int(u1)
		userB = int(u2)
		w1 = int(w1)
		w2 = int(w2)
		if w1 > 0:
			monthly_ment[(u1, u2)] = w1
		if w2 > 0:
			monthly_ment[(u2, u1)] = w2
	f.close()
	return monthly_ment

def save_monthly_network_dir_w(MO):
	monthly_ment = read_in_monthly_mentions(MO)
	f_out = str(MO) + "mention_edgelist_dir_w"
	f = open(f_out, 'w')
	for el in monthly_ment:
		userA = el[0]
		userB = el[1]
		w = monthly_ment[el]
		f.write(str(userA) + '\t' + str(userB) + '\t' + str(w) + '\n')
	f.close()

for MO in MONTHS:
	save_monthly_network_dir_w(MO)
	









