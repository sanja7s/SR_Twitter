#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	extract top taxons for each user:
	movies
	music
	sex
	humor
	school
'''
import codecs
from collections import defaultdict, OrderedDict
import json
import glob, os

f_in = "tweets_taxonomy_clean.JSON"
f_in_user_ids = "user_IDs.dat"
IN_DIR = "../../../DATA/taxonomy_stats/"
OUT_DIR = "user_taxons/"
f_out_topics = "user_score_for_top_topics.tab"
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

###############################################################################
"""
	go through taxon file and extract users scores for top topics
	movies
	music
	sex
	humor
	school
"""
###############################################################################
def extract_usr_topics_score():
	os.chdir(IN_DIR)
	# resulting dictionary in which the counts and tfidf relevance are collected
	res = defaultdict(int)
	# holds all the user ids
	user_ids = read_user_IDs()

	output_file = codecs.open(OUT_DIR+f_out_topics, 'w', encoding='utf8')

	cnt = 0
	with codecs.open(f_in,'r', encoding='utf8') as input_file:
		for line7s in input_file:
			try:
				line = json.loads(line7s)
				taxonomy_all = line["taxonomy"]
				user_name = line["_id"]
				user_id = user_ids[user_name]
				taxonomy = taxonomy_all["taxonomy"]
				docSentiment = taxonomy_all["docSentiment"] 
				# the user we analyze
				user_name = line["_id"]
				user_id = user_ids[user_name]
				res[user_id] = defaultdict(int)
				# procedure for extracting the taxons
				for el in taxonomy:
					try:
						if el["confident"] == "no":
							continue
					except: KeyError
					taxonomy_tree = el["label"]
					taxonomy_tree = taxonomy_tree.split("/")
					taxonomy_tree.pop(0)
					levels = len(taxonomy_tree)
					score = float(el["score"])
					if 'music' in taxonomy_tree:
						res[user_id]['music'] += score
					elif 'movies' in taxonomy_tree:
						res[user_id]['movies'] += score
					elif 'sex' in taxonomy_tree:
						res[user_id]['sex'] += score
					elif 'humor' in taxonomy_tree:
						res[user_id]['humor'] += score
					elif 'school' in taxonomy_tree:
						res[user_id]['school'] += score

				output_file.write(str(user_id) + '\t' + str(res[user_id]['music']) + \
				'\t' + str(res[user_id]['movies']) +  \
				'\t' + str(res[user_id]['sex']) +  \
				'\t' + str(res[user_id]['humor']) +  \
				'\t' + str(res[user_id]['school']) +  '\n')

				cnt += 1

			except KeyError:
				#print line7s
				# we don't print since it is tested, there some 10% users for whom
				# the taxonomy was not successfuly downloaded and they would be listed here
				continue

	print "Topics saved for %d users " % (cnt)
###############################################################################

extract_usr_topics_score()