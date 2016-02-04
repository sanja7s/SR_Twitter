#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pymongo
from pymongo import MongoClient
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict, OrderedDict
import math
import codecs

STEMMER = SnowballStemmer("english", ignore_stopwords=True )

CV = ""
AID7s = ""
USR_TWEETS = ""

#f_in = "usrs_with_more_than_20_tweets_COPY.dat"
f_in = "usrs_with_more_than_20_tweets_100K_COPY.dat"
f_out = "all_usr_pairs_SR_FASTEST_100K.dat"


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


# this function outputs a dictionary with {word: fq} pairs
def stem_text_corpus(txt):
	stemmed_text =  defaultdict(int)
	for el in txt:
		for word, fq in el.iteritems():
			stemmed_word = stem_word(word)
			stemmed_text[stemmed_word] += int(fq)
	return stemmed_text

# txt_fq_dist is here given as a dict with {word: fq} elements
def extract_text_CV(txt_fq_dist):
	CV_txt = defaultdict(int)
	cv_word = defaultdict(int)
	for word, fq in txt_fq_dist.iteritems():
		cv_word = extract_word_CV(word)
		if not cv_word:
			continue
		for concept, tf_idf in cv_word.iteritems():
			#if fq > 4:
				#print concept, tf_idf, fq
			CV_txt[concept] += tf_idf * fq
	# print len(CV_txt.items())
	return OrderedDict(sorted(CV_txt.items(), key=lambda x: x[1], reverse= False)) #normalize ? 


def SR_2_texts(txt1, txt2):
	CV_txt1 = extract_text_CV(txt1)
	CV_txt2 = extract_text_CV(txt2)
	if not CV_txt1 or not CV_txt2:
		return -1
	return cosine_2_vectors(CV_txt1, CV_txt2)


def SR_2_users(usrA, usrB):
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
	#print usrA, stem_text_corpus(txtA)
	#print usrB, stem_text_corpus(txtB)
	return SR_2_texts(stem_text_corpus(txtA), stem_text_corpus(txtB))


def read_users():
	cnt_all_tweets = 0
	users = defaultdict(int)

	with codecs.open(f_in,'r', encoding='utf8') as input_file:
		# the code loops through the input, collects each user into a dict
	    for line in input_file:	
	    	cnt_all_tweets += 1
	    	line = line.split()
	    	user = line[0]
	    	users[user] = user
	    	if cnt_all_tweets % 10000 == 0:
	    		print user

	print "Read: ", cnt_all_tweets, " tweets from: ", len(users.keys()), " distinct users."
	return users


# for a faster processing for all user pairs, we do not want to query MongoDB for the text 
# more than once for one user; so here we colect all the texts in one big dictinary, since we
# have enough memory for it. users is a dictionary representing a list of users.
def extract_all_user_TXT(users):	
	user_TXT_lst = defaultdict(int)

	for userA in users.keys():
		A = USR_TWEETS.find_one({"_id": userA})
		txtA = A['txt']
		user_TXT_lst[userA] = stem_text_corpus(txtA)
	
	return user_TXT_lst


# TODO txt_fq_dist is here given as a dict with {word: fq} elements
# make this faster and more memory demanding by readin in all words also
# so that a concept for one word is never read in twice from MongoDB
def extract_all_user_CVs(user_TXT_lst):
	user_CVs_lst = defaultdict(int)
	words_CVs_lst = defaultdict(int)

	for userA in user_TXT_lst.iterkeys():
		txt_fq_dist = user_TXT_lst[userA]
		CV_txt = defaultdict(int)

		for word, fq in txt_fq_dist.iteritems():
			'''
			# fancy code
			cv_word = [words_CVs_lst[word] if words_CVs_lst[word] else extract_word_CV(word)]
			words_CVs_lst[word] = cv_word
			'''
			# simple code
			if words_CVs_lst[word]:
				cv_word = words_CVs_lst[word]
			else:
				cv_word = extract_word_CV(word)
				words_CVs_lst[word] = cv_word
			
			if not cv_word:
				continue
			for concept, tf_idf in cv_word.iteritems():
				CV_txt[concept] += tf_idf * fq

		user_CVs_lst[userA] = OrderedDict(sorted(CV_txt.items(), key=lambda x: x[1], reverse= False)) #normalize ? 

	return user_CVs_lst


# for all the users who are found to have more than threshold_tweets=20,
# find their SR and save in a file
def all_usr_SR():
	# for the results
	f = open(f_out, 'w')
	SR_dict = defaultdict(int)

	# a list of users with the threshold number of tweets found earlier
	users = read_users()
	# call a function to read in all the users' texts at once from MongoDB
	user_TXT_lst = extract_all_user_TXT(users)
	# call a function to extract CVs for all those user texts from the previous step
	user_CVs_lst = extract_all_user_CVs(user_TXT_lst)

	i = 0
	for userA in users.iterkeys():
		for userB in users.iterkeys():
			CVA = user_CVs_lst[userA]
			CVB = user_CVs_lst[userB]
			SR = cosine_2_vectors(CVA, CVB)

			#SR_dict[(userA,userB)] = SR
			f.write(str(userA) + '\t' + str(userB) + '\t' + str(SR) + '\n')
			i += 1
			if i%1000 == 0:
				print ":) we have ", i, " user pairs SR calculated"

	return #SR_dict


set_global_conn_params()
# print SR_2_users("chowow", "rjwilson")


#print SR_2_words("wolf", "fox")

#print_topN_word_concepts("mathematics", 736)

#print_topN_user_concepts("rjwilson", 850)

#print_topN_common_user_concepts("rjwilson", "chowow")

all_usr_SR()