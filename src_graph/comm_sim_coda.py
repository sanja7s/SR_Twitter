#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import csv
from sklearn.metrics import f1_score
from collections import defaultdict
import sys
import getopt
import itertools
import os, glob

#IN_DIR = "../../../DATA/mention_graph/coda"
IN_DIR = "../../../DATA/mention_graph/CODA2"

def compute_jaccard_index(set_1, set_2):
    return len(set_1.intersection(set_2)) / float(len(set_1.union(set_2)))

"""
print("The script calculates the similarity between ground truth and obtained communities")
print("It receives the ground truth communities as first argument and obtained communities as second argument")
print("Both files must be in the following format:")
print('Node_1\tNode_2\tNode_3\t...Node_k')
print('Node_i\tNode_i+1\tNode_i+1\t...Node_i+k')
print("...")
print('Node_j\tNode_j+1\tNode_j+1\t...Node_n')
print("The results is the jaccardi similarity coef and F1 score similarity coefficient")
print("The files DO NOT HAVE TO BE SORTED by the node id...")
"""
os.chdir(IN_DIR)

y = []
with open(sys.argv[1]) as f_gt:
    for row in f_gt:
        y.append(row.split())

gt_comm_dct = defaultdict(list)
count=0
for item in y:
    gt_comm_dct[count].append(map(int, item))
    count+=1

y = []
with open(sys.argv[2]) as f_comm:
    for row in f_comm:
        y.append(row.split())

comm_dct = defaultdict(list)
count=0
for item in y:
    comm_dct[count].append(map(int,item))
    count+=1

num_gt=len(gt_comm_dct)
num_comm=len(comm_dct)
print "Calculating..."
sum_j=0
sum_f=0
with open(sys.argv[1] + '_' + sys.argv[2] + '_sim_CODA' ,'w') as f:
    for c_star in gt_comm_dct:
        c = c_star
        ji=compute_jaccard_index(set(list(itertools.chain(*gt_comm_dct[c_star]))), set(list(itertools.chain(*comm_dct[c]))))
        f.write(str(c_star) + '\t' + str(c) + '\t' + str(ji) + '\n')
        sum_j+=ji

match_j = sum_j/(2*num_gt)

print "Overall Jaccardi similarity is:"
print match_j
