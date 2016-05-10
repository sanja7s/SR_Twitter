#import networkx as nx
from scipy import stats
from operator import mul    # or mul=lambda x,y:x*y
from fractions import Fraction
import sys
from igraph import *
import numpy as np
# Calculates binomial coefficient (n over k)
def nCk(n,k):
  return int( reduce(mul, (Fraction(n-i, i+1) for i in range(k)), 1) )

#########################
# read from a file that is an edge list with SR weights
#########################
def read_in_SR_graph():
	G = Graph.Read_Ncol(sys.argv[1], directed=False, weights=True)
	print sys.argv[1]
	return G

def study_assort(net, threshold):
	print "stats for %.2f" % threshold
	to_delete_edges = [e.index for e in net.es if float(e["weight"]) <= threshold]
	net.delete_edges(to_delete_edges)
	# just a check
	not_connected_nodes = net.vs(_degree_eq=0)
	print 'Not conneted nodes deleted ', len(not_connected_nodes)
	net.delete_vertices(not_connected_nodes)
	summary(net)
	# calculate the transitivity of the network
	#C=nx.transitivity(net)
	C =  net.transitivity_undirected()
	# Make dictionary nodeID:degree
	#d=dict(nx.degree(net))
	d = {n["name"]: net.degree(n.index, mode=ALL, loops=False) for n in net.vs}

	# The branching is calculated as P2/P1
	# The intermodular connectivity as P3/P2
	suma1=0
	P2=0
	for key in d:
		suma1+=int(d[key])
		P2+=nCk(int(d[key]),2)
	P1=suma1*0.5
	C3=C*P2/3.0
	suma=0
	for e in net.es:
		uid = e.source
		vid = e.target
		u = net.vs[uid]["name"]
		v = net.vs[vid]["name"]
		suma=suma+(d[u]-1)*(d[v]-1)

	P3=suma-3*C3

	P21=float(P2)/float(P1) if float(P1) <> 0 else 0
	P32=float(P3)/float(P2) if float(P2) <> 0 else 0

	# Conditions for assortativity and disassortativity
	DA = net.assortativity_degree(directed=False)
	if P32 + C > P21:
		print("The network is assortative with r = "+str(DA))
	elif P32 + C < P21:
		print("The network is disassortative with r = "+str(DA))
	else:
		print("The network is neutral with r = "+str(DA))

	print("The relative branching is: " + str(P21))
	print("The intermodular connectivity is: " + str(P32))
	print("The transitivity is: " + str(C))

	return P21, P32, C

# Read the network in form of edge list, weighted and undirected
#net=nx.read_edgelist(sys.argv[1], nodetype=int)
net = read_in_SR_graph()
summary(net)

f = open('Deg_assort_study.tab', "w")
for threshold in np.arange(0, 0.9, 0.01):
	P21, P32, C = study_assort(net, threshold)
	f.write(str(threshold) + '\t'+ str(P21) + '\t' + str(P32) + '\t' + str(C) + '\n')