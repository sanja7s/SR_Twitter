#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
import codecs
from collections import defaultdict
from nltk.book import FreqDist
import json

f_in = "en_mentions_reciprocal_six_months1K.dat"
f_out = "en_usr_tweets1K.json"


ENGLISH_STOPWORDS = set(stopwords.words('english'))
def clean(tweet):
	return [i.lower() for i in tweet if i.isalpha() and i not in ENGLISH_STOPWORDS and i != 'RT']

def read_in_graph_with_SR(f_in):
	graph_with_SR = defaultdict(list)
	with codecs.open(f_in,'r', encoding='utf8') as input_file:
	    for line in input_file:	
	    	line = line.split()
	    	usr1 = line[0]
	    	usr2 = line[1]
	    	weight = int(line[2])
	    	SR = line[3]
	    	if SR == 'None' or SR == '-1':
	    		continue
	    	SR = float(SR)
	    	graph_with_SR[(usr1, usr2)] = (weight, SR)
	return graph_with_SR

def collect_tweet_text_per_user(f_in):

	cnt_all_tweets = 0
	user_tweets = defaultdict(list)

	with codecs.open(f_in,'r', encoding='utf8') as input_file:
		# the code loops through the input, collects tweets for each user into a dict
	    for line in input_file:	
	    	cnt_all_tweets += 1
	    	line = line.split()
	    	user = line[0]
	    	tweet = line[5:]
	    	#print line
	    	#print tweet
	    	#print clean(tweet)
	    	#print
	    	user_tweets[user] += clean(tweet)
	    	if cnt_all_tweets % 100000 == 0:
	    		print tweet, clean(tweet)

	print "Read ENG tweets: ", cnt_all_tweets, " from: ", len(user_tweets.keys()), " distinct users."
	#print [len(user_tweets[user]) for user in user_tweets.keys()]
	return user_tweets


def user_tweet_text_2_mongo(f_in, f_out):

	user_tweets = collect_tweet_text_per_user(f_in)
	output_file = codecs.open(f_out, 'w', encoding='utf8')
	for usr in user_tweets.iterkeys():
		usr_tweets_json = {}
		usr_tweets_json['_id'] = str(usr)
		usr_tweets_json['txt'] = [ {el[0]: el[1]} for el in FreqDist(user_tweets[usr]).iteritems() ]
		output_file.write(unicode(json.dumps(usr_tweets_json, ensure_ascii=False)) + '\n')
		#print usr_tweets_json

	print "User with most words had: ", len(max(user_tweets.values(), key=len))

user_tweet_text_2_mongo(f_in, f_out)
