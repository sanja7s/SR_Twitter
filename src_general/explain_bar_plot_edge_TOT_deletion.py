#!/usr/bin/env python
# a bar plot with errorbars
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
from pylab import *


width = 0.37       # the width of the bars

font = {'family' : 'sans-serif',
		'variant' : 'normal',
        'weight' : 'light',
        'size'   : 14}

matplotlib.rc('font', **font)

# plot with various axes scales
plt.figure(1)
fig = gcf()
# tried to have a single y label but did not work
#fig,axes = plt.subplots(sharey=True)


def plot_bars_del_WEAK(DeletionMeans, DeletionStd):

	ind = np.arange(N)  # the x locations for the groups
	#width = 0.3       # the width of the bars

	#ax = plt.subplot(322)
	ax = plt.subplot2grid((2,2),(1, 0))
	rects1 = ax.bar(ind, DeletionMeans, width, color='c', hatch='*', yerr=DeletionStd, label = 'Decomission')


	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg SR')
	
	#ax.set_title('Sum including weak contacts')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(('Before', 'At decomission', 'After'))

	ax.set_ylim([-5, 30])
	ax.set_yticks((0,10,20))

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

def plot_bars_del_STRONG(DeletionMeans, DeletionStd):

	ind = np.arange(N)  # the x locations for the groups
	#width = 0.3       # the width of the bars

	#ax = plt.subplot(322)
	ax = plt.subplot2grid((2,2),(0, 0))
	rects1 = ax.bar(ind, DeletionMeans, width, color='c', hatch='*', yerr=DeletionStd, label = 'Decomission')

	#fig.suptitle('Sum including weak contacts', size = 16)
	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg SR')
	#ax.set_title('Sum of only strong contacts')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(('Before', 'At decomission', 'After'))

	ax.set_ylim([-3, 10])
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



# TOT POP ST
#deletionNoformationMeans = (13.8643607602, 18.3369141778, 12.3431708181)
#deletionNoformationStd = (38.7856471586, 26.0985990524, 17.3296229263)

# TOT STRONG ST
deletionNoformationMeans = (2.21166332192, 4.92409396765, 2.75209538425)
deletionNoformationStd = (2.15302571598, 2.69081589719, 2.67570822571)



deletionMeans = (2.53283730159, 4.89365079365, 2.69990079365)
deletionStd = (2.32599037733, 2.66040920685, 2.63807589629)

plt1 = plot_bars_del_STRONG(deletionNoformationMeans, deletionNoformationStd)

# TOT WEAK ST DIFF
deletionNoformationMeans = (9.40538307166, 14.2992562862, 9.75056073663)
deletionNoformationStd = (19.3285344981, 15.124776683, 10.9994791456)

deletionMeans = (9.79871031746, 14.0166666667, 9.46180555556)
deletionStd = (18.0181967745, 14.2450813009, 10.5294056078)


#plt4 = plot_bars_with_stdev_4(deletionMeans, deletionStd, deletionNoformationMeans, deletionNoformationStd)
# this final, no need for 2 types of deletion
plt2 = plot_bars_del_WEAK(deletionNoformationMeans, deletionNoformationStd)

###################################################################################################
# SR of persisting edges
def plot_bars_persisting_STRONG(SRmeans, SRStd):

	ind = np.arange(N)  # the x locations for the groups

	width = 0.01
	#ax = plt.subplot(111)
	ax = plt.subplot2grid((2,2),(0, 1), colspan=2)
	rects1 = ax.bar(ind, SRmeans, width, color='r',  hatch='O', yerr=SRStd)


	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg Rel Soc St')
	#ax.set_title('Persisting avg')

	ax.set_xticks(ind+0.1)
	ax.set_xticklabels(('Persisting avg'))

	#ax.set_ylim([-0.1, 0.35])
	#ax.set_yticks((-0.1,0.1,0.3))
	ax.set_ylim([-3, 10])
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

###################################################################################################
# SR of persisting edges
def plot_bars_persisting_WEAK(SRmeans, SRStd):

	ind = np.arange(N)  # the x locations for the groups

	width =0.01
	#ax = plt.subplot(111)
	ax = plt.subplot2grid((2,2),(1, 1), colspan=2)
	rects1 = ax.bar(ind, SRmeans, width, color='r',  hatch='O', yerr=SRStd)


	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg Rel Soc St')
	#ax.set_title('Persisting avg')
	ax.set_xticks(ind)
	#ax.set_xticklabels(('Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov'))

	#ax.set_ylim([-0.1, 0.35])
	#ax.set_yticks((-0.1,0.1,0.3))
	ax.set_ylim([-5, 30])
	ax.set_yticks((0,10,20))

	#plt.legend(loc=2,frameon=False)

	def autolabel(rects):
	    # attach some text labels
	    for rect in rects:
	        height = rect.get_height()
	        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
	                '%.2f' % float(height),
	                ha='center', va='bottom')

	autolabel(rects1)

N = 1

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

# TOT WEAK ST DIFF
weakMeans = np.array([8.189207, 7.573472, 7.807217, 7.639467, 8.476268])
weakStd = np.array([5.162568, 5.184013, 5.780744, 5.538762, 5.839845])

wM = np.mean(weakMeans)
wS = np.mean(weakStd)

plt3 = plot_bars_persisting_WEAK(wM, wS)

# TOT MUT ST
strongMeans = (3.309168, 2.979519, 3.132315, 3.079974, 3.662224)
strongStd = (1.973572, 2.118384, 2.240364, 2.206676, 2.354066)



sM = np.mean(strongMeans)
sS = np.mean(strongStd)

plt4 = plot_bars_persisting_STRONG(sM, sS)

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
plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(8.3,6.5)

plt.figtext(0.30, 0.5, 'Sum of all pair\'s contacts, including weak')
plt.figtext(0.37, 0.973, 'Sum of pair\'s strong contacts')

plt.figtext(0.65, 0.53, 'Persisting interactions')
plt.figtext(0.65, 0.05, 'Persisting interactions')
#fig.suptitle('Sum of strong contacts', verticalalignment='center', horizontalalignment='center', size = 16)
#fig.suptitle('Sum including weak contacts', verticalalignment='center', y=0.5, horizontalalignment='center', size = 16)

plt.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/DEL_ST_TOT_explain.eps", dpi=710)

