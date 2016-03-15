#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	extract sentiment for each user, as a label (0,1,-1) and value
'''
import codecs
from collections import defaultdict, OrderedDict
import json
import glob, os

f_in = "tweets_taxonomy_clean.JSON"
f_in_user_ids = "user_IDs.dat"
IN_DIR = "../../../DATA/taxonomy_stats/"
OUT_DIR = "sentiment/"
f_out = "user_sentiment.tab"

##################################################
# read in a map for the twitter username --> id
##################################################
def read_user_IDs():

	user_ids = defaultdict(str)

	with codecs.open(f_in_user_ids,'r', encoding='utf8') as f:
		for line in f:
			line = line.split()
			user_id = line[0]
			user =  line[1]
			user_ids[user] = user_id

	return user_ids

##################################################
# the main function
##################################################
"""
	go through taxon file and extract and save user sentiment
"""
def main():

	os.chdir(IN_DIR)

	# resulting dictionary in which the counts and tfidf relevance are collected
	docSentiment_sum = defaultdict(int)
	# holds all the user ids
	user_ids = read_user_IDs()

	output_file = codecs.open(OUT_DIR+f_out, 'w', encoding='utf8')

	cnt = 0
	with codecs.open(f_in,'r', encoding='utf8') as input_file:
		for line7s in input_file:
			try:
				line = json.loads(line7s)
				taxonomy_all = line["taxonomy"]
				user_name = line["_id"]
				user_id = user_ids[user_name]
				docSentiment = taxonomy_all["docSentiment"] 
				# this counts how many user we have analyzed
				cnt += 1
			except KeyError:
				#print line7s
				# we don't print since it is tested, there some 10% users for whom
				# the taxonomy was not successfuly downloaded and they would be listed here
				continue

			# procedure for extracting the sentiment
			sentiment = docSentiment["type"]
			if sentiment == "neutral":
				snt = "0"
				score = "0"
			elif sentiment == "positive":
				snt = "1"
				score = docSentiment["score"]
			else:
				snt = "-1"
				score = docSentiment["score"]
			output_file.write(str(user_id) + '\t' + str(snt) + '\t' + str(score) +  '\n')
###############################################################################


main()
