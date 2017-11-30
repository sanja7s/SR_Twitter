#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''

'''
import math, os
#from collections import defaultdict, OrderedDict
#import numpy as np
#from scipy.stats.stats import pearsonr
#from scipy import stats

from graph_tool.all import *

#WORKING_FOLDER = '../../../DATA/FIN'
#os.chdir(WORKING_FOLDER)

"""
class graph_tool.inference.OverlapBlockState(g, b=None, 
B=None, recs=[], rec_types=[], rec_params=[], clabel=None, 
pclabel=None, deg_corr=True, allow_empty=False, max_BE=1000,
                                        **kwargs)
"""


def run_SBM_auto_overlapping():
    
    
    g = load_graph('test_small_weighted.graphml')
    
    print(g)

    weight_log = g.new_edge_property("double")
    for edge in g.edges():
        try:
            weight_log[edge] = math.log(g.ep.weight[edge])
        except ValueError:
            print g.ep.weight[edge]

    #print weight_log

    
    
    state = minimize_blockmodel_dl(g, overlap=True, nonoverlap_init=False,verbose=True)
    
    bb = state.get_blocks()
    
    
    #s = OverlapBlockState(g, b=bb)
    
    s = OverlapBlockState(g, b=bb, recs=[weight_log],rec_types=["real-exponential"])
    
    #print s
    
    b = s.get_overlap_blocks()
    

    
    SBM_overlap_blocks = defaultdict(list)
    vprop = g.vertex_properties["name"] 
    for vertex in g.vertices():
        for block_id in b[0][vertex]:
            SBM_overlap_blocks[block_id].append(vprop[vertex])
            

    f_out=open('test_SBM_auto_overlapping_clusters_node_names_7s','w')
    for el in SBM_overlap_blocks:
        for node in SBM_overlap_blocks[el]:
            f_out.write(str(int(node)) + '\t')
        f_out.write('\n')

def run_SBM_auto_overlapping_unweighted():
    
    
    g = load_graph('mutual_unweighted.graphml')
    
    print(g)

    
    state = minimize_blockmodel_dl(g, overlap=True, nonoverlap_init=False)
    
    bb = state.get_blocks()
    
    
    s = OverlapBlockState(g, b=bb)
    
    b = s.get_overlap_blocks()
    
    
    SBM_overlap_blocks = defaultdict(list)
    vprop = g.vertex_properties["name"] 
    for vertex in g.vertices():
        for block_id in b[0][vertex]:
            SBM_overlap_blocks[block_id].append(vprop[vertex])
            

    f_out=open('SBM_auto_overlapping_clusters_node_names_7s','w')
    for el in SBM_overlap_blocks:
        for node in SBM_overlap_blocks[el]:
            f_out.write(str(int(node)) + '\t')
        f_out.write('\n')

    
    

run_SBM_auto_overlapping()

#run_SBM_auto_overlapping_unweighted()