#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os
import matplotlib.cm as cm
from collections import defaultdict
import matplotlib
from scipy import stats

import seaborn as sns
sns.set(color_codes=True, font_scale=2) 
sns.set_style('whitegrid')

import pandas as pd
from scipy import stats, integrate

IN_DIR = "../../../DATA/General/"
os.chdir(IN_DIR)

MONTHS =  ["5", "6", "7", "8", "9", "10", "11"]
MONTHS2 =  ["6", "7", "8", "9", "10"]
MONTHS_name =  {"5":"May", "6":"Jun", "7":"Jul", "8":"Aug", "9":"Sept", "10":"Oct", "11":"Nov"}

parts =  ["0", "1", "2", "3", "4", "5", "6", "7"]

import matplotlib.colors as colors
import matplotlib.cm as cmx
cmBlues = plt.get_cmap('Blues') 
cmReds = plt.get_cmap('Reds') 
cmGreens = plt.get_cmap('Greens') 
cNorm  = colors.Normalize(vmin=5, vmax=10) # 11 for all MOs
scalarMapBlues = cmx.ScalarMappable(norm=cNorm, cmap=cmBlues)
scalarMapReds = cmx.ScalarMappable(norm=cNorm, cmap=cmReds)
scalarMapGreens = cmx.ScalarMappable(norm=cNorm, cmap=cmGreens)

def read_in_MENT_SR(f2, threshold = 0):
	cnt_MO_edges = 0
	edges_SR = []
	for line in f2:
		(uid1, uid2, SR, w1, w2) = line.split()
		uid1 = int(uid1)
		uid2 = int(uid2)
		#if int(w1) == 0 or int(w2) == 0:
		#	continue
		cnt_MO_edges += 1
		SR = float(SR)
		if uid1 != uid2:
			edges_SR.append(SR)
	print 'Monthly edges ', cnt_MO_edges
	return edges_SR

def read_in_MENT_edges(threshold = 0):
	cnt_edges = 0
	edges = defaultdict(int)
	for line in open('mention_graph_weights_7s.dat', 'r'):
		(uid1, uid2, w) = line.split()
		uid1 = int(uid1)
		uid2 = int(uid2)
		cnt_edges += 1
		if uid1 != uid2:
			edges[(uid1,uid2)] = 1
	print 'Total edges ', cnt_edges
	return edges

def read_in_full_SR(f_name, threshold = 0):
	edges_SR = []
	for s in parts:
		f = open(f_name + s, 'r')
		for line in f:
			(uid1, uid2, SR) = line.split()
			uid1 = int(uid1)
			uid2 = int(uid2)
			SR = float(SR)
			if uid1 != uid2:
				edges_SR.append(SR)
		f.close()
		print 'part ', s, ' read'				
	return edges_SR

def read_in_NOMENT_SR(f_name, threshold = 0):
	MENT_edges = read_in_MENT_edges()
	edges_SR = []
	cnt_omitted = 0
	cnt_edges = 0
	for s in parts:
		f = open(f_name + s, 'r')
		for line in f:
			(uid1, uid2, SR) = line.split()
			uid1 = int(uid1)
			uid2 = int(uid2)
			SR = float(SR)
			if (uid1,uid2) in MENT_edges or (uid2,uid1) in MENT_edges:
				cnt_omitted += 1
				continue
			if uid1 != uid2:
				edges_SR.append(SR)
				cnt_edges += 1
		f.close()
		print 'part ', s, ' read'	
		print cnt_edges, cnt_omitted			
	return edges_SR

def plot_one_seaborn(MO, z, c):
	x = np.array(z, dtype=np.float) 
	mu = np.mean(z)
	sigma = np.std(z)

	print MO + ' mention network SR: $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'	
	lab = MONTHS_name[MO] + ' $\mu=' +  "{:.3f}".format(mu) + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'

	sns.kdeplot(x, color=c, label=lab, cumulative=1, shade_lowest=0, legend=0)

	plt.ylim((0.7,1.01))

	plt.xlabel('SR')
	plt.ylabel('CDF')
	plt.xlim(0,1)
	plt.legend(loc='lower right', prop={'size':20})

def plot_inset_seaborn(MO, z, c):

	x = np.array(z, dtype=np.float) 

	sns.kdeplot(x, color=c, cumulative=1, shade_lowest=0)

	plt.ylim((0.7,1.01))

	
def main_MENT_pdf_MO():
	IN_DIR = "monthly_SR_change_list_of_users/"
	os.chdir(IN_DIR)

	for MO in MONTHS2:
		f = open(str(MO) + "mention_edges_monthly_SR", "r")
		edges_SR_MENT = read_in_MENT_SR(f)
		print MO, len(edges_SR_MENT)
		z = np.array(edges_SR_MENT, dtype=np.float) 
		mu = np.mean(z)
		sigma = np.std(z)
		#if MO == '6':
		#	edges_SR_MENT_old = edges_SR_MENT
			
		#if MO == '10':
		#	s = stats.ks_2samp(edges_SR_MENT_old, edges_SR_MENT)
		#	print s
		

		c = scalarMapBlues.to_rgba(int(MO))
		plot_one_seaborn(MO, edges_SR_MENT, c)	
	
	os.chdir("../")
	plt.savefig("MO_MENT_SR_FIN_7s_FIN_log77777_xoxox.eps", bbox_inches='tight' , dpi = 550)

def main_SR_pdf_MO():
	x = defaultdict(list)
	y = defaultdict(list)
	l = defaultdict(str)
	for MO in MONTHS2:
		fn = MO + 'MOSR/' + MO + '_all_user_SR_part_'
		edges_SR_SR = read_in_full_SR(fn)
		z = np.array(edges_SR_SR, dtype=np.float) 
		mu = np.mean(z)
		sigma = np.std(z)
		print MO + ' TOTAL $\mu=' +  "{:.3f}".format(mu)\
		 + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'
		ESR = np.random.choice(edges_SR_SR, 100000)
		if MO == '6':
			ESR_old = ESR
			
		if MO == '10':
			s = stats.ks_2samp(ESR_old, ESR)
			print s
		c = scalarMapReds.to_rgba(int(MO))
		plot_one_seaborn(MO, ESR, c)		

	plt.savefig("MO_SR_SR_hist_FIN_7s_FIN1144777.eps", bbox_inches='tight' ,dpi = 550)

def main_NOMENT_pdf_MO():
	x = defaultdict(list)
	y = defaultdict(list)
	l = defaultdict(str)
	for MO in MONTHS2:
		fn = MO + 'MOSR/' + MO + '_all_user_SR_part_'
		edges_SR_SR = read_in_NOMENT_SR(fn)
		print MO, len(edges_SR_SR)
		z = np.array(edges_SR_SR, dtype=np.float) 
		mu = np.mean(z)
		sigma = np.std(z)
		print MO + ' TOTAL NOMENT $\mu=' +  "{:.3f}".format(mu)\
		 + '$, $\sigma= ' + "{:.3f}".format(sigma) + '$'
		ESR = np.random.choice(edges_SR_SR, 1000000)
		if MO == '6':
			ESR_old = ESR
			
		if MO == '10':
			s = stats.ks_2samp(ESR_old, ESR)
			print s
		c = scalarMapGreens.to_rgba(int(MO))
		plot_one_seaborn(MO, ESR, c)		

	plt.savefig("7sNOMENT_hist_FIN_7s_FIN114477777777777777.eps", bbox_inches='tight' ,dpi = 550)



fig7s = plt.gcf()
plt.rcParams['figure.figsize']=(6,6)
fig7s.set_size_inches((6,6))
plt.figure(figsize=(6, 6))

#main_SR_pdf_MO()
#main_MENT_pdf_MO()

main_NOMENT_pdf_MO()
