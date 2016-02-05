	#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import defaultdict
import math
import json
import codecs
import glob, os

f_in_IDs = "user_IDs.dat"
f_in_CVs = "CV_usrs.json"
f_in = "graph_20_tweets_users.dat"
f_out_id = "mention_graph_IDs_with_SR_weight.dat"
f_in_SR_weight = "mention_graph_IDs_with_SR_weight.dat"
f_out_u = "mention_graph_with_SR_weight.dat"
f_out_undirected = "undirected_mention_graph_with_SR_weight_v2.dat"
IN_DIR = "../DATA/mention_graph"


def read_user_IDs():

	user_ids = defaultdict(str)

	with codecs.open(f_in_IDs,'r', encoding='utf8') as f:
		for line in f:
			line = line.split()
			user_id = line[0]
			user =  line[1]
			user_ids[user] = user_id

	return user_ids


# given two vectors as dictionaries with *ANY* sets of keys
# return their cosine similarity *vectors may be of ANY dim*
# cosine sim (v1,v2) = v1.v2 / ||v1|| ||v2||
def cosine_2_vectors(v1, v2):
	# numerator for the cosine formula 
	SR_num = 0.0
	# two denominator terms in the formula
	v1_sq_sum = 0.0
	v2_sq_sum = 0.0
	keys_1 = set(v1.keys())
	#print len(keys_1)
	keys_2 = set(v2.keys())
	#print len(keys_2)
	# separate the different keys and common keys
	different2_keys = keys_2 - keys_1
	different1_keys = keys_1 - keys_2
	common_keys = keys_1 & keys_2
	#print len(common_keys), common_keys
	# for common keys, we calculate formula as is
	# SR = v1.v2 / ||v1|| ||v2||
	for term in common_keys:
		v1_fq = float(v1[term])
		v2_fq = float(v2[term])
		SR_num += v1_fq * v2_fq
		v1_sq_sum += v1_fq * v1_fq
		v2_sq_sum += v2_fq * v2_fq
	# for different keys, we just take resepective non-zero 
	# dict terms for calculating denominator (nominator is zero)
	for term in different1_keys:
		v1_fq = float(v1[term])
		v1_sq_sum += v1_fq * v1_fq
	for term in different2_keys:
		v2_fq = float(v2[term])
		v2_sq_sum += v2_fq * v2_fq
	# sum all in denominator and sqrt in the end
	SR_den = math.sqrt(v1_sq_sum*v2_sq_sum)
	try:
		SR = SR_num/SR_den
	except ZeroDivisionError:
		SR = 0
	return SR

# for a faster processing for all user pairs, we do not want to query MongoDB for the text 
# more than once for one user; so here we read in all the precaclculated user CVs.
def read_all_user_CVs():

	user_CVs = defaultdict(int)
	cnt = 0

	with open(f_in_CVs) as f:
	    for line in f:
	        line_dict = json.loads(line)
	        usr = line_dict["_id"]
	        user_CVs[usr] = {}
	        user_CVs[usr]["num_tweets"] = line_dict["num_tweets"]
	        CVa = line_dict["CV"]
	        user_CVs[usr]["CV"] = { k: v for d in CVa for k, v in d.items() }
	        if cnt % 10000 == 0:
	        	print cnt, usr
	        cnt += 1

	return user_CVs


def mention_usr_SR():

	user_ids = read_user_IDs()
	USER_CVs = read_all_user_CVs()

	f_out_users = open(f_out_u, "w")
	f_out_IDs = open(f_out_id, "w")

	input_file = open(f_in, "r") 

	cnt = 0

	for line in input_file:
		line = line.split()
		userA = line[0]
		userB = line[1]
		weight = line[2]
		CVA = USER_CVs[userA]["CV"]
		CVB = USER_CVs[userB]["CV"]
		SR = cosine_2_vectors(CVA, CVB)
		#f_out_users.write(str(userA) + '\t' + str(userB) + '\t' + str(SR) + '\n')
		#f_out_IDs.write(str(user_ids[userA]) + '\t' + str(user_ids[userB]) + '\t' + str(SR) + '\n')
		f_out_users.write(str(userA) + '\t' + str(userB) + '\t' + str(SR) + '\t' + str(weight) + '\n')
		f_out_IDs.write(str(user_ids[userA]) + '\t' + str(user_ids[userB]) + '\t' + str(SR) + '\t' + str(weight) + '\n')
		
		cnt += 1
		if cnt % 1000000 == 0:
			print ":) we have ", cnt, " user pairs SR calculated"
	

def read_in_graph_with_SR():

	input_file =  open(f_in_SR_weight, "r")
	directed_graph_with_SR = defaultdict(list)

	cnt = 0
	for line in input_file:
		line = line.strip().split("\t")
		id1 = line[0]
		id2 = line[1]
		SR = float(line[2])
		weight = int(line[3])
		directed_graph_with_SR[(id1,id2)] = (weight, SR)
		if cnt == 100:
			print id1, id2, directed_graph_with_SR[(id1,id2)]
		cnt += 1

	return directed_graph_with_SR


def save_undirected_graph_with_SR():
	directed_graph_with_SR = read_in_graph_with_SR()
	undirected_graph_with_SR = defaultdict(list)

	with codecs.open(f_out_undirected,'w', encoding='utf8') as output_file:
		for edge in directed_graph_with_SR.keys():
			w = directed_graph_with_SR[edge][0]
			sr = directed_graph_with_SR[edge][1]
			key2 = tuple(sorted((edge[1],edge[0])))
			if key2 not in undirected_graph_with_SR:
				undirected_graph_with_SR[key2] = (w, sr)
			else:
				old_w = undirected_graph_with_SR[key2][0]
				#sr = undirected_graph_with_SR[key2][1]
				undirected_graph_with_SR[key2] = (w + old_w, sr)
				#print key2, w, old_w, sr
				output_file.write(str(edge[0]) + '\t' + str(edge[1]) + '\t' + str(w + old_w) + '\t' + str(sr) + '\n')


def main():
	os.chdir(IN_DIR) 
	#mention_usr_SR()
	save_undirected_graph_with_SR()

main()

