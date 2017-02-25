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

def plot_bars_FORMATION_SR(PersistingMeans, PersistingStd, Means, Std, PERSreal, PERSstd):

	ind = np.arange(N)  # the x locations for the groups
	#width = 0.3       # the width of the bars

	#ax = plt.subplot(321)
	ax = plt.subplot2grid((1,2),(0, 0))
	#rects1 = ax.bar(ind-0.2, PersistingMeans, width, color='c', yerr=PersistingStd, align='center')
	#rects2 = ax.bar(ind+0.2, Means, width, color='cyan', yerr=Std, align='center')

	rects1 = ax.bar(ind-width, PersistingMeans, width, color='darkred', \
		align='center', yerr=PersistingStd, linewidth=0,\
		error_kw=dict(ecolor='gray', lw=1.5, capsize=2.7, capthick=1))

	rects2 = ax.bar(ind, Means, width, color='lightcoral', \
		yerr=Std, align='center', linewidth=0,\
		error_kw=dict(ecolor='gray', lw=1.5, capsize=2.7, capthick=1))

	rects3 = ax.bar(ind+width, PERSreal, width, color='r',\
		yerr=PERSstd, align='center',linewidth=0,\
		error_kw=dict(ecolor='gray', lw=1.5, capsize=2.7, capthick=1))


	ax.legend((rects1[0], rects2[0], rects3[0]), \
		('Formed and persisting', \
			'Formed and non-persisting', 'Persisting average'),\
		frameon=False)

	ax.set_title('SR during formation')
	ax.set_xticks(ind )
	ax.set_xticklabels(('Before', 'At formation', 'After'))
	
	ax.set_ylim([-0.03, 0.35])
	ax.set_yticks((0,0.1,0.2,0.3))


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
def plot_bars_DELETION_SR(PersistingMeans, PersistingStd, Means, Std, PERSreal, PERSstd):

	ind = np.arange(N)  # the x locations for the groups
	#width = 0.3       # the width of the bars

	#ax = plt.subplot(321)
	ax = plt.subplot2grid((1,2),(0, 1))
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
		frameon=False)

	ax.set_title('SR during decommission')
	ax.set_xticks(ind )
	ax.set_xticklabels(('Before', 'At decommission', 'After'))
	
	ax.set_ylim([-0.03, 0.35])
	ax.set_yticks((0,0.1,0.2,0.3))


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
formationDeletionMeans = (0.0238877664077, 0.0889947225643, 0.0469454206615)
formationDeletionStd = (0.0737611090458, 0.163802741911, 0.105806861733)


# PERSISTING LINKS
formationNodeletionMeans = (0.0121447496769, 0.110398018511, 0.10617694085)
formationNodeletionStd = (0.0539546551446, 0.192962632767, 0.1715092024)




SRmeans = (0.077627, 0.073275, 0.069833, 0.064159, 0.073046)
SRStd = (0.158114, 0.160656, 0.151127, 0.149817, 0.155852)
SRMeansF = (0.071587999999999999,0.071587999999999999,0.071587999999999999)
SRStdF = (0.15511320000000001,0.15511320000000001,0.15511320000000001)

plt1 = plot_bars_FORMATION_SR(formationNodeletionMeans, formationNodeletionStd,\
formationDeletionMeans, formationDeletionStd, SRMeansF, SRStdF)


##########################################################################
# NON PERSISTING LINKS
deletionFormationMeans = (0.0310193549156, 0.0865167468876, 0.041804038316)
deletionFormationStd = (0.0788210013685, 0.160935564402, 0.106581555167)


# PERSISTING LINKS
deletionNoformationMeans = (0.0727004565385, 0.0680258988703, 0.0229713363971)
deletionNoformationStd = (0.123489476215, 0.140276874039, 0.0746578827396)


# REAL PERSISTING
SRmeans = (0.077627, 0.073275, 0.069833, 0.064159, 0.073046)
SRStd = (0.158114, 0.160656, 0.151127, 0.149817, 0.155852)
SRMeansD = (0.071587999999999999,0.071587999999999999,0.071587999999999999)
SRStdD = (0.15511320000000001,0.15511320000000001,0.15511320000000001)

plt2 = plot_bars_DELETION_SR(deletionNoformationMeans, deletionNoformationStd, \
	deletionFormationMeans, deletionFormationStd, SRMeansD, SRStdD)
##########################################################################

plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(12.4,4.5)
plt.tight_layout()
#plt.figtext(0.20, 0.49, 'Relative status of the pair: weak contacts')
#plt.figtext(0.27, 0.973, 'Relative status of the pair: strong contacts')
#fig.suptitle('Sum of strong contacts', verticalalignment='center', horizontalalignment='center', size = 16)
#fig.suptitle('Sum including weak contacts', verticalalignment='center', y=0.5, horizontalalignment='center', size = 16)

plt.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/simple_explain_SR.eps", dpi=710)

