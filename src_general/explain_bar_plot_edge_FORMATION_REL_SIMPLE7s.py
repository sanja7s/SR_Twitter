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

def plot_bars_FORMATION_STRONG_REL(PersistingMeans, PersistingStd, Means, Std, PERSreal, PERSstd):

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

	# add some text for labels, title and axes ticks
	ax.set_title('Relative status (strong contacts)')
	ax.set_xticks(ind )
	ax.set_xticklabels(('Before', 'At formation', 'After'))
	
	ax.set_ylim([-1, 10])
	ax.set_yticks((0,5,10))


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
def plot_bars_FORMATION_WEAK_REL(PersistingMeans, PersistingStd, Means, Std, PERSreal, PERSstd):

	ind = np.arange(N)  # the x locations for the groups
	#width = 0.3       # the width of the bars

	#ax = plt.subplot(321)
	ax = plt.subplot2grid((1,2),(0, 1))

	#axs[1].bar(x, a, width=1/3, facecolor='b', alpha=.5, linewidth=0)
	#axs[1].bar(x+1/3, b, width=1/3, facecolor='r', alpha=.5, linewidth=0)
	#axs[1].bar(x+2/3, c, width=1/3, facecolor='g', alpha=.5, linewidth=0)

	rects1 = ax.bar(ind-width, PersistingMeans, width, color='darkred', \
		align='center', yerr=PersistingStd, linewidth=0, \
		error_kw=dict(ecolor='gray', lw=1.5, capsize=2.7, capthick=1))

	rects2 = ax.bar(ind, Means, width, color='lightcoral', \
		yerr=Std, align='center', linewidth=0, \
		error_kw=dict(ecolor='gray', lw=1.5, capsize=2.7, capthick=1))

	rects3 = ax.bar(ind+width, PERSreal, width, color='r',\
		yerr=PERSstd, align='center',linewidth=0, \
		error_kw=dict(ecolor='gray', lw=1.5, capsize=2.7, capthick=1))

	# add some text for labels, title and axes ticks
	ax.set_title('Relative status (including weak contacts)')
	ax.set_xticks(ind)
	ax.set_xticklabels(('Before', 'At formation', 'After'))
	
	ax.set_ylim([-2, 20])
	ax.set_yticks((0,10,20))

	ax.legend((rects1[0], rects2[0], rects3[0]), \
		('Formed and persisting', \
			'Formed and non-persisting', 'Persisting average'),\
		frameon=False)

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
# STRONG contacts REL
formationDeletionMeans = (1.12747979427, 1.56808719079, 1.62160176341)
formationDeletionStd = (1.35650452374, 1.71205560699, 1.83913259462)

# PERSISTING LINKS
# STRONG contacts REL
formationNodeletionMeans = (0.964889222681, 1.44874202028, 1.68794592565)
formationNodeletionStd = (1.30256068643, 1.64860382968, 1.94388833634)

SRMeans = (0.856632, 0.906697, 0.995124, 1.010403, 1.031534)
SRStd = (1.114944, 1.194131, 1.283704, 1.245234, 1.317081)
SRMeansS = (0.96007799999999988,0.96007799999999988,0.96007799999999988)
SRStdS = (1.2310188,1.2310188,1.2310188)

plt1 = plot_bars_FORMATION_STRONG_REL(formationNodeletionMeans, formationNodeletionStd,\
formationDeletionMeans, formationDeletionStd, SRMeansS, SRStdS)


##########################################################################
# NON PERSISTING LINKS
# WEAK contacts REL
formationDeletionMeans = (4.2541023757, 4.98150869459, 4.83468038207)
formationDeletionStd = (18.6187951251, 13.3061052863, 8.81918134816)

# PERSISTING FORMED LINKS
# WEAK contacts REL
formationNodeletionMeans = (2.78445362373, 3.80942546001, 4.06346226061)
formationNodeletionStd = (3.74417942972, 4.89548227293, 5.19164363947)

# REAL PERSISTING
SRMeans = (2.062419, 2.089727, 2.247399, 2.279259, 2.290962)
SRStd = (2.614107, 2.647424, 3.026795, 2.916765, 3.009769)
SRMeansW = (2.1939532000000002, 2.1939532000000002, 2.1939532000000002)
SRStdW = (2.8429720000000001, 2.8429720000000001, 2.8429720000000001)

plt2 = plot_bars_FORMATION_WEAK_REL(formationNodeletionMeans, formationNodeletionStd,\
formationDeletionMeans, formationDeletionStd, SRMeansW, SRStdW)
##########################################################################

plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(12.4,4.5)
plt.tight_layout()
#plt.figtext(0.20, 0.49, 'Relative status of the pair: weak contacts')
#plt.figtext(0.27, 0.973, 'Relative status of the pair: strong contacts')
#fig.suptitle('Sum of strong contacts', verticalalignment='center', horizontalalignment='center', size = 16)
#fig.suptitle('Sum including weak contacts', verticalalignment='center', y=0.5, horizontalalignment='center', size = 16)

plt.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/simple_FORMATION_explain_REL_3.eps", dpi=710)

