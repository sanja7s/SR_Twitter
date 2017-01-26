#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os
import matplotlib.cm as cm
from collections import defaultdict
import matplotlib

font = {'family' : 'sans-serif',
		'variant' : 'normal',
		'weight' : 'light',
		'size'   : 14}

matplotlib.rc('font', **font)

IN_DIR = "../../../DATA/General/"
os.chdir(IN_DIR)

MONTHS =  ["5", "6", "7", "8", "9", "10", "11"]
MONTHS2 =  ["6", "7", "8", "9", "10"]
MONTHS_name =  {"5":"May", "6":"Jun", "7":"Jul", "8":"August", "9":"Sept", "10":"Oct", "11":"Nov"}

parts =  ["0", "1", "2", "3", "4", "5", "6", "7"]

import matplotlib.colors as colors
import matplotlib.cm as cmx
cmBlues = plt.get_cmap('Blues') 
cmReds = plt.get_cmap('Reds') 
cNorm  = colors.Normalize(vmin=5, vmax=10) # 11 for all MOs
scalarMapBlues = cmx.ScalarMappable(norm=cNorm, cmap=cmBlues)
scalarMapReds = cmx.ScalarMappable(norm=cNorm, cmap=cmReds)

def read_in_MENT_SR(f2, threshold = 0):
	cnt_MO_edges = 0
	edges_SR = []
	for line in f2:
		(uid1, uid2, SR, w1, w2) = line.split()
		uid1 = int(uid1)
		uid2 = int(uid2)
		if int(w1) == 0 or int(w2) == 0:
			continue
		cnt_MO_edges += 1
		SR = float(SR)
		if uid1 != uid2:
			edges_SR.append(SR)
	print 'Monthly edges ', cnt_MO_edges
	return edges_SR

def read_in_full_SR(f_name, threshold = 0):
	edges_SR = []
	for s in parts:
		f = open(f_name + s, 'r')
		for line in f:
			(uid1, uid2, SR) = line.split()
			uid1 = int(uid1)
			uid2 = int(uid2)
			SR = float(SR)
			if uid1 != uid2:
				edges_SR.append(SR)
		f.close()
		print 'part ', s, ' read'				
	return edges_SR

def calculate_pdf(MO, ydata, logscale=True):
	print 'Calculating ', MO
	x = np.array(ydata) 
	mu = np.mean(x)
	sigma = np.std(x)
	print MO + ' mention network SR: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'	
	lab = MONTHS_name[MO] + ' $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'
	num_bins = 100
	# the histogram of the data
	n, bins, patches = plt.hist(x, normed=1, bins=num_bins)
	plt.clf() # Get rid of this histogram since not the one we want.
	nx_frac = n/float(len(n)) # Each bin divided by total number of objects.
	width = bins[1] - bins[0] # Width of each bin.
	x = np.ravel(zip(bins[:-1], bins[:-1]+width))
	y = np.ravel(zip(nx_frac,nx_frac))
	return x, y, lab

def plot_one(MO, x, y, lab, c):
	plt.plot(x,y,linestyle="-",color=c,label=lab)
	plt.yscale('log', nonposy='clip')
	plt.xlabel('SR')
	plt.ylabel('p(SR)')
	plt.legend(loc='best')
	#plt.title(r'Histogram for mention network pairwise SR: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$')
	plt.grid(True)
	
def main_MENT_pdf_MO():
	IN_DIR = "monthly_SR_change_list_of_users/"
	os.chdir(IN_DIR)
	x = defaultdict(list)
	y = defaultdict(list)
	l = defaultdict(str)
	for MO in MONTHS2:
		f = open(str(MO) + "mention_edges_monthly_SR", "r")
		edges_SR_MENT = read_in_MENT_SR(f)
		x[MO], y[MO], l[MO] = calculate_pdf(MO, edges_SR_MENT)

	for MO in MONTHS2:
		c = scalarMapBlues.to_rgba(int(MO))
		plot_one(MO, x[MO], y[MO], l[MO], c)	
	
	os.chdir("../")
	plt.savefig("MO_MENT_SR_FIN_7s.eps", dpi = 550)

def main_SR_pdf_MO():
	x = defaultdict(list)
	y = defaultdict(list)
	l = defaultdict(str)
	for MO in MONTHS2:
		fn = MO + 'MOSR/' + MO + '_all_user_SR_part_'
		edges_SR_SR = read_in_full_SR(fn)
		x[MO], y[MO], l[MO] = calculate_pdf(MO, edges_SR_SR)

	for MO in MONTHS2:
		c = scalarMapReds.to_rgba(int(MO))
		plot_one(MO, x[MO], y[MO], l[MO], c)	

	plt.savefig("MO_SR_SR_hist_FIN_7s.eps", dpi = 550)

main_SR_pdf_MO()
main_MENT_pdf_MO()