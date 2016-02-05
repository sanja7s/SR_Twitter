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
f_out_id = "graph_20_tweets_IDs_with_SR.dat"
f_out_u = "graph_20_tweets_usr_with_SR.dat"
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
		CVA = USER_CVs[userA]["CV"]
		CVB = USER_CVs[userB]["CV"]
		SR = cosine_2_vectors(CVA, CVB)
		f_out_users.write(str(userA) + '\t' + str(userB) + '\t' + str(SR) + '\n')
		f_out_IDs.write(str(user_ids[userA]) + '\t' + str(user_ids[userB]) + '\t' + str(SR) + '\n')
		
		cnt += 1
		if cnt % 1000000 == 0:
			print ":) we have ", cnt, " user pairs SR calculated"
	


def main():
	os.chdir(IN_DIR) 
	mention_usr_SR()

main()

