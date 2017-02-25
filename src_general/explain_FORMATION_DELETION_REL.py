#!/usr/bin/env python
# a bar plot with errorbars
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
from pylab import *

width = 0.28      # the width of the bars

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
	#ax.set_title('Relative status (strong contacts)')
	ax.set_xticks(ind )
	ax.set_xticklabels(('Before', 'At formation', 'After'))
	
	ax.set_ylim([-0.5, 5])
	ax.set_yticks((0,5))


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


def plot_bars_DELETION_STRONG_REL(PersistingMeans, PersistingStd, Means, Std, PERSreal, PERSstd):

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
		loc='best',frameon=False)

	# add some text for labels, title and axes ticks
	#ax.set_title('Relative status (strong contacts)')
	ax.set_xticks(ind )
	ax.set_xticklabels(('Before', 'At decommission', 'After'))
	
	ax.set_ylim([-0.5, 5])
	ax.set_yticks((0,5))


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

##########################################################################
# NON PERSISTING LINKS
# STRONG contacts REL
#deletionFormationMeans = (1.35860783095, 1.40335612181, 1.38222498446)
#deletionFormationStd = (1.39698763227, 1.515042018, 1.6001731639)

deletionFormationMeans = (1.21614009307, 1.58645603723, 1.613397012)
deletionFormationStd = (1.39228801763, 1.73298601092, 1.84822380219)


# PERSISTING LINKS
#deletionNoformationMeans = (1.16101995042, 1.52591193484, 1.54066816196)
#deletionNoformationStd = (1.36105887603, 1.69996084625, 1.80123581372)

deletionNoformationMeans = (1.09195402299, 1.16457680251, 1.09717868339)
deletionNoformationStd = (1.25857893939, 1.33146910699, 1.31900439894)



SRMeans = (0.856632, 0.906697, 0.995124, 1.010403, 1.031534)
SRStd = (1.114944, 1.194131, 1.283704, 1.245234, 1.317081)
SRMeansS = (0.96007799999999988,0.96007799999999988,0.96007799999999988)
SRStdS = (1.2310188,1.2310188,1.2310188)

plt1 = plot_bars_DELETION_STRONG_REL(deletionNoformationMeans, deletionNoformationStd,\
	deletionFormationMeans, deletionFormationStd, SRMeansS, SRStdS)

##########################################################################


plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(12.4,4.5)
plt.tight_layout()
#plt.figtext(0.20, 0.49, 'Relative status of the pair: weak contacts')
#plt.figtext(0.27, 0.973, 'Relative status of the pair: strong contacts')
fig.suptitle('Relative status (strong contacts)', verticalalignment='center', horizontalalignment='center', size = 16)
#fig.suptitle('Sum including weak contacts', verticalalignment='center', y=0.5, horizontalalignment='center', size = 16)

plt.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/explain_FORMATION_DELETION_REL.eps", dpi=710)

