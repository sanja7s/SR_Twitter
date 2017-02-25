#!/usr/bin/env python
# a bar plot with errorbars
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon

width = 0.97       # the width of the bars

font = {'family' : 'sans-serif',
		'variant' : 'normal',
        'weight' : 'light',
        'size'   : 13}

matplotlib.rc('font', **font)

# plot with various axes scales
plt.figure(1)

# tried to have a single y label but did not work
#fig,axes = plt.subplots(sharey=True)


def plot_bars_with_stdev_MO(SRmeans, SRStd):

	ind = np.arange(N)  # the x locations for the groups
	#width = 0.3       # the width of the bars

	#ax = plt.subplot(223)
	ax = plt.subplot2grid((3,2),(0, 0), colspan=2)
	#rects1 = ax.bar(ind, SRMeans, width, color='m', hatch="//", yerr=SRStd, label = 'Monthly Avg SR')

	rects1 = ax.bar(ind, SRMeans, width, color='m', \
		align='center', yerr=SRStd, linewidth=0, \
		error_kw=dict(ecolor='gray', lw=1.5, capsize=2.7, capthick=1))

	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg SR')
	ax.set_title('Whole network')
	ax.set_xticks(ind)
	ax.set_xticklabels(('Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'))

	ax.set_ylim([-0.1, 0.35])
	ax.set_yticks((-0.1,0.1,0.3))

	#plt.legend(loc=2, frameon=False)


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
	#width = 0.3       # the width of the bars

	#ax = plt.subplot(322)
	ax = plt.subplot2grid((3,2),(1, 1))
	#rects1 = ax.bar(ind, DeletionMeans, width, color='c', hatch='*', yerr=DeletionStd, label = 'decommission')
	rects1 = ax.bar(ind, DeletionMeans, width, color='c', \
		align='center', yerr=DeletionStd, linewidth=0, \
		error_kw=dict(ecolor='gray', lw=1.5, capsize=2.7, capthick=1))

	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg SR')
	ax.set_title('Interaction decommission')
	ax.set_xticks(ind )
	ax.set_xticklabels(('Before', 'At decommission', 'After'))

	ax.set_ylim([-0.1, 0.35])
	ax.set_yticks((-0.1,0.1,0.3))

	#plt.legend(frameon=False)

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
	#width = 0.3       # the width of the bars

	#ax = plt.subplot(321)
	ax = plt.subplot2grid((3,2),(1, 0))
	#rects1 = ax.bar(ind, DeletionMeans, width, color='darkred',  hatch='x', yerr=DeletionStd, label = 'Activation')
	rects1 = ax.bar(ind, DeletionMeans, width, color='darkred', \
		align='center', yerr=DeletionStd, linewidth=0, \
		error_kw=dict(ecolor='gray', lw=1.5, capsize=2.7, capthick=1))

	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg SR')
	ax.set_title('Interaction activation')
	ax.set_xticks(ind )
	ax.set_xticklabels(('Before', 'At activation', 'After'))

	ax.set_ylim([-0.1, 0.35])
	ax.set_yticks((-0.1,0.1,0.3))

	#plt.legend(frameon=False)


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
	#width = 0.3       # the width of the bars

	ax = plt.subplot2grid((4,2),(2, 0), colspan=2)
	#rects1 = ax.bar(ind, formationDeletionMeans, width, color='y',  hatch='+', yerr=formationDeletionStd, label = 'Activation and decommission')
	rects1 = ax.bar(ind, formationDeletionMeans, width, color='y', \
		align='center', yerr=formationDeletionStd, linewidth=0, \
		error_kw=dict(ecolor='gray', lw=1.5, capsize=2.7, capthick=1))

	ax.set_ylim([-0.1, 0.35])
	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg SR')
	ax.set_title('Non-persisting interactions')
	ax.set_xticks(ind)
	ax.set_xticklabels(('Before', 'At activation', 'At Mid', 'At decommission', 'After'))

	#ax.set_xlim([])
	ax.set_yticks((-0.1,0.1,0.3))

	#plt.legend(frameon=False)


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
# PERSISTING LINKS
#formationNodeletionMeans = (0.0121447496769, 0.110398018511, 0.10617694085)
#formationNodeletionStd = (0.0539546551446, 0.192962632767, 0.1715092024)




#processed 13492 edges 
#Average SR 0.019252 and stdev 0.066896 before, at the time 0.097444, 0.176203 and after 0.070327, 0.138657 edges formation 

formationMeans = (0.0192521818311, 0.0974437259893, 0.07032720813)
formationStd = (0.0668960682412, 0.176202988944, 0.138657262854)


#plt3 = plot_bars_with_stdev_3(formationMeans, formationStd, formationNodeletionMeans, formationNodeletionStd)
#plt3.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/monthly_SR_change_list_of_users/edges_SR_change_v2.png", dpi=440)
plt1 = plot_bars_with_stdev_1(formationMeans, formationStd)

###################################################################################
# edge deletion two versions
# v4 # V22 final

N = 3

# PERSISTING LINKS
deletionNoformationMeans = (0.0727004565385, 0.0680258988703, 0.0229713363971)
deletionNoformationStd = (0.123489476215, 0.140276874039, 0.0746578827396)
deletionNoformationMeans = (0.0727004565385, 0.0680258988703, 0.0229713363971)
deletionNoformationStd = (0.123489476215, 0.140276874039, 0.0746578827396)

#processed 10080 edges 
# Average SR 0.038934 and stdev 0.090531 before, at the time 0.083006, 0.157389 and after 0.038228, 0.101566 edges deletion 

deletionMeans = (0.038933802188, 0.0830056870558, 0.0382280669398)
deletionStd = (0.0905313753995, 0.157388968035, 0.101565579395)

#plt4 = plot_bars_with_stdev_4(deletionMeans, deletionStd, deletionNoformationMeans, deletionNoformationStd)
# this final, no need for 2 types of deletion
plt2 = plot_bars_with_stdev_2(deletionMeans, deletionStd)

###################################################################################
# MONTHLY
# 0.008100, 0.017923, 0.025976, 0.037767, 0.048156, 0.054721, 0.029074
# 0.053316, 0.077368, 0.094393, 0.111137, 0.126394, 0.136750, 0.107575

N = 5

#SRMeans = (0.017923, 0.025976, 0.037767, 0.048156, 0.054721)
#SRStd = (0.077368, 0.094393, 0.111137, 0.126394, 0.136750)
# improved to discount for edges not present at the MO
#SRMeans = (0.050, 0.053, 0.058, 0.061, 0.065)
#SRStd = (0.123, 0.130, 0.134, 0.14, 0.147)

# but i should not discount for edges not present
# but as always with formation and deletion etc
# consider the same set of edges as below
"""
Monthly edges  69960
6 mention network SR: $\mu=0.018$, $\sigma= 0.077$
Monthly edges  69960
7 mention network SR: $\mu=0.026$, $\sigma= 0.094$
Monthly edges  69960
8 mention network SR: $\mu=0.038$, $\sigma= 0.111$
Monthly edges  69960
9 mention network SR: $\mu=0.048$, $\sigma= 0.126$
Monthly edges  69960
10 mention network SR: $\mu=0.055$, $\sigma= 0.137$
"""
SRMeans = (0.018, 0.026, 0.038, 0.048, 0.055)
SRStd = (0.077, 0.094, 0.111, 0.126, 0.137)

plt3 = plot_bars_with_stdev_MO(SRMeans, SRStd)
#plt6.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/monthly_SR_change_list_of_users/edges_monthly_SR_change.png", dpi=440)

#plt.show()

#plt.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/monthly_SR_change_list_of_users/ALL_SR_change.png", dpi=1000)


###################################################################################################
# SR of persisting edges

def plot_bars_with_stdev_MO_2(SRmeans, SRStd):

	ind = np.arange(N)  # the x locations for the groups


	#ax = plt.subplot(111)
	ax = plt.subplot2grid((3,2),(2, 0), colspan=2)
	#rects1 = ax.bar(ind, SRmeans, width, color='r',  hatch='O', yerr=SRStd, label = 'Monthly Avg SR')
	rects1 = ax.bar(ind, SRmeans, width, color='r', \
		align='center', yerr=SRStd, linewidth=0, \
		error_kw=dict(ecolor='gray', lw=1.5, capsize=2.7, capthick=1))


	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg SR')
	ax.set_title('Persisting interactions')
	ax.set_xticks(ind)
	ax.set_xticklabels(('Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'))

	ax.set_ylim([-0.1, 0.35])
	ax.set_yticks((-0.1,0.1,0.3))

	#plt.legend(loc=2,frameon=False)


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

#formationDeletionMeans = (0.023888, 0.088995, 0.087686, 0.086517, 0.009626)
#formationDeletionStd = (0.073761, 0.163803, 0.156189, 0.160936, 0.039921)

#plt7 = plot_bars_with_stdev_7(formationDeletionMeans, formationDeletionStd)
###################################################################################

N = 5

SRmeans = (0.077627, 0.073275, 0.069833, 0.064159, 0.073046)
SRStd = (0.158114, 0.160656, 0.151127, 0.149817, 0.155852)



plt4 = plot_bars_with_stdev_MO_2(SRmeans, SRStd)

#plt.show()

#for ax7 in axes:
#    ax7.set_ylabel('Common y-label')

plt.tight_layout()
fig = plt.gcf()
plt.tight_layout()
fig.set_size_inches(8.3,6.5)
plt.tight_layout()
plt.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/monthly_SR_change_list_of_users/temporal_SR_persisting_formations_deletions7s7s.eps", dpi=710)

