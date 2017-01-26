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

def read_in_edges_SR(f2, threshold = 0):

	edges_SR = []
	edges_SR_weighted = []
	for line in f2:
		(uid1, uid2, SR, w) = line.split()
		uid1 = int(uid1)
		uid2 = int(uid2)
		w = int(w)
		SR = float(SR)
		if w > threshold:
			if uid1 != uid2:
				edges_SR.append(SR)
				for i in range(w):
					edges_SR_weighted.append(SR)

	return edges_SR, edges_SR_weighted

def read_in_full_SR(f2, threshold = 0):

	edges_SR = []

	for line in f2:
		(uid1, uid2, SR) = line.split()
		uid1 = int(uid1)
		uid2 = int(uid2)
		SR = float(SR)
		if uid1 != uid2:
			edges_SR.append(SR)
				
	return edges_SR

def plot_pdf(ydata, logscale=False):

	plt.clf()

	x = np.array(ydata) 
	#x = np.log(x + 1)
	mu = np.mean(x)
	sigma = np.std(x)

	num_bins = 100
	# the histogram of the data
	n, bins, patches = plt.hist(x, num_bins, normed=0, histtype='step', color='darkorchid', alpha=0.97)
	if logscale:
		plt.yscale('log', nonposy='clip')
	# add a 'best fit' line
	#y = mlab.normpdf(bins, mu, sigma)
	#plt.plot(bins, y, 'r--', label='Normal distribution')
	plt.xlabel('SR value')
	plt.ylabel('# edges')
	plt.title(r'Histogram for mention network pairwise SR: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$')

	plt.grid(True)
	# Tweak spacing to prevent clipping of ylabel
	plt.subplots_adjust(left=0.15)
	if logscale:
		logs = "_log"
	else:
		logs = ""
	plt.savefig("histogram_mention_SR" + logs + ".eps", dpi = 550)
	#plt.show()

def plot_both_pdf(ydata, ydata2, logscale=False):

	#plt.clf()
	print 'Plotting both'

	x = np.array(ydata) 
	#x = np.log(x + 1)
	mu = np.mean(x)
	sigma = np.std(x)

	x2 = np.array(ydata2) 
	#x = np.log(x + 1)
	mu2 = np.mean(x2)
	sigma2 = np.std(x2)

	num_bins = 100
	# the histogram of the data

	n, bins, patches = plt.hist(x, normed=1, bins=num_bins)
	plt.clf() # Get rid of this histogram since not the one we want.
	nx_frac = n/float(len(n)) # Each bin divided by total number of objects.
	width = bins[1] - bins[0] # Width of each bin.
	x = np.ravel(zip(bins[:-1], bins[:-1]+width))
	y = np.ravel(zip(nx_frac,nx_frac))



	n, bins, patches = plt.hist(x2, normed=1, bins=num_bins)
	plt.clf() # Get rid of this histogram since not the one we want.
	nx_frac = n/float(len(n)) # Each bin divided by total number of objects.
	width = bins[1] - bins[0] # Width of each bin.
	x2 = np.ravel(zip(bins[:-1], bins[:-1]+width))
	y2 = np.ravel(zip(nx_frac,nx_frac))

	lab1 = 'mention network SR: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'	
	plt.plot(x,y,linestyle="-",color='darkorchid',label=lab1)

	lab2 = 'full network SR: $\mu=' +  "{:.3f}".format(mu2) + '$, $\sigma= ' + "{:.3f}".format(sigma2) + '$'	
	plt.plot(x2,y2,linestyle="-",color='blue',label=lab2)

	if logscale:
		plt.yscale('log', nonposy='clip')

	# add a 'best fit' line
	#y = mlab.normpdf(bins, mu, sigma)
	#plt.plot(bins, y, 'r--', label='Normal distribution')
	plt.xlabel('SR')
	plt.ylabel('p(SR)')
	plt.legend()
	#plt.title(r'Histogram for mention network pairwise SR: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$')

	plt.grid(True)
	# Tweak spacing to prevent clipping of ylabel
	#plt.subplots_adjust(left=0.15)
	if logscale:
		logs = "_log"
	else:
		logs = ""
	plt.savefig("27_FIN_normed_histograms_mention_and_FULL_SR" + logs + ".eps", dpi = 550)
	
	plt.show()

def plot_pdf_line(ydata):

	plt.clf()

	x = np.array(ydata)

	mu = np.mean(x)
	sigma = np.std(x)

	num_bins = 100

	y,binEdges=np.histogram(ydata,bins=num_bins)
	bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
	plt.plot(bincenters,y,'-')
	plt.savefig("ALL_SR_line.eps", dpi = 440)

def plot_cum_distr(ydata):

	plt.clf()

	print len(ydata)

	x = np.array(ydata)

	mu = np.mean(x)
	sigma = np.std(x)

	plt.hist(x, 100, normed=0, histtype='step', color='lightsalmon', alpha=0.88, cumulative=1)


	plt.xlabel('SR value')
	plt.ylabel('SR >= x')
	plt.title(r'SR cumulative distribution: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$')

	plt.grid(True)
	# Tweak spacing to prevent clipping of ylabel
	plt.subplots_adjust(left=0.15)
	plt.savefig("ALL_SR_cum.eps", dpi = 440)
	#plt.show()

def main_pdf():

	IN_DIR = "../../../DATA/CV/"
	f_in = "mention_graph_IDs_with_SR_weight.dat"
	os.chdir(IN_DIR)
	f = open(f_in, 'r')
	edges_SR, edges_SR_weighted = read_in_edges_SR(f)
	plot_pdf(edges_SR, False)
	#plot_cum_distr(edges_SR)
	#plot_pdf_line(ydata)
#main_pdf()

def main_full_SR():

	IN_DIR = "../../../ALL_SR/"
	os.chdir(IN_DIR)
	f_in = "SMALL.weighted_edge_list"
	#f_in = 'alltest'
	f = open(f_in, 'r')
	edges_SR = read_in_full_SR(f)
	plot_pdf(edges_SR, False)
	plot_pdf(edges_SR, True)
	plot_cum_distr(edges_SR)
	plot_pdf_line(edges_SR)
#main_full_SR()


def main_both_pdf():

	IN_DIR = "../../../DATA/CV/"
	f_in = "mention_graph_IDs_with_SR_weight.dat"
	os.chdir(IN_DIR)
	f = open(f_in, 'r')
	edges_SR, edges_SR_weighted = read_in_edges_SR(f)

	IN_DIR = "../../ALL_SR/"
	os.chdir(IN_DIR)
	f_in = "SMALL.weighted_edge_list"
	#f_in = 'alltest'
	f = open(f_in, 'r')
	edges_SR_full = read_in_full_SR(f)

	plot_both_pdf(edges_SR, edges_SR_full, True)

main_both_pdf()