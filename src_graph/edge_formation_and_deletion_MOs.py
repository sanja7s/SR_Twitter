#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	from the edge formation matrix, extract the month of edge formation and deletion
	edge is formed if in two months there was no and then afterwards reciprocal interaction appeared
	edge is deleted if in our dataset there was reciprocal interaction and then it stopped in the last 2 months at least
"""
from collections import defaultdict
import codecs
import os
import json

IN_DIR = "../../../DATA/General/"
os.chdir(IN_DIR)

F_IN = "mention/edge_formation_mention.dat"
F_OUT = "mention/edge_formation_deletion_MOs.dat"

def edge_formation_MO(l):

	if l[0] == 2 or l[1] == 2:
		return 4
	for i in range(2,len(l)):
		if l[i] == 2:
			return i+5
	return 12

def edge_deletion_MO(l):

	N = len(l)
	if l[N-1] == 2 or l[N-2] == 2:
		return 12
	for i in range(N-3, -1, -1):
		if l[i] == 2:
			return i+5
	return 4

def extract_edge_formation_deletion_MOs():

	edges_MOs = defaultdict(list)
	cnt = 0

	cnt_formation = 0
	cnt_deletion = 0
	cnt_formation_deletion = 0

	output_file = open(F_OUT, 'w')

	with codecs.open(F_IN,'r', encoding='utf8') as input_file:
		# the code loops through the input, collects tweets text for each user into a dict
		for line in input_file:	
			cnt += 1
			(uid1, uid2, edge_months_list) = line.split('\t')
			edge_months_list = eval(edge_months_list) 
			userA = int(uid1)
			userB = int(uid2)
			MO_formation = edge_formation_MO(edge_months_list)
			MO_deletion = edge_deletion_MO(edge_months_list)
			
			edge_formed = False
			edge_deleted = False

			output_file.write(str(userA) + '\t' + str(userB) + '\t' \
				+ str(MO_formation) + '\t' \
				+ str(MO_deletion) + '\n')
			if MO_formation > 4 and MO_formation < 12:
				cnt_formation += 1
				edge_formed = True
			if MO_deletion > 4 and MO_deletion < 12:
				cnt_deletion += 1
				edge_deleted = True
			if edge_formed and edge_deleted:
				cnt_formation_deletion += 1



	print "Processed %d edges" % (cnt)
	print "Total edges with formation %d, with deletion %d, and both %d " \
		% (cnt_formation, cnt_deletion, cnt_formation_deletion)


extract_edge_formation_deletion_MOs()
	









