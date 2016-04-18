#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	go through user tweets, collect them per user, clean and save in a josn format per each month. we end up with 7 months
	since May and Nov are half included. The output is 7 files json formatted and ready to be inputted to MongoDB
"""
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.book import FreqDist
from collections import defaultdict
import codecs
import matplotlib.pyplot as plt
import pylab as P
import numpy as np
import glob, os
import datetime
import json

IN_DIR = "../../../DATA/General/"
os.chdir(IN_DIR)

F_IN = "usrs_with_more_than_20_tweets.dat"

F_OUT_5 = codecs.open("5_tweets.dat", "w")
F_OUT_6 = codecs.open("6_tweets.dat", "w")
F_OUT_7 = codecs.open("7_tweets.dat", "w")
F_OUT_8 = codecs.open("8_tweets.dat", "w")
F_OUT_9 = codecs.open("9_tweets.dat", "w")
F_OUT_10 = codecs.open("10_tweets.dat", "w")
F_OUT_11 = codecs.open("11_tweets.dat", "w")
F_OUT_12 = codecs.open("12_tweets.dat", "w")

f_out_list = {5:F_OUT_5, 6:F_OUT_6, 7:F_OUT_7, 8:F_OUT_8, 9:F_OUT_9, \
				10:F_OUT_10, 11:F_OUT_11}

ENGLISH_STOPWORDS = set(stopwords.words('english'))
def clean(tweet):
	return [i.lower() for i in tweet if i.isalpha() and i not in ENGLISH_STOPWORDS and i != 'RT']

def extract_monthly_user_CV_and_num_tweets():

	user_monthly_tweets = defaultdict(int)
	user_monthly_count = defaultdict(int)
	cnt_all_tweets = 0

	with codecs.open(F_IN,'r', encoding='utf8') as input_file:
		# the code loops through the input, collects tweets text for each user into a dict
		for line in input_file:	
			cnt_all_tweets += 1
			line = line.split()
			user = line[0]
			if user not in user_monthly_tweets:
				user_monthly_tweets[user] = defaultdict(list)
				user_monthly_count[user] = defaultdict(int)
			UTS = long(line[4])
			month = datetime.datetime.utcfromtimestamp(UTS).month
			tweet = line[5:]
			user_monthly_tweets[user][month] += clean(tweet)
			user_monthly_count[user][month] += 1
			if cnt_all_tweets % 100000 == 0:
				print tweet, clean(tweet)
	print "Processed %d tweets" % cnt_all_tweets

	for user in user_monthly_tweets:
		for MO in user_monthly_tweets[user]:
			output_file = f_out_list[MO]
			usr_tweets_json = {}
			usr_tweets_json['_id'] = str(user)
			usr_tweets_json['count'] = str(user_monthly_count[user][MO])
			usr_tweets_json['txt'] = [ {el[0]: el[1]} for el in FreqDist(user_monthly_tweets[user][MO]).iteritems() ]
			output_file.write(unicode(json.dumps(usr_tweets_json, ensure_ascii=False)) + '\n')

extract_monthly_user_CV_and_num_tweets()
	









