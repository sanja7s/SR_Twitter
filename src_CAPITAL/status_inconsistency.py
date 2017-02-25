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
sns.set(color_codes=True, font_scale=2) 

from scipy.stats.stats import pearsonr


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
def save_node_popularity_rank():
	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)
	N = len(G.vs)
	pct = 10
	min_pct_ind = N / pct
	max_pct_ind = N - min_pct_ind
	print 'We have %d users and min %d pct index is %d and max %d pct index is %d ' % (N,pct,min_pct_ind,pct, max_pct_ind)
	deg_seq = []
	weighted_deg_seq = []

	for v in G.vs:
		node_id = v.index
		#node = G.vs[node_id]['name']
		deg_node = G.degree(node_id, mode=IN)
		deg_seq.append(deg_node)
		weighted_deg_node = G.strength(node_id, weights='weight', mode=IN)
		weighted_deg_seq.append(weighted_deg_node)
		
	deg_seq.sort()
	weighted_deg_seq.sort()
	#print deg_seq
	cnt_top = 0
	cnt_bottom = 0
	fo = open('node_pop_rank', 'w')
	fow = open('node_pop_weighted_rank', 'w')
	for v in G.vs:
		node_id = v.index
		node = G.vs[node_id]['name']
		deg_node = G.degree(node_id, mode=IN)
		weighted_deg_node = G.strength(node_id, weights='weight', mode=IN)
		my_rank = deg_seq.index(deg_node)
		my_weighted_rank = weighted_deg_seq.index(weighted_deg_node)
		
		if my_weighted_rank > max_pct_ind:
			cnt_top += 1
		elif my_weighted_rank < min_pct_ind:
			cnt_bottom += 1
			#print 'my degree is %d and my rank is %d ' % (deg_node, my_rank)
		fo.write(str(node) + '\t' + str(my_rank) + '\n')
		fow.write(str(node) + '\t' + str(my_weighted_rank) + '\n')

	print 'Total in top %d and total in bottom %d ' % (cnt_top, cnt_bottom)
	
# one time call
def save_node_semantic_rank():
	sc = read_sem_capital('entities','entities')
	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)
	N = len(G.vs)
	pct = 10
	min_pct_ind = N / pct
	max_pct_ind = N - min_pct_ind
	print 'We have %d users and min %d pct index is %d and max %d pct index is %d ' % (N,pct,min_pct_ind,pct, max_pct_ind)
	deg_seq = []
	for v in G.vs:
		node_id = v.index
		node = G.vs[node_id]['name']
		deg_node = sc[node]
		deg_seq.append(deg_node)
		
	deg_seq.sort()
	#print deg_seq
	cnt_top = 0
	cnt_bottom = 0

	fo = open('node_sem_rank', 'w')
	for v in G.vs:
		node_id = v.index
		node = G.vs[node_id]['name']
		deg_node = sc[node]

		my_rank = deg_seq.index(deg_node)
		
		if my_rank > max_pct_ind:
			cnt_top += 1
		elif my_rank < min_pct_ind:
			cnt_bottom += 1
			#print 'my degree is %d and my rank is %d ' % (deg_node, my_rank)
		fo.write(str(node) + '\t' + str(my_rank) + '\n')

	print 'Total in top %d and total in bottom %d ' % (cnt_top, cnt_bottom)
	
"""
	here we wanna assign a new attribute to the nodes: status incosistency
	it is defined in sociology as a node having a high status on one attribute
	and a low on another. out attributes are social and semantical capital
"""
def save_node_inconsistency_nominal():
	sc = read_sem_capital('entities','entities')
	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)
	N = len(G.vs)
	pct = 10
	min_pct_ind = N / pct
	max_pct_ind = N - min_pct_ind
	print 'We have %d users and min %d pct index is %d and max %d pct index is %d ' % (N,pct,min_pct_ind,pct, max_pct_ind)
	deg_seq = []
	weighted_deg_seq = []
	sem_seq = []
	# first we read in all the degrees in 3 sequences
	# so that we can sort them and in a second pass
	# check which node ranks how on each attribute
	for v in G.vs:
		node_id = v.index
		node = G.vs[node_id]['name']
		deg_node = G.degree(node_id, mode=IN)
		deg_seq.append(deg_node)
		weighted_deg_node = G.strength(node_id, weights='weight', mode=IN)
		weighted_deg_seq.append(weighted_deg_node)
		sem_deg = sc[node]
		sem_seq.append(sem_deg)
	# sort the attribute values on the nodes
	deg_seq.sort()
	weighted_deg_seq.sort()
	sem_seq.sort()
	#print deg_seq
	cnt_top = 0
	cnt_bottom = 0
	fo = open('node_inconsistency', 'w')
	fow = open('node_inconsistency_weighted', 'w')
	# the second pass where we check for each node whether it is
	# status incosistent and save 1 otherwise we save value 0
	for v in G.vs:
		node_id = v.index
		node = G.vs[node_id]['name']
		deg_node = G.degree(node_id, mode=IN)
		weighted_deg_node = G.strength(node_id, weights='weight', mode=IN)
		sem_deg = sc[node]
		my_rank = deg_seq.index(deg_node)
		my_weighted_rank = weighted_deg_seq.index(weighted_deg_node)
		my_sem_rank = sem_seq.index(sem_deg)
		
		if my_rank > max_pct_ind and my_sem_rank < min_pct_ind:
			cnt_top += 1
			fo.write(str(node) + '\t' + str(1) + '\n')
		elif my_rank < min_pct_ind and my_sem_rank > max_pct_ind:
			cnt_bottom += 1
			fo.write(str(node) + '\t' + str(1) + '\n')
		else:
			fo.write(str(node) + '\t' + str(0) + '\n')		

		if my_weighted_rank > max_pct_ind and my_sem_rank < min_pct_ind:
			cnt_top += 1
			fow.write(str(node) + '\t' + str(1) + '\n')
		elif my_weighted_rank < min_pct_ind and my_sem_rank > max_pct_ind:
			cnt_bottom += 1
			fow.write(str(node) + '\t' + str(1) + '\n')
		else:
			fow.write(str(node) + '\t' + str(0) + '\n')	

	print 'Total in top %d and total in bottom %d ' % (cnt_top, cnt_bottom)

def save_node_inconsistency_scalar():
	sc = read_sem_capital('entities','entities')
	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)
	N = len(G.vs)
	pct = 10
	min_pct_ind = N / pct
	max_pct_ind = N - min_pct_ind
	print 'We have %d users and min %d pct index is %d and max %d pct index is %d ' % (N,pct,min_pct_ind,pct, max_pct_ind)
	deg_seq = []
	weighted_deg_seq = []
	sem_seq = []
	# first we read in all the degrees in 3 sequences
	# so that we can sort them and in a second pass
	# check which node ranks how on each attribute
	for v in G.vs:
		node_id = v.index
		node = G.vs[node_id]['name']
		deg_node = G.degree(node_id, mode=IN)
		deg_seq.append(deg_node)
		weighted_deg_node = G.strength(node_id, weights='weight', mode=IN)
		weighted_deg_seq.append(weighted_deg_node)
		sem_deg = sc[node]
		sem_seq.append(sem_deg)
	# sort the attribute values on the nodes
	deg_seq.sort()
	weighted_deg_seq.sort()
	sem_seq.sort()
	#print deg_seq
	cnt_top = 0
	cnt_bottom = 0
	fo = open('node_scalar_inconsistency_v2', 'w')
	#fow = open('node_incosistency_weighted', 'w')
	# the second pass where we check for each node whether it is
	# status incosistent and save 1 otherwise we save value 0
	for v in G.vs:
		node_id = v.index
		node = G.vs[node_id]['name']
		deg_node = G.degree(node_id, mode=IN)
		weighted_deg_node = G.strength(node_id, weights='weight', mode=IN)
		sem_deg = sc[node]
		my_rank = deg_seq.index(deg_node)
		my_weighted_rank = weighted_deg_seq.index(weighted_deg_node)
		my_sem_rank = sem_seq.index(sem_deg)

		if my_rank < my_sem_rank:
			my_incosistency = (1 - float(my_rank) / float(my_sem_rank)) * (-1)
		elif my_rank > my_sem_rank:
			my_incosistency = (1 - float(my_sem_rank) / float(my_rank))
		else:
			my_rank = 0
		fo.write(str(node) + '\t' + str(my_incosistency) + '\n')		
	#fow.write(str(node) + '\t' + str(my_weighted_rank) + '\n')
	
def read_node_inconsistency_2graph(filename='status_inconsistency'):
	print 'Reading in inconsistency node attributes to G '
	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)
	f = open(filename, "r")

	for line in f:
		(vid, val) = line.split('\t')
		val = float(val)
		v = G.vs.select(name = vid)
		v["att"] = val

	to_delete_vertices = [v.index for v in G.vs if v["att"] == None]
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)	
	return G

# one time call
def save_edge_inconsistency_abs():
	G =  read_node_inconsistency_2graph()
	fo = open('weight_inconsistency_on_edge_float.dat', 'w')
	for e in G.es:
		src_id = e.source
		dest_id = e.target

		src = G.vs[src_id]['name']
		dest = G.vs[dest_id]['name']

		src_inc = G.vs[src_id]['att']
		dest_inc = G.vs[dest_id]['att']

		abs_einc = max(abs(src_inc), abs(dest_inc))
		ew = e['weight']
		fo.write(str(ew) + '\t' + str(abs_einc) + '\n')

# one time call
def save_edge_inconsistency():
	G =  read_node_inconsistency_2graph()
	fo = open('weight_inconsistency_on_edge_float.dat', 'w')
	for e in G.es:
		src_id = e.source
		dest_id = e.target

		src = G.vs[src_id]['name']
		dest = G.vs[dest_id]['name']

		src_inc = G.vs[src_id]['att']
		dest_inc = G.vs[dest_id]['att']

		f_einc = src_inc * dest_inc
		ew = e['weight']
		fo.write(str(ew) + '\t' + str(f_einc) + '\n')

#save_edge_inconsistency()

# one time call
def save_edge_inconsistency_abs_MUTUAL():
	G =  read_node_inconsistency_2graph()
	G.to_undirected(mode='mutual',combine_edges=sum)
	not_connected_nodes = G.vs(_degree_eq=0)
	to_delete_vertices = not_connected_nodes
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)
	fo = open('MUTUAL_sum_weight_inconsistency_on_edge_float.dat', 'w')
	for e in G.es:
		src_id = e.source
		dest_id = e.target

		src = G.vs[src_id]['name']
		dest = G.vs[dest_id]['name']

		src_inc = G.vs[src_id]['att']
		dest_inc = G.vs[dest_id]['att']

		abs_einc = max(abs(src_inc), abs(dest_inc))
		ew = e['weight']
		fo.write(str(ew) + '\t' + str(abs_einc) + '\n')

#save_edge_inconsistency_abs_MUTUAL()

def read_in_edge_weight_inconsistency(file_name= 'weight_inconsistency_on_edge_float.dat'):
	f = open(file_name, 'r')
	s = defaultdict(float)
	for line in f:
		(ew, einc) = line.split('\t')
		s[float(ew)] = float(einc)
	return s

def plot_edge_weight_vs_inconsistency(fn):
	s = read_in_edge_weight_inconsistency(file_name=fn)
	#coef_soc = 100
	w = []
	inc = []
	
	for el in s:
		# weight
		w.append(el)
		# inconsistency
		einc = s[el]
		inc.append(einc)

	w=np.array(w)
	inc=np.array(inc)
	print np.corrcoef(w,inc)

	print pearsonr(w, inc)

	ylabel = '$CI(e)$'
	xlabel = '$st_{inc}(e)$'

	plt.clf()
	fig7s = plt.gcf()
	plt.rcParams['figure.figsize']=(6,6)
	fig7s.set_size_inches((6,6))
	plt.figure(figsize=(6, 6))
	sns.set_style("white")
	g = sns.jointplot(x=inc, y=w, kind="scatter", annot_kws=dict(stat="r"),\
	 color="green", xlim=(-1.07,1.07)).set_axis_labels(xlabel, ylabel)

	#plt.tight_layout()
	
	#plt.grid(True)
	plt.savefig('dir_edge_weight_vs_incon_float7s22scatter7777.eps', dpi=500, bbox_inches='tight')


def plot_edge_weight_vs_inconsistency_binning(fn):
	s = read_in_edge_weight_inconsistency(file_name=fn)
	#coef_soc = 100
	w = []
	inc = []
	
	for el in s:
		# weight
		w.append(el)
		# inconsistency
		einc = s[el]
		inc.append(einc)

	w=np.array(w)
	inc=np.array(inc)
	print np.corrcoef(w,inc)

	print pearsonr(w, inc)

	ylabel = '$CI(e)$'
	xlabel = '$st_{inc}(e)$'

	plt.clf()
	fig7s = plt.gcf()
	plt.rcParams['figure.figsize']=(6,6)
	fig7s.set_size_inches((6,6))
	plt.figure(figsize=(6, 6))
	sns.set_style("white")

	#g = sns.jointplot(x=inc, y=w, kind="scatter", annot_kws=dict(stat="r"),\
	# color="green", xlim=(-1.07,1.07)).set_axis_labels(xlabel, ylabel)

	g = sns.jointplot(y=inc, x=w+1, ylim=(-0.07,1.07),xlim=(0.777,1500),\
		kind='reg',annot_kws=dict(stat="r"),color='green',\
		x_bins=[5,10,20,50,100,200,500,800],logx=1,\
		joint_kws={'line_kws':{'color':'gray','markeredgewidth':0,\
		'alpha':0.3, 'markeredgewidth':0}}).set_axis_labels(ylabel, xlabel)

	ax = g.ax_joint
	ax.set_xscale('log')
	#g.ax_marg_y.set_xscale('log')
	
	#plt.grid(True)
	plt.savefig('dir_edge_weight_vs_incon_float7s22scatter7777.pdf', dpi=500, bbox_inches='tight')


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

def jackknife_dir(G, r):
	ri = []
	G1 = G.copy()
	print len(G.es)
	i = 0
	for e in G.es:
		G1.delete_edges((e.source, e.target))

		r1 = G1.assortativity("att",directed=True)

		ri.append(r1)
		if i%1000==0:
			print i, r1
		i += 1

		G1.add_edge(e.source, e.target)
	s = 0.0
	for r1 in ri:
		s += (r1-r)*(r1-r)
	return math.sqrt(s)

def jackknife_undir(G, r):
	ri = []
	G1 = G.copy()
	print len(G.es)
	i = 0
	for e in G.es:
		G1.delete_edges((e.source, e.target))

		r1 = G1.assortativity("att",directed=False)

		ri.append(r1)
		if i%1000==0:
			print i, r1
		i += 1

		G1.add_edge(e.source, e.target)
	s = 0.0
	for r1 in ri:
		s += (r1-r)*(r1-r)
	return math.sqrt(s)

def status_inconsistency_igraph_assortativity(filename='node_inconsistency'):

	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)
	f = open(filename, "r")

	for line in f:
		(vid, val) = line.split('\t')
		val = int(val)
		v = G.vs.select(name = vid)
		v["att"] = val

	to_delete_vertices = [v.index for v in G.vs if v["att"] == None]
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	print "nominal node incosistency assortativity is %f " %  (G.assortativity_nominal(types="att",directed=True))
	#print "label assortativity is %f " %  (G.assortativity(types1="att",types2="att",directed=True))
	print "label node incosistency assortativity is %f " %  (G.assortativity("att",directed=True))

	r = G.assortativity("att",directed=True)
	s = jackknife_dir(G, r)
	print filename + " DIR assortativity is %f and st. sign. is %f " % (r, s)

	###########################################

	G.to_undirected(mode='mutual')

	not_connected_nodes = G.vs(_degree_eq=0)

	to_delete_vertices = not_connected_nodes
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)

	r = G.assortativity("att",directed=False)
	s = jackknife_undir(G, r)
	print " MUTUAL node incosistency assortativity is %f and st. sign. is %f " % (r, s)

def status_inconsistency_scalar_igraph_assortativity(filename='node_scalar_inconsistency_v2'):
	G = Graph.Read_Ncol(f_in_graph_weights,names=True, directed=True, weights=True)
	summary(G)
	f = open(filename, "r")
	for line in f:
		(vid, val) = line.split('\t')
		val = float(val)
		v = G.vs.select(name = vid)
		v["att"] = val

	to_delete_vertices = [v.index for v in G.vs if v["att"] == None]
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)
	print "label node incosistency assortativity is %f " %  (G.assortativity("att",directed=True))

	#r = G.assortativity("att",directed=True)
	#s = jackknife_dir(G, r)
	#print filename + " DIR assortativity is %f and st. sign. is %f " % (r, s)

	###########################################

	G.to_undirected(mode='mutual')

	not_connected_nodes = G.vs(_degree_eq=0)

	to_delete_vertices = not_connected_nodes
	print len(to_delete_vertices)
	G.delete_vertices(to_delete_vertices)
	summary(G)
	print "label node incosistency assortativity MUTUAL is %f " %  (G.assortativity("att",directed=False))

	#r = G.assortativity("att",directed=False)
	#s = jackknife_undir(G, r)
	#print " MUTUAL node incosistency assortativity is %f and st. sign. is %f " % (r, s)


#plot_edge_weight_vs_inconsistency('weight_inconsistency_on_edge_float.dat')

plot_edge_weight_vs_inconsistency_binning('weight_inconsistency_on_edge_float.dat')

#status_inconsistency_igraph_assortativity()
#status_inconsistency_scalar_igraph_assortativity()

#save_node_inconsistency_scalar()