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

import seaborn as sns
sns.set(color_codes=True)

sns.set(font_scale=2) 

import pandas as pd
from scipy import stats, integrate

font = {'family' : 'sans-serif',
		'variant' : 'normal',
		'weight' : 'light',
		'size'   : 16}

matplotlib.rc('font', **font)

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
	plot_cap_distr_CVs(cap, tname)

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

	sns.distplot(z, bins=30, \
		hist_kws={"histtype": "step", "linewidth": 1, "alpha": 0.3, "color": "g"}, \
		color="r")
	plt.title(lab)

	plt.xlabel('entity diversity')
	plt.ylabel('kde(entity diversity)')
	plt.xlim(-1,31)
	plt.tight_layout()

	plt.savefig(tname + '_v7.eps')

def plot_cap_distr_CVs(z, tname):

	z = np.array(z, dtype=np.float) 
	mu = np.mean(z)
	sigma = np.std(z)

	lab = '$\mu=' +  "{:.3f}".format(mu) \
	 + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'

	sns.distplot(z, \
		hist_kws={"histtype": "step", "linewidth": 1, "alpha": 0.3, "color": "g"}, \
		color="r")
	plt.title(lab)

	plt.xlabel('CVs diversity')
	plt.ylabel('kde(CVs diversity)')
	plt.xlim(0,2000)
	plt.tight_layout()

	plt.savefig(tname + '_v7.eps')


social_capital_distributions('CVs', 'Cvs')

#social_capital_distributions('node_scalar_inconsistency_v2', 'status inconsistency')