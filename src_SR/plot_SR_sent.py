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
from scipy import stats

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
	maxdelta = 0
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
		deltasent = abs(sent1 - sent2)
		if deltasent > maxdelta:
			maxdelta = deltasent
		if sent1 > 0 and sent2 > 0:
			xSR.append(SR)
			yDELTASENT.append(deltasent)
		elif sent1 * sent2 <= 0:
			xSR.append(SR)
			yDELTASENT.append(deltasent*-1)
			xSR.append(SR*-1)
			yDELTASENT.append(deltasent)
		elif sent1 < 0 and sent2 < 0:
			xSR.append(SR*-1)
			yDELTASENT.append(deltasent*-1)
		cnt += 1
		if cnt % 1700000 == 0:
			print 'Processed %d edges' % cnt
			#break
	print 'MAX ', maxdelta

	return xSR, yDELTASENT

#########################
# read from a file the MENT graph
#########################
def read_in_res_MENT():
	SENT = read_in_user_sent()

	f = open('mutual_graph_weights_and_SR', 'r')
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
		if w < 0:
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

#########################
# read from a file the MENT graph
#########################
def read_in_res_MENT_v2():
	SENT = read_in_user_sent()

	f = open('mutual_graph_SR_and_weights', 'r')
	xSR = []
	yDELTASENT = []
	yWEIGHT = []
	cnt = 0
	maxdelta = 0 

	for line in f:
		(uid1, uid2, SR, w) = line.split()
		if uid1 == uid2:
			continue
		uid1 = int(uid1)
		uid2 = int(uid2)
		SR = float(SR)
		w = int(w)
		if w < 0:
			continue
		sent1 = SENT[uid1] 
		sent2 = SENT[uid2]
		deltasent = abs(sent1 - sent2)
		if deltasent > maxdelta:
			maxdelta = deltasent
		if deltasent > 1.5:
			print deltasent, sent1, sent2
		
		if sent1 > 0 and sent2 > 0:
			#continue
			xSR.append(SR)
			yDELTASENT.append(deltasent)
			yWEIGHT.append(w)
		elif sent1 * sent2 <= 0:
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

	print 'MAX delta', maxdelta

	print len(xSR), len(yDELTASENT), len(yWEIGHT)

	print stats.pearsonr(np.array(xSR), np.array(yDELTASENT))

	return xSR, yDELTASENT, yWEIGHT


#########################
# read from a file the MENT graph
#########################
def read_in_res_MENT_SIMPLE():
	SENT = read_in_user_sent()

	f = open('mutual_graph_SR_and_weights', 'r')
	xSR = []
	yDELTASENT = []
	yWEIGHT = []
	cnt = 0
	maxdelta = 0
	for line in f:
		(uid1, uid2, SR, w) = line.split()
		if uid1 == uid2:
			continue
		uid1 = int(uid1)
		uid2 = int(uid2)
		SR = float(SR)
		w = float(w)
		if w < 0:
			continue
		sent1 = SENT[uid1] 
		sent2 = SENT[uid2]
		deltasent = abs(sent1 - sent2)
		if deltasent > 1.5:
			print deltasent, sent1, sent2
		if deltasent > maxdelta:
			maxdelta = deltasent
		
		xSR.append(SR)
		yDELTASENT.append(deltasent)
		yWEIGHT.append(w)
	print 'MAX delta', maxdelta
	print len(xSR), len(yDELTASENT), len(yWEIGHT)
	print stats.pearsonr(np.array(xSR), np.array(yDELTASENT))
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

	heatmap, xedges, yedges = np.histogram2d(xx, yy,  bins=50) 
	heatmap = heatmap.T
	extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

	return heatmap, extent

def plot_heatmap(heatmap, extent, fig_name, colmap=cm.PuOr):
	plt.clf()
	plt.imshow(np.log(heatmap + 1), cmap=colmap, interpolation='nearest', extent=extent, origin = 'lower') # 
	plt.colorbar(label='log(density)')

	xmajor_ticks = np.arange(-1, 1.01, 0.5)
	xlabels = ['1','0.5','0','0.5','1']                                    
	plt.xticks(xmajor_ticks, xlabels) 

	ymajor_ticks = np.arange(-2, 2.01, 0.5)
	ylabels = ['2','1.5','1','0.5','0','0.5','1','1.5', '2']
	plt.yticks(ymajor_ticks, ylabels)

	plt.xlabel('pair SR')
	plt.ylabel('pair absolute delta sentiment')

	plt.savefig("sentiment/" + 'S7S1_' + fig_name, dpi = 220)

	#plt.show()

def scatterplot_SR_deltasent(x, y):

	heatmap, extent = get_heatmap(x, y)
	fig_name = "SR_deltasent_ALL_v6.png"
	plot_heatmap(heatmap, extent, fig_name, colmap=cm.coolwarm)

def get_heatmap_MENT(xx, yy, ww):

	xx = np.array(xx, dtype='float32')
	yy = np.array(yy, dtype='float32')
	ww = np.array(ww, dtype='float32')

	heatmap, xedges, yedges = np.histogram2d(xx, yy, weights=ww, bins=100, normed=False) # range=([-0.6,0.7],[-0.6,0.7]),

	heatmap = heatmap.T
	extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

	return heatmap, extent

def get_colormesh_MENT(xx, yy, ww):

	xx = np.array(xx, dtype='float32')
	yy = np.array(yy, dtype='float32')
	ww = np.array(ww, dtype='float32')

	heatmap, xedges, yedges = np.histogram2d(xx, yy, weights=ww, bins=100, normed=False) 
	heatmap = heatmap.T

	return heatmap, xedges, yedges

def plot_heatmap_MENT(heatmap, extent, fig_name, colmap=cm.PuOr):
	plt.clf()
	plt.imshow(np.log(1+heatmap), cmap=colmap, interpolation='none', extent=extent, origin = 'lower') # 
	plt.colorbar(label='mention weight based density')

	xmajor_ticks = np.arange(-1, 1, 0.5)
	xlabels = ['1','0.5','0','0.5','1']                                    
	plt.xticks(xmajor_ticks, xlabels) 

	ymajor_ticks = np.arange(-2, 2.01, 0.5)
	ylabels = ['2', '1.5','1','0.5','0','0.5','1','1.5', '2']
	plt.yticks(ymajor_ticks, ylabels)

	plt.xlabel('link SR')
	plt.ylabel('link absolute delta sentiment')

	plt.savefig("sentiment/" +   fig_name, dpi = 220)

	plt.show()

def plot_colormesh_MENT(heatmap, xedges, yedges, fig_name, colmap=cm.PuOr):
	plt.clf()
	fig = plt.figure()
	X, Y = np.meshgrid(xedges, yedges)
	ax = fig.add_subplot(111)
	ax.pcolormesh(X, Y, np.log(heatmap + 1))

	xmajor_ticks = np.arange(-1, 1, 0.5)
	xlabels = ['1','0.5','0','0.5','1']                                    
	plt.xticks(xmajor_ticks, xlabels) 

	#plt.xlim(-0.2,0.2)

	ymajor_ticks = np.arange(-1.5, 1.5, 0.5)
	#ymajor_ticks = np.arange(-1, 1, 0.5)
	#plt.ylim(-1,1)
	ylabels = ['1.5','1','0.5','0','0.5','1','1.5']
	#ylabels = ['1','0.5','0','0.5','1']   
	plt.yticks(ymajor_ticks, ylabels)
	plt.xlabel('link SR')
	plt.ylabel('link absolute delta sentiment')

	plt.savefig("sentiment/" +  'S7S_' + fig_name, dpi = 200)

def scatterplot_SR_deltasent_MENT(x, y, w):

	heatmap, extent = get_heatmap_MENT(x, y, w)
	fig_name = "SR_deltasent_MENT_v7_log_7.png"
	plot_heatmap_MENT(heatmap, extent, fig_name)

def colormesh_SR_deltasent_MENT(x, y, w):

	heatmap, xedges, yedges = get_colormesh_MENT(x, y, w)
	fig_name = "SR_deltasent_MENT_v7_log_colormesh.png"
	plot_colormesh_MENT(heatmap,  xedges, yedges, fig_name)


def colormesh_SR_deltasent_MENT_SIMPLE(x, y, w):

	heatmap, xedges, yedges = get_colormesh_MENT(x, y, w)
	fig_name = "SR_deltasent_MENT_SIMPLE_colormesh.png"

	plt.clf()
	fig = plt.figure()
	X, Y = np.meshgrid(xedges, yedges)
	ax = fig.add_subplot(111)
	ax.pcolormesh(X, Y, np.log(heatmap + 1))

	#xmajor_ticks = np.arange(-1, 1, 0.5)
	#xlabels = ['1','0.5','0','0.5','1']                                    
	#plt.xticks(xmajor_ticks, xlabels) 

	#plt.xlim(-0.2,0.2)

	ymajor_ticks = np.arange(-1.5, 1.5, 0.5)
	#ymajor_ticks = np.arange(-1, 1, 0.5)
	#plt.ylim(-1,1)
	ylabels = ['1.5','1','0.5','0','0.5','1','1.5']
	#ylabels = ['1','0.5','0','0.5','1']   
	#plt.yticks(ymajor_ticks, ylabels)
	plt.xlabel('link SR')
	plt.ylabel('link absolute delta sentiment')

	plt.savefig("sentiment/" +  'S7S3_' + fig_name)

def main_FULL_SR():
	
	x, y = read_in_res()
	#plot_SR_deltaSENT(x, y)
	scatterplot_SR_deltasent(x, y)

def main_MENT():
	
	x, y, w = read_in_res_MENT_v2()
	#plot_SR_deltaSENT_MENT(x, y, w)
	scatterplot_SR_deltasent_MENT(x, y, w)
	#colormesh_SR_deltasent_MENT(x, y, w)

def main_MENT_SIMPLE():
	
	x, y, w = read_in_res_MENT_SIMPLE()
	colormesh_SR_deltasent_MENT_SIMPLE(x, y, w)	

os.chdir(IN_DIR)
main_MENT()
main_FULL_SR()