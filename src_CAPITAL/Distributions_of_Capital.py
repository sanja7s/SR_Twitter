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
import pandas as pd

import seaborn as sns
sns.set(color_codes=True, font_scale=2) 
sns.set_style('whitegrid')

import pandas as pd
from scipy import stats, integrate

f_in_user_labels = "usr_num_CVs.tab"
##################
f_in_user_taxons = "user_taxons.tab"
f_in_user_concepts = "user_concepts.tab"
f_in_user_entities = "user_entities.tab"
f_in_num_tweets = "usr_num_tweets.tab"
#########################
#
f_in_user_sentiment = "user_sentiment.tab"
# mention graph
#########################
f_in_graph = "threshold_mention_graphs/directed_threshold0.tab"
f_in_graph_weights = "threshold_mention_graphs/mention_graph_weights.dat"
f_out_sent_mention_graph = "directed_threshold0_sent_val.tab"
IN_DIR = "../../../DATA/CAPITAL/"
f_out_mention = "sentiment_assortativity_mention_2.txt"
#########################

f_in_graph_weights = "mention_graph_weights.dat"

os.chdir(IN_DIR)

def social_capital_distributions(f_name, tname):
	f = open(f_name, "r")
	cap = []
	cnt = 0
	for line in f:
		if tname == 'sentiment':
			(vid, vn, val) = line.split('\t')
			val = float(val)
		elif tname == 'status inconsistency':
			(vid, val) = line.split('\t')
			val = float(val)	
		else:
			(vid, val) = line.split('\t')
			val = int(val)
		cap.append(val)
		cnt += 1
	print cnt
	#plot_cap_distr_CVs(cap, tname)
	plot_cap_distr_entities(cap, 'entities')
	#plot_cap_distr_CVs(cap, 'CVs')

def social_capital_distributions_1(f_name, tname):
	f = open(f_name, "r")
	cap = []
	cnt = 0
	for line in f:
		(vid, val) = line.split('\t')
		val = int(val)
		cap.append(val)
		cnt += 1

	print cnt
	plot_cap_distr_1(cap, tname)

def plot_cap_distr_1(x, tname):

	x = np.array(x) 
	mu = np.mean(x)
	sigma = np.std(x)

	num_bins = 100
	# the histogram of the data
	n, bins, patches = plt.hist(x, normed=1, bins=num_bins)
	plt.clf() # Get rid of this histogram since not the one we want.
	nx_frac = n/float(len(n)) # Each bin divided by total number of objects.
	width = bins[1] - bins[0] # Width of each bin.
	x = np.ravel(zip(bins[:-1], bins[:-1]+width))
	y = np.ravel(zip(nx_frac,nx_frac))

	lab = '$\mu=' +  "{:.3f}".format(mu) \
	 + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'	
	plt.plot(x,y,color='darkorchid',label=lab)
	plt.xlabel('# '+tname)
	plt.ylabel('p(# ' +tname+ ' )')
	plt.yscale('log')
	#plt.xscale('log')
	plt.legend()
	
	plt.savefig(tname + '1.eps')

def plot_cap_distr(x, tname):

	x = np.array(x) 
	mu = np.mean(x)
	sigma = np.std(x)

	lab = '$\mu=' +  "{:.3f}".format(mu) \
	 + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'

	num_bins = 100
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
	plt.tight_layout()
	#plt.yscale('log')
	#plt.xscale('log')
	#xint = range(int(min(x)), int(math.ceil(max(x))+1))
	#plt.xticks(xint)
	plt.xlim(-1,1)
	#plt.ylim(-0.005,0.015)
	#plt.grid(True)
	
	plt.savefig(tname + '_v2.eps')

def create_distr_sent(x):

	d = stats.gaussian_kde(x)
	print d

	return d



def plot_cap_distr_7s(z, tname):

	z = np.array(z, dtype=np.float) 
	mu = np.mean(z)
	sigma = np.std(z)

	lab = '$\mu=' +  "{:.3f}".format(mu) \
	 + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'

	sns.distplot(z, hist_kws={"histtype": "step", "linewidth": 1, "alpha": 0.3, "color": "g"}, color="r")
	plt.title(lab)

	plt.xlabel('' + tname)
	plt.ylabel('kde('+ tname +')')
	plt.xlim(-1,1)
	plt.tight_layout()

	plt.savefig(tname + '_v7.eps')
	
	"""
	kde1 = create_distr_sent(z)

	fig = plt.figure()
	ax = fig.add_subplot(111)

	ax.plot(z, np.zeros(z.shape), 'b+', ms=20)  # rug plot
	x_eval = np.linspace(-1, 1, num=2000)
	ax.plot(x_eval, kde1(x_eval), 'k-', label="Scott's Rule")
	"""

	#plt.show()

	"""
	x = d.keys()
	y = d.values()
	
	
	
	plt.scatter(x,y,color='darkorchid',label=lab)
	plt.xlabel('' + tname)
	plt.ylabel('p('+ tname +')')
	plt.tight_layout()
	#plt.yscale('log')
	#plt.xscale('log')
	#xint = range(int(min(x)), int(math.ceil(max(x))+1))
	#plt.xticks(xint)
	plt.xlim(-1,1)
	#plt.ylim(-0.005,0.015)
	#plt.grid(True)
	"""	
	

def plot_cap_distr_entities(z, tname):

	z = np.array(z, dtype=np.float) 
	mu = np.mean(z)
	sigma = np.std(z)

	lab = '$\mu=' +  "{:.3f}".format(mu) \
	 + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'

	fig7s = plt.gcf()
	plt.rcParams['figure.figsize']=(6,6)
	fig7s.set_size_inches((6,6))
	plt.figure(figsize=(6, 6))

	sns.distplot(z, bins=30, hist=0, \
		#hist_kws={"histtype": "step", "linewidth": 1, "alpha": 0.3, "color": "g"}, \
		color="r")
	plt.title(lab)

	plt.xlabel('entity diversity')
	plt.ylabel('kde')
	plt.xlim(-1,31)
	plt.tight_layout()

	plt.savefig(tname + '_v7.eps')

def plot_cap_distr_CVs(z, tname):

	z = np.array(z, dtype=np.float) 
	mu = np.mean(z)
	sigma = np.std(z)

	fig7s = plt.gcf()
	plt.rcParams['figure.figsize']=(6,6)
	fig7s.set_size_inches((6,6))
	plt.figure(figsize=(6, 6))

	lab = '$\mu=' +  "{:.3f}".format(mu) \
	 + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'

	sns.distplot(z, \
		#hist_kws={"histtype": "step", "linewidth": 1, "alpha": 0.3, "color": "g"}, \
		color="r", hist=0)
	plt.title(lab)

	plt.xlabel('CV concept diversity')
	plt.ylabel('kde')
	plt.xlim(0,2000)
	plt.tight_layout()

	plt.savefig(tname + '_v77.eps')


#social_capital_distributions('entities', 'entities')

#social_capital_distributions('node_scalar_inconsistency_v2', 'status inconsistency')


def plot_cap_distr_BI(z, tname):

	z = np.array(z, dtype=np.float) 
	mu = np.mean(z)
	sigma = np.std(z)

	lab = '$\mu=' +  "{:.3f}".format(mu) \
	 + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'

	fig7s = plt.gcf()
	plt.rcParams['figure.figsize']=(6,6)
	fig7s.set_size_inches((6,6))
	plt.figure(figsize=(6, 6))

	sns.distplot(z, bins=30, hist=0, \
		#hist_kws={"histtype": "step", "linewidth": 1, "alpha": 0.3, "color": "g"}, \
		color="r")
	plt.title(lab)

	plt.xlabel('Burt\'s index')
	plt.ylabel('kde')
	plt.xlim(-0.1,max(z)+0.1)
	plt.tight_layout()

	plt.savefig(tname + '_v7s.eps')

def read_BI():
	return pd.read_csv('BI_indexR_full.txt',\
		encoding='utf-8', delim_whitespace=1)

def BI_capital_distribution():
	bi = read_BI()
	print max(bi['bi']), min(bi['bi'])

	bidict = bi.set_index('id')['bi'].to_dict()
	cnt = 0
	for el in bidict:
		if bidict[el] > 1:
			bidict[el] = 1
			cnt += 1
	print cnt
	


	plot_cap_distr_BI(bidict.values(), 'Burt\'s index')

BI_capital_distribution()

