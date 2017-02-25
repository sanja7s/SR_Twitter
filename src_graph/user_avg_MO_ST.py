#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	from the month of edge formation, find the SR before, at the time and after
"""
from collections import defaultdict
import codecs
import os
import json
import numpy as np
from igraph import *

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib

import seaborn as sns
sns.set(color_codes=True, font_scale=2) 
sns.set_style('whitegrid')

IN_DIR = "../../../DATA/General/"
os.chdir(IN_DIR)

F_IN = "mention/edge_formation_deletion_MOs.dat"
F_OUT = "mention/user_avg_MO_ST"

MONTHS =  ["6", "7", "8", "9", "10"]

#########################
# read from a file that is an edge list with weights
#########################
def read_in_MO_graph(MO):
	G = Graph.Read_Ncol('mention/' + MO + '_MENT_weight_dir_self_loops', directed=True, weights=True)
	print G.summary()
	return G

def read_in_MO_graph_MUTUAL_UNW(MO):
	G = Graph.Read_Ncol('mention/' + MO + '_MENT_weight_dir_self_loops', directed=True, weights=True)
	G.to_undirected(mode="mutual", combine_edges='ignore')
	print G.summary()
	return G

def read_persisting_links_per_user():
	F_IN_P = "mention/edge_formation_deletion_MOs.dat"
	cnt = 0
	with codecs.open(F_IN_P,'r', encoding='utf8') as input_file:
		user_P_links = defaultdict(int)
		for line in input_file:
			(userA, userB, MO_formation, MO_deletion) = line.split()
			MO_formation = int(MO_formation)
			if MO_formation != 4:
				continue			
			MO_deletion = int(MO_deletion)
			if MO_deletion != 12:
				continue

			cnt += 1
			userA = int(userA)
			userB = int(userB)
			if userA < userB:
				u1 = userA
				u2 = userB
			else:
				u1 = userB
				u2 = userA
			user_P_links[u1] += 1
			user_P_links[u2] += 1
	print 'Persisting links in total ', cnt
	print 'User participtaing in persiting links ', len(user_P_links)

	print min(user_P_links.values()), max(user_P_links.values()), \
		np.std(np.array(user_P_links.values()))

	return np.array(user_P_links.values())

def plot_persisting_links_per_user():

	z = read_persisting_links_per_user()

	z = np.array(z, dtype=np.float) 
	mu = np.mean(z)
	sigma = np.std(z)

	lab = '$\mu=' +  "{:.3f}".format(mu) \
	 + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'

	fig7s = plt.gcf()
	plt.rcParams['figure.figsize']=(6,6)
	fig7s.set_size_inches((6,6))
	plt.figure(figsize=(6, 6))

	sns.distplot(z, bins=100, hist=1, \
		hist_kws={"histtype": "step", "linewidth": 1, "alpha": 0.3, "color": "g"}, \
		color="r")
	plt.title(lab)

	plt.xlabel('persisting links per user')
	plt.ylabel('kde')
	plt.xlim(-0.1,10.1)
	plt.tight_layout()
	#plt.show()
	plt.savefig('persisting_links_per_user_distr.eps')


def extract_user_avg_ST_weak():

	MO_MENT = defaultdict(int)
	for MO in MONTHS:
		MO_MENT[MO] = read_in_MO_graph(MO).copy()

	nd = defaultdict(list)

	for MO7s in MONTHS: 
		G = MO_MENT[MO7s]
		for node in G.vs:
			try:
				deg = G.degree(node.index)
			except IndexError:
				deg = 0 
			nd[node['name']].append(deg)

	nd_std = []
	for node in nd:
		#nd1_std = np.std(np.array(nd[node]))
		#nd_std.append(nd1_std)
		max_nd_diff = np.max(np.array(nd[node])) - np.min(np.array(nd[node]))
		nd_std.append(max_nd_diff)

	nd_std = np.array(nd_std)

	print 'Max std is %.2f and min std is %.2f and std of std is %2f ' \
		% (np.max(nd_std), np.min(nd_std), np.std(nd_std))

def extract_user_avg_ST_strong():

	MO_MENT = defaultdict(int)
	for MO in MONTHS:
		MO_MENT[MO] = read_in_MO_graph_MUTUAL_UNW(MO).copy()

	nd = defaultdict(list)

	for MO7s in MONTHS: 
		G = MO_MENT[MO7s]
		for node in G.vs:
			try:
				deg = G.degree(node.index)
			except IndexError:
				deg = 0 
			nd[node['name']].append(deg)

	nd_std = []
	for node in nd:
		#nd1_std = np.std(np.array(nd[node]))
		#nd_std.append(nd1_std)
		max_nd_diff = np.max(np.array(nd[node])) - np.min(np.array(nd[node]))
		nd_std.append(max_nd_diff)

	nd_std = np.array(nd_std)

	print 'Max std is %.2f and min std is %.2f and std of std is %2f ' \
		% (np.max(nd_std), np.min(nd_std), np.std(nd_std))

#extract_user_avg_ST_weak()
#extract_user_avg_ST_strong()

#read_persisting_links_per_user()



plot_persisting_links_per_user()



