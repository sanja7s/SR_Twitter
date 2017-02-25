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

def plot_bars_FORMATION_all_TOT_STRONG(DeletionMeans, DeletionStd):

	ind = np.arange(N)  # the x locations for the groups
	#width = 0.3       # the width of the bars

	#ax = plt.subplot(321)
	ax = plt.subplot2grid((2,2),(0, 1))
	rects1 = ax.bar(ind, DeletionMeans, width, color='darkred', yerr=DeletionStd, label = 'Activation')


	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg Rel Soc St')
	ax.set_title('Non persisting interactions')
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

def plot_bars_FORMATION_persisting_TOT_STRONG(DeletionMeans, DeletionStd):

	ind = np.arange(N)  # the x locations for the groups
	#width = 0.3       # the width of the bars

	#ax = plt.subplot(321)
	ax = plt.subplot2grid((2,2),(0, 0))
	rects1 = ax.bar(ind, DeletionMeans, width, color='darkred', yerr=DeletionStd, label = 'Activation')


	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg Rel Soc St')
	ax.set_title('Persisting interactions')
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

###################################################################################################
def plot_bars_FORMATION_all_TOT_WEAK(DeletionMeans, DeletionStd):

	ind = np.arange(N)  # the x locations for the groups
	#width = 0.3       # the width of the bars

	#ax = plt.subplot(321)
	ax = plt.subplot2grid((2,2),(1, 1))
	rects1 = ax.bar(ind, DeletionMeans, width, color='darkred', yerr=DeletionStd, label = 'Activation')


	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg Rel Soc St')
	ax.set_title('Non persisting interactions')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(('Before', 'At activation', 'After'))
	
	ax.set_ylim([-10, 40])
	ax.set_yticks((0,20))

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

def plot_bars_FORMATION_persisting_TOT_WEAK(DeletionMeans, DeletionStd):

	ind = np.arange(N)  # the x locations for the groups
	#width = 0.3       # the width of the bars

	#ax = plt.subplot(321)
	ax = plt.subplot2grid((2,2),(1, 0))
	rects1 = ax.bar(ind, DeletionMeans, width, color='darkred', yerr=DeletionStd, label = 'Activation')


	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg Rel Soc St')
	ax.set_title('Persisting interactions')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(('Before', 'At activation', 'After'))
	
	ax.set_ylim([-10, 40])
	ax.set_yticks((0,20))

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



N = 3

##########################################################################
# NON PERSISTING LINKS
# STRONG contacts TOT
formationDeletionMeans = (1.80394317904, 5.00428606417, 3.27749204017)
formationDeletionStd = (1.9755148583, 2.72691364807, 2.81912929162)

plt1 = plot_bars_FORMATION_all_TOT_STRONG(formationDeletionMeans, formationDeletionStd)

# PERSISTING LINKS
# STRONG contacts TOT

formationNodeletionMeans = (1.37082238077, 4.7303792715, 4.65264739016)
formationNodeletionStd = (1.82950665268, 2.75023723532, 3.33011040538)

plt2 = plot_bars_FORMATION_persisting_TOT_STRONG(formationNodeletionMeans, formationNodeletionStd)


# NON PERSISTING LINKS
# WEAK contacts TOT
formationDeletionMeans = (8.96632378153, 14.7865540044, 10.9745285329)
formationDeletionStd = (19.6694822091, 15.3839941013, 11.2672905848)


plt1 = plot_bars_FORMATION_all_TOT_WEAK(formationDeletionMeans, formationDeletionStd)

# PERSISTING FORMED LINKS
# WEAK contacts TOT

formationNodeletionMeans = (6.9913631243, 12.496620353, 12.0570784829)
formationNodeletionStd = (6.69449758508, 8.88552641326, 9.38191875769)

plt2 = plot_bars_FORMATION_persisting_TOT_WEAK(formationNodeletionMeans, formationNodeletionStd)






plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(8.3,6.5)

plt.figtext(0.30, 0.5, 'Sum of pair\'s weak contacts')
plt.figtext(0.37, 0.973, 'Sum of pair\'s strong contacts')
#fig.suptitle('Sum of strong contacts', verticalalignment='center', horizontalalignment='center', size = 16)
#fig.suptitle('Sum including weak contacts', verticalalignment='center', y=0.5, horizontalalignment='center', size = 16)

plt.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/FORMATION_explain.eps", dpi=710)

