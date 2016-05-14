#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	Given the taxonomy output from AlchemyAPI, for each level of taxonomies, extract the graph
	so that the taxons in this level are connected based on
	***Jaccardi score*** for the users sharing these taxons in their tweets
"""

import codecs
from collections import defaultdict, OrderedDict
import json
import re
import glob, os
import math
import itertools

f_in = "tweets_taxonomy_clean.JSON"
#f_in = "testme"
f_in_user_ids = "user_IDs.dat"
IN_DIR = "../../../DATA/taxonomy_stats"

#
# taxonomy has user names and we need ids
#
def read_user_IDs():

	user_ids = defaultdict(str)

	with codecs.open(f_in_user_ids,'r', encoding='utf8') as f:
		for line in f:
			line = line.split()
			user_id = line[0]
			user =  line[1]
			user_ids[user] = user_id

	return user_ids

#
# go through taxonomy file and save the co-ccurence networks on 
#  different levels of taxonomy 
#
def read_save_taxonomy_graph():

	docSentiment_sum = defaultdict(int) 

	taxonomies_sum = [defaultdict(list)]*5
	# One needs to be careful with this dedinition of dict
	# the code works without those 5 lines below, but it
	# creates a copies of the data in one dict, instead of 5 different ones
	# as i would expect!!!
	taxonomies_sum[0] = defaultdict(list)
	taxonomies_sum[1] = defaultdict(list)
	taxonomies_sum[2] = defaultdict(list)
	taxonomies_sum[3] = defaultdict(list)
	taxonomies_sum[4] = defaultdict(list)

	user_ids = read_user_IDs()
	cnt = 0

	with codecs.open(f_in,'r', encoding='utf8') as input_file:
		for line7s in input_file:
			try:
				line = json.loads(line7s)
				user_name = line["_id"]
				user_id = user_ids[user_name]
				taxonomy_all = line["taxonomy"]
				#keywords = taxonomy_all["keywords"]
				#entities = taxonomy_all["entities"]
				taxonomy = taxonomy_all["taxonomy"] 
				docSentiment = taxonomy_all["docSentiment"] 
				concepts = taxonomy_all["concepts"] 
			except KeyError:
				#print line7s
				continue

			sentiment = docSentiment["type"]
			if sentiment == "neutral":
				docSentiment_sum[sentiment] += 1
			else:
				if not sentiment in docSentiment_sum:
					docSentiment_sum[sentiment] = defaultdict(int)
				old_score = docSentiment_sum[sentiment][0]
				old_cnt = docSentiment_sum[sentiment][1]
				old_mixed_cnt = docSentiment_sum[sentiment][2]
				try:
					new_score = old_score + float(docSentiment["score"])
				except KeyError:
					continue
				new_cnt = old_cnt + 1
				try:
					new_mixed_cnt = old_mixed_cnt + int(docSentiment["mixed"])
				except KeyError:
					continue
				docSentiment_sum[sentiment] = (new_score, new_cnt, new_mixed_cnt)

			# just take taxonomy for which Alchemy is confident
			for el in taxonomy:
				try:
					if el["confident"] == "no":
						continue
				except: KeyError
				taxonomy_tree = el["label"]
				taxonomy_tree = taxonomy_tree.split("/")
				taxonomy_tree.pop(0)
				levels = len(taxonomy_tree)

				# go through the levels, from 0 until max 5
				for i in range(levels):
					tax_class = taxonomy_tree[i]
					# if this is a new user for this taxon: append him
					if user_id not in taxonomies_sum[i][tax_class]:
						taxonomies_sum[i][tax_class].append(user_id)

			cnt += 1

		com_size = cnt
		N = cnt 
		print cnt     
		print 'Total taxons on different levels found ',    len(taxonomies_sum[0]), \
			len(taxonomies_sum[1]),len(taxonomies_sum[2]), \
			len(taxonomies_sum[3]), len(taxonomies_sum[4])
		print "Total Sentiments found ", len(docSentiment_sum)

	for i in range(5):
		f_out_name = "graph/Jaccard/vth20_level_" + str(i) + ".tab"

		# now we record the scores for each taxonomy edge for each of the levels i
		with codecs.open(f_out_name,'w', encoding='utf8') as f: 
			# for an edge (el0, el1) we go through elements of the level twice
			for el0 in taxonomies_sum[i]:
				for el1 in taxonomies_sum[i]:
					# and check that they are different, no self-loops
					if el0 >= el1:
						continue
					# set of users for one taxon and for the other
					set0 = set(taxonomies_sum[i][el0])
					set1 = taxonomies_sum[i][el1]
					# frequency of each element is equal
					# the number of users who talked about it
					# so the lenght of the array of users recorded
					fel0 = len(set0)
					fel1 = len(set1)
					# formula for intersect 
					intersect = len(set0.intersection(set1))
					# let us not record 0 weight edge == no co-occurence
					if intersect < 20:
						continue
					# formula for union
					union = len(set0.union(set1))
					# formula for Jaccard score
					Jaccard = intersect / float(union)
					# write to the file all:
					# taxon1, taxon2, frequency 1, frequency 2, interect, Jaccard score
					f.write(str(el0) + "\t" + str(el1) + "\t" \
					 + str(fel0) + "\t" + str(fel1) + "\t" \
					 + str(intersect) + "\t"  + str(Jaccard) + "\n ")


def main():

	os.chdir(IN_DIR)
	read_save_taxonomy_graph()
	
main()
