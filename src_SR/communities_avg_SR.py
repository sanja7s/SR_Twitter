#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
	Given a set of communities, find average SR for the user pairs inside (not just those connected)
"""

import codecs
from collections import defaultdict
import json
import glob, os
import math
import numpy as np
import random

f_in = "CV_usrs.json"
f_in_user_ids = "user_IDs.dat"
IN_DIR = "../../../DATA/taxonomy_stats"
# the communities we analyze (from the mention graph)
spec_users = "mention/communitiesMent.txt"
f_in_mention_graph = "mention_graph_weights.dat"

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

#
# all the user ids (id map)
#
def read_user_IDs():

	user_ids = defaultdict(str)

	with codecs.open(f_in_user_ids,'r', encoding='utf8') as f:
		for line in f:
			line = line.split()
			user_id = int(line[0])
			user =  line[1]
			user_ids[user] = user_id

	return user_ids

#
# all the user ids (id map)
#
def read_in_mention_graph():

	edge_list = defaultdict(str)

	with codecs.open(f_in_mention_graph,'r', encoding='utf8') as f:
		for line in f:
			(user1, user2, weight) = line.split()
			if int(user1) > int(user2):
				edge_list[(int(user1), int(user2))] = float(weight)

	print 'Mention edges ', len(edge_list)

	return edge_list

# to return top sizeN communities, as many as there are
# in a form of a dictionary: {community_id: defaultdict{id_usr1:1, id_usr2:1, ...}}
# and also another dict, as a map (res3) to tell us the community id of a user
# and finally the whole set of communities (not limited in size) and similar map in res4
def read_in_communities(sizeN=20):

	res = defaultdict(int)
	res7s = defaultdict(int)
	res3 = defaultdict(int)
	res3 = defaultdict(lambda: -1, res3)
	res4 = defaultdict(int)
	res4 = defaultdict(lambda: -1, res4)

	f = open(spec_users, "r")

	for line in f:
		line = line.split()
		user_id = int(line[0])
		com_id = line[1]
		if com_id not in res:
			res[com_id] = defaultdict(int)
		res[com_id][user_id] = 1

	for com in res:
		if len(res[com]) >= sizeN:
			res7s[com] = res[com]
			for usr in res[com]:
				res4[usr] = com

	for com in res7s:
		for usr in res7s[com]:
			res3[usr] = com

	return res7s, res3, res, res4

# for a faster processing for all user pairs, we do not want to query MongoDB for the text 
# more than once for one user; so here we read in all the precaclculated user CVs.
def read_all_user_CVs():

	user_CVs = defaultdict(int)
	user_ids = read_user_IDs()
	cnt = 0

	with open(f_in) as f:
	    for line in f:
	        line_dict = json.loads(line)
	        usr = line_dict["_id"]
	        #user_ids[cnt] = usr
	        usr_id = int(user_ids[usr])
	        usr = cnt
	        assert usr == usr_id
	        user_CVs[usr] = {}
	        user_CVs[usr]["num_tweets"] = line_dict["num_tweets"]
	        CVa = line_dict["CV"]
	        user_CVs[usr]["CV"] = { k: v for d in CVa for k, v in d.items() }
	        if cnt % 10000 == 0:
	        	print cnt, usr
	        cnt += 1

	return user_CVs

def find_COMM_avg_SR_full(comm_id, comm_user_list, f, USER_CVs):

	COM_SR = []

	for userA in comm_user_list:
		for userB in comm_user_list:
			if userA < userB:
				CVA = USER_CVs[userA]["CV"]
				CVB = USER_CVs[userB]["CV"]
				SR = cosine_2_vectors(CVA, CVB)
				COM_SR.append(SR)


	COM_SR = np.array(COM_SR)
	
	comm_avg = np.mean(COM_SR)
	comm_std = np.std(COM_SR)

	print 'Comm %s of size %d analyzed for %d edges' % (comm_id, len(comm_user_list), COM_SR.size)
	print comm_id, comm_avg, comm_std

	f.write(str(comm_id) + '\t' + str(comm_avg) + '\t' + str(comm_std) + '\n')


########################################################################################

def COMM_avg_SR_full(comm_id, comm_user_list, USER_CVs):

	COM_SR = []

	for userA in comm_user_list:
		for userB in comm_user_list:
			if userA < userB:
				CVA = USER_CVs[userA]["CV"]
				CVB = USER_CVs[userB]["CV"]
				SR = cosine_2_vectors(CVA, CVB)
				COM_SR.append(SR)


	COM_SR = np.array(COM_SR)
	
	comm_avg = np.mean(COM_SR)
	comm_std = np.std(COM_SR)

	print 'Comm %s of size %d analyzed for %d edges' % (comm_id, len(comm_user_list), COM_SR.size)
	return comm_avg, comm_std

def COMM_avg_SR_ment(comm_id, comm_user_list, USER_CVs, mention_edges):

	COM_SR = []

	for userA in comm_user_list:
		for userB in comm_user_list:
			if (userA, userB) in mention_edges:
				CVA = USER_CVs[userA]["CV"]
				CVB = USER_CVs[userB]["CV"]
				SR = cosine_2_vectors(CVA, CVB)
				COM_SR.append(SR)

	COM_SR = np.array(COM_SR)
	
	comm_avg = np.mean(COM_SR)
	comm_std = np.std(COM_SR)

	print 'Comm %s of size %d analyzed for %d edges' % (comm_id, len(comm_user_list), COM_SR.size)
	return comm_avg, comm_std

def COMM_avg_SR_full_rnd(comm_id, comm_user_list, USER_CVs, user_ids):

	COM_SR = []
	N = len(comm_user_list)
	rnd_usr_list = random.sample(user_ids.values(), N)

	for userA in rnd_usr_list:
		for userB in rnd_usr_list:
			if userA < userB:
				CVA = USER_CVs[userA]["CV"]
				CVB = USER_CVs[userB]["CV"]
				SR = cosine_2_vectors(CVA, CVB)
				COM_SR.append(SR)

	COM_SR = np.array(COM_SR)
	
	comm_avg = np.mean(COM_SR)
	comm_std = np.std(COM_SR)

	print 'Comm %s of size %d analyzed for %d edges' % (comm_id, N, COM_SR.size)
	return comm_avg, comm_std

def COMM_avg_SR_ment_rnd(comm_id, comm_user_list, USER_CVs, mention_edges, user_ids):

	COM_SR = []
	N = len(comm_user_list)
	rnd_usr_list = random.sample(user_ids.values(), N)

	for userA in rnd_usr_list:
		for userB in rnd_usr_list:
			if (userA, userB) in mention_edges:
				CVA = USER_CVs[userA]["CV"]
				CVB = USER_CVs[userB]["CV"]
				SR = cosine_2_vectors(CVA, CVB)
				COM_SR.append(SR)

	COM_SR = np.array(COM_SR)
	
	comm_avg = np.nanmean(COM_SR)
	comm_std = np.nanstd(COM_SR)

	print 'Comm %s of size %d analyzed for %d edges' % (comm_id, len(comm_user_list), COM_SR.size)
	return comm_avg, comm_std

def find_COMM_avg_SR_ALL(comm_id, comm_user_list, f, USER_CVs, mention_edges, user_ids):

	full_avg, full_std = COMM_avg_SR_full(comm_id, comm_user_list, USER_CVs)
	ment_avg, ment_std = COMM_avg_SR_ment(comm_id, comm_user_list, USER_CVs, mention_edges)

	rnd_full_avg, rnd_full_std = COMM_avg_SR_full_rnd(comm_id, comm_user_list, USER_CVs, user_ids)
	rnd_ment_avg, rnd_ment_std = COMM_avg_SR_ment_rnd(comm_id, comm_user_list, USER_CVs, mention_edges, user_ids)


	f.write(str(comm_id) + '\t' + str(len(comm_user_list)) + '\t' + str(full_avg) + '\t' + str(full_std) +  \
			'\t' + str(ment_avg) + '\t' + str(ment_std) + '\t' + str(rnd_full_avg) +  '\t' + str(rnd_full_std) + \
			'\t' + str(rnd_ment_avg) +  '\t' + str(rnd_ment_std) + '\n')

###
### call the SR avg calculation for all communities
###
def do():

	os.chdir(IN_DIR)
	# number of nodes in a community
	sizeN = 20
	top_communities, top_com_id_map, all_communities, all_com_id_map = read_in_communities(sizeN)
	N = len(top_communities)
	print N, "top communities found"
	NALL = len(all_communities)
	print NALL, "all communities found"

	USER_CVs =  read_all_user_CVs()

	f_out_name = "AVG_SR_MENT_COMM/mention_COMM_AVG_SR_size_" + str(sizeN) + ".tab"
	with codecs.open(f_out_name, 'w') as output_file:
		for com in top_communities:
			#print com, type(top_communities)
			find_COMM_avg_SR_full(com, top_communities[com], output_file, USER_CVs)	
#do()

def do_all():

	os.chdir(IN_DIR)
	# number of nodes in a community
	sizeN = 20
	top_communities, top_com_id_map, all_communities, all_com_id_map = read_in_communities(sizeN)
	N = len(top_communities)
	print N, "top communities found"
	NALL = len(all_communities)
	print NALL, "all communities found"

	USER_CVs =  read_all_user_CVs()
	mention_edges = read_in_mention_graph()
	user_ids = read_user_IDs()

	f_out_name = "AVG_SR_MENT_COMM/mention_COMM_AVG_SR_ALL_size_" + str(sizeN) + "_v2.tab"
	with codecs.open(f_out_name, 'w') as output_file:
		for com in top_communities:
			#print com, type(top_communities)
			find_COMM_avg_SR_ALL(com, top_communities[com], output_file, USER_CVs, mention_edges, user_ids)

	
do_all()