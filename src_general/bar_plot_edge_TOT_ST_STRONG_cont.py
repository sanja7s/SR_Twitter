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
        'size'   : 14}

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
	ax.set_xticklabels(('Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov'))

	ax.set_ylim([-1, 10])
	ax.set_yticks((0,5))

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

	ax.set_ylim([-1, 10])
	ax.set_yticks((0,5))

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
	

	ax.set_ylim([-1, 10])
	ax.set_yticks((0,5))

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



	ax.set_ylim([-1, 10])
	ax.set_yticks((0,5))
	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg Rel Soc St')
	ax.set_title('Status change on the interaction')
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

# TOT MUT ST
#formationMeans = (1.37082238077, 4.7303792715, 4.65264739016)
#formationStd = (1.82950665268, 2.75023723532, 3.33011040538)

# TOT POP ST
#formationMeans = (14.072850169, 24.1012016523, 23.9553135561)
#formationStd = (17.7286454459, 27.9054800901, 23.7392716035)


# TOT WEAK ST DIFF
#formationMeans = (6.9913631243, 12.496620353, 12.0570784829)
#formationStd = (6.69449758508, 8.88552641326, 9.38191875769)

formationNodeletionMeans = (1.37082238077, 4.7303792715, 4.65264739016)
formationNodeletionStd = (1.82950665268, 2.75023723532, 3.33011040538)

# for all
#plt1 = plot_bars_with_stdev_1(formationMeans, formationStd)
# for persisting
plt1 = plot_bars_with_stdev_1(formationNodeletionMeans, formationNodeletionStd)
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

# TOT MUT ST
#deletionNoformationMeans = (2.21166332192, 4.92409396765, 2.75209538425)
#deletionNoformationStd = (2.15302571598, 2.69081589719, 2.67570822571)

# TOT POP ST
#deletionNoformationMeans = (13.8643607602, 18.3369141778, 12.3431708181)
#deletionNoformationStd = (38.7856471586, 26.0985990524, 17.3296229263)

# TOT STRONG ST
deletionNoformationMeans = (2.21166332192, 4.92409396765, 2.75209538425)
deletionNoformationStd = (2.15302571598, 2.69081589719, 2.67570822571)


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

# TOT MUT ST
#SRMeans = (4.060416, 4.259099, 4.589963, 5.006377, 5.673211)
#SRStd = (1.920565, 2.110132, 2.381383, 2.874757, 3.557735)

# TOT POP ST
#SRMeans = (19.724441, 23.096860, 38.203174, 29.150279, 28.663356)
#SRStd = (38.914648, 57.435557, 135.730294, 67.370534, 38.075933)

SRMeans = (4.060416, 4.259099,  4.259099, 5.006377, 5.673211)
SRStd = (1.920565, 2.110132, 2.381383, 2.874757, 3.557735)

"""
[ 3  5  4 ...,  2  6 10]
Average REL ST MUTUAL CONTACTS, stdev 7.730565, 9.826779, at the time 5 
[ 3 12  9 ...,  4  2  4]
Average REL ST MUTUAL CONTACTS, stdev 11.628465, 20.909712, at the time 6 
[13  8 12 ..., 11 14  6]
Average REL ST MUTUAL CONTACTS, stdev 13.905983, 31.739882, at the time 7 
[10 18 22 ...,  5 32  9]
Average REL ST MUTUAL CONTACTS, stdev 21.058478, 67.469715, at the time 8 
[ 4 25  6 ...,  6 21 14]
Average REL ST MUTUAL CONTACTS, stdev 17.592901, 38.432495, at the time 9 
[ 9 20 10 ..., 11  8 12]
Average REL ST MUTUAL CONTACTS, stdev 16.619965, 20.981538, at the time 10 
"""

# TOT MUT ST
"""
Average REL ST MUTUAL CONTACTS, stdev 3.390316, 1.531720, at the time 5 
[3 3 4 ..., 4 4 4]
Average REL ST MUTUAL CONTACTS, stdev 4.060416, 1.920565, at the time 6 
[5 5 4 ..., 4 4 4]
Average REL ST MUTUAL CONTACTS, stdev 4.259099, 2.110132, at the time 7 
[5 7 7 ..., 4 4 4]
Average REL ST MUTUAL CONTACTS, stdev 4.589963, 2.381383, at the time 8 
[10 16  8 ...,  4  4  4]
Average REL ST MUTUAL CONTACTS, stdev 5.006377, 2.874757, at the time 9 
[6 4 2 ..., 4 4 4]
Average REL ST MUTUAL CONTACTS, stdev 5.673211, 3.557735, at the time 10 
"""

# TOT POP ST
"""
[ 2.  3.  3. ...,  1.  9.  9.]
Average REL ST POP, stdev 11.116142, 17.391853, at the time 5 
[  4.   4.  19. ...,  18.  15.   4.]
Average REL ST POP, stdev 19.724441, 38.914648, at the time 6 
[ 14.  10.  34. ...,  15.  11.   6.]
Average REL ST POP, stdev 23.096860, 57.435557, at the time 7 
[  5.  32.  27. ...,   6.  77.  13.]
Average REL ST POP, stdev 38.203174, 135.730294, at the time 8 
[  2.  76.   8. ...,  11.  28.  31.]
Average REL ST POP, stdev 29.150279, 67.370534, at the time 9 
[ 18.  20.   9. ...,   9.   6.  14.]
Average REL ST POP, stdev 28.663356, 38.075933, at the time 10 
"""


# MO
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
	ax.set_xticklabels(('Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov'))

	#ax.set_ylim([-0.1, 0.35])
	#ax.set_yticks((-0.1,0.1,0.3))

	ax.set_ylim([-1, 10])
	ax.set_yticks((0,5))

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

# TOT MUT ST
#formationDeletionMeans = (1.80394317904, 5.00428606417, 4.40114068441, 5.06331129072, 2.8840313495)
#formationDeletionStd = (1.9755148583, 2.72691364807, 2.52679906754, 2.74966361941, 2.7298384276)

# TOT POP ST
#formationDeletionMeans = (13.0487386725, 19.3046779329, 17.5118821293, 19.1933627235, 12.9170952731)
#formationDeletionStd = (39.2967830019, 27.0693948638, 17.5651381818, 27.0166349646, 17.7301902562)



formationDeletionMeans = (1.80394317904, 5.00428606417, 4.40114068441, 5.06331129072, 2.8840313495)
formationDeletionStd = (1.9755148583, 2.72691364807, 2.52679906754, 2.74966361941, 2.7298384276)



plt7 = plot_bars_with_stdev_7(formationDeletionMeans, formationDeletionStd)
###################################################################################

N = 5

#SRmeans = (0.077627, 0.073275, 0.069833, 0.064159, 0.073046)
#SRStd = (0.158114, 0.160656, 0.151127, 0.149817, 0.155852)

#SRMeans = (5.904096, 5.662549, 6.104681, 5.969116,  6.033810)
#SRStd = (8.490351, 7.771688, 9.604471, 9.214502, 8.443850)

# TOT MUT ST
#SRMeans = (3.309168, 2.979519, 3.132315, 3.079974, 3.662224)
#SRStd = (1.973572, 2.118384, 2.240364, 2.206676, 2.354066)

# TOT POP ST
#SRMeans = (17.246749, 16.111183, 16.693758, 15.847529, 16.784135)
#SRStd = (18.663537, 19.904322, 19.386473, 18.003734, 18.131461)


SRMeans = (3.3091687, 2.979519, 3.132315, 3.079974, 3.662224)
SRStd = (1.973572, 2.118384, 2.240364, 2.206676, 2.354066)



# TOT WEAK ST DIF
"""
Average REL ST MUTUAL CONTACTS, stdev nan, nan, at the time 5 
[20  6  5 ..., 10  7  1]
Average REL ST MUTUAL CONTACTS, stdev 8.189207, 5.162568, at the time 6 
[12  8  4 ...,  6  6  0]
Average REL ST MUTUAL CONTACTS, stdev 7.573472, 5.184013, at the time 7 
[17  8  1 ...,  0  7  6]
Average REL ST MUTUAL CONTACTS, stdev 7.807217, 5.780744, at the time 8 
[12  9  3 ...,  4  7 10]
Average REL ST MUTUAL CONTACTS, stdev 7.639467, 5.538762, at the time 9 
[17  7  5 ...,  4  6  7]
Average REL ST MUTUAL CONTACTS, stdev 8.476268, 5.839845, at the time 10 
"""

# TOT MUT ST
"""
Average REL ST MUTUAL CONTACTS, stdev nan, nan, at the time 5 
[6 2 2 ..., 6 3 0]
Average REL ST MUTUAL CONTACTS, stdev 3.309168, 1.973572, at the time 6 
[1 4 2 ..., 3 3 0]
Average REL ST MUTUAL CONTACTS, stdev 2.979519, 2.118384, at the time 7 
[7 4 0 ..., 0 3 2]
Average REL ST MUTUAL CONTACTS, stdev 3.132315, 2.240364, at the time 8 
[5 4 0 ..., 2 3 4]
Average REL ST MUTUAL CONTACTS, stdev 3.079974, 2.206676, at the time 9 
[7 3 1 ..., 2 3 3]
Average REL ST MUTUAL CONTACTS, stdev 3.662224, 2.354066, at the time 10 
"""

# TOT POP ST
"""
Average REL ST, stdev nan, nan, at the time 5 
[ 20.  34.   4. ...,  27.   9.   0.]
Average REL ST, stdev 17.246749, 18.663537, at the time 6 
[  5.  18.   2. ...,   9.  23.   0.]
Average REL ST, stdev 16.111183, 19.904322, at the time 7 
[ 25.  74.   0. ...,   0.  37.  12.]
Average REL ST, stdev 16.693758, 19.386473, at the time 8 
[ 19.  76.   1. ...,   9.  22.  15.]
Average REL ST, stdev 15.847529, 18.003734, at the time 9 
[ 62.  38.   6. ...,   3.  22.  13.]
Average REL ST, stdev 16.784135, 18.131461, at the time 10 
"""



# PERSISTING
plt4 = plot_bars_with_stdev_MO_2(SRMeans, SRStd)

#plt.show()

#for ax7 in axes:
#    ax7.set_ylabel('Common y-label')

plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(8.3,6.5)

fig.suptitle('Sum of pair\'s strong contacts', verticalalignment='center', horizontalalignment='center', size = 16)
plt.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/ST_TOT_STRONG_cont.eps", dpi=710)

