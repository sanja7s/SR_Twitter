#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os
import matplotlib.cm as cm
from collections import defaultdict
from igraph import *

IN_DIR = "../../../DATA/taxonomy_stats/"
f_sent_in = "sentiment/user_sentiment.tab"
f_weighted_edges_in = "sentiment/mention_graph_weights.dat"

def read_in_neighborhood_sent_dir():

	f = open(f_sent_in, "r")
	G = Graph.Read_Ncol(f_weighted_edges_in,names=True, directed=True, weights=True)
	summary(G)

	G.simplify(multiple=False)
	summary(G)

	cnt = 0
	for line in f:
		(vid, vsent, vsentval) = line[:-1].split('\t')
		vsent = int(vsent)
		vsentval = float(vsentval)
		v = G.vs.select(name = vid)
		v["sent"] = vsentval
		cnt += 1
	print cnt

	to_delete_vertices = [v.index for v in G.vs if v["sent"] == None]
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	neighborhood_sent = []
	cnt_no_neighbors = 0
	for v in G.vs:
		nb = G.neighbors(v.index)
		NS = G.vs.select(nb)["sent"]
		if NS == []:
			cnt_no_neighbors += 1
			print v.index, nb
			continue
		ns = np.array(NS)
		ns_mean = np.mean(ns)
		neighborhood_sent.append((v["sent"],ns_mean))

	print cnt_no_neighbors

	return neighborhood_sent

def read_in_neighborhood_sent_recip():

	f = open(f_sent_in, "r")
	G = Graph.Read_Ncol(f_weighted_edges_in,names=True, directed=True, weights=True)
	summary(G)
	G.to_undirected(mode="mutual")
	summary(G)

	G.simplify(multiple=False)
	summary(G)

	cnt = 0
	for line in f:
		(vid, vsent, vsentval) = line[:-1].split('\t')
		vsentval = float(vsentval)
		v = G.vs.select(name = vid)
		v["sent"] = vsentval
		cnt += 1
	print cnt

	to_delete_vertices = [v.index for v in G.vs if v["sent"] == None]
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	neighborhood_sent = []
	cnt_no_neighbors = 0
	for v in G.vs:
		nb = G.neighbors(v.index)
		NS = G.vs.select(nb)["sent"]
		if NS == []:
			cnt_no_neighbors += 1
			print v.index, nb
			continue
		ns = np.array(NS)
		ns_mean = np.mean(ns)
		neighborhood_sent.append((v["sent"],ns_mean))

	print cnt_no_neighbors

	return neighborhood_sent

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
	plt.ylabel('neighborhood sentiment')

	plt.savefig("sentiment/neighborhood/" + fig_name, dpi = 200)

	#plt.show()

def scatterplot_edges_sent_hist2d_recip(edges_sent):

	heatmap, extent = get_heatmap(edges_sent)
	fig_name = "recip_neighborhood.png"
	plot_heatmap(heatmap, extent, fig_name, colmap=cm.cool)


def scatterplot_edges_sent_hist2d_dir(edges_sent):

	heatmap, extent = get_heatmap(edges_sent)
	fig_name = "dir_neighborhood.png"
	plot_heatmap(heatmap, extent, fig_name, colmap=cm.winter)



def main_pdf():
	os.chdir(IN_DIR)
	ydata = read_in_sent()
	#plot_pdf(ydata)
	plot_cum_distr(ydata)
	#plot_pdf_line(ydata)
#main_pdf()

def main_scatter_directed():
	os.chdir(IN_DIR)
	edges_sent = read_in_neighborhood_sent_dir()
	scatterplot_edges_sent_hist2d_dir(edges_sent) 
#main_scatter_directed()

def main_scatter_reciprocal():
	os.chdir(IN_DIR)
	edges_sent = read_in_neighborhood_sent_recip()
	scatterplot_edges_sent_hist2d_recip(edges_sent) 
main_scatter_reciprocal()

