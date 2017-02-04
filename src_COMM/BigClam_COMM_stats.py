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
from scipy import stats

WORKING_FOLDER = "../../../DATA/mention_graph/BigClam"
os.chdir(WORKING_FOLDER)
F_IN = 'MENT_COMM7scmtyvv.txt'
f_in_graph = 'mention_graph_weights.dat'

font = {'family' : 'sans-serif',
		'variant' : 'normal',
        'weight' : 'light',
        'size'   : 24}

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
	print sorted(COMM_sizes)
	print sum(COMM_sizes)
	input_file.close()

def find_nodes_in_more_COMM():
	nodes_num_COMM = defaultdict(int)
	input_file = codecs.open(F_IN, 'r', encoding='utf8')
	for line in input_file:
		line = line.split()
		for node in line:
			nodes_num_COMM[int(node)] += 1

	#nodes_num_COMM2 = {node: nodes_num_COMM[node] if nodes_num_COMM[node] < 10 else 10 for node in nodes_num_COMM}
	sorted_nodes_num_COMM = OrderedDict(sorted(nodes_num_COMM.items(), key=lambda t:t[1]))
	return sorted_nodes_num_COMM

def read_in_mention_graph():

	d = defaultdict(int)

	fn = 'mention_graph_weights.dat'
	f = open(fn, 'r')

	for line in f:
		(u1, u2, w) = line.split()
		#print u1, u2, w

		d[int(u1), int(u2)] = int(w)
	return d


def read_in_mention_graph_undir():

	d = defaultdict(int)

	fn = 'undirected_mention_graph_with_SR_weight.dat'
	f = open(fn, 'r')

	for line in f:
		(u1, u2, w, SR) = line.split()
		#print u1, u2, w
		if int(u1) > int(u2):
			pom = u1
			u1 = u2
			u2 = pom
		if (int(u1), int(u2)) in d:
			w1 = d[int(u1), int(u2)]
			w2 = min(w1, int(w))
			d[int(u1), int(u2)] = int(w2)
		else:
			d[int(u1), int(u2)] = int(w)
	print len(d)
	return d


def read_all_users():
	d = []
	fn = 'mention_graph_weights.dat'
	f = open(fn, 'r')
	for line in f:
		(u1, u2, w) = line.split()
		d.append(int(u1))
		d.append(int(u2))
	d = set(d)
	print len(d)
	return d


# nodes with highest avg COMM membership
def read_nodes_COMM():
	COMM = 0
	nodes_COMM = defaultdict(list)
	input_file = codecs.open(F_IN, 'r', encoding='utf8')
	for line in input_file:
		line = line.split()
		for node in line:
			nodes_COMM[int(node)].append(COMM)
		COMM += 1
	return nodes_COMM

def find_node_interaction_comm_propensity():

	d = read_in_mention_graph_undir()
	d_all = read_all_users()

	d_weak = read_in_mention_graph()
	cnt_edges = 0
	node_comm_membership = read_nodes_COMM()
	comm_mem = defaultdict(list)
	for (u1, u2) in d:
		comms_u1 = node_comm_membership[u1]
		comms_u2 = node_comm_membership[u2]
		shared = len(set(comms_u1).intersection(set(comms_u2)))
		comm_mem[shared].append(d[(u1, u2)])
		cnt_edges += 1

	N = cnt_edges
	print N
	cnt_edges = 0

	comm_mem_weak = defaultdict(list)
	for (u1, u2) in d_weak:
		comms_u1 = node_comm_membership[u1]
		comms_u2 = node_comm_membership[u2]
		shared = len(set(comms_u1).intersection(set(comms_u2)))
		comm_mem_weak[shared].append(d[(u1, u2)])
		cnt_edges += 1

	N_weak = cnt_edges
	print N_weak
	cnt = 0
	
	"""
	print len(d_all)
	print len(d_all) * len(d_all)

	
	full_comm_mem = defaultdict(int)
	for u1 in d_all:
		for u2 in d_all:
			if u1 >= u2:
				continue
			#print u1, u2
			comms_u1 = node_comm_membership[u1]
			comms_u2 = node_comm_membership[u2]
			shared = len(set(comms_u1).intersection(set(comms_u2)))
			#shared = cnt
			full_comm_mem[shared] += 1
			if cnt % 1000000 == 0:
				print cnt
			cnt += 1

	print cnt
	#print full_comm_mem
	"""
	comm_mem2 = OrderedDict()
	comm_mem3 = OrderedDict()

	comm_mem4 = OrderedDict()
	comm_mem5 = OrderedDict()
	for comm in comm_mem:
		#comm_mem2[comm] = np.mean(np.array(comm_mem[comm]))
		comm_mem2[comm] = stats.mode(np.array(comm_mem[comm]))[0][0]
		comm_mem3[comm] = np.std(np.array(comm_mem[comm]))
		comm_mem4[comm] = float(len(np.array(comm_mem[comm]))) / float(N)
		#n = full_comm_mem[comm]
		#comm_mem4[comm] = float(len(np.array(comm_mem[comm]))) / float((n*(n-1)/2)) if n > 0 else 0
		comm_mem5[comm] = float(len(np.array(comm_mem_weak[comm]))) / float(N_weak)

	return comm_mem2, comm_mem3 , comm_mem4, comm_mem5

#find_node_interaction_comm_propensity()

def plot_interaction_comm_propensity():
	cm1, cm2, cm3, cm4 = find_node_interaction_comm_propensity()
	x = cm3.keys()
	y = cm3.values()
	#e = cm2.values()
	#x = cm3.keys()
	z = cm4.values()
	print y
	print z

	plt.plot(x, y, c='r')
	plt.plot(x, z, c='b')

	#plt.errorbar(x, y, e)

	#plt.xlim(-1,12)

	#plt.yscale('log')

	print pearsonr(np.array(x), np.array(y))
	print pearsonr(np.array(x), np.array(z))

	plt.show()

plot_interaction_comm_propensity()

# nodes with highest avg COMM membership
def find_overlapping_COMM():
	COMM = 0
	nodes_num_COMM = find_nodes_in_more_COMM()
	COMM_density =  defaultdict(list)
	input_file = codecs.open(F_IN, 'r', encoding='utf8')
	for line in input_file:
		line = line.split()
		for node in line:
			COMM_density[COMM].append(nodes_num_COMM[int(node)])
		COMM += 1
	COMM_density2 =  defaultdict(tuple)
	for COMM in COMM_density:
		COMM_density2[COMM] = (np.mean(np.array(COMM_density[COMM])), len(COMM_density[COMM]))
	COMM_density3 = OrderedDict(sorted(COMM_density2.items(), key=lambda t:t[1][0]))
	#for COMM in COMM_density3:
	#	print COMM, COMM_density3[COMM]
	return COMM_density3



def plot_COMM_size_vs_density():

	import seaborn as sns
	sns.set(color_codes=True)

	sns.set(font_scale=2) 

	x = []
	y = []

	data = find_overlapping_COMM()

	for COMM in data:
		x.append(data[COMM][0])
		y.append(data[COMM][1])

	x = np.array(x)
	y = np.array(y)

	print 'Corrcoef COMM size and density ',  pearsonr(np.array(x), np.array(y))
	(r, p) = pearsonr(np.array(x), np.array(y))

	lab = r'$r=' +  "{:.2f}".format(r) + '$, $p= ' + "{:.2f}".format(p) + '$'
	xlabel = 'comm density'
	ylabel = 'comm size'

	#plt.scatter(x, y, edgecolors='none', c='c', label=lab)
	with sns.axes_style("white"):
		g = sns.jointplot(x=x, y=y, kind="reg", color="c").set_axis_labels(xlabel, ylabel)

	#plt.legend(frameon=0, loc=2)
	#plt.show()
	#plt.tight_layout()
	plt.savefig('node_comm_size_density.eps',bbox_inches='tight' , dpi=550)



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

def find_MEDIAN_SEM_cap_per_node_COMM_membership():
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
		res_mean[COMM] = np.median(np.array(res[COMM]))
		res_stdev[COMM] = np.std(np.array(res[COMM]))
	return res_mean, res_stdev

def find_avg_sentiment_per_node_COMM_membership():
	node_comm_membership = find_nodes_in_more_COMM()
	sem_cap = read_sem_capital(f_name='user_sentiment.tab', tname='sentiment')
	res = defaultdict(list)
	for node in node_comm_membership:
		n_sem = sem_cap[str(node)]
		nCOMM = node_comm_membership[node] # if node_comm_membership[node] < 10 else 10
		res[nCOMM].append(n_sem)
	res_mean = defaultdict(float)
	res_stdev = defaultdict(float)
	for COMM in res:
		res_mean[COMM] = np.median(np.array(res[COMM]))
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
	num_bins = 10
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
	plt.plot(x,y,linestyle="-",color='red',label=lab)
	plt.yscale('log', nonposy='clip')
	plt.xlabel('node comm membership')
	plt.ylabel('p(node comm membership)')
	plt.legend(loc='best', frameon=0)
	plt.xlim(1,10)
	#plt.title(r'Histogram for mention network pairwise SR: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$')
	plt.grid(True)
	plt.tight_layout()
	plt.savefig('node_comm_membership_pdf77.eps',bbox_inches='tight' , dpi=550)

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
	plt.errorbar(x,y,e,linestyle="-",marker='*',color='darkgreen',fmt='o',elinewidth=3.4)
		#,label='mean node neighborhood SR per comm membership ')
	#plt.yscale('log', nonposy='clip')
	plt.xlabel('node comm membership')
	plt.ylabel('mean node SR with neighbors')
	#plt.legend(loc='best',frameon=False)
	plt.xlim(0,11)
	plt.tight_layout()
	#plt.title(r'Histogram for mention network pairwise SR: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$')
	#plt.grid(True)
	plt.savefig('node_comm_membership_vs_mean_SR.eps', bbox_inches='tight' ,dpi=550)
	plt.show()

def plot_SEM_CAP_vs_COMM_membership():
	d, std = find_avg_SEM_cap_per_node_COMM_membership()
	x = d.keys()
	y = d.values()
	e = std.values()
	plt.errorbar(x,y,e,linestyle="-",marker='*',color='darkred',fmt='o',elinewidth=3.4)
	#plt.yscale('log', nonposy='clip')
	plt.xlabel('node comm membership')
	plt.ylabel('mean node semantic capital')
	plt.legend(loc=2,frameon=False)
	plt.xlim(0,11)
	#plt.title(r'Histogram for mention network pairwise SR: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$')
	#plt.grid(True)
	plt.tight_layout()
	plt.savefig('node_comm_membership_vs_avg_SEM_CAP6.eps', bbox_inches='tight',  dpi=550)
	plt.show()

def plot_MEDIAN_SEM_CAP_vs_COMM_membership():
	d, std = find_MEDIAN_SEM_cap_per_node_COMM_membership()
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
	plt.savefig('node_comm_membership_vs_MEDIAN_SEM_CAP1.eps', dpi=550)
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
	plt.errorbar(x,y,e,linestyle="-",marker='*',fmt='o',elinewidth=3.4,color='darkcyan')

	plt.xlabel('node comm membership')
	plt.ylabel(r'mean node $st_{inc}$')
	plt.legend(loc=2,frameon=False)
	plt.xlim(0,11)
	plt.tight_layout()
	#plt.title(r'Histogram for mention network pairwise SR: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$')
	#plt.grid(True)
	plt.savefig('node_comm_membership_vs_MEDIAN_ST_INC7.eps', bbox_inches='tight' , dpi=550)
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
	#plt.legend(loc=2,frameon=False)
	#plt.xlim(0,11)
	#plt.ylim(-0.1,0.1)
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
	plt.errorbar(x1,y1,e1,linestyle="-",marker='*',fmt='o',elinewidth=3.4,color='darkred',label='popularity')
	plt.errorbar(x2,y2,e2,linestyle="-",marker='*',fmt='o',elinewidth=3.4,color='darkblue',label='activity')
	plt.xlabel('node comm membership')
	plt.ylabel('mean node social capital')
	plt.legend(loc='best',frameon=False)
	plt.xlim(0,11)
	plt.tight_layout()
	#plt.grid(True)
	plt.savefig('node_comm_membership_vs_avg_DIR_deg7.eps', bbox_inches='tight' , dpi=550)
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
#plot_MEDIAN_ST_INC_vs_COMM_membership()
#plot_sentiment_vs_COMM_membership()
#plot_avg_neighborhood_SR_vs_COMM_membership()
#plot_SEM_CAP_vs_COMM_membership()
#plot_DIR_deg_vs_COMM_membership()
#plot_MEDIAN_DIR_deg_vs_COMM_membership()
#plot_deg_vs_COMM_membership()
#output_basic_stats_BigClam_COMM()
#find_nodes_in_more_COMM()
#plot_pdf_node_in_COMM()
#plot_MEDIAN_SEM_CAP_vs_COMM_membership()

#plot_COMM_size_vs_density()
