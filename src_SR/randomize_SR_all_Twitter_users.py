#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
	we want to make sure that our SR network behavior in terms of degree assortativity is not accident
	for that reason, we will mix (randomize) the CV vectors input and calculate new "SR values"
	with which we can recalculate "random" SR networs and see their behavior  
"""

from collections import defaultdict
import math
import json
import numpy as np
import glob, os
import time
import random
#####################################################
# input
#####################################################
WORKING_FOLDER = "../../../DATA/CV/"

F_IN = "CVs_usrs.json"

F_OUT_v1 = "randomize_" + F_IN
#####################################################
F_OUT_v2 = "scaled_randomize_v27s_" + F_IN


# for a faster processing for all user pairs, we do not want to query MongoDB for the text 
# more than once for one user; so here we read in all the precaclculated user CVs.
def read_all_user_CVs():

	user_CVs = defaultdict(int)
	#raw_CVs = defaultdict(int)
	cnt = 0

	with open(F_IN) as f:
	    for line in f:
	        line_dict = json.loads(line)
	        usr = line_dict["_id"]
	        user_CVs[cnt] = {}
	        user_CVs[cnt]["num_tweets"] = line_dict["num_tweets"]
	        CVa = line_dict["CV"]
	        user_CVs[cnt]["CV"] = { k: v for d in CVa for k, v in d.items() }
	        #raw_CVs[cnt] = { k: v for d in CVa for k, v in d.items() }
	        if cnt % 1000 == 0:
	        	print cnt, usr
	        cnt += 1

	return user_CVs #, raw_CVs


# the same as above, just scale the CVs for each user by the number of tweets
def read_all_user_CVs_v2():

	user_CVs = defaultdict(int)
	cnt = 0

	with open(F_IN) as f:
	    for line in f:
	        line_dict = json.loads(line)
	        usr = line_dict["_id"]
	        user_CVs[cnt] = {}
	        user_CVs[cnt]["num_tweets"] = line_dict["num_tweets"]
	        scale_factor_num_tweets = float(user_CVs[cnt]["num_tweets"])
	        CVa = line_dict["CV"]
	        user_CVs[cnt]["CV"] = { k: float(v)/scale_factor_num_tweets for d in CVa for k, v in d.items() }
	        if cnt % 1000 == 0:
	        	print cnt, usr
	        cnt += 1

	return user_CVs 

########################################################
#	v1 randomize outputs a json valid for this save function
########################################################
def save_CVs(CVs, F_OUT):

	f = open(F_OUT, 'w')

	for usr in CVs:
		cv_line = {}
		cv_line["_id"] = str(usr)
		cv_line["CV"] = [ {k:v} for k,v in CVs[usr]["CV"].items()]
		cv_line["num_tweets"] = CVs[usr]["num_tweets"]
		f.write(unicode(json.dumps(cv_line, ensure_ascii=False)) + '\n')

########################################################
#	v1 randomzies only the user ids in the dicitonary
#	basically assigning the same CVs to shuffled user ids
########################################################
def randomize_v1():
	
	randomized_user_CVs = defaultdict(int)

	user_CVs = read_all_user_CVs()

	SHUFFLE_USERS =  user_CVs.keys()
	#print SHUFFLE_USERS
	random.shuffle(SHUFFLE_USERS)
	#print SHUFFLE_USERS

	for k in range(len(SHUFFLE_USERS)):
		randomized_user_CVs[SHUFFLE_USERS[k]] = user_CVs[k]

	for k in randomized_user_CVs:
		if randomized_user_CVs[k] == user_CVs[k]:
			print k

	return randomized_user_CVs

########################################################
#	v2 randomzies all the CVs as Aris suggested
#	for a more efficient structure, we use numpy matrix to do the shuffle we need
########################################################
def randomize_v2():
	# read in the original CVs json that we now want to randomize
	user_CVs = read_all_user_CVs_v2()
	# the output in a format that we can save to a json with save_CVs_v2()
	randomized_user_CVs = defaultdict(int)
	# for working with an np matrix, we need ids in range 0 .. num_of_concepts 
	# to save the TFs and shuffle easily
	conceptID7s = defaultdict(int)
	reverse_conceptID7s = defaultdict(int)
	# let's see what is that num_of_concepts (distinct), 
	# that will be the number of columns in the numpy matrix
	count_all_vectors = defaultdict(int)
	for user in user_CVs:
		for vec in user_CVs[user]["CV"]:
			   count_all_vectors[vec] = 1
	N_all_vec = sum(count_all_vectors.values())
	print "Number of distinct concepts in the data is %d " % N_all_vec
	# for the numpy matrix, we also need the number of users, as the number of rows
	N_users = len(user_CVs)
	# conceptID7s will hold a map: concepts --> IDs, in the range N_all_vec
	i = 0
	for vec in count_all_vectors:
		conceptID7s[vec] = i 
		reverse_conceptID7s[i] = vec
		i += 1

	# finally we can define an np matrix
	# defalut dtype=float64 is NOT OK due to size limit, we'd need 90GB RAM
	shuffled_CVs = np.zeros((N_users,N_all_vec), dtype='float32') 
	# and we can add the CVs in it
	for user in user_CVs:
		CV = user_CVs[user]["CV"]
		for concept in CV:
			concept_id = conceptID7s[concept]
			# shuffled_Cvs will hold concept_id --> TF
			shuffled_CVs[user][concept_id] = CV[concept]
	print "We have copied the CVs to a numpy array for a shufffffle ;) "

	t0 = time.time()
	# and shuffle them finally
	for col_id in range(N_all_vec):
		np.random.shuffle(shuffled_CVs[:,col_id]) 
	print "took %.3f seconds " % (time.time() - t0)
	print "You've got the CVs shuffled, well... "

	t0 = time.time()

	# for each user
	for user in range(N_users):
		# let us assign the desired output in a dict
		randomized_user_CVs[user] = {}
		# first assign the neccesary stuff from eariler
		randomized_user_CVs[user]["num_tweets"] = user_CVs[user]["num_tweets"]
		# next take the new random Cv for that user
		single_CV = shuffled_CVs[user]
		# and properly assign it (select only the nonzero entries from the numpy array)
		randomized_user_CVs[user]["CV"] = { reverse_conceptID7s[k]:str(single_CV[k]) \
		for k in np.nonzero(single_CV)[0] }

		#randomized_user_CVs[user]["CV"] = [ {reverse_conceptID7s[k]:single_CV[k]} \
		#for k in np.nonzero(single_CV)[0] ]

	print "took %.3f seconds " % (time.time() - t0)
	print "You've got the data ready for saving to .json, cool stuff ;) "

	return randomized_user_CVs
	

def randomize_and_save_v1():
	randomized_user_CVs = randomize_v1()
	print "Data shuffled per user V1 :)"
	save_CVs(randomized_user_CVs, F_OUT_v1)
	print "Shuffled CVs V1 saved in %s :)" % F_OUT_v1

def randomize_and_save_v2():
	randomized_user_CVs = randomize_v2()
	print "Data shuffled per column V2 :)"
	save_CVs(randomized_user_CVs, F_OUT_v2)
	print "Shuffled CVs V2 saved in %s :)" % F_OUT_v2

def main():

	os.chdir(WORKING_FOLDER)
	#randomize_and_save_v1()
	randomize_and_save_v2()

main()

