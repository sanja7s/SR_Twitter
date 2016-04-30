#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
	Given a set of communities, plot average SR against their size
"""

import matplotlib
import math
import numpy as np
from matplotlib import pyplot as plt
import os

IN_DIR = "../../../DATA/taxonomy_stats"
os.chdir(IN_DIR)

def hist_full_SR():

	sizeN = 20

	f_in_name = "AVG_SR_MENT_COMM/mention_COMM_AVG_SR_size_" + str(sizeN) + ".tab"

	AVG = []
	STD = []

	f = open(f_in_name, 'r')
	for line in f:
		(comm, avg, std) = line.split()
		AVG.append(float(avg))
		STD.append(float(std))


	plt.hist(AVG)
	plt.show()



def plot_ALL_SR():

	sizeN = 20
	f_in_name = "AVG_SR_MENT_COMM/mention_COMM_AVG_SR_ALL_size_" + str(sizeN) + "_v2.tab"

	mentAVG = []
	mentSTD = []
	fullAVG = []
	fullSTD = []
	rndAVG = []
	rndSTD = []

	x = []


	f = open(f_in_name, 'r')
	for line in f:
		(com, size, full_avg, full_std, ment_avg, ment_std, rnd_full_avg, rnd_full_std, rnd_ment_avg, rnd_ment_std) = line.split()
		fullAVG.append(float(full_avg))
		fullSTD.append(float(full_std))
		mentAVG.append(float(ment_avg))
		mentSTD.append(float(ment_std))
		rndAVG.append(float(rnd_full_avg))
		rndSTD.append(float(rnd_full_std))

		x.append(int(size))

	plt.loglog(x, mentAVG, '*', label = 'mention edges')
	plt.loglog(x, fullAVG, '+', label = 'full subgraph')
	plt.loglog(x, rndAVG, '.', label = 'rnd full subgraph')

	plt.xlabel('comm size')
	plt.ylabel('Avg SR')

	plt.legend()
	#plt.show()

	plt.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/taxonomy_stats/AVG_SR_MENT_COMM/comm_avg_SR_v3.png")


plot_ALL_SR()