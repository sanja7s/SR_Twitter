#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	go through user cleaned monthly tweets (MO_tweets.dat) and create user monthly CVs (MO_CV.json)
	need access to MongoDB for individual word CVs. Both, input and output are .json txt files.
"""
import sys, io, json, os
import pymongo
from pymongo import MongoClient
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict, OrderedDict
import math
import codecs
import logging
import traceback
import multiprocessing
import functools
from itertools import repeat
import numpy as np

# used for our Wiki SR database querying. We saved CVs for stemmed words for better accuracy.
STEMMER = SnowballStemmer("english", ignore_stopwords=True )

# where we work
IN_DIR = "../../../DATA/General/"

# Mongo collections
CV = ""
AID7s = ""

# this global dictionary will change for each month MO
USR_TWEETS = defaultdict(int)

# .json input and output
F_IN_NAME = "_tweets.dat"
F_OUT_CV_NAME = "_CV.json"

# I put this here in order to cache the word CVs
# so to reduce the number of queries to MongoDB
words_CVs_lst = defaultdict(int)
#############################################################################################
# take the right collection = TF-IDF based concept vectors (CV) based on Wiki
#############################################################################################
def set_global_conn_params(client = MongoClient(), dbs="test", CV_collection="CV_stemmed_pruned",
	aid_collection="AID"):
	global CV, AID7s
	# connect to Mongo db test
	db = client[dbs]
	CV = db[CV_collection]
	AID7s = db[aid_collection]

#############################################################################################
# read in monthly user tweets from the right file (one per each month, 
# created by ""monthly_user_tweets_clean_2_json.py)
#############################################################################################
def read_in_monthly_user_tweets(MO):

	f = codecs.open(str(MO) + F_IN_NAME, "r")

	for line in f:
		line7s = json.loads(line)
		user = line7s["_id"]
		tweets_text = line7s["txt"]
		count = line7s["count"]
		USR_TWEETS[user] = defaultdict(int)
		USR_TWEETS[user]["text"] = tweets_text
		USR_TWEETS[user]["count"] = count

	f.close()

def stem_word(token):
	return STEMMER.stem( token ) 

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
	#return OrderedDict(sorted(vec.items(), key=lambda x: x[1], reverse= False))
	return vec

# this function outputs a dictionary with {stemmed(word): fq} pairs
def stem_text_corpus(txt):
	stemmed_text =  defaultdict(int)
	for el in txt:
		for word, fq in el.iteritems():
			stemmed_word = stem_word(word)
			stemmed_text[stemmed_word] += int(fq)
	return stemmed_text

# for given user, if a word in his text is in the global cached words_CVs_lst, take it,
# otherwise extract from MongoDB and add to the global cache; and then calculate his CV
def calculate_user_CV(userA):
	# from read in users cleaned tweets with frequencies
	A = USR_TWEETS[userA]  
	#print A  
	txtA = A['text']
	num_tweets = A['count']
	txt_fq_dist = stem_text_corpus(txtA)
	CV_txt = defaultdict(int)
	for word, fq in txt_fq_dist.iteritems():
		# simple code
		if words_CVs_lst[word]:
			cv_word = words_CVs_lst[word]
		else:
			# expensive step going to Mongo
			cv_word = extract_word_CV(word)
			words_CVs_lst[word] = cv_word

		if cv_word:
			for concept, tf_idf in cv_word.iteritems():
				CV_txt[concept] += tf_idf * fq
	if not CV_txt or not CV_txt.values():
		print userA
	return OrderedDict(sorted(CV_txt.items(), key=lambda x: x[1], reverse= True)), num_tweets #normalize -- will do in the pruning step 

# we prune CVs according to the original algorithms and save them to the given f output file
def prune_CV_and_dump(userA, num_tweets, CV_userA, f, threshold = 0.005, window = 100):
	N = len(CV_userA.items())
	CNT = 0
	chck_pruning = 0
	
	CV_dict = {}
	CV_dict['_id'] = userA
	CV_dict['num_tweets'] = num_tweets
	CV_dict['CV'] = []
	vec = CV_userA.values()
	# HOWTO take the first element from OrderedDict already
	if not vec:
		return
	highest_scoring_concept = max(vec)
	highest_scoring_concept_pct = highest_scoring_concept * threshold
	remembered_tfidf = highest_scoring_concept
	remembered_id = 0
	k = 0
	for (concept, tfidf) in CV_userA.iteritems():
		CNT += 1
		k += 1
		tfidf_dict = {}
		tfidf_dict[concept] = str(tfidf)
		CV_dict['CV'].append(tfidf_dict)
		if k >= window:
			if remembered_tfidf - tfidf < highest_scoring_concept_pct:
				chck_pruning += (len(CV_userA.items()) - k)
				break
			else:
				remembered_id += 1
				remembered_tfidf = np.sort(vec)[::-1][remembered_id]


	CV_new = OrderedDict(sorted(CV_dict.items(), key=lambda x: x[1], reverse= False))
	f.write(unicode(json.dumps(CV_new, ensure_ascii=False)) + '\n')


if __name__ == "__main__":

	set_global_conn_params()
	os.chdir(IN_DIR)
	ss = 0

	# go for all the 7 months we have the data for
	# May until Nov
	for MO in [9]:

		read_in_monthly_user_tweets(MO)
		print "read in ", str(MO)

		with codecs.open(str(MO) + F_OUT_CV_NAME, 'w', encoding='utf-8') as f:

			for userA in USR_TWEETS:
				#print userA
				ss += 1
				if ss % 1000 == 0:
					print ss, userA
				CV_userA, num_tweets = calculate_user_CV(userA)
				#print CV_userA, num_tweets
				prune_CV_and_dump(userA, num_tweets, CV_userA, f, threshold = 0.005, window = 100)

		f.close()