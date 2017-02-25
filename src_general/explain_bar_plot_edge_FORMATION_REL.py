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

def plot_bars_FORMATION_all_REL_STRONG(DeletionMeans, DeletionStd):

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
	
	ax.set_ylim([-1, 5])
	ax.set_yticks((0,3))

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

def plot_bars_FORMATION_persisting_REL_STRONG(DeletionMeans, DeletionStd):

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
	
	ax.set_ylim([-1, 5])
	ax.set_yticks((0,3))

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
def plot_bars_FORMATION_all_REL_WEAK(DeletionMeans, DeletionStd):

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
	
	ax.set_ylim([-10, 20])
	ax.set_yticks((0,10))

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

def plot_bars_FORMATION_persisting_REL_WEAK(DeletionMeans, DeletionStd):

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
	
	ax.set_ylim([-10, 20])
	ax.set_yticks((0,10))

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
# STRONG contacts REL
formationDeletionMeans = (1.12747979427, 1.56808719079, 1.62160176341)
formationDeletionStd = (1.35650452374, 1.71205560699, 1.83913259462)


plt1 = plot_bars_FORMATION_all_REL_STRONG(formationDeletionMeans, formationDeletionStd)

# PERSISTING LINKS
# STRONG contacts REL

formationNodeletionMeans = (0.964889222681, 1.44874202028, 1.68794592565)
formationNodeletionStd = (1.30256068643, 1.64860382968, 1.94388833634)

plt2 = plot_bars_FORMATION_persisting_REL_STRONG(formationNodeletionMeans, formationNodeletionStd)


# NON PERSISTING LINKS
# WEAK contacts REL
formationDeletionMeans = (4.2541023757, 4.98150869459, 4.83468038207)
formationDeletionStd = (18.6187951251, 13.3061052863, 8.81918134816)





plt1 = plot_bars_FORMATION_all_REL_WEAK(formationDeletionMeans, formationDeletionStd)

# PERSISTING FORMED LINKS
# WEAK contacts REL

formationNoDeletionMeans = (2.78445362373, 3.80942546001, 4.06346226061)
formationNoDeletionStd = (3.74417942972, 4.89548227293, 5.19164363947)

plt2 = plot_bars_FORMATION_persisting_REL_WEAK(formationNoDeletionMeans, formationNoDeletionStd)






plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(8.3,6.5)

plt.figtext(0.20, 0.49, 'Relative status of the pair: weak contacts')
plt.figtext(0.27, 0.973, 'Relative status of the pair: strong contacts')
#fig.suptitle('Sum of strong contacts', verticalalignment='center', horizontalalignment='center', size = 16)
#fig.suptitle('Sum including weak contacts', verticalalignment='center', y=0.5, horizontalalignment='center', size = 16)

plt.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/FORMATION_explain_REL.eps", dpi=710)

