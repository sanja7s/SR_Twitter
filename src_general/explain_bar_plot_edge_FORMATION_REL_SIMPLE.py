#!/usr/bin/env python
# a bar plot with errorbars
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
from pylab import *

width = 0.37      # the width of the bars

font = {'family' : 'sans-serif',
		'variant' : 'normal',
        'weight' : 'light',
        'size'   : 14}

matplotlib.rc('font', **font)
# plot with various axes scales
plt.figure(1)
fig = gcf()


def plot_bars_FORMATION_STRONG_REL(PersistingMeans, PersistingStd, Means, Std):

	ind = np.arange(N)  # the x locations for the groups
	#width = 0.3       # the width of the bars

	#ax = plt.subplot(321)
	ax = plt.subplot2grid((1,2),(0, 0))
	rects1 = ax.bar(ind-0.2, PersistingMeans, width, color='darkred', yerr=PersistingStd, align='center')

	rects2 = ax.bar(ind+0.2, Means, width, color='lightcoral', yerr=Std, align='center')

	ax.legend((rects1[0], rects2[0]), ('Persisting', 'Non-persisting'),frameon=False)

	# add some text for labels, title and axes ticks
	ax.set_title('Strong contacts rel. status')
	ax.set_xticks(ind )
	ax.set_xticklabels(('Before', 'At activation', 'After'))
	
	ax.set_ylim([-1, 10])
	ax.set_yticks((0,5,10))

	#plt.legend(frameon=False)


	def autolabel(rects):
	    # attach some text labels
	    for rect in rects:
	        height = rect.get_height()
	        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
	                '%.2f' % float(height),
	                ha='center', va='bottom')

	autolabel(rects1)
	autolabel(rects2)

	return plt

###################################################################################################
def plot_bars_FORMATION_WEAK_REL(PersistingMeans, PersistingStd, Means, Std):

	ind = np.arange(N)  # the x locations for the groups
	#width = 0.3       # the width of the bars

	#ax = plt.subplot(321)
	ax = plt.subplot2grid((1,2),(0, 1))
	rects1 = ax.bar(ind-0.2, PersistingMeans, width, color='darkred', align='center', yerr=PersistingStd, label = 'Activation')
	rects2 = ax.bar(ind+0.2, Means, width, color='lightcoral', yerr=Std, align='center', label = 'Activation')


	# add some text for labels, title and axes ticks
	#ax.set_ylabel('Avg Rel Soc St')
	ax.set_title('Weak contacts rel. status')
	ax.set_xticks(ind)
	ax.set_xticklabels(('Before', 'At activation', 'After'))
	
	ax.set_ylim([-2, 20])
	ax.set_yticks((0,10,20))

	ax.legend((rects1[0], rects2[0]), ('Persisting', 'Non-persisting'),frameon=False)

	def autolabel(rects):
	    # attach some text labels
	    for rect in rects:
	        height = rect.get_height()
	        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
	                '%.2f' % float(height),
	                ha='center', va='bottom')

	autolabel(rects1)
	autolabel(rects2)

	return plt



N = 3
##########################################################################
# NON PERSISTING LINKS
# STRONG contacts REL
formationDeletionMeans = (1.12747979427, 1.56808719079, 1.62160176341)
formationDeletionStd = (1.35650452374, 1.71205560699, 1.83913259462)

# PERSISTING LINKS
# STRONG contacts REL
formationNodeletionMeans = (0.964889222681, 1.44874202028, 1.68794592565)
formationNodeletionStd = (1.30256068643, 1.64860382968, 1.94388833634)

plt1 = plot_bars_FORMATION_STRONG_REL(formationNodeletionMeans, formationNodeletionStd, formationDeletionMeans, formationDeletionStd)

##########################################################################
# NON PERSISTING LINKS
# WEAK contacts REL
formationDeletionMeans = (4.2541023757, 4.98150869459, 4.83468038207)
formationDeletionStd = (18.6187951251, 13.3061052863, 8.81918134816)

# PERSISTING FORMED LINKS
# WEAK contacts REL
formationNoDeletionMeans = (2.78445362373, 3.80942546001, 4.06346226061)
formationNoDeletionStd = (3.74417942972, 4.89548227293, 5.19164363947)

plt2 = plot_bars_FORMATION_WEAK_REL(formationNoDeletionMeans, formationNoDeletionStd, formationDeletionMeans, formationDeletionStd)
##########################################################################

plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(8.3,6.5)

#plt.figtext(0.20, 0.49, 'Relative status of the pair: weak contacts')
#plt.figtext(0.27, 0.973, 'Relative status of the pair: strong contacts')
#fig.suptitle('Sum of strong contacts', verticalalignment='center', horizontalalignment='center', size = 16)
#fig.suptitle('Sum including weak contacts', verticalalignment='center', y=0.5, horizontalalignment='center', size = 16)

plt.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/simple_FORMATION_explain_REL.eps", dpi=710)

