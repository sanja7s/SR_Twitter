#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	go through user monthly counts per edge (userA --> userB) that is
	in a json file formatted as { (userA, userB) :  5:x5, 6:x6, ..., 11:x11}
	# and merge them to undirected and
	extract edge formation data 
"""
from collections import defaultdict
import codecs
encoding = "ascii"
import os
import json

IN_DIR = "../../../DATA/General/"
os.chdir(IN_DIR)

F_IN = "mention/monthly_edges_weight_IDs_7s.dat"
F_OUT = "mention/edge_formation_mention.dat"

def extract_edge_formation():

	edges_undir = defaultdict(list)
	cnt = 0

	with codecs.open(F_IN,'r', encoding='utf8') as input_file:
		# the code loops through the input, collects tweets text for each user into a dict
		for line in input_file:	
			cnt += 1
			line = json.loads(line)
			edge = eval(line['_id']) 
			monthly_mentions = dict(line['monthly_weights'])
			userA = int(edge[0])
			userB = int(edge[1])
			if userA < userB:
				u1 = userA
				u2 = userB
			else:
				u1 = userB
				u2 = userA

			if (u1, u2) not in edges_undir:
				edges_undir[(u1, u2)] = [0,0,0,0,0,0,0] 

			for i in range(7):
				bit = monthly_mentions[str(i+5)] > 0 
				edges_undir[(u1, u2)][i] += bit


			if cnt % 500 == 0:
				print cnt, line
	print "Processed %d tweets" % (cnt)
	print "Total edges %d in the dict " % len(edges_undir)

	output_file = open(F_OUT, 'w')
	for edge in edges_undir:

		output_file.write(str(edge[0]) + '\t' + str(edge[1]) + '\t' +str(edges_undir[edge]) + '\n')


extract_edge_formation()
	









