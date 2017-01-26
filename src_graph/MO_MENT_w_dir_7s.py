#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	go through user tweets, collect counts per edge (userA --> userB) and 
	save to a json file { (userA, userB) :  5:x5, 6:x6, ..., 11:x11}
"""
from collections import defaultdict
import codecs
import os
import datetime
import json

IN_DIR = "../../../DATA/General/"
os.chdir(IN_DIR)

F_IN = "usrs_with_more_than_20_tweets.dat"
F_OUT = "_MENT_weight_dir_self_loops"

MONTHS =  ["5", "6", "7", "8", "9", "10", "11"]

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

def extract_MO_edges_w_dir():

	user_monthly_mention = defaultdict(dict)
	cnt_all_tweets = 0
	user_ids = read_user_IDs()
	cnt_mess = 0

	with codecs.open(F_IN,'r', encoding='utf8') as input_file:
		# the code loops through the input, collects tweets text for each user into a dict
		for line in input_file:	
			cnt_all_tweets += 1
			line = line.split()
			userA = line[0]
			userB = line[1]
			if userA not in user_ids or userB not in user_ids:
				cnt_mess += 1
				continue
			userA = user_ids[userA]
			userB = user_ids[userB]
			edge = (userA, userB)
			if edge not in user_monthly_mention:
				user_monthly_mention[edge] = {'5':0, '6':0, '7':0, '8':0, '9':0, '10':0, '11':0}
			UTS = long(line[4])
			month = datetime.datetime.utcfromtimestamp(UTS).month
			user_monthly_mention[edge][str(month)] += 1
			if cnt_all_tweets % 100000 == 0:
				print cnt_all_tweets, line
	print "Processed %d tweets, and removed %d considered to be mess (no ids for them)" % (cnt_all_tweets, cnt_mess)
	print "Total edges %d in the dict " % len(user_monthly_mention)

	output_file = defaultdict(int)

	for MO in MONTHS:
		output_file[MO] = open(MO + F_OUT, 'w')

	for edge in user_monthly_mention:
		for MO in user_monthly_mention[edge]:
			w = user_monthly_mention[edge][MO]
			if  w > 0:
				u1 = edge[0]
				u2 = edge[1]
				output_file[MO].write(str(u1) + '\t' + str(u2) + '\t' + str(w) + '\n' )

extract_MO_edges_w_dir()
	









