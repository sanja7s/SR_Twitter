from collections import defaultdict
import codecs
import matplotlib.pyplot as plt
import pylab as P
import numpy as np
import networkx as nx
import time
import matplotlib.dates as mdates
import community
import graph as GG

WORKING_FOLDER = "filter_more_20_tweets/"
F_IN = WORKING_FOLDER + "graph_data.tab"

F_OUT_1 = WORKING_FOLDER + "com_SR_avg_mode.tab"
F_OUT_2 = WORKING_FOLDER + "set_of_com_nodes.tab"

G = nx.DiGraph()
G_WITH_SR = GG.read_in_graph_with_SR()

def graphs_stats():
	print "Created directed graph, with: ", G.number_of_nodes(), "nodes; and: ", G.number_of_edges(), " edges."
	print "7 maximum degrees of nodes: ", sorted(nx.degree(G).values())[-7:]
	print "7 maximum indegrees of nodes: ", sorted(G.in_degree().values())[-7:]
	print "7 maximum outdegrees of nodes: ", sorted(G.out_degree().values())[-7:]
	print "Connected components: ", len(nx.connected_components(G.to_undirected()))
	i = 0
	print "7 maximum connected components: "
	for el in sorted(nx.connected_components(G.to_undirected()), key=lambda x: len(x), reverse=True):
		i+=1
		print len(el)
		if i==7: break
	#nx.draw(G)
	#plt.show()

def read_in_graph_data():
	global G
	input_file = codecs.open(F_IN, 'r', encoding='utf8')
	for line in input_file:
		line = line.split()
		usr1 = line[0]
		usr2 = line[1]
		weight = int(line[2])
		G.add_edge(usr1, usr2, weight=weight)
	input_file.close()

def subgraph_SR(list_nodes):
	SR_lst = []
	for node1 in list_nodes:
		for node2 in list_nodes:
			k = (node1, node2)
			try:
				SR_lst.append(G_WITH_SR[k][1])
			except:
				KeyError
	return SR_lst

def save_communities():
	partition = community.best_partition(G.to_undirected())
	output_file = codecs.open(F_OUT_2, 'w', encoding = 'utf8')
	for com in set(partition.values()):
		list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
		output_file.write(str(com) + ': \t' + str(list_nodes) + '\n')


def SR_in_graph_communities():
	output_file = codecs.open(F_OUT_1, 'w', encoding = 'utf8')
	partition = community.best_partition(G.to_undirected())
	size = float(len(set(partition.values())))
	cnt = 0
	print size
	for com in set(partition.values()):
		cnt = cnt + 1
		list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
		SR_lst = subgraph_SR(list_nodes)
		print com, np.mean(SR_lst), np.median(SR_lst)
		output_file.write(str(com) + '\t' + str(len(list_nodes)) + '\t' + str(np.mean(SR_lst)) + '\t' + str(np.median(SR_lst)) + '\n')
	print cnt, "communities found."


read_in_graph_data()
#save_communities()
SR_in_graph_communities()