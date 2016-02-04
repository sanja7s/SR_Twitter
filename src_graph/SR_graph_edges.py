#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pymongo
from pymongo import MongoClient
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict, OrderedDict
import math
import codecs
import SR_2_Twitter_users as SR2
STEMMER = SnowballStemmer("english", ignore_stopwords=True )

f_in = "graph_data_100K.tab"
f_out = "graph_data_with_SR_100K.tab"

def read_in_graph_data(f_in):
	usr_data = defaultdict(int)
	with codecs.open(f_in,'r', encoding='utf8') as input_file:
		for line in input_file:
			line = line.split()
			usr1 = line[0]
			usr2 = line[1]
			weight = line[2]
			usr_data[(usr1, usr2)] = weight
	return usr_data

def calculate_edges_SR():
	usr_data = read_in_graph_data(f_in)
	usr_data_with_SR = defaultdict(int)
	for e in usr_data.iterkeys():
		usr1 = e[0]
		usr2 = e[1]
		weight = usr_data[(usr1, usr2)]
		usr_data_with_SR[(usr1, usr2)] = (weight, SR2.SR_2_users(usr1, usr2))
		print usr1, usr2, weight, usr_data_with_SR[(usr1, usr2)]
	return usr_data_with_SR


def save_weighted_edges_SR(f_out):
	usr_data_with_SR = calculate_edges_SR()
	with codecs.open(f_out,'w', encoding='utf8') as output_file:
		for key in usr_data_with_SR:
			usr1 = key[0]
			usr2 = key[1]
			output_file.write(str(usr1) + '\t' + str(usr2) + '\t' + str(usr_data_with_SR[key][0]) + '\t' + str(usr_data_with_SR[key][1]) +  '\n')

save_weighted_edges_SR(f_out)