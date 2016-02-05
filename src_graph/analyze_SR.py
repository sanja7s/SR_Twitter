import codecs
from scipy.stats.stats import pearsonr, spearmanr
from collections import defaultdict, OrderedDict
import numpy as np
from scipy.interpolate import UnivariateSpline
import matplotlib.mlab as mlab
from matplotlib import pyplot as plt

f_in = "graph_data_with_SR.tab"
f_out = "mention_graph_with_SR_undirected.tab"
f_undirected_in = "graph_data_with_SR_undirected.tab"

def read_in_graph_with_SR(f_in):
	graph_with_SR = defaultdict(list)
	with codecs.open(f_in,'r', encoding='utf8') as input_file:
	    for line in input_file:	
	    	line = line.split()
	    	usr1 = line[0]
	    	usr2 = line[1]
	    	weight = int(line[2])
	    	SR = line[3]
	    	if SR == 'None' or SR == '-1':
	    		continue
	    	SR = float(SR)
	    	graph_with_SR[(usr1, usr2)] = (weight, SR)
	return graph_with_SR

def read_in_undirected_graph_with_SR():

	graph_with_SR = defaultdict(list)
	with codecs.open(f_undirected_in,'r', encoding='utf8') as input_file:
	    for line in input_file:	
	    	line = line.split()
	    	usr1 = line[0]
	    	usr2 = line[1]
	    	weight = int(line[2])
	    	SR = line[3]
	    	if SR == 'None' or SR == '-1':
	    		continue
	    	SR = float(SR)
	    	graph_with_SR[(usr1, usr2)] = (weight, SR)
	return graph_with_SR


def save_undirected_graph_with_SR():
	directed_graph_with_SR = read_in_graph_with_SR(f_in)
	undirected_graph_with_SR = defaultdict(list)
	with codecs.open(f_out,'w', encoding='utf8') as output_file:
		for edge in directed_graph_with_SR.keys():
			w = directed_graph_with_SR[edge][0]
			sr = directed_graph_with_SR[edge][1]
			key2 = tuple(sorted((edge[1],edge[0])))
			if key2 not in undirected_graph_with_SR.iterkeys():
				undirected_graph_with_SR[key2] = (w, sr)
			else:
				undirected_graph_with_SR[key2] = (w + undirected_graph_with_SR[key2][0], undirected_graph_with_SR[key2][1])
				output_file.write(str(edge[0]) + '\t' + str(edge[1]) + '\t' + str(undirected_graph_with_SR[key2][0]) + '\t' + str(undirected_graph_with_SR[key2][1]) + '\n')
	return undirected_graph_with_SR


def SR_vs_weight(threshold=50):
	graph_with_SR = read_in_undirected_graph_with_SR()
	SR = []
	weights = []
	cnt = 0
	for key in graph_with_SR.iterkeys():
		sr = graph_with_SR[key][1]
		w = graph_with_SR[key][0]
		cnt += 1
		if cnt % 10000 == 0:
			print "Read ", cnt, " edges."
		if w > threshold and sr > 0:
			SR.append(sr)
			weights.append(w)
	print "Pearson cor (undirected) with threshold ", threshold, 
	print ('is: {0:.3f}'.format(float(pearsonr(SR, weights))))
	print "Spearman cor (undirected) with threshold ", threshold,
	print ('is: {0:.3f}'.format(float(spearmanr(SR, weights))))

SR_vs_weight()

def SR_pdf():
	graph_with_SR = read_in_graph_with_SR(f_in)
	SR = []
	weights = []
	for key in graph_with_SR.iterkeys():
		sr = float(graph_with_SR[key][1])
		# print sr
		if sr >= 0 and sr < 1:
			SR.append(sr)
		weights.append(graph_with_SR[key][0])


	# took this code from StackOverflow and edited to plot pdf and add a function to smooth the data 
	N = len(SR)
	n = N/10
	print N
	s = np.asarray(SR)   # generate your data sample with N elements
	print len(s)

	'''
	p, x = np.histogram(s, bins=n) # bin it into n = N/10 bins
	x = x[:-1] + (x[1] - x[0])/2   # convert bin edges to centers
	f = UnivariateSpline(x, p, s=n)
	plt.plot(x, f(x))
	plt.show()
	'''

	mu, sigma = 100, 15
	# the histogram of the data
	n, bins, patches = plt.hist(s, 100, normed=0, facecolor='green', alpha=0.55)

	
	# add a 'best fit' line
	#y = mlab.normpdf( bins, mu, sigma)
	#l = plt.plot(bins, y, 'r--', linewidth=1)

	plt.xlabel('SR value')
	plt.ylabel('Number of user pairs')
	plt.title('Histogram of SR')
	plt.axis([0, 1, 0, 115])
	plt.grid(True)
	

	plt.show()

#SR_pdf()

save_undirected_graph_with_SR()