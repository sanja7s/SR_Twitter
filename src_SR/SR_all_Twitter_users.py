#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import defaultdict
import math
import multiprocessing
from multiprocessing import Pool
from itertools import repeat
import json
#from stemming.porter2 import stem
import numpy as np
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager, DictProxy

N_PROCESSES = multiprocessing.cpu_count()
RESULTS = []


#f_in = "usrs_with_more_than_20_tweets_COPY.dat"
f_in = "CV_usrs_v2.json"
#f_out = "more_usr_pairs_SR_v2.dat"
#f_out2 = "more_usr_pairs_SR_FILTERED_v2.dat"

class MyManager(BaseManager):
    pass

MyManager.register('defaultdict', defaultdict, DictProxy)

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
def read_all_user_CVs(f_in):

	user_CVs = defaultdict(int)
	user_ids = defaultdict(int)
	cnt = 0

	with open(f_in) as f:
	    for line in f:
	        line_dict = json.loads(line)
	        usr = line_dict["_id"]
	        user_ids[cnt] = usr
	        user_CVs[usr] = {}
	        user_CVs[usr]["num_tweets"] = line_dict["num_tweets"]
	        CVa = line_dict["CV"]
	        user_CVs[usr]["CV"] = { k: v for d in CVa for k, v in d.items() }
	        if cnt % 10000 == 0:
	        	print cnt, usr
	        cnt += 1

	return user_CVs, user_ids

# for all the users who are found to have more than threshold_tweets=20,
# find their SR and save in a file
def all_usr_SR(NUM_USR, DIVIDE_USERS, USER_IDs, USER_CVs, c):
	#SR_dict = defaultdict(int)
	f_name_out = "ALL_SR/all_user_SR_part_" + str(c)
	f_name_out_filter = "ALL_SR/filter_user_SR_part_" + str(c)
	f_out_c_filter = open(f_name_out_filter, "w")

	with open(f_name_out, "w") as f_out_c:
		cnt = 0
		start_of_range = c * DIVIDE_USERS
		e = start_of_range + DIVIDE_USERS 
		eof_range = e if e < NUM_USR else NUM_USR-1
		print "Process %d for the range %d to %d " % (c, start_of_range, eof_range)
		for i in xrange(start_of_range, eof_range):
			for j in xrange (i+1,NUM_USR,1):
				userA = USER_IDs[i]
				userB = USER_IDs[j]
				CVA = USER_CVs[userA]["CV"]
				CVB = USER_CVs[userB]["CV"]
				SR = cosine_2_vectors(CVA, CVB)
				f_out_c.write(str(userA) + '\t' + str(userB) + '\t' + str(SR) + '\n')
				if float(SR) > 0.2:
					f_out_c_filter.write(str(userA) + '\t' + str(userB) + '\t' + str(SR) + '\n')
				#SR_dict[(userA,userB)] = SR
				cnt += 1
				if cnt % 1000000 == 0:
					print ":) we have ", cnt, " user pairs SR calculated "
					#print "Example SR ", SR
					#return
	return
	

def func((data, i)):
    return all_usr_SR(data[0],data[1],data[2],data[3],i)

def main():
	# for testing the speed
	#from meliae import scanner
	print 'cpu_count() = %d\n' % N_PROCESSES

	MGR = MyManager()
	MGR.start()
	
	# from previous step we calculated the CVs for each user. Read in the whole file, it is 500MB only
	# we need user_ids to divide users into groups and process each in one process
	USER_CVs1, USER_IDs1 = read_all_user_CVs(f_in)

	USER_CVs = MGR.defaultdict(int)

	#SR_dict = MGR.defaultdict(int)

	for usr in USER_CVs1.iterkeys():
		USER_CVs[usr] = USER_CVs1[usr]

	USER_IDs = MGR.defaultdict(int)

	for el in USER_IDs1.iterkeys():
		USER_IDs[el] = USER_IDs1[el]

	print "Distribute task started."
	p = Pool(processes=N_PROCESSES) 
	# for the results
	#f = open(f_out, 'w')
	#f2 = open(f_out2, 'w')

	# number of users for whom we have CV calculated
	NUM_USR = len(USER_IDs.items())
	DIVIDE_USERS = int(math.ceil(NUM_USR/N_PROCESSES))
	print "We have in total %d users" % NUM_USR
	# number of user pairs = n*(n-1)/2

	params_tuple = (NUM_USR, DIVIDE_USERS, USER_IDs, USER_CVs)
	params = zip(repeat(params_tuple), range(N_PROCESSES))
	p.map(func, params) 


	print "Distribute task finished."


	print "Data saved :)"

#import cProfile
#cProfile.run('main()')
#command = """main()"""
#cProfile.runctx( command, globals(), locals(), filename="OpenGLContext_SR_more_Twitter_usr.profile" )
main()

