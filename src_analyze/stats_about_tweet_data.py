#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import defaultdict
import codecs
import matplotlib.pyplot as plt
import pylab as P
import numpy as np
import glob, os

IN_DIR = "../../../DATA/General/"
F_IN = "usrs_with_more_than_20_tweets.dat"
#F_OUT = "tweets_with_usrs_with_more_than_20_tweets.dat"
#f_out = "usrs_with_more_than_20_tweets.dat"
F_USR_TWEETS = "usr_num_tweets.tab"
f_in_user_ids = "user_IDs.dat"

USR_TWEETS = defaultdict(int)

def plot_hist(data):

	n, bins, patches = P.hist(data,  bins=np.logspace(0.1, 3.5), histtype='step', log=True, label="# of tweets per user")
	P.setp(patches, 'facecolor', 'g', 'alpha', 0.75)


	#y = P.normpdf( bins, mu, sigma)
	#l = P.plot(bins, y, 'k--', linewidth=1.5)
	#
	# create a histogram by providing the bin edges (unequally spaced)
	#
	#P.figure()
	#
	# now we create a cumulative histogram of the data
	#
	#P.grid(True)
	#P.ylim(0, 1.05)
	#P.legend()
	P.gca().set_xscale("log")
	P.show()

def filter_users(thrshld=20):
	filtered_lst = []
	for usr, tweets in USR_TWEETS.iteritems():
		if USR_TWEETS[usr] > thrshld:
				filtered_lst.append(usr)
	return filtered_lst
'''
# DONE once is enough
def filter_dataset(thrshld=20):
	user_tweets = tweets_per_user(F_IN)
	filtered_lst = filter_users(user_tweets)
	cnt_selected_tweets = 0
	output_file = codecs.open(F_OUT, 'w', encoding='utf8')
	with codecs.open(F_IN,'r', encoding='utf8') as input_file:
		for line in input_file:	
			line_splt = line.split()
			usr = line_splt[0]
			if usr in filtered_lst:
				cnt_selected_tweets += 1
				output_file.write(line)
	output_file.close()
	input_file.close()
	print "Filtered dataset for users with more than: ", thrshld, " tweets."
	print "New number of tweets: ", cnt_selected_tweets
	print "New number of users: ", len(filtered_lst)
'''

#
# put to the global vairable USR_TWEETS number of tweets per username
#
def tweets_per_user():
	cnt_all_tweets = 0
	global USR_TWEETS
	with codecs.open(F_IN,'r', encoding='utf8') as input_file:
		# the code loops through the input, collects tweets for each user into a dict
	    for line in input_file:	
	    	cnt_all_tweets += 1
	    	line = line.split()
	    	user = line[0]
	    	USR_TWEETS[user] += 1

	print "Read ENG tweets: ", cnt_all_tweets, " from: ", len(USR_TWEETS.keys()), " distinct users."
	max_tweets = max(USR_TWEETS.values())
	print "MAX tweets ", max_tweets, " has/ve the user/s ", \
	[usr for usr, tweets in USR_TWEETS.iteritems() if USR_TWEETS[usr] == max_tweets]
	input_file.close()

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
#
# user outputs of tweets_per_user() and read_user_IDs()
# to create number of tweets per user ID
#
def tweets_per_user_id():

	tweets_per_id = defaultdict(int)

	tweets_per_user()
	usr_tweets = USR_TWEETS
	usr_ids = read_user_IDs()
	for usr in usr_tweets:
		if usr in usr_ids:
			tweets_per_id[usr_ids[usr]] = usr_tweets[usr]

	return tweets_per_id


def plot_hist_usr_tweets():
	usr_tweets = tweets_per_user()
	plot_hist(usr_tweets.values())

def filter_dataset_double_usr_filter(thrshld=20):
	
	filtered_lst = filter_users(USR_TWEETS)
	cnt_selected_tweets = 0
	output_file = codecs.open(F_OUT, 'w', encoding='utf8')
	with codecs.open(F_IN,'r', encoding='utf8') as input_file:
		for line in input_file:	
			line_splt = line.split()
			usr = line_splt[0]
			usr2 = line_splt[1]
			if usr and usr2 in filtered_lst:
				cnt_selected_tweets += 1
				output_file.write(line)
	output_file.close()
	input_file.close()
	print "Filtered dataset for users with more than: ", thrshld, " tweets."
	print "New number of tweets: ", cnt_selected_tweets
	print "New number of users: ", len(filtered_lst)

def save_usr_num_tweets(thrshld=20):
	
	usr_tweets = tweets_per_user_id()
	f = codecs.open(F_USR_TWEETS, 'w', encoding='utf8')
	for el in usr_tweets:
		f.write(str(el) + "\t" +  str(usr_tweets[el]) + "\n")


#plot_hist_usr_tweets()
#filter_dataset()

#tweets_per_user()
#print len(filter_users())
#filter_dataset_double_usr_filter()

os.chdir(IN_DIR)
save_usr_num_tweets()