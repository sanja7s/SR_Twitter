#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
	Let's extract popular taxonomies in different communities, but using TF-IDF-like calculation.
	Take all the communities above threshold (300) users and treat them as documents. In each,
	calculate the term frequency scores for the taxonomies that are found with confidence. 
	Also calculate the taxonomy scores for the whole dataset. Now the scores represent term frequency.
	So IDF for a taxonomy will be log(N/num_communities_where_found)
"""
# for reading json files with possible unicode chars
import codecs
from collections import defaultdict
import json
#import re
import glob, os
import math
#import itertools

# here we have the results from Alchemy API per user
f_in = "tweets_taxonomy_clean.JSON"
# the id map we defined for the Twitter usernames
f_in_user_ids = "user_IDs.dat"
IN_DIR = "../DATA/taxonomy_stats"
# the communities we analyze (from the mention graph)
spec_users = "mention/communitiesMent.txt"

#
# all the user ids (id map)
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

# to return top sizeN communities, as many as there are
# in a form of a dictionary: {community_id: defaultdict{id_usr1:1, id_usr2:1, ...}}
# and also another dict, as a map (res3) to tell us the community id of a user
# and finally the whole set of communities (not limited in size) and similar map in res4
def read_in_communities(sizeN=300):

	res = defaultdict(int)
	res7s = defaultdict(int)
	res3 = defaultdict(int)
	res3 = defaultdict(lambda: -1, res3)
	res4 = defaultdict(int)
	res4 = defaultdict(lambda: -1, res4)

	f = open(spec_users, "r")

	for line in f:
		line = line.split()
		user_id = line[0]
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

#
# here we will extract IDF values, i.e., document counts for the taxonomies
# 
def find_full_tfIDF_taxonomy(user_com):

	taxonomies_sum= defaultdict(int) 
	user_ids = read_user_IDs()
	cnt = 0

	with codecs.open(f_in,'r', encoding='utf8') as input_file:
		for line7s in input_file:
			try:
				line = json.loads(line7s)
				user_name = line["_id"]
				user_id = user_ids[user_name]
				COM = user_com[user_id]
				taxonomy_all = line["taxonomy"]
				taxonomy = taxonomy_all["taxonomy"] 
			except KeyError:
				continue

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
					if tax_class not in s.keys():
						s[tax_class] = defaultdict(int)
						s[tax_class]["documents_found"] = []
					s = s[tax_class]

				if COM <> -1:
					s["documents_found"].append(COM)
	return taxonomies_sum

#
# here we will extract IDF values, i.e., document counts for the taxonomies
# 
def read_save_com_tfIDF_taxonomy(taxonomies_sum, N, users, user_list):

	#taxonomies_sum= defaultdict(int) 
	user_ids = read_user_IDs()
	cnt = 0

	with codecs.open(f_in,'r', encoding='utf8') as input_file:
		for line7s in input_file:
			try:
				line = json.loads(line7s)
				user_name = line["_id"]
				user_id = user_ids[user_name]
				if user_list[user_id] == 0:
					continue    
				taxonomy_all = line["taxonomy"]
				taxonomy = taxonomy_all["taxonomy"] 
			except KeyError:
				continue

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
					#if tax_class not in s.keys():
					#    s[tax_class] = defaultdict(int)
					s = s[tax_class]

				old_score = s["size"]
				new_score = old_score + float(el["score"])
				s["size"] = new_score

			cnt += 1
	 
		print cnt        
		print "Total taxonomies on different levels found ", len(taxonomies_sum)

		TOP_N = 100

		f_out_name = "tfIDF_v2/tfidf_taxon_COM_" + str(users) + ".json"

		print len(taxonomies_sum), type(taxonomies_sum)
		taxonomies_out7s = recursive_writeable_json_from_dict(N, taxonomies_sum, "thing")
		print type(taxonomies_out7s)

		with codecs.open(f_out_name,'w', encoding='utf8') as f: 
			f.write("{ \"name\": \"thing\", \n \"children\": \n ")
			f.write(unicode(json.dumps(taxonomies_out7s, ensure_ascii=False)) + '\n')
			f.write("\n }")



def recursive_writeable_json_from_dict(N, d, dname):

	# stop criteria: len(d) == 1 means this is a leaf 
	# (should not allow here to arrive, for example { "size": 1.381699 }  )
	# only, for example { "poetry": { "size": 1.381699 } }
	if len(d) == 1:
		s = {}
		size = d.items()[0][1]["size"]
		doc_fq = len(set(d.items()[0][1]["documents_found"])) 
		inv_doc_fq = 0 if doc_fq == 0 else N/float(doc_fq)
		IDF = math.log(1.0 + inv_doc_fq)
		#s["size"] = size
		s["name"] = d.items()[0][0]
		#s["tfdif_size"] = size * IDF
		ss["tfdif_size"] = size * IDF
		return s

	# recursive criteria satisfied: create a new dict
	# add me my children, since I have
	s = []
	for child_k in d.keys():
		if child_k == "size" or child_k == "documents_found":
			continue
		else:
			child_el = d[child_k]
			ss = {"name": child_k}

			try:
				size = child_el["size"]
				#ss["size"] = size
				doc_fq = len(set(child_el["documents_found"])) 
				inv_doc_fq = 0 if doc_fq == 0 else N/float(doc_fq)
				IDF = math.log(1.0 + inv_doc_fq)
				#ss["tfdif_size"] = size * IDF
				ss["size"] = size * IDF
			except KeyError:
				pass
			#if type(child_el) == "<type 'collections.defaultdict'>":
			#	if child_el.items()[0][0] == "size" and len(child_el) == 1:
			#		s.append(ss)
			#		continue
			ss["children"] = recursive_writeable_json_from_dict(N, child_el, child_k)
			s.append(ss)

	return s


###
### call the tfidf visualization
###
def main():

	os.chdir(IN_DIR)
	# number of nodes in a community
	sizeN = 300
	top_communities, com_id_map, all_communities, all_com_id_map = read_in_communities(sizeN)

	f_out_name = "taxonomy_summary_of_" + str(sizeN) + ".json"

	N = len(top_communities)
	print N, "top communities found"

	NALL = len(all_communities)
	print NALL, "all communities found"

	all_users = read_user_IDs()

	#################################################################
	# v1 one way is to consider only the top N communities for documents
	# full_taxonomy_tfidf = find_full_tfIDF_taxonomy(all_com_id_map)
	# for community in top_communities:
	# 	read_save_com_tfIDF_taxonomy(full_taxonomy_tfidf, N, str(community), top_communities[community])
	#################################################################

	#################################################################
	# v2 another way is to consider all NALL comuunities for documents
	full_taxonomy_tfidf = find_full_tfIDF_taxonomy(all_com_id_map)
	for community in top_communities:
		read_save_com_tfIDF_taxonomy(full_taxonomy_tfidf, NALL, str(community), top_communities[community])
	#################################################################
	

main()
