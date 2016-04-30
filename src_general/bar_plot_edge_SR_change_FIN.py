#!/usr/bin/env python
# a bar plot with errorbars
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

font = {'family' : 'monospace',
		'variant' : 'normal',
        'weight' : 'light',
        'size'   : 7}

matplotlib.rc('font', **font)

# plot with various axes scales
plt.figure(1)


def plot_bars_with_stdev_MO(SRmeans, SRStd):

	ind = np.arange(N)  # the x locations for the groups
	width = 0.3       # the width of the bars

	#ax = plt.subplot(223)
	ax = plt.subplot2grid((4,2),(0, 0), colspan=2)
	rects1 = ax.bar(ind, SRMeans, width, color='m', yerr=SRStd, label = 'Monthly Avg SR')


	# add some text for labels, title and axes ticks
	ax.set_ylabel('Avg SR')
	ax.set_title('Whole network')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(('June', 'July', 'August', 'Sept', 'Oct', 'Nov'))

	ax.set_ylim([-0.1, 0.35])

	plt.legend(loc=2)


	def autolabel(rects):
	    # attach some text labels
	    for rect in rects:
	        height = rect.get_height()
	        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
	                '%.3f' % float(height),
	                ha='center', va='bottom')

	autolabel(rects1)

	return plt

def plot_bars_with_stdev_2(DeletionMeans, DeletionStd):

	ind = np.arange(N)  # the x locations for the groups
	width = 0.3       # the width of the bars

	#ax = plt.subplot(322)
	ax = plt.subplot2grid((4,2),(1, 1))
	rects1 = ax.bar(ind, DeletionMeans, width, color='c', yerr=DeletionStd, label = 'Deletion')


	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg SR')
	ax.set_title('Edge deletion')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(('Before', 'At deletion month', 'After'))

	ax.set_ylim([-0.1, 0.35])

	plt.legend()

	def autolabel(rects):
	    # attach some text labels
	    for rect in rects:
	        height = rect.get_height()
	        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
	                '%.3f' % float(height),
	                ha='center', va='bottom')

	autolabel(rects1)

	return plt

def plot_bars_with_stdev_1(DeletionMeans, DeletionStd):

	ind = np.arange(N)  # the x locations for the groups
	width = 0.3       # the width of the bars

	#ax = plt.subplot(321)
	ax = plt.subplot2grid((4,2),(1, 0))
	rects1 = ax.bar(ind, DeletionMeans, width, color='darkred', yerr=DeletionStd, label = 'Formation')


	# add some text for labels, title and axes ticks
	ax.set_ylabel('Avg SR')
	ax.set_title('Edge formation')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(('Before', 'At formation month', 'After'))

	ax.set_ylim([-0.1, 0.35])

	plt.legend()


	def autolabel(rects):
	    # attach some text labels
	    for rect in rects:
	        height = rect.get_height()
	        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
	                '%.3f' % float(height),
	                ha='center', va='bottom')

	autolabel(rects1)

	return plt

def plot_bars_with_stdev_7(formationDeletionMeans, formationDeletionStd):

	ind = np.arange(N)  # the x locations for the groups
	width = 0.3       # the width of the bars

	ax = plt.subplot2grid((4,2),(2, 0), colspan=2)
	rects1 = ax.bar(ind, formationDeletionMeans, width, color='y', yerr=formationDeletionStd, label = 'Formation and deletion')


	ax.set_ylim([-0.1, 0.35])
	# add some text for labels, title and axes ticks
	ax.set_ylabel('Avg SR')
	ax.set_title('SR change on the edge')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(('Before', 'At formation', 'In the Mid', 'At deletion', 'After'))

	#ax.set_xlim([])

	plt.legend()


	def autolabel(rects):
	    # attach some text labels
	    for rect in rects:
	        height = rect.get_height()
	        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
	                '%.3f' % float(height),
	                ha='center', va='bottom')

	autolabel(rects1)

	return plt


# this is to have 3 in one, but as this
# 1) edge formation: those that are deleted and those that are not
# 2) edge deletion: those that are formed in our dataset and before
# 3) 6 months SR change
###################################################################################
# edge formation two version
# V3

N = 3

#formationNodeletionMeans = (0.012145, 0.110398, 0.106177)
#formationNodeletionStd = (0.053955, 0.192963, 0.171509)

#processed 13492 edges 
#Average SR 0.019252 and stdev 0.066896 before, at the time 0.097444, 0.176203 and after 0.070327, 0.138657 edges formation 

formationMeans = (0.019252, 0.097444 , 0.070327)
formationStd = (0.066896, 0.176203, 0.138657)

#plt3 = plot_bars_with_stdev_3(formationMeans, formationStd, formationNodeletionMeans, formationNodeletionStd)
#plt3.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/monthly_SR_change_list_of_users/edges_SR_change_v2.png", dpi=440)
plt1 = plot_bars_with_stdev_1(formationMeans, formationStd)

###################################################################################
# edge deletion two versions
# v4 # V22 final

N = 3

deletionNoformationMeans = (0.072700, 0.068026, 0.022971)
deletionNoformationStd = (0.123489, 0.140277, 0.074658)

#processed 10080 edges 
# Average SR 0.038934 and stdev 0.090531 before, at the time 0.083006, 0.157389 and after 0.038228, 0.101566 edges deletion 

deletionMeans = (0.038934, 0.083006, 0.038228)
deletionStd = (0.090531, 0.157389, 0.101566)

#plt4 = plot_bars_with_stdev_4(deletionMeans, deletionStd, deletionNoformationMeans, deletionNoformationStd)
# this final, no need for 2 types of deletion
plt2 = plot_bars_with_stdev_2(deletionNoformationMeans, deletionNoformationStd)

###################################################################################
# MONTHLY
# 0.008100, 0.017923, 0.025976, 0.037767, 0.048156, 0.054721, 0.029074
# 0.053316, 0.077368, 0.094393, 0.111137, 0.126394, 0.136750, 0.107575

N = 5

SRMeans = (0.017923, 0.025976, 0.037767, 0.048156, 0.054721)
SRStd = (0.077368, 0.094393, 0.111137, 0.126394, 0.136750)

plt3 = plot_bars_with_stdev_MO(SRMeans, SRStd)
#plt6.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/monthly_SR_change_list_of_users/edges_monthly_SR_change.png", dpi=440)

#plt.show()

#plt.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/monthly_SR_change_list_of_users/ALL_SR_change.png", dpi=1000)


###################################################################################################
# SR of persisting edges

def plot_bars_with_stdev_MO_2(SRmeans, SRStd):

	ind = np.arange(N)  # the x locations for the groups
	width = 0.3       # the width of the bars

	#ax = plt.subplot(111)
	ax = plt.subplot2grid((4,2),(3, 0), colspan=2)
	rects1 = ax.bar(ind, SRmeans, width, color='r', yerr=SRStd, label = 'Monthly Avg SR')


	# add some text for labels, title and axes ticks
	ax.set_ylabel('Avg SR')
	ax.set_title('Persisting edges')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(('June', 'July', 'August', 'Sept', 'Oct', 'Nov'))

	ax.set_ylim([-0.1, 0.35])

	plt.legend(loc=2)


	def autolabel(rects):
	    # attach some text labels
	    for rect in rects:
	        height = rect.get_height()
	        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
	                '%.3f' % float(height),
	                ha='center', va='bottom')

	autolabel(rects1)

#processed 3076 edges 
#Average SR, stdev 0.077627, 0.158114, at the time 6 
#Average SR, stdev 0.073275, 0.160656, at the time 7 
#Average SR, stdev 0.069833, 0.151127, at the time 8 
#Average SR, stdev 0.064159, 0.149817, at the time 9 
#Average SR, stdev 0.073046, 0.155852, at the time 10 

###################################################################################
# edge formation deletion separate

N = 5

formationDeletionMeans = (0.023888, 0.088995, 0.087686, 0.086517, 0.009626)
formationDeletionStd = (0.073761, 0.163803, 0.156189, 0.160936, 0.039921)

plt7 = plot_bars_with_stdev_7(formationDeletionMeans, formationDeletionStd)
###################################################################################

N = 5

SRmeans = (0.077627, 0.073275, 0.069833, 0.064159, 0.073046)
SRStd = (0.158114, 0.160656, 0.151127, 0.149817, 0.155852)



plt4 = plot_bars_with_stdev_MO_2(SRmeans, SRStd)

#plt.show()

plt.tight_layout()
plt.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/monthly_SR_change_list_of_users/SR_edges_temporal.png", dpi=730)

