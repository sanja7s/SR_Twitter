#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	plot the results from the files igraph_degree_assort_study where we have also
	the data that enable us to calculate density
'''
from igraph import *
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

font = {'family' : 'sans-serif',
		'variant' : 'normal',
		'weight' : 'light',
		'size'   : 14}

matplotlib.rc('font', **font)
#########################

IN_DIR = '/home/sscepano/Projects7s/Twitter-workspace/ALL_SR'
img_out_plot = "SR_density.eps"
#########################

#########################
# read from a file the res
#########################
def read_in_res():
	f = open('Deg_assort_study.weighted_edge_list', 'r')

	ALL_NODES = 29611

	DE = []
	DE1 = []
	TH = []
	NODES = []
	ALL_EDGES = (ALL_NODES * (ALL_NODES-1)) / 2

	for line in f:
		if line.startswith('stats for'):
			th = float(line.split()[-1])
			TH.append(th)
		if line.startswith('IGRAPH'):
			line = line.split()
			nodes = float(line[2])
			NODES.append(nodes)
			edges = float(line[3])
			de = (2 * edges) / (nodes * (nodes-1))
			DE.append(de)
			de1 = (edges) / ALL_EDGES
			DE1.append(de1)
	th_last = th

	print len(TH), len(DE)
	
	f3 = open('Density_largest_comp_SR_th.tab', 'w')
	f4 = open('Density_SR_th.tab', 'w')
	for i in range(len(TH)):
		f3.write(str(TH[i]) + '\t' + str(DE[i]) + '\n')
		f4.write(str(TH[i]) + '\t' + str(DE1[i]) + '\n')
	return TH, DE, DE1, NODES

def plot_DE(xaxis, da1, da, no, label1, label, col1, col):
	fig, ax1 = plt.subplots()
	x = np.array(xaxis)
	y = np.array(da)
	y1 = np.array(da1)
	ax1.plot(x, y, col, label=label)
	ax1.plot(x, y1, col1, label=label1)
	ax1.set_xlabel('$SR_{th}$')
	ax1.set_ylabel('Density', color = 'm')
	for tl in ax1.get_yticklabels():
	    tl.set_color('m')
	#plt.grid(True)
	plt.yscale('log', nonposy='clip')
	ax1.legend(loc=3, frameon=False)
	
	ax2 = ax1.twinx()
	y3 = np.array(no)
	ax2.plot(x, y3/1000, 'c+', label='size of largest comp.')
	ax2.set_ylabel('# nodes (in thousands)', color = 'c')
	for tl in ax2.get_yticklabels():
	    tl.set_color('c')
	ax2.legend(frameon=False)

	#plt.show()
	plt.savefig(img_out_plot,format='eps',dpi=550)


def main():
	os.chdir(IN_DIR)
	x, DE, DE1, NODES = read_in_res()
	plot_DE(x, DE1, DE, NODES, label1 = 'whole SR network', \
		 label = 'largest conn. comp.', col1 = 'm^', col = 'm*')

main()