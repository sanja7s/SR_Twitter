#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pymongo
from pymongo import MongoClient
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict, OrderedDict
import math
import codecs
import os

# where we work
IN_DIR = "../../../DATA/General/"

STEMMER = SnowballStemmer("english", ignore_stopwords=True )

CV = ""
AID7s = ""
MO5 = ""
MO6 = ""
MO7 = ""
MO8 = ""
MO9 = ""
MO10 = ""
MO11 = ""

MONTHS =  {}

f_in_user_ids = "user_IDs.dat"
def read_user_names():

	user_names = defaultdict(int)

	with codecs.open(f_in_user_ids,'r', encoding='utf8') as f:
		for line in f:
			line = line.split()
			user_id = line[0]
			user =  line[1]
			user_names[user_id] = user

	return user_names


#############################################################################################
# take the right collection = TF-IDF based concept vectors (CV) based on Wiki
# and also the usr_clean_tweets collection
#############################################################################################
def set_global_conn_params(client = MongoClient(), dbs="test", CV_collection="CV_stemmed_pruned",
	aid_collection="AID", 
	MO5_collection = "MO5_CVs", MO6_collection = "MO6_CVs", MO7_collection = "MO7_CVs",
	MO8_collection = "MO8_CVs", MO9_collection = "MO9_CVs", MO10_collection = "MO10_CVs",
	MO11_collection = "MO11_CVs" ):
	global CV, AID7s, MO5, MO56, MO7, MO8, MO9, MO10, MO11, MONTHS
	# connect to Mongo db test
	db = client[dbs]
	CV = db[CV_collection]
	AID7s = db[aid_collection]
	MO5 = db[MO5_collection]
	MO6 = db[MO6_collection]
	MO7 = db[MO7_collection]
	MO8 = db[MO8_collection]
	MO9 = db[MO9_collection]
	MO10 = db[MO10_collection]
	MO11 = db[MO11_collection]

	MONTHS =  {5: MO5, 6: MO6, 7: MO7, 8: MO8, 9: MO9, 10: MO10, 11: MO11}
#############################################################################################
# 
#############################################################################################

def stem_word(token):
	token = token.lower()
	return STEMMER.stem( token ) 

# function takes any two words, looks up their CVs in the collection
# exctracts the CVs and invokes standard vector cosine similarity
def SR_2_words(w1, w2):
	v1 = extract_word_CV(w1)
	v2 = extract_word_CV(w2)
	if not v1 or not v2:
		return -1
	return cosine_2_vectors(v1, v2)

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
		v1_fq = v1[term]
		v2_fq = v2[term]
		SR_num += v1_fq * v2_fq
		v1_sq_sum += v1_fq * v1_fq
		v2_sq_sum += v2_fq * v2_fq
	# for different keys, we just take resepective non-zero 
	# dict terms for calculating denominator (nominator is zero)
	for term in different1_keys:
		v1_fq = v1[term]
		v1_sq_sum += v1_fq * v1_fq
	for term in different2_keys:
		v2_fq = v2[term]
		v2_sq_sum += v2_fq * v2_fq
	# sum all in denominator and sqrt in the end
	SR_den = math.sqrt(v1_sq_sum*v2_sq_sum)
	try:
		SR = SR_num/SR_den
	except ZeroDivisionError:
		SR = 0
	return SR

# extract the CV vector in the form for calculation with true ids for articles
def extract_word_CV(w):
	vec = defaultdict(int)
	w = stem_word(w)
	cv = CV.find_one({"_id": w})
	if cv == None:
		return None
	v = cv['CV']
	if v == None:
		return None
	for el in v: # can code better this part ?
		for key, value in el.iteritems():
			vec[value[1]] = float(value[0])
	return OrderedDict(sorted(vec.items(), key=lambda x: x[1], reverse= False))

# NB this function takes important elements away from the CV array
def print_topN_word_concepts(w, topN):
	w1 = stem_word(w)
	v = extract_word_CV(w1)
	if not v:
		print  w, " stemmed is ", w1, " and not found ccc!"
		return
	print w, " stemmed is ", w1, " and has ", len(v.items()), " concepts CV."
	print "Top concepts are: "
	for i in range (topN):
		print_topN_concept(v, topN)

# NB this function takes important elements away from the CV array
def print_top_concept(v):
		term = v.popitem()
		article_name = AID7s.find_one({"_id": long(str(term[0]))})
		print term[1], article_name

# NB this function takes important elements away from the CV array
def print_topN_common_user_concepts(usrA, usrB, topN=100):
	A = USR_TWEETS.find_one({"_id": usrA})
	if not A:
		print "No data found for user: ", usrA
		return
	txtA = A['txt']
	B = USR_TWEETS.find_one({"_id": usrB})
	if not B:
		print "No data found for user: ", usrB
		return
	txtB = B['txt']

	stemmed_txtA = stem_text_corpus(txtA)
	stemmed_txtB = stem_text_corpus(txtB)

	CV_txtA = extract_text_CV(stemmed_txtA)
	CV_txtB = extract_text_CV(stemmed_txtB)
	if not CV_txtA or not CV_txtB:
		print "No data for user text found ccc! Error?"
		return

	keys_A = set(CV_txtA.keys())
	print len(keys_A)
	keys_B = set(CV_txtB.keys())
	print len(keys_B)
	common_keys = keys_A & keys_B
	print len(common_keys), common_keys

	print "Top common concepts for: ", usrA, usrB, " are: "
	i = 0
	for concept in common_keys:
		termA = CV_txtA[concept]
		#print termA
		article_nameA = AID7s.find_one({"_id": long(str(concept))})
		termB = CV_txtB[concept]
		article_nameB = AID7s.find_one({"_id": long(str(concept))})
		assert article_nameA == article_nameB
		print termA, termB, article_nameA
		i+=1
		if i == topN:
			break
		
# NB this function takes important elements away from the CV array
def print_topN_user_concepts(usr, topN):
	txt = USR_TWEETS.find_one({"_id": usr})['txt']
	stemmed_txt = stem_text_corpus(txt)
	print "User text CV info for: ", usr
	print_topN_text_concepts(stemmed_txt, topN)

# NB this function takes important elements away from the CV array
def print_topN_text_concepts(txt, topN):
	v = extract_text_CV(txt)
	if not v:
		print "Not found ccc!"
		return
	print " Given text has ", len(v.items()), " concepts CV."
	print "Top concepts are: "
	for i in range (topN):
		print_top_concept(v)

def MO_extract_user_CV(user, MO):	
	vec = defaultdict(int)
	MO7s = MONTHS[MO]
	#print MO7s, user
	cv = MO7s.find_one({"_id": user})
	if cv == None:
		return None, 0
	v = cv['CV']
	#print v
	num_tweets = cv['num_tweets']
	if v == None:
		return None, num_tweets
	for el in v: # can code better this part ?
		#print el
		for key, value in el.iteritems():
			vec[key] = float(value)
	return OrderedDict(sorted(vec.items(), key=lambda x: x[1], reverse= False)), num_tweets

def MO_SR_2_users(usrA, usrB, MO):
	CVA, num_tweetsA = MO_extract_user_CV(usrA, MO)
	CVB, num_tweetsB = MO_extract_user_CV(usrB, MO)
	if num_tweetsA <> 0 and num_tweetsB <> 0:
		#print CVA
		#print CVB
		return cosine_2_vectors(CVA, CVB), num_tweetsA, num_tweetsB
	return 0, num_tweetsA, num_tweetsB

def read_in_mention_edge_list_undir():
	mention_edge_list_undir = defaultdict(int)
	mention_edges = "mention_graph_weights.dat"
	f = open(mention_edges, 'r')
	for line in f:
		(userA_id, userB_id, weight) = line.split()
		if (userA_id, userB_id) not in mention_edge_list_undir and (userB_id, userA_id) not in mention_edge_list_undir:
			mention_edge_list_undir[(userA_id, userB_id)] = 1
	print "Read %d undirected edges from mention graph " % len(mention_edge_list_undir)
	return mention_edge_list_undir


def save_monthly_SR_list_of_users():

	mention_edge_list_undir = read_in_mention_edge_list_undir()
	user_names = read_user_names()

	for MO in MONTHS.keys():
		f = open("monthly_SR_change_list_of_users/" + str(MO) + "mention_edges_monthly_SR", "w")
		print MO
		for (usrA_id, usrB_id) in mention_edge_list_undir:
			usrA = user_names[usrA_id]
			usrB = user_names[usrB_id]
			# because I saved the SR with user names, not IDs
			SR, num_tweetsA, num_tweetsB = MO_SR_2_users(usrA, usrB, MO)
			f.write(str(usrA_id) + '\t' + str(usrB_id) + '\t' + \
					str(SR) + '\t' + str(num_tweetsA) + '\t' + str(num_tweetsB) + '\n')
		f.close()


set_global_conn_params()

os.chdir(IN_DIR)

save_monthly_SR_list_of_users()

