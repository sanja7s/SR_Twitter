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
import os, codecs

MO = "8"

# where we work
IN_DIR = "../../../DATA/General/"

N_PROCESSES = multiprocessing.cpu_count()
RESULTS = []

f_in = MO + "_CV.json"


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

f_in_user_ids = "user_IDs.dat"
def read_user_IDs():

	user_ids = defaultdict(int)

	with codecs.open(f_in_user_ids,'r', encoding='utf8') as f:
		for line in f:
			line = line.split()
			user_id = line[0]
			user =  line[1]
			user_ids[user] = user_id

	return user_ids

# for a faster processing for all user pairs, we do not want to query MongoDB for the text 
# more than once for one user; so here we read in all the precaclculated user CVs.
def read_all_user_CVs(f_in):

	user_CVs = defaultdict(int)
	user_ids = read_user_IDs()
	cnt = 0

	with open(f_in) as f:
		for line in f:
			line_dict = json.loads(line)
			usr7s = line_dict["_id"]
			#user_ids[cnt] = usr
			usr = user_ids[usr7s]
			user_CVs[usr] = {}
			user_CVs[usr]["num_tweets"] = line_dict["num_tweets"]
			CVa = line_dict["CV"]
			user_CVs[usr]["CV"] = { k: v for d in CVa for k, v in d.items() }
			if cnt % 10000 == 0:
				print cnt, usr, usr7s
			cnt += 1

	return user_CVs, user_ids

# for all the users who are found to have more than threshold_tweets=20,
# find their SR and save in a file
def all_usr_SR(NUM_USR, DIVIDE_USERS, USER_CVs, c):

	f_name_out = MO + "MOSR/" + MO + "_all_user_SR_part_" + str(c)

	with open(f_name_out, "w") as f_out_c:
		cnt = 0
		start_of_range = c * DIVIDE_USERS
		e = start_of_range + DIVIDE_USERS 
		eof_range = e if e < NUM_USR else NUM_USR-1
		print "Process %d for the range %d to %d " % (c, start_of_range, eof_range)
		for i in xrange(start_of_range, eof_range):
			for j in xrange (i+1,NUM_USR,1):
				userA = str(i)
				userB = str(j)
				if userA in USER_CVs and userB in USER_CVs:
					CVA = USER_CVs[userA]["CV"]
					CVB = USER_CVs[userB]["CV"]
					SR = cosine_2_vectors(CVA, CVB)
				else:
					SR = 0.0
				f_out_c.write(str(userA) + '\t' + str(userB) + '\t' + str(SR) + '\n')
				cnt += 1
				if cnt % 1000000 == 0:
					print str(c), " :) we have ", cnt, " user pairs SR calculated "
	

def func((data, i)):
	return all_usr_SR(data[0],data[1],data[2],i)

def main():
	# for testing the speed
	#from meliae import scanner
	print 'cpu_count() = %d\n' % N_PROCESSES

	os.chdir(IN_DIR)

	MGR = MyManager()
	MGR.start()
	
	# from previous step we calculated the CVs for each user. Read in the whole file, it is 500MB only
	# we need user_ids to divide users into groups and process each in one process
	USER_CVs1, USER_IDs = read_all_user_CVs(f_in)

	USER_CVs = MGR.defaultdict(int)

	for usr in USER_CVs1.iterkeys():
		USER_CVs[usr] = USER_CVs1[usr]


	print "Distribute task started."
	p = Pool(processes=N_PROCESSES) 

	# number of users for whom we have CV calculated
	NUM_USR = len(USER_IDs.items())
	DIVIDE_USERS = int(math.ceil(NUM_USR/N_PROCESSES))
	print "We have in total %d users" % NUM_USR
	# number of user pairs = n*(n-1)/2

	params_tuple = (NUM_USR, DIVIDE_USERS, USER_CVs)
	params = zip(repeat(params_tuple), range(N_PROCESSES))
	p.map(func, params) 


	print "Distribute task finished."


	print "Data saved :)"

#import cProfile
#cProfile.run('main()')
#command = """main()"""
#cProfile.runctx( command, globals(), locals(), filename="OpenGLContext_SR_more_Twitter_usr.profile" )
main()

