#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import codecs
import glob, os
from collections import defaultdict
import json


f_out = "missing_users.tab"
in_dir = "taxonomy/"
f_in = "user_IDs.dat"

def read_user_IDs():

	user_ids = defaultdict(str)

	with codecs.open(f_in,'r', encoding='utf8') as f:
		for line in f:
			line = line.split()
			user_id = line[0]
			user =  line[1]
			user_ids[user] = user_id

	return user_ids


def check_missing_and_save():

	user_ids = read_user_IDs()
	found_users = defaultdict(int)

	with codecs.open(f_out,'w', encoding='utf8') as output_file:
		cnt = 0
		for f_in in glob.glob("*.json"):
			print(f_in)
			with codecs.open(f_in,'r', encoding='utf8') as input_file:
				# the code loops through the input, collects taxonomies per user
				for line7s in input_file: 
					if line7s.strip() == "null":
						continue
					#print line7s
					cnt += 1
					if cnt % 10000 == 0:
						print('Processing users: ', cnt)
					line = json.loads(line7s)
					user = line["_id"]
					found_users[user] = 1

		print "Found ", len(found_users.keys())

		for user in user_ids.keys():
			if user not in found_users.keys():
				output_file.write(str(user_ids[user]) + '\t' + user + '\n')

	print("Read ALL users: ", cnt)



def main():

	os.chdir(in_dir)
	check_missing_and_save()

main()