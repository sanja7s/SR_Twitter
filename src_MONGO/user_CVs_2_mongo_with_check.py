#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, io, json, os
import pymongo
from pymongo import MongoClient
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict, OrderedDict
import math
import codecs
from multiprocessing import Pool
import logging
import traceback
import multiprocessing
import functools
from itertools import repeat
#from stemming.porter2 import stem
import numpy as np

STEMMER = SnowballStemmer("english", ignore_stopwords=True )

CV = ""
AID7s = ""
USR_TWEETS = ""

f_in = "usrs_with_more_than_20_tweets_COPY_check.dat"
F_OUT_CV = "CV_usrs_with_more_than_20_tweets_COPY_check.json"

# I put this here in order to cache the word CVs
# so to reduce the number of queries to MongoDB
words_CVs_lst = defaultdict(int)
#############################################################################################
# take the right collection = TF-IDF based concept vectors (CV) based on Wiki
# and also the usr_clean_tweets collection
#############################################################################################
def set_global_conn_params(client = MongoClient(), dbs="test", CV_collection="CV_stemmed_pruned",
	aid_collection="AID", usr_tweets_collection = "usr_clean_tweets"):
	global CV, AID7s, USR_TWEETS
	# connect to Mongo db test
	db = client[dbs]
	CV = db[CV_collection]
	AID7s = db[aid_collection]
	USR_TWEETS = db[usr_tweets_collection]
#############################################################################################
# 
#############################################################################################

# read in all the data to only count #tweets per user
def count_tweets_per_user():
	cnt_all_tweets = 0
	user_tweets = defaultdict(int)
	with codecs.open(f_in,'r', encoding='utf8') as input_file: # the code loops through the input, counts tweets for each user
	    for line in input_file:	
	    	cnt_all_tweets += 1
	    	line = line.split()
	    	user = line[0]
	    	user_tweets[user] += 1
	    	if cnt_all_tweets % 100000 == 0:
	    		print user
	print "Read ENG tweets: ", cnt_all_tweets, " from: ", len(user_tweets.keys()), " distinct users."
	return user_tweets


def stem_word(token):
	#token = token.lower()
	return STEMMER.stem( token ) 
	# return stem( token )

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
	# extract users cleaned tweets with frequencies
	A = USR_TWEETS.find_one({"_id": userA})
	txtA = A['txt']
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
	return OrderedDict(sorted(CV_txt.items(), key=lambda x: x[1], reverse= True)) #normalize -- will do in the pruning step 


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
		#if CNT % 100 == 0:
			#print CNT, highest_scoring_concept, concept, tfidf
		tfidf_dict = {}
		tfidf_dict[concept] = str(tfidf)
		CV_dict['CV'].append(tfidf_dict)
		if k >= window:
			if remembered_tfidf - tfidf < highest_scoring_concept_pct:
				#if the_word == TEST_WORD:
				#	print "PRUNED ", value, remembered_tfidf, highest_scoring_concept_pct, remembered_tfidf - value
				chck_pruning += (len(CV_userA.items()) - k)
				break
			else:
				remembered_id += 1
				remembered_tfidf = np.sort(vec)[::-1][remembered_id]

	#if the_word == TEST_WORD:
	#	print CV_dict
	#	print np.sort(col.data)[::-1]
	CV_new = OrderedDict(sorted(CV_dict.items(), key=lambda x: x[1], reverse= False))
	#print CV_new.values()
	f.write(unicode(json.dumps(CV_new, ensure_ascii=False)) + '\n')
	#print "For user ", userA, " pruned # concepts is: ", chck_pruning



def main():
	set_global_conn_params()
	#print 'cpu_count() = %d\n' % multiprocessing.cpu_count()

	# a dict of users with their number of tweets found
	users = count_tweets_per_user()
	ss = 0
	with io.open(F_OUT_CV, 'w', encoding='utf-8') as f:

		for userA in users.keys():
			ss +=1
			if ss % 1000 == 0:
				print ss, userA
			CV_userA = calculate_user_CV(userA)
			num_tweets = users[userA]
			prune_CV_and_dump(userA, num_tweets, CV_userA, f, threshold = 0.005, window = 100)



import cProfile
command = """main()"""
cProfile.runctx( command, globals(), locals(), filename="OpenGLContext_user_CVs_2_mongo.profile" )