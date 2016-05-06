#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os
import matplotlib.cm as cm
from collections import defaultdict

IN_DIR = "../../../DATA/CV/"
f_in = "mention_graph_IDs_with_SR_weight.dat"

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

def plot_pdf(ydata, logscale=False):

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
	plt.title(r'Histogram for user pairwise SR: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$')

	plt.grid(True)
	# Tweak spacing to prevent clipping of ylabel
	plt.subplots_adjust(left=0.15)
	if logscale:
		logs = "_log"
	else:
		logs = ""
	plt.savefig("histogram_pairwise_SR" + logs + ".png", dpi = 200)
	#plt.show()

def plot_pdf_line(ydata):

	x = np.array(ydata)

	mu = np.mean(x)
	sigma = np.std(x)

	num_bins = 100

	y,binEdges=np.histogram(ydata,bins=num_bins)
	bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
	plt.plot(bincenters,y,'-')
	plt.show()

def plot_cum_distr(ydata):

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
	plt.savefig("SR_cum.eps", dpi = 440)
	#plt.show()



def main_pdf():
	os.chdir(IN_DIR)
	f = open(f_in, 'r')
	edges_SR, edges_SR_weighted = read_in_edges_SR(f)
	#plot_pdf(edges_SR, False)
	#plot_cum_distr(edges_SR)
	#plot_pdf_line(ydata)
main_pdf()

