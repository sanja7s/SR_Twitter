#!/usr/bin/env python
# a bar plot with errorbars
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon

width = 0.37       # the width of the bars

font = {'family' : 'sans-serif',
		'variant' : 'normal',
        'weight' : 'light',
        'size'   : 16}

matplotlib.rc('font', **font)

# plot with various axes scales
plt.figure(1)

# tried to have a single y label but did not work
#fig,axes = plt.subplots(sharey=True)


def plot_bars_with_stdev_MO(SRmeans, SRStd):

	ind = np.arange(N)  # the x locations for the groups
	#width = 0.3       # the width of the bars

	#ax = plt.subplot(223)
	ax = plt.subplot2grid((4,2),(0, 0), colspan=2)
	rects1 = ax.bar(ind, SRMeans, width, color='m', hatch="//", yerr=SRStd, label = 'Monthly Avg Rel Soc St')


	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg Rel Soc St')
	ax.set_title('Whole network')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(('June', 'July', 'August', 'Sept', 'Oct', 'Nov'))

	ax.set_ylim([-1, 4])
	ax.set_yticks((0,4))

	#plt.legend(loc=2, frameon=False)


	def autolabel(rects):
	    # attach some text labels
	    for rect in rects:
	        height = rect.get_height()
	        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
	                '%.2f' % float(height),
	                ha='center', va='bottom')

	autolabel(rects1)

	return plt

def plot_bars_with_stdev_2(DeletionMeans, DeletionStd):

	ind = np.arange(N)  # the x locations for the groups
	#width = 0.3       # the width of the bars

	#ax = plt.subplot(322)
	ax = plt.subplot2grid((4,2),(1, 1))
	rects1 = ax.bar(ind, DeletionMeans, width, color='c', hatch='*', yerr=DeletionStd, label = 'Decomission')


	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg SR')
	ax.set_title('Interaction decomission')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(('Before', 'At decomission', 'After'))

	ax.set_ylim([-1, 4])
	ax.set_yticks((0,4))

	#plt.legend(frameon=False)

	def autolabel(rects):
	    # attach some text labels
	    for rect in rects:
	        height = rect.get_height()
	        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
	                '%.2f' % float(height),
	                ha='center', va='bottom')

	autolabel(rects1)

	return plt

def plot_bars_with_stdev_1(DeletionMeans, DeletionStd):

	ind = np.arange(N)  # the x locations for the groups
	#width = 0.3       # the width of the bars

	#ax = plt.subplot(321)
	ax = plt.subplot2grid((4,2),(1, 0))
	rects1 = ax.bar(ind, DeletionMeans, width, color='darkred',  hatch='x', yerr=DeletionStd, label = 'Activation')


	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg Rel Soc St')
	ax.set_title('Interaction activation')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(('Before', 'At activation', 'After'))

	ax.set_ylim([-1, 4])
	ax.set_yticks((0,4))

	#plt.legend(frameon=False)


	def autolabel(rects):
	    # attach some text labels
	    for rect in rects:
	        height = rect.get_height()
	        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
	                '%.2f' % float(height),
	                ha='center', va='bottom')

	autolabel(rects1)

	return plt

def plot_bars_with_stdev_7(formationDeletionMeans, formationDeletionStd):

	ind = np.arange(N)  # the x locations for the groups
	#width = 0.3       # the width of the bars

	ax = plt.subplot2grid((4,2),(2, 0), colspan=2)
	rects1 = ax.bar(ind, formationDeletionMeans, width, color='y',  hatch='+', yerr=formationDeletionStd, label = 'Activation and decomission')


	ax.set_ylim([-1, 4])
	ax.set_yticks((0,4))
	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg Rel Soc St')
	ax.set_title('Rel. soc. st. change on the interaction')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(('Before', 'At activation', 'In the Mid', 'At decomission', 'After'))


	#plt.legend(frameon=False)


	def autolabel(rects):
	    # attach some text labels
	    for rect in rects:
	        height = rect.get_height()
	        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
	                '%.2f' % float(height),
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

#formationMeans = (0.019252, 0.097444 , 0.070327)
#formationStd = (0.066896, 0.176203, 0.138657)

#formationMeans = (9.132078, 9.717981, 8.969463)
#formationStd = (9.132078, 21.033700, 14.425127)

#formationMeans = (2.97398458346, 3.35672991402, 3.22265045953)
#formationStd = (14.5673494118, 10.228554967, 6.70779046053)

#formationMeans = (2.17630491926, 2.70540743522, 2.71986481412)
#formationStd = (3.15964775795, 3.8723235949, 3.77149710905)

# strong contacts rel st
formationMeans = (0.964889222681, 1.44874202028, 1.68794592565)
formationStd = (1.30256068643, 1.64860382968, 1.94388833634)




#plt3 = plot_bars_with_stdev_3(formationMeans, formationStd, formationNodeletionMeans, formationNodeletionStd)
#plt3.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/monthly_SR_change_list_of_users/edges_SR_change_v2.png", dpi=440)
plt1 = plot_bars_with_stdev_1(formationMeans, formationStd)

###################################################################################
# edge deletion two versions
# v4 # V22 final

N = 3

#deletionNoformationMeans = (0.072700, 0.068026, 0.022971)
#deletionNoformationStd = (0.123489, 0.140277, 0.074658)

#processed 10080 edges 
# Average SR 0.038934 and stdev 0.090531 before, at the time 0.083006, 0.157389 and after 0.038228, 0.101566 edges deletion 

#deletionMeans = (0.038934, 0.083006, 0.038228)
#deletionStd = (0.090531, 0.157389, 0.101566)

#deletionNoformationMeans = (8.480853, 8.712103, 7.560913)
#deletionNoformationStd = (34.624987, 22.163709, 13.956631)

#deletionNoformationMeans = (3.26706349206, 3.44027777778, 3.19642857143)
#deletionNoformationStd = (16.7550012229, 11.5805325803, 7.35757000995)

#deletionNoformationMeans = (3.38496045331, 3.58269389682, 3.33042143785)
#deletionNoformationStd = (18.1964374136, 12.5044382296, 7.83958630876)

deletionNoformationMeans = (1.16101995042, 1.52591193484, 1.54066816196)
deletionNoformationStd = (1.36105887603, 1.69996084625, 1.80123581372)



#plt4 = plot_bars_with_stdev_4(deletionMeans, deletionStd, deletionNoformationMeans, deletionNoformationStd)
# this final, no need for 2 types of deletion
plt2 = plot_bars_with_stdev_2(deletionNoformationMeans, deletionNoformationStd)

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
#SRMeans = (5.463340, 7.537845, 15.656386, 9.706566, 7.034683)
#SRStd = (22.706669, 35.442416, 77.172580, 42.471410, 21.453634)

SRMeans = (0.756911, 0.907188, 1.049831, 1.263494, 1.581871)
SRStd = (1.075074, 1.254395, 1.398652, 1.711709, 2.107371)


plt3 = plot_bars_with_stdev_MO(SRMeans, SRStd)
#plt6.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/monthly_SR_change_list_of_users/edges_monthly_SR_change.png", dpi=440)

#plt.show()

#plt.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/monthly_SR_change_list_of_users/ALL_SR_change.png", dpi=1000)


###################################################################################################
# SR of persisting edges

def plot_bars_with_stdev_MO_2(SRmeans, SRStd):

	ind = np.arange(N)  # the x locations for the groups


	#ax = plt.subplot(111)
	ax = plt.subplot2grid((4,2),(3, 0), colspan=2)
	rects1 = ax.bar(ind, SRmeans, width, color='r',  hatch='O', yerr=SRStd, label = 'Monthly Avg Rel Soc St')


	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg Rel Soc St')
	ax.set_title('Persisting interactions')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(('June', 'July', 'August', 'Sept', 'Oct', 'Nov'))

	#ax.set_ylim([-0.1, 0.35])
	#ax.set_yticks((-0.1,0.1,0.3))
	ax.set_ylim([-1, 4])
	ax.set_yticks((0,4))

	#plt.legend(loc=2,frameon=False)


	def autolabel(rects):
	    # attach some text labels
	    for rect in rects:
	        height = rect.get_height()
	        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
	                '%.2f' % float(height),
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

#formationDeletionMeans = (8.83810923341, 9.3989713446, 7.68298479087, 9.34668136174, 8.12821454813)
#formationDeletionStd = (38.1328644866, 24.1286964744, 12.6131673996, 24.2443565601, 14.8904513016)

#formationDeletionMeans = (3.49424442812, 3.78153318638, 2.6069391635, 3.79402400196, 3.50967425912)
#formationDeletionStd = (18.5314872918, 12.7523859509, 4.09603923313, 12.7706724373, 8.01655108646)

formationDeletionMeans  = (1.12747979427, 1.56808719079, 1.38498098859, 1.58645603723, 1.613397012)
formationDeletionStd  = (1.35650452374, 1.71205560699, 1.49017144356, 1.73298601092, 1.84822380219)


plt7 = plot_bars_with_stdev_7(formationDeletionMeans, formationDeletionStd)
###################################################################################

N = 5

#SRmeans = (0.077627, 0.073275, 0.069833, 0.064159, 0.073046)
#SRStd = (0.158114, 0.160656, 0.151127, 0.149817, 0.155852)

#SRMeans = (5.904096, 5.662549, 6.104681, 5.969116,  6.033810)
#SRStd = (8.490351, 7.771688, 9.604471, 9.214502, 8.443850)

#SRMeans = (1.461964, 1.414499, 1.501951, 1.520481, 1.500000)
#SRStd = (1.943158, 1.843390, 2.125224, 2.086998, 2.146382)

SRMeans = (0.856632, 0.906697, 0.995124, 1.010403, 1.031534)
SRStd = (1.114944, 1.194131, 1.283704, 1.245234, 1.317081)



plt4 = plot_bars_with_stdev_MO_2(SRMeans, SRStd)

#plt.show()

#for ax7 in axes:
#    ax7.set_ylabel('Common y-label')

plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(8.3,6.5)

plt.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/ST_DIFF_STRONG_CONTACTS_DIFF7s.eps", dpi=710)

