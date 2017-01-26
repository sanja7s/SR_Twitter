#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	analyze assortativity of the graphs in terms of sentiment
'''
from igraph import *
import networkx as nx
import os
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os
import matplotlib.cm as cm
from collections import defaultdict
import matplotlib

from scipy.stats.stats import pearsonr

font = {'family' : 'sans-serif',
		'variant' : 'normal',
		'weight' : 'light',
		'size'   : 20}

matplotlib.rc('font', **font)

import seaborn as sns
sns.set(color_codes=True)

sns.set(font_scale=2) 

f_in_user_labels = "usr_num_CVs.tab"
##################
f_in_user_taxons = "user_taxons.tab"
f_in_user_concepts = "user_concepts.tab"
f_in_user_entities = "user_entities.tab"
#########################
#
f_in_user_sentiment = "user_sentiment.tab"
#
# mention graph
#########################
f_in_graph_weights = "mention_graph_weights.dat"
########################
IN_DIR = "../../../DATA/CAPITAL/"
os.chdir(IN_DIR)



def read_sem_capital(f_name, tname):
	f = open(f_name, "r")
	cap = defaultdict(int)
	cnt = 0
	for line in f:
		if tname == 'sentiment':
			(vid, vn, val) = line.split('\t')
			val = float(val)
		else:
			(vid, val) = line.split('\t')
			val = int(val)
		cap[vid] = val
		cnt += 1
	return cap

# one time call
def save_edge_popularity_and_semantic_capital_diff():

	sc = read_sem_capital('entities','entities')

	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)
	fo = open('sem_capital_edge_src_dest_INdeg.dat', 'w')
	fow = open('sem_capital_edge_src_dest_weighted_INdeg.dat', 'w')
	for e in G.es:
		src_id = e.source
		dest_id = e.target

		src = G.vs[src_id]['name']
		dest = G.vs[dest_id]['name']

		sc_src = sc[src]
		sc_dest = sc[dest]

		deg_src = G.degree(src_id, mode=IN)
		deg_dest = G.degree(dest_id, mode=IN)
		w_deg_src = G.strength(src_id, mode=IN, weights='weight')
		w_deg_dest = G.strength(dest_id, mode=IN, weights='weight')	
		
		fo.write(str(sc_src) + '\t' + str(sc_dest) + '\t'+ str(deg_src) + '\t' + str(deg_dest) + '\n')
		fow.write(str(sc_src) + '\t' + str(sc_dest) + '\t'+ str(w_deg_src) + '\t' + str(w_deg_dest) + '\n')

def read_edge_popularity_and_semantic_capital_diff(f_in):
	f = open(f_in, 'r')
	res = []
	for line in f:
		(src_sc,dest_sc,src_IN,dest_IN) = line.split('\t')
		res.append((float(src_sc)-float(dest_sc),(float(src_IN)-float(dest_IN))))
	return res

def read_edge_semantic_capital_diff(f_in):
	f = open(f_in, 'r')
	res = []
	for line in f:
		(src_sc,dest_sc,src_IN,dest_IN) = line.split('\t')
		res.append(float(src_sc)-float(dest_sc))
	return res

# one time call
def save_edge_popularity_diff():

	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)
	fo = open('edge_src_dest_INdeg.dat', 'w')
	fow = open('edge_src_dest_weighted_INdeg.dat', 'w')
	for e in G.es:
		src_id = e.source
		dest_id = e.target
		#src = G.vs[src_id]
		#dest = G.vs[dest_id]

		deg_src = G.degree(src_id, mode=IN)
		deg_dest = G.degree(dest_id, mode=IN)
		w_deg_src = G.strength(src_id, mode=IN, weights='weight')
		w_deg_dest = G.strength(dest_id, mode=IN, weights='weight')	
		
		fo.write(str(deg_src) + '\t' + str(deg_dest) + '\n')
		fow.write(str(w_deg_src) + '\t' + str(w_deg_dest) + '\n')

def read_edge_popularity_diff(f_in):
	f = open(f_in, 'r')
	res = []
	for line in f:
		(src,dest) = line.split('\t')
		res.append(float(src)-float(dest))
	return res

def plot_edge_popularity_diff_distr(x, tname):

	x = np.array(x) 
	mu = np.mean(x)
	sigma = np.std(x)
	med = np.median(x)

	lab = '$\mu=' +  "{:.3f}".format(mu) \
	 + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'

	num_bins = 150
	# the histogram of the data
	n, bins, patches = plt.hist(x, normed=1, bins=num_bins, histtype='step',color='darkorchid')
	#plt.clf() # Get rid of this histogram since not the one we want.
	#nx_frac = n/float(len(n)) # Each bin divided by total number of objects.
	#width = bins[1] - bins[0] # Width of each bin.
	#x = np.ravel(zip(bins[:-1], bins[:-1]+width))
	#y = np.ravel(zip(nx_frac,nx_frac))
	plt.title(lab)
	plt.tight_layout()
	#plt.scatter(x,y,color='darkorchid',label=lab)
	plt.xlabel('' + tname)
	plt.ylabel('p('+ tname +')')
	plt.yscale('log')
	#plt.xscale('log')
	#xint = range(int(min(x)), int(math.ceil(max(x))+1))
	#plt.xticks(xint)
	plt.xlim(-1000,1000)
	#plt.grid(True)
	
	plt.savefig(tname + 'weighted.png')

def plot_edge_popularity_diff_distr_seaborn(x, tname):

	x = np.array(x) 
	mu = np.mean(x)
	sigma = np.std(x)
	med = np.median(x)

	lab = '$\mu=' +  "{:.3f}".format(mu) \
	 + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'

	xlabel = 'relative social status'
	ylabel = 'kde(relative social status)'

	print max(x)
	z = [xel if xel == 0 else np.log10(abs(xel))*np.sign(xel) for xel in x]
	print max(z)
	z = np.array(z)

	g = sns.distplot(z, \
		hist_kws={"histtype": "step", "linewidth": 1, "alpha": 0.3, "color": "g"}, \
		color="r")
	plt.title(lab)
	labels = [r'$ 10^{-4} $', r'$ 10^{-3} $', r'$ 10^{-2} $', \
	r'$ 10^{-1} $', r'$ 10^0 $', r'$ 10^1 $', r'$ 10^2 $', \
	r'$ 10^3 $', r'$ 10^4 $']
	g.set(xticklabels=labels)

	plt.xlabel(xlabel)
	plt.ylabel(ylabel)

	plt.tight_layout()	
	plt.savefig(tname + 'weighted7log.eps', bbox_inches='tight', dpi=550)

def plot_edge_semantic_capital_diff_distr(x, tname):

	x = np.array(x) 
	mu = np.mean(x)
	sigma = np.std(x)

	lab = '$\mu=' +  "{:.3f}".format(mu) \
	 + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'

	num_bins = 60
	# the histogram of the data
	n, bins, patches = plt.hist(x, normed=1, bins=num_bins, histtype='step',color='darkorchid')
	plt.title(lab)
	plt.tight_layout()
	#plt.scatter(x,y,color='darkorchid',label=lab)
	plt.xlabel('' + tname)
	plt.ylabel('p('+ tname +')')
	plt.yscale('log')
	#plt.xscale('log')
	#xint = range(int(min(x)), int(math.ceil(max(x))+1))
	#plt.xticks(xint)
	#plt.ylim(0.000001,0.01)
	#plt.grid(True)
	plt.savefig(tname + 'weighted.png')

def plot_edge_semantic_capital_diff_distr_seaborn(x, tname):

	x = np.array(x) 
	mu = np.mean(x)
	sigma = np.std(x)

	lab = '$\mu=' +  "{:.3f}".format(mu) \
	 + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'

	xlabel = 'relative semantic status'
	ylabel = 'kde(relative semantic status)'

	print max(x)
	z = [xel if xel == 0 else np.log10(abs(xel))*np.sign(xel) for xel in x]
	print max(z)
	z = np.array(x)

	g = sns.distplot(z, \
		hist_kws={"histtype": "step", "linewidth": 1, "alpha": 0.3, "color": "g"}, \
		color="r")
	plt.title(lab)
	labels = [r'$ 10^{-4} $', r'$ 10^{-3} $', r'$ 10^{-2} $', \
	r'$ 10^{-1} $', r'$ 10^0 $', r'$ 10^1 $', r'$ 10^2 $', \
	r'$ 10^3 $', r'$ 10^4 $']
	#g.set(xticklabels=labels)

	plt.xlabel(xlabel)
	plt.ylabel(ylabel)

	plt.tight_layout()	
	plt.savefig(tname + 'weighted7.eps', bbox_inches='tight', dpi=550)

def plot_edge_popularity_distr_2(x, tname):

	x = np.array(x) 
	mu = np.mean(x)
	sigma = np.std(x)

	lab = '$\mu=' +  "{:.3f}".format(mu) \
	 + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'

	num_bins = 1500
	# the histogram of the data
	n, bins, patches = plt.hist(x, normed=1, bins=num_bins, histtype='step',color='darkorchid')
	plt.clf() # Get rid of this histogram since not the one we want.
	nx_frac = n/float(len(n)) # Each bin divided by total number of objects.
	width = bins[1] - bins[0] # Width of each bin.
	x = np.ravel(zip(bins[:-1], bins[:-1]+width))
	y = np.ravel(zip(nx_frac,nx_frac))
	plt.title(lab)
	
	plt.scatter(x,y,color='darkorchid',label=lab)
	plt.xlabel('' + tname)
	plt.ylabel('p('+ tname +')')
	plt.yscale('log')
	#plt.xscale('log')
	#xint = range(int(min(x)), int(math.ceil(max(x))+1))
	#plt.xticks(xint)
	plt.ylim(0.0000000001,0.01)
	#plt.grid(True)
	
	plt.savefig(tname + 'weighted_v2.png')

def plot_edge_sc_vs_pop_diff(diff, tname):

	x = []
	y = []

	for el in diff:
		x.append(el[0])
		y.append(el[1])

	lab = ''
	
	plt.scatter(x,y,color='darkorchid',label=lab)
	plt.xlabel('semantic capital status diff')
	plt.ylabel('popularity status diff')
	#plt.yscale('log')
	#plt.xscale('log')
	#xint = range(int(min(x)), int(math.ceil(max(x))+1))
	#plt.xticks(xint)
	plt.ylim(-1000,1000)
	#plt.grid(True)
	plt.savefig(tname + '.png')


def plot_edge_sc_vs_pop_diff_2(diff, tname):
	coef_soc = 100
	soc = []
	sem = []
	d = defaultdict(int)
	for el in diff:
		# sc
		s1 = el[0]
		sem.append(s1)
		# pop
		s2 = int(el[1]/coef_soc)
		soc.append(s2)
		if s1 in d:
			d[s1][s2] += 1
		else:
			d[s1] = defaultdict(int)
			d[s1][s2] += 1

	soc=np.array(soc)
	sem=np.array(sem)
	print np.corrcoef(soc,sem)

	print pearsonr(soc, sem)

	x = []
	y = []
	v = []
	for i in d:
		for j in d[i]:
			if d[i][j] > 0:
				x.append(j*coef_soc)
				y.append(i)
				v.append(d[i][j])

	plt.clf()
	plt.scatter(x,y,s=v, c='darkorchid', edgecolors='none',alpha=0.4)	
	plt.ylabel('sem cap diff (source - receiver)')
	plt.xlabel('pop status diff (source - receiver)')
	plt.tight_layout()
	plt.xlim(-1000,1000)
	#plt.grid(True)
	plt.savefig(tname + 'pretty.png')


def plot_edge_sc_vs_pop_diff_2_seaborn(diff, tname):
	coef_soc = 100
	soc = []
	sem = []
	d = defaultdict(int)
	for el in diff:
		# sc
		s1 = el[0]
		sem.append(s1)
		# pop
		s2 = int(el[1]/coef_soc)
		soc.append(el[1])
		if s1 in d:
			d[s1][s2] += 1
		else:
			d[s1] = defaultdict(int)
			d[s1][s2] += 1

	x=np.array(soc)
	y=np.array(sem)
	
	ylabel = 'relative semantic status'
	xlabel = 'relative social status'

	print len(x)
	print len(y)


	print max(x)
	z = [xel if xel == 0 else np.log10(abs(xel))*np.sign(xel) for xel in x]
	print max(z)
	z = np.array(z)

	labels = [r'$ 10^{-4} $', r'$ 10^{-3} $', r'$ 10^{-2} $', \
	r'$ 10^{-1} $', r'$ 10^0 $', r'$ 10^1 $', r'$ 10^2 $', \
	r'$ 10^3 $', r'$ 10^4 $']

	with sns.axes_style("white"):
		g = sns.jointplot(x=z, y=y, kind="scatter", color="darkorchid").set_axis_labels(xlabel, ylabel)

	#g.set(xticklabels=labels)
	g.ax_joint.set_xticklabels(labels)
	#plt.tight_layout()
	plt.savefig(tname + 'scatter.eps', bbox_inches='tight')


#pop_diff = read_edge_popularity_diff('edge_src_dest_weighted_INdeg.dat')	
#plot_edge_popularity_diff_distr_seaborn(pop_diff, 'popularity diff (source - receiver)')

#sc_diff = read_edge_semantic_capital_diff('sem_capital_edge_src_dest_weighted_INdeg.dat')
#plot_edge_semantic_capital_diff_distr_seaborn(sc_diff,'sem cap diff (source - receiver)')

#pop_sc_diff = read_edge_popularity_and_semantic_capital_diff('sem_capital_edge_src_dest_weighted_INdeg.dat')
#plot_edge_sc_vs_pop_diff_2(pop_sc_diff, 'pop vs. sem cap status diff')

pop_sc_diff = read_edge_popularity_and_semantic_capital_diff('sem_capital_edge_src_dest_weighted_INdeg.dat')
plot_edge_sc_vs_pop_diff_2_seaborn(pop_sc_diff, 'pop vs. sem cap status diff')