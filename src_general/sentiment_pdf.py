#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os
import matplotlib.cm as cm
from collections import defaultdict

IN_DIR = "../../../DATA/taxonomy_stats/"
f_sent_in = "sentiment/user_sentiment.tab"
f_weighted_edges_in = "sentiment/mention_graph_weights.dat"
f_recip_weighted_edges_in = "sentiment/recip_mention_graph_weights_simmetrical.dat"

def read_in_sent():

	f = open(f_sent_in, 'r')

	sent_dat = []

	for line in f:
		(uid, sent_cat, sent) = line.split()
		if float(sent) != 0:
			sent_dat.append(float(sent))

	return sent_dat

def read_in_edges_sent(f2, threshold = 0):

	f1 = open(f_sent_in, 'r')

	sent_dat = defaultdict(int)
	for line in f1:
		(uid, sent_cat, sent) = line.split()
		sent_dat[int(uid)] = float(sent)

	edges_sent_weighted = []
	edges_sent = []
	for line in f2:
		(uid1, uid2, w) = line.split()
		uid1 = int(uid1)
		uid2 = int(uid2)
		w = int(w)
		if w > threshold:
			#if sent_dat[uid1] != 0 and sent_dat[uid2] != 0 and uid1 != uid2:
			if uid1 != uid2:
				edges_sent.append((sent_dat[uid1], sent_dat[uid2]))
				for i in range(w):
					edges_sent_weighted.append((sent_dat[uid1], sent_dat[uid2]))

	return edges_sent, edges_sent_weighted

def read_in_one_side_edges_sent(f2, threshold = 0):

	f1 = open(f_sent_in, 'r')

	sent_dat = defaultdict(int)
	for line in f1:
		(uid, sent_cat, sent) = line.split()
		sent_dat[int(uid)] = float(sent)

	dir_edges = defaultdict(int)
	for line in f2:
		(uid1, uid2, w) = line.split()
		uid1 = int(uid1)
		uid2 = int(uid2)
		w = int(w)
		dir_edges[(uid1, uid2)] = w

	edges_sent_weighted = []
	edges_sent = []
	for (uid1, uid2) in dir_edges:
		if (uid2, uid1) not in dir_edges:
			if w > threshold:
				if sent_dat[uid1] != 0 and sent_dat[uid2] != 0 and uid1 != uid2:
					edges_sent.append((sent_dat[uid1], sent_dat[uid2]))
					for i in range(w):
						edges_sent_weighted.append((sent_dat[uid1], sent_dat[uid2]))

	return edges_sent, edges_sent_weighted

def plot_pdf(ydata):

	x = np.array(ydata)

	mu = np.mean(x)
	sigma = np.std(x)

	num_bins = 100
	# the histogram of the data
	n, bins, patches = plt.hist(x, num_bins, normed=1, histtype='step', color='lightsalmon', alpha=0.44)
	# add a 'best fit' line
	y = mlab.normpdf(bins, mu, sigma)
	plt.plot(bins, y, 'r--', label='Normal distribution')
	plt.xlabel('Sentiment value')
	plt.ylabel('Normed probability')
	plt.title(r'Histogram for user sentiment: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$')

	plt.grid(True)
	# Tweak spacing to prevent clipping of ylabel
	plt.subplots_adjust(left=0.15)
	plt.savefig("sentiment/histogram_user_sent.eps", dpi = 440)
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

	x = np.array(ydata)

	mu = np.mean(x)
	sigma = np.std(x)

	plt.hist(x, 100, normed=True, histtype='step', color='lightsalmon', alpha=0.44, cumulative=1)


	plt.xlabel('Sentiment value')
	plt.ylabel('Sent >= x')
	plt.title(r'Sentiment cumulative distribution: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$')

	plt.grid(True)
	# Tweak spacing to prevent clipping of ylabel
	plt.subplots_adjust(left=0.15)
	plt.savefig("sentiment/user_sent_cum.eps", dpi = 440)
	#plt.show()

def get_heatmap(edges_sent):
	xx = []
	yy = []
	for edge in edges_sent:
		xx.append(edge[0])
		yy.append(edge[1])
	xx = np.array(xx)
	yy = np.array(yy)

	heatmap, xedges, yedges = np.histogram2d(yy, xx,  bins=100) # range=([-0.6,0.7],[-0.6,0.7]),
	extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

	return heatmap, extent


def plot_heatmap(heatmap, extent, fig_name, colmap=cm.PuOr):
	plt.clf()
	plt.imshow(np.log(heatmap + 1), cmap=colmap, interpolation='nearest', extent=extent, origin = 'lower') # 
	plt.colorbar(label='log(density)')

	plt.xlabel('user A sentiment')
	plt.ylabel('user B sentiment')

	plt.savefig("sentiment/" + fig_name, dpi = 200)

	#plt.show()

def scatterplot_edges_sent_hist2d_recip(edges_sent, edges_sent_weighted):

	heatmap, extent = get_heatmap(edges_sent)
	fig_name = "recip_neutral.png"
	plot_heatmap(heatmap, extent, fig_name, colmap=cm.coolwarm)

	heatmap_w, extent_w = get_heatmap(edges_sent_weighted)
	fig_name_w = "recip_weighted_neutral.png"
	plot_heatmap(heatmap_w, extent_w, fig_name_w, colmap=cm.coolwarm)

	#heatmap_diff = np.subtract(heatmap_w, heatmap)
	#fig_name_diff = "recip_diff_th10.png"
	#plot_heatmap(heatmap_diff, extent_w, fig_name_diff, colmap=cm.coolwarm)	


def scatterplot_edges_sent_hist2d_dir(edges_sent, edges_sent_weighted):

	heatmap, extent = get_heatmap(edges_sent)
	fig_name = "dir_neutral.png"
	plot_heatmap(heatmap, extent, fig_name)

	heatmap_w, extent_w = get_heatmap(edges_sent_weighted)
	fig_name_w = "dir_weighted_neutral.png"
	plot_heatmap(heatmap_w, extent_w, fig_name_w)

	#heatmap_diff = np.subtract(heatmap_w, heatmap)
	#fig_name_diff = "dir_diff_neutral.png"
	#plot_heatmap(heatmap_diff, extent_w, fig_name_diff)

def scatterplot_edges_sent_hist2d_diff(edges_sent_dir, edges_sent_weighted_dir, edges_sent_rec, edges_sent_weighted_rec):

	heatmap_dir, extent_dir = get_heatmap(edges_sent_dir)
	heatmap_w_dir, extent_w_dir = get_heatmap(edges_sent_weighted_dir)

	heatmap_rec, extent_rec = get_heatmap(edges_sent_rec)
	heatmap_w_rec, extent_w_rec = get_heatmap(edges_sent_weighted_rec)


	heatmap_diff = np.subtract(heatmap_dir, heatmap_rec)
	fig_name_diff = "diff_dir_rec.png"
	plot_heatmap(heatmap_diff, extent_dir, fig_name_diff, colmap=cm.RdYlBu)

	heatmap_diff_w = np.subtract(heatmap_w_dir, heatmap_w_rec)
	fig_name_diff = "diff_dir_rec_weighted.png"
	plot_heatmap(heatmap_diff_w, extent_dir, fig_name_diff, colmap=cm.RdYlBu)

def scatterplot_edges_sent_diff_v2(edges_sent, edges_sent_weighted):

	heatmap, extent = get_heatmap(edges_sent)
	fig_name = "one_sided.png"
	plot_heatmap(heatmap, extent, fig_name, colmap=cm.RdGy)

	heatmap_w, extent_w = get_heatmap(edges_sent_weighted)
	fig_name_w = "one_sided_weighted.png"
	plot_heatmap(heatmap_w, extent_w, fig_name_w, colmap=cm.RdGy)

def main_pdf():
	os.chdir(IN_DIR)
	ydata = read_in_sent()
	#plot_pdf(ydata)
	plot_cum_distr(ydata)
	#plot_pdf_line(ydata)
#main_pdf()

def main_scatter_directed():
	os.chdir(IN_DIR)
	f = open(f_weighted_edges_in, 'r')
	edges_sent, edges_sent_weighted = read_in_edges_sent(f, 0)
	scatterplot_edges_sent_hist2d_dir(edges_sent, edges_sent_weighted) 
#main_scatter_directed()

def main_scatter_reciprocal():
	os.chdir(IN_DIR)
	f = open(f_recip_weighted_edges_in, 'r')
	edges_sent, edges_sent_weighted = read_in_edges_sent(f, 0)
	scatterplot_edges_sent_hist2d_recip(edges_sent, edges_sent_weighted) 
main_scatter_reciprocal()

def main_scatter_diff():
	os.chdir(IN_DIR)
	f = open(f_weighted_edges_in, 'r')
	edges_sent_dir, edges_sent_weighted_dir = read_in_edges_sent(f, 0)
 

	f = open(f_recip_weighted_edges_in, 'r')
	edges_sent_rec, edges_sent_weighted_rec = read_in_edges_sent(f, 0)

	scatterplot_edges_sent_hist2d_diff(edges_sent_dir, edges_sent_weighted_dir, edges_sent_rec, edges_sent_weighted_rec) 
#main_scatter_diff()

def main_scatter_diff_v2():
	os.chdir(IN_DIR)
	f = open(f_weighted_edges_in, 'r')
	edges_sent, edges_sent_weighted = read_in_one_side_edges_sent(f, 0)
	scatterplot_edges_sent_diff_v2(edges_sent, edges_sent_weighted) 
#main_scatter_diff_v2()