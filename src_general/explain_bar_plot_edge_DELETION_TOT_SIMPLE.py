#!/usr/bin/env python
# a bar plot with errorbars
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
from pylab import *

width=0.28     # the width of the bars

font = {'family' : 'sans-serif',
		'variant' : 'normal',
        'weight' : 'light',
        'size'   : 14}

matplotlib.rc('font', **font)
# plot with various axes scales
plt.figure(1)
fig = gcf()


def plot_bars_DELETION_STRONG_TOT(PersistingMeans, PersistingStd, Means, Std, PERSreal, PERSstd):

	ind = np.arange(N)  # the x locations for the groups
	#width = 0.3       # the width of the bars

	#ax = plt.subplot(321)
	ax = plt.subplot2grid((1,2),(0, 0))
	#rects1 = ax.bar(ind-0.2, PersistingMeans, width, color='c', yerr=PersistingStd, align='center')
	#rects2 = ax.bar(ind+0.2, Means, width, color='cyan', yerr=Std, align='center')

	rects1 = ax.bar(ind-width, PersistingMeans, width, color='c', \
		align='center', yerr=PersistingStd, linewidth=0,\
		error_kw=dict(ecolor='gray', lw=1.5, capsize=2.7, capthick=1))

	rects2 = ax.bar(ind, Means, width, color='cyan', \
		yerr=Std, align='center', linewidth=0,\
		error_kw=dict(ecolor='gray', lw=1.5, capsize=2.7, capthick=1))

	rects3 = ax.bar(ind+width, PERSreal, width, color='r',\
		yerr=PERSstd, align='center',linewidth=0,\
		error_kw=dict(ecolor='gray', lw=1.5, capsize=2.7, capthick=1))


	ax.legend((rects1[0], rects2[0], rects3[0]), \
		('Persisting decommissioned', \
			'Non-persisting decommissioned', 'Persisting average'),\
		loc='best',frameon=False)

	# add some text for labels, title and axes ticks
	ax.set_title('Sum of pair\'s strong contacts')
	ax.set_xticks(ind )
	ax.set_xticklabels(('Before', 'At decommission', 'After'))
	
	ax.set_ylim([-1, 15])
	ax.set_yticks((0,5,10,15))


	def autolabel(rects):
	    # attach some text labels
	    for rect in rects:
	        height = rect.get_height()
	        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
	                '%.2f' % float(height),
	                ha='center', va='bottom')

	autolabel(rects1)
	autolabel(rects2)
	autolabel(rects3)

	return plt

###################################################################################################
def plot_bars_DELETION_WEAK_TOT(PersistingMeans, PersistingStd, Means, Std, PERSreal, PERSstd):

	ind = np.arange(N)  # the x locations for the groups
	#width = 0.3       # the width of the bars

	#ax = plt.subplot(321)
	ax = plt.subplot2grid((1,2),(0, 1))

	#axs[1].bar(x, a, width=1/3, facecolor='b', alpha=.5, linewidth=0)
	#axs[1].bar(x+1/3, b, width=1/3, facecolor='r', alpha=.5, linewidth=0)
	#axs[1].bar(x+2/3, c, width=1/3, facecolor='g', alpha=.5, linewidth=0)

	rects1 = ax.bar(ind-width, PersistingMeans, width, color='c', \
		align='center', yerr=PersistingStd, linewidth=0, \
		error_kw=dict(ecolor='gray', lw=1.5, capsize=2.7, capthick=1))

	rects2 = ax.bar(ind, Means, width, color='cyan', \
		yerr=Std, align='center', linewidth=0, \
		error_kw=dict(ecolor='gray', lw=1.5, capsize=2.7, capthick=1))

	rects3 = ax.bar(ind+width, PERSreal, width, color='r',\
		yerr=PERSstd, align='center',linewidth=0, \
		error_kw=dict(ecolor='gray', lw=1.5, capsize=2.7, capthick=1))

	# add some text for labels, title and axes ticks
	ax.set_title('Sum of all pair\'s contacts, including weak')
	ax.set_xticks(ind)
	ax.set_xticklabels(('Before', 'At decommission', 'After'))
	
	ax.set_ylim([-2, 40])
	ax.set_yticks((0,20,40))

	ax.legend((rects1[0], rects2[0], rects3[0]), \
		('Persisting decommissioned', \
			'Non-persisting decommissioned', 'Persisting average'),\
		loc='best',frameon=False)

	def autolabel(rects):
	    # attach some text labels
	    for rect in rects:
	        height = rect.get_height()
	        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
	                '%.2f' % float(height),
	                ha='center', va='bottom')

	autolabel(rects1)
	autolabel(rects2)
	autolabel(rects3)

	return plt



N = 3
##########################################################################
# NON PERSISTING LINKS
# STRONG contacts REL TODO
deletionFormationMeans = (2.3721528288, 5.06331129072, 2.8840313495)
deletionFormationStd = (2.30971994302, 2.74966361941, 2.7298384276)


# PERSISTING LINKS
deletionNoformationMeans = (3.2183908046, 4.1698014629, 1.91431556949)
deletionNoformationStd = (2.26977696782, 2.09065874393, 2.02388400217)


SRMeans = (3.3091687, 2.979519, 3.132315, 3.079974, 3.662224)
SRStd = (1.973572, 2.118384, 2.240364, 2.206676, 2.354066)
SRMeansS = (3.2326401399999996,3.2326401399999996,3.2326401399999996)
SRStdS = (2.1786123999999996,2.1786123999999996,2.1786123999999996)

plt1 = plot_bars_DELETION_STRONG_TOT(deletionNoformationMeans, deletionNoformationStd,\
	deletionFormationMeans, deletionFormationStd, SRMeansS, SRStdS)

##########################################################################
# NON PERSISTING LINKS
# WEAK contacts REL
#deletionFormationMeans = (11.8694841516, 12.5288999378, 7.94157862026)
#deletionFormationStd = (7.86842513803, 8.01656559249, 7.40527537721)

deletionFormationMeans = (10.0062454078, 14.8485182464, 10.164707323)
deletionFormationStd = (19.8008783499, 15.427485234, 11.1890193881)


# PERSISTING LINKS
# WEAK contacts REL
#deletionNoformationMeans = (9.40538307166, 14.2992562862, 9.75056073663)
#deletionNoformationStd = (19.3285344981, 15.124776683, 10.9994791456)

deletionNoformationMeans = (8.91327063741, 10.4676071055, 6.46290491118)
deletionNoformationStd = (6.00381291795, 6.13887060538, 6.21665047084)

# REAL PERSISTING
SRMeans = (8.189207, 7.573472, 7.807217, 7.639467, 8.476268)
SRStd = (5.162568, 5.184013, 5.780744, 5.538762, 5.839845)
SRMeansW = (7.9371261999999998,7.9371261999999998,7.9371261999999998)
SRStdW = (5.5011863999999999,5.5011863999999999,5.5011863999999999)

plt2 = plot_bars_DELETION_WEAK_TOT(deletionNoformationMeans, deletionNoformationStd, \
	deletionFormationMeans, deletionFormationStd, SRMeansW, SRStdW)
##########################################################################

plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(12.4,4.5)
plt.tight_layout()
#plt.figtext(0.20, 0.49, 'Relative status of the pair: weak contacts')
#plt.figtext(0.27, 0.973, 'Relative status of the pair: strong contacts')
#fig.suptitle('Sum of strong contacts', verticalalignment='center', horizontalalignment='center', size = 16)
#fig.suptitle('Sum including weak contacts', verticalalignment='center', y=0.5, horizontalalignment='center', size = 16)

plt.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/simple_DELETION_explain_TOT_v2.eps", dpi=710)

