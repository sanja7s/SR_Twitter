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
f_in_num_tweets = "usr_num_tweets.tab"
#########################
#
f_in_user_sentiment = "user_sentiment.tab"
#
# mention graph
#########################
f_in_graph = "threshold_mention_graphs/directed_threshold0.tab"
f_in_graph_weights = "mention_graph_weights.dat"
f_out_sent_mention_graph = "directed_threshold0_sent_val.tab"
IN_DIR = "../../../DATA/CAPITAL/"
f_out_mention = "sentiment_assortativity_mention_2.txt"
#########################

soc_capital = 'node_degree.dat'
sem_capital = 'user_entities.tab'

os.chdir(IN_DIR)

# one time call
def save_node_degree():

	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	fo = open('node_degree.dat', 'w')

	for v in G.vs:
		d = G.degree(v.index)
		n = v['name']
		fo.write(str(n) + '\t' + str(d) + '\n')

# one time call
def save_node_MUTUAL_degree():

	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	G.to_undirected(mode='mutual')

	not_connected_nodes = G.vs(_degree_eq=0)

	to_delete_vertices = not_connected_nodes
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)


	fo = open('mutual degree', 'w')

	for v in G.vs:
		d = G.degree(v.index)
		n = v['name']
		fo.write(str(n) + '\t' + str(d) + '\n')

# one time call
def save_node_MUTUAL_weighted_degree():

	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	G.to_undirected(mode='mutual',combine_edges=sum)

	not_connected_nodes = G.vs(_degree_eq=0)

	to_delete_vertices = not_connected_nodes
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)


	fo = open('mutual weighted degree', 'w')

	for v in G.vs:
		d = G.strength(v.index,weights='weight')
		n = v['name']
		fo.write(str(n) + '\t' + str(d) + '\n')

# one time call
def save_node_indegree():

	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	fo = open('indegree', 'w')

	for v in G.vs:
		d = G.degree(v.index,mode=IN)
		n = v['name']
		fo.write(str(n) + '\t' + str(d) + '\n')

# one time call
def save_node_outdegree():

	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	fo = open('outdegree', 'w')

	for v in G.vs:
		d = G.degree(v.index,mode=OUT)
		n = v['name']
		fo.write(str(n) + '\t' + str(d) + '\n')

# one time call
def save_node_weighted_degree():

	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	fo = open('weighted_node_degree.dat', 'w')

	for v in G.vs:
		d = G.strength(v.index, weights='weight', loops=False)
		n = v['name']
		fo.write(str(n) + '\t' + str(d) + '\n')

# one time call
def save_node_weighted_outdegree():

	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	fo = open('weighted outdegree', 'w')

	for v in G.vs:
		d = G.strength(v.index,mode=OUT, weights='weight')
		n = v['name']
		fo.write(str(n) + '\t' + str(d) + '\n')

# one time call
def save_node_weighted_indegree():

	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)

	fo = open('weighted indegree', 'w')

	for v in G.vs:
		d = G.strength(v.index,mode=IN, weights='weight')
		n = v['name']
		fo.write(str(n) + '\t' + str(d) + '\n')


def read_soc_capital(soc_capital=soc_capital):
	cap = defaultdict(int)
	f = open(soc_capital, "r")
	for line in f:
		(n,d) = line.split('\t')
		cap[int(n)] = float(d)
	return cap

def read_sem_capital(sem_capital=sem_capital):
	cap = defaultdict(int)
	f = open(sem_capital, "r")
	for line in f:
		try:
			if sem_capital <> 'sentiment':
				(n,d) = line.split('\t')
				if sem_capital == 'status inconsistency':
					cap[int(n)] = float(d)
				else:
					cap[int(n)] = int(d)
			else:
				(n,nd,d) = line.split('\t')
				cap[int(n)] = float(d)

		except ValueError:
			pass
	return cap

def social_capital_vs_sem(soc='weighted degree',sem='entities'):

	soc_cap = read_soc_capital(soc)
	sem_cap = read_sem_capital(sem)
	max_soc_cap = max(soc_cap.values())
	max_sem_cap = max(sem_cap.values())

	print max_sem_cap, max_soc_cap

	coef_sem = 100
	coef_soc = 10
	soca = []
	sema = []

	cap = np.zeros((max_soc_cap+1,max_sem_cap+1))

	for n in soc_cap:
		if n in sem_cap:
			v1 = soc_cap[n] / coef_soc
			v2 = sem_cap[n] / coef_sem
			soca.append(soc_cap[n])
			sema.append(sem_cap[n])
			cap[v1][v2] += 1

	print soc, sem
	soca = np.array(soca)
	sema = np.array(sema)
	print pearsonr(soca, sema)
	plot_capitals_seaborn(soca, sema, name_soc=soc, name_sem=sem)

def social_capital_vs_sentiment(soc='weighted degree'):
	soc_cap = read_soc_capital(soc)
	sem_cap = read_sem_capital('sentiment')
	max_soc_cap = max(soc_cap.values())
	print max_soc_cap

	coef_soc = 50

	cap = defaultdict(int)

	soca = []
	sema = []

	for n in soc_cap:
		if n in sem_cap:
			v1 = soc_cap[n] / coef_soc
			v2 = math.ceil(sem_cap[n] * 20) / 20
			soca.append(soc_cap[n])
			sema.append(sem_cap[n])
			if v1 in cap:
				cap[v1][v2] += 1
			else:
				cap[v1] = defaultdict(float)
				cap[v1][v2] += 1

	soca = np.array(soca)
	sema = np.array(sema)
	print pearsonr(soca, sema)

	plot_sentiment_capital_seaborn(soca, sema, name_soc=soc)

def social_capital_vs_status_inconsistency(soc='weighted degree'):
	soc_cap = read_soc_capital(soc)
	sem_cap = read_sem_capital('status inconsistency')
	max_soc_cap = max(soc_cap.values())
	print max_soc_cap
	soca = []
	sema = []
	coef_soc = 50
	cap = defaultdict(int)
	for n in soc_cap:
		if n in sem_cap:
			v1 = soc_cap[n] / coef_soc
			v2 = math.ceil(sem_cap[n] * 20) / 20
			soca.append(soc_cap[n])
			sema.append(sem_cap[n])
			if v1 in cap:
				cap[v1][v2] += 1
			else:
				cap[v1] = defaultdict(float)
				cap[v1][v2] += 1
	soca = np.array(soca)
	sema = np.array(sema)
	print pearsonr(soca, sema)

	plot_status_inconsistency_capital(cap, coef_soc, name_soc=soc)

def plot_status_inconsistency_capital(cap, coef_soc, name_soc='deg'):
	x = []
	y = []
	vol = []
	for i in cap:
		for j in cap[i]:
			if cap[i][j] > 0 and i < 16:
				x.append(i*coef_soc)
				y.append(j)
				vol.append(cap[i][j]*7)
	#print cap
	plt.clf()
	plt.scatter(y,x,s=vol, c='darkblue', edgecolors='none',alpha=0.4)
	plt.tight_layout()
	plt.ylabel('social capital:' + name_soc )
	#plt.yscale('log')
	plt.xlim(-1,1)
	plt.xlabel('status inconsistency')
	plt.savefig(name_soc  + 'status inconsistency v7.png')
	#plt.show()

def plot_sentiment_capital(cap, coef_soc, name_soc='deg'):

	x = []
	y = []
	vol = []

	for i in cap:
		for j in cap[i]:
			if cap[i][j] > 0 and i < 16:
				x.append(i*coef_soc)
				y.append(j)
				vol.append(cap[i][j]*20)

	print cap
	plt.clf()

	plt.scatter(y,x,s=vol, c='darkorchid', edgecolors='none',alpha=0.4)
	plt.tight_layout()
	plt.ylabel('social capital: popularity' )
	#plt.yscale('log')
	plt.xlim(-1,1)
	plt.xlabel('sentiment score ')
	plt.savefig(name_soc  + 'setiment3.png')
	#plt.show()

def plot_sentiment_capital_seaborn(x, y, name_soc='deg'):

	xlabel = 'social capital: popularity'
	ylabel = 'sentiment'

	labels = [r'$ 10^0 $', r'$ 10^0 $', r'$ 10^1 $', r'$ 10^2 $', r'$ 10^3 $', r'$ 10^4 $', r'$ 10^5 $', r'$ 10^6 $', r'$ 10^7 $', r'$ 10^8 $']
	labelsy = ['-1','-0.5','0','0.5','1']
	with sns.axes_style("white"):
		g = sns.jointplot(x=np.log(x+1), y=y, kind="hex", color="darkorchid").set_axis_labels(xlabel, ylabel)

	#g.set(xticklabels=labels)
	g.ax_joint.set_xticklabels(labels)
	#g.ax_joint.set_yticklabels(labelsy)
	#plt.tight_layout()

	plt.savefig(name_soc  + 'setiment77.eps', bbox_inches='tight', dpi=550)

	"""
	plt.ylabel('social capital: popularity' )
	#plt.yscale('log')
	plt.xlim(-1,1)
	plt.xlabel('sentiment score ')
	"""

def social_capital_vs_IN_OUT_sentiment_plot(coef_socIN=50, coef_socOUT=50, name_soc='weighted degINOUT'):

	soc_capIN = read_soc_capital('weighted indegree')
	soc_capOUT = read_soc_capital('weighted outdegree')
	sem_cap = read_sem_capital('sentiment')

	capIN = defaultdict(int)
	for n in soc_capIN:
		if n in sem_cap:
			v1 = soc_capIN[n] / coef_socIN
			v2 = math.ceil(sem_cap[n] * 10) / 10
			if v1 in capIN:
				capIN[v1][v2] += 1
			else:
				capIN[v1] = defaultdict(float)
				capIN[v1][v2] += 1


	capOUT = defaultdict(int)
	for n in soc_capOUT:
		if n in sem_cap:
			v1 = soc_capOUT[n] / coef_socOUT
			v2 = math.ceil(sem_cap[n] * 10) / 10
			if v1 in capOUT:
				capOUT[v1][v2] += 1
			else:
				capOUT[v1] = defaultdict(float)
				capOUT[v1][v2] += 1

	xIN = []
	yIN = []
	volIN = []

	for i in capIN:
		for j in capIN[i]:
			if capIN[i][j] > 0 and i < 16:
				xIN.append(i*coef_socIN)
				yIN.append(j)
				volIN.append(capIN[i][j]*10)

	xOUT = []
	yOUT = []
	volOUT = []

	for i in capOUT:
		for j in capOUT[i]:
			if capOUT[i][j] > 0 and i < 16:
				xOUT.append(i*coef_socOUT)
				yOUT.append(j)
				volOUT.append(capOUT[i][j]*10)


	plt.clf()
	plt.scatter(yOUT,xOUT,s=volOUT, c='red', edgecolors='none',alpha=0.7)
	plt.scatter(yIN,xIN,s=volIN, edgecolors='none',alpha=0.1)

	plt.ylabel('Social capital ')
	plt.xlabel('Semantiment score')

	plt.savefig(name_soc  + '2setiment.png')
	#plt.show()
	
def plot_capitals(cap, coef_soc, coef_sem, name_soc='degree', name_sem='CVs'):

	x = []
	y = []
	vol = []

	for i in range(len(cap)):
		for j in range(len(cap[i])):
			if cap[i][j] > 0 and i < 16:
				x.append(i*coef_soc)
				y.append(j*coef_sem)
				vol.append(cap[i][j])

	print cap
	plt.clf()
	plt.scatter(y,x,s=vol,c='darkorchid', edgecolors='none',alpha=0.7)
	plt.tight_layout()
	plt.ylabel('social capital: ' + name_soc)
	#plt.yscale('log')
	plt.xlabel('semantic capital: ' + name_sem )
	#plt.xlim(-3,33)
	plt.savefig(name_sem + name_soc + '3.png')
	
	#plt.show()

def plot_capitals_seaborn(x, y, name_soc='degree', name_sem='CVs'):

	xlabel = 'social capital: popularity'
	ylabel = 'semantic capital: ' + name_sem

	labels = [r'$ 10^0 $', r'$ 10^0 $', r'$ 10^1 $', r'$ 10^2 $', r'$ 10^3 $', r'$ 10^4 $', r'$ 10^5 $', r'$ 10^6 $', r'$ 10^7 $', r'$ 10^8 $']
	#labels = ['s','d','g','s','d','g','s','d','g']
	with sns.axes_style("white"):
		g = sns.jointplot(x=np.log(x+1), y=y, kind="hex", color="darkorchid").set_axis_labels(xlabel, ylabel)

	#g.set(xticklabels=labels)
	g.ax_joint.set_xticklabels(labels)
	#plt.tight_layout()

	plt.savefig(name_sem + name_soc + '7.eps', bbox_inches='tight', dpi=550)

soc='weighted indegree'
social_capital_vs_sem(soc=soc,sem='CVs')
#social_capital_vs_sem(soc=soc,sem='entities')
#social_capital_vs_sem(soc=soc,sem='concepts')


#soc='weighted indegree'
#social_capital_vs_sentiment(soc)

#soc='weighted outdegree'
#social_capital_vs_sentiment(soc)

#social_capital_vs_IN_OUT_sentiment_plot()

#soc='outdegree'
#social_capital_vs_status_inconsistency(soc=soc)