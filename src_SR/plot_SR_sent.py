#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	plot SR vs sentiment delta
'''
import os
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.cm as cm

IN_DIR = '../../../ALL_SR'
img_out_plot = "sentiment/SR_delta_SENT_ALL.png"
# from 5 and higher they are ok
img_out_plot_MENT = "sentiment/SR_delta_SENT_MENT_v7.png"
#########################

#########################
# read from a file user sent
#########################
def read_in_user_sent():
	SENT = defaultdict(int)
	f = open('sentiment/user_sentiment.tab', "r")
	cnt = 0
	for line in f:
		(vid, vsent, vsentval) = line[:-1].split('\t')
		vid = int(vid)
		vsent = int(vsent)
		vsentval = float(vsentval)
		SENT[vid] = vsentval
		cnt += 1

	print 'Read in %d users sentiment' % cnt
	return SENT

#########################
# read from a file the full SR graph
#########################
def read_in_res():
	SENT = read_in_user_sent()

	f = open('ALL_SR_IDs.weighted_edge_list', 'r')
	#f = open('filter_IDs_SR', 'r')
	xSR = []
	yDELTASENT = []
	cnt = 0
	for line in f:
		(uid1, uid2, SR) = line.split()
		uid1 = int(uid1)
		uid2 = int(uid2)
		SR = float(SR)
		sent1 = SENT[uid1] 
		sent2 = SENT[uid2]
		deltasent = abs(abs(sent1) - abs(sent2))
		if sent1 > 0 and sent2 > 0:
			xSR.append(SR)
			yDELTASENT.append(deltasent)
		elif sent1 * sent2 < 0:
			xSR.append(SR)
			yDELTASENT.append(deltasent*-1)
			xSR.append(SR*-1)
			yDELTASENT.append(deltasent)
		elif sent1 < 0 and sent2 < 0:
			xSR.append(SR*-1)
			yDELTASENT.append(deltasent*-1)
		cnt += 1
		if cnt % 100000 == 0:
			print 'Processed %d edges' % cnt

	"""
	f3 = open('sentiment/SR_delta_sent_0.2.tab', 'w')
	for i in range(len(xSR)):
		f3.write(str(xSR[i]) + '\t' + str(yDELTASENT[i]) + '\n')
	"""

	return xSR, yDELTASENT

#########################
# read from a file the MENT graph
#########################
def read_in_res_MENT():
	SENT = read_in_user_sent()

	f = open('mention_graph_IDs_with_SR_weight.dat', 'r')
	xSR = []
	yDELTASENT = []
	yWEIGHT = []
	cnt = 0
	for line in f:
		(uid1, uid2, SR, w) = line.split()
		if uid1 == uid2:
			continue
		uid1 = int(uid1)
		uid2 = int(uid2)
		SR = float(SR)
		w = int(w)
		if w < 20:
			continue
		sent1 = SENT[uid1] 
		sent2 = SENT[uid2]
		deltasent = abs(abs(sent1) - abs(sent2))
		
		if sent1 > 0 and sent2 > 0:
			#continue
			xSR.append(SR)
			yDELTASENT.append(deltasent)
			yWEIGHT.append(w)
		elif sent1 * sent2 < 0:
			xSR.append(SR)
			yDELTASENT.append(deltasent*-1)
			yWEIGHT.append(w)
			xSR.append(SR*-1)
			yDELTASENT.append(deltasent)
			yWEIGHT.append(w)
		elif sent1 < 0 and sent2 < 0:
			#continue
			xSR.append(SR*-1)
			yDELTASENT.append(deltasent*-1)
			yWEIGHT.append(w)
		cnt += 1
		if cnt % 1000 == 0:
			print 'Processed %d edges' % cnt

	"""
	f3 = open('sentiment/SR_delta_sent_0.2.tab', 'w')
	for i in range(len(xSR)):
		f3.write(str(xSR[i]) + '\t' + str(yDELTASENT[i]) + '\n')
	"""

	print len(xSR), len(yDELTASENT), len(yWEIGHT)

	return xSR, yDELTASENT, yWEIGHT

def plot_SR_deltaSENT(xaxis, yaxis):
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1) 
	x = np.array(xaxis)
	y = np.array(yaxis)
	plt.plot(x, y, 'oc')
	#plt.scatter(x, y,  s=1,  marker='+', facecolor='0.5', lw = 0)
	plt.grid(True)
	plt.title('SR vs. delta sent')
	#plt.legend(bbox_to_anchor=(0, 1), bbox_transform=plt.gcf().transFigure)
	plt.ylabel('delta sentiment on the edge')
	plt.xlabel('SR on the edge')

                                   
	major_ticks = np.arange(-1, 1, 0.5)                                    
	plt.xticks(major_ticks, np.absolute(major_ticks) )
	plt.yticks(major_ticks, np.absolute(major_ticks) )

	plt.savefig(img_out_plot,format='png',dpi=200)

def plot_SR_deltaSENT_MENT(xaxis, yaxis, zaxis):
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1) 
	x = np.array(xaxis)
	y = np.array(yaxis)
	w = np.array(zaxis)
	#plt.plot(x, y, 'oc', s = w)
	plt.scatter(x, y,  s=w,  marker='o', facecolor='c', lw =0.02)
	plt.grid(True)
	plt.title('SR vs. delta sent in mention network')
	#plt.legend(bbox_to_anchor=(0, 1), bbox_transform=plt.gcf().transFigure)
	plt.ylabel('delta sentiment on mention edge')
	plt.xlabel('SR on mention edge')

                                   
	major_ticks = np.arange(-1, 1, 0.5)                                    
	plt.xticks(major_ticks, np.absolute(major_ticks) )
	plt.yticks(major_ticks, np.absolute(major_ticks) )

	plt.xlim(-1, 1)
	plt.ylim(-1, 1)

	plt.savefig(img_out_plot_MENT,format='png',dpi=200)

def get_heatmap(xx, yy):

	xx = np.array(xx, dtype='float32')
	yy = np.array(yy, dtype='float32')

	heatmap, xedges, yedges = np.histogram2d(yy, xx,  bins=50) # range=([-0.6,0.7],[-0.6,0.7]),
	extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

	return heatmap, extent


def plot_heatmap(heatmap, extent, fig_name, colmap=cm.PuOr):
	plt.clf()
	plt.imshow(np.log(heatmap + 1), cmap=colmap, interpolation='nearest', extent=extent, origin = 'lower') # 
	plt.colorbar(label='log(density)')

	major_ticks = np.arange(-1, 1, 0.5)                                    
	plt.xticks(major_ticks, np.absolute(major_ticks) )
	plt.yticks(major_ticks, np.absolute(major_ticks) )

	plt.xlabel('Edge SR')
	plt.ylabel('edge delta sentiment')

	plt.savefig("sentiment/" + fig_name, dpi = 700)

	#plt.show()

def scatterplot_SR_deltasent(x, y):

	heatmap, extent = get_heatmap(x, y)
	fig_name = "SR_deltasent_ALL_v2.png"
	plot_heatmap(heatmap, extent, fig_name, colmap=cm.coolwarm)

def get_heatmap_MENT(xx, yy, ww):

	xx = np.array(xx, dtype='float32')
	yy = np.array(yy, dtype='float32')
	ww = np.array(ww, dtype='float32')

	heatmap, xedges, yedges = np.histogram2d(yy, xx, weights=ww, bins=100, normed=False) # range=([-0.6,0.7],[-0.6,0.7]),

	"""
	xxx = []
	yyy = []

	for i in range(len(ww)):
		for j in range(ww[i]):
			xxx.append(xx[i])
			yyy.append(yy[i])

	print len(xxx)
	print len(yyy)


	xxx = np.array(xxx, dtype='float32')
	yyy = np.array(yyy, dtype='float32')
	

	heatmap, xedges, yedges = np.histogram2d(xxx, yyy,  bins=100) # range=([-0.6,0.7],[-0.6,0.7]),
	"""


	extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

	return heatmap, extent


def plot_heatmap_MENT(heatmap, extent, fig_name, colmap=cm.PuOr):
	plt.clf()
	plt.imshow(np.log(1+heatmap), cmap=colmap, interpolation='none', extent=extent, origin = 'lower') # 
	plt.colorbar(label='mention weight based density')

	major_ticks = np.arange(-1, 1, 0.5)                                    
	#plt.xticks(major_ticks, np.absolute(major_ticks) )
	#plt.yticks(major_ticks, np.absolute(major_ticks) )

	plt.xlabel('Mention edge SR')
	plt.ylabel('Mention edge delta sentiment')

	plt.savefig("sentiment/" + fig_name, dpi = 440)

	#plt.show()

def scatterplot_SR_deltasent_MENT(x, y, w):

	heatmap, extent = get_heatmap_MENT(x, y, w)
	fig_name = "SR_deltasent_MENT_v7_log.png"
	plot_heatmap_MENT(heatmap, extent, fig_name)


def main_FULL_SR():
	os.chdir(IN_DIR)
	x, y = read_in_res()
	#plot_SR_deltaSENT(x, y)
	scatterplot_SR_deltasent(x, y)

#main_FULL_SR()


def main_MENT():
	os.chdir(IN_DIR)
	x, y, w = read_in_res_MENT()
	#plot_SR_deltaSENT_MENT(x, y, w)
	scatterplot_SR_deltasent_MENT(x, y, w)

main_MENT()