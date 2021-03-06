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
f_out_sent = "user_sent.tab"
f_out_taxon = "user_taxons.tab"
f_out_concepts = "user_concepts.tab"
f_out_entities = "user_entities.tab"
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
	go through taxon file and extract and save user sent
"""
def extract_usr_sentiment():

	os.chdir(IN_DIR)

	# resulting dictionary in which the counts and tfidf relevance are collected
	docSentiment_sum = defaultdict(int)
	# holds all the user ids
	user_ids = read_user_IDs()

	output_file = codecs.open(OUT_DIR+f_out_sent, 'w', encoding='utf8')

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

					s = taxonomies_sum
					# go until the last element; on the last, we will not create a dict NONO
					for tax_class in taxonomy_tree:
						#print tax_class
						if tax_class not in s.keys():
							s[tax_class] = defaultdict(int)
							#print taxonomies_sum
							#return
						s = s[tax_class]
					#last_tax_class = taxonomy_tree[levels-1]
					#s = s[last_tax_class]

					old_score = s["size"]
					#old_cnt = s[tax_class][1]
					#old_sent = s[tax_class][2]
					new_score = old_score + float(el["score"])
					s["size"] = new_score
					# this shows that it takes as confident only those above 0.4
					if float(el["score"]) < 0.4:
						print float(el["score"])
					output_file.write(str(user_id) + '\t' + str(snt) + '\t' + str(score) +  '\n')

					cnt += 1

			except KeyError:
				#print line7s
				# we don't print since it is tested, there some 10% users for whom
				# the taxonomy was not successfuly downloaded and they would be listed here
				continue

	print "Saved sentiment for %d users " % (cnt)

###############################################################################

"""
	go through taxon file and extract and save user taxons: diversity 1
	number of top level taxons in user tweets
"""
def extract_usr_taxonomies():
	os.chdir(IN_DIR)
	# resulting dictionary in which the counts and tfidf relevance are collected
	res = defaultdict(int)
	# holds all the user ids
	user_ids = read_user_IDs()

	output_file = codecs.open(OUT_DIR+f_out_taxon, 'w', encoding='utf8')

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

					res[user_id][taxonomy_tree[0]] = 1


				output_file.write(str(user_id) + '\t' + str(len(res[user_id])) + '\n')

				cnt += 1

			except KeyError:
				#print line7s
				# we don't print since it is tested, there some 10% users for whom
				# the taxonomy was not successfuly downloaded and they would be listed here
				continue

	print "Taxon saved for %d users " % (cnt)
###############################################################################


"""
	go through taxon file and extract and save user concepts
"""
def extract_usr_concepts():
	os.chdir(IN_DIR)
	# resulting dictionary in which the counts and tfidf relevance are collected
	res = defaultdict(int)
	# holds all the user ids
	user_ids = read_user_IDs()

	output_file = codecs.open(OUT_DIR+f_out_concepts, 'w', encoding='utf8')

	cnt = 0
	with codecs.open(f_in,'r', encoding='utf8') as input_file:
		for line7s in input_file:
			try:
				line = json.loads(line7s)
				taxonomy_all = line["taxonomy"]
				user_name = line["_id"]
				user_id = user_ids[user_name]
				concepts = taxonomy_all["concepts"] 
				docSentiment = taxonomy_all["docSentiment"] 
				# the user we analyze
				user_name = line["_id"]
				user_id = user_ids[user_name]
				res[user_id] = defaultdict(int)
				# procedure for extracting the concepts


				for el in concepts:
					concept = el["text"]
					res[user_id][concept] = 1

				output_file.write(str(user_id) + '\t' + str(len(res[user_id])) + '\n')

				cnt += 1

			except KeyError:
				#print line7s
				# we don't print since it is tested, there some 10% users for whom
				# the taxonomy was not successfuly downloaded and they would be listed here
				continue

	print "Concepts saved for %d users " % (cnt)

"""
	go through taxon file and extract and save user entities
"""
def extract_usr_entities():
	os.chdir(IN_DIR)
	# resulting dictionary in which the counts and tfidf relevance are collected
	res = defaultdict(int)
	# holds all the user ids
	user_ids = read_user_IDs()

	output_file = codecs.open(OUT_DIR+f_out_entities, 'w', encoding='utf8')

	cnt = 0
	with codecs.open(f_in,'r', encoding='utf8') as input_file:
		for line7s in input_file:
			try:
				line = json.loads(line7s)
				taxonomy_all = line["taxonomy"]
				user_name = line["_id"]
				user_id = user_ids[user_name]
				entities = taxonomy_all["entities"]
				docSentiment = taxonomy_all["docSentiment"] 
				# the user we analyze
				user_name = line["_id"]
				user_id = user_ids[user_name]
				res[user_id] = defaultdict(int)
				# procedure for extracting the entities
				for el in entities:
					entity = el["text"]
					res[user_id][entity] = 1

				output_file.write(str(user_id) + '\t' + str(len(res[user_id])) + '\n')

				cnt += 1

			except KeyError:
				#print line7s
				# we don't print since it is tested, there some 10% users for whom
				# the taxonomy was not successfuly downloaded and they would be listed here
				continue

	print "Concepts saved for %d users " % (cnt)

#extract_usr_taxonomies()
#extract_usr_concepts()
extract_usr_entities()