#!/usr/bin/env python

"""
	go through the all dataset and collect tweets per month and then per user
	in a dictionary. then save them in five files for each month, all the tweets
	of one user in one line claned a bit)
"""

import codecs
import re
from collections import defaultdict
import os
import datetime

IN_DIR = "../../../DATA/taxonomy_raw/MO"
f_in = "usrs_with_more_than_20_tweets"

f_out = "tweets_per_usr_"

def clean(tweet):
	pattern = re.compile("(@)\S*", re.I)
	return pattern.sub("", tweet.replace('\n',' ').replace('\r', '').replace('RT', ' '))

def collect_tweet_text_per_user_per_MO(f_in):
	cnt_all_tweets = 0
	user_tweets = {'5':defaultdict(str), '6':defaultdict(str), \
		'7':defaultdict(str), '8':defaultdict(str), '9':defaultdict(str), \
		'10':defaultdict(str), '11':defaultdict(str)}
	with codecs.open(f_in,'r', encoding='utf8') as input_file:
		# the code loops through the input, collects tweets for each user into a dict
		for line7s in input_file: 
			cnt_all_tweets += 1
			line = line7s.split(' ',5)
			user = line[0]
			tweet = line[len(line)-1]
			UTS = long(line[4])
			month = datetime.datetime.utcfromtimestamp(UTS).month
			user_tweets[str(month)][user] += clean(tweet)
			if cnt_all_tweets % 10000 == 0:
				print('Processing lines: ', cnt_all_tweets, ' and tweet text:', tweet)
	print("Read ENG tweets: ", cnt_all_tweets, " from: ", len(user_tweets.keys()), " distinct users.")
	return user_tweets

def save_tweets_per_user_per_MO(f_out):

	os.chdir(IN_DIR)

	user_tweets = collect_tweet_text_per_user_per_MO(f_in)

	for MO in ['5', '6', '7', '8', '9', '10', '11']:
		user_tweets_MO = user_tweets[MO]
		f = codecs.open(f_out + MO,'w', encoding='utf8')
		for user in user_tweets_MO.iterkeys():
			f.write(str(user) + '\t' + str(user_tweets_MO[user]) + '\n')
		f.close()

save_tweets_per_user_per_MO(f_out)