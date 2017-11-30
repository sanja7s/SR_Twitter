
# coding: utf-8

# # BigClam: Cluster Affiliation Model
# This algorithm works only for undirected unlabeled (unweighted) networks

# In[297]:


import os
from graph_tool.all import *
import codecs
from collections import defaultdict, OrderedDict
import matplotlib.pyplot as plt
import numpy as np
get_ipython().magic(u'matplotlib inline')
from igraph import *
from scipy.stats.stats import pearsonr
from scipy import stats


# In[298]:


WORKING_FOLDER = '../../DATA/FIN/BigClam'
os.chdir(WORKING_FOLDER)
f_in_graph = 'mention_graph_weights.dat'
f_in_BigClam_output_comm = 'BigClam_MENT_COMM7scmtyvv.txt'


# In[299]:


# returns a dict with nodes ids per community in each value
# dict keys are just community ids in returned order 
def read_BigClam_output(F_IN):  
    input_file = codecs.open(F_IN, 'r', encoding='utf8')
    BigClam_output = defaultdict(int)
    num_COMM = 0
    for line in input_file:
        line = line.split()
        BigClam_output[num_COMM] = line
        num_COMM += 1
    return BigClam_output


# In[300]:


# a helper function to show us info when print info is true
# otherwise returns only the list of community sizes
def num_and_sizes_BigClam_COMM(F_IN, print_info=False):
    num_COMM = 0
    COMM_sizes = []
    ALL_users = defaultdict(int)
    input_file = codecs.open(F_IN, 'r', encoding='utf8')
    for line in input_file:
        line = line.split()
        num_COMM += 1
        COMM_sizes.append(len(line))
        for el in line:
            ALL_users[el] = 1
    if print_info:
        print 'BigClam has output: %d COMM ' % (num_COMM)
        print 'Their sizes in increasing order:'
        print sorted(COMM_sizes)
        print 'Total number of users in COMM:'
        print len(ALL_users.keys())
        print 'Total size of COMM:'
        print sum(COMM_sizes)
    input_file.close()
    return COMM_sizes


# In[301]:


num_and_sizes_BigClam_COMM(f_in_BigClam_output_comm, print_info=True)


# In[315]:


# returns the node membership for each node
# i.e., in how many communities in participates
def find_nodes_in_more_COMM(F_IN):
    nodes_num_COMM = defaultdict(int)
    input_file = codecs.open(F_IN, 'r', encoding='utf8')
    for line in input_file:
        line = line.split()
        for node in line:
            nodes_num_COMM[int(node)] += 1
    #nodes_num_COMM2 = {node: nodes_num_COMM[node] if nodes_num_COMM[node] < 10 else 10 for node in nodes_num_COMM}
    sorted_nodes_num_COMM = OrderedDict(sorted(nodes_num_COMM.items(), key=lambda t:t[1], reverse=True))
    #print sorted_nodes_num_COMM
    return sorted_nodes_num_COMM


# In[316]:


find_nodes_in_more_COMM(f_in_BigClam_output_comm)


# # Let us visualize the overalpping community structure

# In[304]:


def plot_ccdf_node_comm_membership(F_IN):
    nodes_num_COMM = find_nodes_in_more_COMM(F_IN)
    data = np.array(nodes_num_COMM.values())
    sorted_data = np.sort(data)
    yvals=1-np.arange(len(sorted_data))/float(len(sorted_data)-1)
    plt.plot(sorted_data,yvals,color='r')
    plt.yscale('log')
    plt.ylabel('complementary CDF')
    plt.xscale('log')
    plt.xlabel('memberships')
    plt.show()


# In[305]:


plot_ccdf_node_comm_membership(f_in_BigClam_output_comm)


# In[306]:


def plot_ccdf_comm_sizes(F_IN):
    COMM_sizes = num_and_sizes_BigClam_COMM(F_IN)
    data = np.array(COMM_sizes)
    sorted_data = np.sort(data)
    yvals=1-np.arange(len(sorted_data))/float(len(sorted_data)-1)
    plt.plot(sorted_data,yvals,color='r')
    plt.yscale('log')
    plt.ylabel('complementary CDF')
    plt.xscale('log')
    plt.xlabel('community size')
    plt.show()


# In[307]:


plot_ccdf_comm_sizes(f_in_BigClam_output_comm)


# In[308]:


def transform_decimal_format():
    input_file = codecs.open('undirected_mention_graph_with_SR.csv', 'r', encoding='utf8')
    output_file = codecs.open('undirected_mention_graph_with_SR_NCOL_edgelist', 'w', encoding='utf8')
    for line in input_file:
        print line
        line = line.replace('.', ',')
        print line
        output_file.write(line)


# In[309]:


def read_in_SR_graph():
    #G = Graph.Read_Ncol('undirected_mention_graph_with_SR.csv', directed=False, weights=True)
    #G = read("test", format="ncol", directed=False, weights=True)
    G = Graph.Read_Ncol('undirected_mention_graph_with_SR_NCOL_edgelist', directed=False, weights=True, names=True)
    print G.summary()
    #for edge in G.es():
    #    print edge.tuple[0], edge.tuple[1], edge["weight"]
    return G


# In[310]:


def find_avg_SR(G, nodes):
    node_SR_list = []
    node_indices = []
    for el in nodes:
        n = G.vs.select(name = str(el))[0]
        n = n.index
        node_indices.append(n)
    edges = G.es.select(_within = node_indices)
    for e in edges:
        w = e['weight']
        node_SR_list.append(w)
    avg_SR = np.mean(np.array(node_SR_list))
    std_SR = np.std(np.array(node_SR_list))
    return (avg_SR, std_SR)      


# In[311]:


def avg_SR_per_COMM_size(F_IN):
    BigClam_output = read_BigClam_output(F_IN)
    G = read_in_SR_graph()
    size_vs_SR = defaultdict(int)
    for comm_nodes in BigClam_output.values():
        size_vs_SR[len(comm_nodes)] = find_avg_SR(G, comm_nodes)
    return size_vs_SR


# In[312]:


avg_SR_per_COMM_size(f_in_BigClam_output_comm)


# In[317]:


def plot_avg_SR_per_COMM_size(F_IN):
    size_vs_SR = avg_SR_per_COMM_size(F_IN)
    x = np.array(size_vs_SR.keys())
    y = np.array([s[0] for s in size_vs_SR.values()])
    e = np.array([s[1] for s in size_vs_SR.values()])
    print 'Corrcoef',  pearsonr(x, y)
    plt.errorbar(x,y,e,linestyle="-",marker='*',color='maroon',label='mean SR per comm')
    #plt.yscale('log', nonposy='clip')
    plt.xlabel('comm size')
    plt.ylabel('mean SR')
    plt.legend(loc='best',frameon=False)
    plt.show()


# In[318]:


plot_avg_SR_per_COMM_size(f_in_BigClam_output_comm)

