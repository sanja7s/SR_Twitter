#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from collections import defaultdict, OrderedDict
import codecs
import matplotlib
import matplotlib.pyplot as plt
import pylab as P
import numpy as np
import networkx as nx
import time
import matplotlib.dates as mdates
import os
from igraph import *
from scipy.stats.stats import pearsonr

WORKING_FOLDER = "../../../DATA/mention_graph/BigClam"
os.chdir(WORKING_FOLDER)
F_IN = 'MENT_COMM7scmtyvv.txt'
f_in_graph = 'mention_graph_weights.dat'

font = {'family' : 'sans-serif',
		'variant' : 'normal',
        'weight' : 'light',
        'size'   : 14}

matplotlib.rc('font', **font)

# DONE
def output_basic_stats_BigClam_COMM():
	num_COMM = 0
	COMM_sizes = []
	input_file = codecs.open(F_IN, 'r', encoding='utf8')
	for line in input_file:
		line = line.split()
		num_COMM += 1
		COMM_sizes.append(len(line))
	print 'Read in BigClam output: %d COMM ' % (num_COMM)
	print 'Their size in decreasing order '
	print COMM_sizes
	input_file.close()

def find_nodes_in_more_COMM():
	nodes_num_COMM = defaultdict(int)
	input_file = codecs.open(F_IN, 'r', encoding='utf8')
	for line in input_file:
		line = line.split()
		for node in line:
			nodes_num_COMM[int(node)] += 1

	sorted_nodes_num_COMM = OrderedDict(sorted(nodes_num_COMM.items(), key=lambda t:t[1]))
	return sorted_nodes_num_COMM

#########################
# read from a file that is an edge list with weights
#########################
def read_in_graph():
	G = Graph.Read_Ncol(f_in_graph, directed=True, weights=True)
	print f_in_graph
	print G.summary()
	return G

#########################
# read from a file that is an edge list with SR weights
#########################
def read_in_SR_graph():
	G = Graph.Read_Ncol('undirected_mention_graph_with_SR.csv', directed=False, weights=True)
	print G.summary()
	return G

def find_avg_neighborhood_SR_per_node_COMM_membership():
	node_comm_membership = find_nodes_in_more_COMM()
	G = read_in_SR_graph()
	res = defaultdict(list)
	for node in node_comm_membership:
		n = G.vs.select(name = str(node))
		nCOMM = node_comm_membership[node] if node_comm_membership[node] < 10 else 10
		total_SR = G.strength(n[0].index, weights='weight')
		total_neighbors = G.degree(n[0].index)
		meanSR =  total_SR / float(total_neighbors)
		res[nCOMM].append(meanSR)
	res_mean = defaultdict(float)
	res_stdev = defaultdict(float)
	for COMM in res:
		res_mean[COMM] = np.mean(np.array(res[COMM]))
		res_stdev[COMM] = np.std(np.array(res[COMM]))
	return res_mean, res_stdev

def read_sem_capital(f_name='user_entities.tab', tname='entities'):
	f = open(f_name, "r")
	cap = defaultdict(int)
	cnt = 0
	for line in f:
		if tname == 'sentiment':
			(vid, vn, val) = line.split('\t')
			val = float(val)
		else:
			(vid, val) = line.split('\t')
			val = float(val)
		cap[vid] = val
		cnt += 1
	return cap

def find_avg_ST_INC_per_node_COMM_membership():
	node_comm_membership = find_nodes_in_more_COMM()
	sem_cap = read_sem_capital(f_name='status_inconsistency', tname='status_inconsistency')
	res = defaultdict(list)
	for node in node_comm_membership:
		n_sem = sem_cap[str(node)]
		nCOMM = node_comm_membership[node] if node_comm_membership[node] < 10 else 10
		res[nCOMM].append(n_sem)
	res_mean = defaultdict(float)
	res_stdev = defaultdict(float)
	for COMM in res:
		res_mean[COMM] = np.mean(np.array(res[COMM]))
		res_stdev[COMM] = np.std(np.array(res[COMM]))
	return res_mean, res_stdev

def find_MEDIAN_ST_INC_per_node_COMM_membership():
	node_comm_membership = find_nodes_in_more_COMM()
	sem_cap = read_sem_capital(f_name='status_inconsistency', tname='status_inconsistency')
	res = defaultdict(list)
	for node in node_comm_membership:
		n_sem = sem_cap[str(node)]
		nCOMM = node_comm_membership[node] if node_comm_membership[node] < 10 else 10
		res[nCOMM].append(abs(n_sem))
	res_mean = defaultdict(float)
	res_stdev = defaultdict(float)
	for COMM in res:
		res_mean[COMM] = np.median(np.array(res[COMM]))
		res_stdev[COMM] = np.std(np.array(res[COMM]))
	return res_mean, res_stdev

def find_avg_SEM_cap_per_node_COMM_membership():
	node_comm_membership = find_nodes_in_more_COMM()
	sem_cap = read_sem_capital()
	res = defaultdict(list)
	for node in node_comm_membership:
		n_sem = sem_cap[str(node)]
		nCOMM = node_comm_membership[node] if node_comm_membership[node] < 10 else 10
		res[nCOMM].append(n_sem)
	res_mean = defaultdict(float)
	res_stdev = defaultdict(float)
	for COMM in res:
		res_mean[COMM] = np.mean(np.array(res[COMM]))
		res_stdev[COMM] = np.std(np.array(res[COMM]))
	return res_mean, res_stdev

def find_avg_sentiment_per_node_COMM_membership():
	node_comm_membership = find_nodes_in_more_COMM()
	sem_cap = read_sem_capital(f_name='user_sentiment.tab', tname='sentiment')
	res = defaultdict(list)
	for node in node_comm_membership:
		n_sem = sem_cap[str(node)]
		nCOMM = node_comm_membership[node] if node_comm_membership[node] < 10 else 10
		res[nCOMM].append(n_sem)
	res_mean = defaultdict(float)
	res_stdev = defaultdict(float)
	for COMM in res:
		res_mean[COMM] = np.mean(np.array(res[COMM]))
		res_stdev[COMM] = np.std(np.array(res[COMM]))
	return res_mean, res_stdev

def find_avg_deg_per_node_COMM_membership():
	node_comm_membership = find_nodes_in_more_COMM()
	G = read_in_graph()
	G_undir = G.copy()
	# this copy is then transformed into undir weighted mutual
	G_undir.to_undirected(mode="mutual", combine_edges='sum')
	res = defaultdict(list)
	for node in node_comm_membership:
		n = G_undir.vs.select(name = str(node))
		nCOMM = node_comm_membership[node] if node_comm_membership[node] < 10 else 10
		res[nCOMM].append(G_undir.degree(n[0].index))
	res_mean = defaultdict(float)
	res_stdev = defaultdict(float)
	for COMM in res:
		res_mean[COMM] = np.mean(np.array(res[COMM]))
		res_stdev[COMM] = np.std(np.array(res[COMM]))
	return res_mean, res_stdev

def find_avg_WEIGHTED_deg_per_node_COMM_membership():
	node_comm_membership = find_nodes_in_more_COMM()
	G = read_in_graph()
	G_undir = G.copy()
	# this copy is then transformed into undir weighted mutual
	G_undir.to_undirected(mode="mutual", combine_edges='min')
	res = defaultdict(list)
	for node in node_comm_membership:
		n = G_undir.vs.select(name = str(node))
		nCOMM = node_comm_membership[node] if node_comm_membership[node] < 10 else 10
		res[nCOMM].append(G_undir.strength(n[0].index, weights='weight'))
	res_mean = defaultdict(float)
	res_stdev = defaultdict(float)
	for COMM in res:
		res_mean[COMM] = np.mean(np.array(res[COMM]))
		res_stdev[COMM] = np.std(np.array(res[COMM]))
	return res_mean, res_stdev

def find_avg_DIR_deg_per_node_COMM_membership():
	node_comm_membership = find_nodes_in_more_COMM()
	G = read_in_graph()
	res_IN = defaultdict(list)
	res_OUT = defaultdict(list)
	for node in node_comm_membership:
		n = G.vs.select(name = str(node))
		IN_deg = G.strength(n[0].index, weights='weight', mode=IN)
		OUT_deg = G.strength(n[0].index, weights='weight', mode=OUT)
		nCOMM = node_comm_membership[node] if node_comm_membership[node] < 10 else 10
		res_IN[nCOMM].append(IN_deg)
		res_OUT[nCOMM].append(OUT_deg)
	res_IN_mean = defaultdict(float)
	res_IN_std = defaultdict(float)
	res_OUT_mean = defaultdict(float)
	res_OUT_std = defaultdict(float)
	for COMM in res_IN:
		res_IN_mean[COMM] = np.mean(np.array(res_IN[COMM]))
		res_OUT_mean[COMM] = np.mean(np.array(res_OUT[COMM]))
		res_IN_std[COMM] = np.std(np.array(res_IN[COMM]))
		res_OUT_std[COMM] = np.std(np.array(res_OUT[COMM]))
	return res_IN_mean, res_IN_std, res_OUT_mean, res_OUT_std

def find_median_DIR_deg_per_node_COMM_membership():
	node_comm_membership = find_nodes_in_more_COMM()
	G = read_in_graph()
	res_IN = defaultdict(list)
	res_OUT = defaultdict(list)
	for node in node_comm_membership:
		n = G.vs.select(name = str(node))
		IN_deg = G.strength(n[0].index, weights='weight', mode=IN)
		OUT_deg = G.strength(n[0].index, weights='weight', mode=OUT)
		nCOMM = node_comm_membership[node] if node_comm_membership[node] < 10 else 10
		res_IN[nCOMM].append(IN_deg)
		res_OUT[nCOMM].append(OUT_deg)
	res_IN_m = defaultdict(float)
	res_IN_std = defaultdict(float)
	res_OUT_m = defaultdict(float)
	res_OUT_std = defaultdict(float)
	for COMM in res_IN:
		res_IN_m[COMM] = np.median(np.array(res_IN[COMM]))
		res_OUT_m[COMM] = np.median(np.array(res_OUT[COMM]))
		res_IN_std[COMM] = np.std(np.array(res_IN[COMM]))
		res_OUT_std[COMM] = np.std(np.array(res_OUT[COMM]))
	return res_IN_m, res_IN_std, res_OUT_m, res_OUT_std

def calculate_pdf(ydata, logscale=True):
	x = np.array(ydata) 
	mu = np.mean(x)
	sigma = np.std(x)
	print '$\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'	
	lab = ' $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'
	num_bins = 14
	# the histogram of the data
	n, bins, patches = plt.hist(x, normed=1, bins=num_bins)
	plt.clf() # Get rid of this histogram since not the one we want.
	nx_frac = n/float(len(n)) # Each bin divided by total number of objects.
	width = bins[1] - bins[0] # Width of each bin.
	x = np.ravel(zip(bins[:-1], bins[:-1]+width))
	y = np.ravel(zip(nx_frac,nx_frac))
	return x, y, lab

def plot_pdf_node_in_COMM():
	node_in_COMM = find_nodes_in_more_COMM()
	ydata = node_in_COMM.values()
	x, y,lab = calculate_pdf(ydata)
	plt.plot(x,y,linestyle="-",color='red',label='node comm membership ' + lab)
	plt.yscale('log', nonposy='clip')
	plt.xlabel('# comm')
	plt.ylabel('p(# comm)')
	plt.legend(loc='best')
	plt.xlim(1,15)
	#plt.title(r'Histogram for mention network pairwise SR: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$')
	plt.grid(True)
	plt.savefig('node_comm_membership_pdf.eps', dpi=550)

def plot_deg_vs_COMM_membership():
	d, std = find_avg_deg_per_node_COMM_membership()
	x = d.keys()
	y = d.values()
	e = std.values()
	plt.errorbar(x,y,e,linestyle="-",marker='*',color='red',label='mean contacts per comm membership ')
	#plt.yscale('log', nonposy='clip')
	plt.xlabel('node comm membership')
	plt.ylabel('mean node contacts')
	plt.legend(loc='best',frameon=False)
	plt.xlim(0,11)
	#plt.title(r'Histogram for mention network pairwise SR: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$')
	plt.grid(True)
	plt.savefig('node_comm_membership_vs_avg_deg4.eps', dpi=550)
	plt.show()

def plot_WEIGHTED_deg_vs_COMM_membership():
	d, std = find_avg_WEIGHTED_deg_per_node_COMM_membership()
	x = d.keys()
	y = d.values()
	e = std.values()
	print 'Corrcoef strong commun int and comm membership ',  pearsonr(np.array(x), np.array(y))
	plt.errorbar(x,y,e,linestyle="-",marker='*',color='maroon',label='mean strong communication intensity')
	#plt.yscale('log', nonposy='clip')
	plt.xlabel('node comm membership')
	plt.ylabel('mean strong communication intensity')
	plt.legend(loc='best',frameon=False)
	plt.xlim(0,11)
	#plt.title(r'Histogram for mention network pairwise SR: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$')
	plt.grid(True)
	plt.savefig('node_comm_membership_vs_mean_strong_comm_intensity2.eps', dpi=550)
	plt.show()

def plot_avg_neighborhood_SR_vs_COMM_membership():
	d, std = find_avg_neighborhood_SR_per_node_COMM_membership()
	x = d.keys()
	y = d.values()
	e = std.values()
	print 'Corrcoef SR and comm membership ',  pearsonr(np.array(x), np.array(y))
	plt.errorbar(x,y,e,linestyle="-",marker='*',color='darkgreen',label='mean node neighborhood SR per comm membership ')
	#plt.yscale('log', nonposy='clip')
	plt.xlabel('node comm membership')
	plt.ylabel('mean node SR with neighbors')
	plt.legend(loc='best',frameon=False)
	plt.xlim(0,11)
	#plt.title(r'Histogram for mention network pairwise SR: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$')
	#plt.grid(True)
	plt.savefig('node_comm_membership_vs_mean_SR.eps', dpi=550)
	plt.show()

def plot_SEM_CAP_vs_COMM_membership():
	d, std = find_avg_SEM_cap_per_node_COMM_membership()
	x = d.keys()
	y = d.values()
	e = std.values()
	plt.errorbar(x,y,e,linestyle="-",marker='*',color='darkred',label='mean sem capital per comm membership ')
	#plt.yscale('log', nonposy='clip')
	plt.xlabel('node comm membership')
	plt.ylabel('mean node semantic capital')
	plt.legend(loc=2,frameon=False)
	plt.xlim(0,11)
	#plt.title(r'Histogram for mention network pairwise SR: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$')
	#plt.grid(True)
	plt.savefig('node_comm_membership_vs_avg_SEM_CAP5.eps', dpi=550)
	plt.show()

def plot_ST_INC_vs_COMM_membership():
	d, std = find_avg_ST_INC_per_node_COMM_membership()
	x = d.keys()
	y = d.values()
	e = std.values()
	print 'Corrcoef ST INC and comm membership ',  pearsonr(np.array(x), np.array(y))
	plt.errorbar(x,y,e,linestyle="-",marker='*',color='darkcyan',label='mean status inconsistency per comm membership ')
	#plt.yscale('log', nonposy='clip')
	plt.xlabel('node comm membership')
	plt.ylabel('mean node status inconsistency')
	plt.legend(loc=2,frameon=False)
	plt.xlim(0,11)
	#plt.title(r'Histogram for mention network pairwise SR: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$')
	#plt.grid(True)
	plt.savefig('node_comm_membership_vs_mean_ST_INC2.eps', dpi=550)
	plt.show()

def plot_MEDIAN_ST_INC_vs_COMM_membership():
	d, std = find_avg_ST_INC_per_node_COMM_membership()
	x = d.keys()
	y = d.values()
	e = std.values()
	print 'Corrcoef MEDIAN ST INC and comm membership ',  pearsonr(np.array(x), np.array(y))
	plt.errorbar(x,y,e,linestyle="-",marker='*',color='darkcyan',label='median status inconsistency per comm membership ')
	#plt.yscale('log', nonposy='clip')
	plt.xlabel('node comm membership')
	plt.ylabel('median node status inconsistency')
	plt.legend(loc=2,frameon=False)
	plt.xlim(0,11)
	#plt.title(r'Histogram for mention network pairwise SR: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$')
	#plt.grid(True)
	plt.savefig('node_comm_membership_vs_MEDIAN_ST_INC2.eps', dpi=550)
	plt.show()

def plot_sentiment_vs_COMM_membership():
	d, std = find_avg_sentiment_per_node_COMM_membership()
	x = d.keys()
	y = d.values()
	e = std.values()
	print 'Corrcoef sentiment and comm membership ',  pearsonr(np.array(x), np.array(y))
	plt.errorbar(x,y,e,linestyle="-",marker='*',color='darkcyan',label='mean sentiment per comm membership ')
	#plt.yscale('log', nonposy='clip')
	plt.xlabel('node comm membership')
	plt.ylabel('mean node sentiment')
	plt.legend(loc=2,frameon=False)
	plt.xlim(0,11)
	#plt.title(r'Histogram for mention network pairwise SR: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$')
	#plt.grid(True)
	plt.savefig('node_comm_membership_vs_avg_sentiment.eps', dpi=550)
	plt.show()

def plot_DIR_deg_vs_COMM_membership():
	rIN_deg, rIN_std, rOUT_deg, rOUT_std = find_avg_DIR_deg_per_node_COMM_membership()
	x1 = rIN_deg.keys()
	y1 = rIN_deg.values()
	e1 = rIN_std.values()
	print 'Corrcoef weighted INdeg and comm membership ',  pearsonr(np.array(x1), np.array(y1))
	x2 = rOUT_deg.keys()
	y2 = rOUT_deg.values()
	e2 = rOUT_std.values()
	print 'Corrcoef weighted OUTdeg and comm membership ',  pearsonr(np.array(x2), np.array(y2))
	plt.errorbar(x1,y1,e1,linestyle="-",marker='*',color='darkred',label='mean popularity per comm membership ')
	plt.errorbar(x2,y2,e2,linestyle="-",marker='*',color='darkblue',label='mean activity per comm membership ')
	plt.xlabel('node comm membership')
	plt.ylabel('mean node social capital')
	plt.legend(loc='best',frameon=False)
	plt.xlim(0,11)
	#plt.grid(True)
	plt.savefig('node_comm_membership_vs_avg_DIR_deg3.eps', dpi=550)
	plt.show()

def plot_MEDIAN_DIR_deg_vs_COMM_membership():
	rIN_deg, rIN_std, rOUT_deg, rOUT_std = find_median_DIR_deg_per_node_COMM_membership()
	x1 = rIN_deg.keys()
	y1 = rIN_deg.values()
	e1 = rIN_std.values()
	x2 = rOUT_deg.keys()
	y2 = rOUT_deg.values()
	e2 = rOUT_std.values()
	plt.errorbar(x1,y1,e1,linestyle="-",marker='*',color='darkred',label='median popularity per comm membership ')
	plt.errorbar(x2,y2,e2,linestyle="-",marker='*',color='darkblue',label='median activity per comm membership ')
	plt.xlabel('node comm membership')
	plt.ylabel('median node social capital')
	plt.legend(loc='best',frameon=False)
	plt.xlim(0,11)
	#plt.grid(True)
	plt.savefig('node_comm_membership_vs_MEDIAN_DIR_deg3.eps', dpi=550)
	plt.show()

#plot_WEIGHTED_deg_vs_COMM_membership()
plot_MEDIAN_ST_INC_vs_COMM_membership()
#plot_sentiment_vs_COMM_membership()
plot_avg_neighborhood_SR_vs_COMM_membership()
#plot_SEM_CAP_vs_COMM_membership()
plot_DIR_deg_vs_COMM_membership()
#plot_MEDIAN_DIR_deg_vs_COMM_membership()
#plot_deg_vs_COMM_membership()
#output_basic_stats_BigClam_COMM()
#find_nodes_in_more_COMM()
#plot_pdf_node_in_COMM()
