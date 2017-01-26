#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	plot the results from the files igraph_degree_assort_study and degree_assortativity
'''
from igraph import *
import os
import numpy as np
import matplotlib.pyplot as plt
#########################

IN_DIR = '/home/sscepano/Projects7s/Twitter-workspace/ALL_SR'
img_out_plot = "7MOda_unweighted.png"
#########################

#########################
# read from a file the res
#########################
def read_in_res():
	f = open('7MODeg_assort_study.weighted_edge_list', 'r')

	DA = []
	TH = []

	for line in f:
		if line.startswith('stats for'):
			th = float(line.split()[-1])
			TH.append(th)
		if line.startswith('The network is'):
			da = float(line.split()[-1])
			DA.append(da)
	th_last = th
	
	f2 = open('plot_da_0.2.txt', 'r')
	for line in f2:
		(th, da) = line.split()
		th = float(th)
		if th < th_last:
			continue
		da = float(da)
		TH.append(th)
		DA.append(da)

	f3 = open('DA_SR_th.tab', 'w')
	for i in range(len(TH)):
		f3.write(str(TH[i]) + '\t' + str(DA[i]) + '\n')


	return TH, DA


def plot_DA(xaxis, da):
	x = np.array(xaxis)
	y = np.array(da)
	plt.plot(x, y, 'c')
	plt.grid(True)
	plt.title('SR network')
	#plt.legend(bbox_to_anchor=(0, 1), bbox_transform=plt.gcf().transFigure)
	plt.ylabel('degree assortativity')
	plt.xlabel('SR threshold')
	plt.savefig(img_out_plot,format='png',dpi=200)


def main():
	os.chdir(IN_DIR)
	x, DA = read_in_res()
	plot_DA(x, DA)

main()