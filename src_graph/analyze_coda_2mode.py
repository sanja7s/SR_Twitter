#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	extract the 2-mode IN OUT (or OUT IN, depending on the input order) comm
	and print the PCT of such communities in the network
"""
from collections import defaultdict
import os, glob, sys

IN_DIR = "../../../DATA/mention_graph/CODA2"

os.chdir(IN_DIR)

s = []
c = []
total_comm = 0
two_mode_comm = 0
with open(sys.argv[1]) as f_res:
	for row in f_res:
		(com_in, com_out, j) = row.split()
		total_comm += 1
		if float(j) < 0.2:
			s.append((com_in, com_out, j))
			two_mode_comm += 1
		else:
			c.append((com_in, com_out, j))


print "Out of total %d found %d 2-mode comm. The pct is %f" % (total_comm, two_mode_comm, (two_mode_comm/float(total_comm)))

with open('CODA_2_mode_comm',  'w') as f_out:
	for (com_in, com_out, j) in s:
		f_out.write((str(com_in) + '\t' + str(com_out) + '\t' + str(j) + '\n'))

with open('CODA_cohesive',  'w') as f_out:
	for (com_in, com_out, j) in c:
		f_out.write((str(com_in) + '\t' + str(com_out) + '\t' + str(j) + '\n'))
