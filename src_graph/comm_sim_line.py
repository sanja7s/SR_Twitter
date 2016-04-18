#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import csv
from sklearn.metrics import f1_score
from collections import defaultdict
import sys
import getopt
import itertools
import os, glob

IN_DIR = "../../../DATA/mention_graph/coda"

def compute_jaccard_index(set_1, set_2):
    return len(set_1.intersection(set_2)) / float(len(set_1.union(set_2)))

def F1_score(tags,predicted):
    tags = set(tags)
    predicted = set(predicted)

    tp = len(tags & predicted)
    fp = len(predicted) - tp
    fn = len(tags) - tp

    if tp>0:
        precision=float(tp)/(tp+fp)
        recall=float(tp)/(tp+fn)
        return 2*((precision*recall)/(precision+recall))
    else:
        return 0

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
with open(sys.argv[1] + '_' + sys.argv[2] + '_sim_line' ,'w') as f:
    for c_star in gt_comm_dct:
        max_j=0
        max_f=0
        for c in comm_dct:
            ji=compute_jaccard_index(set(list(itertools.chain(*gt_comm_dct[c_star]))), set(list(itertools.chain(*comm_dct[c]))))
            if ji>max_j:
                max_j=ji
                max_jc=c
            f1=F1_score(set(list(itertools.chain(*gt_comm_dct[c_star]))), set(list(itertools.chain(*comm_dct[c]))))
            if f1>max_f:
                max_f=f1
                max_fc=c
        f.write(str(c_star) + '\t' + str(max_jc) + '\t' + str(max_j) + '\t' + str(max_f) + '\n')
        sum_j+=max_j
        sum_f+=max_f

match_j_1 = sum_j/(2*num_gt)
match_f_1 = sum_f/(2*num_gt)

sum_j=0
sum_f=0
with open(sys.argv[2] + '_' + sys.argv[1] + '_sim_line','w') as f:
    for c in comm_dct:
        max_j=0
        max_f=0
        for c_star in gt_comm_dct:
            ji=compute_jaccard_index(set(list(itertools.chain(*gt_comm_dct[c_star]))), set(list(itertools.chain(*comm_dct[c]))))
            if ji>max_j:
                max_j=ji
                max_jc=c_star
            f1=F1_score(set(list(itertools.chain(*gt_comm_dct[c_star]))), set(list(itertools.chain(*comm_dct[c]))))
            if f1>max_f:
                max_f=f1
                max_fc=c_star
        f.write(str(c) + '\t' + str(max_jc) + '\t' + str(max_j) + '\t' + str(max_f) +'\n')
        sum_j+=max_j
        sum_f+=max_f

match_j_2 = sum_j/(2*num_comm)
match_f_2 = sum_f/(2*num_comm)

match_j=match_j_1 + match_j_2
match_f=match_f_1 + match_f_2
"""
print("Jaccardi similarity is:")
print(match_j)
print('\n')
print("F1 Score similarity is: ")
print(match_f)
"""
print "Jaccardi similarity is:"
print match_j
print"F1 Score similarity is: "
print match_f

# print(f1_score(gt_comm_dct[c_star], comm_dct[c], average='weighted'))

# we have dictionary for the grountd thruth gt_comm_dct and obtained comm_dct